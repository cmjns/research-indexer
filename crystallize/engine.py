"""
CrystallizationEngine — the individuation machine.

Each step extends the SimplexNetwork from the germ's traversal,
classifies propagation events as Deductive / Inductive / Transductive,
and records the full CrystallizationStep.

Phase 1 implementation: a structural / heuristic engine.
Full probabilistic and thermodynamic treatment is Phase 2.
"""
from __future__ import annotations

import uuid
from collections import Counter

from core.germ import Germ, RoleRotation
from core.network import SimplexNetwork
from core.field import PotentialField
from core.simplex import Simplex, Role
from core.term import Term
from core import thermodynamics as thermo
from crystallize.state import (
    CrystallizationStep,
    PropagationEvent,
    PropagationMode,
)
from crystallize.germ_detector import GermDetector


class CrystallizationEngine:
    """
    Runs the individuation process from a germ over a SimplexNetwork.

    temperature : controls aggressiveness of crystallization.
                  High T = diffuse, exploratory.
                  Low T  = concentrated, conservative.

    regime_threshold : Lyapunov estimate above which we flag regime_change.
    """

    def __init__(self,
                 temperature: float = 1.0,
                 regime_threshold: float = 0.5) -> None:
        self.temperature = temperature
        self.regime_threshold = regime_threshold
        self._detector = GermDetector()

    def run(self,
            network: SimplexNetwork,
            germ: Germ,
            max_steps: int = 50,
            halt_on_stable: bool = True) -> list[CrystallizationStep]:
        """
        Crystallize from germ for up to max_steps steps.
        If halt_on_stable, stop when entropy_delta ≈ 0 for 3 consecutive steps.
        """
        steps: list[CrystallizationStep] = []
        entropy_history: list[float] = []
        stable_count = 0

        # working copy
        current_network = self._copy_network(network)

        for i in range(max_steps):
            step = self._step(current_network, germ, i, entropy_history)
            steps.append(step)
            entropy_history.append(step.entropy)
            current_network = step.network

            if halt_on_stable and abs(step.entropy_delta) < 1e-6:
                stable_count += 1
                if stable_count >= 3:
                    break
            else:
                stable_count = 0

        return steps

    def _step(self,
              network: SimplexNetwork,
              germ: Germ,
              index: int,
              entropy_history: list[float]) -> CrystallizationStep:

        field_before = PotentialField.from_network(network)
        entropy_before = thermo.entropy(field_before) if entropy_history else 0.0

        events = self._propagate(network, germ, field_before)

        # apply new simplexes to network
        new_network = self._copy_network(network)
        for event in events:
            new_network.add(event.new_simplex)

        field_after = PotentialField.from_network(new_network)
        entropy_after = thermo.entropy(field_after)
        fe = thermo.free_energy(field_after, self.temperature)

        entropy_delta = entropy_after - (entropy_history[-1] if entropy_history else 0.0)

        # mode distribution
        mode_counts = Counter(e.mode.value for e in events)
        total_events = len(events) or 1
        mode_dist = {m: c / total_events for m, c in mode_counts.items()}

        # regime change
        lyapunov = thermo.lyapunov_estimate(entropy_history + [entropy_after])
        regime = abs(lyapunov) > self.regime_threshold

        # detect new aporiae
        new_rotations = self._detector._find_role_rotations(new_network, field_after)
        new_rotations = [
            r for r in new_rotations
            if r.cycle not in [x.cycle for x in germ.pattern.cycle]
            and r.is_genuine(0.01)
        ]

        return CrystallizationStep(
            index=index,
            network=new_network,
            field=field_after,
            propagation_events=events,
            mode_distribution=mode_dist,
            entropy=entropy_after,
            entropy_delta=entropy_delta,
            free_energy=fe,
            new_role_rotations=new_rotations,
            regime_change=regime,
        )

    def _propagate(self,
                   network: SimplexNetwork,
                   germ: Germ,
                   field: PotentialField) -> list[PropagationEvent]:
        """
        Generate new PropagationEvents from the germ and existing network.

        Phase 1 heuristics:
        - DEDUCTIVE : extend a simplex whose target has high potential
                      and an unsaturated modulator.
        - INDUCTIVE  : generalise a repeated A→B pattern across modulators.
        - TRANSDUCTIVE: propagate role structure across domain boundary
                        (currently: flip source/target of high-gain simplexes
                        to explore the other side of a polarity).
        """
        events: list[PropagationEvent] = []

        germ_simplexes = [
            network.simplexes[sid]
            for sid in germ.pattern.cycle
            if sid in network.simplexes
        ]

        for gs in germ_simplexes:
            # DEDUCTIVE: follow necessary entailment from germ simplex
            deductive = self._deductive_extension(gs, network, field)
            if deductive:
                events.append(deductive)

            # INDUCTIVE: generalise pattern if similar simplexes exist
            inductive = self._inductive_generalisation(gs, network, field)
            if inductive:
                events.append(inductive)

            # TRANSDUCTIVE: propagate role structure across polarity
            transductive = self._transductive_extension(gs, network, field)
            if transductive:
                events.append(transductive)

        return events

    def _deductive_extension(self,
                              source_simplex: Simplex,
                              network: SimplexNetwork,
                              field: PotentialField) -> PropagationEvent | None:
        """
        If source_simplex.target has adjacent simplexes where it is a SOURCE,
        actualise a new simplex extending the chain: A→B→D under same C.
        """
        target_term = source_simplex.target
        extensions = [
            s for s in network.simplexes_containing(target_term)
            if network.role_of(target_term, s.id) == Role.SOURCE
        ]
        if not extensions:
            return None

        ext = max(extensions, key=lambda s: field.phi(s.target))
        new_simplex = Simplex(
            id=str(uuid.uuid4()),
            source=source_simplex.source,
            target=ext.target,
            modulator=source_simplex.modulator,
            intensity=source_simplex.intensity * ext.intensity,
            asymmetry=(source_simplex.asymmetry + ext.asymmetry) / 2,
            gain=source_simplex.gain,
        )
        return PropagationEvent(
            mode=PropagationMode.DEDUCTIVE,
            source_simplex_ids=[source_simplex.id, ext.id],
            new_simplex=new_simplex,
            confidence=0.8,
            information_gain=0.0,
        )

    def _inductive_generalisation(self,
                                   source_simplex: Simplex,
                                   network: SimplexNetwork,
                                   field: PotentialField) -> PropagationEvent | None:
        """
        If the same A→B pair appears under multiple modulators,
        actualise a 'generalised' simplex with an averaged modulator.
        """
        same_pair = [
            s for s in network.simplexes.values()
            if s.source == source_simplex.source
            and s.target == source_simplex.target
            and s.id != source_simplex.id
        ]
        if not same_pair:
            return None

        # create a generalised simplex: average intensity, use the dominant modulator
        dominant_mod = max(same_pair, key=lambda s: s.gain).modulator
        avg_intensity = sum(s.intensity for s in same_pair) / len(same_pair)

        new_simplex = Simplex(
            id=str(uuid.uuid4()),
            source=source_simplex.source,
            target=source_simplex.target,
            modulator=dominant_mod,
            intensity=avg_intensity,
            asymmetry=source_simplex.asymmetry,
            gain=max(s.gain for s in same_pair),
        )
        return PropagationEvent(
            mode=PropagationMode.INDUCTIVE,
            source_simplex_ids=[source_simplex.id] + [s.id for s in same_pair],
            new_simplex=new_simplex,
            confidence=0.6,
            information_gain=0.0,
        )

    def _transductive_extension(self,
                                 source_simplex: Simplex,
                                 network: SimplexNetwork,
                                 field: PotentialField) -> PropagationEvent | None:
        """
        Propagate the role-structure of the simplex across a polarity:
        actualise the 'other side' — swap A and B, retain C, adjust gain.
        This explores what the aporia opens on the other side of the rotation.
        """
        # check the reverse isn't already in the network
        reverse_exists = any(
            s.source == source_simplex.target and s.target == source_simplex.source
            for s in network.simplexes.values()
        )
        if reverse_exists:
            return None

        new_simplex = Simplex(
            id=str(uuid.uuid4()),
            source=source_simplex.target,
            target=source_simplex.source,
            modulator=source_simplex.modulator,
            intensity=source_simplex.intensity * (1 - abs(source_simplex.asymmetry)),
            asymmetry=-source_simplex.asymmetry,  # reversed
            gain=source_simplex.gain * (1 + source_simplex.gain),  # amplified
        )
        return PropagationEvent(
            mode=PropagationMode.TRANSDUCTIVE,
            source_simplex_ids=[source_simplex.id],
            new_simplex=new_simplex,
            confidence=0.4,
            information_gain=0.0,   # filled in by analysis layer
        )

    @staticmethod
    def _copy_network(network: SimplexNetwork) -> SimplexNetwork:
        new = SimplexNetwork()
        for sid, s in network.simplexes.items():
            new.simplexes[sid] = s
        return new

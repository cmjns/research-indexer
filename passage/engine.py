"""
PassageEngine — the individuation machine.

Runs a passage through a corpus, driven by a germ.
Produces an Eddy: a local coherence that emerged from the flow.

The engine:
  1. Reads Domains from a CorpusProvider
  2. Extracts SimplexNetworks via a SimplexExtractor
  3. Merges networks into a single working field
  4. Injects the germ and runs passage steps
  5. Classifies each step as Deductive / Inductive / Transductive
  6. Tracks cycle_potentials → computes OperativeZero
  7. Returns an Eddy

The engine discovers its effective regime from the passage dynamics.
It is not pre-set to crystallise or oscillate — it finds out.
"""
from __future__ import annotations

import uuid
from collections import Counter
from typing import Optional

from core.germ import Germ
from core.network import SimplexNetwork
from core.field import PotentialField
from core.simplex import Simplex, Role
from core.propagation import PropagationMode, InterferenceCharacter
from core.operative_zero import OperativeZero
from core import thermodynamics as thermo

from corpus.base import CorpusProvider
from extract.base import SimplexExtractor

from passage.state import PassageStep, PropagationEvent
from passage.germ_detector import GermDetector
from passage.eddy import Eddy, VocabRotation, RemainderEntry


class PassageEngine:
    """
    temperature      : exploratory reach. High = diffuse. Low = concentrated.
    regime_threshold : Lyapunov estimate above which step is flagged as regime_change.
    """

    def __init__(
        self,
        extractor: SimplexExtractor,
        temperature: float = 1.0,
        regime_threshold: float = 0.5,
    ) -> None:
        self.extractor = extractor
        self.temperature = temperature
        self.regime_threshold = regime_threshold
        self._detector = GermDetector()

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def run(
        self,
        provider: CorpusProvider,
        germ: Germ,
        max_steps: int = 50,
        halt_on_stable: bool = True,
    ) -> Eddy:
        network, domains = self._ingest(provider)

        steps: list[PassageStep] = []
        entropy_history: list[float] = []
        cycle_potentials: list[float] = []
        stable_count = 0
        current = _copy(network)

        for i in range(max_steps):
            step, entry_phi = self._step(current, germ, i, entropy_history)
            steps.append(step)
            entropy_history.append(step.entropy)
            cycle_potentials.append(entry_phi)
            current = step.network

            if halt_on_stable and abs(step.entropy_delta) < 1e-6:
                stable_count += 1
                if stable_count >= 3:
                    break
            else:
                stable_count = 0

        return self._build_eddy(steps, cycle_potentials, germ, provider, domains)

    # ------------------------------------------------------------------
    # Ingestion
    # ------------------------------------------------------------------

    def _ingest(self, provider: CorpusProvider) -> tuple[SimplexNetwork, list]:
        merged = SimplexNetwork()
        domains = []
        for domain in provider.domains():
            net = self.extractor.extract(domain)
            for sid, s in net.simplexes.items():
                merged.simplexes[sid] = s
            domains.append(domain)
        return merged, domains

    # ------------------------------------------------------------------
    # Single step
    # ------------------------------------------------------------------

    def _step(
        self,
        network: SimplexNetwork,
        germ: Germ,
        index: int,
        entropy_history: list[float],
    ) -> tuple[PassageStep, float]:

        field = PotentialField.from_network(network)

        # Entry potential for OperativeZero tracking
        entry_phi = 0.0
        if germ.pattern.cycle and germ.pattern.cycle[0] in network.simplexes:
            s = network.simplexes[germ.pattern.cycle[0]]
            entry_phi = field.phi(s.source)

        events = self._propagate(network, germ, field)

        new_net = _copy(network)
        for ev in events:
            new_net.add(ev.new_simplex)

        new_field = PotentialField.from_network(new_net)
        s_after  = thermo.entropy(new_field)
        s_delta  = s_after - (entropy_history[-1] if entropy_history else 0.0)
        fe       = thermo.free_energy(new_field, self.temperature)

        mode_counts = Counter(ev.mode.value for ev in events)
        total = len(events) or 1
        mode_dist = {m: c / total for m, c in mode_counts.items()}

        lyapunov = thermo.lyapunov_estimate(entropy_history + [s_after])
        regime   = abs(lyapunov) > self.regime_threshold

        new_rotations = [
            r for r in self._detector._find_role_rotations(new_net, new_field)
            if r.is_genuine(0.01)
        ]

        return PassageStep(
            index=index,
            network=new_net,
            field=new_field,
            propagation_events=events,
            mode_distribution=mode_dist,
            entropy=s_after,
            entropy_delta=s_delta,
            free_energy=fe,
            new_role_rotations=new_rotations,
            regime_change=regime,
        ), entry_phi

    # ------------------------------------------------------------------
    # Propagation — three modes, never pure
    # ------------------------------------------------------------------

    def _propagate(
        self,
        network: SimplexNetwork,
        germ: Germ,
        field: PotentialField,
    ) -> list[PropagationEvent]:
        events: list[PropagationEvent] = []
        germ_simplexes = [
            network.simplexes[sid]
            for sid in germ.pattern.cycle
            if sid in network.simplexes
        ]
        for gs in germ_simplexes:
            for fn in (self._deductive, self._inductive, self._transductive):
                if ev := fn(gs, network, field):
                    events.append(ev)
        return events

    def _deductive(
        self, gs: Simplex, network: SimplexNetwork, field: PotentialField
    ) -> Optional[PropagationEvent]:
        """A→B, B→D (same C) → A→D.  Necessary entailment."""
        candidates = [
            s for s in network.simplexes_containing(gs.target)
            if network.role_of(gs.target, s.id) == Role.SOURCE
        ]
        if not candidates:
            return None
        ext = max(candidates, key=lambda s: field.phi(s.target))
        new = Simplex(
            id=str(uuid.uuid4()),
            source=gs.source, target=ext.target, modulator=gs.modulator,
            intensity=gs.intensity * ext.intensity,
            asymmetry=(gs.asymmetry + ext.asymmetry) / 2,
            gain=gs.gain,
        )
        return PropagationEvent(
            mode=PropagationMode.DEDUCTIVE,
            source_simplex_ids=[gs.id, ext.id],
            new_simplex=new, confidence=0.8,
        )

    def _inductive(
        self, gs: Simplex, network: SimplexNetwork, field: PotentialField
    ) -> Optional[PropagationEvent]:
        """Same A→B under multiple C → generalised simplex with dominant C."""
        same_pair = [
            s for s in network.simplexes.values()
            if s.source == gs.source and s.target == gs.target and s.id != gs.id
        ]
        if not same_pair:
            return None
        dominant_mod = max(same_pair, key=lambda s: s.gain).modulator
        avg_intensity = sum(s.intensity for s in same_pair) / len(same_pair)
        new = Simplex(
            id=str(uuid.uuid4()),
            source=gs.source, target=gs.target, modulator=dominant_mod,
            intensity=avg_intensity, asymmetry=gs.asymmetry,
            gain=max(s.gain for s in same_pair),
        )
        return PropagationEvent(
            mode=PropagationMode.INDUCTIVE,
            source_simplex_ids=[gs.id] + [s.id for s in same_pair],
            new_simplex=new, confidence=0.6,
        )

    def _transductive(
        self, gs: Simplex, network: SimplexNetwork, field: PotentialField
    ) -> Optional[PropagationEvent]:
        """Propagate role-structure across polarity: explore the other side of the rotation."""
        already = any(
            s.source == gs.target and s.target == gs.source
            for s in network.simplexes.values()
        )
        if already:
            return None
        new = Simplex(
            id=str(uuid.uuid4()),
            source=gs.target, target=gs.source, modulator=gs.modulator,
            intensity=gs.intensity * (1 - abs(gs.asymmetry)),
            asymmetry=-gs.asymmetry,
            gain=gs.gain * (1 + gs.gain),
        )
        return PropagationEvent(
            mode=PropagationMode.TRANSDUCTIVE,
            source_simplex_ids=[gs.id],
            new_simplex=new, confidence=0.4,
        )

    # ------------------------------------------------------------------
    # Eddy construction
    # ------------------------------------------------------------------

    def _build_eddy(
        self,
        steps: list[PassageStep],
        cycle_potentials: list[float],
        germ: Germ,
        provider: CorpusProvider,
        domains: list,
    ) -> Eddy:
        oz   = OperativeZero.compute(cycle_potentials)
        char = self._interference_character(steps)

        vocab_rotations: list[VocabRotation] = []
        if steps:
            final_net = steps[-1].network
            for term, sid_a, role_a, sid_b, role_b in final_net.role_shifts():
                if role_a != role_b:
                    vocab_rotations.append(VocabRotation(
                        term=term,
                        role_from=role_a, field_from=sid_a,
                        role_to=role_b,   field_to=sid_b,
                    ))

        remainder = self._collect_remainder(steps)
        fields    = list({d.definition.name for d in domains})
        summary   = self._summarise(steps, char, oz)

        return Eddy(
            id=str(uuid.uuid4()),
            scale=_scale(steps),
            source=provider.name,
            fields_in_rotation=fields,
            vocabulary_rotations=vocab_rotations,
            interference_character=char,
            what_appeared=summary,
            remainder=remainder,
            operative_zero=oz,
            steps=steps,
        )

    def _interference_character(
        self, steps: list[PassageStep]
    ) -> Optional[InterferenceCharacter]:
        if not steps:
            return None
        entropies = [s.entropy for s in steps]
        mode_totals: Counter = Counter()
        for step in steps:
            for mode, p in step.mode_distribution.items():
                mode_totals[mode] += p

        dominant = mode_totals.most_common(1)[0][0] if mode_totals else None
        delta_s  = (entropies[-1] - entropies[0]) if len(entropies) >= 2 else 0.0
        oscillating = (
            len(entropies) > 2 and any(
                entropies[i] > entropies[i - 1] and entropies[i] > entropies[i + 1]
                for i in range(1, len(entropies) - 1)
            )
        )

        if dominant == PropagationMode.TRANSDUCTIVE.value and oscillating:
            return InterferenceCharacter.TRANSVERSE
        if dominant == PropagationMode.INDUCTIVE.value:
            return InterferenceCharacter.RESONANT
        if delta_s < 0:
            return InterferenceCharacter.CONSTRUCTIVE
        return InterferenceCharacter.DESTRUCTIVE

    def _collect_remainder(self, steps: list[PassageStep]) -> list[RemainderEntry]:
        return [
            RemainderEntry(
                term_id=ev.new_simplex.modulator.id,
                amount=ev.information_gain,
                source_step=step.index,
                disposition="accumulated",
            )
            for step in steps
            for ev in step.propagation_events
            if ev.information_gain > 0
        ]

    def _summarise(
        self,
        steps: list[PassageStep],
        char: Optional[InterferenceCharacter],
        oz: OperativeZero,
    ) -> str:
        if not steps:
            return ""
        char_str  = char.value if char else "undetermined"
        n_rot     = sum(len(s.new_role_rotations) for s in steps)
        n_regime  = sum(1 for s in steps if s.regime_change)
        return (
            f"{char_str.capitalize()} interference. "
            f"{len(steps)} steps, {n_rot} role rotations, "
            f"{n_regime} regime change(s). "
            f"Operative zero: {oz}."
        )


# ------------------------------------------------------------------
# Module-level helpers
# ------------------------------------------------------------------

def _copy(network: SimplexNetwork) -> SimplexNetwork:
    new = SimplexNetwork()
    new.simplexes = dict(network.simplexes)
    return new

def _scale(steps: list[PassageStep]) -> str:
    n = len(steps)
    return "micro" if n < 5 else "meso" if n < 20 else "macro"

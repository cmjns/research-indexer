"""
GermDetector — finds RoleRotation patterns (aporiae) in a SimplexNetwork.

A RoleRotation is a cycle where A and B swap roles under the same or
related modulator. This is the structural form of an aporia.

Detection is a graph operation. The analyst selects from candidates;
the act of selection preserves externality (Simondon: the germ comes from outside).

Displacement is a pre-estimate from the current field.
The OperativeZero is computed during the passage, not at detection time.
"""
from __future__ import annotations

import itertools

from core.germ import Germ, GermSource, RoleRotation
from core.network import SimplexNetwork
from core.simplex import Role
from core.field import PotentialField


class GermDetector:

    def __init__(self, min_displacement: float = 0.01) -> None:
        self.min_displacement = min_displacement

    def detect(self,
               network: SimplexNetwork,
               field: PotentialField) -> list[Germ]:
        """
        Scan the network for RoleRotations above min_displacement.
        Returns candidate Germs for analyst selection.
        """
        rotations = self._find_role_rotations(network, field)
        germs = []
        for i, rotation in enumerate(rotations):
            if rotation.is_genuine(self.min_displacement):
                germs.append(Germ(
                    id=f"detected-{i:04d}",
                    label=self._label(rotation, network),
                    source=GermSource.DETECTED,
                    pattern=rotation,
                ))
        return germs

    def _find_role_rotations(self,
                              network: SimplexNetwork,
                              field: PotentialField) -> list[RoleRotation]:
        """
        Find 2-cycles: pairs where s1.source == s2.target AND s1.target == s2.source.
        These are the minimum structure of an aporia.
        Longer cycles are a future extension.
        """
        rotations = []
        simplexes = list(network.simplexes.values())

        for s1, s2 in itertools.combinations(simplexes, 2):
            if s1.source == s2.target and s1.target == s2.source:
                modulator_stable = (s1.modulator == s2.modulator)
                phi_entry  = field.phi(s1.source)
                phi_return = field.phi(s2.target)
                displacement = abs(phi_return - phi_entry)

                rotations.append(RoleRotation(
                    cycle=[s1.id, s2.id],
                    modulator_stable=modulator_stable,
                    displacement=displacement,
                    source_simplex_ids=[s1.id, s2.id],
                ))

        return sorted(rotations, key=lambda r: r.displacement, reverse=True)

    def _label(self, rotation: RoleRotation, network: SimplexNetwork) -> str:
        if not rotation.cycle:
            return "unnamed rotation"
        s = network.simplexes.get(rotation.cycle[0])
        if s is None:
            return "unnamed rotation"
        stable = "stable-C" if rotation.modulator_stable else "shifting-C"
        return (
            f"{s.source.label!r} ↔ {s.target.label!r} "
            f"[{stable}, Δφ={rotation.displacement:.3f}]"
        )

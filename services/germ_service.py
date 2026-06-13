from __future__ import annotations

import uuid

from core.field import PotentialField
from core.germ import Germ, GermSource, RoleRotation
from core.network import SimplexNetwork
from crystallize.germ_detector import GermDetector


class GermService:

    def __init__(self, min_displacement: float = 0.01) -> None:
        self._detector = GermDetector(min_displacement=min_displacement)

    def detect(self, network: SimplexNetwork) -> list[Germ]:
        """Scan network for candidate germs. Analyst selects from the list."""
        field = PotentialField.from_network(network)
        return self._detector.detect(network, field)

    def supply(self,
               label: str,
               simplex_ids: list[str],
               network: SimplexNetwork,
               notes: str = "") -> Germ:
        """Analyst supplies a germ directly by naming the simplex cycle."""
        field = PotentialField.from_network(network)

        for sid in simplex_ids:
            if sid not in network.simplexes:
                raise KeyError(f"Simplex {sid!r} not in network")

        # estimate displacement for the supplied cycle
        simplexes = [network.simplexes[sid] for sid in simplex_ids]
        if simplexes:
            phi_entry  = field.phi(simplexes[0].source)
            phi_return = field.phi(simplexes[-1].target)
            displacement = abs(phi_return - phi_entry)
        else:
            displacement = 0.0

        # check modulator stability
        modulators = {s.modulator for s in simplexes}
        modulator_stable = len(modulators) == 1

        pattern = RoleRotation(
            cycle=list(simplex_ids),
            modulator_stable=modulator_stable,
            displacement=displacement,
            source_simplex_ids=list(simplex_ids),
        )

        return Germ(
            id=str(uuid.uuid4()),
            label=label,
            source=GermSource.ANALYST_SUPPLIED,
            pattern=pattern,
            notes=notes,
        )

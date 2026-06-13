from __future__ import annotations

from dataclasses import dataclass

from core.term import Term
from core.simplex import Role
from core.network import SimplexNetwork


# Role weights for potential aggregation.
# SOURCE carries more potential than MODULATOR; TARGET receives it.
ROLE_WEIGHTS: dict[Role, float] = {
    Role.SOURCE:    1.0,
    Role.TARGET:    0.8,
    Role.MODULATOR: 0.5,
}


@dataclass
class PotentialField:
    """
    A scalar projection derived from a SimplexNetwork.

    φ(term) aggregates the intensities of all simplexes in which the term
    participates, weighted by the role the term plays in each simplex.

    This is not prior to the SimplexNetwork — it is computed from it.
    It is useful for thermodynamic measures (entropy, free energy) but
    should not be mistaken for the ground of individuation.
    """
    potentials: dict[str, float]   # term.id → φ

    @classmethod
    def from_network(cls, network: SimplexNetwork) -> "PotentialField":
        potentials: dict[str, float] = {}

        for term in network.terms():
            phi = 0.0
            simplexes = network.simplexes_containing(term)
            for s in simplexes:
                role = network.role_of(term, s.id)
                weight = ROLE_WEIGHTS.get(role, 0.5)
                phi += s.intensity * weight * (1.0 + abs(s.asymmetry)) * (1.0 + s.gain)
            potentials[term.id] = phi

        return cls(potentials=potentials)

    def phi(self, term: Term) -> float:
        return self.potentials.get(term.id, 0.0)

    def sorted_terms(self) -> list[tuple[str, float]]:
        return sorted(self.potentials.items(), key=lambda x: x[1], reverse=True)

    def total(self) -> float:
        return sum(self.potentials.values())

    def __repr__(self) -> str:
        top = self.sorted_terms()[:3]
        return f"PotentialField(top={top})"

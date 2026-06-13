from __future__ import annotations

from dataclasses import dataclass, field
from collections import defaultdict

from core.term import Term
from core.simplex import Simplex, Role


@dataclass
class SimplexNetwork:
    """
    The primitive representation of a text's individuation.

    We start already moving. The SimplexNetwork is not built on a prior
    potential field — it is what we have when we begin. The PotentialField
    is derived from this network, not the other way around.

    Adjacency: two simplexes are adjacent if they share at least one term.
    Role mobility: the shared term may play different roles in each simplex.
    This role difference is how individuation propagates across the network.
    """
    simplexes: dict[str, Simplex] = field(default_factory=dict)

    def add(self, simplex: Simplex) -> None:
        self.simplexes[simplex.id] = simplex

    def terms(self) -> set[Term]:
        result: set[Term] = set()
        for s in self.simplexes.values():
            result |= s.terms()
        return result

    def simplexes_containing(self, term: Term) -> list[Simplex]:
        return [s for s in self.simplexes.values() if term in s.terms()]

    def role_of(self, term: Term, simplex_id: str) -> Role | None:
        s = self.simplexes.get(simplex_id)
        if s is None:
            return None
        for role, t in s.roles().items():
            if t == term:
                return role
        return None

    def adjacency(self) -> dict[str, list[str]]:
        """
        Returns a map of simplex_id → [adjacent simplex_ids].
        Two simplexes are adjacent iff they share at least one term.
        """
        term_to_simplexes: dict[str, list[str]] = defaultdict(list)
        for sid, s in self.simplexes.items():
            for t in s.terms():
                term_to_simplexes[t.id].append(sid)

        adj: dict[str, list[str]] = defaultdict(list)
        for sid in self.simplexes:
            neighbours: set[str] = set()
            for t in self.simplexes[sid].terms():
                for neighbour in term_to_simplexes[t.id]:
                    if neighbour != sid:
                        neighbours.add(neighbour)
            adj[sid] = list(neighbours)
        return dict(adj)

    def role_shifts(self) -> list[tuple[Term, str, Role, str, Role]]:
        """
        Returns all role-shift events: (term, simplex_a_id, role_in_a,
                                                simplex_b_id, role_in_b)
        where role_in_a != role_in_b.
        These are the joints of individuation in the network.
        """
        shifts = []
        adj = self.adjacency()
        for sid, neighbours in adj.items():
            for nid in neighbours:
                s = self.simplexes[sid]
                n = self.simplexes[nid]
                shared = s.terms() & n.terms()
                for term in shared:
                    role_s = self.role_of(term, sid)
                    role_n = self.role_of(term, nid)
                    if role_s != role_n:
                        shifts.append((term, sid, role_s, nid, role_n))
        return shifts

    def __len__(self) -> int:
        return len(self.simplexes)

    def __repr__(self) -> str:
        return f"SimplexNetwork({len(self.simplexes)} simplexes, {len(self.terms())} terms)"

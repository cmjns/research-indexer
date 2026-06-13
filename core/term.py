from dataclasses import dataclass


@dataclass(frozen=True)
class Term:
    """
    A term in the simplex network.

    Terms carry no intrinsic potential. φ(term) is derived from the
    SimplexNetwork — from the intensities of all simplexes in which
    this term participates, weighted by role.

    Terms are identified by id; label is for human readability only.
    """
    id: str
    label: str

    def __repr__(self) -> str:
        return f"Term({self.label!r})"

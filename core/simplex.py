from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from core.term import Term


class Role(Enum):
    """
    The role a term plays within a simplex.

    Roles are local to a simplex — a term that is SOURCE in one simplex
    may be MODULATOR in an adjacent one. Role mobility is how the network
    propagates individuation.
    """
    SOURCE    = "A"   # emitter; signification flows from here
    TARGET    = "B"   # receiver; individuated by the relation
    MODULATOR = "C"   # relation-to-the-relation; shapes A→B without being consumed


@dataclass
class HistoricalContext:
    """
    Our now-representation of distance between domains.

    When relating texts separated in time or space (e.g. Nagarjuna and
    Candrakīrti), the distance is not an objective property of the past —
    it is a modulating construction we supply as analysts, running this
    machine now. It enters the system as C-term metadata.

    analyst_confidence makes the constructedness explicit.
    """
    temporal_distance: Optional[float] = None    # years, or transmission steps
    spatial_distance: Optional[float] = None
    institutional_factors: list[str] = field(default_factory=list)
    medium_noise: float = 0.0
    analyst_confidence: float = 1.0              # [0, 1]; 1 = high confidence


@dataclass
class Simplex:
    """
    The primitive unit: an asymmetric, modulated 3-simplex.

        A ──[C]──► B

    After Serres's triode / parasite model. Small signal at C modulates
    the large relation from A to B. C is the noise that becomes signal;
    the parasite that conditions the host relation.

    intensity  : magnitude of the A→B relation under modulation C
    asymmetry  : deviation from symmetry in the A↔B exchange; [-1, 1]
                 0 = symmetric (degenerate); ±1 = fully directional
    gain       : degree to which C amplifies (+) or attenuates (-) A→B

    historical_context: None for synchronic simplexes (within a single text);
                        supplied for diachronic simplexes (across texts/times).
    """
    id: str
    source: Term        # A
    target: Term        # B
    modulator: Term     # C
    intensity: float
    asymmetry: float    # [-1.0, 1.0]
    gain: float
    historical_context: Optional[HistoricalContext] = None

    def is_synchronic(self) -> bool:
        return self.historical_context is None

    def roles(self) -> dict[Role, Term]:
        return {
            Role.SOURCE:    self.source,
            Role.TARGET:    self.target,
            Role.MODULATOR: self.modulator,
        }

    def terms(self) -> set[Term]:
        return {self.source, self.target, self.modulator}

    def __repr__(self) -> str:
        return (
            f"Simplex({self.source.label!r} "
            f"──[{self.modulator.label!r}]──► "
            f"{self.target.label!r})"
        )

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class GermSource(Enum):
    ANALYST_SUPPLIED = "analyst"
    DETECTED         = "detected"


@dataclass
class RoleRotation:
    """
    A cycle in the SimplexNetwork where A and B swap roles under the
    same or related modulator.

    This is the structural form of an aporia. The Euthyphro:
        Simplex 1: piety → gods-love   [C: definition-seeking]
        Simplex 2: gods-love → piety   [C: definition-seeking]

    The necessary condition for germiness is displacement > 0 after
    completing the cycle: the return differs from the origin. Non-closure
    is a property revealed by traversal, not pre-computed.

    cycle              : ordered list of Simplex ids forming the rotation
    modulator_stable   : True if the same modulator term is used throughout
    displacement       : φ(return) - φ(origin); > 0 for a true aporia.
                         Computed during traversal; 0.0 until measured.
    """
    cycle: list[str]                  # ordered Simplex ids
    modulator_stable: bool = True
    displacement: float = 0.0        # filled in during GermTraversal
    source_simplex_ids: list[str] = field(default_factory=list)

    def is_genuine(self, threshold: float = 0.0) -> bool:
        """A genuine aporia has displacement strictly above threshold."""
        return self.displacement > threshold


@dataclass
class Germ:
    """
    A germ is a process — a traversal operator — not a static structure.

    It is only actualized when enacted on a specific SimplexNetwork.
    The analyst's act of selection or supply is what is 'outside':
    externality is preserved in the recognition, not in the structure.

    The germ is injected at a RoleRotation site in the network.
    Crystallization extends the network from the germ's traversal.
    """
    id: str
    label: str
    source: GermSource
    pattern: RoleRotation
    notes: str = ""                   # analyst commentary

    def __repr__(self) -> str:
        return f"Germ({self.label!r}, source={self.source.value}, displacement={self.pattern.displacement:.3f})"

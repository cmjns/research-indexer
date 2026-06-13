"""
Passage step state — the record of one step of a passage through a corpus.

PropagationMode and InterferenceCharacter live in core/propagation.py
to avoid circular imports with extract/.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from core.network import SimplexNetwork
from core.field import PotentialField
from core.simplex import Simplex
from core.germ import RoleRotation
from core.propagation import PropagationMode, InterferenceCharacter


@dataclass
class PropagationEvent:
    """
    A single simplex actualization during a passage step.

    information_gain: KL(posterior ‖ prior) — how much new information
    this actualization introduced. Contributes to the remainder ledger.
    """
    mode: PropagationMode
    source_simplex_ids: list[str]
    new_simplex: Simplex
    confidence: float
    domain_jump: Optional[tuple[str, str]] = None  # (domain_a_id, domain_b_id); transductive only
    information_gain: float = 0.0


@dataclass
class PassageStep:
    """
    The state of the passage at one step.

    mode_distribution: proportion of each PropagationMode this step.
    A shift in distribution across steps is a primary finding.

    Predominantly DEDUCTIVE  → converging toward closure
    Predominantly TRANSDUCTIVE → generative; domain-jumping; watch for regime change
    Abrupt shift             → bifurcation event

    new_role_rotations: aporiae that emerged this step —
        new sites where the passage may seed further eddies.
    """
    index: int
    network: SimplexNetwork
    field: PotentialField
    propagation_events: list[PropagationEvent] = field(default_factory=list)
    mode_distribution: dict[str, float] = field(default_factory=dict)
    entropy: float = 0.0
    entropy_delta: float = 0.0
    free_energy: float = 0.0
    new_role_rotations: list[RoleRotation] = field(default_factory=list)
    regime_change: bool = False

    def dominant_mode(self) -> Optional[PropagationMode]:
        if not self.mode_distribution:
            return None
        key = max(self.mode_distribution, key=self.mode_distribution.get)
        return PropagationMode(key)

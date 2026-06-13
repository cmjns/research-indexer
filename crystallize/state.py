from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from core.network import SimplexNetwork
from core.field import PotentialField
from core.simplex import Simplex
from core.germ import RoleRotation


class PropagationMode(Enum):
    """
    The mode of a crystallization propagation event.

    These are never pure — the mode_distribution across steps is the signal,
    not any single mode in isolation.

    DEDUCTIVE   : necessary entailment from existing simplexes.
                  Conservative; no new information; tends toward closure.

    INDUCTIVE   : pattern following across multiple simplexes.
                  Generalizing; mild compression; risks premature closure.

    TRANSDUCTIVE: structural form propagates across a domain boundary.
                  Lateral; genuinely new information; risks instability
                  without inductive support.
                  This is Simondon's primary epistemic operation.
    """
    DEDUCTIVE    = "deductive"
    INDUCTIVE    = "inductive"
    TRANSDUCTIVE = "transductive"


@dataclass
class PropagationEvent:
    """
    A single actualization during crystallization.

    Records what was actualized, how, and how much new information
    was introduced. information_gain = KL(posterior ‖ prior).
    """
    mode: PropagationMode
    source_simplex_ids: list[str]
    new_simplex: Simplex
    confidence: float
    domain_jump: Optional[tuple[str, str]] = None   # (domain_id_a, domain_id_b); transductive only
    information_gain: float = 0.0


@dataclass
class CrystallizationStep:
    """
    The state of the individuation process at one step.

    mode_distribution: proportion of each PropagationMode this step.
        A shift in distribution across steps is a primary finding.
        Predominantly DEDUCTIVE → converging.
        Predominantly TRANSDUCTIVE → generative; watch for regime change.
        Abrupt shift → bifurcation event.

    new_role_rotations: aporiae that emerged this step — new sites
        where crystallization may be seeded further.

    regime_change: True if mode_distribution has shifted abruptly
        from the previous step (Lyapunov estimate crosses threshold).
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

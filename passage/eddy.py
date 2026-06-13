"""
Eddy — the session-level output of a passage.

An eddy is a local coherence in a continuous turbulent flow.
Not a container of the flow but a momentary thickening within it.

Corresponds structurally to the eddy_ledger entry format so that
engine output can be directly serialized to the ledger
(with analyst annotation for the fields requiring judgment).

The flow is primary. The eddy is what the flow does locally.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from core.term import Term
from core.simplex import Role
from core.propagation import InterferenceCharacter
from core.operative_zero import OperativeZero
from passage.state import PassageStep


@dataclass
class VocabRotation:
    """
    A term that entered the passage in one role and exited in another.
    The eddy-level view of a role shift in the simplex network.

    Corresponds to eddy_ledger.vocabulary_in_play.rotations.
    """
    term: Term
    role_from: Role
    field_from: str     # simplex id or domain label where this role was observed
    role_to: Role
    field_to: str


@dataclass
class PatternMatch:
    """
    A recognized structural pattern instantiated by this passage.
    Corresponds to eddy_ledger.structural_pattern.

    Filled in when a known germ template matches the passage's
    RoleRotations. Retrospective — the pattern is recognized, not imposed.
    """
    pattern_name: str
    minimum_structure: str      # smallest relational config that defines the pattern
    confidence: float           # [0, 1]
    other_instances: list[str]  # eddy ids of known instances


@dataclass
class RemainderEntry:
    """
    What a passage step left behind.

    The remainder is not waste — it is the productive residue that
    motivates further passages. It re-enters the flow.
    """
    term_id: str
    amount: float
    source_step: int
    disposition: str    # "accumulated" | "discharged" | "suppressed"
    # accumulated: building toward a new potential
    # discharged:  became a new simplex in a subsequent step
    # suppressed:  absorbed by the modulator, not visible in the network


@dataclass
class Eddy:
    """
    The local coherence produced by a passage.

    Fields that require analyst judgment are left empty by the engine
    and flagged for annotation:
      - dominant_field
      - feeds_into
      - structural_pattern
      - annotations

    Fields the engine computes:
      - vocabulary_rotations (from role_shifts in the final network)
      - interference_character (from mode_distribution + entropy trajectory)
      - operative_zero (from cycle_potentials across steps)
      - remainder (from AccountingLedger)
      - what_appeared (computed summary; analyst may replace)

    Corresponds to eddy_ledger entry structure.
    """
    id: str
    scale: str                                  # "micro" | "meso" | "macro"
    source: str                                 # corpus provider name

    fields_in_rotation: list[str]               # domain/field names active in this passage
    dominant_field: Optional[str] = None        # analyst annotation

    vocabulary_rotations: list[VocabRotation] = field(default_factory=list)

    interference_character: Optional[InterferenceCharacter] = None
    what_appeared: str = ""                     # computed summary

    remainder: list[RemainderEntry] = field(default_factory=list)
    feeds_into: list[str] = field(default_factory=list)   # analyst annotation: eddy ids

    structural_pattern: Optional[PatternMatch] = None     # analyst annotation

    operative_zero: Optional[OperativeZero] = None

    steps: list[PassageStep] = field(default_factory=list)

    # analyst annotation fields — empty from engine, filled by hand
    annotations: str = ""

    def to_ledger_entry(self) -> dict:
        """
        Serialize to the eddy_ledger entry format.
        Fields requiring analyst judgment are marked with '_needs_annotation'.
        """
        return {
            "id": self.id,
            "scale": self.scale,
            "source": self.source,
            "fields_in_rotation": {
                "fields": self.fields_in_rotation,
                "dominant_field": self.dominant_field or "_needs_annotation",
            },
            "vocabulary_in_play": {
                "terms": list({r.term.label for r in self.vocabulary_rotations}),
                "rotations": [
                    {
                        "term": r.term.label,
                        "from": f"role:{r.role_from.value} in {r.field_from}",
                        "to":   f"role:{r.role_to.value} in {r.field_to}",
                    }
                    for r in self.vocabulary_rotations
                ],
            },
            "interference": {
                "what_appeared": self.what_appeared,
                "character": self.interference_character.value
                             if self.interference_character else "_needs_annotation",
            },
            "remainder": {
                "unresolved": [
                    f"{e.term_id}: {e.amount:.4f} ({e.disposition})"
                    for e in self.remainder
                ],
                "feeds_into": self.feeds_into or ["_needs_annotation"],
            },
            "structural_pattern": {
                "pattern_name": self.structural_pattern.pattern_name
                                 if self.structural_pattern else "_needs_annotation",
                "minimum_structure": self.structural_pattern.minimum_structure
                                      if self.structural_pattern else "",
                "other_instances": self.structural_pattern.other_instances
                                    if self.structural_pattern else [],
            },
            "operative_zero": str(self.operative_zero) if self.operative_zero else None,
            "step_count": len(self.steps),
            "annotations": self.annotations or "_needs_annotation",
        }

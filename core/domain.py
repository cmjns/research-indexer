from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DomainDefinition:
    """
    A named level in the domain hierarchy, with an ordinal scale of extension
    and a reference to the segmenter that produces instances of this level.

    Segmenters are registered by name in DomainRegistry. The NLP segmenter
    is the default first implementation, with explicit theoretical commitments.

    level: higher = more extended.
        sentence=1, thought=2, argument=3, work=4, corpus=5 (defaults)
    """
    name: str
    level: int
    segmenter: str   # name of a registered Segmenter


@dataclass
class Medium:
    """
    The carrier of a Domain. Separate from the domain it carries.

    The medium contributes structured noise and velocity — a PDF and a
    handwritten manuscript of the same text are not equivalent. These
    differences modulate what can be extracted and at what fidelity.

    velocity         : distributability / bandwidth coefficient
    noise_coefficient: signal degradation per extraction step
    extraction_cost  : computational / metabolic cost of processing
    """
    format: str                  # "plaintext", "pdf", "epub", "audio", ...
    velocity: float = 1.0
    noise_coefficient: float = 0.0
    extraction_cost: float = 1.0


@dataclass
class Domain:
    """
    A unit of meaning at a given scale of extension.

    Domains are hierarchically nested: a corpus contains works contains
    arguments contains thoughts contains sentences. The hierarchy is
    user-defined via DomainDefinitions.

    content  : raw content at this scale (before simplex extraction)
    medium   : the carrier
    """
    id: str
    definition: DomainDefinition
    content: str
    medium: Medium
    parent_id: Optional[str] = None
    children_ids: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)   # open slot for historical context etc.

    def __repr__(self) -> str:
        return f"Domain({self.definition.name!r}, id={self.id!r})"


class DomainRegistry:
    """
    Holds all DomainDefinitions for a session.
    Ships with defaults; fully replaceable.
    """

    DEFAULT_DEFINITIONS: list[DomainDefinition] = [
        DomainDefinition("sentence",  1, "nlp_sentence"),
        DomainDefinition("thought",   2, "nlp_paragraph"),
        DomainDefinition("argument",  3, "nlp_section"),
        DomainDefinition("work",      4, "file"),
        DomainDefinition("corpus",    5, "directory"),
    ]

    def __init__(self) -> None:
        self._definitions: dict[str, DomainDefinition] = {
            d.name: d for d in self.DEFAULT_DEFINITIONS
        }

    def register(self, defn: DomainDefinition) -> None:
        self._definitions[defn.name] = defn

    def get(self, name: str) -> DomainDefinition:
        if name not in self._definitions:
            raise KeyError(f"No DomainDefinition named {name!r}")
        return self._definitions[name]

    def all(self) -> list[DomainDefinition]:
        return sorted(self._definitions.values(), key=lambda d: d.level)

"""
CorpusProvider — the engine's only entry point to content.

The engine knows nothing about source format. A library of JSON entries,
a directory of analyst reports, a set of URLs — all are providers.
The provider knows how to read from its source and produce Domains.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator

from core.domain import Domain


class CorpusProvider(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable identifier for this corpus."""
        ...

    @abstractmethod
    def domains(self, level: str = "work") -> Iterator[Domain]:
        """
        Yield Domains at the requested level of extension.

        level: any DomainDefinition name — "sentence", "work", "corpus", etc.
        The provider decides how to segment its content at that level.
        If the level is not supported, yield at the provider's natural level.
        """
        ...

    def vocabulary(self) -> dict[str, list[str]]:
        """
        Optional: a pre-existing topic map for this corpus.
        Returns tag → [specific terms].

        If absent (empty dict), the engine builds vocabulary from the text.
        A library provider may return its topic_map here.
        A directory provider returns {} by default.
        """
        return {}

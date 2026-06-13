"""
DirectoryProvider — reads plain text (and optionally PDF) files from a directory.

The simplest provider: a folder of files, each treated as one Domain at
the "work" level. Segments to finer levels on request using the DomainRegistry.

PDF support requires pdfplumber (optional dependency).
"""
from __future__ import annotations

import uuid
from pathlib import Path
from typing import Iterator

from core.domain import Domain, DomainDefinition, DomainRegistry, Medium
from corpus.base import CorpusProvider


class DirectoryProvider(CorpusProvider):

    def __init__(
        self,
        path: str | Path,
        glob: str = "**/*.txt",
        medium_format: str = "plaintext",
    ) -> None:
        self._path = Path(path)
        self._glob = glob
        self._medium_format = medium_format
        self._registry = DomainRegistry()

    @property
    def name(self) -> str:
        return f"directory:{self._path.name}"

    def domains(self, level: str = "work") -> Iterator[Domain]:
        medium = self._make_medium()

        for file_path in sorted(self._path.glob(self._glob)):
            content = self._read(file_path)
            if not content:
                continue

            defn = self._registry.get(level) if level in [
                d.name for d in self._registry.all()
            ] else self._registry.get("work")

            domain = Domain(
                id=str(uuid.uuid4()),
                definition=defn,
                content=content,
                medium=medium,
                metadata={"source_file": str(file_path)},
            )
            yield domain

    def _read(self, path: Path) -> str:
        suffix = path.suffix.lower()
        if suffix in (".txt", ".md", ".rst"):
            return path.read_text(encoding="utf-8", errors="replace")
        elif suffix == ".pdf":
            return self._read_pdf(path)
        return ""

    def _read_pdf(self, path: Path) -> str:
        try:
            import pdfplumber
            with pdfplumber.open(path) as pdf:
                return "\n".join(
                    page.extract_text() or ""
                    for page in pdf.pages
                )
        except ImportError:
            raise ImportError(
                "PDF support requires pdfplumber. "
                "Install: pip install pdfplumber"
            )

    def _make_medium(self) -> Medium:
        noise = {"pdf": 0.15, "plaintext": 0.0}.get(self._medium_format, 0.05)
        cost  = {"pdf": 2.0,  "plaintext": 1.0}.get(self._medium_format, 1.5)
        return Medium(
            format=self._medium_format,
            velocity=1.0,
            noise_coefficient=noise,
            extraction_cost=cost,
        )

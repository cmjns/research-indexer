"""
PassageService — SOA interface for the passage engine.

Manages sessions (provider + germ + accumulated steps).
The stable API surface; engine internals can change without breaking callers.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from core.germ import Germ
from corpus.base import CorpusProvider
from extract.base import SimplexExtractor
from passage.engine import PassageEngine
from passage.eddy import Eddy


@dataclass
class PassageSession:
    id: str
    provider: CorpusProvider
    germ: Germ
    eddy: Eddy | None = None


class PassageService:

    def __init__(
        self,
        extractor: SimplexExtractor,
        temperature: float = 1.0,
    ) -> None:
        self._engine = PassageEngine(extractor=extractor, temperature=temperature)
        self._sessions: dict[str, PassageSession] = {}

    def new_session(self, provider: CorpusProvider, germ: Germ) -> str:
        sid = str(uuid.uuid4())
        self._sessions[sid] = PassageSession(id=sid, provider=provider, germ=germ)
        return sid

    def run(
        self,
        session_id: str,
        max_steps: int = 50,
        halt_on_stable: bool = True,
    ) -> Eddy:
        session = self._get(session_id)
        eddy = self._engine.run(
            provider=session.provider,
            germ=session.germ,
            max_steps=max_steps,
            halt_on_stable=halt_on_stable,
        )
        session.eddy = eddy
        return eddy

    def get_eddy(self, session_id: str) -> Eddy | None:
        return self._get(session_id).eddy

    def list_sessions(self) -> list[str]:
        return list(self._sessions.keys())

    def _get(self, session_id: str) -> PassageSession:
        if session_id not in self._sessions:
            raise KeyError(f"No session {session_id!r}")
        return self._sessions[session_id]

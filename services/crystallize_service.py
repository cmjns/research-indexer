"""
CrystallizeService — SOA interface for the crystallization engine.

All business logic lives in crystallize/engine.py.
This service manages sessions and is the stable API surface.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from core.germ import Germ
from core.network import SimplexNetwork
from crystallize.engine import CrystallizationEngine
from crystallize.state import CrystallizationStep


@dataclass
class Session:
    id: str
    network: SimplexNetwork
    germ: Germ
    steps: list[CrystallizationStep] = field(default_factory=list)


class CrystallizeService:

    def __init__(self, temperature: float = 1.0) -> None:
        self._engine = CrystallizationEngine(temperature=temperature)
        self._sessions: dict[str, Session] = {}

    def new_session(self, network: SimplexNetwork, germ: Germ) -> str:
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = Session(
            id=session_id, network=network, germ=germ
        )
        return session_id

    def step(self, session_id: str) -> CrystallizationStep:
        session = self._get(session_id)
        entropy_history = [s.entropy for s in session.steps]
        step = self._engine._step(
            session.network, session.germ,
            index=len(session.steps),
            entropy_history=entropy_history,
        )
        session.steps.append(step)
        session.network = step.network
        return step

    def run(self,
            session_id: str,
            max_steps: int = 50,
            halt_on_stable: bool = True) -> list[CrystallizationStep]:
        session = self._get(session_id)
        new_steps = self._engine.run(
            session.network, session.germ,
            max_steps=max_steps,
            halt_on_stable=halt_on_stable,
        )
        session.steps.extend(new_steps)
        if new_steps:
            session.network = new_steps[-1].network
        return new_steps

    def get_steps(self, session_id: str) -> list[CrystallizationStep]:
        return self._get(session_id).steps

    def list_sessions(self) -> list[str]:
        return list(self._sessions.keys())

    def _get(self, session_id: str) -> Session:
        if session_id not in self._sessions:
            raise KeyError(f"No session {session_id!r}")
        return self._sessions[session_id]

"""In-memory session store + per-session agent orchestration.

MVP persistence is in-memory only (no DB). A session holds both agents, their
retention/pruning config, and the accumulated turn records.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from .pruning.retention_policy import RetentionPolicy


@dataclass
class Session:
    """One comparison session (a single conversation run through both agents)."""

    session_id: str
    retention_policy: RetentionPolicy
    prune_every: int
    recent_turns_to_keep: int
    turns: list[dict[str, Any]] = field(default_factory=list)
    # Agent instances are attached during wiring (feat/agents-ab-endpoint).


class SessionManager:
    """Creates and looks up in-memory sessions."""

    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    def create(
        self,
        retention_policy: RetentionPolicy,
        prune_every: int,
        recent_turns_to_keep: int,
    ) -> Session:
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        session = Session(
            session_id=session_id,
            retention_policy=retention_policy,
            prune_every=prune_every,
            recent_turns_to_keep=recent_turns_to_keep,
        )
        self._sessions[session_id] = session
        return session

    def get(self, session_id: str) -> Session | None:
        return self._sessions.get(session_id)

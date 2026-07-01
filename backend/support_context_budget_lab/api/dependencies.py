"""Shared FastAPI dependencies (singletons)."""

from __future__ import annotations

from functools import lru_cache

from ..session_manager import SessionManager


@lru_cache
def get_session_manager() -> SessionManager:
    """Process-wide in-memory session store."""
    return SessionManager()

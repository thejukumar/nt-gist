"""Write a full session log to logs/session_<timestamp>.json."""

from __future__ import annotations

from pathlib import Path

_LOGS_DIR = Path(__file__).resolve().parents[3] / "logs"


def write_session_log(session: object) -> Path:
    """Serialize a session (setup, turns, metrics, summary) to JSON.

    TODO(feat/reporting-polish): build the JSON structure from the session and
    write it under logs/; return the path.
    """
    raise NotImplementedError

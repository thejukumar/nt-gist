"""Build and write a full session log to logs/session_<timestamp>.json."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from ..config import get_settings

_LOGS_DIR = Path(__file__).resolve().parents[3] / "logs"


def _ratio(saved: float, base: float) -> float:
    return saved / base if base else 0.0


def build_session_log(session) -> dict:
    """Serialize a session (setup, turns, metrics, summary) to a dict."""
    settings = get_settings()
    b = session.baseline_stats
    p = session.pruned_stats
    cost_saved = b.total_cost - p.total_cost
    return {
        "session_id": session.session_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "model": settings.nebius_model,
        "provider": "Nebius",
        "tool_provider": "Tavily",
        "prune_every": session.prune_every,
        "recent_turns_to_keep": session.recent_turns_to_keep,
        "retention_policy": asdict(session.retention_policy),
        "turns": session.turns,
        "summary": {
            "turns": b.turns,
            "baseline_total_input_tokens": b.total_input_tokens,
            "pruned_total_input_tokens": p.total_input_tokens,
            "baseline_total_tokens": b.total_tokens,
            "pruned_total_tokens": p.total_tokens,
            "input_token_reduction_percent": _ratio(
                b.total_input_tokens - p.total_input_tokens, b.total_input_tokens
            ),
            "baseline_total_cost": b.total_cost,
            "pruned_total_cost": p.total_cost,
            "estimated_cost_savings": cost_saved,
            "cost_reduction_percent": _ratio(cost_saved, b.total_cost),
            "baseline_avg_latency": b.average_latency,
            "pruned_avg_latency": p.average_latency,
        },
    }


def write_session_log(session, path: Path | None = None) -> Path:
    """Write the session log JSON; return the path."""
    _LOGS_DIR.mkdir(exist_ok=True)
    if path is None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        path = _LOGS_DIR / f"session_{stamp}.json"
    path.write_text(json.dumps(build_session_log(session), indent=2))
    return path

"""Shared, deterministic search decision used identically by both agents.

MVP heuristic: search when the user's message looks like it needs external
info. Both agents use the same rule so the only variable between them stays the
context strategy. (A model-driven tool-calling loop is a documented future
enhancement.)
"""

from __future__ import annotations

from ..tools.tavily_client import SourceRecord

_SEARCH_KEYWORDS = (
    "research",
    "find",
    "search",
    "latest",
    "current",
    "recent",
    "news",
    "cause",
    "causes",
    "common",
    "web",
    "look up",
    "check",
    "explain",
    "price",
    "compare",
)


def should_search(message: str) -> bool:
    """True if the message suggests external/web information is needed."""
    lowered = message.lower()
    return any(keyword in lowered for keyword in _SEARCH_KEYWORDS)


def format_evidence(records: list[SourceRecord]) -> str:
    """Render Tavily results as a compact text block."""
    return "\n".join(f"- {r.title} ({r.url}): {r.snippet}" for r in records)

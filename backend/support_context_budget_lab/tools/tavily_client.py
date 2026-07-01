"""Tavily search wrapper (TavilySearch via langchain-tavily).

Runs searches, normalizes results into compact SourceRecords, and counts tool
calls (a per-turn metric). MVP uses Tavily Search only. langchain is imported
lazily so importing this module does not require it to be installed.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any


@dataclass
class SourceRecord:
    """A normalized Tavily result."""

    title: str
    url: str
    snippet: str


def _normalize_results(raw: Any) -> list[SourceRecord]:
    """Coerce TavilySearch output (dict / JSON string / list) to SourceRecords."""
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except json.JSONDecodeError:
            return []
    if isinstance(raw, dict):
        results = raw.get("results", [])
    elif isinstance(raw, list):
        results = raw
    else:
        results = []

    records: list[SourceRecord] = []
    for r in results:
        if not isinstance(r, dict):
            continue
        records.append(
            SourceRecord(
                title=r.get("title", "Untitled"),
                url=r.get("url", ""),
                snippet=" ".join((r.get("content", "") or "").split()),
            )
        )
    return records


class TavilyClient:
    """Thin wrapper around TavilySearch with normalization + call counting."""

    def __init__(self, api_key: str, max_results: int = 5) -> None:
        from langchain_tavily import TavilySearch

        if api_key:
            os.environ.setdefault("TAVILY_API_KEY", api_key)
        self._search = TavilySearch(max_results=max_results)
        self.tool_calls = 0

    def search(self, query: str) -> list[SourceRecord]:
        """Run a search, count the call, and return normalized records."""
        raw = self._search.invoke({"query": query})
        self.tool_calls += 1
        return _normalize_results(raw)

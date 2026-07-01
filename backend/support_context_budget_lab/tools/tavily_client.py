"""Tavily search wrapper (TavilySearch via langchain-tavily).

Runs searches, normalizes results into compact SourceRecords, and tracks the
number of tool calls made (a per-turn metric). MVP uses Tavily Search only.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SourceRecord:
    """A normalized Tavily result."""

    title: str
    url: str
    snippet: str


class TavilyClient:
    """Thin wrapper around TavilySearch with normalization + call counting."""

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self.tool_calls = 0
        # TODO(feat/providers-metrics): instantiate TavilySearch(...)

    def search(self, query: str, max_results: int = 5) -> list[SourceRecord]:
        """Run a search and return normalized source records.

        TODO(feat/providers-metrics): call TavilySearch, normalize results,
        increment self.tool_calls.
        """
        raise NotImplementedError

"""Evidence ledger — compact Tavily sources instead of raw tool output."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class EvidenceItem:
    """A single compact Tavily source retained across turns."""

    source_id: str
    title: str
    url: str
    snippet: str
    relevant_claim: str
    first_seen_turn: int
    last_used_turn: int


@dataclass
class EvidenceLedger:
    """Holds compact evidence items, deduplicated by URL/source."""

    items: list[EvidenceItem] = field(default_factory=list)

    def upsert(self, item: EvidenceItem) -> None:
        """Add a new item or update the existing one with the same url."""
        for existing in self.items:
            if existing.url and existing.url == item.url:
                existing.snippet = item.snippet or existing.snippet
                existing.relevant_claim = item.relevant_claim or existing.relevant_claim
                existing.last_used_turn = max(existing.last_used_turn, item.last_used_turn)
                return
        self.items.append(item)

    def to_prompt_block(self) -> str:
        """Render the ledger as a compact prompt-ready block."""
        if not self.items:
            return "Evidence ledger: (empty)"
        lines = ["Evidence ledger:"]
        for it in self.items:
            claim = it.relevant_claim or it.snippet
            lines.append(f"- [{it.source_id}] {it.title} ({it.url}): {claim}")
        return "\n".join(lines)

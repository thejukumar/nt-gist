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
        """Add or update an evidence item (dedupe by url).

        TODO(feat/pruning-engine): merge by url, update last_used_turn.
        """
        raise NotImplementedError

    def to_prompt_block(self) -> str:
        """Render the ledger as a compact prompt-ready block.

        TODO(feat/pruning-engine): list source_id, title, url, relevant_claim.
        """
        raise NotImplementedError

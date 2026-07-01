"""Context pruner — builds the compact context sent to the pruned agent.

Decoupled from metrics: this module returns a pruned message list and updated
state only. It never measures tokens/latency/cost — that is the metrics layer's
job (see support_context_budget_lab.metrics).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .evidence_ledger import EvidenceLedger
from .retention_policy import RetentionPolicy
from .support_memory import SupportMemory

Message = dict[str, Any]  # {"role": ..., "content": ...}


@dataclass
class PruningEvent:
    """A record of one pruning pass, for the UI timeline + report."""

    turn: int
    compressed_messages: int
    preserved: list[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class PruneResult:
    """Output of a pruning pass."""

    messages: list[Message]
    memory: SupportMemory
    ledger: EvidenceLedger
    event: PruningEvent | None  # None when no pruning happened this turn


class ContextPruner:
    """Retention-aware pruner: keep recent turns + memory + evidence ledger.

    Default trigger: prune every `prune_every` turns, keep the last
    `recent_turns_to_keep` turns verbatim.
    """

    def __init__(self, prune_every: int = 2, recent_turns_to_keep: int = 2) -> None:
        self.prune_every = prune_every
        self.recent_turns_to_keep = recent_turns_to_keep

    def should_prune(self, turn: int) -> bool:
        """Whether pruning fires on this turn."""
        return turn > 0 and turn % self.prune_every == 0

    def prune(
        self,
        history: list[Message],
        *,
        turn: int,
        policy: RetentionPolicy,
        memory: SupportMemory,
        ledger: EvidenceLedger,
    ) -> PruneResult:
        """Produce the compact message list for the pruned agent.

        TODO(feat/pruning-engine):
          - keep system prompt + current message + last N turns
          - fold older turns into SupportMemory; move Tavily blobs to the ledger
          - drop duplicate snippets / raw blobs already captured
          - emit a PruningEvent describing what was compressed/preserved
        """
        raise NotImplementedError

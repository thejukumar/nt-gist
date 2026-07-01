"""Pruned agent — uses compact context from the pruning engine."""

from __future__ import annotations

from typing import Any

from ..llm.nebius_client import NebiusClient
from ..metrics.metrics_models import TurnMetrics
from ..pruning.context_pruner import ContextPruner, PruningEvent
from ..pruning.evidence_ledger import EvidenceLedger
from ..pruning.retention_policy import RetentionPolicy
from ..pruning.support_memory import SupportMemory
from ..tools.tavily_client import TavilyClient


class PrunedAgent:
    """Retention-aware agent: recent turns + support memory + evidence ledger."""

    def __init__(
        self,
        llm: NebiusClient,
        tavily: TavilyClient,
        pruner: ContextPruner,
        policy: RetentionPolicy,
    ) -> None:
        self.llm = llm
        self.tavily = tavily
        self.pruner = pruner
        self.policy = policy
        self.memory = SupportMemory()
        self.ledger = EvidenceLedger()
        self.history: list[dict[str, Any]] = []

    def run_turn(
        self, user_message: str, turn: int
    ) -> tuple[str, TurnMetrics, PruningEvent | None]:
        """Prune context, answer, return response + metrics + pruning event.

        TODO(feat/agents-ab-endpoint): run history through the pruner, send the
        compact context to Nebius, capture TurnMetrics, surface the PruningEvent.
        """
        raise NotImplementedError

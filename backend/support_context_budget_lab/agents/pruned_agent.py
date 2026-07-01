"""Pruned agent — uses compact context from the pruning engine.

Keeps only the original user/assistant turns in history; Tavily evidence goes
into the compact ledger rather than being carried raw. The pruner rebuilds a
compact context each turn, so input tokens stay lean.
"""

from __future__ import annotations

from typing import Any

from ..llm.nebius_client import NebiusClient
from ..metrics.cost import estimate_cost
from ..metrics.metrics_models import TurnMetrics
from ..pruning.context_pruner import ContextPruner, PruningEvent
from ..pruning.evidence_ledger import EvidenceItem, EvidenceLedger
from ..pruning.retention_policy import RetentionPolicy
from ..pruning.support_memory import SupportMemory
from ..tools.tavily_client import TavilyClient
from .prompts import PRUNED_SYSTEM_PROMPT
from .search_policy import should_search


class PrunedAgent:
    """Retention-aware agent: recent turns + support memory + evidence ledger."""

    def __init__(
        self,
        llm: NebiusClient,
        tavily: TavilyClient,
        pruner: ContextPruner,
        policy: RetentionPolicy,
        input_cost_per_1m: float = 0.0,
        output_cost_per_1m: float = 0.0,
    ) -> None:
        self.llm = llm
        self.tavily = tavily
        self.pruner = pruner
        self.policy = policy
        self.input_cost_per_1m = input_cost_per_1m
        self.output_cost_per_1m = output_cost_per_1m
        self.memory = SupportMemory()
        self.ledger = EvidenceLedger()
        self.history: list[dict[str, Any]] = []

    def run_turn(
        self, user_message: str, turn: int
    ) -> tuple[str, TurnMetrics, PruningEvent | None]:
        """Prune context, answer, return response + metrics + pruning event."""
        self.history.append({"role": "user", "content": user_message})

        tool_calls = 0
        if should_search(user_message):
            records = self.tavily.search(user_message)
            tool_calls = 1
            for i, r in enumerate(records):
                self.ledger.upsert(
                    EvidenceItem(
                        source_id=f"src_{turn}_{i + 1}",
                        title=r.title,
                        url=r.url,
                        snippet=r.snippet,
                        relevant_claim=r.snippet[:160],
                        first_seen_turn=turn,
                        last_used_turn=turn,
                    )
                )

        pruned = self.pruner.prune(
            self.history,
            turn=turn,
            policy=self.policy,
            memory=self.memory,
            ledger=self.ledger,
            system_prompt=PRUNED_SYSTEM_PROMPT,
        )

        result = self.llm.complete(pruned.messages)
        self.history.append({"role": "assistant", "content": result.text})

        metrics = TurnMetrics(
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            latency_seconds=result.latency_seconds,
            estimated_cost=estimate_cost(
                result.input_tokens,
                result.output_tokens,
                input_cost_per_1m=self.input_cost_per_1m,
                output_cost_per_1m=self.output_cost_per_1m,
            ),
            tool_calls=tool_calls,
            estimated=result.estimated,
        )
        return result.text, metrics, pruned.event

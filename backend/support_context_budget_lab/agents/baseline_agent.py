"""Baseline agent — keeps the full conversation history every turn.

Carries prior turns AND prior raw Tavily evidence forever, so its input tokens
grow across a long conversation.
"""

from __future__ import annotations

from typing import Any

from ..llm.nebius_client import NebiusClient
from ..metrics.cost import estimate_cost
from ..metrics.metrics_models import TurnMetrics
from ..tools.tavily_client import TavilyClient
from .prompts import BASELINE_SYSTEM_PROMPT
from .search_policy import format_evidence, should_search


class BaselineAgent:
    """Full-history support agent (the naive, ever-growing-context approach)."""

    def __init__(
        self,
        llm: NebiusClient,
        tavily: TavilyClient,
        input_cost_per_1m: float = 0.0,
        output_cost_per_1m: float = 0.0,
    ) -> None:
        self.llm = llm
        self.tavily = tavily
        self.input_cost_per_1m = input_cost_per_1m
        self.output_cost_per_1m = output_cost_per_1m
        self.history: list[dict[str, Any]] = []

    def run_turn(self, user_message: str, turn: int) -> tuple[str, TurnMetrics]:
        """Answer using the full history; return response text + real metrics."""
        tool_calls = 0
        content = user_message
        if should_search(user_message):
            records = self.tavily.search(user_message)
            tool_calls = 1
            if records:
                # Baseline persists raw evidence into history -> context bloat.
                content = f"{user_message}\n\n[Web evidence]\n{format_evidence(records)}"

        self.history.append({"role": "user", "content": content})
        messages = [{"role": "system", "content": BASELINE_SYSTEM_PROMPT}, *self.history]

        result = self.llm.complete(messages)
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
        return result.text, metrics

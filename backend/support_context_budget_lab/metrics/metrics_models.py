"""Shared metric data models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TurnMetrics:
    """Real stats captured from one agent's Nebius call on one turn."""

    input_tokens: int
    output_tokens: int
    latency_seconds: float
    estimated_cost: float
    tool_calls: int
    estimated: bool = False  # True if token counts came from the fallback estimator

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

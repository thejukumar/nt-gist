"""Cumulative session statistics and baseline-vs-pruned comparison."""

from __future__ import annotations

from dataclasses import dataclass, field

from .metrics_models import TurnMetrics


@dataclass
class CumulativeStats:
    """Running totals for one agent across a session."""

    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0
    total_tool_calls: int = 0
    turns: int = 0
    _latencies: list[float] = field(default_factory=list)

    def add(self, m: TurnMetrics) -> None:
        """Fold one turn's metrics into the totals.

        TODO(feat/reporting-polish): accumulate tokens/cost/tool_calls/latency.
        """
        raise NotImplementedError

    @property
    def total_tokens(self) -> int:
        return self.total_input_tokens + self.total_output_tokens

    @property
    def average_latency(self) -> float:
        return sum(self._latencies) / len(self._latencies) if self._latencies else 0.0


def comparison(baseline: CumulativeStats, pruned: CumulativeStats) -> dict:
    """Compute savings of pruned vs baseline (tokens, cost, %).

    TODO(feat/reporting-polish): input_tokens_saved, reduction %, cost saved, %.
    """
    raise NotImplementedError

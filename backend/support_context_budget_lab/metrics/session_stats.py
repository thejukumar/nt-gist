"""Cumulative session statistics and baseline-vs-pruned comparison.

Percent fields are fractions in [0, 1] (the frontend formatter multiplies by 100).
"""

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
        """Fold one turn's metrics into the totals."""
        self.total_input_tokens += m.input_tokens
        self.total_output_tokens += m.output_tokens
        self.total_cost += m.estimated_cost
        self.total_tool_calls += m.tool_calls
        self.turns += 1
        self._latencies.append(m.latency_seconds)

    @property
    def total_tokens(self) -> int:
        return self.total_input_tokens + self.total_output_tokens

    @property
    def average_latency(self) -> float:
        return sum(self._latencies) / len(self._latencies) if self._latencies else 0.0


def _safe_ratio(saved: float, base: float) -> float:
    return saved / base if base else 0.0


def comparison(baseline: CumulativeStats, pruned: CumulativeStats) -> dict:
    """Savings of pruned vs baseline (cumulative). Percents are fractions."""
    input_tokens_saved = baseline.total_input_tokens - pruned.total_input_tokens
    estimated_cost_saved = baseline.total_cost - pruned.total_cost
    return {
        "input_tokens_saved": input_tokens_saved,
        "input_token_reduction_percent": _safe_ratio(
            input_tokens_saved, baseline.total_input_tokens
        ),
        "estimated_cost_saved": estimated_cost_saved,
        "cost_reduction_percent": _safe_ratio(estimated_cost_saved, baseline.total_cost),
        "latency_delta_seconds": pruned.average_latency - baseline.average_latency,
    }

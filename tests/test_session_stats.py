"""CumulativeStats aggregation + baseline-vs-pruned comparison."""

from support_context_budget_lab.metrics.metrics_models import TurnMetrics
from support_context_budget_lab.metrics.session_stats import CumulativeStats, comparison


def _turn(inp, out, latency, cost, tools=1):
    return TurnMetrics(
        input_tokens=inp,
        output_tokens=out,
        latency_seconds=latency,
        estimated_cost=cost,
        tool_calls=tools,
    )


def test_average_latency_empty_is_zero():
    assert CumulativeStats().average_latency == 0.0


def test_total_tokens_property():
    stats = CumulativeStats(total_input_tokens=100, total_output_tokens=25)
    assert stats.total_tokens == 125


def test_add_accumulates():
    stats = CumulativeStats()
    stats.add(_turn(100, 20, 1.0, 0.001))
    stats.add(_turn(200, 30, 3.0, 0.002))
    assert stats.total_input_tokens == 300
    assert stats.total_output_tokens == 50
    assert stats.total_tool_calls == 2
    assert stats.turns == 2
    assert stats.average_latency == 2.0
    assert round(stats.total_cost, 6) == 0.003


def test_comparison_reports_fractional_savings():
    baseline = CumulativeStats()
    pruned = CumulativeStats()
    baseline.add(_turn(1000, 100, 5.0, 0.010))
    pruned.add(_turn(400, 100, 4.0, 0.006))

    cmp = comparison(baseline, pruned)
    assert cmp["input_tokens_saved"] == 600
    assert round(cmp["input_token_reduction_percent"], 3) == 0.6  # 60% as a fraction
    assert round(cmp["estimated_cost_saved"], 6) == 0.004
    assert cmp["latency_delta_seconds"] == -1.0


def test_comparison_handles_zero_baseline():
    cmp = comparison(CumulativeStats(), CumulativeStats())
    assert cmp["input_token_reduction_percent"] == 0.0
    assert cmp["cost_reduction_percent"] == 0.0

"""CumulativeStats properties (aggregation lands in feat/reporting-polish)."""

import pytest

from support_context_budget_lab.metrics.session_stats import CumulativeStats


def test_average_latency_empty_is_zero():
    assert CumulativeStats().average_latency == 0.0


def test_total_tokens_property():
    stats = CumulativeStats(total_input_tokens=100, total_output_tokens=25)
    assert stats.total_tokens == 125


@pytest.mark.skip(reason="add()/comparison() land in feat/reporting-polish")
def test_add_accumulates():
    ...

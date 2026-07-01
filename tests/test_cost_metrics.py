"""Cost estimation is pure and implemented in the scaffold."""

from support_context_budget_lab.metrics.cost import estimate_cost


def test_estimate_cost_basic():
    cost = estimate_cost(
        1_000_000, 500_000, input_cost_per_1m=0.60, output_cost_per_1m=2.40
    )
    # 1.0 * 0.60 + 0.5 * 2.40 = 1.80
    assert round(cost, 6) == 1.80


def test_estimate_cost_zero_tokens():
    assert estimate_cost(0, 0, input_cost_per_1m=0.60, output_cost_per_1m=2.40) == 0.0

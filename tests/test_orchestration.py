"""SessionManager A/B orchestration (with an injected fake agent factory)."""

from conftest import FakeLLM, FakeTavily

from support_context_budget_lab.agents.baseline_agent import BaselineAgent
from support_context_budget_lab.agents.pruned_agent import PrunedAgent
from support_context_budget_lab.pruning.context_pruner import ContextPruner
from support_context_budget_lab.pruning.retention_policy import RetentionPolicy
from support_context_budget_lab.session_manager import SessionManager


def _fake_factory(session):
    pruner = ContextPruner(
        prune_every=session.prune_every,
        recent_turns_to_keep=session.recent_turns_to_keep,
    )
    baseline = BaselineAgent(FakeLLM(), FakeTavily())
    pruned = PrunedAgent(FakeLLM(), FakeTavily(), pruner, session.retention_policy)
    return baseline, pruned


def _msg(i: int) -> str:
    # Realistically long so baseline history growth dominates pruned overhead.
    return (
        f"Turn {i}: the customer reports a detailed issue needing a thorough, "
        "substantial support reply every single time. " * 3
    )


def _run(turns=6):
    sm = SessionManager(agent_factory=_fake_factory)
    session = sm.create(RetentionPolicy(), prune_every=2, recent_turns_to_keep=2)
    records = [sm.run_turn(session, _msg(i)) for i in range(1, turns + 1)]
    return sm, session, records


def test_turn_record_shape():
    _, _, records = _run(turns=1)
    rec = records[0]
    assert rec["turn"] == 1
    assert set(rec) == {"turn", "baseline", "pruned", "comparison"}
    assert set(rec["baseline"]) == {"response", "metrics"}
    assert rec["pruned"]["pruning_triggered"] in (True, False)
    assert set(rec["comparison"]) >= {
        "input_tokens_saved",
        "input_token_reduction_percent",
        "estimated_cost_saved",
        "cost_reduction_percent",
        "latency_delta_seconds",
    }


def test_cumulative_savings_positive():
    sm, session, records = _run(turns=10)
    assert len(session.turns) == 10
    # Baseline carries full history -> more cumulative input tokens than pruned.
    assert records[-1]["comparison"]["input_tokens_saved"] > 0
    assert session.baseline_stats.total_input_tokens > session.pruned_stats.total_input_tokens


def test_turn_counter_increments():
    _, session, _ = _run(turns=3)
    assert session.turn_count == 3

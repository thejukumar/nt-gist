"""Reporting: session-log dict + Markdown report structure."""

from conftest import FakeLLM, FakeTavily

from support_context_budget_lab.agents.baseline_agent import BaselineAgent
from support_context_budget_lab.agents.pruned_agent import PrunedAgent
from support_context_budget_lab.pruning.context_pruner import ContextPruner
from support_context_budget_lab.pruning.retention_policy import RetentionPolicy
from support_context_budget_lab.reporting.json_logger import build_session_log
from support_context_budget_lab.reporting.markdown_report import build_markdown_report
from support_context_budget_lab.session_manager import SessionManager


def _factory(session):
    pruner = ContextPruner(session.prune_every, session.recent_turns_to_keep)
    return (
        BaselineAgent(FakeLLM(), FakeTavily(), input_cost_per_1m=0.6, output_cost_per_1m=2.4),
        PrunedAgent(
            FakeLLM(), FakeTavily(), pruner, session.retention_policy,
            input_cost_per_1m=0.6, output_cost_per_1m=2.4,
        ),
    )


def _session_with_turns(n=12):
    sm = SessionManager(agent_factory=_factory)
    session = sm.create(RetentionPolicy(), prune_every=2, recent_turns_to_keep=2)
    for i in range(1, n + 1):
        sm.run_turn(
            session,
            f"Turn {i}: the customer needs a detailed, substantial support reply. " * 3,
        )
    return session


def test_session_log_structure():
    log = build_session_log(_session_with_turns(12))
    assert log["provider"] == "Nebius"
    assert log["tool_provider"] == "Tavily"
    assert len(log["turns"]) == 12
    summary = log["summary"]
    assert summary["turns"] == 12
    assert summary["baseline_total_input_tokens"] >= summary["pruned_total_input_tokens"]
    assert {"input_token_reduction_percent", "estimated_cost_savings"} <= set(summary)


def test_markdown_report_sections():
    report = build_markdown_report(_session_with_turns(12))
    for heading in [
        "# Support Context Budget Lab Report",
        "## Customer Scenario",
        "## Results Summary",
        "## Turn-by-Turn Metrics",
        "## Business Projection",
        "## Limitations",
    ]:
        assert heading in report
    # Turn-by-turn table has a row per turn.
    assert report.count("\n| 1 |") == 1

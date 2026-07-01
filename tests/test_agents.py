"""Agent behavior: baseline context grows, pruned stays lean, events fire."""

from conftest import FakeLLM, FakeTavily

from support_context_budget_lab.agents.baseline_agent import BaselineAgent
from support_context_budget_lab.agents.pruned_agent import PrunedAgent
from support_context_budget_lab.pruning.context_pruner import ContextPruner
from support_context_budget_lab.pruning.retention_policy import RetentionPolicy


# Neutral messages (no search keywords), realistically long so baseline history
# growth eventually dominates the pruned agent's fixed context overhead.
_MESSAGES = [
    f"Turn {i}: the customer reports a detailed issue that needs careful, "
    "thorough support handling and a substantial reply every single time. " * 3
    for i in range(1, 11)
]


def test_baseline_input_tokens_exceed_pruned_over_time():
    baseline = BaselineAgent(FakeLLM(), FakeTavily())
    pruner = ContextPruner(prune_every=2, recent_turns_to_keep=2)
    pruned = PrunedAgent(FakeLLM(), FakeTavily(), pruner, RetentionPolicy())

    baseline_inputs, pruned_inputs = [], []
    for turn, msg in enumerate(_MESSAGES, start=1):
        _, b_metrics = baseline.run_turn(msg, turn)
        _, p_metrics, _ = pruned.run_turn(msg, turn)
        baseline_inputs.append(b_metrics.input_tokens)
        pruned_inputs.append(p_metrics.input_tokens)

    # Early on they are comparable; by the last turn baseline carries far more.
    assert baseline_inputs[-1] > pruned_inputs[-1]
    # Pruned input tokens should stay bounded (compact window), baseline should grow.
    assert baseline_inputs[-1] > baseline_inputs[0]
    assert max(pruned_inputs) < baseline_inputs[-1]


def test_pruning_event_fires_on_even_turns_with_history():
    pruner = ContextPruner(prune_every=2, recent_turns_to_keep=2)
    pruned = PrunedAgent(FakeLLM(), FakeTavily(), pruner, RetentionPolicy())

    events = {}
    for turn, msg in enumerate(_MESSAGES, start=1):
        _, _, event = pruned.run_turn(msg, turn)
        events[turn] = event

    # No compression possible while everything fits the recent window.
    assert events[1] is None
    # Once history exceeds the window, events fire on prune-cadence (even) turns.
    assert events[4] is not None
    assert events[6] is not None
    assert events[5] is None  # odd turn -> no event


def test_search_triggers_tool_call_and_ledger():
    records = [SourceRecordStub("Cause of drops", "http://x", "congestion")]
    tavily = FakeTavily(records=records)
    pruner = ContextPruner(prune_every=2, recent_turns_to_keep=2)
    pruned = PrunedAgent(FakeLLM(), tavily, pruner, RetentionPolicy())

    _, metrics, _ = pruned.run_turn("please research common causes of this", turn=1)
    assert metrics.tool_calls == 1
    assert len(pruned.ledger.items) == 1


# Local stub matching SourceRecord shape (avoids importing dataclass fields here).
class SourceRecordStub:
    def __init__(self, title, url, snippet):
        self.title = title
        self.url = url
        self.snippet = snippet

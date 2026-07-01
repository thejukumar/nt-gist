"""ContextPruner: trigger cadence + compact-context construction."""

from support_context_budget_lab.pruning.context_pruner import ContextPruner
from support_context_budget_lab.pruning.evidence_ledger import EvidenceLedger
from support_context_budget_lab.pruning.retention_policy import RetentionPolicy
from support_context_budget_lab.pruning.support_memory import SupportMemory


def _history(num_pairs: int) -> list[dict]:
    """Build `num_pairs` user/assistant exchanges."""
    msgs = []
    for i in range(num_pairs):
        msgs.append({"role": "user", "content": f"user message {i}"})
        msgs.append({"role": "assistant", "content": f"assistant reply {i}"})
    return msgs


def test_should_prune_every_two_turns():
    pruner = ContextPruner(prune_every=2, recent_turns_to_keep=2)
    assert [pruner.should_prune(t) for t in range(1, 7)] == [
        False, True, False, True, False, True
    ]


def test_prune_keeps_recent_and_rebuilds_system():
    pruner = ContextPruner(prune_every=2, recent_turns_to_keep=2)
    history = _history(4)  # 8 messages
    result = pruner.prune(
        history,
        turn=6,
        policy=RetentionPolicy(),
        memory=SupportMemory(),
        ledger=EvidenceLedger(),
        system_prompt="SYSTEM",
    )
    # 1 rebuilt system message + last (2*2)=4 conversation messages.
    assert result.messages[0]["role"] == "system"
    assert "SYSTEM" in result.messages[0]["content"]
    assert "Retention policy" in result.messages[0]["content"]
    assert len(result.messages) == 1 + 4
    # Older messages (8 - 4 = 4) were compressed -> event emitted on a prune turn.
    assert result.event is not None
    assert result.event.compressed_messages == 4


def test_prune_captures_first_user_message_as_issue():
    pruner = ContextPruner(prune_every=2, recent_turns_to_keep=2)
    memory = SupportMemory()
    pruner.prune(
        _history(4),
        turn=6,
        policy=RetentionPolicy(),
        memory=memory,
        ledger=EvidenceLedger(),
    )
    assert memory.customer_issue == "user message 0"


def test_no_event_on_non_prune_turn():
    pruner = ContextPruner(prune_every=2, recent_turns_to_keep=2)
    result = pruner.prune(
        _history(4),
        turn=5,  # odd turn -> no pruning event
        policy=RetentionPolicy(),
        memory=SupportMemory(),
        ledger=EvidenceLedger(),
    )
    assert result.event is None
    # Still compacts to system + recent window.
    assert len(result.messages) == 1 + 4


def test_no_event_when_history_within_window():
    pruner = ContextPruner(prune_every=2, recent_turns_to_keep=2)
    result = pruner.prune(
        _history(1),  # only 2 messages, within the keep window
        turn=2,
        policy=RetentionPolicy(),
        memory=SupportMemory(),
        ledger=EvidenceLedger(),
    )
    assert result.event is None

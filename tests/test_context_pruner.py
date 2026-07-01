"""ContextPruner trigger cadence (prune-every-2 implemented in scaffold)."""

import pytest

from support_context_budget_lab.pruning.context_pruner import ContextPruner


def test_should_prune_every_two_turns():
    pruner = ContextPruner(prune_every=2, recent_turns_to_keep=2)
    assert [pruner.should_prune(t) for t in range(1, 7)] == [
        False,  # turn 1
        True,   # turn 2
        False,  # turn 3
        True,   # turn 4
        False,  # turn 5
        True,   # turn 6
    ]


@pytest.mark.skip(reason="prune() lands in feat/pruning-engine")
def test_prune_keeps_recent_and_preserves_memory():
    ...

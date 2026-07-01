"""RetentionPolicy defaults + custom rules (dataclass implemented in scaffold)."""

import pytest

from support_context_budget_lab.pruning.retention_policy import RetentionPolicy


def test_defaults_all_enabled():
    policy = RetentionPolicy()
    flags = [v for k, v in vars(policy).items() if k.startswith("preserve_")]
    assert all(flags)
    assert policy.custom_rules == []


def test_custom_rules_accepted():
    policy = RetentionPolicy(custom_rules=["always keep the ticket ID"])
    assert policy.custom_rules == ["always keep the ticket ID"]


@pytest.mark.skip(reason="to_prompt_block lands in feat/pruning-engine")
def test_serializes_to_prompt_block():
    RetentionPolicy().to_prompt_block()

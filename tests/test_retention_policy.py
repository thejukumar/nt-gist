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


def test_serializes_to_prompt_block():
    block = RetentionPolicy(custom_rules=["always keep the ticket ID"]).to_prompt_block()
    assert "Retention policy" in block
    assert "Customer issue" in block
    assert "always keep the ticket ID" in block


def test_disabled_flag_omitted_from_block():
    block = RetentionPolicy(preserve_source_snippets=False).to_prompt_block()
    assert "Tavily source snippets" not in block
    assert "Customer issue" in block

"""Token usage: local estimator + usage_metadata extraction."""

from support_context_budget_lab.metrics.token_usage import (
    estimate_message_tokens,
    estimate_tokens,
    extract_usage,
)


class _FakeResponse:
    def __init__(self, usage_metadata):
        self.usage_metadata = usage_metadata


def test_estimate_tokens_nonempty():
    assert estimate_tokens("hello world") > 0


def test_estimate_tokens_empty_is_zero():
    assert estimate_tokens("") == 0


def test_estimate_message_tokens_sums():
    messages = [
        {"role": "system", "content": "You are a support agent."},
        {"role": "user", "content": "My internet is down."},
    ]
    assert estimate_message_tokens(messages) > 0


def test_extract_usage_primary_path():
    resp = _FakeResponse({"input_tokens": 120, "output_tokens": 42})
    assert extract_usage(resp) == (120, 42)


def test_extract_usage_missing_returns_none():
    assert extract_usage(_FakeResponse(None)) is None
    assert extract_usage(object()) is None

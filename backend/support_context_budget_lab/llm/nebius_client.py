"""Nebius chat client wrapper (ChatNebius via langchain-nebius).

Wraps the same model the starter uses, but returns response text *and* a
TokenUsage record. Token counting strategy:
  primary  -> read `usage_metadata` from the LangChain/Nebius response
  fallback -> local tokenizer estimate (see metrics.token_usage), flagged
              `estimated=True`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class LLMResult:
    """A single model call's output plus measured usage."""

    text: str
    input_tokens: int
    output_tokens: int
    latency_seconds: float
    estimated: bool  # True if tokens came from the fallback estimator


class NebiusClient:
    """Thin wrapper around ChatNebius with usage + latency capture."""

    def __init__(self, model: str, api_key: str) -> None:
        self.model = model
        self._api_key = api_key
        # TODO(feat/providers-metrics): instantiate ChatNebius(model=..., ...)

    def complete(self, messages: list[dict[str, Any]]) -> LLMResult:
        """Send messages, measure latency, extract usage (or estimate).

        TODO(feat/providers-metrics):
          - time the call
          - read response.usage_metadata (input/output tokens) when present
          - else fall back to metrics.token_usage estimator (estimated=True)
        """
        raise NotImplementedError

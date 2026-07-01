"""Token usage extraction with a local-tokenizer fallback.

Primary path: read `usage_metadata` from the LangChain/Nebius response.
Fallback: a local tiktoken estimate (an approximation for non-OpenAI models).
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any


@lru_cache(maxsize=1)
def _encoder():
    import tiktoken

    # cl100k_base is a reasonable general-purpose approximation; the model here
    # (moonshotai/Kimi-K2.6) is not OpenAI, so treat fallback counts as estimates.
    return tiktoken.get_encoding("cl100k_base")


def estimate_tokens(text: str) -> int:
    """Estimate the token count of a string with a local tokenizer."""
    if not text:
        return 0
    return len(_encoder().encode(text))


def estimate_message_tokens(messages: list[dict[str, Any]]) -> int:
    """Estimate prompt tokens across a list of {'role','content'} messages."""
    return sum(estimate_tokens(str(m.get("content", ""))) for m in messages)


def extract_usage(response: Any) -> tuple[int, int] | None:
    """Return (input_tokens, output_tokens) from a LangChain response.

    Returns None when provider metadata is unavailable so the caller can fall
    back to the local estimator.
    """
    usage = getattr(response, "usage_metadata", None)
    if isinstance(usage, dict):
        input_tokens = usage.get("input_tokens")
        output_tokens = usage.get("output_tokens")
        if input_tokens is not None and output_tokens is not None:
            return int(input_tokens), int(output_tokens)
    return None

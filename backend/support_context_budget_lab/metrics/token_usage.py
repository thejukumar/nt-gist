"""Token usage extraction with a local-tokenizer fallback.

Primary path lives in the Nebius client (reads `usage_metadata`). This module
provides the *fallback* estimator used when provider metadata is unavailable.
"""

from __future__ import annotations

from typing import Any


def estimate_tokens(text: str) -> int:
    """Estimate token count for a string using a local tokenizer.

    TODO(feat/providers-metrics): use tiktoken (cl100k_base) as an approximation
    and document that it is an estimate for non-OpenAI models.
    """
    raise NotImplementedError


def extract_usage(response: Any) -> tuple[int, int] | None:
    """Return (input_tokens, output_tokens) from a LangChain response.

    TODO(feat/providers-metrics): read response.usage_metadata; return None if
    absent so the caller can fall back to estimate_tokens().
    """
    raise NotImplementedError

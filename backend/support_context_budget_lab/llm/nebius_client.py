"""Nebius chat client wrapper (ChatNebius via langchain-nebius).

Wraps the same model the starter uses, returning response text plus a measured
usage record. Token counting:
  primary  -> read `usage_metadata` from the response
  fallback -> local tiktoken estimate (LLMResult.estimated = True)

langchain is imported lazily inside methods so importing this module (and the
`agents` package) does not require langchain to be installed.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from ..metrics.latency import measure_latency
from ..metrics.token_usage import estimate_message_tokens, estimate_tokens, extract_usage


@dataclass
class LLMResult:
    """A single model call's output plus measured usage."""

    text: str
    input_tokens: int
    output_tokens: int
    latency_seconds: float
    estimated: bool  # True if tokens came from the fallback estimator


def _to_lc_messages(messages: list[dict[str, Any]]):
    """Convert {'role','content'} dicts to LangChain message objects."""
    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

    role_map = {"system": SystemMessage, "user": HumanMessage, "assistant": AIMessage}
    return [
        role_map.get(m.get("role", "user"), HumanMessage)(content=m.get("content", ""))
        for m in messages
    ]


def _extract_text(response: Any) -> str:
    """Pull plain text out of a LangChain message/content (str or block list)."""
    content = getattr(response, "content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "".join(parts)
    return str(content)


class NebiusClient:
    """Thin wrapper around ChatNebius with usage + latency capture."""

    def __init__(self, model: str, api_key: str, temperature: float = 0.0) -> None:
        from langchain_nebius import ChatNebius

        self.model = model
        if api_key:
            os.environ.setdefault("NEBIUS_API_KEY", api_key)
        # temperature=0 keeps the A/B comparison as deterministic as possible.
        self._chat = ChatNebius(model=model, temperature=temperature)

    def complete(self, messages: list[dict[str, Any]]) -> LLMResult:
        """Send messages, measure latency, extract usage (or estimate)."""
        lc_messages = _to_lc_messages(messages)
        with measure_latency() as elapsed:
            response = self._chat.invoke(lc_messages)

        text = _extract_text(response)
        usage = extract_usage(response)
        if usage is not None:
            input_tokens, output_tokens = usage
            estimated = False
        else:
            input_tokens = estimate_message_tokens(messages)
            output_tokens = estimate_tokens(text)
            estimated = True

        return LLMResult(
            text=text,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_seconds=elapsed[0],
            estimated=estimated,
        )

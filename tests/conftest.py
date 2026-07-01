"""Shared test fakes for agent/orchestration tests (no langchain / no keys)."""

from support_context_budget_lab.llm.nebius_client import LLMResult
from support_context_budget_lab.tools.tavily_client import SourceRecord


class FakeLLM:
    """Deterministic LLM: input tokens = total chars of the sent messages."""

    def complete(self, messages):
        input_tokens = sum(len(str(m.get("content", ""))) for m in messages)
        return LLMResult(
            text="ok",
            input_tokens=input_tokens,
            output_tokens=3,
            latency_seconds=0.01,
            estimated=True,
        )


class FakeTavily:
    """Tavily stub returning canned sources; tracks call count."""

    def __init__(self, records=None):
        self.tool_calls = 0
        self._records = records or []

    def search(self, query):
        self.tool_calls += 1
        return list(self._records)

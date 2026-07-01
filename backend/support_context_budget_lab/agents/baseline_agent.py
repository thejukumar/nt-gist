"""Baseline agent — keeps the full conversation history every turn."""

from __future__ import annotations

from typing import Any

from ..llm.nebius_client import NebiusClient
from ..metrics.metrics_models import TurnMetrics
from ..tools.tavily_client import TavilyClient


class BaselineAgent:
    """Full-history support agent (the naive, ever-growing-context approach)."""

    def __init__(self, llm: NebiusClient, tavily: TavilyClient) -> None:
        self.llm = llm
        self.tavily = tavily
        self.history: list[dict[str, Any]] = []

    def run_turn(self, user_message: str, turn: int) -> tuple[str, TurnMetrics]:
        """Answer using the full history; return response text + real metrics.

        TODO(feat/agents-ab-endpoint): append user msg, send full history to
        Nebius (with Tavily as a tool), capture TurnMetrics from the call.
        """
        raise NotImplementedError

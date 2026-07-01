"""In-memory session store + per-session A/B orchestration.

A session holds both agents, their config, cumulative stats, and turn records.
Agent construction is injected (agent_factory) so the orchestration is testable
without langchain or API keys.
"""

from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Callable

from .agents.baseline_agent import BaselineAgent
from .agents.pruned_agent import PrunedAgent
from .config import Settings, get_settings
from .metrics.metrics_models import TurnMetrics
from .metrics.session_stats import CumulativeStats, comparison
from .pruning.context_pruner import ContextPruner
from .pruning.retention_policy import RetentionPolicy

# (baseline_agent, pruned_agent)
AgentFactory = Callable[["Session"], tuple[Any, Any]]


@dataclass
class Session:
    """One comparison session (a single conversation run through both agents)."""

    session_id: str
    retention_policy: RetentionPolicy
    prune_every: int
    recent_turns_to_keep: int
    baseline_agent: Any = None
    pruned_agent: Any = None
    baseline_stats: CumulativeStats = field(default_factory=CumulativeStats)
    pruned_stats: CumulativeStats = field(default_factory=CumulativeStats)
    turns: list[dict] = field(default_factory=list)
    turn_count: int = 0


def _metrics_to_dict(m: TurnMetrics) -> dict:
    return {
        "input_tokens": m.input_tokens,
        "output_tokens": m.output_tokens,
        "total_tokens": m.total_tokens,
        "latency_seconds": m.latency_seconds,
        "estimated_cost": m.estimated_cost,
        "tool_calls": m.tool_calls,
        "estimated": m.estimated,
    }


def default_agent_factory(session: Session, settings: Settings | None = None):
    """Build real Nebius/Tavily-backed agents from settings (needs keys)."""
    settings = settings or get_settings()
    settings.require_keys()

    # Imported here so importing this module never requires langchain.
    from .llm.nebius_client import NebiusClient
    from .tools.tavily_client import TavilyClient

    llm = NebiusClient(model=settings.nebius_model, api_key=settings.nebius_api_key)
    pruner = ContextPruner(
        prune_every=session.prune_every,
        recent_turns_to_keep=session.recent_turns_to_keep,
    )
    pricing = dict(
        input_cost_per_1m=settings.input_cost_per_1m,
        output_cost_per_1m=settings.output_cost_per_1m,
    )
    baseline = BaselineAgent(llm, TavilyClient(settings.tavily_api_key), **pricing)
    pruned = PrunedAgent(
        llm, TavilyClient(settings.tavily_api_key), pruner, session.retention_policy, **pricing
    )
    return baseline, pruned


class SessionManager:
    """Creates and looks up in-memory sessions; runs A/B turns."""

    def __init__(self, agent_factory: AgentFactory | None = None) -> None:
        self._sessions: dict[str, Session] = {}
        self._agent_factory = agent_factory or default_agent_factory

    def create(
        self,
        retention_policy: RetentionPolicy,
        prune_every: int,
        recent_turns_to_keep: int,
    ) -> Session:
        session = Session(
            session_id=f"session_{uuid.uuid4().hex[:8]}",
            retention_policy=retention_policy,
            prune_every=prune_every,
            recent_turns_to_keep=recent_turns_to_keep,
        )
        session.baseline_agent, session.pruned_agent = self._agent_factory(session)
        self._sessions[session.session_id] = session
        return session

    def get(self, session_id: str) -> Session | None:
        return self._sessions.get(session_id)

    def run_turn(self, session: Session, message: str) -> dict:
        """Run one prompt through both agents; accumulate stats; build response."""
        session.turn_count += 1
        turn = session.turn_count

        baseline_text, baseline_metrics = session.baseline_agent.run_turn(message, turn)
        pruned_text, pruned_metrics, event = session.pruned_agent.run_turn(message, turn)

        session.baseline_stats.add(baseline_metrics)
        session.pruned_stats.add(pruned_metrics)

        record = {
            "turn": turn,
            "baseline": {
                "response": baseline_text,
                "metrics": _metrics_to_dict(baseline_metrics),
            },
            "pruned": {
                "response": pruned_text,
                "metrics": _metrics_to_dict(pruned_metrics),
                "pruning_triggered": event is not None,
                "pruning_event": asdict(event) if event is not None else None,
            },
            "comparison": comparison(session.baseline_stats, session.pruned_stats),
        }
        session.turns.append(record)
        return record

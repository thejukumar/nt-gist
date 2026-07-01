"""Context pruner — builds the compact context sent to the pruned agent.

Decoupled from metrics: this module returns a pruned message list and updated
state only. It never measures tokens/latency/cost — that is the metrics layer's
job (see support_context_budget_lab.metrics).

Strategy (deterministic, no extra LLM call):
- The compact context each turn = one synthesized system message (agent persona
  + retention policy + support memory + evidence ledger) followed by the last
  `recent_turns_to_keep * 2` conversation messages verbatim.
- Older messages are dropped from the prompt (that is the token saving); their
  essence is retained via the support memory + evidence ledger.
- A PruningEvent is emitted on trigger turns (every `prune_every`) when there
  are older messages beyond the recent window.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .evidence_ledger import EvidenceLedger
from .retention_policy import RetentionPolicy
from .support_memory import SupportMemory

Message = dict[str, Any]  # {"role": ..., "content": ...}


@dataclass
class PruningEvent:
    """A record of one pruning pass, for the UI timeline + report."""

    turn: int
    compressed_messages: int
    preserved: list[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class PruneResult:
    """Output of a pruning pass."""

    messages: list[Message]
    memory: SupportMemory
    ledger: EvidenceLedger
    event: PruningEvent | None  # None when no pruning happened this turn


class ContextPruner:
    """Retention-aware pruner: keep recent turns + memory + evidence ledger.

    Default trigger: prune every `prune_every` turns, keep the last
    `recent_turns_to_keep` turns verbatim.
    """

    def __init__(self, prune_every: int = 2, recent_turns_to_keep: int = 2) -> None:
        self.prune_every = prune_every
        self.recent_turns_to_keep = recent_turns_to_keep

    def should_prune(self, turn: int) -> bool:
        """Whether pruning fires on this turn."""
        return turn > 0 and turn % self.prune_every == 0

    def _build_system_message(
        self,
        system_prompt: str,
        policy: RetentionPolicy,
        memory: SupportMemory,
        ledger: EvidenceLedger,
    ) -> Message:
        content = "\n\n".join(
            [
                system_prompt.strip(),
                policy.to_prompt_block(),
                memory.to_prompt_block(),
                ledger.to_prompt_block(),
            ]
        )
        return {"role": "system", "content": content}

    def _capture_memory(self, conversation: list[Message], memory: SupportMemory) -> None:
        """Lightweight, deterministic memory capture.

        MVP heuristic: the first user message is the customer's core issue. (A
        richer LLM-based extractor is a documented future enhancement.)
        """
        if memory.customer_issue is None:
            for m in conversation:
                if m.get("role") == "user" and m.get("content"):
                    memory.customer_issue = str(m["content"]).strip()
                    break

    def prune(
        self,
        history: list[Message],
        *,
        turn: int,
        policy: RetentionPolicy,
        memory: SupportMemory,
        ledger: EvidenceLedger,
        system_prompt: str = "",
    ) -> PruneResult:
        """Produce the compact message list for the pruned agent."""
        # Conversation = non-system messages (system is rebuilt from state).
        conversation = [m for m in history if m.get("role") != "system"]

        self._capture_memory(conversation, memory)

        keep_count = max(self.recent_turns_to_keep * 2, 1)
        recent = conversation[-keep_count:]
        older = conversation[:-keep_count]

        system_message = self._build_system_message(system_prompt, policy, memory, ledger)
        messages: list[Message] = [system_message, *recent]

        event: PruningEvent | None = None
        if self.should_prune(turn) and older:
            preserved: list[str] = []
            if memory.customer_issue:
                preserved.append("customer issue")
            if not memory.is_empty():
                preserved.append("support memory")
            if ledger.items:
                preserved.append(f"{len(ledger.items)} evidence source(s)")
            event = PruningEvent(
                turn=turn,
                compressed_messages=len(older),
                preserved=preserved,
                notes=f"Kept last {len(recent)} message(s); compressed {len(older)} older message(s).",
            )

        return PruneResult(messages=messages, memory=memory, ledger=ledger, event=event)

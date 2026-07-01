"""Support memory — durable customer-support state that survives pruning."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SupportMemory:
    """Compact, structured record of the support case.

    Carried forward across turns so the pruned agent retains continuity even
    after older raw messages are compressed away.
    """

    customer_issue: str | None = None
    product_or_service: str | None = None
    account_or_plan: str | None = None
    troubleshooting_steps: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    unresolved_questions: list[str] = field(default_factory=list)
    prior_decisions: list[str] = field(default_factory=list)
    escalation_status: str | None = None

    def to_prompt_block(self) -> str:
        """Render the memory as a prompt-ready summary block.

        TODO(feat/pruning-engine): format non-empty fields into text.
        """
        raise NotImplementedError

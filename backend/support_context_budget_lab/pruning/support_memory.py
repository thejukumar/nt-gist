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

    def is_empty(self) -> bool:
        scalars = [
            self.customer_issue,
            self.product_or_service,
            self.account_or_plan,
            self.escalation_status,
        ]
        lists = [
            self.troubleshooting_steps,
            self.constraints,
            self.unresolved_questions,
            self.prior_decisions,
        ]
        return not any(scalars) and not any(lists)

    def to_prompt_block(self) -> str:
        """Render non-empty memory fields into a prompt-ready block."""
        if self.is_empty():
            return "Support memory: (none captured yet)"

        lines = ["Support memory:"]
        if self.customer_issue:
            lines.append(f"- Customer issue: {self.customer_issue}")
        if self.product_or_service:
            lines.append(f"- Product/service: {self.product_or_service}")
        if self.account_or_plan:
            lines.append(f"- Account/plan: {self.account_or_plan}")
        if self.troubleshooting_steps:
            lines.append("- Troubleshooting tried: " + "; ".join(self.troubleshooting_steps))
        if self.constraints:
            lines.append("- Constraints: " + "; ".join(self.constraints))
        if self.unresolved_questions:
            lines.append("- Open questions: " + "; ".join(self.unresolved_questions))
        if self.prior_decisions:
            lines.append("- Prior decisions: " + "; ".join(self.prior_decisions))
        if self.escalation_status:
            lines.append(f"- Escalation status: {self.escalation_status}")
        return "\n".join(lines)

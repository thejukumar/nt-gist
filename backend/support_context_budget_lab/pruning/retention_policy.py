"""Retention policy — what the pruned agent must always keep."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RetentionPolicy:
    """Flags for the support context the pruned agent must never drop.

    Populated from defaults or from the UI's retention modal. `custom_rules`
    holds free-text rules the user adds.
    """

    preserve_customer_issue: bool = True
    preserve_product_or_service: bool = True
    preserve_account_constraints: bool = True
    preserve_troubleshooting_steps: bool = True
    preserve_unresolved_questions: bool = True
    preserve_prior_decisions: bool = True
    preserve_escalation_status: bool = True
    preserve_source_urls: bool = True
    preserve_source_snippets: bool = True
    custom_rules: list[str] = field(default_factory=list)

    _LABELS = {
        "preserve_customer_issue": "Customer issue",
        "preserve_product_or_service": "Product or service",
        "preserve_account_constraints": "Account / plan constraints",
        "preserve_troubleshooting_steps": "Troubleshooting steps already tried",
        "preserve_unresolved_questions": "Open questions",
        "preserve_prior_decisions": "Prior decisions",
        "preserve_escalation_status": "Escalation status",
        "preserve_source_urls": "Tavily source URLs",
        "preserve_source_snippets": "Tavily source snippets",
    }

    def enabled_labels(self) -> list[str]:
        """Human labels for the enabled retention flags (+ custom rules)."""
        labels = [
            label for attr, label in self._LABELS.items() if getattr(self, attr)
        ]
        return labels + list(self.custom_rules)

    def to_prompt_block(self) -> str:
        """Serialize enabled rules into a prompt-ready retention block."""
        lines = ["Retention policy — always preserve:"]
        lines += [f"- {label}" for label in self.enabled_labels()]
        return "\n".join(lines)

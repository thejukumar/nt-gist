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

    def to_prompt_block(self) -> str:
        """Serialize enabled rules into a prompt-ready retention block.

        TODO(feat/pruning-engine): render enabled flags + custom rules as text.
        """
        raise NotImplementedError

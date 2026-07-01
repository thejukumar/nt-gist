"""API request/response DTOs (mirrors docs/api-contract).

Kept separate from domain models. Metric field names match the frontend's
`lib/types.ts` so the typed client maps 1:1.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class RetentionPolicyDTO(BaseModel):
    preserve_customer_issue: bool = True
    preserve_product_or_service: bool = True
    preserve_account_constraints: bool = True
    preserve_troubleshooting_steps: bool = True
    preserve_unresolved_questions: bool = True
    preserve_prior_decisions: bool = True
    preserve_escalation_status: bool = True
    preserve_source_urls: bool = True
    preserve_source_snippets: bool = True
    custom_rules: list[str] = Field(default_factory=list)


class SessionStartRequest(BaseModel):
    retention_policy: RetentionPolicyDTO | None = None
    prune_every: int = 2
    recent_turns_to_keep: int = 2


class SessionStartResponse(BaseModel):
    session_id: str
    status: str = "started"


class ChatTurnRequest(BaseModel):
    session_id: str
    message: str


class TurnMetricsDTO(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int
    latency_seconds: float
    estimated_cost: float
    tool_calls: int
    estimated: bool = False


class AgentTurnDTO(BaseModel):
    response: str
    metrics: TurnMetricsDTO


class PrunedTurnDTO(AgentTurnDTO):
    pruning_triggered: bool = False
    pruning_event: dict | None = None


class ComparisonDTO(BaseModel):
    input_tokens_saved: int
    input_token_reduction_percent: float
    estimated_cost_saved: float
    cost_reduction_percent: float
    latency_delta_seconds: float


class ChatTurnResponse(BaseModel):
    turn: int
    baseline: AgentTurnDTO
    pruned: PrunedTurnDTO
    comparison: ComparisonDTO


class DemoRunRequest(BaseModel):
    session_id: str
    scenario: str = "telecom_support"
    sleep_seconds: float = 2.0


class DemoRunResponse(BaseModel):
    scenario: str
    description: str
    prompts: list[str]

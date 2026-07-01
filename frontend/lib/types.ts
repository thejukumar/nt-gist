// Shared API types — mirror backend/support_context_budget_lab/api/schemas.py.

export interface TurnMetrics {
  input_tokens: number;
  output_tokens: number;
  total_tokens: number;
  latency_seconds: number;
  estimated_cost: number;
  tool_calls: number;
  estimated: boolean;
}

export interface AgentTurn {
  response: string;
  metrics: TurnMetrics;
}

export interface PrunedTurn extends AgentTurn {
  pruning_triggered: boolean;
  pruning_event: Record<string, unknown> | null;
}

export interface Comparison {
  input_tokens_saved: number;
  input_token_reduction_percent: number;
  estimated_cost_saved: number;
  cost_reduction_percent: number;
  latency_delta_seconds: number;
}

export interface ChatTurnResponse {
  turn: number;
  baseline: AgentTurn;
  pruned: PrunedTurn;
  comparison: Comparison;
}

export interface RetentionPolicy {
  preserve_customer_issue: boolean;
  preserve_product_or_service: boolean;
  preserve_account_constraints: boolean;
  preserve_troubleshooting_steps: boolean;
  preserve_unresolved_questions: boolean;
  preserve_prior_decisions: boolean;
  preserve_escalation_status: boolean;
  preserve_source_urls: boolean;
  preserve_source_snippets: boolean;
  custom_rules: string[];
}

export interface SessionStartResponse {
  session_id: string;
  status: string;
}

export interface DemoRunResponse {
  scenario: string;
  description: string;
  prompts: string[];
}

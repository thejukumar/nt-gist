// Display formatters + cumulative aggregation for metrics.

import type { AgentCumulative, ChatTurnResponse } from "./types";

export const formatTokens = (n: number): string => n.toLocaleString("en-US");

export const formatCost = (usd: number): string =>
  `$${usd.toFixed(usd < 0.01 ? 5 : 4)}`;

export const formatLatency = (seconds: number): string => `${seconds.toFixed(1)}s`;

export const formatPercent = (fraction: number): string =>
  `${(fraction * 100).toFixed(1)}%`;

const emptyCumulative = (): AgentCumulative => ({
  inputTokens: 0,
  outputTokens: 0,
  totalTokens: 0,
  cost: 0,
  avgLatency: 0,
  toolCalls: 0,
  turns: 0,
});

/** Sum per-turn metrics into cumulative totals for each agent. */
export function computeCumulative(turns: ChatTurnResponse[]): {
  baseline: AgentCumulative;
  pruned: AgentCumulative;
} {
  const baseline = emptyCumulative();
  const pruned = emptyCumulative();
  let baselineLatency = 0;
  let prunedLatency = 0;

  for (const t of turns) {
    baseline.inputTokens += t.baseline.metrics.input_tokens;
    baseline.outputTokens += t.baseline.metrics.output_tokens;
    baseline.totalTokens += t.baseline.metrics.total_tokens;
    baseline.cost += t.baseline.metrics.estimated_cost;
    baseline.toolCalls += t.baseline.metrics.tool_calls;
    baselineLatency += t.baseline.metrics.latency_seconds;

    pruned.inputTokens += t.pruned.metrics.input_tokens;
    pruned.outputTokens += t.pruned.metrics.output_tokens;
    pruned.totalTokens += t.pruned.metrics.total_tokens;
    pruned.cost += t.pruned.metrics.estimated_cost;
    pruned.toolCalls += t.pruned.metrics.tool_calls;
    prunedLatency += t.pruned.metrics.latency_seconds;
  }

  baseline.turns = pruned.turns = turns.length;
  baseline.avgLatency = turns.length ? baselineLatency / turns.length : 0;
  pruned.avgLatency = turns.length ? prunedLatency / turns.length : 0;
  return { baseline, pruned };
}

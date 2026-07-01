// Per-agent metrics card (sits ABOVE that agent's response). Stats are
// bifurcated by agent (doc §9). TODO(feat/frontend): render live metrics.

export type AgentStatusCardProps = {
  agentType: "baseline" | "pruned";
  title: string;
  subtitle: string;
  contextMode: string;
  currentTurnMetrics: {
    inputTokens: number;
    outputTokens: number;
    totalTokens: number;
    latencySeconds: number;
    estimatedCost: number;
    toolCalls: number;
  };
  cumulativeMetrics: {
    totalInputTokens: number;
    totalOutputTokens: number;
    totalTokens: number;
    totalCost: number;
    averageLatency: number;
  };
  pruning?: {
    enabled: boolean;
    triggeredThisTurn: boolean;
    totalEvents: number;
    tokensSavedPercent?: number;
    costSavedPercent?: number;
  };
};

export function AgentStatusCard(props: AgentStatusCardProps) {
  const accent = props.agentType === "baseline" ? "text-baseline" : "text-pruned";
  return (
    <div className="glass p-4">
      <div className={`text-sm font-medium ${accent}`}>{props.title}</div>
      <div className="text-xs text-white/50">{props.subtitle}</div>
      {/* TODO(feat/frontend): current-turn + cumulative metric rows. */}
    </div>
  );
}

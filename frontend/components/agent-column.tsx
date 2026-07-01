"use client";

import { AgentResponsePanel, type ChatMessage } from "./agent-response-panel";
import { AgentStatusCard } from "./agent-status-card";
import type { AgentCumulative, TurnMetrics } from "@/lib/types";

// Reusable column: status card on top, response panel below.
export function AgentColumn({
  agentType,
  current,
  cumulative,
  messages,
  busy,
  pruning,
}: {
  agentType: "baseline" | "pruned";
  current: TurnMetrics | null;
  cumulative: AgentCumulative;
  messages: ChatMessage[];
  busy: boolean;
  pruning?: { events: number; triggeredThisTurn: boolean };
}) {
  const isBaseline = agentType === "baseline";
  return (
    <div className="flex flex-col gap-3">
      <AgentStatusCard
        agentType={agentType}
        title={isBaseline ? "Baseline Agent" : "Pruned Agent"}
        subtitle={isBaseline ? "Full-history context" : "Retention-aware context"}
        contextMode={isBaseline ? "Full history" : "Pruned memory"}
        current={current}
        cumulative={cumulative}
        pruning={pruning}
      />
      <AgentResponsePanel agentType={agentType} messages={messages} busy={busy} />
    </div>
  );
}

"use client";

import { AgentResponsePanel, type ChatMessage } from "./agent-response-panel";
import { AgentStatusCard } from "./agent-status-card";
import type { AgentCumulative, TurnMetrics } from "@/lib/types";

// One framed section per agent: header → contained stats → response area.
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
  const accent = isBaseline ? "text-baseline" : "text-pruned";

  return (
    <section className="glass flex flex-col overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-white/10 px-4 py-3">
        <div>
          <h2 className={`text-sm font-semibold ${accent}`}>
            {isBaseline ? "Baseline Agent" : "Pruned Agent"}
          </h2>
          <p className="text-xs text-white/45">
            {isBaseline ? "Full-history context" : "Retention-aware context"}
          </p>
        </div>
        <span className="rounded-full border border-white/15 px-2 py-0.5 text-[10px] uppercase tracking-wide text-white/50">
          {isBaseline ? "Full history" : "Pruned memory"}
        </span>
      </div>

      {/* Contained stats frame */}
      <div className="border-b border-white/10 p-4">
        <AgentStatusCard
          agentType={agentType}
          current={current}
          cumulative={cumulative}
          pruning={pruning}
        />
      </div>

      {/* Response area (fills the rest so both columns align) */}
      <div className="flex-1 p-4">
        <AgentResponsePanel agentType={agentType} messages={messages} busy={busy} />
      </div>
    </section>
  );
}

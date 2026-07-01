"use client";

import { AgentColumn } from "./agent-column";
import type { ChatMessage } from "./agent-response-panel";
import type { AgentCumulative, ChatTurnResponse } from "@/lib/types";

type TurnView = ChatTurnResponse & { userMessage: string };

function toMessages(turns: TurnView[], agent: "baseline" | "pruned"): ChatMessage[] {
  const out: ChatMessage[] = [];
  for (const t of turns) {
    out.push({ role: "user", content: t.userMessage, turn: t.turn });
    out.push({ role: "assistant", content: t[agent].response, turn: t.turn });
  }
  return out;
}

// Top-level split screen: baseline (left) vs pruned (right).
export function AgentComparisonGrid({
  turns,
  latest,
  cumulative,
  busy,
}: {
  turns: TurnView[];
  latest: TurnView | null;
  cumulative: { baseline: AgentCumulative; pruned: AgentCumulative };
  busy: boolean;
}) {
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
      <AgentColumn
        agentType="baseline"
        current={latest ? latest.baseline.metrics : null}
        cumulative={cumulative.baseline}
        messages={toMessages(turns, "baseline")}
        busy={busy}
      />
      <AgentColumn
        agentType="pruned"
        current={latest ? latest.pruned.metrics : null}
        cumulative={cumulative.pruned}
        messages={toMessages(turns, "pruned")}
        busy={busy}
        pruning={{
          events: turns.filter((t) => t.pruned.pruning_triggered).length,
          triggeredThisTurn: latest ? latest.pruned.pruning_triggered : false,
        }}
      />
    </div>
  );
}

// Reusable column wrapper: AgentStatusCard on top, AgentResponsePanel below.
// TODO(feat/frontend): pass live metrics + response through.

import { AgentResponsePanel } from "./agent-response-panel";

export function AgentColumn({ agentType }: { agentType: "baseline" | "pruned" }) {
  const isBaseline = agentType === "baseline";
  return (
    <div className="flex flex-col gap-3">
      <div className="glass p-4">
        <div
          className={`text-sm font-medium ${
            isBaseline ? "text-baseline" : "text-pruned"
          }`}
        >
          {isBaseline ? "Baseline Agent" : "Pruned Agent"}
        </div>
        <div className="text-xs text-white/50">
          {isBaseline ? "Full-history context" : "Retention-aware context"}
        </div>
      </div>
      <AgentResponsePanel agentType={agentType} />
    </div>
  );
}

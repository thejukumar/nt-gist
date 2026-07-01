// Top-level split-screen: baseline (left) vs pruned (right).

import { AgentColumn } from "./agent-column";

export function AgentComparisonGrid() {
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
      <AgentColumn agentType="baseline" />
      <AgentColumn agentType="pruned" />
    </div>
  );
}

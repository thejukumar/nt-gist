// Displays one agent's response text + turn number + loading state.
// TODO(feat/frontend): render response, sources, loading skeleton.

export function AgentResponsePanel({
  agentType,
}: {
  agentType: "baseline" | "pruned";
}) {
  return (
    <div className="glass min-h-[200px] p-4 text-sm text-white/70">
      {agentType} response will render here.
    </div>
  );
}

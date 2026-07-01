// Secondary cross-agent savings strip (doc §9). Primary stats live per-agent.
// TODO(feat/frontend): show input-token savings, cost savings, latency delta, events.

export function ComparisonSavingsStrip() {
  return (
    <div className="glass mt-4 flex flex-wrap gap-6 px-6 py-3 text-sm text-white/70">
      <span>Tokens saved —</span>
      <span>Cost saved —</span>
      <span>Latency delta —</span>
      <span>Pruning events —</span>
    </div>
  );
}

"use client";

import { formatCost, formatLatency, formatPercent } from "@/lib/formatters";
import type { Comparison } from "@/lib/types";

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col">
      <span className="text-[10px] uppercase tracking-wide text-white/40">{label}</span>
      <span className="font-mono text-sm text-white/90">{value}</span>
    </div>
  );
}

// Secondary cross-agent savings strip (cumulative).
export function ComparisonSavingsStrip({
  comparison,
  eventsCount,
}: {
  comparison: Comparison | null;
  eventsCount: number;
}) {
  return (
    <div className="glass mt-4 flex flex-wrap gap-8 px-6 py-3">
      <Stat
        label="Input-token reduction"
        value={comparison ? formatPercent(comparison.input_token_reduction_percent) : "—"}
      />
      <Stat
        label="Est. cost reduction"
        value={comparison ? formatPercent(comparison.cost_reduction_percent) : "—"}
      />
      <Stat
        label="Est. cost saved"
        value={comparison ? formatCost(comparison.estimated_cost_saved) : "—"}
      />
      <Stat
        label="Latency delta"
        value={comparison ? formatLatency(comparison.latency_delta_seconds) : "—"}
      />
      <Stat label="Pruning events" value={String(eventsCount)} />
    </div>
  );
}

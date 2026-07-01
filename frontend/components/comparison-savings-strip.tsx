"use client";

import { formatCost, formatLatency, formatPercent } from "@/lib/formatters";
import type { Comparison } from "@/lib/types";

function Stat({
  label,
  value,
  highlight,
}: {
  label: string;
  value: string;
  highlight?: boolean;
}) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/[0.03] px-4 py-3">
      <div className="text-[10px] uppercase tracking-wide text-white/40">{label}</div>
      <div className={`font-mono text-lg ${highlight ? "text-pruned" : "text-white/90"}`}>
        {value}
      </div>
    </div>
  );
}

// Secondary cross-agent savings strip (cumulative), as contained stat boxes.
export function ComparisonSavingsStrip({
  comparison,
  eventsCount,
}: {
  comparison: Comparison | null;
  eventsCount: number;
}) {
  return (
    <div className="glass mt-4 p-4">
      <div className="mb-3 text-[10px] uppercase tracking-wide text-white/35">Overall savings</div>
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
        <Stat
          label="Input-token reduction"
          value={comparison ? formatPercent(comparison.input_token_reduction_percent) : "—"}
          highlight
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
    </div>
  );
}

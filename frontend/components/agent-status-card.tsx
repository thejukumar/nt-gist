"use client";

import { formatCost, formatLatency, formatTokens } from "@/lib/formatters";
import type { AgentCumulative, TurnMetrics } from "@/lib/types";

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between text-xs">
      <span className="text-white/45">{label}</span>
      <span className="font-mono text-white/85">{value}</span>
    </div>
  );
}

function StatBox({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/[0.03] p-3">
      <div className="mb-2 text-[10px] uppercase tracking-wide text-white/35">{title}</div>
      <div className="space-y-1">{children}</div>
    </div>
  );
}

// Two contained stat boxes (current turn + cumulative). Row counts are kept equal
// across agents (baseline shows "N/A" for pruning) so the columns align.
export function AgentStatusCard({
  agentType,
  current,
  cumulative,
  pruning,
}: {
  agentType: "baseline" | "pruned";
  current: TurnMetrics | null;
  cumulative: AgentCumulative;
  pruning?: { events: number; triggeredThisTurn: boolean };
}) {
  const isBaseline = agentType === "baseline";
  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
      <StatBox title="Current turn">
        <Row label="Input tokens" value={current ? formatTokens(current.input_tokens) : "—"} />
        <Row label="Output tokens" value={current ? formatTokens(current.output_tokens) : "—"} />
        <Row label="Latency" value={current ? formatLatency(current.latency_seconds) : "—"} />
        <Row label="Est. cost" value={current ? formatCost(current.estimated_cost) : "—"} />
        <Row label="Tool calls" value={current ? String(current.tool_calls) : "—"} />
        <Row
          label="Pruning"
          value={isBaseline ? "N/A" : pruning?.triggeredThisTurn ? "triggered" : "—"}
        />
      </StatBox>

      <StatBox title="Cumulative">
        <Row label="Total input" value={formatTokens(cumulative.inputTokens)} />
        <Row label="Total output" value={formatTokens(cumulative.outputTokens)} />
        <Row label="Total tokens" value={formatTokens(cumulative.totalTokens)} />
        <Row label="Total est. cost" value={formatCost(cumulative.cost)} />
        <Row label="Avg latency" value={formatLatency(cumulative.avgLatency)} />
        <Row
          label="Pruning events"
          value={isBaseline ? "N/A" : String(pruning?.events ?? 0)}
        />
      </StatBox>
    </div>
  );
}

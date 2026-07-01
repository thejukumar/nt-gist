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

export function AgentStatusCard({
  agentType,
  title,
  subtitle,
  contextMode,
  current,
  cumulative,
  pruning,
}: {
  agentType: "baseline" | "pruned";
  title: string;
  subtitle: string;
  contextMode: string;
  current: TurnMetrics | null;
  cumulative: AgentCumulative;
  pruning?: { events: number; triggeredThisTurn: boolean };
}) {
  const accent = agentType === "baseline" ? "text-baseline" : "text-pruned";
  return (
    <div className="glass p-4">
      <div className="mb-2 flex items-baseline justify-between">
        <div>
          <div className={`text-sm font-semibold ${accent}`}>{title}</div>
          <div className="text-xs text-white/45">{subtitle}</div>
        </div>
        <span className="rounded-full border border-white/15 px-2 py-0.5 text-[10px] uppercase tracking-wide text-white/50">
          {contextMode}
        </span>
      </div>

      <div className="mb-1 text-[10px] uppercase tracking-wide text-white/35">Current turn</div>
      <div className="space-y-0.5">
        <Row label="Input tokens" value={current ? formatTokens(current.input_tokens) : "—"} />
        <Row label="Output tokens" value={current ? formatTokens(current.output_tokens) : "—"} />
        <Row label="Latency" value={current ? formatLatency(current.latency_seconds) : "—"} />
        <Row label="Est. cost" value={current ? formatCost(current.estimated_cost) : "—"} />
        <Row label="Tool calls" value={current ? String(current.tool_calls) : "—"} />
        {pruning ? (
          <Row
            label="Pruning"
            value={pruning.triggeredThisTurn ? "triggered" : "—"}
          />
        ) : null}
      </div>

      <div className="mb-1 mt-3 text-[10px] uppercase tracking-wide text-white/35">Cumulative</div>
      <div className="space-y-0.5">
        <Row label="Total input" value={formatTokens(cumulative.inputTokens)} />
        <Row label="Total output" value={formatTokens(cumulative.outputTokens)} />
        <Row label="Total tokens" value={formatTokens(cumulative.totalTokens)} />
        <Row label="Total est. cost" value={formatCost(cumulative.cost)} />
        <Row label="Avg latency" value={formatLatency(cumulative.avgLatency)} />
        {pruning ? <Row label="Pruning events" value={String(pruning.events)} /> : null}
      </div>
    </div>
  );
}

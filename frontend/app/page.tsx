"use client";

import { useMemo, useState } from "react";

import { AgentComparisonGrid } from "@/components/agent-comparison-grid";
import { ChatInput } from "@/components/chat-input";
import { ComparisonSavingsStrip } from "@/components/comparison-savings-strip";
import { Header } from "@/components/header";
import { PruningTimeline } from "@/components/pruning-timeline";
import { api } from "@/lib/api";
import { computeCumulative } from "@/lib/formatters";
import type { ChatTurnResponse } from "@/lib/types";

type TurnView = ChatTurnResponse & { userMessage: string };

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

export default function Home() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [turns, setTurns] = useState<TurnView[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const latest = turns.length ? turns[turns.length - 1] : null;
  const cumulative = useMemo(() => computeCumulative(turns), [turns]);
  const pruningEvents = useMemo(
    () =>
      turns
        .filter((t) => t.pruned.pruning_triggered && t.pruned.pruning_event)
        .map((t) => ({ turn: t.turn, event: t.pruned.pruning_event! })),
    [turns],
  );

  async function ensureSession(): Promise<string> {
    if (sessionId) return sessionId;
    const res = await api.startSession({ prune_every: 2, recent_turns_to_keep: 2 });
    setSessionId(res.session_id);
    return res.session_id;
  }

  async function send(text: string) {
    setError(null);
    setBusy(true);
    try {
      const id = await ensureSession();
      const res = await api.chatTurn(id, text);
      setTurns((prev) => [...prev, { ...res, userMessage: text }]);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setBusy(false);
    }
  }

  async function runDemo() {
    setError(null);
    setBusy(true);
    try {
      const id = await ensureSession();
      const { prompts } = await api.runDemo(id);
      for (const prompt of prompts) {
        const res = await api.chatTurn(id, prompt);
        setTurns((prev) => [...prev, { ...res, userMessage: prompt }]);
        await sleep(600);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Demo failed");
    } finally {
      setBusy(false);
    }
  }

  function reset() {
    setTurns([]);
    setSessionId(null);
    setError(null);
  }

  return (
    <main className="mx-auto max-w-6xl p-4 md:p-8">
      <Header onRunDemo={runDemo} onReset={reset} busy={busy} />

      {error && (
        <div className="glass mb-4 border-red-400/40 px-4 py-2 text-sm text-red-300">
          {error}
        </div>
      )}

      <AgentComparisonGrid turns={turns} latest={latest} cumulative={cumulative} busy={busy} />
      <ComparisonSavingsStrip
        comparison={latest ? latest.comparison : null}
        eventsCount={pruningEvents.length}
      />
      <PruningTimeline events={pruningEvents} />
      <ChatInput onSend={send} busy={busy} />

      <p className="mt-6 text-center text-xs text-white/40">
        Metrics are read from each Nebius call. Cost is estimated. Pruning every 2 turns, keep last 2.
      </p>
    </main>
  );
}

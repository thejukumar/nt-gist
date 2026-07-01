"use client";

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  turn: number;
}

export function AgentResponsePanel({
  agentType,
  messages,
  busy,
}: {
  agentType: "baseline" | "pruned";
  messages: ChatMessage[];
  busy: boolean;
}) {
  const accent = agentType === "baseline" ? "text-baseline" : "text-pruned";
  return (
    <div className="flex max-h-[460px] min-h-[260px] flex-col gap-3 overflow-y-auto rounded-xl border border-white/10 bg-white/[0.02] p-4">
      {messages.length === 0 && !busy ? (
        <p className="text-sm text-white/40">
          Responses will appear here. Send a message or run the demo.
        </p>
      ) : null}

      {messages.map((m, i) => (
        <div key={i} className={m.role === "user" ? "text-white/60" : ""}>
          <div className="mb-0.5 text-[10px] uppercase tracking-wide text-white/35">
            {m.role === "user" ? `You · turn ${m.turn}` : `Agent · turn ${m.turn}`}
          </div>
          <div className={`whitespace-pre-wrap text-sm ${m.role === "assistant" ? accent : ""}`}>
            {m.content}
          </div>
        </div>
      ))}

      {busy ? <div className="text-sm text-white/40">…thinking</div> : null}
    </div>
  );
}

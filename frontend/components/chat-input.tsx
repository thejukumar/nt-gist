"use client";

import { useState } from "react";

// Bottom ChatGPT-style prompt bar; sends the same message to both agents.
export function ChatInput({
  onSend,
  busy,
}: {
  onSend: (text: string) => void;
  busy: boolean;
}) {
  const [value, setValue] = useState("");

  function submit() {
    const text = value.trim();
    if (!text || busy) return;
    onSend(text);
    setValue("");
  }

  return (
    <div className="glass mt-4 flex items-center gap-3 px-4 py-3">
      <input
        className="flex-1 bg-transparent text-sm outline-none placeholder:text-white/40"
        placeholder="Ask your next support question..."
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") submit();
        }}
        disabled={busy}
      />
      <button
        onClick={submit}
        disabled={busy || !value.trim()}
        className="rounded-xl bg-white/10 px-4 py-1.5 text-sm hover:bg-white/20 disabled:opacity-40"
      >
        Send
      </button>
    </div>
  );
}

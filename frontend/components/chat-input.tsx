// Bottom ChatGPT-style prompt bar (sends the same message to both agents).
// TODO(feat/frontend): controlled input, Enter-to-submit, disabled while running.

export function ChatInput() {
  return (
    <div className="glass mt-4 flex items-center gap-3 px-4 py-3">
      <input
        className="flex-1 bg-transparent text-sm outline-none placeholder:text-white/40"
        placeholder="Ask your next support question..."
        disabled
      />
      <button
        className="rounded-xl bg-white/10 px-4 py-1.5 text-sm"
        disabled
      >
        Send
      </button>
    </div>
  );
}

"use client";

// Demo automation controls: Run 15-Turn Demo / Reset.
export function DemoControls({
  onRunDemo,
  onReset,
  busy,
}: {
  onRunDemo: () => void;
  onReset: () => void;
  busy: boolean;
}) {
  return (
    <div className="flex gap-2">
      <button
        onClick={onRunDemo}
        disabled={busy}
        className="rounded-xl bg-white/10 px-4 py-1.5 text-sm hover:bg-white/20 disabled:opacity-40"
      >
        {busy ? "Running…" : "Run 15-Turn Demo"}
      </button>
      <button
        onClick={onReset}
        disabled={busy}
        className="rounded-xl border border-white/15 px-4 py-1.5 text-sm hover:bg-white/10 disabled:opacity-40"
      >
        Reset
      </button>
    </div>
  );
}

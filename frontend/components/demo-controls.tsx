// Demo automation controls: Run 15-Turn Demo / Pause / Reset.
// TODO(feat/frontend): fetch prompts via api.runDemo and step through /chat/turn.

export function DemoControls() {
  return (
    <button className="rounded-xl bg-white/10 px-4 py-1.5 text-sm" disabled>
      Run 15-Turn Demo
    </button>
  );
}

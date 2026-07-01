// Project header: title, subtitle, top-level actions (Run Demo / Reset / Export).
// TODO(feat/frontend): wire action buttons to demo-controls + export-report-button.

export function Header() {
  return (
    <header className="glass mb-4 px-6 py-4">
      <h1 className="text-xl font-semibold tracking-tight">
        Support Context Budget Lab
      </h1>
      <p className="text-sm text-white/60">
        Baseline vs pruned agent for long enterprise support chats.
      </p>
    </header>
  );
}

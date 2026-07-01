"use client";

import { DemoControls } from "./demo-controls";
import { ExportReportButton } from "./export-report-button";

// Project header: title, subtitle, and top-level actions.
export function Header({
  onRunDemo,
  onReset,
  onExport,
  busy,
  canExport,
}: {
  onRunDemo: () => void;
  onReset: () => void;
  onExport: () => void;
  busy: boolean;
  canExport: boolean;
}) {
  return (
    <header className="glass mb-4 flex flex-col gap-3 px-6 py-4 md:flex-row md:items-center md:justify-between">
      <div>
        <h1 className="text-xl font-semibold tracking-tight">Support Context Budget Lab</h1>
        <p className="text-sm text-white/60">
          Baseline vs pruned agent for long enterprise support chats.
        </p>
      </div>
      <div className="flex gap-2">
        <DemoControls onRunDemo={onRunDemo} onReset={onReset} busy={busy} />
        <ExportReportButton onExport={onExport} disabled={busy || !canExport} />
      </div>
    </header>
  );
}

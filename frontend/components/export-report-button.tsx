"use client";

// Triggers report export (writes Markdown + JSON server-side, shows paths).
export function ExportReportButton({
  onExport,
  disabled,
}: {
  onExport: () => void;
  disabled: boolean;
}) {
  return (
    <button
      onClick={onExport}
      disabled={disabled}
      className="rounded-xl border border-white/15 px-4 py-1.5 text-sm hover:bg-white/10 disabled:opacity-40"
    >
      Export Report
    </button>
  );
}

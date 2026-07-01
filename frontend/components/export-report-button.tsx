// Triggers report export (Markdown + JSON) via GET /report/{session_id}.
// TODO(feat/reporting-polish): wire to backend report endpoint.

export function ExportReportButton() {
  return (
    <button className="rounded-xl bg-white/10 px-4 py-1.5 text-sm" disabled>
      Export Report
    </button>
  );
}

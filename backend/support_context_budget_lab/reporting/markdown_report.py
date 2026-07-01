"""Write a Markdown report to reports/session_<timestamp>.md."""

from __future__ import annotations

from pathlib import Path

_REPORTS_DIR = Path(__file__).resolve().parents[3] / "reports"


def write_markdown_report(session: object) -> Path:
    """Render a human-readable report (scenario, results, timeline, projection).

    TODO(feat/reporting-polish): render sections incl. business projection for
    10,000 monthly conversations; write under reports/; return the path.
    """
    raise NotImplementedError

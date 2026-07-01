"""Build and write a Markdown report to reports/session_<timestamp>.md."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .json_logger import build_session_log

_REPORTS_DIR = Path(__file__).resolve().parents[3] / "reports"

# Customer scenario constants (doc §3) used for the business projection.
MONTHLY_CONVERSATIONS = 10_000
AVG_TURNS = 15


def _pct(fraction: float) -> str:
    return f"{fraction * 100:.1f}%"


def _usd(value: float) -> str:
    return f"${value:.4f}"


def build_markdown_report(session) -> str:
    """Render a human-readable report string from a session."""
    log = build_session_log(session)
    s = log["summary"]

    per_conv_cost_saved = s["estimated_cost_savings"]
    per_conv_tokens_saved = s["baseline_total_input_tokens"] - s["pruned_total_input_tokens"]
    monthly_cost_saved = per_conv_cost_saved * MONTHLY_CONVERSATIONS
    monthly_tokens_saved = per_conv_tokens_saved * MONTHLY_CONVERSATIONS

    lines: list[str] = [
        "# Support Context Budget Lab Report",
        "",
        f"_Generated {log['created_at']} · session `{log['session_id']}`_",
        "",
        "## Customer Scenario",
        "Enterprise support chatbot with 100,000+ users, 10,000+ monthly support conversations, "
        "and an average of ~15 turns per conversation.",
        "",
        "## Experiment Setup",
        f"- LLM provider: {log['provider']} (`{log['model']}`)",
        f"- Web tool: {log['tool_provider']}",
        "- Baseline: full-history context",
        "- Optimized: pruning-aware support memory + evidence ledger",
        f"- Pruning frequency: every {log['prune_every']} turns",
        f"- Recent turns retained: {log['recent_turns_to_keep']}",
        f"- Turns in this session: {s['turns']}",
        "",
        "## Results Summary",
        f"- Baseline total input tokens: {s['baseline_total_input_tokens']:,}",
        f"- Pruned total input tokens: {s['pruned_total_input_tokens']:,}",
        f"- Input-token reduction: {_pct(s['input_token_reduction_percent'])}",
        f"- Baseline estimated cost: {_usd(s['baseline_total_cost'])}",
        f"- Pruned estimated cost: {_usd(s['pruned_total_cost'])}",
        f"- Estimated cost savings: {_usd(s['estimated_cost_savings'])} "
        f"({_pct(s['cost_reduction_percent'])})",
        f"- Avg latency — baseline {s['baseline_avg_latency']:.2f}s vs "
        f"pruned {s['pruned_avg_latency']:.2f}s",
        "",
        "## Turn-by-Turn Metrics",
        "| Turn | Baseline in | Pruned in | Baseline cost | Pruned cost | Pruned |",
        "|-----:|------------:|----------:|--------------:|------------:|:------:|",
    ]

    for rec in log["turns"]:
        bm = rec["baseline"]["metrics"]
        pm = rec["pruned"]["metrics"]
        flag = "✂️" if rec["pruned"]["pruning_triggered"] else ""
        lines.append(
            f"| {rec['turn']} | {bm['input_tokens']:,} | {pm['input_tokens']:,} "
            f"| {_usd(bm['estimated_cost'])} | {_usd(pm['estimated_cost'])} | {flag} |"
        )

    lines += ["", "## Pruning Timeline"]
    events = [r for r in log["turns"] if r["pruned"]["pruning_triggered"]]
    if events:
        for r in events:
            ev = r["pruned"]["pruning_event"]
            preserved = ", ".join(ev.get("preserved", [])) or "—"
            lines.append(
                f"- Turn {r['turn']}: compressed {ev['compressed_messages']} message(s); "
                f"preserved {preserved}"
            )
    else:
        lines.append("- No pruning events (conversation stayed within the recent window).")

    lines += [
        "",
        "## Business Projection",
        f"Scaling this conversation's savings across {MONTHLY_CONVERSATIONS:,} monthly "
        f"conversations (~{AVG_TURNS} turns each):",
        f"- Input tokens saved / month: ~{monthly_tokens_saved:,.0f}",
        f"- Estimated cost saved / month: ~{_usd(monthly_cost_saved)}",
        "",
        "## Limitations",
        "- Cost is estimated from configurable pricing, not an actual bill.",
        "- Answer accuracy is not scored in the MVP.",
        "- Token usage is measured from provider metadata when available; otherwise estimated.",
        "- Pruning wins on long conversations; short chats may favor the baseline due to the "
        "pruned agent's fixed retention overhead.",
    ]
    return "\n".join(lines)


def write_markdown_report(session, path: Path | None = None) -> Path:
    """Write the Markdown report; return the path."""
    _REPORTS_DIR.mkdir(exist_ok=True)
    if path is None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        path = _REPORTS_DIR / f"session_{stamp}.md"
    path.write_text(build_markdown_report(session))
    return path

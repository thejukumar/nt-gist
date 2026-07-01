# Technical Statement — Support Context Budget Lab

> Deliverable for the Tavily FDE take-home (Option 1: improve an existing application).
> _Draft skeleton — filled in as the build progresses._

## What I built
I improved the starter Tavily agent by turning it into a **UI-first enterprise support-agent
benchmark**. The starter demonstrates a single Nebius-powered LangChain agent using Tavily search.
This project keeps the same Nebius + Tavily core but expands it into an **A/B comparison** for
long-running support conversations.

## Approach
- Run the same prompt through a **full-history baseline agent** and a **pruning-aware agent**.
- The pruned agent maintains **support memory**, **recent turns**, and a compact **Tavily evidence
  ledger** via a reusable pruning engine that is fully **decoupled from metrics**.
- Capture real per-turn metrics (input/output tokens, latency, estimated cost, tool calls) for both
  agents and render them side by side.

## Why this creates value
- **Business:** at 10,000+ support conversations/month, carrying full history + raw tool output every
  turn is a real cost/latency line item. The lab quantifies the savings from pruning.
- **Technical:** demonstrates context engineering, agent architecture, metrics/observability, and an
  evaluation-style comparison loop.

## Key design decisions
- _TODO: metrics ⟂ pruning separation; usage_metadata primary + tokenizer fallback; prune-every-2._

## Results (from a 15-turn demo)
- _TODO: baseline vs pruned totals, % input-token reduction, estimated cost saved, projection._

## Limitations
- _TODO: estimated cost, no accuracy scoring in MVP, single scenario._

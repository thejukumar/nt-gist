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
- **Metrics are independent of pruning.** The pruner only decides *what context the pruned agent
  sends*; the metrics layer measures each Nebius call identically for both agents. Pruning could
  change entirely and the measurement path would not.
- **Honest token counting.** Primary = `usage_metadata` from the Nebius/LangChain response; fallback
  = a local tiktoken estimate, flagged `estimated`. Cost is always labeled *estimated*, never a bill.
- **Deterministic pruning, no extra LLM call.** Prune every 2 turns, keep last 2: the pruner rebuilds
  a compact system message (persona + retention policy + support memory + evidence ledger) and keeps
  the recent window. Evidence is compacted into a ledger instead of carrying raw Tavily blobs.
- **Clean A/B.** Both agents share model, prompt intent, tool, and `temperature=0`; the only variable
  is the context strategy.

## Results (illustrative 15-turn telecom run; see `reports/sample_report.md`)
Generated deterministically with a mock provider (real runs use live Nebius/Tavily):
- Baseline total input tokens **9,140** vs pruned **5,113** → **44.1% input-token reduction**.
- Baseline input grows every turn (94 → 998); pruned stays flat (~360) once the window fills.
- Estimated cost saved **36.2%**; pruning events on turns 4/6/8/10/12/14.
- The Markdown report projects per-conversation savings across 10,000 monthly conversations.

## Limitations
- Cost is estimated from configurable pricing, not an actual bill.
- Answer accuracy is not scored in the MVP (no LLM-judge); we show context retention + pruning events.
- Pruning wins on long conversations; short chats can favor the baseline due to the pruned agent's
  fixed retention overhead (crossover ~turn 5 in the sample).
- Single scenario, single pruning strategy, in-memory sessions (no DB/auth).

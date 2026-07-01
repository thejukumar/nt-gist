# Build Log — Support Context Budget Lab

> How this project was built. Paired with the [`build-record/`](build-record/) folder and Traces.com
> session links. _Skeleton — appended to as each branch lands._

## Initial idea
Turn the single-shot Tavily starter agent into a side-by-side benchmark that makes the cost of
context bloat — and the savings from pruning — visible for enterprise support chats.

## Why this use case
Enterprise support: high conversation volume, long chats, real cost/latency sensitivity.

## Architecture decisions
- FastAPI backend + Next.js frontend, all local (no Docker), one-command `run.sh`.
- Layered backend: controllers → service → business logic (pruning/metrics) → integration adapters.
- **Metrics independent of pruning**; token usage from `usage_metadata` with tokenizer fallback.

## Why UI-first
The core value is a *visual* comparison; a reviewer should see the divergence immediately.

## Why a separate pruning module
Pruning is a reusable capability (retention policy + support memory + evidence ledger + pruner), not
a hardcoded prompt trick.

## Branch-by-branch
1. `feat/scaffold` — repo structure, layering stubs, `/health`, run script, docs. _(in progress)_
2. `feat/providers-metrics` — Nebius client (usage_metadata primary + tiktoken fallback, latency
   capture), Tavily client (normalized sources + tool-call count), metrics layer (session stats +
   comparison). langchain imported lazily so the app still boots without it.
3. `feat/pruning-engine` — retention policy / support memory / evidence ledger serialization,
   ledger dedup, and the deterministic context pruner (rebuilds a compact system message + keeps the
   last N turns; emits a PruningEvent every `prune_every`). All prior skips now implemented.
4. `feat/agents-ab-endpoint` — _TODO_
5. `feat/frontend` — _TODO_
6. `feat/reporting-polish` — _TODO_

## Verification
See [`build-record/verification-log.md`](build-record/verification-log.md).

## What I'd improve next
- _TODO: streaming, LLM-judge quality scoring, semantic-retrieval pruning, persistence._

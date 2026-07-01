# Session Summaries

## Session 1 — Planning + Scaffold (`feat/scaffold`)
Goal: agree on architecture and lay down the layered repo skeleton.
Decisions:
- FastAPI + Next.js, all local, one-command `run.sh`; uv for Python.
- Metrics layer decoupled from pruning; token usage via `usage_metadata` + tokenizer fallback.
- Prune every 2 turns, keep last 2. Six branches off `main`.
Result: runnable backend (`/health`, `/session/start`, `/demo/run`), typed API stubs, layer
interfaces, docs skeletons, tests green.

## Session 2 — Providers + Metrics — _TODO_
## Session 3 — Pruning Engine — _TODO_
## Session 4 — Agents + A/B Endpoint — _TODO_
## Session 5 — Frontend — _TODO_
## Session 6 — Reporting + Polish — _TODO_

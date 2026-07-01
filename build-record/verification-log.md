# Verification Log

## `feat/scaffold`
- [x] `uv sync` installs backend deps
- [x] `uv run pytest -q` passes (cost, retention defaults, prune cadence, /health smoke)
- [x] Backend starts; `GET /health` returns `{"status":"ok", ...}`
- [x] `POST /api/demo/run` returns the 15 telecom prompts
- [x] `npm install` + `npm run dev` serve the placeholder UI
- [x] `starter_agent.py` is git-ignored; `.env` is git-ignored

## `feat/providers-metrics`
- [x] `pytest` passes: 23 passed, 2 skipped (token usage, session stats, provider helpers, LC message mapping)
- [x] Token usage: usage_metadata primary path + tiktoken fallback estimator
- [x] Session stats: cumulative totals + fractional savings comparison
- [x] Provider clients import without langchain installed (lazy import); app still boots
- [ ] Real Nebius call returns a response (needs uv + NEBIUS_API_KEY)
- [ ] Real Tavily search returns sources (needs uv + TAVILY_API_KEY)

## `feat/pruning-engine`
- [x] `pytest` passes: 32 passed, 0 skipped
- [x] Prune cadence: fires every 2 turns; keeps last N turns verbatim
- [x] Compact context rebuilds system message (persona + retention + memory + ledger)
- [x] Evidence ledger dedupes by url; memory/policy serialize to prompt blocks
- [ ] Baseline tokens grow across turns (feat/agents-ab-endpoint)

## `feat/agents-ab-endpoint`
- [x] `pytest` passes: 38 passed (agents + orchestration via injected fakes)
- [x] Baseline cumulative input tokens exceed pruned over a long conversation
- [x] Pruning events fire on prune-cadence turns once history exceeds the window
- [x] Tavily search increments tool_calls and populates the pruned ledger
- [x] `POST /api/chat/turn` returns baseline + pruned + comparison (shape validated)
- [ ] LIVE: real Nebius/Tavily 15-turn run (needs uv + keys) — pending
- [ ] 15-turn demo completes; report + JSON log generated (feat/reporting-polish)

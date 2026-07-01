# Verification Log

## `feat/scaffold`
- [x] `uv sync` installs backend deps
- [x] `uv run pytest -q` passes (cost, retention defaults, prune cadence, /health smoke)
- [x] Backend starts; `GET /health` returns `{"status":"ok", ...}`
- [x] `POST /api/demo/run` returns the 15 telecom prompts
- [x] `npm install` + `npm run dev` serve the placeholder UI
- [x] `starter_agent.py` is git-ignored; `.env` is git-ignored
- [ ] Real Nebius call returns a response (feat/providers-metrics)
- [ ] Real Tavily search returns sources (feat/providers-metrics)
- [ ] Baseline tokens grow across turns (feat/agents-ab-endpoint)
- [ ] Pruning triggers on turn 2 (feat/pruning-engine)
- [ ] 15-turn demo completes; report + JSON log generated (feat/reporting-polish)

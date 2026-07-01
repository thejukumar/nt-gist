# Support Context Budget Lab

**A UI-first A/B benchmark for context pruning in enterprise support agents.**

Two Nebius + Tavily support agents run the *same* multi-turn conversation side by side:

- **Baseline agent** — keeps the full conversation history and all prior Tavily output every turn.
- **Pruned agent** — sends a compact context (recent turns + support memory + a Tavily evidence
  ledger), preserving what matters while dropping context bloat.

After every turn we capture the **real** stats from each Nebius call — input tokens, output tokens,
latency, estimated cost, tool calls — and show them side by side, so you can watch the baseline get
heavier while the pruned agent stays lean.

> Built on top of the Tavily FDE starter agent (LangChain + `ChatNebius` + `TavilySearch`).
> The metrics layer is **independent** of the pruning logic: pruning only changes *what context the
> pruned agent sends*; measurement is identical for both agents.

---

## Quick start

```bash
git clone <repo> && cd support-context-budget-lab
cp .env.example .env        # then add your TAVILY_API_KEY and NEBIUS_API_KEY
./run.sh                     # checks prereqs, installs deps, starts both servers
```

- Backend (FastAPI): http://127.0.0.1:8000  (`/health`, docs at `/docs`)
- Frontend (Next.js): http://localhost:3000

`./run.sh` verifies prerequisites, installs backend (uv) + frontend (npm) deps, and runs both.
Other entrypoints: `./run.sh --check`, `./run.sh --install`, or `make help` for granular targets.

### Prerequisites
- [uv](https://docs.astral.sh/uv/) (Python 3.11+ toolchain) — `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Node.js 18+ and npm

---

## Customer scenario

An enterprise support org with **100,000+ users**, **10,000+ support conversations/month**, and an
average of **~15 turns** per chat. Long chats accumulate history + prior tool output, driving up
input tokens, latency, and cost. This lab makes that cost — and the savings from pruning — measurable.

---

## How it works

| Layer | Responsibility |
|-------|----------------|
| `backend/main.py` + routers | HTTP controllers (thin) |
| `session_manager`, `agents/` | orchestration / service layer |
| `pruning/`, `metrics/` | business logic (pure, unit-tested) |
| `llm/`, `tools/` | Nebius + Tavily integration adapters |
| `reporting/` | JSON session log + Markdown report |
| `frontend/` | Next.js side-by-side comparison UI |

**Pruning** (every 2 turns, keep last 2): a retention policy defines what must survive; a support
memory holds durable state (issue, product, plan, steps tried, open questions, escalation); an
evidence ledger keeps compact Tavily sources instead of raw blobs.

**Token counting:** primary = `usage_metadata` from the Nebius/LangChain response; fallback = a local
tokenizer estimate (clearly labeled). Cost is always **estimated**, never an actual bill.

---

## Environment variables

See [`.env.example`](.env.example). Required: `TAVILY_API_KEY`, `NEBIUS_API_KEY`. Optional pricing,
pruning defaults, ports, and LangSmith tracing.

---

## Project docs
- [`TECHNICAL_STATEMENT.md`](TECHNICAL_STATEMENT.md) — approach + value (submission deliverable)
- [`BUILD_LOG.md`](BUILD_LOG.md) — how it was built
- [`build-record/`](build-record/) — Traces.com links, session summaries, verification log

## Limitations
Cost is estimated from configurable pricing. Answer accuracy is **not** scored in the MVP (no
LLM-judge); we show context retention + pruning events instead. Token usage is measured when provider
metadata is available, otherwise estimated. Single scenario, single pruning strategy, in-memory
sessions (no DB/auth).

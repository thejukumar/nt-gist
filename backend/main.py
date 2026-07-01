"""FastAPI application entrypoint for Support Context Budget Lab.

Run: `uv run uvicorn main:app --reload` (from backend/), or use ../run.sh.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from support_context_budget_lab import __version__
from support_context_budget_lab.api.routes import router as api_router
from support_context_budget_lab.config import get_settings

app = FastAPI(
    title="Support Context Budget Lab",
    version=__version__,
    description="A/B benchmark comparing full-history vs pruning-aware support agents.",
)

# Allow the Next.js dev server to call the API locally.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health", tags=["health"])
def health() -> dict:
    """Liveness check + which provider keys are configured (booleans only)."""
    settings = get_settings()
    return {
        "status": "ok",
        "version": __version__,
        "model": settings.nebius_model,
        "keys_configured": {
            "tavily": bool(settings.tavily_api_key and not settings.tavily_api_key.startswith("tvly-...")),
            "nebius": bool(settings.nebius_api_key),
        },
    }

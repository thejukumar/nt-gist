"""FastAPI application entrypoint for Support Context Budget Lab.

Run: `uv run uvicorn main:app --reload` (from backend/), or use ../run.sh.
"""

from __future__ import annotations

import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from support_context_budget_lab import __version__
from support_context_budget_lab.api.routes import router as api_router
from support_context_budget_lab.config import get_settings
from support_context_budget_lab.logging_config import configure_logging, get_logger

configure_logging()
log = get_logger("http")

app = FastAPI(
    title="Support Context Budget Lab",
    version=__version__,
    description="A/B benchmark comparing full-history vs pruning-aware support agents.",
)

# Allow the Next.js dev server on any local port (3000, 3001, …) so the UI works
# even when the default port is taken.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log each request's method/path, status, and duration to the terminal."""
    start = time.perf_counter()
    log.info(f"→ {request.method} {request.url.path}")
    try:
        response = await call_next(request)
    except Exception as exc:  # pragma: no cover - defensive
        log.exception(f"✗ {request.method} {request.url.path} raised: {exc}")
        raise
    duration_ms = (time.perf_counter() - start) * 1000
    log.info(f"← {request.method} {request.url.path} {response.status_code} {duration_ms:.0f}ms")
    return response


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

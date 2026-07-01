"""Application configuration and environment validation.

Loads settings from the environment (and the root `.env` via python-dotenv).
`require_keys()` gives a clear error early if provider keys are missing.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load the repo-root .env (one level above backend/) if present.
_ROOT_ENV = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(_ROOT_ENV)


class Settings(BaseSettings):
    """Runtime settings, overridable via environment variables."""

    model_config = SettingsConfigDict(env_file=_ROOT_ENV, extra="ignore")

    # Providers
    tavily_api_key: str = ""
    nebius_api_key: str = ""
    nebius_model: str = "moonshotai/Kimi-K2.6"

    # Estimated pricing (USD per 1M tokens) — for "estimated cost" only.
    input_cost_per_1m: float = 0.60
    output_cost_per_1m: float = 2.40

    # Pruning defaults (overridable per session).
    prune_every: int = 2
    recent_turns_to_keep: int = 2

    # Server
    backend_host: str = "127.0.0.1"
    backend_port: int = 8000

    @property
    def missing_keys(self) -> list[str]:
        missing = []
        if not self.tavily_api_key or self.tavily_api_key.startswith("tvly-..."):
            missing.append("TAVILY_API_KEY")
        if not self.nebius_api_key:
            missing.append("NEBIUS_API_KEY")
        return missing

    def require_keys(self) -> None:
        """Raise a clear error if required provider keys are absent."""
        if self.missing_keys:
            raise RuntimeError(
                "Missing required env vars: "
                + ", ".join(self.missing_keys)
                + ". Copy .env.example to .env and fill them in."
            )


@lru_cache
def get_settings() -> Settings:
    """Cached settings accessor (FastAPI dependency-friendly)."""
    return Settings()

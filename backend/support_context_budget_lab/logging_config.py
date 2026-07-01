"""Small logging setup so each API/provider call is visible in the terminal.

Uses a dedicated `scbl` logger (own handler, no propagation) so it prints
cleanly alongside uvicorn's own logs. Call `configure_logging()` once at
startup, then `get_logger(name)` anywhere.
"""

from __future__ import annotations

import logging
import sys

_CONFIGURED = False


def configure_logging(level: int = logging.INFO) -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return
    logger = logging.getLogger("scbl")
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s [scbl] %(levelname)s %(message)s", datefmt="%H:%M:%S")
    )
    logger.addHandler(handler)
    logger.propagate = False
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Return a namespaced logger, e.g. get_logger('nebius') -> 'scbl.nebius'."""
    return logging.getLogger(f"scbl.{name}")

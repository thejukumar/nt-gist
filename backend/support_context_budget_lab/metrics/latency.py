"""Latency measurement helper."""

from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def measure_latency() -> Iterator[list[float]]:
    """Context manager that records wall-clock seconds.

    Usage:
        with measure_latency() as elapsed:
            ...call...
        seconds = elapsed[0]
    """
    holder: list[float] = [0.0]
    start = time.perf_counter()
    try:
        yield holder
    finally:
        holder[0] = time.perf_counter() - start

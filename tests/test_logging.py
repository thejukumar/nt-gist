"""Logging setup: namespaced loggers + idempotent configuration."""

import logging

from support_context_budget_lab.logging_config import configure_logging, get_logger


def test_get_logger_is_namespaced():
    assert get_logger("nebius").name == "scbl.nebius"


def test_configure_logging_is_idempotent():
    configure_logging()
    before = len(logging.getLogger("scbl").handlers)
    configure_logging()
    after = len(logging.getLogger("scbl").handlers)
    # A second call must not add another handler (no duplicate log lines).
    assert after == before


def test_scbl_logger_does_not_propagate():
    configure_logging()
    assert logging.getLogger("scbl").propagate is False

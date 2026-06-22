from __future__ import annotations

import logging
import sys
from functools import cached_property
from logging.handlers import RotatingFileHandler
from pathlib import Path

from src.config import settings

_MAX_BYTES = 50 * 1024   # ~50 KB ≈ 500 lines per file
_BACKUP_COUNT = 20        # FIFO: oldest file evicted when limit reached


class LoggingMixin:
    """Injects a class-scoped :class:`logging.Logger` via ``self.log``.

    Pure mixin — carries no ``__init__`` state.  The logger is created lazily
    on first access and named after the concrete class that inherits this mixin.

    Usage::

        class MyAnalyzer(LoggingMixin):
            def run(self) -> None:
                self.log.info("Starting analysis")
                self.log.debug("detail=%s", some_value)
    """

    @cached_property
    def log(self) -> logging.Logger:
        return _get_logger(type(self).__name__)

    def configure_root_logging(
        self,
        level: str = "INFO",
        fmt: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        log_file: Path = settings.log_file,
    ) -> None:
        """One-shot root logger setup — call once at process entry point.

        Attaches both a stderr StreamHandler and a RotatingFileHandler so that
        logs are visible in the terminal and persisted with FIFO rotation.
        """
        formatter = logging.Formatter(fmt)

        stream_h = logging.StreamHandler(sys.stderr)
        stream_h.setFormatter(formatter)

        file_h = RotatingFileHandler(
            log_file,
            maxBytes=_MAX_BYTES,
            backupCount=_BACKUP_COUNT,
        )
        file_h.setFormatter(formatter)

        root = logging.getLogger()
        if not root.handlers:
            root.addHandler(stream_h)
            root.addHandler(file_h)
        root.setLevel(getattr(logging, level.upper(), logging.INFO))


def _get_logger(name: str) -> logging.Logger:
    """Return a logger scoped to *name*, inheriting root handler config."""
    return logging.getLogger(f"graphify.{name}")

from __future__ import annotations

import logging
import sys
from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


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
    ) -> None:
        """One-shot root logger setup — call once at process entry point."""
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(fmt))
        root = logging.getLogger()
        if not root.handlers:
            root.addHandler(handler)
        root.setLevel(getattr(logging, level.upper(), logging.INFO))


def _get_logger(name: str) -> logging.Logger:
    """Return a logger scoped to *name*, inheriting root handler config."""
    return logging.getLogger(f"graphify.{name}")

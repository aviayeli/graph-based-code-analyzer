from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any

log = logging.getLogger("graphify.CheckpointMixin")


class CheckpointMixin:
    """Persists intermediate graph-build state to disk (Rule R2).

    Pure mixin — no ``__init__`` state.  Requires the concrete class to
    expose a ``checkpoint_dir`` attribute (a :class:`~pathlib.Path`).

    Checkpoints are plain JSON files written atomically via a temp-file swap
    so a crash mid-write never corrupts the previous checkpoint.
    """

    checkpoint_dir: Path = Path(".checkpoints")

    def save_checkpoint(self, name: str, data: dict[str, Any]) -> Path:
        """Persist *data* as ``<checkpoint_dir>/<name>.json``.

        Write is atomic: we write to ``<name>.tmp`` then rename.
        """
        dest = self._cp_dir() / f"{name}.json"
        tmp = dest.with_suffix(".tmp")
        payload = {"_saved_at": time.time(), **data}
        tmp.write_text(json.dumps(payload, default=str), encoding="utf-8")
        tmp.replace(dest)
        log.debug("Checkpoint saved: %s", dest)
        return dest

    def load_checkpoint(self, name: str) -> dict[str, Any] | None:
        """Return previously saved checkpoint data, or ``None`` if absent."""
        dest = self._cp_dir() / f"{name}.json"
        if not dest.exists():
            return None
        data: dict[str, Any] = json.loads(dest.read_text(encoding="utf-8"))
        log.info("Checkpoint restored: %s (saved_at=%s)", name, data.get("_saved_at"))
        return data

    def clear_checkpoint(self, name: str) -> None:
        dest = self._cp_dir() / f"{name}.json"
        if dest.exists():
            dest.unlink()
            log.debug("Checkpoint cleared: %s", name)

    def emit_progress(
        self,
        *,
        phase: str,
        completed: int,
        total: int,
        tokens_used: int = 0,
    ) -> None:
        """Log a structured progress line — consumed by CI and monitoring."""
        pct = (completed / total * 100) if total else 0.0
        log.info(
            "[PROGRESS] phase=%s %d/%d (%.1f%%) tokens_used=%d",
            phase, completed, total, pct, tokens_used,
        )

    def _cp_dir(self) -> Path:
        d = Path(self.checkpoint_dir)
        d.mkdir(parents=True, exist_ok=True)
        return d

from __future__ import annotations

import subprocess
from pathlib import Path

from src.mixins import LoggingMixin

_EXCLUDE: frozenset[str] = frozenset(
    {"test", "tests", "__pycache__", ".git", "docs", "migrations"}
)


class RepoFetcher(LoggingMixin):
    """Locates Python source files within an already-cloned repository.

    The repository is treated as read-only (Rule R6).  No cloning is performed
    here — pass the path to an existing checkout.
    """

    def __init__(self, root: Path) -> None:
        self.root = Path(root)

    def collect_files(
        self,
        *,
        extensions: tuple[str, ...] = (".py",),
        exclude_dirs: frozenset[str] = _EXCLUDE,
    ) -> list[Path]:
        """Return a sorted list of source files, skipping excluded directories."""
        results: list[Path] = []
        for path in self.root.rglob("*"):
            if path.suffix not in extensions:
                continue
            if any(part in exclude_dirs for part in path.parts):
                continue
            results.append(path)
        results.sort()
        self.log.info("Collected %d files under %s", len(results), self.root)
        return results

    def get_sha(self) -> str:
        """Return the short HEAD commit SHA, or ``'unknown'`` on failure."""
        try:
            result = subprocess.run(
                ["git", "-C", str(self.root), "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.stdout.strip() if result.returncode == 0 else "unknown"
        except Exception:
            return "unknown"

    def get_repo_name(self) -> str:
        return self.root.name

    def relative_path(self, absolute: Path, *, base: Path | None = None) -> str:
        """Return a posix path relative to *base* (defaults to ``self.root``)."""
        ref = base or self.root
        try:
            return absolute.relative_to(ref).as_posix()
        except ValueError:
            return absolute.as_posix()

from __future__ import annotations

import ast
from pathlib import Path

from src._visitor import _Visitor
from src.mixins import LoggingMixin, TokenBudgetMixin
from src.models import NodeType, RawEdge, RawNode


class ASTParser(LoggingMixin, TokenBudgetMixin):
    """Deterministic AST extractor.

    All edges are tagged ``EXTRACTED``; zero LLM token spend (Rule R1).
    Uses :class:`~src._visitor._Visitor` for single-pass traversal and
    :class:`~src.mixins.TokenBudgetMixin` so any future LLM augmentation
    is automatically budget-tracked.
    """

    def __init__(self, src_root: Path, repo_root: Path) -> None:
        self.src_root = Path(src_root)
        self.repo_root = Path(repo_root)

    # ── private helpers ───────────────────────────────────────────────────

    def _module_id(self, path: Path) -> str:
        """Convert an absolute path to a dotted module string."""
        rel = path.relative_to(self.src_root)
        parts = list(rel.with_suffix("").parts)
        if parts and parts[-1] == "__init__":
            parts = parts[:-1]
        return ".".join(parts)

    def _file_rel(self, path: Path) -> str:
        try:
            return path.relative_to(self.repo_root).as_posix()
        except ValueError:
            return path.as_posix()

    # ── public API ────────────────────────────────────────────────────────

    def parse_file(self, path: Path) -> tuple[list[RawNode], list[RawEdge]]:
        """Parse one file deterministically. Returns empty lists on syntax error."""
        module = self._module_id(path)
        file_rel = self._file_rel(path)
        try:
            source = path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(source, filename=str(path))
        except SyntaxError as exc:
            self.log.warning("SyntaxError in %s: %s", path.name, exc)
            return [], []
        loc = source.count("\n") + 1
        mod_node = RawNode(
            id=module,
            type=NodeType.MODULE,
            name=module.split(".")[-1],
            file=file_rel,
            line=1,
            end_line=loc,
            module=module,
            loc=loc,
        )
        visitor = _Visitor(module, file_rel)
        visitor.visit(tree)
        return [mod_node, *visitor.nodes], visitor.edges

    def parse_files(
        self, paths: list[Path], *, log_interval: int = 100
    ) -> tuple[list[RawNode], list[RawEdge]]:
        all_nodes: list[RawNode] = []
        all_edges: list[RawEdge] = []
        total = len(paths)
        for i, path in enumerate(paths):
            nodes, edges = self.parse_file(path)
            all_nodes.extend(nodes)
            all_edges.extend(edges)
            if (i + 1) % log_interval == 0:
                self.log.info(
                    "[PARSE] %d/%d | nodes=%d edges=%d",
                    i + 1, total, len(all_nodes), len(all_edges),
                )
        self.log.info(
            "Parse complete: %d nodes, %d edges from %d files",
            len(all_nodes), len(all_edges), total,
        )
        return all_nodes, all_edges

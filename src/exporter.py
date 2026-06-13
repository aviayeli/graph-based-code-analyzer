from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from src.mixins import LoggingMixin

# ── Pure formatting helpers (no class state needed) ───────────────────────────

def _wl(name: str) -> str:
    """Wrap *name* in Obsidian wikilink syntax."""
    return f"[[{name}]]"


def _score(node: dict) -> int:
    return node["in_degree"] + node["out_degree"]


def _subdomain(module: str) -> str:
    """Return the first sub-package component of a dotted module path.

    ``crewai.agents.crew_agent_executor`` → ``agents``
    ``crewai`` → ``crewai``
    """
    parts = module.split(".")
    return parts[1] if len(parts) > 1 else parts[0]


class GraphExporter(LoggingMixin):
    """Converts graph.json into Obsidian-ready ``index.md`` and ``hot.md``.

    Separation of concerns: this class only formats and writes Markdown.
    It never modifies the source JSON or any AST logic.
    """

    def __init__(self, graph_dict: dict) -> None:
        self._meta: dict = graph_dict["meta"]
        self._nodes: list[dict] = graph_dict["nodes"]
        self._edges: list[dict] = graph_dict["edges"]

    @classmethod
    def from_json(cls, path: Path) -> GraphExporter:
        """Load a ``graph.json`` file and return a ready exporter."""
        data: dict = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(data)

    # ── index.md ──────────────────────────────────────────────────────────

    def write_index(self, path: Path) -> None:
        """Write the master navigation hub (``index.md``) to *path*."""
        lines = self._index_lines()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines), encoding="utf-8")
        self.log.info("index.md → %s (%d lines)", path, len(lines))

    def _index_lines(self) -> list[str]:
        m = self._meta
        lines: list[str] = [
            f"# {m['repo']} — Knowledge Graph Index",
            f"> SHA `{m['sha']}` · {m['total_nodes']:,} nodes · "
            f"{m['total_edges']:,} edges · {m['generated_at'][:10]}",
            "",
            "## Quick Navigation",
            f"- {_wl('hot')} — God-node hot-spot cache",
            f"- {_wl('index')} — This file (domain map)",
            "",
            "## Domain Architecture",
            "",
        ]
        # Group class nodes by sub-package
        by_domain: dict[str, list[dict]] = defaultdict(list)
        for n in self._nodes:
            if n["type"] == "class":
                by_domain[_subdomain(n["module"])].append(n)

        for domain, classes in sorted(by_domain.items(), key=lambda x: -len(x[1])):
            lines.append(f"### {domain} ({len(classes)} classes)")
            lines.append("")
            top = sorted(classes, key=_score, reverse=True)[:10]
            for cls in top:
                s = _score(cls)
                lines.append(
                    f"- {_wl(cls['name'])} · `{cls['id']}` · "
                    f"in: {cls['in_degree']} out: {cls['out_degree']} "
                    f"loc: {cls['loc']:,} score: **{s}**"
                )
            if len(classes) > 10:
                lines.append(f"- *…and {len(classes) - 10} more*")
            lines.append("")
        return lines

    # ── hot.md ────────────────────────────────────────────────────────────

    def write_hot(self, path: Path, *, top_n: int = 30) -> None:
        """Write the god-node hot-spot cache (``hot.md``) to *path*."""
        lines = self._hot_lines(top_n=top_n)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines), encoding="utf-8")
        self.log.info("hot.md → %s (%d lines)", path, len(lines))

    def _hot_lines(self, *, top_n: int) -> list[str]:
        ranked = sorted(self._nodes, key=_score, reverse=True)
        god_nodes = [n for n in ranked if _score(n) > 0][:top_n]
        m = self._meta
        lines: list[str] = [
            f"# {m['repo']} — Hot-Spot Cache",
            f"> Top {top_n} god-nodes · ranked by score (in\\_degree + out\\_degree)",
            f"> {_wl('index')} ← back to domain map",
            "",
            "## Top 5 Architectural Bottlenecks",
            "",
        ]
        for i, node in enumerate(god_nodes[:5], 1):
            s = _score(node)
            lines += [
                f"### {i}. {_wl(node['name'])} — Score: {s}",
                f"- **ID:** `{node['id']}`  |  **Type:** `{node['type']}`",
                f"- **File:** `{node['file']}`  |  **LOC:** {node['loc']:,}",
                f"- **In-degree:** {node['in_degree']} · "
                f"**Out-degree:** {node['out_degree']}",
                "",
            ]
        lines += [
            "## Full God-Node Table",
            "",
            "| Rank | Node | Score | In | Out | LOC | Type |",
            "|------|------|-------|----|-----|-----|------|",
        ]
        for i, node in enumerate(god_nodes, 1):
            s = _score(node)
            lines.append(
                f"| {i} | {_wl(node['name'])} | {s} "
                f"| {node['in_degree']} | {node['out_degree']} "
                f"| {node['loc']:,} | `{node['type']}` |"
            )
        return lines

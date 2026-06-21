"""FinOps analyzer: benchmarks graph-nav context vs. naive file ingestion.

Token estimation uses the standard Anthropic approximation (1 token ≈ 4 chars).
No LLM API calls are made — counts are deterministic context-length measurements.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.config import settings
from src.mixins import LoggingMixin, TokenBudgetMixin


def _tokens(text: str) -> int:
    return max(1, len(text) // int(settings.chars_per_token))


def _naive_context(files: list[str], repo_root: Path) -> str:
    parts: list[str] = []
    for rel in files:
        p = repo_root / rel
        if p.exists():
            parts.append(f"# === {rel} ===\n{p.read_text(encoding='utf-8', errors='replace')}")
    return "\n\n".join(parts)


def _graph_nav_context(node_ids: list[str], graph: dict) -> str:
    node_map = {n["id"]: n for n in graph["nodes"]}
    edges = graph["edges"]
    lines: list[str] = ["=== Graph-Nav Context ===", ""]
    for nid in node_ids:
        node = node_map.get(nid)
        if not node:
            continue
        lines += [
            f"Node: {nid}",
            f"  type={node['type']} loc={node['loc']} "
            f"in={node['in_degree']} out={node['out_degree']} file={node['file']}",
        ]
        imports_to = [e["target"] for e in edges if e["source"] == nid][:8]
        imports_from = [e["source"] for e in edges if e["target"] == nid][:8]
        if imports_to:
            lines.append(f"  → imports: {', '.join(imports_to)}")
        if imports_from:
            lines.append(f"  ← used by: {', '.join(imports_from)}")
        lines.append("")
    return "\n".join(lines)


def _report_lines(results: list[dict]) -> list[str]:
    avg = sum(r["saving_pct"] for r in results) / len(results) if results else 0.0
    status = "✅ TARGET MET" if avg >= 70 else "❌ BELOW TARGET"
    lines = [
        "# Token FinOps Report — Graph-Nav vs. Naive Ingestion",
        "", "## Executive Summary", "",
        "| Metric | Value |", "|--------|-------|",
        f"| Queries benchmarked | {len(results)} |",
        f"| Average token savings | **{avg:.1f}%** |",
        "| Target savings | ≥ 70% (aim 95%) |",
        f"| Status | {status} |",
        "", "## Query Results", "",
        "| ID | Question | Naive Tokens | Nav Tokens | Savings |",
        "|----|----------|-------------|------------|---------|",
    ]
    for r in results:
        q = (r["question"][:52] + "…") if len(r["question"]) > 52 else r["question"]
        lines.append(f"| {r['id']} | {q} | {r['naive_tokens']:,} "
                     f"| {r['nav_tokens']:,} | **{r['saving_pct']:.1f}%** |")
    lines += ["", "## Methodology", "",
              "- **Naive**: full source files concatenated for the query.",
              "- **Graph-nav**: node metadata + 1-hop edges from `vault/graph.json`.",
              "- **Token estimate**: `floor(char_count / 4)` (Anthropic standard).",
              "", "## Per-Query Detail", ""]
    for r in results:
        saved = r["naive_tokens"] - r["nav_tokens"]
        lines += [f"### {r['id']}: {r['question']}", "",
                  f"- Naive: {r['naive_chars']:,} chars → **{r['naive_tokens']:,} tokens**",
                  f"- Graph-nav: {r['nav_chars']:,} chars → **{r['nav_tokens']:,} tokens**",
                  f"- Saved: {saved:,} tokens (**{r['saving_pct']:.1f}%**)", ""]
    return lines


class FinOpsAnalyzer(LoggingMixin, TokenBudgetMixin):
    """Measures token savings of graph-nav context vs. raw file ingestion."""

    def __init__(self, repo_root: Path, graph_path: Path) -> None:
        self.repo_root = Path(repo_root)
        self._graph: dict = json.loads(Path(graph_path).read_text(encoding="utf-8"))
        self._queries: list[dict[str, Any]] = json.loads(
            Path(settings.finops_queries_path).read_text(encoding="utf-8")
        )

    def benchmark_query(self, query: dict) -> dict:
        naive = _naive_context(query["naive_files"], self.repo_root)
        nav = _graph_nav_context(query["node_ids"], self._graph)
        t_naive, t_nav = _tokens(naive), _tokens(nav)
        saving_pct = (t_naive - t_nav) / t_naive * 100 if t_naive else 0.0
        self.log.info("[FinOps] %s naive=%d nav=%d saving=%.1f%%",
                      query["id"], t_naive, t_nav, saving_pct)
        return {"id": query["id"], "question": query["question"],
                "naive_tokens": t_naive, "nav_tokens": t_nav,
                "saving_pct": round(saving_pct, 1),
                "naive_chars": len(naive), "nav_chars": len(nav)}

    def run_benchmarks(self, queries: list[dict] | None = None) -> list[dict]:
        return [self.benchmark_query(q) for q in (queries or self._queries)]

    def write_report(self, results: list[dict], path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(_report_lines(results)), encoding="utf-8")
        self.log.info("finops_report.md → %s", path)

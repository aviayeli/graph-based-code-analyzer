"""End-to-end Graphify pipeline.  Run with:  python -m src.pipeline"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

from src.config import settings
from src.differ import GraphDiffer
from src.exporter import GraphExporter
from src.fetcher import RepoFetcher
from src.finops import FinOpsAnalyzer
from src.graph import GraphBuilder
from src.mixins import LoggingMixin
from src.models import GraphMeta
from src.parser import ASTParser

# Paths are relative to the project root (where the command is invoked).
_WORKSPACE = Path("workspace/crewAI")
_SRC_ROOT = _WORKSPACE / "lib/crewai/src"
_CREWAI_PKG = _SRC_ROOT / "crewai"
_OUTPUT = Path("vault/graph.json")

_TARGET_URL = "https://github.com/crewAIInc/crewAI"


class Pipeline(LoggingMixin):
    """Orchestrates Fetch → Parse → Build → Export."""

    def run(self) -> dict[str, object]:  # pragma: no cover
        self.configure_root_logging(
            level=settings.log_level, fmt=settings.log_format
        )
        self.log.info("=== Graphify Pipeline START ===")

        # ── A: Fetch ───────────────────────────────────────────────────────
        fetcher = RepoFetcher(_CREWAI_PKG)
        files = fetcher.collect_files()
        sha = fetcher.get_sha()
        self.log.info("SHA: %s | files: %d", sha, len(files))

        # ── B: Parse ───────────────────────────────────────────────────────
        parser = ASTParser(src_root=_SRC_ROOT, repo_root=_WORKSPACE)
        nodes, edges = parser.parse_files(files, log_interval=100)
        self.log.info("Parsed: nodes=%d edges=%d", len(nodes), len(edges))

        # ── C: Build ───────────────────────────────────────────────────────
        builder = GraphBuilder(checkpoint_dir=settings.checkpoint_dir)
        builder.ingest(nodes, edges, interval=settings.checkpoint_interval_nodes)
        builder.compute_metrics()

        god_nodes = builder.get_god_nodes(n=10)
        self.log.info("Top god-nodes: %s", [g[0] for g in god_nodes[:5]])

        # ── D: Export ──────────────────────────────────────────────────────
        meta = GraphMeta(
            repo="crewAI",
            sha=sha,
            target_url=settings.target_repo_url or _TARGET_URL,
        )
        result = builder.write_json(_OUTPUT, meta)

        # ── E: Obsidian Vault ──────────────────────────────────────────────
        exporter = GraphExporter(result)
        exporter.write_index(_OUTPUT.parent / "index.md")
        exporter.write_hot(_OUTPUT.parent / "hot.md")

        # ── F: FinOps Benchmark ────────────────────────────────────────────
        finops = FinOpsAnalyzer(repo_root=_WORKSPACE, graph_path=_OUTPUT)
        benchmark_results = finops.run_benchmarks()
        finops.write_report(benchmark_results, Path("docs/finops_report.md"))

        # ── G: Graph Diff (God-node refactoring simulation) ────────────────
        differ = GraphDiffer(_OUTPUT)
        diff = differ.compute_diff()
        differ.write_diff_json(Path("vault/graph_diff.json"), diff)
        differ.write_report(Path("docs/refactor_report.md"), diff)

        self.log.info(
            "=== Pipeline DONE: %d nodes, %d edges ===",
            meta.total_nodes,
            meta.total_edges,
        )
        return result


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    Pipeline().run()

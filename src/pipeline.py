"""End-to-end Graphify pipeline.  Run with:  python -m src.pipeline"""
from __future__ import annotations

import logging
import sys

from src.config import settings
from src.differ import GraphDiffer
from src.exporter import GraphExporter
from src.fetcher import RepoFetcher
from src.finops import FinOpsAnalyzer
from src.graph import GraphBuilder
from src.mixins import LoggingMixin
from src.models import GraphMeta
from src.parser import ASTParser


class Pipeline(LoggingMixin):
    """Orchestrates Fetch → Parse → Build → Export."""

    def run(self) -> dict[str, object]:  # pragma: no cover
        self.configure_root_logging(
            level=settings.log_level, fmt=settings.log_format
        )
        self.log.info("=== Graphify Pipeline START ===")

        src_root = settings.workspace_dir / settings.repo_src_subdir
        pkg_root = src_root / settings.repo_pkg_name
        graph_out = settings.vault_path / "graph.json"

        # ── A: Fetch ───────────────────────────────────────────────────────
        fetcher = RepoFetcher(pkg_root)
        files = fetcher.collect_files()
        sha = fetcher.get_sha()
        self.log.info("SHA: %s | files: %d", sha, len(files))

        # ── B: Parse ───────────────────────────────────────────────────────
        parser = ASTParser(src_root=src_root, repo_root=settings.workspace_dir)
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
            repo=settings.repo_name or settings.target_repo_url.rstrip("/").split("/")[-1],
            sha=sha,
            target_url=settings.target_repo_url,
        )
        result = builder.write_json(graph_out, meta)

        # ── E: Obsidian Vault ──────────────────────────────────────────────
        exporter = GraphExporter(result)
        exporter.write_index(settings.vault_path / "index.md")
        exporter.write_hot(settings.vault_path / "hot.md")

        # ── F: FinOps Benchmark ────────────────────────────────────────────
        finops = FinOpsAnalyzer(repo_root=settings.workspace_dir, graph_path=graph_out)
        benchmark_results = finops.run_benchmarks()
        finops.write_report(benchmark_results, settings.docs_dir / "finops_report.md")

        # ── G: Graph Diff (God-node refactoring simulation) ────────────────
        differ = GraphDiffer(graph_out)
        diff = differ.compute_diff()
        differ.write_diff_json(settings.vault_path / "graph_diff.json", diff)
        differ.write_report(settings.docs_dir / "refactor_report.md", diff)

        self.log.info(
            "=== Pipeline DONE: %d nodes, %d edges ===",
            meta.total_nodes,
            meta.total_edges,
        )
        return result


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    Pipeline().run()

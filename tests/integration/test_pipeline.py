"""Integration test: parse → build → export against a minimal 3-file fixture repo."""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from src.config import settings as _settings
from src.fetcher import RepoFetcher
from src.graph import GraphBuilder
from src.models import GraphMeta
from src.parser import ASTParser
from src.pipeline import Pipeline

_MIN_FILES = 3


@pytest.fixture()
def fixture_repo(tmp_path: Path) -> Path:
    pkg = tmp_path / "mypkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("from .core import MyClass\n")
    (pkg / "core.py").write_text(
        textwrap.dedent("""\
            class MyClass:
                def method(self) -> None:
                    pass
        """)
    )
    (pkg / "utils.py").write_text(
        textwrap.dedent("""\
            from .core import MyClass

            def helper(obj: MyClass) -> str:
                return repr(obj)
        """)
    )
    return tmp_path


def test_parse_build_export(fixture_repo: Path, tmp_path: Path) -> None:
    pkg = fixture_repo / "mypkg"
    fetcher = RepoFetcher(pkg)
    files = fetcher.collect_files()
    assert len(files) >= _MIN_FILES

    parser = ASTParser(src_root=fixture_repo, repo_root=fixture_repo)
    nodes, edges = parser.parse_files(files)
    assert len(nodes) > 0

    builder = GraphBuilder(checkpoint_dir=tmp_path / ".ckpt")
    builder.ingest(nodes, edges)
    builder.compute_metrics()

    out = tmp_path / "graph.json"
    meta = GraphMeta(repo="mypkg", sha="abc123", target_url="")
    result = builder.write_json(out, meta)

    assert out.exists()
    data = json.loads(out.read_text())
    assert "nodes" in data and len(data["nodes"]) > 0
    assert result is not None


def test_pipeline_run_end_to_end(
    fixture_repo: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    vault = tmp_path / "vault"
    docs = tmp_path / "docs"
    ckpt = tmp_path / ".ckpt"
    for d in (vault, docs, ckpt):
        d.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(_settings, "workspace_dir", tmp_path)
    monkeypatch.setattr(_settings, "repo_src_subdir", ".")
    monkeypatch.setattr(_settings, "repo_pkg_name", "mypkg")
    monkeypatch.setattr(_settings, "vault_path", vault)
    monkeypatch.setattr(_settings, "docs_dir", docs)
    monkeypatch.setattr(_settings, "checkpoint_dir", ckpt)
    monkeypatch.setattr(_settings, "repo_name", "mypkg")
    monkeypatch.setattr(
        "src.finops.FinOpsAnalyzer.run_benchmarks",
        lambda self, queries=None: [],
    )

    Pipeline().run()

    assert (vault / "graph.json").exists()
    assert (vault / "index.md").exists()
    assert (vault / "hot.md").exists()
    assert (vault / "graph_diff.json").exists()
    assert (docs / "finops_report.md").exists()
    assert (docs / "refactor_report.md").exists()

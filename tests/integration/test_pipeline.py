"""Integration test: parse → build → export against a minimal 3-file fixture repo."""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from src.fetcher import RepoFetcher
from src.graph import GraphBuilder
from src.models import GraphMeta
from src.parser import ASTParser


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
    assert len(files) >= 3  # noqa: PLR2004

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

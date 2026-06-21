"""Tests for ASTParser — edge extraction (import, inherits) and error handling."""
from __future__ import annotations

from pathlib import Path

from src.models import EdgeKind, EdgeSource
from src.parser import ASTParser

_SOURCE = '''\
import os
from pathlib import Path
from crewai.task import Task

class MyAgent:
    role: str = "assistant"
    def run(self) -> None:
        pass

class SubAgent(MyAgent):
    async def execute(self) -> None:
        pass
'''

_SYNTAX_ERROR = "def foo(:\n    pass\n"


def _p(tmp_path: Path) -> tuple[ASTParser, Path]:
    src = tmp_path / "src"
    src.mkdir()
    return ASTParser(src_root=src, repo_root=tmp_path), src


def _w(src: Path, name: str, text: str) -> Path:
    f = src / name
    f.write_text(text, encoding="utf-8")
    return f


# ── import edges ──────────────────────────────────────────────────────────────

def test_import_from_edge_extracted(tmp_path: Path) -> None:
    parser, src = _p(tmp_path)
    _, edges = parser.parse_file(_w(src, "m.py", _SOURCE))
    targets = {e.target for e in edges if e.kind == EdgeKind.IMPORT}
    assert "crewai.task" in targets


def test_plain_import_edge_extracted(tmp_path: Path) -> None:
    parser, src = _p(tmp_path)
    _, edges = parser.parse_file(_w(src, "m.py", _SOURCE))
    targets = {e.target for e in edges if e.kind == EdgeKind.IMPORT}
    assert "os" in targets


def test_pathlib_import_captured(tmp_path: Path) -> None:
    parser, src = _p(tmp_path)
    _, edges = parser.parse_file(_w(src, "m.py", _SOURCE))
    targets = {e.target for e in edges if e.kind == EdgeKind.IMPORT}
    assert "pathlib" in targets


def test_self_import_not_added(tmp_path: Path) -> None:
    source = "from m import something\n"
    parser, src = _p(tmp_path)
    _, edges = parser.parse_file(_w(src, "m.py", source))
    import_targets = {e.target for e in edges if e.kind == EdgeKind.IMPORT}
    assert "m" not in import_targets


# ── inheritance edges ─────────────────────────────────────────────────────────

def test_inherits_edge_extracted(tmp_path: Path) -> None:
    parser, src = _p(tmp_path)
    _, edges = parser.parse_file(_w(src, "m.py", _SOURCE))
    pairs = [(e.source, e.target) for e in edges if e.kind == EdgeKind.INHERITS]
    assert ("m.SubAgent", "MyAgent") in pairs


def test_no_spurious_inherits_for_base_class(tmp_path: Path) -> None:
    parser, src = _p(tmp_path)
    _, edges = parser.parse_file(_w(src, "m.py", _SOURCE))
    inh_sources = {e.source for e in edges if e.kind == EdgeKind.INHERITS}
    assert "m.MyAgent" not in inh_sources  # no bases in _SOURCE


# ── evidence tag ──────────────────────────────────────────────────────────────

def test_all_edges_are_extracted(tmp_path: Path) -> None:
    parser, src = _p(tmp_path)
    _, edges = parser.parse_file(_w(src, "m.py", _SOURCE))
    assert all(e.evidence == EdgeSource.EXTRACTED for e in edges)


# ── error handling ────────────────────────────────────────────────────────────

def test_syntax_error_returns_empty(tmp_path: Path) -> None:
    parser, src = _p(tmp_path)
    nodes, edges = parser.parse_file(_w(src, "bad.py", _SYNTAX_ERROR))
    assert nodes == []
    assert edges == []

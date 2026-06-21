"""Tests for ASTParser — node extraction (module, class, function)."""
from __future__ import annotations

from pathlib import Path

from src.models import NodeType
from src.parser import ASTParser

_SOURCE = '''\
import os
from pathlib import Path
from crewai.task import Task

class MyAgent:
    """A simple agent."""
    role: str = "assistant"
    def run(self) -> None:
        pass

class SubAgent(MyAgent):
    async def execute(self) -> None:
        pass
'''


def _p(tmp_path: Path) -> tuple[ASTParser, Path]:
    src = tmp_path / "src"
    src.mkdir()
    return ASTParser(src_root=src, repo_root=tmp_path), src


def _w(src: Path, name: str, text: str) -> Path:
    f = src / name
    f.write_text(text, encoding="utf-8")
    return f


# ── module node ───────────────────────────────────────────────────────────────

def test_module_node_present(tmp_path: Path) -> None:
    parser, src = _p(tmp_path)
    f = _w(src, "mymod.py", _SOURCE)
    nodes, _ = parser.parse_file(f)
    assert "mymod" in {n.id for n in nodes}


def test_module_node_type(tmp_path: Path) -> None:
    parser, src = _p(tmp_path)
    f = _w(src, "mymod.py", _SOURCE)
    nodes, _ = parser.parse_file(f)
    mod = next(n for n in nodes if n.id == "mymod")
    assert mod.type == NodeType.MODULE


def test_init_module_strips_init(tmp_path: Path) -> None:
    parser, src = _p(tmp_path)
    pkg = src / "mypkg"
    pkg.mkdir()
    f = _w(pkg, "__init__.py", "class X:\n    pass\n")
    nodes, _ = parser.parse_file(f)
    ids = {n.id for n in nodes}
    assert "mypkg" in ids
    assert "mypkg.X" in ids


# ── class nodes ───────────────────────────────────────────────────────────────

def test_class_nodes_extracted(tmp_path: Path) -> None:
    parser, src = _p(tmp_path)
    f = _w(src, "mymod.py", _SOURCE)
    nodes, _ = parser.parse_file(f)
    ids = {n.id for n in nodes}
    assert "mymod.MyAgent" in ids
    assert "mymod.SubAgent" in ids


def test_class_node_type(tmp_path: Path) -> None:
    parser, src = _p(tmp_path)
    f = _w(src, "mymod.py", _SOURCE)
    nodes, _ = parser.parse_file(f)
    cls = next(n for n in nodes if n.id == "mymod.MyAgent")
    assert cls.type == NodeType.CLASS


# ── function nodes ────────────────────────────────────────────────────────────

def test_function_nodes_extracted(tmp_path: Path) -> None:
    parser, src = _p(tmp_path)
    f = _w(src, "mymod.py", _SOURCE)
    nodes, _ = parser.parse_file(f)
    ids = {n.id for n in nodes}
    assert "mymod.MyAgent.run" in ids
    assert "mymod.SubAgent.execute" in ids


def test_async_function_flagged(tmp_path: Path) -> None:
    parser, src = _p(tmp_path)
    f = _w(src, "mymod.py", _SOURCE)
    nodes, _ = parser.parse_file(f)
    n = next(n for n in nodes if n.id == "mymod.SubAgent.execute")
    assert n.is_async is True


def test_sync_function_not_async(tmp_path: Path) -> None:
    parser, src = _p(tmp_path)
    f = _w(src, "mymod.py", _SOURCE)
    nodes, _ = parser.parse_file(f)
    n = next(n for n in nodes if n.id == "mymod.MyAgent.run")
    assert n.is_async is False


def test_method_parent_class_set(tmp_path: Path) -> None:
    parser, src = _p(tmp_path)
    f = _w(src, "mymod.py", _SOURCE)
    nodes, _ = parser.parse_file(f)
    n = next(n for n in nodes if n.id == "mymod.MyAgent.run")
    assert n.parent_class == "MyAgent"


# ── multi-file ────────────────────────────────────────────────────────────────

def test_parse_files_aggregates(tmp_path: Path) -> None:
    parser, src = _p(tmp_path)
    f1 = _w(src, "mod_a.py", "class A:\n    pass\n")
    f2 = _w(src, "mod_b.py", "class B:\n    pass\n")
    nodes, _ = parser.parse_files([f1, f2])
    ids = {n.id for n in nodes}
    assert "mod_a.A" in ids
    assert "mod_b.B" in ids

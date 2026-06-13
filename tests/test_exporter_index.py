"""Tests for GraphExporter — module helpers, from_json, and index.md output."""
from __future__ import annotations

import json
from pathlib import Path

from src.exporter import GraphExporter, _score, _subdomain, _wl

# ── Shared fixture data ───────────────────────────────────────────────────────

_META = {
    "repo": "test_repo", "sha": "abc1234", "target_url": "",
    "generated_at": "2026-01-01T00:00:00+00:00",
    "total_nodes": 6, "total_edges": 3,
}


def _mk(nid: str, typ: str, name: str, module: str, ind: int, outd: int, loc: int = 50) -> dict:
    return {
        "id": nid, "type": typ, "name": name, "file": f"{nid}.py",
        "line": 1, "end_line": loc, "module": module, "parent_class": None,
        "is_async": False, "loc": loc, "in_degree": ind, "out_degree": outd,
    }


_NODES = [
    _mk("crewai.crew", "module", "crew", "crewai.crew", 17, 51, 2356),
    _mk("crewai.crew.Crew", "class", "Crew", "crewai.crew", 17, 51, 2356),
    _mk("crewai.task", "module", "task", "crewai.task", 40, 21, 1464),
    _mk("crewai.task.Task", "class", "Task", "crewai.task", 40, 21, 1464),
    _mk("crewai.agents.base", "module", "base", "crewai.agents", 35, 30, 900),
    _mk("crewai.agents.BaseAgent", "class", "BaseAgent", "crewai.agents", 35, 30, 900),
]

_GRAPH: dict = {"meta": _META, "nodes": _NODES, "edges": []}


def _exp() -> GraphExporter:
    return GraphExporter(_GRAPH)


# ── Module-level pure helpers ─────────────────────────────────────────────────

def test_wl_formats_wikilink() -> None:
    assert _wl("Crew") == "[[Crew]]"


def test_wl_preserves_spaces() -> None:
    assert _wl("My Node") == "[[My Node]]"


def test_score_sums_degrees() -> None:
    assert _score(_mk("a.X", "class", "X", "a", 3, 7)) == 10


def test_subdomain_two_parts() -> None:
    assert _subdomain("crewai.agents") == "agents"


def test_subdomain_deep_path() -> None:
    assert _subdomain("crewai.agents.crew_agent_executor") == "agents"


def test_subdomain_root_only() -> None:
    assert _subdomain("crewai") == "crewai"


# ── from_json ─────────────────────────────────────────────────────────────────

def test_from_json_loads_meta(tmp_path: Path) -> None:
    p = tmp_path / "graph.json"
    p.write_text(json.dumps(_GRAPH), encoding="utf-8")
    exp = GraphExporter.from_json(p)
    assert exp._meta["repo"] == "test_repo"


def test_from_json_loads_nodes(tmp_path: Path) -> None:
    p = tmp_path / "graph.json"
    p.write_text(json.dumps(_GRAPH), encoding="utf-8")
    exp = GraphExporter.from_json(p)
    assert len(exp._nodes) == 6


# ── write_index ───────────────────────────────────────────────────────────────

def test_write_index_creates_file(tmp_path: Path) -> None:
    _exp().write_index(tmp_path / "index.md")
    assert (tmp_path / "index.md").exists()


def test_index_contains_repo_name(tmp_path: Path) -> None:
    out = tmp_path / "index.md"
    _exp().write_index(out)
    assert "test_repo" in out.read_text()


def test_index_contains_sha(tmp_path: Path) -> None:
    out = tmp_path / "index.md"
    _exp().write_index(out)
    assert "abc1234" in out.read_text()


def test_index_wikilinks_class_names(tmp_path: Path) -> None:
    out = tmp_path / "index.md"
    _exp().write_index(out)
    content = out.read_text()
    assert "[[Crew]]" in content
    assert "[[Task]]" in content
    assert "[[BaseAgent]]" in content


def test_index_nav_links_hot(tmp_path: Path) -> None:
    out = tmp_path / "index.md"
    _exp().write_index(out)
    assert "[[hot]]" in out.read_text()


def test_index_nav_links_self(tmp_path: Path) -> None:
    out = tmp_path / "index.md"
    _exp().write_index(out)
    assert "[[index]]" in out.read_text()


def test_index_grouped_by_domain(tmp_path: Path) -> None:
    out = tmp_path / "index.md"
    _exp().write_index(out)
    content = out.read_text()
    assert "### agents" in content
    assert "### crew" in content
    assert "### task" in content


def test_index_class_count_in_header(tmp_path: Path) -> None:
    out = tmp_path / "index.md"
    _exp().write_index(out)
    assert "1 classes" in out.read_text()


def test_index_creates_parent_dirs(tmp_path: Path) -> None:
    out = tmp_path / "deep" / "vault" / "index.md"
    _exp().write_index(out)
    assert out.exists()


def test_index_overflow_message_shown(tmp_path: Path) -> None:
    # Build a domain with 12 classes to trigger the "…and N more" branch (line 89).
    many_nodes = [
        _mk(f"crewai.big.C{i}", "class", f"C{i}", "crewai.big", i, i)
        for i in range(12)
    ]
    graph = {**_GRAPH, "nodes": many_nodes}
    out = tmp_path / "index.md"
    GraphExporter(graph).write_index(out)
    assert "and 2 more" in out.read_text()

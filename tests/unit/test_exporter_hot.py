"""Tests for GraphExporter — hot.md god-node cache output."""
from __future__ import annotations

from pathlib import Path

from src.exporter import GraphExporter

# ── Minimal fixture ───────────────────────────────────────────────────────────

_META = {
    "repo": "myrepo", "sha": "deadbeef", "target_url": "",
    "generated_at": "2026-01-01T00:00:00+00:00",
    "total_nodes": 4, "total_edges": 2,
}


def _mk(nid: str, name: str, ind: int, outd: int, loc: int = 100) -> dict:
    return {
        "id": nid, "type": "module", "name": name, "file": f"{nid}.py",
        "line": 1, "end_line": loc, "module": nid, "parent_class": None,
        "is_async": False, "loc": loc, "in_degree": ind, "out_degree": outd,
    }


_NODES = [
    _mk("crewai.crew", "crew", 17, 51, 2356),   # score=68
    _mk("crewai.task", "task", 40, 21, 1464),   # score=61
    _mk("crewai.agents", "agents", 35, 30, 900), # score=65
    _mk("crewai.events", "events", 44, 10, 800), # score=54
]

_GRAPH: dict = {"meta": _META, "nodes": _NODES, "edges": []}


def _exp() -> GraphExporter:
    return GraphExporter(_GRAPH)


# ── write_hot ─────────────────────────────────────────────────────────────────

def test_write_hot_creates_file(tmp_path: Path) -> None:
    _exp().write_hot(tmp_path / "hot.md")
    assert (tmp_path / "hot.md").exists()


def test_hot_contains_repo_name(tmp_path: Path) -> None:
    out = tmp_path / "hot.md"
    _exp().write_hot(out)
    assert "myrepo" in out.read_text()


def test_hot_back_link_to_index(tmp_path: Path) -> None:
    out = tmp_path / "hot.md"
    _exp().write_hot(out)
    assert "[[index]]" in out.read_text()


def test_hot_wikilinks_node_names(tmp_path: Path) -> None:
    out = tmp_path / "hot.md"
    _exp().write_hot(out)
    content = out.read_text()
    assert "[[crew]]" in content or "[[task]]" in content


def test_hot_contains_table_headers(tmp_path: Path) -> None:
    out = tmp_path / "hot.md"
    _exp().write_hot(out)
    content = out.read_text()
    assert "| Rank |" in content
    assert "| Score |" in content
    assert "| LOC |" in content


def test_hot_top5_section_present(tmp_path: Path) -> None:
    out = tmp_path / "hot.md"
    _exp().write_hot(out)
    assert "Top 5 Architectural Bottlenecks" in out.read_text()


def test_hot_top_n_limits_rows(tmp_path: Path) -> None:
    out = tmp_path / "hot.md"
    _exp().write_hot(out, top_n=2)
    rows = [
        line for line in out.read_text().splitlines()
        if line.startswith("| ") and "Rank" not in line and "---" not in line
    ]
    assert len(rows) <= 2


def test_hot_score_present_in_table(tmp_path: Path) -> None:
    out = tmp_path / "hot.md"
    _exp().write_hot(out)
    content = out.read_text()
    # crew: in=17 out=51 → score=68
    assert "| 68 |" in content or "68" in content


def test_hot_zero_score_nodes_excluded(tmp_path: Path) -> None:
    zero_node: dict = {
        "id": "z.Zero", "type": "module", "name": "Zero", "file": "z.py",
        "line": 1, "end_line": 1, "module": "z", "parent_class": None,
        "is_async": False, "loc": 1, "in_degree": 0, "out_degree": 0,
    }
    graph = {**_GRAPH, "nodes": [*_NODES, zero_node]}
    out = tmp_path / "hot.md"
    GraphExporter(graph).write_hot(out, top_n=10)
    content = out.read_text()
    assert "[[Zero]]" not in content


def test_hot_creates_parent_dirs(tmp_path: Path) -> None:
    out = tmp_path / "nested" / "vault" / "hot.md"
    _exp().write_hot(out)
    assert out.exists()

"""Tests for GraphDiffer output methods and report-line helpers."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.differ import GraphDiffer, _mermaid, _refactor_lines

# ── Shared fixtures ───────────────────────────────────────────────────────────


def _mk(nid: str, in_d: int, out_d: int, loc: int = 100) -> dict:
    return {"id": nid, "type": "module", "name": nid.split(".")[-1],
            "file": f"{nid}.py", "in_degree": in_d, "out_degree": out_d, "loc": loc}


_GRAPH: dict = {
    "meta": {"repo": "crewai", "sha": "d80719d", "total_nodes": 2, "total_edges": 1},
    "nodes": [_mk("crewai.crew", 17, 51, 2356), _mk("crewai.task", 40, 21, 1464)],
    "edges": [{"source": "crewai.crew", "target": "crewai.task", "kind": "import"}],
}

_PLAN = [{
    "node_id": "crewai.crew",
    "issue": "out_degree too high",
    "extractions": [{"new_id": "crewai.crew_orchestrator",
                     "description": "Orchestration logic", "absorbed_out": 20}],
    "after_out_degree": 10,
    "after_loc": 500,
}]


def _minimal_diff() -> dict:
    return {
        "node_deltas": [{
            "node_id": "crewai.crew", "issue": "test",
            "before": {"in_degree": 17, "out_degree": 51, "loc": 2356, "score": 68},
            "after":  {"in_degree": 17, "out_degree": 15, "loc": 740, "score": 32},
            "delta":  {"in_degree": 0,  "out_degree": -36, "loc": -1616, "score": -36},
        }],
        "new_nodes": [{"id": "crewai.crew_orchestrator", "extracted_from": "crewai.crew",
                       "description": "Orchestration logic", "estimated_score": 23}],
        "summary": {"nodes_refactored": 1, "new_modules_created": 1,
                    "avg_score_before": 68.0, "avg_score_after": 32.0,
                    "avg_score_reduction": 36.0},
    }


@pytest.fixture()
def graph_file(tmp_path: Path) -> Path:
    p = tmp_path / "graph.json"
    p.write_text(json.dumps(_GRAPH), encoding="utf-8")
    return p


@pytest.fixture()
def differ(graph_file: Path) -> GraphDiffer:
    return GraphDiffer(graph_file)


# ── write_diff_json ───────────────────────────────────────────────────────────

def test_write_diff_json_valid_output(differ: GraphDiffer, tmp_path: Path) -> None:
    diff = differ.compute_diff(_PLAN)
    out = tmp_path / "vault" / "graph_diff.json"
    differ.write_diff_json(out, diff)
    loaded = json.loads(out.read_text())
    assert "node_deltas" in loaded
    assert loaded["meta"]["before_sha"] == "d80719d"


# ── write_report ──────────────────────────────────────────────────────────────

def test_write_report_content(differ: GraphDiffer, tmp_path: Path) -> None:
    diff = differ.compute_diff(_PLAN)
    out = tmp_path / "docs" / "refactor_report.md"
    differ.write_report(out, diff)
    content = out.read_text()
    assert "crewai.crew" in content
    assert "mermaid" in content
    assert "crewai.crew_orchestrator" in content


# ── _mermaid helper ───────────────────────────────────────────────────────────

def test_mermaid_has_before_subgraph() -> None:
    lines = _mermaid(_minimal_diff())
    assert any("BEFORE" in line for line in lines)


def test_mermaid_has_after_subgraph() -> None:
    lines = _mermaid(_minimal_diff())
    assert any("AFTER" in line for line in lines)


def test_mermaid_before_score() -> None:
    text = "\n".join(_mermaid(_minimal_diff()))
    assert "score=68" in text


def test_mermaid_after_score() -> None:
    text = "\n".join(_mermaid(_minimal_diff()))
    assert "score=32" in text


def test_mermaid_new_node_present() -> None:
    text = "\n".join(_mermaid(_minimal_diff()))
    assert "crew_orchestrator" in text


# ── _refactor_lines helper ────────────────────────────────────────────────────

def test_refactor_lines_has_summary() -> None:
    text = "\n".join(_refactor_lines(_minimal_diff()))
    assert "Summary" in text


def test_refactor_lines_has_new_modules_section() -> None:
    text = "\n".join(_refactor_lines(_minimal_diff()))
    assert "New Extracted Modules" in text


def test_refactor_lines_has_per_node_section() -> None:
    text = "\n".join(_refactor_lines(_minimal_diff()))
    assert "Per-Node Analysis" in text


def test_refactor_lines_shows_score_reduction() -> None:
    text = "\n".join(_refactor_lines(_minimal_diff()))
    assert "36.0" in text

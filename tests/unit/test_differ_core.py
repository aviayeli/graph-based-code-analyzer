"""Tests for GraphDiffer: construction and compute_diff delta logic."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.differ import GraphDiffer

# ── Fixtures ──────────────────────────────────────────────────────────────────


def _mk(nid: str, in_d: int, out_d: int, loc: int = 100) -> dict:
    return {"id": nid, "type": "module", "name": nid.split(".")[-1],
            "file": f"{nid}.py", "in_degree": in_d, "out_degree": out_d, "loc": loc}


_GRAPH: dict = {
    "meta": {"repo": "crewai", "sha": "d80719d", "total_nodes": 3, "total_edges": 2},
    "nodes": [
        _mk("crewai.crew", 17, 51, 2356),
        _mk("crewai.task", 40, 21, 1464),
        _mk("crewai.agent.core", 7, 43, 1953),
    ],
    "edges": [{"source": "crewai.crew", "target": "crewai.task", "kind": "import"},
              {"source": "crewai.crew", "target": "crewai.agent.core", "kind": "import"}],
}

_PLAN = [
    {
        "node_id": "crewai.crew",
        "issue": "out_degree too high",
        "extractions": [
            {"new_id": "crewai.crew_orchestrator", "description": "Orchestration logic",
             "absorbed_out": 20},
        ],
        "after_out_degree": 10,
        "after_loc": 500,
    },
]


@pytest.fixture()
def graph_file(tmp_path: Path) -> Path:
    p = tmp_path / "graph.json"
    p.write_text(json.dumps(_GRAPH), encoding="utf-8")
    return p


@pytest.fixture()
def differ(graph_file: Path) -> GraphDiffer:
    return GraphDiffer(graph_file)


# ── construction ──────────────────────────────────────────────────────────────

def test_differ_loads_sha(differ: GraphDiffer) -> None:
    assert differ._sha == "d80719d"


def test_differ_loads_nodes(differ: GraphDiffer) -> None:
    assert len(differ._graph["nodes"]) == 3


# ── compute_diff: structure ───────────────────────────────────────────────────

def test_compute_diff_top_level_keys(differ: GraphDiffer) -> None:
    diff = differ.compute_diff(_PLAN)
    for key in ("node_deltas", "new_nodes", "summary", "meta"):
        assert key in diff


def test_compute_diff_meta_shas(differ: GraphDiffer) -> None:
    diff = differ.compute_diff(_PLAN)
    assert diff["meta"]["before_sha"] == "d80719d"
    assert diff["meta"]["after_sha"] == "simulated"


# ── compute_diff: delta values ────────────────────────────────────────────────

def test_compute_diff_out_degree_delta(differ: GraphDiffer) -> None:
    diff = differ.compute_diff(_PLAN)
    delta = diff["node_deltas"][0]["delta"]
    assert delta["out_degree"] == 10 - 51


def test_compute_diff_loc_delta(differ: GraphDiffer) -> None:
    diff = differ.compute_diff(_PLAN)
    delta = diff["node_deltas"][0]["delta"]
    assert delta["loc"] == 500 - 2356


def test_compute_diff_score_before_and_after(differ: GraphDiffer) -> None:
    diff = differ.compute_diff(_PLAN)
    d = diff["node_deltas"][0]
    assert d["before"]["score"] == 17 + 51
    assert d["after"]["score"] < d["before"]["score"]


# ── compute_diff: new nodes ───────────────────────────────────────────────────

def test_compute_diff_new_node_attrs(differ: GraphDiffer) -> None:
    diff = differ.compute_diff(_PLAN)
    n = diff["new_nodes"][0]
    assert n["id"] == "crewai.crew_orchestrator"
    assert n["extracted_from"] == "crewai.crew"
    assert n["estimated_score"] == n["estimated_in"] + n["estimated_out"]


# ── compute_diff: summary ─────────────────────────────────────────────────────

def test_compute_diff_summary(differ: GraphDiffer) -> None:
    diff = differ.compute_diff(_PLAN)
    s = diff["summary"]
    assert s["nodes_refactored"] == 1
    assert s["new_modules_created"] == 1
    assert s["avg_score_reduction"] > 0


# ── compute_diff: edge cases ──────────────────────────────────────────────────

def test_compute_diff_missing_node_skipped(differ: GraphDiffer) -> None:
    plan = [{"node_id": "no.such.node", "issue": "x", "extractions": [],
             "after_out_degree": 5, "after_loc": 100}]
    diff = differ.compute_diff(plan)
    assert len(diff["node_deltas"]) == 0


def test_compute_diff_uses_default_plans(differ: GraphDiffer) -> None:
    diff = differ.compute_diff()
    assert len(diff["node_deltas"]) == 2

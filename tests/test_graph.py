"""Tests for GraphBuilder — ingest, metrics, god-node ranking, and export."""
from __future__ import annotations

import json
from pathlib import Path

from src.graph import GraphBuilder
from src.models import EdgeKind, EdgeSource, GraphMeta, NodeType, RawEdge, RawNode


def _node(nid: str, module: str = "a") -> RawNode:
    return RawNode(
        id=nid, type=NodeType.CLASS, name=nid.split(".")[-1],
        file=f"{module}.py", line=1, end_line=10, module=module, loc=10,
    )


def _edge(src: str, tgt: str, kind: EdgeKind = EdgeKind.INHERITS) -> RawEdge:
    return RawEdge(source=src, target=tgt, kind=kind, evidence=EdgeSource.EXTRACTED)


def _builder(tmp_path: Path) -> GraphBuilder:
    return GraphBuilder(checkpoint_dir=tmp_path / ".cp")


# ── ingest ────────────────────────────────────────────────────────────────────

def test_ingest_adds_nodes(tmp_path: Path) -> None:
    b = _builder(tmp_path)
    b.ingest([_node("a.Foo"), _node("a.Bar")], [])
    assert len(b._nodes) == 2


def test_ingest_internal_edge_kept(tmp_path: Path) -> None:
    b = _builder(tmp_path)
    nodes = [_node("a.Foo"), _node("a.Bar")]
    edges = [_edge("a.Foo", "a.Bar")]
    b.ingest(nodes, edges)
    assert len(b._edges) == 1


def test_ingest_external_edge_skipped(tmp_path: Path) -> None:
    b = _builder(tmp_path)
    nodes = [_node("a.Foo")]
    edges = [_edge("a.Foo", "pydantic.BaseModel", EdgeKind.INHERITS)]
    b.ingest(nodes, edges)
    assert len(b._edges) == 0  # target unknown → skipped


def test_ingest_checkpoint_created(tmp_path: Path) -> None:
    b = _builder(tmp_path)
    many_nodes = [_node(f"a.N{i}") for i in range(600)]
    b.ingest(many_nodes, [], interval=500)
    cp = (tmp_path / ".cp" / "graph_build.json")
    assert cp.exists()


# ── compute_metrics ───────────────────────────────────────────────────────────

def test_compute_metrics_updates_degrees(tmp_path: Path) -> None:
    b = _builder(tmp_path)
    nodes = [_node("a.X"), _node("a.Y"), _node("a.Z")]
    edges = [_edge("a.Z", "a.X"), _edge("a.Z", "a.Y")]
    b.ingest(nodes, edges)
    b.compute_metrics()
    assert b._nodes["a.Z"].out_degree == 2
    assert b._nodes["a.X"].in_degree == 1
    assert b._nodes["a.Y"].in_degree == 1


def test_compute_metrics_zero_for_isolated(tmp_path: Path) -> None:
    b = _builder(tmp_path)
    b.ingest([_node("a.Lone")], [])
    b.compute_metrics()
    assert b._nodes["a.Lone"].in_degree == 0
    assert b._nodes["a.Lone"].out_degree == 0


# ── get_god_nodes ─────────────────────────────────────────────────────────────

def test_get_god_nodes_ranking(tmp_path: Path) -> None:
    b = _builder(tmp_path)
    nodes = [_node("a.Hub"), _node("a.Spoke1"), _node("a.Spoke2"), _node("a.Leaf")]
    edges = [
        _edge("a.Spoke1", "a.Hub"),
        _edge("a.Spoke2", "a.Hub"),
        _edge("a.Hub", "a.Leaf"),
    ]
    b.ingest(nodes, edges)
    b.compute_metrics()
    god = b.get_god_nodes(n=1)
    assert god[0][0] == "a.Hub"  # in=2 out=1 → score=3


def test_get_god_nodes_capped_at_n(tmp_path: Path) -> None:
    b = _builder(tmp_path)
    b.ingest([_node(f"a.N{i}") for i in range(20)], [])
    b.compute_metrics()
    assert len(b.get_god_nodes(n=5)) == 5


# ── to_graph_dict / write_json ────────────────────────────────────────────────

def test_to_graph_dict_structure(tmp_path: Path) -> None:
    b = _builder(tmp_path)
    b.ingest([_node("a.Foo")], [])
    b.compute_metrics()
    meta = GraphMeta(repo="test", sha="abc")
    d = b.to_graph_dict(meta)
    assert set(d.keys()) == {"meta", "nodes", "edges"}
    assert d["meta"]["total_nodes"] == 1
    assert d["meta"]["total_edges"] == 0


def test_write_json_creates_file(tmp_path: Path) -> None:
    b = _builder(tmp_path)
    b.ingest([_node("a.Foo"), _node("a.Bar")], [_edge("a.Foo", "a.Bar")])
    b.compute_metrics()
    out = tmp_path / "graph.json"
    b.write_json(out, GraphMeta(repo="r", sha="s"))
    assert out.exists()
    loaded = json.loads(out.read_text())
    assert loaded["meta"]["total_nodes"] == 2
    assert loaded["meta"]["total_edges"] == 1


def test_write_json_creates_parent_dirs(tmp_path: Path) -> None:
    b = _builder(tmp_path)
    b.ingest([_node("a.X")], [])
    out = tmp_path / "deep" / "nested" / "graph.json"
    b.write_json(out, GraphMeta(repo="r", sha="s"))
    assert out.exists()

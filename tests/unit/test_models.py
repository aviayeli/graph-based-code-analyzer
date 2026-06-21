"""Tests for dataclasses and enums in src.models."""
from __future__ import annotations

from src.models import EdgeKind, EdgeSource, GraphMeta, NodeType, RawEdge, RawNode


def _node(**kw: object) -> RawNode:
    defaults: dict[str, object] = {
        "id": "a.Foo", "type": NodeType.CLASS, "name": "Foo", "file": "a.py",
        "line": 1, "end_line": 10, "module": "a", "loc": 10,
    }
    defaults.update(kw)
    return RawNode(**defaults)  # type: ignore[arg-type]


def _edge(**kw: object) -> RawEdge:
    defaults: dict[str, object] = {
        "source": "a.Foo", "target": "a.Bar", "kind": EdgeKind.INHERITS,
    }
    defaults.update(kw)
    return RawEdge(**defaults)  # type: ignore[arg-type]


# ── NodeType ──────────────────────────────────────────────────────────────────

def test_node_type_values() -> None:
    assert NodeType.MODULE.value == "module"
    assert NodeType.CLASS.value == "class"
    assert NodeType.FUNCTION.value == "function"


def test_edge_kind_values() -> None:
    assert EdgeKind.IMPORT.value == "import"
    assert EdgeKind.INHERITS.value == "inherits"
    assert EdgeKind.CALL.value == "call"


def test_edge_source_values() -> None:
    assert EdgeSource.EXTRACTED.value == "EXTRACTED"
    assert EdgeSource.INFERRED.value == "INFERRED"


# ── RawNode ───────────────────────────────────────────────────────────────────

def test_raw_node_as_dict_keys() -> None:
    d = _node().as_dict()
    assert set(d.keys()) == {
        "id", "type", "name", "file", "line", "end_line",
        "module", "parent_class", "is_async", "loc", "in_degree", "out_degree",
    }


def test_raw_node_as_dict_type_is_string() -> None:
    d = _node().as_dict()
    assert d["type"] == "class"


def test_raw_node_defaults() -> None:
    n = _node()
    assert n.parent_class is None
    assert n.is_async is False
    assert n.in_degree == 0
    assert n.out_degree == 0


def test_raw_node_parent_class() -> None:
    n = _node(parent_class="Parent")
    assert n.as_dict()["parent_class"] == "Parent"


def test_raw_node_async_function() -> None:
    n = _node(type=NodeType.FUNCTION, is_async=True)
    assert n.as_dict()["is_async"] is True


# ── RawEdge ───────────────────────────────────────────────────────────────────

def test_raw_edge_as_dict_keys() -> None:
    d = _edge().as_dict()
    assert set(d.keys()) == {"source", "target", "kind", "evidence"}


def test_raw_edge_default_evidence() -> None:
    d = _edge().as_dict()
    assert d["evidence"] == "EXTRACTED"


def test_raw_edge_inferred() -> None:
    e = _edge(evidence=EdgeSource.INFERRED)
    assert e.as_dict()["evidence"] == "INFERRED"


def test_raw_edge_kind_serialised() -> None:
    e = _edge(kind=EdgeKind.IMPORT)
    assert e.as_dict()["kind"] == "import"


# ── GraphMeta ─────────────────────────────────────────────────────────────────

def test_graph_meta_as_dict_keys() -> None:
    m = GraphMeta(repo="test", sha="abc123")
    d = m.as_dict()
    assert set(d.keys()) == {
        "repo", "sha", "target_url", "generated_at", "total_nodes", "total_edges"
    }


def test_graph_meta_defaults() -> None:
    m = GraphMeta(repo="r", sha="s")
    assert m.total_nodes == 0
    assert m.total_edges == 0
    assert m.target_url == ""


def test_graph_meta_generated_at_is_iso() -> None:
    m = GraphMeta(repo="r", sha="s")
    assert "T" in m.generated_at  # ISO 8601 contains a T separator

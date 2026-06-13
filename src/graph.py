from __future__ import annotations

import json
from pathlib import Path

import networkx as nx

from src.mixins import CheckpointMixin, LoggingMixin
from src.models import GraphMeta, RawEdge, RawNode


def _node_attrs(n: RawNode) -> dict[str, object]:
    return {"type": n.type.value, "file": n.file, "loc": n.loc, "module": n.module}


class GraphBuilder(LoggingMixin, CheckpointMixin):
    """Builds a weighted directed graph and computes structural metrics.

    Inherits ``CheckpointMixin`` to persist progress every *interval* nodes
    (Rule R2).  Only edges whose source AND target are known nodes are kept —
    external dependencies are filtered to keep graph.json focused on internal
    structure.
    """

    def __init__(self, checkpoint_dir: Path = Path(".checkpoints")) -> None:
        self.checkpoint_dir = checkpoint_dir
        self._graph: nx.DiGraph = nx.DiGraph()
        self._nodes: dict[str, RawNode] = {}
        self._edges: list[RawEdge] = []

    # ── ingestion ─────────────────────────────────────────────────────────

    def ingest(
        self,
        nodes: list[RawNode],
        edges: list[RawEdge],
        *,
        cp_name: str = "graph_build",
        interval: int = 500,
    ) -> None:
        total = len(nodes)
        for i, node in enumerate(nodes):
            self._graph.add_node(node.id, **_node_attrs(node))
            self._nodes[node.id] = node
            if (i + 1) % interval == 0:
                self.emit_progress(phase="ingest", completed=i + 1, total=total)
                self.save_checkpoint(cp_name, {"nodes_done": i + 1, "total": total})

        known = set(self._graph.nodes)
        skipped = 0
        for edge in edges:
            if edge.source not in known or edge.target not in known:
                skipped += 1
                continue
            self._graph.add_edge(
                edge.source,
                edge.target,
                kind=edge.kind.value,
                evidence=edge.evidence.value,
            )
            self._edges.append(edge)

        self.log.info(
            "Graph ingested: %d nodes, %d internal edges (%d external skipped)",
            len(self._graph),
            len(self._edges),
            skipped,
        )

    # ── metrics ───────────────────────────────────────────────────────────

    def compute_metrics(self) -> None:
        """Write in/out degree back onto each RawNode for serialisation."""
        for nid, node in self._nodes.items():
            node.in_degree = self._graph.in_degree(nid)
            node.out_degree = self._graph.out_degree(nid)
        self.log.info("Metrics computed for %d nodes", len(self._nodes))

    def get_god_nodes(self, n: int = 10) -> list[tuple[str, int]]:
        """Return top-*n* nodes ranked by combined in+out degree (god-node score)."""
        scored = {
            nid: self._graph.in_degree(nid) + self._graph.out_degree(nid)
            for nid in self._graph.nodes
        }
        return sorted(scored.items(), key=lambda x: x[1], reverse=True)[:n]

    # ── export ────────────────────────────────────────────────────────────

    def to_graph_dict(self, meta: GraphMeta) -> dict[str, object]:
        meta.total_nodes = len(self._nodes)
        meta.total_edges = len(self._edges)
        return {
            "meta": meta.as_dict(),
            "nodes": [n.as_dict() for n in self._nodes.values()],
            "edges": [e.as_dict() for e in self._edges],
        }

    def write_json(self, path: Path, meta: GraphMeta) -> dict[str, object]:
        """Serialise the graph to *path* and return the dict."""
        graph_dict = self.to_graph_dict(meta)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(graph_dict, indent=2), encoding="utf-8")
        self.log.info(
            "graph.json → %s  (%d nodes, %d edges)",
            path,
            meta.total_nodes,
            meta.total_edges,
        )
        return graph_dict

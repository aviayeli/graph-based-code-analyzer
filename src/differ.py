"""Graph Differ: before/after metrics for simulated God-node refactoring."""
from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from src.mixins import LoggingMixin

_PLANS: list[dict] = [
    {
        "node_id": "crewai.crew",
        "issue": "2,356 LOC, out_degree=51: orchestration + state + checkpoint all entangled",
        "extractions": [
            {"new_id": "crewai.crew_orchestrator", "description": "Sequential/hierarchical process scheduling", "absorbed_out": 22},
            {"new_id": "crewai.crew_checkpoint", "description": "Fork, restore, snapshot state management", "absorbed_out": 14},
        ],
        "after_out_degree": 15,
        "after_loc": 740,
    },
    {
        "node_id": "crewai.task",
        "issue": "1,464 LOC, in_degree=40: output handling and guardrails mixed into core",
        "extractions": [
            {"new_id": "crewai.task_output_handler", "description": "TaskOutput validation, output_file, guardrail logic", "absorbed_in": 25},
        ],
        "after_in_degree": 15,
        "after_loc": 580,
    },
]


def _node_map(graph: dict) -> dict[str, dict]:
    return {n["id"]: n for n in graph["nodes"]}


class GraphDiffer(LoggingMixin):
    """Computes before/after deltas for God-node refactoring simulations."""

    def __init__(self, graph_path: Path) -> None:
        raw = Path(graph_path).read_text(encoding="utf-8")
        self._graph: dict = json.loads(raw)
        self._sha: str = self._graph["meta"].get("sha", "unknown")

    def compute_diff(self, plans: list[dict] | None = None) -> dict:
        plans = plans or _PLANS
        nodes = _node_map(self._graph)
        node_deltas: list[dict] = []
        new_nodes: list[dict] = []
        for plan in plans:
            nid = plan["node_id"]
            node = nodes.get(nid)
            if not node:
                self.log.warning("node %s not found in graph — skipping", nid)
                continue
            before = {"in_degree": node["in_degree"], "out_degree": node["out_degree"],
                      "loc": node["loc"], "score": node["in_degree"] + node["out_degree"]}
            after_out = plan.get("after_out_degree", node["out_degree"])
            after_in = plan.get("after_in_degree", node["in_degree"])
            after_loc = plan.get("after_loc", node["loc"])
            after = {"in_degree": after_in, "out_degree": after_out,
                     "loc": after_loc, "score": after_in + after_out}
            delta = {k: after[k] - before[k] for k in before}
            node_deltas.append({"node_id": nid, "issue": plan["issue"],
                                 "before": before, "after": after, "delta": delta})
            for ext in plan.get("extractions", []):
                absorbed = ext.get("absorbed_out", ext.get("absorbed_in", 0))
                new_nodes.append({"id": ext["new_id"], "extracted_from": nid,
                                  "description": ext["description"],
                                  "estimated_in": absorbed, "estimated_out": 3,
                                  "estimated_score": absorbed + 3})

        avg_before = (sum(d["before"]["score"] for d in node_deltas)
                      / len(node_deltas) if node_deltas else 0.0)
        avg_after = (sum(d["after"]["score"] for d in node_deltas)
                     / len(node_deltas) if node_deltas else 0.0)
        return {
            "meta": {"before_sha": self._sha, "after_sha": "simulated",
                     "generated_at": datetime.now(UTC).isoformat(),
                     "description": "Simulated refactoring of top God-nodes"},
            "node_deltas": node_deltas,
            "new_nodes": new_nodes,
            "summary": {"nodes_refactored": len(node_deltas),
                        "new_modules_created": len(new_nodes),
                        "avg_score_before": round(avg_before, 1),
                        "avg_score_after": round(avg_after, 1),
                        "avg_score_reduction": round(avg_before - avg_after, 1)},
        }

    def write_diff_json(self, path: Path, diff: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(diff, indent=2), encoding="utf-8")
        self.log.info("graph_diff.json → %s (%d deltas)", path, len(diff["node_deltas"]))

    def write_report(self, path: Path, diff: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(_refactor_lines(diff)), encoding="utf-8")
        self.log.info("refactor_report.md → %s", path)


def _mermaid(diff: dict) -> list[str]:
    lines = ["```mermaid", "graph LR", "  subgraph BEFORE[Before Refactoring]"]
    for d in diff["node_deltas"]:
        b = d["before"]
        short = d["node_id"].split(".")[-1]
        lines.append(f"    {short}_b[\"{short}\\nout={b['out_degree']} "
                     f"in={b['in_degree']} score={b['score']}\"]")
    lines += ["  end", "  subgraph AFTER[After Refactoring]"]
    for d in diff["node_deltas"]:
        a = d["after"]
        short = d["node_id"].split(".")[-1]
        lines.append(f"    {short}_a[\"{short}\\nout={a['out_degree']} "
                     f"in={a['in_degree']} score={a['score']}\"]")
    for n in diff["new_nodes"]:
        short = n["id"].split(".")[-1]
        lines.append(f"    {short}[\"{short}\\nnew · score≈{n['estimated_score']}\"]")
    lines += ["  end", "```"]
    return lines


def _refactor_lines(diff: dict) -> list[str]:
    s = diff["summary"]
    lines = ["# God-Node Refactoring Report", "",
             "## Summary", "",
             "| Metric | Value |", "|--------|-------|",
             f"| Nodes refactored | {s['nodes_refactored']} |",
             f"| New modules created | {s['new_modules_created']} |",
             f"| Avg score before | {s['avg_score_before']} |",
             f"| Avg score after | {s['avg_score_after']} |",
             f"| Avg score reduction | **{s['avg_score_reduction']}** |",
             "", "## Before / After Architecture", ""]
    lines += _mermaid(diff)
    lines += ["", "## Per-Node Analysis", ""]
    for d in diff["node_deltas"]:
        b, a, delta = d["before"], d["after"], d["delta"]
        lines += [f"### `{d['node_id']}`", f"*{d['issue']}*", "",
                  "| Metric | Before | After | Δ |", "|--------|--------|-------|---|",
                  f"| Score | {b['score']} | {a['score']} | **{delta['score']}** |",
                  f"| in_degree | {b['in_degree']} | {a['in_degree']} | {delta['in_degree']} |",
                  f"| out_degree | {b['out_degree']} | {a['out_degree']} | {delta['out_degree']} |",
                  f"| LOC | {b['loc']:,} | {a['loc']:,} | {delta['loc']:,} |", ""]
    lines += ["## New Extracted Modules", ""]
    for n in diff["new_nodes"]:
        lines += [f"- **`{n['id']}`** — {n['description']}",
                  f"  extracted from `{n['extracted_from']}`, "
                  f"est. score ≈ {n['estimated_score']}"]
    return lines

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum


class NodeType(StrEnum):
    MODULE = "module"
    CLASS = "class"
    FUNCTION = "function"


class EdgeKind(StrEnum):
    IMPORT = "import"
    INHERITS = "inherits"
    CALL = "call"


class EdgeSource(StrEnum):
    EXTRACTED = "EXTRACTED"
    INFERRED = "INFERRED"


@dataclass
class RawNode:
    """One node in the code graph.  ``id`` is the canonical dotted path."""

    id: str
    type: NodeType
    name: str
    file: str        # repo-relative posix path
    line: int
    end_line: int
    module: str      # dotted module string, e.g. ``crewai.crew``
    parent_class: str | None = None
    is_async: bool = False
    loc: int = 0
    # Populated by GraphBuilder.compute_metrics():
    in_degree: int = 0
    out_degree: int = 0

    def as_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "type": self.type.value,
            "name": self.name,
            "file": self.file,
            "line": self.line,
            "end_line": self.end_line,
            "module": self.module,
            "parent_class": self.parent_class,
            "is_async": self.is_async,
            "loc": self.loc,
            "in_degree": self.in_degree,
            "out_degree": self.out_degree,
        }


@dataclass
class RawEdge:
    """One directed edge in the code graph."""

    source: str       # node id
    target: str       # node id
    kind: EdgeKind
    evidence: EdgeSource = EdgeSource.EXTRACTED

    def as_dict(self) -> dict[str, object]:
        return {
            "source": self.source,
            "target": self.target,
            "kind": self.kind.value,
            "evidence": self.evidence.value,
        }


@dataclass
class GraphMeta:
    """Top-level metadata block written into graph.json."""

    repo: str
    sha: str
    target_url: str = ""
    generated_at: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )
    total_nodes: int = 0
    total_edges: int = 0

    def as_dict(self) -> dict[str, object]:
        return {
            "repo": self.repo,
            "sha": self.sha,
            "target_url": self.target_url,
            "generated_at": self.generated_at,
            "total_nodes": self.total_nodes,
            "total_edges": self.total_edges,
        }

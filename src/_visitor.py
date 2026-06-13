"""Private AST visitor implementation — imported only by src.parser."""
from __future__ import annotations

import ast

from src.models import EdgeKind, EdgeSource, NodeType, RawEdge, RawNode


class _Visitor(ast.NodeVisitor):
    """Single-pass, context-tracking AST visitor.

    Produces ``EXTRACTED`` nodes and edges only — no LLM calls, no guessing.
    ``_class_stack`` tracks nesting so method ids are correctly qualified,
    e.g. ``crewai.crew.Crew.kickoff``.
    """

    def __init__(self, module: str, file_rel: str) -> None:
        self.module = module
        self.file = file_rel
        self.nodes: list[RawNode] = []
        self.edges: list[RawEdge] = []
        self._class_stack: list[str] = []

    # ── private helpers ───────────────────────────────────────────────────

    def _nid(self, name: str) -> str:
        return ".".join([self.module, *self._class_stack, name])

    def _make_node(
        self,
        ast_node: ast.AST,
        name: str,
        ntype: NodeType,
        *,
        is_async: bool = False,
    ) -> RawNode:
        start: int = ast_node.lineno  # type: ignore[attr-defined]
        end: int = getattr(ast_node, "end_lineno", start)
        return RawNode(
            id=self._nid(name),
            type=ntype,
            name=name,
            file=self.file,
            line=start,
            end_line=end,
            module=self.module,
            parent_class=self._class_stack[-1] if self._class_stack else None,
            is_async=is_async,
            loc=end - start + 1,
        )

    # ── visitors ──────────────────────────────────────────────────────────

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        rn = self._make_node(node, node.name, NodeType.CLASS)
        self.nodes.append(rn)
        for base in node.bases:
            base_name = ast.unparse(base).split(".")[-1]
            self.edges.append(
                RawEdge(source=rn.id, target=base_name,
                        kind=EdgeKind.INHERITS, evidence=EdgeSource.EXTRACTED)
            )
        self._class_stack.append(node.name)
        self.generic_visit(node)
        self._class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.nodes.append(self._make_node(node, node.name, NodeType.FUNCTION))
        # No generic_visit: nested defs are intentionally out of scope.

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.nodes.append(
            self._make_node(node, node.name, NodeType.FUNCTION, is_async=True)
        )

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        mod = node.module or ""
        if mod and mod != self.module:
            self.edges.append(
                RawEdge(source=self.module, target=mod,
                        kind=EdgeKind.IMPORT, evidence=EdgeSource.EXTRACTED)
            )

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            if alias.name != self.module:
                self.edges.append(
                    RawEdge(source=self.module, target=alias.name,
                            kind=EdgeKind.IMPORT, evidence=EdgeSource.EXTRACTED)
                )

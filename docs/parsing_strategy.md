# Graphify Parsing Strategy — crewAI

## 1. Scope Decision
Parse only `lib/crewai/src/crewai/` (497 files, 106,761 LOC).
Exclude: `tests/`, `__pycache__`, generated stubs.
Optional second pass: `lib/crewai-tools/` and `lib/crewai-core/` as satellite graphs.

## 2. Node Types

| Node Type | Source | Attributes |
|-----------|--------|------------|
| `module` | each `.py` file | path, LOC, domain |
| `class` | `ast.ClassDef` | name, file, line, bases, LOC (body end - start) |
| `function` | `ast.FunctionDef / AsyncFunctionDef` | name, file, line, is_async, parent_class |

## 3. Edge Types

| Edge Kind | Detected Via | AST Node |
|-----------|-------------|----------|
| `import` | module → module | `ast.Import`, `ast.ImportFrom` |
| `inherits` | class → class | `node.bases` in `ast.ClassDef` |
| `call` | function → function (best-effort) | `ast.Call` with `ast.Attribute`/`ast.Name` |
| `instantiates` | function → class | `ast.Call` where callee matches class name |

### Why call-edges are best-effort
Python call resolution is dynamic (duck typing, late binding). We use name-matching heuristics:
- If `node.func.id` matches a known class/function name in the registry → add edge.
- Attribute calls (`self.method()`) are resolved by parent class lookup.
- Unresolvable calls are logged but not dropped (they go into `unresolved_calls` metadata).

## 4. Metric Computation (Phase 5 — GraphBuilder)

| Metric | Method | Library |
|--------|--------|---------|
| LOC | `end_lineno - lineno` from AST node | stdlib `ast` |
| Cyclomatic complexity | McCabe complexity | `radon.complexity.cc_visit` |
| In-degree | count of incoming edges | `networkx.DiGraph.in_degree` |
| Out-degree | count of outgoing edges | `networkx.DiGraph.out_degree` |
| Betweenness centrality | shortest-path centrality | `networkx.betweenness_centrality` |
| God-node score | `in_degree + out_degree + complexity` (weighted) | computed |

## 5. Obsidian Output Rules

### graph.json
- One entry per node; edges as `[source_id, target_id, kind]` triples.
- `id` format: `domain.ClassName` or `domain.module.function_name`.
- Validated against `src/schemas/graph_schema.json` before write.

### index.md
- Grouped by domain (directory prefix).
- Each class → `[[ClassName]]` wikilink with LOC and in-degree annotation.
- Each class lists its methods as sub-bullets.

### hot.md
- Top-30 nodes sorted by God-node score (descending).
- Columns: Rank, Node, Score, Complexity, In-Degree, Out-Degree, File, LOC.
- Marked CRITICAL (score > 75th percentile), HIGH, MEDIUM.

## 6. Parsing Order (respects token budget R1)
1. File walk → collect all `Path` objects (no I/O cost).
2. AST parse each file → emit `RawNode` + `RawEdge` dataclasses (no LLM).
3. GraphBuilder: construct `nx.DiGraph`, compute metrics (no LLM).
4. GraphExporter: serialize + validate (no LLM).
5. LLMAnalyzer (Bonus D only): query graph-nav context → LLM call with token logging.

**Total estimated LLM tokens for core pipeline: 0** (pure AST + graph math).
LLM calls reserved for Bonus D (FinOps benchmark) and Bonus E (R&D analysis).

## 7. Known Parsing Challenges

| Challenge | Mitigation |
|-----------|-----------|
| Dynamic imports (`importlib`) | Flag as unresolved; do not fabricate edges |
| Pydantic model fields (not methods) | Parse `model_fields` as node attributes, not edges |
| `__init__.py` re-exports | Treat as pass-through; attribute imports to source module |
| 3,873-LOC `flow/runtime/__init__.py` | Parse normally; flag as God-file in hot.md |
| `TypedDict` / `NamedTuple` subclasses | Include as class nodes; tag type=data_model |

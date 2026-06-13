# PLAN — System Architecture & Flow

## 1. High-Level Architecture

```
[Target Repo URL]
       │
       ▼
 ┌─────────────┐
 │  RepoFetcher │  clone → temp dir (read-only)
 └──────┬──────┘
        │ file tree
        ▼
 ┌─────────────┐
 │  ASTParser  │  per-file AST walk (ast / tree-sitter)
 └──────┬──────┘
        │ raw nodes + edges
        ▼
 ┌──────────────┐
 │ GraphBuilder │  nx.DiGraph construction + metric computation
 └──────┬───────┘
        │ enriched graph
        ├──────────────────────────────┐
        ▼                              ▼
 ┌──────────────┐              ┌───────────────┐
 │GraphExporter │              │  LLMAnalyzer  │
 │  graph.json  │              │ (graph-nav)   │
 │  index.md    │              └──────┬────────┘
 │  hot.md      │                     │
 └──────────────┘               finops / rnd reports
```

## 2. Module Breakdown

### 2.1 `src/fetcher.py` — RepoFetcher
- Clones the target repo into `tmp/<repo-name>/` using `subprocess` + `git clone --depth=1`.
- Walks the tree, returns a list of `Path` objects filtered by language extension.
- **Mixin**: `LoggingMixin` (emits structured log lines with timestamps).

### 2.2 `src/parser.py` — ASTParser
- Uses Python `ast` module for `.py` files; `tree-sitter` bindings for TS/Go/Rust (optional).
- Extracts: module name, class definitions, function definitions, import statements, function calls.
- Returns a list of `RawNode` and `RawEdge` dataclasses.
- **Mixin**: `TokenBudgetMixin` (tracks tokens if an LLM call is embedded for docstring extraction).

### 2.3 `src/graph.py` — GraphBuilder
- Ingests `RawNode`/`RawEdge` lists; builds `nx.DiGraph`.
- Computes per-node metrics: LOC, cyclomatic complexity (via `radon`), in-degree, out-degree, betweenness centrality.
- Identifies God-nodes: top-N by `in_degree + out_degree`.
- **Mixin**: `CheckpointMixin` (emits progress after each 500-node batch).

### 2.4 `src/exporter.py` — GraphExporter
- Serializes graph to `graph.json` (schema: `{nodes: [...], edges: [...], meta: {...}}`).
- Renders `index.md` — one `[[wikilink]]` per node, grouped by module.
- Renders `hot.md` — sorted heat-map table (complexity × coupling score).
- Validates all outputs against JSON Schema / markdown schema before write.

### 2.5 `src/llm.py` — LLMAnalyzer
- Wraps Anthropic `claude-sonnet-4-6` via the `anthropic` SDK.
- **Graph-nav mode**: extracts hot nodes + 1-hop subgraph context; feeds to LLM.
- **Naive mode**: feeds raw file contents (benchmark only).
- Logs exact input/output token counts per call.
- **Mixin**: `TokenBudgetMixin` (hard-stops at 8,000 input tokens; raises if exceeded).

### 2.6 `src/diff.py` — GraphDiffer (Bonus C)
- Loads two `graph.json` files (before/after refactor).
- Computes delta per node: Δin-degree, Δout-degree, Δcomplexity.
- Outputs `graph_diff.json` and Mermaid diagram string.

### 2.7 `src/rnd.py` — RnDAnalyzer (Bonus E)
- Runs Louvain / greedy-modularity community detection on the graph.
- Calls `git log --format=...` to map file → primary author.
- Cross-references community membership with author map → bottleneck table.

### 2.8 `src/cli.py` — Entry Point
- `argparse` CLI: `graphify <repo-url> [--vault-path PATH] [--lang python|ts|go] [--naive-bench]`.
- Orchestrates all modules sequentially with checkpoint logging.

## 3. Data Schemas

### graph.json
```json
{
  "meta": { "repo": "str", "sha": "str", "generated_at": "ISO8601", "total_nodes": 0, "total_edges": 0 },
  "nodes": [{ "id": "str", "type": "module|class|function", "file": "str", "line": 0,
               "loc": 0, "complexity": 0, "in_degree": 0, "out_degree": 0 }],
  "edges": [{ "source": "str", "target": "str", "kind": "call|import|inherit" }]
}
```

### index.md structure
```
# Index — <repo>
## <module>
- [[ClassName]]
  - [[method_name]]
```

### hot.md structure
```
| Rank | Node | Complexity | In-Degree | Out-Degree | Score |
|------|------|-----------|-----------|-----------|-------|
```

## 4. CI/CD Flow (Bonus B)

```
push to main
  └─ github-actions: graphify.yml
       ├─ pip install -e .
       ├─ python -m graphify $TARGET_REPO_URL
       ├─ upload-artifact: graph.json, index.md, hot.md
       └─ check: no Python file > 150 lines (wc -l guard)
```

## 5. Mixin Hierarchy

```
LoggingMixin          ← all classes inherit
TokenBudgetMixin      ← ASTParser, LLMAnalyzer
CheckpointMixin       ← GraphBuilder, LLMAnalyzer
```

All Mixins are pure (no `__init__` state); they inject methods only.

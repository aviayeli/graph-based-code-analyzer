# graph-based-code-analyzer — Master Index

> Karpathy LLM wiki pattern. Start here. See [hot.md](hot.md) for the most recent session context.

## Purpose

Reverse-engineer large OSS repositories using AST-based graph analysis. Produces Obsidian-ready knowledge artifacts and proves FinOps savings from graph-guided LLM navigation. Primary target: [crewAI](https://github.com/crewAIInc/crewAI).

---

## Pipeline (A → G)

```
RepoFetcher → ASTParser → GraphBuilder → GraphExporter
                                       → FinOpsAnalyzer
                                       → GraphDiffer
```

| Stage | Module | Responsibility |
|-------|--------|---------------|
| A — Fetch | `src/fetcher.py` | Collect `.py` files from a cloned repo; resolve commit SHA |
| B — Parse | `src/parser.py` + `src/_visitor.py` | Walk AST; emit `RawNode` / `RawEdge` lists |
| C — Build | `src/graph.py` | Ingest nodes/edges into `networkx`; compute metrics; checkpoint |
| D — Export JSON | `src/graph.py` `GraphBuilder.write_json()` | Serialise `graph.json` with `GraphMeta` header |
| E — Obsidian Vault | `src/exporter.py` | Write `vault/index.md` and `vault/hot.md` |
| F — FinOps | `src/finops.py` | Benchmark token cost: raw-file vs graph-guided navigation |
| G — Diff | `src/differ.py` | Simulate god-node refactoring; write `vault/graph_diff.json` + `docs/refactor_report.md` |

Entry point: `python -m src.pipeline`

---

## Module Map

| File | Role |
|------|------|
| `src/models.py` | Shared data types (`RawNode`, `RawEdge`, `GraphMeta`, enums) |
| `src/config.py` | Pydantic `Settings` loaded from env / `.env` |
| `src/pipeline.py` | `Pipeline` orchestrator — the only file that imports all others |
| `src/parser.py` | `ASTParser` — drives `_visitor.py` over file lists |
| `src/_visitor.py` | `ast.NodeVisitor` subclass; extracts nodes and edges |
| `src/graph.py` | `GraphBuilder` — networkx graph, metrics, god-node ranking, JSON output |
| `src/exporter.py` | `GraphExporter` — renders `index.md` and `hot.md` from graph data |
| `src/fetcher.py` | `RepoFetcher` — filesystem walker + git SHA resolver |
| `src/finops.py` | `FinOpsAnalyzer` — token cost benchmarks, Markdown report |
| `src/differ.py` | `GraphDiffer` — detects high-degree nodes; simulates split; reports delta |
| `src/vuln03_crew.py` | Autonomous CrewAI workflow that produced the VULN-03 patch |

Mixin utilities live in `src/mixins.py` (logging, token tracking).

---

## Key Data Types (`src/models.py`)

| Type | Description |
|------|-------------|
| `RawNode` | One symbol: `id` (dotted path), `type` (module/class/function), `file`, `line`, metrics |
| `RawEdge` | Directed edge: `source → target`, `kind` (import/inherits/call), `evidence` |
| `GraphMeta` | JSON header: `repo`, `sha`, `target_url`, `generated_at`, `total_nodes/edges` |
| `NodeType` | StrEnum: `module`, `class`, `function` |
| `EdgeKind` | StrEnum: `import`, `inherits`, `call` |
| `EdgeSource` | StrEnum: `EXTRACTED`, `INFERRED` |

---

## Output Artifacts

| Path | Producer | Contents |
|------|----------|----------|
| `vault/graph.json` | `GraphBuilder.write_json()` | Full serialised graph |
| `vault/index.md` | `GraphExporter.write_index()` | Obsidian master index |
| `vault/hot.md` | `GraphExporter.write_hot()` | Hot cache (recent context) |
| `docs/finops_report.md` | `FinOpsAnalyzer.write_report()` | Token-cost comparison table |
| `docs/refactor_report.md` | `GraphDiffer.write_report()` | God-node refactor simulation |
| `graphify-out/graph.json` | Graphify CLI | Knowledge graph of *this* repo |

---

## Architecture Constraints (from CLAUDE.md)

- **R1** — 8 k token ceiling per LLM call; graph paths replace raw ingestion.
- **R7** — No `src/` file may exceed 150 lines; CI enforces with `wc -l`.
- **R8** — All imports must appear in `pyproject.toml` with a pinned version range.
- Data flows strictly: `GraphBuilder → GraphExporter → output files`.
- OOP with Mixins for cross-cutting concerns; tests in `tests/`; coverage ≥ 80 %.

---

## Navigation

- **Recent work / hot context** → [hot.md](hot.md)
- **PRD & requirements** → [docs/PRD.md](docs/PRD.md)
- **FinOps analysis** → [docs/finops_report.md](docs/finops_report.md)
- **Refactor simulation** → [docs/refactor_report.md](docs/refactor_report.md)
- **Security sign-off** → [security_signoff_report.md](security_signoff_report.md)
- **Graph browser** → `graphify-out/graph.html`
- **Graphify commands** → `graphify query "<q>"` · `graphify path "<A>" "<B>"` · `graphify explain "<concept>"`

# CLAUDE.md — graph-based-code-analyzer

## Project
Reverse-engineer large OSS repositories using AST-based graph analysis, output Obsidian-ready knowledge artifacts, and prove FinOps savings from graph-guided LLM navigation.

## Karpathy's 4 Core Rules

1. **Think Before Coding** — Fully understand the problem before writing a line. Read relevant code, trace call paths, form a mental model. If the plan is fuzzy, stop and clarify.
2. **Simplicity First** — Choose the simplest correct implementation. Prefer stdlib over dependencies, flat over nested, explicit over clever. Add complexity only when simplicity demonstrably fails.
3. **Surgical Changes** — Modify only what the task requires. No collateral refactors, no opportunistic cleanups. One PR, one concern.
4. **Goal-Driven Execution** — Every action maps to a stated requirement. If an action cannot be traced to a PRD line or TODO item, do not take it.

## 8 Agent-Specific Rules

### R1 — Hard Token Budgets
Every LLM call must declare an estimated token cost before execution. Default ceiling: 8,000 input tokens per call. Graph-navigation paths replace raw file ingestion; raw ingestion requires explicit approval.

### R2 — Checkpoints for Long Operations
Any operation >30 seconds or >5 LLM calls must emit a progress checkpoint to stdout (phase name, % complete, tokens used so far) before proceeding to the next step.

### R3 — No Non-Language Tasks
The agent analyses Python/TypeScript/Go/Rust ASTs only. It does not parse binary files, images, compiled artifacts, or generated protobuf stubs unless explicitly scoped.

### R4 — Schema Validation
All structured outputs (`graph.json`, `index.md`, `hot.md`) must be validated against their declared schema before writing to disk. Invalid output raises a hard error; silent truncation is forbidden.

### R5 — HITL for External/Destructive Actions
Any action that writes to a remote system (GitHub push, Obsidian vault write, external API call) or deletes local files requires explicit human-in-the-loop confirmation before execution.

### R6 — Immutable Inputs
Source repository files are read-only during analysis. The agent clones into a temp dir and never modifies the original working tree of the target repo.

### R7 — 150-Line File Budget
No Python source file in this project may exceed 150 lines. Functionality that would breach this limit must be extracted into a Mixin or a new module. CI enforces this with `wc -l`.

### R8 — Explicit Dependency Declaration
Every external library used must appear in `pyproject.toml` with a pinned version range. Transitive-only dependencies must not be imported directly.

## Conventions
- Python >=3.12; type hints on all public functions.
- OOP with Mixins for cross-cutting concerns (logging, token tracking, caching).
- Tests in `tests/`; coverage fail_under = 85 for core modules.
- All graph data flows through `GraphBuilder` → `GraphExporter` → output files.
- Commit messages: `type(scope): short description` (conventional commits).

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

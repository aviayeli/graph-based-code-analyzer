# PRD — Graph-Based Code Analyzer
**Homework 4: Reverse Engineering with Graphify & Obsidian**
**Target grade: 100/100 + all advanced bonuses**

---

## 1. Problem Statement

Large codebases are opaque. Onboarding engineers waste weeks tracing call graphs manually. LLM-assisted analysis naively ingests raw files, burning tokens on irrelevant code. This project builds a graph-based reverse-engineering pipeline that turns any OSS repository into a navigable knowledge architecture — and proves the FinOps savings of doing so.

---

## 2. Base Requirements (graded core)

| ID | Requirement |
|----|-------------|
| BR-1 | Accept a GitHub repository URL as input |
| BR-2 | Parse all Python (and optionally TS/Go) source files via AST |
| BR-3 | Build a directed call/dependency graph (nodes = modules/classes/functions; edges = calls/imports) |
| BR-4 | Output `graph.json` — machine-readable graph with node metadata (LOC, cyclomatic complexity, in-degree, out-degree) |
| BR-5 | Output `index.md` — Obsidian-ready index of all nodes with backlinks |
| BR-6 | Output `hot.md` — ranked list of hot-spots: highest in-degree, highest complexity, cross-module coupling |
| BR-7 | Target repository must exceed **10,000 lines of code** |
| BR-8 | All Python source files in this project ≤ 150 lines (enforced by CI) |
| BR-9 | OOP design using Mixin pattern for cross-cutting concerns |

---

## 3. Dr. Segal's Advanced Bonuses

### Bonus A — Obsidian Vault Integration
- `index.md` uses `[[wikilink]]` syntax so Obsidian renders the graph natively.
- `hot.md` includes a heat-map table sortable by complexity, coupling, and change-frequency.
- All three output files land in a configurable `--vault-path` directory.

### Bonus B — GitHub Actions CI/CD
- `.github/workflows/graphify.yml` runs the analyzer on every push to `main`.
- Workflow artifacts: `graph.json`, `index.md`, `hot.md` uploaded per-run.
- Badge in `README.md` showing last-run status.

### Bonus C — Before/After Graph Diff (Architectural Refactoring)
- Identify the top-3 God-nodes (highest in-degree + out-degree combined) in the target repo.
- Propose and document a refactoring plan per node (extract interface, introduce mediator, etc.).
- Re-run the analyzer on the refactored snapshot; output `graph_diff.json` showing delta metrics.
- Visualize delta as a Mermaid diagram in `docs/refactor_report.md`.

### Bonus D — Token FinOps Proof
- Instrument every LLM call with exact input/output token counts.
- Run two benchmarks on the same analytical question:
  1. **Naive**: feed raw source files to the LLM.
  2. **Graph-nav**: feed only graph-extracted context (hot nodes + 1-hop neighbors).
- Output `docs/finops_report.md` with token counts, cost estimates (at current Anthropic pricing), and % savings.
- Savings target: ≥ 70% token reduction for equivalent answer quality.

### Bonus E — R&D Management Analysis
- Cluster the graph by connected components and betweenness-centrality communities.
- Map clusters to likely team/domain ownership (heuristic: directory prefix + commit-author analysis via `git log`).
- Identify human bottlenecks: nodes with high betweenness owned by a single author.
- Output `docs/rnd_report.md` with bottleneck table and recommended ownership redistributions.

---

## 4. Non-Requirements (explicitly out of scope)
- No UI / web dashboard (CLI only for this homework).
- No real-time streaming analysis.
- No support for binary or compiled artifacts.

---

## 5. Success Metrics

| Metric | Target |
|--------|--------|
| Graph node coverage | ≥ 95% of non-test Python files parsed |
| Token savings (Bonus D) | ≥ 70% vs naive ingestion |
| CI pipeline green | Pass on every push |
| File size budget | 0 Python files > 150 lines |
| Output schema validity | 100% (all outputs validate against schema) |

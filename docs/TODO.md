# TODO — Implementation Phases

## Phase 0 — Project Bootstrap ✅
- [x] Create `CLAUDE.md` with Karpathy rules + agent rules
- [x] Create `docs/PRD.md`
- [x] Create `docs/PLAN.md`
- [x] Create `docs/TODO.md`
- [x] Confirm `pyproject.toml` scaffold exists

---

## Phase 1 — Target Repository Selection 🔲 ← **START HERE**
- [ ] **Receive target repo URL from user** (must be >10,000 LOC, Python-primary)
- [ ] Run `tokei` or `cloc` on the repo to confirm LOC count ≥ 10,000
- [ ] Document repo name, URL, primary language, and rough module count in `docs/target.md`
- [ ] Perform a quick manual graph sketch: identify 3–5 likely God-nodes by eye
- [ ] Confirm repo is publicly accessible (no auth required for clone)

---

## Phase 2 — Core Infrastructure
- [ ] Finalize `pyproject.toml`: pin `networkx`, `radon`, `anthropic`, `jsonschema`, `tree-sitter` (optional)
- [ ] Implement `LoggingMixin` in `src/mixins/logging.py`
- [ ] Implement `TokenBudgetMixin` in `src/mixins/token_budget.py`
- [ ] Implement `CheckpointMixin` in `src/mixins/checkpoint.py`
- [ ] Write unit tests for all three Mixins (`tests/test_mixins.py`)

---

## Phase 3 — Repo Fetcher
- [ ] Implement `RepoFetcher` in `src/fetcher.py`
  - [ ] `clone(url) → Path` — shallow clone into temp dir
  - [ ] `collect_files(root, exts) → list[Path]` — filtered file walk
  - [ ] `cleanup()` — remove temp dir on exit
- [ ] Test with a small public repo (<500 LOC) as smoke test

---

## Phase 4 — AST Parser
- [ ] Implement `ASTParser` in `src/parser.py`
  - [ ] `parse_file(path) → tuple[list[RawNode], list[RawEdge]]`
  - [ ] Handle import resolution (relative vs absolute)
  - [ ] Extract: modules, classes, functions, calls, inheritance
- [ ] Define `RawNode` and `RawEdge` dataclasses in `src/models.py`
- [ ] Test on target repo's largest file — confirm node/edge counts are reasonable

---

## Phase 5 — Graph Builder
- [ ] Implement `GraphBuilder` in `src/graph.py`
  - [ ] `build(nodes, edges) → nx.DiGraph`
  - [ ] `compute_metrics(graph) → nx.DiGraph` — attach LOC, complexity, centrality
  - [ ] `get_god_nodes(graph, n=3) → list[str]`
- [ ] Checkpoint every 500 nodes (via `CheckpointMixin`)
- [ ] Test: verify in-degree + out-degree sums match edge count

---

## Phase 6 — Graph Exporter + Schema Validation
- [ ] Define JSON Schema for `graph.json` in `src/schemas/graph_schema.json`
- [ ] Implement `GraphExporter` in `src/exporter.py`
  - [ ] `to_json(graph, path)` — serialize + validate
  - [ ] `to_index_md(graph, path)` — Obsidian wikilinks
  - [ ] `to_hot_md(graph, path)` — heat-map table
- [ ] Run full pipeline on target repo; inspect outputs manually in Obsidian

---

## Phase 7 — CLI Entry Point
- [ ] Implement `src/cli.py` with `argparse`
- [ ] Wire all phases: fetch → parse → build → export
- [ ] Add `--vault-path` and `--lang` flags
- [ ] End-to-end test on target repo; time the run

---

## Phase 8 — Bonus B: GitHub Actions CI/CD
- [ ] Create `.github/workflows/graphify.yml`
  - [ ] Trigger: push to `main`
  - [ ] Steps: checkout, install, run graphify, upload artifacts
  - [ ] LOC guard: `find src -name "*.py" | xargs wc -l | awk '$1 > 150 {exit 1}'`
- [ ] Add CI badge to `README.md`
- [ ] Verify workflow runs green on first push

---

## Phase 9 — Bonus C: Graph Diff (Architectural Refactoring)
- [ ] Document refactoring plan for top-3 God-nodes in `docs/refactor_plan.md`
- [ ] Apply minimal refactoring to a fork/branch of the target repo
- [ ] Implement `GraphDiffer` in `src/diff.py`
- [ ] Generate `graph_diff.json` and Mermaid diagram
- [ ] Write `docs/refactor_report.md`

---

## Phase 10 — Bonus D: Token FinOps Proof
- [ ] Select 3 analytical questions about the target repo
- [ ] Run naive benchmark: raw file ingestion per question — log tokens
- [ ] Run graph-nav benchmark: hot-node context per question — log tokens
- [ ] Compute savings % and cost delta (using current Anthropic pricing)
- [ ] Write `docs/finops_report.md` with full table + conclusion

---

## Phase 11 — Bonus E: R&D Management Analysis
- [ ] Run community detection (Louvain) on `nx.DiGraph`
- [ ] Run `git log` author mapping on target repo
- [ ] Cross-reference communities → author ownership → bottleneck table
- [ ] Write `docs/rnd_report.md` with recommendations

---

## Phase 12 — Polish & Submission
- [ ] Confirm all Python files ≤ 150 lines
- [ ] Confirm test coverage ≥ 80% for `src/` modules
- [ ] Final end-to-end run — all 3 outputs valid + Obsidian vault loads correctly
- [ ] Write `README.md` with setup instructions, usage examples, and output samples
- [ ] Tag release `v1.0.0` and submit

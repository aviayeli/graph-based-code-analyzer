# TODO — Implementation Phases

## Phase 0 — Project Bootstrap ✅
- [x] Create `CLAUDE.md` with Karpathy rules + agent rules (R1–R8)
- [x] Create `docs/PRD.md` (BR-1–BR-9 + Bonuses A–E)
- [x] Create `docs/PLAN.md` (module breakdown + Mixin hierarchy)
- [x] Create `docs/TODO.md`
- [x] Confirm `pyproject.toml` scaffold exists

---

## Phase 1 — Target Repository Selection ✅
- [x] Target repo selected: **crewAIInc/crewAI** (https://github.com/crewAIInc/crewAI)
- [x] Cloned to `workspace/crewAI/`
- [x] Confirmed: 497 Python files, 106,761 LOC, 855 classes — satisfies >10K bonus
- [x] Top God-nodes identified by eye: `crew.py`, `task.py`, `agent/core.py`
- [x] Repo publicly accessible (no auth)

---

## Phase 2 — Core Infrastructure ✅
- [x] Finalized `pyproject.toml`: pinned `networkx`, `anthropic`, `jsonschema`, `pydantic-settings`, `radon`
- [x] Implemented `LoggingMixin` — `cached_property` logger, `configure_root_logging()`
- [x] Implemented `TokenBudgetMixin` — hard 8K token ceiling, `_CallRecord`, cost tracking
- [x] Implemented `CheckpointMixin` — atomic JSON writes (tmp→rename), `emit_progress()`
- [x] Implemented `Settings` (Pydantic `BaseSettings`) in `src/config.py`
- [x] Unit tests for all Mixins and Settings (`tests/test_mixins.py`, `tests/test_config.py`)
- [x] Ruff clean · Coverage ≥ 85% · All files ≤ 150 lines

---

## Phase 3 — Core Graphify Pipeline ✅
- [x] Defined `RawNode`, `RawEdge`, `GraphMeta` dataclasses in `src/models.py`
- [x] Implemented `RepoFetcher` in `src/fetcher.py`
- [x] Implemented `ASTParser` + `_Visitor` in `src/parser.py` + `src/_visitor.py`
- [x] Implemented `GraphBuilder` in `src/graph.py` (checkpoint every 500 nodes)
- [x] Implemented `Pipeline` in `src/pipeline.py`
- [x] Generated `vault/graph.json`: 4,256 nodes, 1,463 internal edges, 0 LLM tokens

---

## Phase 4 — Obsidian Exporter ✅
- [x] Implemented `GraphExporter` in `src/exporter.py`
- [x] Generated `vault/index.md` (316 lines, 26 domain sections, `[[wikilinks]]`)
- [x] Generated `vault/hot.md` (65 lines, top-30 god-node table)
- [x] Cross-navigation: `[[hot]]` ↔ `[[index]]`
- [x] All tests passing, coverage ≥ 85%

---

## Phase 5 — FinOps Proof + Graph Diff ✅  *(Bonuses C + D)*
- [x] Implemented `FinOpsAnalyzer` in `src/finops.py`
  - [x] 3 analytical queries benchmarked: Q1 99.2%, Q2 98.6%, Q3 98.9% savings
  - [x] Average token savings: **98.9%** (target ≥ 70%)
  - [x] Generated `docs/finops_report.md`
- [x] Implemented `GraphDiffer` in `src/differ.py`
  - [x] Simulated refactoring of `crewai.crew` (score 68→32) and `crewai.task` (score 61→36)
  - [x] Proposed 3 new extracted modules
  - [x] Generated `vault/graph_diff.json`
  - [x] Generated `docs/refactor_report.md` with Mermaid before/after diagram
- [x] 168 tests, 99.03% coverage, ruff clean, all files ≤ 150 lines

---

## Phase 6 — README & Submission Prep ✅
- [x] Finalized `README.md` — executive summary with all required sections
- [x] FinOps results table embedded
- [x] God-node Mermaid diagram embedded
- [x] Obsidian screenshot placeholder added
- [x] `.gitignore` verified: `workspace/` excluded, `vault/*.md` and `vault/*.json` tracked
- [x] Final quality gates passed: ruff clean, 168 tests, 99.03% coverage

---

## Phase 7 — Bonus B: GitHub Actions CI/CD ⬜ *(pending)*
- [ ] Create `.github/workflows/graphify.yml`
  - [ ] Trigger: push to `main`
  - [ ] Steps: checkout → install → `ruff check` → `pytest --cov` → LOC guard
  - [ ] LOC guard: `find src -name "*.py" | xargs wc -l | awk '$1 > 150 {exit 1}'`
- [ ] Add CI badge to `README.md`

---

## Phase 8 — Bonus E: R&D Management Analysis ⬜ *(pending)*
- [ ] Run Louvain community detection on `nx.DiGraph`
- [ ] Run `git log` author mapping on `workspace/crewAI`
- [ ] Cross-reference communities → author ownership → bottleneck table
- [ ] Write `docs/rnd_report.md`

---

## Phase 9 — Tag & Submit ⬜
- [ ] Insert Obsidian Graph View screenshots into `README.md`
- [ ] Tag release `v1.0.0`
- [ ] Submit

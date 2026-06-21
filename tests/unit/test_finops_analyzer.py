"""Tests for FinOpsAnalyzer class: benchmark_query, run_benchmarks, write_report."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.finops import FinOpsAnalyzer

# ── Fixtures ──────────────────────────────────────────────────────────────────


def _mk(nid: str, in_d: int, out_d: int, loc: int = 100) -> dict:
    return {"id": nid, "type": "module", "name": nid.split(".")[-1],
            "file": f"{nid}.py", "in_degree": in_d, "out_degree": out_d, "loc": loc}


_GRAPH: dict = {
    "meta": {"repo": "test", "sha": "abc", "total_nodes": 2, "total_edges": 1},
    "nodes": [_mk("crewai.crew", 17, 51, 2356), _mk("crewai.task", 40, 21, 1464)],
    "edges": [{"source": "crewai.crew", "target": "crewai.task",
               "kind": "import", "evidence": "EXTRACTED"}],
}

_QUERY: dict = {
    "id": "q_test",
    "question": "How does Crew orchestrate tasks?",
    "naive_files": ["lib/crewai/src/crewai/crew.py"],
    "node_ids": ["crewai.crew", "crewai.task"],
}


@pytest.fixture()
def graph_file(tmp_path: Path) -> Path:
    p = tmp_path / "graph.json"
    p.write_text(json.dumps(_GRAPH), encoding="utf-8")
    return p


@pytest.fixture()
def repo_root(tmp_path: Path) -> Path:
    src = tmp_path / "lib" / "crewai" / "src" / "crewai" / "crew.py"
    src.parent.mkdir(parents=True)
    src.write_text("class Crew:\n    pass\n" * 100, encoding="utf-8")
    return tmp_path


@pytest.fixture()
def analyzer(repo_root: Path, graph_file: Path) -> FinOpsAnalyzer:
    return FinOpsAnalyzer(repo_root, graph_file)


# ── benchmark_query ───────────────────────────────────────────────────────────

def test_benchmark_query_returns_dict(analyzer: FinOpsAnalyzer) -> None:
    result = analyzer.benchmark_query(_QUERY)
    assert isinstance(result, dict)


def test_benchmark_query_id_matches(analyzer: FinOpsAnalyzer) -> None:
    assert analyzer.benchmark_query(_QUERY)["id"] == "q_test"


def test_benchmark_query_question_matches(analyzer: FinOpsAnalyzer) -> None:
    assert "Crew" in analyzer.benchmark_query(_QUERY)["question"]


def test_benchmark_query_has_token_counts(analyzer: FinOpsAnalyzer) -> None:
    r = analyzer.benchmark_query(_QUERY)
    assert r["naive_tokens"] > 0
    assert r["nav_tokens"] > 0


def test_benchmark_query_naive_larger_than_nav(analyzer: FinOpsAnalyzer) -> None:
    r = analyzer.benchmark_query(_QUERY)
    assert r["naive_tokens"] > r["nav_tokens"]


def test_benchmark_query_saving_pct_positive(analyzer: FinOpsAnalyzer) -> None:
    assert analyzer.benchmark_query(_QUERY)["saving_pct"] > 0


def test_benchmark_query_saving_pct_below_100(analyzer: FinOpsAnalyzer) -> None:
    assert analyzer.benchmark_query(_QUERY)["saving_pct"] < 100


def test_benchmark_query_has_char_counts(analyzer: FinOpsAnalyzer) -> None:
    r = analyzer.benchmark_query(_QUERY)
    assert "naive_chars" in r and "nav_chars" in r


def test_benchmark_query_no_naive_files(analyzer: FinOpsAnalyzer) -> None:
    q = {**_QUERY, "naive_files": []}
    r = analyzer.benchmark_query(q)
    assert r["naive_tokens"] == 1


# ── run_benchmarks ────────────────────────────────────────────────────────────

def test_run_benchmarks_custom_queries(analyzer: FinOpsAnalyzer) -> None:
    results = analyzer.run_benchmarks([_QUERY])
    assert len(results) == 1


def test_run_benchmarks_multiple_queries(analyzer: FinOpsAnalyzer) -> None:
    q2 = {**_QUERY, "id": "q2"}
    results = analyzer.run_benchmarks([_QUERY, q2])
    assert len(results) == 2


def test_run_benchmarks_ids_preserved(analyzer: FinOpsAnalyzer) -> None:
    q2 = {**_QUERY, "id": "q_other"}
    results = analyzer.run_benchmarks([_QUERY, q2])
    ids = {r["id"] for r in results}
    assert "q_test" in ids and "q_other" in ids


# ── write_report ──────────────────────────────────────────────────────────────

_MOCK_RESULTS = [{"id": "q1", "question": "How?", "naive_tokens": 10000,
                  "nav_tokens": 200, "saving_pct": 98.0,
                  "naive_chars": 40000, "nav_chars": 800}]


def test_write_report_creates_file(analyzer: FinOpsAnalyzer, tmp_path: Path) -> None:
    out = tmp_path / "docs" / "finops_report.md"
    analyzer.write_report(_MOCK_RESULTS, out)
    assert out.exists()


def test_write_report_target_met(analyzer: FinOpsAnalyzer, tmp_path: Path) -> None:
    out = tmp_path / "finops_report.md"
    analyzer.write_report(_MOCK_RESULTS, out)
    assert "TARGET MET" in out.read_text()


def test_write_report_contains_query_id(analyzer: FinOpsAnalyzer, tmp_path: Path) -> None:
    out = tmp_path / "finops_report.md"
    analyzer.write_report(_MOCK_RESULTS, out)
    assert "q1" in out.read_text()


def test_write_report_creates_parent_dirs(analyzer: FinOpsAnalyzer, tmp_path: Path) -> None:
    out = tmp_path / "deep" / "nested" / "report.md"
    analyzer.write_report(_MOCK_RESULTS, out)
    assert out.exists()

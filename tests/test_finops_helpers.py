"""Tests for finops module-level helpers: token estimator, context builders, report."""
from __future__ import annotations

from pathlib import Path

from src.finops import _graph_nav_context, _naive_context, _report_lines, _tokens

# ── Shared graph fixture ───────────────────────────────────────────────────────

def _mk(nid: str, in_d: int, out_d: int, loc: int = 100) -> dict:
    return {"id": nid, "type": "module", "name": nid.split(".")[-1],
            "file": f"{nid}.py", "in_degree": in_d, "out_degree": out_d, "loc": loc}


_GRAPH: dict = {
    "meta": {"repo": "test", "sha": "abc"},
    "nodes": [_mk("crewai.crew", 17, 51, 2356), _mk("crewai.task", 40, 21, 1464)],
    "edges": [{"source": "crewai.crew", "target": "crewai.task",
               "kind": "import", "evidence": "EXTRACTED"}],
}


# ── _tokens ───────────────────────────────────────────────────────────────────

def test_tokens_empty_returns_one() -> None:
    assert _tokens("") == 1


def test_tokens_four_chars_is_one() -> None:
    assert _tokens("abcd") == 1


def test_tokens_eight_chars_is_two() -> None:
    assert _tokens("abcdefgh") == 2


def test_tokens_scales_with_length() -> None:
    assert _tokens("a" * 4000) == 1000


# ── _naive_context ────────────────────────────────────────────────────────────

def test_naive_context_reads_file(tmp_path: Path) -> None:
    f = tmp_path / "lib" / "crewai" / "src" / "crewai" / "crew.py"
    f.parent.mkdir(parents=True)
    f.write_text("class Crew: pass\n", encoding="utf-8")
    ctx = _naive_context(["lib/crewai/src/crewai/crew.py"], tmp_path)
    assert "class Crew" in ctx


def test_naive_context_skips_missing(tmp_path: Path) -> None:
    ctx = _naive_context(["no_such_file.py"], tmp_path)
    assert ctx == ""


def test_naive_context_concatenates(tmp_path: Path) -> None:
    (tmp_path / "a.py").write_text("# A\n", encoding="utf-8")
    (tmp_path / "b.py").write_text("# B\n", encoding="utf-8")
    ctx = _naive_context([str(tmp_path / "a.py"), str(tmp_path / "b.py")], Path("/"))
    assert "# A" in ctx and "# B" in ctx


def test_naive_context_includes_filename_header(tmp_path: Path) -> None:
    f = tmp_path / "crew.py"
    f.write_text("pass\n", encoding="utf-8")
    ctx = _naive_context([str(f)], Path("/"))
    assert "crew.py" in ctx


# ── _graph_nav_context ────────────────────────────────────────────────────────

def test_graph_nav_has_header() -> None:
    assert "Graph-Nav Context" in _graph_nav_context(["crewai.crew"], _GRAPH)


def test_graph_nav_includes_in_degree() -> None:
    assert "in=17" in _graph_nav_context(["crewai.crew"], _GRAPH)


def test_graph_nav_includes_out_degree() -> None:
    assert "out=51" in _graph_nav_context(["crewai.crew"], _GRAPH)


def test_graph_nav_shows_import_targets() -> None:
    ctx = _graph_nav_context(["crewai.crew"], _GRAPH)
    assert "crewai.task" in ctx


def test_graph_nav_shows_used_by() -> None:
    ctx = _graph_nav_context(["crewai.task"], _GRAPH)
    assert "crewai.crew" in ctx


def test_graph_nav_skips_unknown_node() -> None:
    ctx = _graph_nav_context(["no.such.node"], _GRAPH)
    assert "no.such.node" not in ctx


def test_graph_nav_multiple_nodes() -> None:
    ctx = _graph_nav_context(["crewai.crew", "crewai.task"], _GRAPH)
    assert "crewai.crew" in ctx and "crewai.task" in ctx


# ── _report_lines ─────────────────────────────────────────────────────────────

_RESULTS = [{"id": "q1", "question": "How?", "naive_tokens": 10000,
             "nav_tokens": 200, "saving_pct": 98.0,
             "naive_chars": 40000, "nav_chars": 800}]


def test_report_lines_target_met() -> None:
    text = "\n".join(_report_lines(_RESULTS))
    assert "TARGET MET" in text


def test_report_lines_below_target() -> None:
    poor = [{**_RESULTS[0], "saving_pct": 50.0}]
    text = "\n".join(_report_lines(poor))
    assert "BELOW TARGET" in text


def test_report_lines_empty_no_crash() -> None:
    lines = _report_lines([])
    assert any("0" in line for line in lines)


def test_report_lines_has_methodology() -> None:
    text = "\n".join(_report_lines(_RESULTS))
    assert "Methodology" in text

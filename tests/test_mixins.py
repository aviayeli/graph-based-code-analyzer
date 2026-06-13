"""Unit tests for the three core Mixins — no LLM calls, no I/O side-effects."""
from __future__ import annotations

import logging
from pathlib import Path

import pytest

from src.mixins import CheckpointMixin, LoggingMixin, TokenBudgetMixin
from src.mixins.token_budget_mixin import TokenBudgetExceededError

# ── Helpers ───────────────────────────────────────────────────────────────────

class _Logged(LoggingMixin):
    pass


class _Budgeted(TokenBudgetMixin):
    pass


class _Checkpointed(CheckpointMixin):
    def __init__(self, tmp_path: Path) -> None:
        self.checkpoint_dir = tmp_path


# ── LoggingMixin ──────────────────────────────────────────────────────────────

def test_logging_mixin_returns_logger() -> None:
    obj = _Logged()
    assert isinstance(obj.log, logging.Logger)


def test_logging_mixin_name_scoped() -> None:
    obj = _Logged()
    assert "_Logged" in obj.log.name


def test_logging_mixin_cached_property() -> None:
    obj = _Logged()
    assert obj.log is obj.log  # same instance on repeat access


# ── TokenBudgetMixin ──────────────────────────────────────────────────────────

def test_track_tokens_accumulates() -> None:
    b = _Budgeted()
    b.track_tokens(model="test-model", tokens_in=100, tokens_out=50)
    b.track_tokens(model="test-model", tokens_in=200, tokens_out=80)
    assert b.session_tokens_in == 300
    assert b.session_tokens_out == 130


def test_session_cost_calculation() -> None:
    b = _Budgeted()
    b.configure_budget(hard_limit_input=8000, cost_per_m_input=3.00, cost_per_m_output=15.00)
    b.track_tokens(model="test-model", tokens_in=1_000_000, tokens_out=1_000_000)
    assert abs(b.session_cost_usd - 18.00) < 0.001


def test_assert_within_budget_passes() -> None:
    b = _Budgeted()
    b.configure_budget(hard_limit_input=8000, cost_per_m_input=3.0, cost_per_m_output=15.0)
    b.assert_within_budget(7999)  # must not raise


def test_assert_within_budget_raises() -> None:
    b = _Budgeted()
    b.configure_budget(hard_limit_input=8000, cost_per_m_input=3.0, cost_per_m_output=15.0)
    with pytest.raises(TokenBudgetExceededError):
        b.assert_within_budget(8001)


def test_session_summary_structure() -> None:
    b = _Budgeted()
    b.track_tokens(model="m", tokens_in=10, tokens_out=5)
    summary = b.session_summary()
    assert set(summary.keys()) == {"calls", "tokens_in", "tokens_out", "cost_usd"}
    assert summary["calls"] == 1


def test_fresh_instance_zero_state() -> None:
    b = _Budgeted()
    assert b.session_tokens_in == 0
    assert b.session_tokens_out == 0
    assert b.session_cost_usd == 0.0


# ── CheckpointMixin ───────────────────────────────────────────────────────────

def test_save_and_load_checkpoint(tmp_path: Path) -> None:
    c = _Checkpointed(tmp_path)
    data = {"phase": "test", "nodes": 42}
    c.save_checkpoint("phase1", data)
    loaded = c.load_checkpoint("phase1")
    assert loaded is not None
    assert loaded["phase"] == "test"
    assert loaded["nodes"] == 42


def test_load_missing_checkpoint_returns_none(tmp_path: Path) -> None:
    c = _Checkpointed(tmp_path)
    assert c.load_checkpoint("nonexistent") is None


def test_clear_checkpoint(tmp_path: Path) -> None:
    c = _Checkpointed(tmp_path)
    c.save_checkpoint("x", {"v": 1})
    c.clear_checkpoint("x")
    assert c.load_checkpoint("x") is None


def test_emit_progress_does_not_raise(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    c = _Checkpointed(tmp_path)
    with caplog.at_level(logging.INFO, logger="graphify.CheckpointMixin"):
        c.emit_progress(phase="graph_build", completed=250, total=500, tokens_used=0)
    assert "50.0%" in caplog.text


def test_checkpoint_atomic_write_survives_existing_file(tmp_path: Path) -> None:
    c = _Checkpointed(tmp_path)
    c.save_checkpoint("atomic", {"v": 1})
    c.save_checkpoint("atomic", {"v": 2})  # overwrite
    loaded = c.load_checkpoint("atomic")
    assert loaded is not None
    assert loaded["v"] == 2

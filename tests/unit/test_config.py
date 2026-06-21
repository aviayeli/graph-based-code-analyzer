"""Tests for Settings config — validates defaults, path coercion, and properties."""
from __future__ import annotations

import logging
from pathlib import Path

from src.config import Settings
from src.mixins.logging_mixin import LoggingMixin

# ── Settings defaults ─────────────────────────────────────────────────────────

def test_settings_default_llm_model() -> None:
    s = Settings()
    assert s.llm_model == "claude-sonnet-4-6"


def test_settings_default_token_budget() -> None:
    s = Settings()
    assert s.token_budget_input == 8000
    assert s.token_budget_output == 4096


def test_settings_default_log_level() -> None:
    s = Settings()
    assert s.log_level == "INFO"


def test_settings_default_checkpoint_interval() -> None:
    s = Settings()
    assert s.checkpoint_interval_nodes == 500


def test_settings_default_max_file_loc() -> None:
    s = Settings()
    assert s.max_file_loc == 150


def test_settings_path_coercion() -> None:
    s = Settings(workspace_dir="my_workspace")  # type: ignore[call-arg]
    assert isinstance(s.workspace_dir, Path)
    assert s.workspace_dir == Path("my_workspace")


def test_settings_vault_path_is_path() -> None:
    s = Settings()
    assert isinstance(s.vault_path, Path)


def test_settings_checkpoint_dir_is_path() -> None:
    s = Settings()
    assert isinstance(s.checkpoint_dir, Path)


def test_settings_cost_defaults() -> None:
    s = Settings()
    assert s.cost_per_m_input_usd == 3.00
    assert s.cost_per_m_output_usd == 15.00


def test_settings_env_override(monkeypatch: object) -> None:
    monkeypatch.setenv("LLM_MODEL", "claude-haiku-4-5-20251001")  # type: ignore[attr-defined]
    s = Settings()
    assert s.llm_model == "claude-haiku-4-5-20251001"


def test_settings_vault_path_abs_creates_dir(tmp_path: Path, monkeypatch: object) -> None:
    monkeypatch.chdir(tmp_path)  # type: ignore[attr-defined]
    s = Settings(vault_path=tmp_path / "vault_test")  # type: ignore[call-arg]
    created = s.vault_path_abs
    assert created.exists()


def test_settings_checkpoint_dir_abs_creates_dir(tmp_path: Path, monkeypatch: object) -> None:
    monkeypatch.chdir(tmp_path)  # type: ignore[attr-defined]
    s = Settings(checkpoint_dir=tmp_path / "cp_test")  # type: ignore[call-arg]
    created = s.checkpoint_dir_abs
    assert created.exists()


# ── LoggingMixin.configure_root_logging ───────────────────────────────────────

class _L(LoggingMixin):
    pass


def test_configure_root_logging_sets_level() -> None:
    obj = _L()
    # Reset root logger state so the test is deterministic.
    root = logging.getLogger()
    original_handlers = root.handlers[:]
    original_level = root.level
    root.handlers.clear()

    obj.configure_root_logging(level="DEBUG")
    assert root.level == logging.DEBUG

    # Restore so other tests are not polluted.
    root.handlers.clear()
    root.handlers.extend(original_handlers)
    root.setLevel(original_level)


def test_configure_root_logging_idempotent() -> None:
    obj = _L()
    root = logging.getLogger()
    original_handlers = root.handlers[:]
    root.handlers.clear()

    obj.configure_root_logging(level="WARNING")
    handler_count_after_first = len(root.handlers)
    obj.configure_root_logging(level="WARNING")  # second call — must not add duplicate
    assert len(root.handlers) == handler_count_after_first

    root.handlers.clear()
    root.handlers.extend(original_handlers)

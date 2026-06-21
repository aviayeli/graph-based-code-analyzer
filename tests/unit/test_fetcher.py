"""Tests for RepoFetcher — file collection and utility methods."""
from __future__ import annotations

from pathlib import Path

from src.fetcher import RepoFetcher


def _tree(root: Path) -> None:
    """Create a small file tree for testing."""
    (root / "pkg").mkdir()
    (root / "pkg" / "mod.py").write_text("x = 1")
    (root / "pkg" / "helper.py").write_text("y = 2")
    (root / "pkg" / "tests").mkdir()
    (root / "pkg" / "tests" / "test_mod.py").write_text("assert True")
    (root / "pkg" / "__pycache__").mkdir()
    (root / "pkg" / "__pycache__" / "mod.cpython-312.pyc").write_bytes(b"")
    (root / "README.md").write_text("# hello")


# ── collect_files ─────────────────────────────────────────────────────────────

def test_collect_files_returns_py_only(tmp_path: Path) -> None:
    _tree(tmp_path)
    fetcher = RepoFetcher(tmp_path)
    files = fetcher.collect_files()
    assert all(f.suffix == ".py" for f in files)


def test_collect_files_excludes_tests(tmp_path: Path) -> None:
    _tree(tmp_path)
    fetcher = RepoFetcher(tmp_path)
    files = fetcher.collect_files()
    names = [f.name for f in files]
    assert "test_mod.py" not in names


def test_collect_files_excludes_pycache(tmp_path: Path) -> None:
    _tree(tmp_path)
    fetcher = RepoFetcher(tmp_path)
    files = fetcher.collect_files()
    assert not any("__pycache__" in str(f) for f in files)


def test_collect_files_returns_sorted(tmp_path: Path) -> None:
    _tree(tmp_path)
    fetcher = RepoFetcher(tmp_path)
    files = fetcher.collect_files()
    assert files == sorted(files)


def test_collect_files_count(tmp_path: Path) -> None:
    _tree(tmp_path)
    fetcher = RepoFetcher(tmp_path)
    files = fetcher.collect_files()
    assert len(files) == 2  # mod.py and helper.py only


def test_collect_files_custom_extension(tmp_path: Path) -> None:
    (tmp_path / "a.ts").write_text("const x = 1")
    (tmp_path / "b.py").write_text("x = 1")
    fetcher = RepoFetcher(tmp_path)
    ts_files = fetcher.collect_files(extensions=(".ts",))
    assert len(ts_files) == 1
    assert ts_files[0].name == "a.ts"


def test_collect_empty_dir(tmp_path: Path) -> None:
    fetcher = RepoFetcher(tmp_path)
    assert fetcher.collect_files() == []


# ── get_repo_name ─────────────────────────────────────────────────────────────

def test_get_repo_name(tmp_path: Path) -> None:
    target = tmp_path / "my_project"
    target.mkdir()
    fetcher = RepoFetcher(target)
    assert fetcher.get_repo_name() == "my_project"


# ── relative_path ─────────────────────────────────────────────────────────────

def test_relative_path_default_base(tmp_path: Path) -> None:
    fetcher = RepoFetcher(tmp_path)
    child = tmp_path / "pkg" / "mod.py"
    assert fetcher.relative_path(child) == "pkg/mod.py"


def test_relative_path_custom_base(tmp_path: Path) -> None:
    fetcher = RepoFetcher(tmp_path)
    alt_base = tmp_path / "pkg"
    child = tmp_path / "pkg" / "mod.py"
    assert fetcher.relative_path(child, base=alt_base) == "mod.py"


def test_relative_path_outside_base(tmp_path: Path) -> None:
    fetcher = RepoFetcher(tmp_path / "sub")
    outside = tmp_path / "other.py"
    result = fetcher.relative_path(outside)
    assert result == outside.as_posix()


# ── get_sha — non-git dir returns 'unknown' ───────────────────────────────────

def test_get_sha_non_git(tmp_path: Path) -> None:
    fetcher = RepoFetcher(tmp_path)
    assert fetcher.get_sha() == "unknown"

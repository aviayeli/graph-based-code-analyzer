from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration loaded from environment / .env file.

    All secrets are sourced exclusively from the environment — no hardcoded
    values anywhere in this module.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── LLM ──────────────────────────────────────────────────────────────────
    anthropic_api_key: str = Field(default="", repr=False)
    llm_model: str = Field(default="claude-sonnet-4-6")
    crew_llm_model: str = Field(default="anthropic/claude-haiku-4-5-20251001")
    llm_max_tokens: int = Field(default=8192, ge=1, le=32768)

    # ── Token FinOps ─────────────────────────────────────────────────────────
    token_budget_input: int = Field(
        default=8000,
        ge=100,
        description="Hard ceiling on input tokens per LLM call (Rule R1).",
    )
    token_budget_output: int = Field(default=4096, ge=100)

    # Cost per million tokens in USD (updated from Anthropic pricing page).
    cost_per_m_input_usd: float = Field(default=3.00)
    cost_per_m_output_usd: float = Field(default=15.00)

    # ── Analysis targets ─────────────────────────────────────────────────────
    target_repo_url: str = Field(default="")
    workspace_dir: Path = Field(default=Path("workspace"))
    vault_path: Path = Field(default=Path("vault"))

    # ── Parser ───────────────────────────────────────────────────────────────
    supported_languages: list[str] = Field(default=["python"])
    max_file_loc: int = Field(
        default=150,
        description="CI enforcement ceiling — our own files must stay under this.",
    )

    # ── Checkpointing ────────────────────────────────────────────────────────
    checkpoint_dir: Path = Field(default=Path(".checkpoints"))
    checkpoint_interval_nodes: int = Field(
        default=500,
        description="Emit a checkpoint every N nodes during graph build (Rule R2).",
    )

    # ── Logging ──────────────────────────────────────────────────────────────
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(default="INFO")
    log_format: str = Field(
        default="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    @field_validator("workspace_dir", "vault_path", "checkpoint_dir", mode="before")
    @classmethod
    def _coerce_path(cls, v: object) -> Path:
        return Path(str(v))

    @property
    def checkpoint_dir_abs(self) -> Path:
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        return self.checkpoint_dir

    @property
    def vault_path_abs(self) -> Path:
        self.vault_path.mkdir(parents=True, exist_ok=True)
        return self.vault_path


# Module-level singleton — import this everywhere instead of re-instantiating.
settings = Settings()

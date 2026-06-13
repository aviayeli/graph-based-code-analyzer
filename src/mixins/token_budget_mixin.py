from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Final

log = logging.getLogger("graphify.TokenBudgetMixin")

_MICRODOLLARS_PER_DOLLAR: Final[int] = 1_000_000


@dataclass
class _CallRecord:
    model: str
    tokens_in: int
    tokens_out: int
    cost_usd: float


class TokenBudgetMixin:
    """Tracks per-call and session-level token usage for FinOps reporting.

    Pure mixin — no ``__init__`` state.  Session accumulators are initialised
    on first use via :meth:`_ensure_budget_state`.

    Rule R1 enforcement: :meth:`assert_within_budget` raises
    :class:`TokenBudgetExceededError` before the LLM call is made.
    """

    # Pricing defaults (USD per 1 M tokens) — overridden by Settings at runtime.
    _cost_per_m_input: float = 3.00
    _cost_per_m_output: float = 15.00
    _hard_limit_input: int = 8_000

    def _ensure_budget_state(self) -> None:
        if not hasattr(self, "_call_records"):
            self._call_records: list[_CallRecord] = []
            self._session_tokens_in: int = 0
            self._session_tokens_out: int = 0

    def configure_budget(
        self,
        *,
        hard_limit_input: int,
        cost_per_m_input: float,
        cost_per_m_output: float,
    ) -> None:
        """Wire in values from :class:`~src.config.Settings` at startup."""
        self._hard_limit_input = hard_limit_input
        self._cost_per_m_input = cost_per_m_input
        self._cost_per_m_output = cost_per_m_output

    def assert_within_budget(self, tokens_in: int, context: str = "") -> None:
        """Raise before an LLM call if *tokens_in* exceeds the hard limit."""
        if tokens_in > self._hard_limit_input:
            raise TokenBudgetExceededError(
                f"Input token count {tokens_in:,} exceeds hard limit "
                f"{self._hard_limit_input:,}. context={context!r}"
            )

    def track_tokens(
        self, *, model: str, tokens_in: int, tokens_out: int
    ) -> _CallRecord:
        """Record a completed LLM call and return its cost record."""
        self._ensure_budget_state()
        cost = (tokens_in * self._cost_per_m_input + tokens_out * self._cost_per_m_output) / _MICRODOLLARS_PER_DOLLAR
        record = _CallRecord(model=model, tokens_in=tokens_in, tokens_out=tokens_out, cost_usd=cost)
        self._call_records.append(record)
        self._session_tokens_in += tokens_in
        self._session_tokens_out += tokens_out
        log.info(
            "LLM call | model=%s in=%d out=%d cost=$%.4f session_total_in=%d",
            model, tokens_in, tokens_out, cost, self._session_tokens_in,
        )
        return record

    @property
    def session_tokens_in(self) -> int:
        self._ensure_budget_state()
        return self._session_tokens_in

    @property
    def session_tokens_out(self) -> int:
        self._ensure_budget_state()
        return self._session_tokens_out

    @property
    def session_cost_usd(self) -> float:
        self._ensure_budget_state()
        return sum(r.cost_usd for r in self._call_records)

    def session_summary(self) -> dict[str, object]:
        """Return a serialisable summary for FinOps reporting."""
        self._ensure_budget_state()
        return {
            "calls": len(self._call_records),
            "tokens_in": self._session_tokens_in,
            "tokens_out": self._session_tokens_out,
            "cost_usd": round(self.session_cost_usd, 6),
        }


class TokenBudgetExceededError(RuntimeError):
    """Raised when a planned LLM call would breach the hard token ceiling."""

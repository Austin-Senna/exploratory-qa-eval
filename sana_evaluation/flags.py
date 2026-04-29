"""SanaFlags — opt-in feature flags for SANA runtime-control primitives."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


_VALID_FEATURE_NAMES = {
    "short_plan",
    "CoT",
    "results_apis",
}

_VALID_SHORT_PLAN_MODES = {"cadence", "source_budget"}


@dataclass
class SanaFlags:
    """Feature flags controlling which SANA primitives are active for a run.

    All flags default to off. One dependency rule is enforced by `validate()`:
      - `short_plan` requires `agent_management` to be `standard` or `ideal`

    The state-of-task readout is bundled into `short_plan`'s reflection.
    `potential_answer` and `answer_confidence` are also part of every k-turn
    reflection JSON; no separate plugin watches confidence trends.
    """

    short_plan: bool = False
    CoT: bool = False
    results_apis: bool = False

    macro_reflection_k: int = 5
    short_plan_mode: str = "cadence"
    source_budget_calls: int = 3

    def validate(self, *, agent_management: str) -> None:
        if self.short_plan and agent_management not in {"standard", "ideal"}:
            raise ValueError(
                "SANA flag short_plan requires agent_management ∈ {standard, ideal}; "
                f"got agent_management={agent_management!r}."
            )
        if self.short_plan_mode not in _VALID_SHORT_PLAN_MODES:
            raise ValueError(
                f"short_plan_mode must be one of {sorted(_VALID_SHORT_PLAN_MODES)}; "
                f"got {self.short_plan_mode!r}."
            )
        if self.macro_reflection_k <= 0:
            raise ValueError(
                f"macro_reflection_k must be > 0; got {self.macro_reflection_k}."
            )
        if self.source_budget_calls <= 0:
            raise ValueError(
                f"source_budget_calls must be > 0; got {self.source_budget_calls}."
            )

    @classmethod
    def from_feature_names(
        cls,
        feature_names: Iterable[str],
        *,
        macro_reflection_k: int = 5,
        short_plan_mode: str = "cadence",
        source_budget_calls: int = 3,
    ) -> "SanaFlags":
        """Build a SanaFlags from a list of feature-name strings (e.g. CLI repeats)."""
        normalized = [str(n).strip() for n in feature_names if str(n).strip()]
        unknown = [n for n in normalized if n not in _VALID_FEATURE_NAMES]
        if unknown:
            raise ValueError(
                f"Unknown SANA feature(s): {unknown}. "
                f"Expected from: {sorted(_VALID_FEATURE_NAMES)}."
            )
        kwargs = {name: True for name in normalized}
        return cls(
            macro_reflection_k=macro_reflection_k,
            short_plan_mode=short_plan_mode,
            source_budget_calls=source_budget_calls,
            **kwargs,
        )

    def active_features(self) -> List[str]:
        """Return list of active feature names, useful for labels/logs."""
        return [name for name in sorted(_VALID_FEATURE_NAMES) if getattr(self, name)]

    def any_active(self) -> bool:
        return any(getattr(self, name) for name in _VALID_FEATURE_NAMES)


__all__ = ["SanaFlags"]

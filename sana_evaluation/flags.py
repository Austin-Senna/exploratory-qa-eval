"""SanaFlags — opt-in feature flags for SANA runtime-control primitives."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


_VALID_FEATURE_NAMES = {
    "sprint",
    "cot",
    "results",
    "delegation",
}

_VALID_SPRINT_MODES = {"cadence", "commitment"}


@dataclass
class SanaFlags:
    """Feature flags controlling which SANA primitives are active for a run.

    All flags default to off. One dependency rule is enforced by `validate()`:
      - `sprint` requires `agent_management` to be `standard` or `ideal`

    The state-of-task readout is bundled into `sprint`'s reflection.
    `potential_answer` and `answer_confidence` are also part of every k-turn
    reflection JSON; no separate plugin watches confidence trends.
    """

    sprint: bool = False
    cot: bool = False
    results: bool = False
    delegation: bool = False

    macro_reflection_k: int = 5
    sprint_mode: str = "cadence"
    commitment_budget_calls: int = 3
    max_search_subagent_calls: int = 3
    max_inspect_subagent_calls: int = 8

    def validate(self, *, agent_management: str) -> None:
        if self.sprint and self.delegation:
            raise ValueError("SANA features sprint and delegation are mutually exclusive.")
        if self.sprint and agent_management not in {"standard", "ideal"}:
            raise ValueError(
                "SANA flag sprint requires agent_management ∈ {standard, ideal}; "
                f"got agent_management={agent_management!r}."
            )
        if self.delegation and agent_management not in {"standard", "ideal"}:
            raise ValueError(
                "SANA flag delegation requires agent_management ∈ {standard, ideal}; "
                f"got agent_management={agent_management!r}."
            )
        if self.sprint_mode not in _VALID_SPRINT_MODES:
            raise ValueError(
                f"sprint_mode must be one of {sorted(_VALID_SPRINT_MODES)}; "
                f"got {self.sprint_mode!r}."
            )
        if self.macro_reflection_k <= 0:
            raise ValueError(
                f"macro_reflection_k must be > 0; got {self.macro_reflection_k}."
            )
        if self.commitment_budget_calls <= 0:
            raise ValueError(
                f"commitment_budget_calls must be > 0; got {self.commitment_budget_calls}."
            )
        if self.max_search_subagent_calls <= 0:
            raise ValueError(
                "max_search_subagent_calls must be > 0; "
                f"got {self.max_search_subagent_calls}."
            )
        if self.max_inspect_subagent_calls <= 0:
            raise ValueError(
                "max_inspect_subagent_calls must be > 0; "
                f"got {self.max_inspect_subagent_calls}."
            )

    @classmethod
    def from_feature_names(
        cls,
        feature_names: Iterable[str],
        *,
        macro_reflection_k: int = 5,
        sprint_mode: str = "cadence",
        commitment_budget_calls: int = 3,
        max_search_subagent_calls: int = 3,
        max_inspect_subagent_calls: int = 8,
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
            sprint_mode=sprint_mode,
            commitment_budget_calls=commitment_budget_calls,
            max_search_subagent_calls=max_search_subagent_calls,
            max_inspect_subagent_calls=max_inspect_subagent_calls,
            **kwargs,
        )

    def active_features(self) -> List[str]:
        """Return list of active feature names, useful for labels/logs."""
        return [name for name in sorted(_VALID_FEATURE_NAMES) if getattr(self, name)]

    def any_active(self) -> bool:
        return any(getattr(self, name) for name in _VALID_FEATURE_NAMES)


__all__ = ["SanaFlags"]

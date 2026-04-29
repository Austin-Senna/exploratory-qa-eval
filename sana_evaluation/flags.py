"""SanaFlags — opt-in feature flags for SANA runtime-control primitives."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List


_VALID_FEATURE_NAMES = {
    "short_plan",
    "CoT",
    "results_apis",
    "confidence_advisory",
    "dashboard",
}


@dataclass
class SanaFlags:
    """Feature flags controlling which SANA primitives are active for a run.

    All flags default to off. Two dependency rules are enforced by `validate()`:
      - `short_plan` requires `agent_management` to be `standard` or `ideal`
      - `confidence_advisory` requires `CoT=True`
    """

    short_plan: bool = False
    CoT: bool = False
    results_apis: bool = False
    confidence_advisory: bool = False
    dashboard: bool = False

    macro_reflection_k: int = 5

    def validate(self, *, agent_management: str) -> None:
        if self.short_plan and agent_management not in {"standard", "ideal"}:
            raise ValueError(
                "SANA flag short_plan requires agent_management ∈ {standard, ideal}; "
                f"got agent_management={agent_management!r}."
            )
        if self.confidence_advisory and not self.CoT:
            raise ValueError(
                "SANA flag confidence_advisory requires CoT=True (confidence is parsed from "
                "the CoT post-record). Enable both or neither."
            )
        if self.macro_reflection_k <= 0:
            raise ValueError(
                f"macro_reflection_k must be > 0; got {self.macro_reflection_k}."
            )

    @classmethod
    def from_feature_names(
        cls, feature_names: Iterable[str], *, macro_reflection_k: int = 5
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
        return cls(macro_reflection_k=macro_reflection_k, **kwargs)

    def active_features(self) -> List[str]:
        """Return list of active feature names, useful for labels/logs."""
        return [name for name in sorted(_VALID_FEATURE_NAMES) if getattr(self, name)]

    def any_active(self) -> bool:
        return any(getattr(self, name) for name in _VALID_FEATURE_NAMES)


__all__ = ["SanaFlags"]

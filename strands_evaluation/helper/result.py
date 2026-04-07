"""
AgentResult dataclass for the Strands evaluation runner.
"""
from dataclasses import dataclass, field
import logging
from typing import Any, Dict, List, Optional, Tuple

from strands_evaluation.helper.constants import MODEL_PRICING

# Baseline API tools
_API_TOOL_NAMES = {"search", "search_keyword", "list_files", "peek_file", "query_file", "download"}
# Condition A (augmented search backends — sparse/hybrid/graph)
_CONDITION_A_TOOL_NAMES = {"search_sparse", "search_hybrid", "search_graph"}

logger = logging.getLogger(__name__)


@dataclass
class AgentResult:
    """Result from a DataLakeAgent run."""

    answer: str
    model: str
    model_name: Optional[str] = None   # short pricing key e.g. "bedrock/claude-sonnet-4.5"
    reasoning: str = ""
    sources: List[str] = field(default_factory=list)
    # Strands EventLoopMetrics object (or None when not available)
    metrics: Any = None
    elapsed_time: float = 0.0
    success: bool = True
    error: Optional[str] = None

    @property
    def cycle_count(self) -> Optional[int]:
        return self.metrics.cycle_count if self.metrics else None

    @property
    def cycle_times(self) -> Optional[List[float]]:
        return self.metrics.cycle_durations if self.metrics else None

    @property
    def tool_metrics(self) -> Optional[Dict[str, Any]]:
        return self.metrics.tool_metrics if self.metrics else None

    @property
    def input_tokens(self) -> int:
        return self.metrics.accumulated_usage.get("inputTokens", 0) if self.metrics else 0

    @property
    def output_tokens(self) -> int:
        return self.metrics.accumulated_usage.get("outputTokens", 0) if self.metrics else 0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    @property
    def cost_usd(self) -> float:
        return self.get_price()

    def get_price(self) -> float:
        candidates: List[str] = []
        model_key = str(self.model_name) if self.model_name is not None else ""
        if model_key:
            candidates.append(model_key)
            if "/" in model_key:
                suffix_key = model_key.split("/", 1)[1].strip()
                if suffix_key and suffix_key not in candidates:
                    candidates.append(suffix_key)

        for key in candidates:
            pricing = MODEL_PRICING.get(key)
            if pricing:
                return (
                    pricing["input"] * self.input_tokens / 1_000_000
                    + pricing["output"] * self.output_tokens / 1_000_000
                )

        if model_key:
            logger.warning(
                "No pricing configured for model_name=%s. Tried keys: %s",
                model_key,
                ", ".join(candidates) if candidates else "(none)",
            )
        return 0.0

    def get_tool_counts(self) -> List[Dict[str, Any]]:
        if not self.tool_metrics:
            return []
        return [
            {
                "name": tool_name,
                "call_count": m.call_count,
                "success_count": m.success_count,
                "average_time": (m.total_time / m.call_count if m.call_count > 0 else 0),
            }
            for tool_name, m in self.tool_metrics.items()
        ]

    def get_api_tool_calls(self) -> int:
        if not self.tool_metrics:
            return 0
        return sum(m.call_count for name, m in self.tool_metrics.items() if name in _API_TOOL_NAMES)

    def get_cumulative_tool_counts(self) -> tuple:
        if not self.tool_metrics:
            return 0, 0
        total_calls = sum(m.call_count for m in self.tool_metrics.values())
        return 0, total_calls

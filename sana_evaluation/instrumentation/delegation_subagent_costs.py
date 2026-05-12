"""Cost telemetry for Tabular SANA delegation subagents."""

from __future__ import annotations

import logging
from typing import Any, Dict

from strands_evaluation.helper.constants import MODEL_PRICING
from strands_evaluation.instrumentation.trace_plugin import write_trace_record

logger = logging.getLogger(__name__)

_TOOL_NAMES = ("search_subagent", "inspect_subagent")


def _initial_stats() -> Dict[str, Any]:
    stats: Dict[str, Any] = {
        "delegation_subagent_calls": 0,
        "delegation_subagent_input_tokens": 0,
        "delegation_subagent_cached_input_tokens": 0,
        "delegation_subagent_uncached_input_tokens": 0,
        "delegation_subagent_output_tokens": 0,
        "delegation_subagent_total_tokens": 0,
        "delegation_subagent_cost_usd": 0.0,
        "delegation_gold_datasets_read": [],
    }
    for tool_name in _TOOL_NAMES:
        stats[f"{tool_name}_calls"] = 0
        stats[f"{tool_name}_cost_usd"] = 0.0
    return stats


_STATS: Dict[str, Any] = _initial_stats()


def reset_stats() -> None:
    """Reset per-task delegation subagent cost counters."""

    _STATS.clear()
    _STATS.update(_initial_stats())


def get_stats() -> Dict[str, Any]:
    """Return per-task delegation subagent cost counters."""

    return dict(_STATS)


def _coerce_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _usage_from_agent_result(agent_result: Any) -> Dict[str, int]:
    metrics = getattr(agent_result, "metrics", None)
    usage = getattr(metrics, "accumulated_usage", {}) or {}
    input_tokens = _coerce_int(usage.get("inputTokens"))
    output_tokens = _coerce_int(usage.get("outputTokens"))
    cached_input_tokens = _coerce_int(usage.get("cacheReadInputTokens"))
    total_tokens = _coerce_int(usage.get("totalTokens")) or input_tokens + output_tokens
    return {
        "input_tokens": input_tokens,
        "cached_input_tokens": cached_input_tokens,
        "uncached_input_tokens": max(0, input_tokens - cached_input_tokens),
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
    }


def _cost_for_usage(model_name: str, usage: Dict[str, int]) -> float:
    candidates = [model_name]
    if "/" in model_name:
        candidates.append(model_name.split("/", 1)[1].strip())
    pricing = next((MODEL_PRICING.get(key) for key in candidates if key), None)
    if not pricing:
        logger.warning("No pricing configured for delegation subagent model_name=%s", model_name)
        return 0.0

    cached_input_rate = pricing.get("cache_read_input", pricing["input"])
    return (
        pricing["input"] * usage["uncached_input_tokens"] / 1_000_000
        + cached_input_rate * usage["cached_input_tokens"] / 1_000_000
        + pricing["output"] * usage["output_tokens"] / 1_000_000
    )


def record_subagent_call(
    *,
    tool: str,
    subagent_kind: str,
    model_name: str,
    agent_result: Any = None,
    success: bool = True,
    **extras: Any,
) -> Dict[str, Any]:
    """Record cost telemetry for one SANA delegation helper-agent invocation."""

    usage = _usage_from_agent_result(agent_result)
    model_key = str(model_name or "")
    cost_usd = _cost_for_usage(model_key, usage)

    _STATS["delegation_subagent_calls"] += 1
    _STATS["delegation_subagent_input_tokens"] += usage["input_tokens"]
    _STATS["delegation_subagent_cached_input_tokens"] += usage["cached_input_tokens"]
    _STATS["delegation_subagent_uncached_input_tokens"] += usage["uncached_input_tokens"]
    _STATS["delegation_subagent_output_tokens"] += usage["output_tokens"]
    _STATS["delegation_subagent_total_tokens"] += usage["total_tokens"]
    _STATS["delegation_subagent_cost_usd"] += cost_usd

    if tool in _TOOL_NAMES:
        _STATS[f"{tool}_calls"] += 1
        _STATS[f"{tool}_cost_usd"] += cost_usd

    gold_datasets_read = extras.get("gold_datasets_read") or []
    seen = set(_STATS["delegation_gold_datasets_read"])
    for value in gold_datasets_read:
        dataset_id = str(value).strip()
        if dataset_id and dataset_id not in seen:
            _STATS["delegation_gold_datasets_read"].append(dataset_id)
            seen.add(dataset_id)

    record: Dict[str, Any] = {
        "event": "delegation_subagent_cost",
        "tool": tool,
        "subagent_kind": subagent_kind,
        "model_name": model_key,
        "success": bool(success),
        **usage,
        "cost_usd": cost_usd,
    }
    record.update(extras)
    write_trace_record(record)

    logger.info(
        "%s %s subagent cost model=%s input=%s cached_input=%s output=%s cost_usd=%.8f success=%s",
        tool,
        subagent_kind,
        model_key,
        usage["input_tokens"],
        usage["cached_input_tokens"],
        usage["output_tokens"],
        cost_usd,
        success,
    )
    return record


__all__ = [
    "get_stats",
    "record_subagent_call",
    "reset_stats",
]

"""Composition layer for multi-axis ablation modes.

This module keeps mode selection thin by composing three independent axes:
  - search_tool: naive | standard | ideal
  - search_results: naive | standard | ideal
  - agent_management: naive | standard | ideal
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

from strands.tools.decorator import DecoratedFunctionTool

from strands_evaluation.config import RunConfig
from strands_evaluation.tools.agent_tools import search_prefix as search_prefix_base
from strands_evaluation.tools.agent_tools_v2 import summarize_context
from strands_evaluation.tools.external.plan_ideal import (
    inject_reasoning_chain_prompt,
    plan_ideal,
)
from strands_evaluation.tools.external.plan_tools import plan
from strands_evaluation.tools.external.search_wrapper import (
    build_search_tools as build_search_tools_by_mode,
    search_tool_names_in,
)

logger = logging.getLogger(__name__)

_MODES = {"naive", "standard", "ideal"}


@dataclass
class ModeBundle:
    tools: List[Any]
    system_prompt: str
    search_tool_names: Tuple[str, ...]
    enable_skills: bool
    enable_stagnation: bool
    modes: Dict[str, str]


def _normalize_mode(value: Optional[str], default: str, label: str) -> str:
    mode = (value or default).strip().lower()
    if mode not in _MODES:
        raise ValueError(f"Unsupported {label} mode '{value}'. Expected one of: {', '.join(sorted(_MODES))}")
    return mode


def _load_condition_prompt(condition: str, fallback: str) -> str:
    path = f"prompts/condition_{condition}.txt"
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        logger.warning("%s not found — using fallback prompt", path)
        return fallback


def _resolve_search_base_tools(search_tool_mode: str) -> List[DecoratedFunctionTool]:
    if search_tool_mode == "naive":
        from strands_evaluation.tools.external.search_b_tools import (
            search_schema as search_schema_sparse,
            search_value as search_value_sparse,
        )

        return [search_value_sparse, search_schema_sparse, search_prefix_base]

    if search_tool_mode == "standard":
        from strands_evaluation.tools.external.search_a_tools import (
            search_schema as search_schema_hybrid,
            search_value as search_value_hybrid,
        )

        # Standard = hybrid BM25+dense without cross-encoder reranking.
        return [search_value_hybrid, search_schema_hybrid, search_prefix_base]

    from strands_evaluation.tools.external.search_ideal import (
        search_prefix as search_prefix_ideal,
        search_schema as search_schema_ideal,
        search_value as search_value_ideal,
    )

    return [search_value_ideal, search_schema_ideal, search_prefix_ideal]


def _resolve_management(
    management_mode: str,
    *,
    base_prompt: str,
    task_context: Optional[Dict[str, Any]],
) -> tuple[str, List[Any], bool, bool]:
    if management_mode == "naive":
        return base_prompt, [], False, False

    if management_mode == "standard":
        prompt = _load_condition_prompt("b", fallback=base_prompt)
        return prompt, [plan, summarize_context], True, True

    # ideal
    prompt = _load_condition_prompt("b", fallback=base_prompt)
    task_context = task_context or {}
    prompt = inject_reasoning_chain_prompt(
        prompt,
        task_context.get("reasoning_chain"),
        task_id=str(task_context.get("task_id", "")),
    )
    return prompt, [plan_ideal], False, False


def build_mode_bundle(
    run_config: RunConfig,
    *,
    data_tools: Sequence[Any],
    task_context: Optional[Dict[str, Any]] = None,
) -> ModeBundle:
    """Build final tools/prompt/plugin toggles from multi-axis ablation modes."""
    search_tool_mode = _normalize_mode(run_config.search_tool_mode, "standard", "search_tool")
    search_results_mode = _normalize_mode(run_config.search_results_mode, "standard", "search_results")
    agent_management_mode = _normalize_mode(run_config.agent_management_mode, "standard", "agent_management")

    if search_tool_mode == "ideal":
        try:
            import strands_evaluation.tools.external.search_ideal as search_ideal

            search_ideal.set_task_context(task_context or {})
        except Exception as exc:
            logger.warning("Could not set search_ideal task context: %s", exc)

    raw_search_tools = _resolve_search_base_tools(search_tool_mode)
    search_tools = build_search_tools_by_mode(
        raw_search_tools,
        fixed_k=run_config.search_k,
        results_mode=search_results_mode,
    )

    system_prompt, management_tools, enable_skills, enable_stagnation = _resolve_management(
        agent_management_mode,
        base_prompt=run_config.system_prompt,
        task_context=task_context,
    )

    tools = list(search_tools) + list(management_tools) + list(data_tools)
    return ModeBundle(
        tools=tools,
        system_prompt=system_prompt,
        search_tool_names=search_tool_names_in(search_tools),
        enable_skills=enable_skills,
        enable_stagnation=enable_stagnation,
        modes={
            "search_tool": search_tool_mode,
            "search_results": search_results_mode,
            "agent_management": agent_management_mode,
        },
    )


from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)

_PROMPTS_DIR = Path("prompts")
_MODES = {"naive", "standard", "ideal"}
_DEBUG_MODES = {"decision_notes"}

_PLAN_AGENT_SKILL = "strands_evaluation/tools/skills/plan-agent"
_PLAN_IDEAL_SKILL = "strands_evaluation/tools/skills/plan-ideal"
_DISCOVER_SKILL_PATHS = {
    "naive": "strands_evaluation/tools/skills/discover-data-naive",
    "standard": "strands_evaluation/tools/skills/discover-data-standard",
    "ideal": "strands_evaluation/tools/skills/discover-data-ideal",
}
_QUERY_DATA_SKILL = "strands_evaluation/tools/skills/query-data"


def _normalize_mode(value: Optional[str], default: str, label: str) -> str:
    mode = (value or default).strip().lower()
    if mode not in _MODES:
        raise ValueError(
            f"Unsupported {label} mode '{value}'. Expected one of: {', '.join(sorted(_MODES))}"
        )
    return mode


def normalize_debug_mode(value: Optional[str]) -> Optional[str]:
    mode = (value or "").strip().lower()
    if not mode or mode == "none":
        return None
    if mode not in _DEBUG_MODES:
        raise ValueError(
            f"Unsupported debug mode '{value}'. Expected one of: none, {', '.join(sorted(_DEBUG_MODES))}"
        )
    return mode


def load_prompt_text(path: str | Path, fallback: str = "") -> str:
    prompt_path = Path(path)
    try:
        return prompt_path.read_text()
    except FileNotFoundError:
        logger.warning("%s not found — using fallback prompt text", prompt_path)
        return fallback


def load_condition_prompt(condition: str, fallback: str = "") -> str:
    if str(condition).strip().lower() == "baseline":
        return load_prompt_text(_PROMPTS_DIR / "baseline.txt", fallback)
    return load_prompt_text(_PROMPTS_DIR / f"condition_{condition}.txt", fallback)


def _compose_search_overlay_prompt(
    base_prompt_path: str | Path,
    search_tool_mode: Optional[str],
    *,
    fallback: str = "",
) -> str:
    mode = _normalize_mode(search_tool_mode, "naive", "search_tool")
    base_prompt = load_prompt_text(base_prompt_path, fallback).rstrip()
    overlay = load_prompt_text(_PROMPTS_DIR / f"search_{mode}.txt", "").strip()

    if not base_prompt:
        return overlay
    if not overlay:
        return base_prompt
    return f"{base_prompt}\n\n{overlay}"


def compose_condition_b_prompt(search_tool_mode: Optional[str], *, fallback: str = "") -> str:
    return _compose_search_overlay_prompt(
        _PROMPTS_DIR / "condition_b.txt",
        search_tool_mode,
        fallback=fallback,
    )


def compose_baseline_prompt(search_tool_mode: Optional[str], *, fallback: str = "") -> str:
    return _compose_search_overlay_prompt(
        _PROMPTS_DIR / "baseline.txt",
        search_tool_mode,
        fallback=fallback,
    )


def planning_skill_path(agent_management_mode: Optional[str]) -> str:
    management_mode = _normalize_mode(agent_management_mode, "standard", "agent_management")
    return _PLAN_IDEAL_SKILL if management_mode == "ideal" else _PLAN_AGENT_SKILL


def discover_skill_path(search_tool_mode: Optional[str]) -> str:
    mode = _normalize_mode(search_tool_mode, "naive", "search_tool")
    return _DISCOVER_SKILL_PATHS[mode]


def skill_paths_for_modes(
    search_tool_mode: Optional[str],
    agent_management_mode: Optional[str],
) -> List[str]:
    return [
        planning_skill_path(agent_management_mode),
        discover_skill_path(search_tool_mode),
        _QUERY_DATA_SKILL,
    ]


def inject_debug_prompt(prompt: str, debug_mode: Optional[str]) -> str:
    mode = normalize_debug_mode(debug_mode)
    if mode is None:
        return prompt

    if mode == "decision_notes":
        section = (
            "\n\n## DEBUG DECISION NOTES\n"
            "- Debug mode is active.\n"
            "- Before every tool call, emit a short structured note immediately before the tool-use block.\n"
            "- Keep it concise and action-oriented. Do not dump long reasoning.\n"
            "- Use exactly these four fields:\n"
            "goal: <one short sentence>\n"
            "why_this_tool: <one short sentence>\n"
            "what_success_looks_like: <one short sentence>\n"
            "confidence: <low|medium|high>\n"
            "- Then call the tool in the same response.\n"
        )
        return prompt.rstrip() + section

    return prompt


__all__ = [
    "compose_baseline_prompt",
    "compose_condition_b_prompt",
    "discover_skill_path",
    "inject_debug_prompt",
    "load_condition_prompt",
    "load_prompt_text",
    "normalize_debug_mode",
    "planning_skill_path",
    "skill_paths_for_modes",
]

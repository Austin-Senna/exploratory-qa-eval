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


def load_prompt_text(path: str | Path) -> str:
    prompt_path = Path(path)
    if not prompt_path.is_file():
        raise FileNotFoundError(
            f"Required prompt file missing: {prompt_path}. "
            "Run preflight to confirm your prompts/ directory is complete."
        )
    return prompt_path.read_text()


def _compose_search_overlay_prompt(
    base_prompt_path: str | Path,
    search_tool_mode: Optional[str],
) -> str:
    mode = _normalize_mode(search_tool_mode, "naive", "search_tool")
    base_prompt = load_prompt_text(base_prompt_path).rstrip()
    overlay = load_prompt_text(_PROMPTS_DIR / f"search_{mode}.txt").strip()
    return f"{base_prompt}\n\n{overlay}"


def compose_managed_prompt(search_tool_mode: Optional[str]) -> str:
    return _compose_search_overlay_prompt(
        _PROMPTS_DIR / "managed.txt",
        search_tool_mode,
    )


def compose_baseline_prompt(search_tool_mode: Optional[str]) -> str:
    return _compose_search_overlay_prompt(
        _PROMPTS_DIR / "baseline.txt",
        search_tool_mode,
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


def inject_sana_prompt(prompt: str, sana_level: Optional[int]) -> str:
    """Append a short section describing SANA Agent 1's enriched peek_file.

    Only runs when sana_level >= 1. Keeps the baseline/managed prompts unmodified
    on disk — the extra guidance is appended at agent construction time.
    """
    if sana_level is None or sana_level < 1:
        return prompt

    section = (
        "\n\n## DATASET PROFILE (SANA Agent 1)\n"
        "`peek_file` may return an extra `profile` field with cached metadata for the dataset:\n"
        "`schema_columns`, `table_kind`, `llm_description`, `snippet`.\n"
        "When `profile` is present, use it instead of follow-up `read_file` / `grep_file` probes to learn column names, types, or dataset purpose.\n"
        "Fall back to the usual preview-then-query flow when `profile` is absent (not every dataset is cached)."
    )
    return prompt.rstrip() + section


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
    "compose_managed_prompt",
    "discover_skill_path",
    "inject_debug_prompt",
    "inject_sana_prompt",
    "load_prompt_text",
    "normalize_debug_mode",
    "planning_skill_path",
    "skill_paths_for_modes",
]

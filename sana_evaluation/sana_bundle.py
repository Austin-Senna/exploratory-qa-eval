"""SanaDataLakeAgent — wraps the baseline DataLakeAgent with SANA primitives.

Composes SANA prompt blocks and runtime plugins via the generic extension
hooks exposed on DataLakeAgent. SanaDataLakeAgent reads SanaFlags from
`run_config.sana_flags` (a SanaRunConfig); plain RunConfigs degrade to all
flags off (and SanaDataLakeAgent then behaves identically to DataLakeAgent).
"""

from __future__ import annotations

import logging
from typing import Any, List, Optional

from strands_evaluation.agent_with_mode import DataLakeAgent
from strands_evaluation.config import AgentConfig, RunConfig

from sana_evaluation.helper.conversation import build_sana_conversation_manager
from sana_evaluation.flags import SanaFlags
from sana_evaluation.plugins import (
    CoTPostRecordPlugin,
    ShortPlanSteerHandler,
    StateOfTaskDashboardPlugin,
)
from sana_evaluation.prompts import (
    cot_block,
    short_plan_block,
)

logger = logging.getLogger(__name__)


class SanaDataLakeAgent(DataLakeAgent):
    """DataLakeAgent + SANA prompt blocks + SANA plugins driven by SanaFlags."""

    def __init__(
        self,
        agent_config: AgentConfig,
        run_config: Optional[RunConfig] = None,
    ) -> None:
        super().__init__(agent_config, run_config)
        flags = getattr(self.run_config, "sana_flags", None)
        self.sana_flags: SanaFlags = flags if isinstance(flags, SanaFlags) else SanaFlags()

        am = (self.run_config.agent_management_mode or "").strip().lower() or "naive"
        try:
            self.sana_flags.validate(agent_management=am)
        except ValueError as exc:
            raise ValueError(f"SanaFlags validation failed: {exc}") from exc

        if self.sana_flags.any_active():
            logger.info(
                "SANA features active: %s (macro_reflection_k=%d)",
                ", ".join(self.sana_flags.active_features()) or "none",
                self.sana_flags.macro_reflection_k,
            )

    # ------------------------------------------------------------------
    # Hook overrides
    # ------------------------------------------------------------------

    def _pre_build_setup(
        self,
        *,
        search_tool_mode: Optional[str],
        agent_management_mode: Optional[str],
    ) -> None:
        # results_apis is now a tool swap (see _decorate_tools), not a runtime
        # toggle. Nothing to do here.
        return None

    def _extra_prompt_text(
        self,
        *,
        search_tool_mode: Optional[str],
        agent_management_mode: Optional[str],
    ) -> str:
        flags = self.sana_flags
        if not flags.any_active():
            return ""
        st = (search_tool_mode or "naive").strip().lower()
        parts: List[str] = []
        if flags.cot:
            parts.append(cot_block(st))
        if flags.sprint:
            parts.append(short_plan_block(st, short_plan_mode=flags.sprint_mode))
        # results: no system-prompt block — the peek_file docstring already
        # documents the `profile` field. The flag toggles the profile loader
        # callback at runtime in _pre_build_setup.
        return "".join(parts)

    def _extra_plugins(
        self,
        *,
        search_tool_mode: Optional[str],
        agent_management_mode: Optional[str],
    ) -> List[Any]:
        flags = self.sana_flags
        if not flags.any_active():
            return []

        plugins: List[Any] = []

        if flags.cot:
            plugins.append(CoTPostRecordPlugin())

        short_plan_plugin: Optional[ShortPlanSteerHandler] = None
        if flags.sprint:
            short_plan_plugin = ShortPlanSteerHandler(
                macro_reflection_k=flags.macro_reflection_k,
                short_plan_mode=flags.sprint_mode,
                source_budget_calls=flags.commitment_budget_calls,
            )
            plugins.append(short_plan_plugin)

        # State-of-task readout is bundled with short_plan: when short_plan is on,
        # always wire the dashboard plugin and have it surface its readout inside
        # the k-turn reflection Guide reason (peer-wired into ShortPlanSteerHandler).
        if short_plan_plugin is not None:
            dashboard_plugin = StateOfTaskDashboardPlugin(
                max_tool_calls=int(self.run_config.max_tool_calls),
            )
            dashboard_plugin.short_plan_plugin = short_plan_plugin
            short_plan_plugin.dashboard_plugin = dashboard_plugin
            plugins.append(dashboard_plugin)

        return plugins

    def _conversation_manager(
        self,
        *,
        search_tool_mode: Optional[str],
        agent_management_mode: Optional[str],
    ) -> Optional[Any]:
        if not self.sana_flags.any_active():
            return None
        return build_sana_conversation_manager(self.run_config)

    def _decorate_tools(
        self,
        tools: List[Any],
        *,
        search_tool_mode: Optional[str],
        agent_management_mode: Optional[str],
    ) -> List[Any]:
        if not self.sana_flags.results:
            return tools
        from sana_evaluation.tools.peek_file_with_profile import peek_file as sana_peek_file
        return [sana_peek_file if getattr(t, "tool_name", None) == "peek_file" else t for t in tools]


__all__ = ["SanaDataLakeAgent"]

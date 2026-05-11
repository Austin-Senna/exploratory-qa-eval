"""SanaDataLakeAgent — wraps the baseline DataLakeAgent with SANA primitives.

Composes SANA prompt blocks and runtime plugins via the generic extension
hooks exposed on DataLakeAgent. SanaDataLakeAgent reads SanaFlags from
`run_config.sana_flags` (a SanaRunConfig); plain RunConfigs degrade to all
flags off (and SanaDataLakeAgent then behaves identically to DataLakeAgent).
"""

from __future__ import annotations

import logging
from typing import Any, List, Optional, Sequence

from strands_evaluation.agent_with_mode import DataLakeAgent
from strands_evaluation.config import AgentConfig, RunConfig

from sana_evaluation.helper.conversation import build_sana_conversation_manager
from sana_evaluation.flags import SanaFlags
from sana_evaluation.plugins import (
    CoTSteerHandler,
    SprintSteerHandler,
    StateOfTaskDashboardPlugin,
)
from sana_evaluation.prompts import (
    cot_block,
    delegation_block,
    sprint_block,
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

        active_plan_mode = (
            self.run_config.agent_management_mode
            or self.run_config.plan_mode
            or ""
        ).strip().lower() or "naive"
        try:
            self.sana_flags.validate(agent_management=active_plan_mode)
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
        agent_management_mode: Optional[str] = None,
        plan_mode: Optional[str] = None,
    ) -> None:
        if self.sana_flags.delegation:
            from sana_evaluation.instrumentation import delegation_subagent_costs

            delegation_subagent_costs.reset_stats()
        # results is a tool swap (see _decorate_tools), not a runtime
        # toggle. Nothing to do here.
        return None

    def _extra_prompt_text(
        self,
        *,
        search_tool_mode: Optional[str],
        agent_management_mode: Optional[str] = None,
        plan_mode: Optional[str] = None,
    ) -> str:
        flags = self.sana_flags
        if not flags.any_active():
            return ""
        st = (search_tool_mode or "naive").strip().lower()
        parts: List[str] = []
        if flags.cot:
            parts.append(cot_block(st))
        if flags.delegation:
            parts.append(delegation_block(st))
        if flags.sprint:
            parts.append(sprint_block(st, sprint_mode=flags.sprint_mode))
        # results: no system-prompt block — the peek_file docstring already
        # documents the `profile` field. The flag toggles the profile loader
        # callback at runtime in _pre_build_setup.
        return "".join(parts)

    def _extra_plugins(
        self,
        *,
        search_tool_mode: Optional[str],
        agent_management_mode: Optional[str] = None,
        plan_mode: Optional[str] = None,
    ) -> List[Any]:
        flags = self.sana_flags
        if not flags.any_active():
            return []

        plugins: List[Any] = []

        if flags.cot:
            plugins.append(CoTSteerHandler())

        sprint_plugin: Optional[SprintSteerHandler] = None
        if flags.sprint:
            sprint_plugin = SprintSteerHandler(
                macro_reflection_k=flags.macro_reflection_k,
                sprint_mode=flags.sprint_mode,
                commitment_budget_calls=flags.commitment_budget_calls,
                max_tool_calls=int(self.run_config.max_tool_calls),
            )
            plugins.append(sprint_plugin)

        # State-of-task readout is bundled with sprint: when sprint is on,
        # always wire the dashboard plugin and have it surface its readout inside
        # the reflection Guide reason (peer-wired into SprintSteerHandler).
        if sprint_plugin is not None:
            dashboard_plugin = StateOfTaskDashboardPlugin(
                max_tool_calls=int(self.run_config.max_tool_calls),
            )
            dashboard_plugin.sprint_plugin = sprint_plugin
            sprint_plugin.dashboard_plugin = dashboard_plugin
            plugins.append(dashboard_plugin)

        return plugins

    def _conversation_manager(
        self,
        *,
        search_tool_mode: Optional[str],
        agent_management_mode: Optional[str] = None,
        plan_mode: Optional[str] = None,
    ) -> Optional[Any]:
        if not self.sana_flags.any_active():
            return None
        return build_sana_conversation_manager(self.run_config)

    def _decorate_tools(
        self,
        tools: List[Any],
        *,
        search_tool_mode: Optional[str],
        agent_management_mode: Optional[str] = None,
        plan_mode: Optional[str] = None,
        task_context: Optional[dict[str, Any]] = None,
    ) -> List[Any]:
        decorated = list(tools)
        if self.sana_flags.results:
            from sana_evaluation.tools.peek_file_with_profile import (
                peek_file as sana_peek_file,
                peek_multiple as sana_peek_multiple,
            )

            decorated = [
                sana_peek_file if getattr(t, "tool_name", None) == "peek_file"
                else sana_peek_multiple if getattr(t, "tool_name", None) == "peek_multiple"
                else t
                for t in decorated
            ]
        if self.sana_flags.delegation:
            from sana_evaluation.tools.delegation_tool import (
                DelegationRuntime,
                set_delegation_runtime,
                tools_for_delegation_planner,
            )

            set_delegation_runtime(
                DelegationRuntime(
                    agent_config=self.agent_config,
                    run_config=self.run_config,
                    task_context=dict(task_context or {}),
                    base_tools=list(decorated),
                    max_search_subagent_calls=self.sana_flags.max_search_subagent_calls,
                    max_inspect_subagent_calls=self.sana_flags.max_inspect_subagent_calls,
                )
            )
            include_search_subagent = (search_tool_mode or "").strip().lower() != "preloaded"
            return tools_for_delegation_planner(
                decorated,
                include_search_subagent=include_search_subagent,
            )
        if self.sana_flags.sprint:
            from sana_evaluation.tools.sprint_tool import sprint

            if not any(getattr(t, "tool_name", None) == "sprint" for t in decorated):
                decorated.append(sprint)
        if self.sana_flags.cot:
            from sana_evaluation.tools.cot_tool import cot

            if not any(getattr(t, "tool_name", None) == "cot" for t in decorated):
                decorated.append(cot)
        return decorated

    def _decorate_plugins(
        self,
        plugins: List[Any],
        *,
        search_tool_mode: Optional[str],
        agent_management_mode: Optional[str] = None,
        plan_mode: Optional[str] = None,
    ) -> List[Any]:
        if not self.sana_flags.delegation:
            return plugins
        return [
            plugin
            for plugin in plugins
            if getattr(plugin, "name", None) != "agent_skills"
        ]

    def _tool_limit_excluded_tools(
        self,
        *,
        search_tool_mode: Optional[str],
        agent_management_mode: Optional[str] = None,
        plan_mode: Optional[str] = None,
    ) -> Sequence[str]:
        excluded = list(
            super()._tool_limit_excluded_tools(
                search_tool_mode=search_tool_mode,
                agent_management_mode=agent_management_mode or plan_mode,
            )
        )
        if self.sana_flags.cot:
            excluded.append("cot")
        if self.sana_flags.sprint:
            excluded.append("sprint")
        return tuple(excluded)


__all__ = ["SanaDataLakeAgent"]

"""Tests for SanaDataLakeAgent._decorate_tools — swaps peek_file when results is on."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from sana_evaluation.flags import SanaFlags
from sana_evaluation.sana_bundle import SanaDataLakeAgent
from sana_evaluation.sana_config import SanaRunConfig
from strands_evaluation.config import AgentConfig


def _make_agent(
    *,
    results: bool = False,
    sprint: bool = False,
    cot: bool = False,
    delegation: bool = False,
) -> SanaDataLakeAgent:
    flags = SanaFlags(results=results, sprint=sprint, cot=cot, delegation=delegation)
    rc = SanaRunConfig(
        plan_mode="standard",
        search_tool_mode="preloaded",
        search_results_mode="ideal",
        sana_flags=flags,
    )
    return SanaDataLakeAgent(AgentConfig(model_name="openai/gpt-5.4-nano"), rc)


class DecorateToolsTests(unittest.TestCase):
    def test_results_off_keeps_baseline_peek_file(self) -> None:
        agent = _make_agent(results=False)
        baseline_peek = MagicMock()
        baseline_peek.tool_name = "peek_file"
        other = MagicMock()
        other.tool_name = "query_file"
        decorated = agent._decorate_tools(
            [baseline_peek, other],
            search_tool_mode="preloaded",
            plan_mode="standard",
        )
        self.assertIs(decorated[0], baseline_peek)
        self.assertIs(decorated[1], other)

    def test_results_on_swaps_peek_file(self) -> None:
        agent = _make_agent(results=True)
        baseline_peek = MagicMock()
        baseline_peek.tool_name = "peek_file"
        other = MagicMock()
        other.tool_name = "query_file"
        decorated = agent._decorate_tools(
            [baseline_peek, other],
            search_tool_mode="preloaded",
            plan_mode="standard",
        )
        # peek_file should be replaced; query_file untouched
        self.assertIsNot(decorated[0], baseline_peek)
        self.assertEqual(getattr(decorated[0], "tool_name", None), "peek_file")
        self.assertIs(decorated[1], other)

    def test_results_on_swaps_peek_multiple(self) -> None:
        agent = _make_agent(results=True)
        baseline_peek = MagicMock()
        baseline_peek.tool_name = "peek_file"
        baseline_multi = MagicMock()
        baseline_multi.tool_name = "peek_multiple"
        other = MagicMock()
        other.tool_name = "query_file"
        decorated = agent._decorate_tools(
            [baseline_peek, baseline_multi, other],
            search_tool_mode="preloaded",
            plan_mode="standard",
        )
        self.assertEqual(getattr(decorated[0], "tool_name", None), "peek_file")
        self.assertEqual(getattr(decorated[1], "tool_name", None), "peek_multiple")
        self.assertIsNot(decorated[1], baseline_multi)
        self.assertIs(decorated[2], other)

    def test_sprint_on_adds_sprint_tool(self) -> None:
        agent = _make_agent(sprint=True)
        baseline_peek = MagicMock()
        baseline_peek.tool_name = "peek_file"
        decorated = agent._decorate_tools(
            [baseline_peek],
            search_tool_mode="preloaded",
            plan_mode="standard",
        )
        self.assertIn("sprint", [getattr(t, "tool_name", None) for t in decorated])

    def test_sprint_on_excludes_sprint_from_tool_limit(self) -> None:
        agent = _make_agent(sprint=True)
        excluded = agent._tool_limit_excluded_tools(
            search_tool_mode="preloaded",
            plan_mode="standard",
        )
        self.assertIn("sprint", excluded)

    def test_cot_on_does_not_add_post_tool_plugin(self) -> None:
        agent = _make_agent(cot=True)
        plugins = agent._extra_plugins(
            search_tool_mode="preloaded",
            plan_mode="standard",
        )
        self.assertNotIn("sana-cot-post-record", [plugin.name for plugin in plugins])

    def test_delegation_filters_planner_tools_to_delegation_surface(self) -> None:
        agent = _make_agent(delegation=True)
        tool_names = [
            "search_reranked",
            "plan",
            "list_files",
            "peek_file",
            "query_file",
            "execute_code",
            "submit_answer",
        ]
        tools = []
        for name in tool_names:
            tool = MagicMock()
            tool.tool_name = name
            tools.append(tool)

        decorated = agent._decorate_tools(
            tools,
            search_tool_mode="standard",
            plan_mode="standard",
        )

        decorated_names = [getattr(t, "tool_name", None) for t in decorated]
        self.assertEqual(
            decorated_names,
            ["plan", "submit_answer", "search_subagent", "inspect_subagent"],
        )
        self.assertNotIn("query_file", decorated_names)
        self.assertNotIn("execute_code", decorated_names)

    def test_delegation_removes_agent_skills_plugin(self) -> None:
        agent = _make_agent(delegation=True)
        skills_plugin = MagicMock()
        skills_plugin.name = "agent_skills"
        logging_plugin = MagicMock()
        logging_plugin.name = "logging"

        decorated = agent._decorate_plugins(
            [skills_plugin, logging_plugin],
            search_tool_mode="preloaded",
            plan_mode="standard",
        )

        self.assertEqual([plugin.name for plugin in decorated], ["logging"])


if __name__ == "__main__":
    unittest.main()

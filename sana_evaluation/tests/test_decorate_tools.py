"""Tests for SanaDataLakeAgent._decorate_tools — swaps peek_file when results is on."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from sana_evaluation.flags import SanaFlags
from sana_evaluation.sana_bundle import SanaDataLakeAgent
from sana_evaluation.sana_config import SanaRunConfig
from strands_evaluation.config import AgentConfig


def _make_agent(*, results: bool = False, sprint: bool = False, cot: bool = False) -> SanaDataLakeAgent:
    flags = SanaFlags(results=results, sprint=sprint, cot=cot)
    rc = SanaRunConfig(
        agent_management_mode="standard",
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
            agent_management_mode="standard",
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
            agent_management_mode="standard",
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
            agent_management_mode="standard",
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
            agent_management_mode="standard",
        )
        self.assertIn("sprint", [getattr(t, "tool_name", None) for t in decorated])

    def test_sprint_on_excludes_sprint_from_tool_limit(self) -> None:
        agent = _make_agent(sprint=True)
        excluded = agent._tool_limit_excluded_tools(
            search_tool_mode="preloaded",
            agent_management_mode="standard",
        )
        self.assertIn("sprint", excluded)

    def test_cot_on_adds_cot_tool(self) -> None:
        agent = _make_agent(cot=True)
        baseline_peek = MagicMock()
        baseline_peek.tool_name = "peek_file"
        decorated = agent._decorate_tools(
            [baseline_peek],
            search_tool_mode="preloaded",
            agent_management_mode="standard",
        )
        self.assertIn("cot", [getattr(t, "tool_name", None) for t in decorated])

    def test_cot_on_wires_steering_plugin_before_sprint(self) -> None:
        agent = _make_agent(cot=True, sprint=True)
        plugins = agent._extra_plugins(
            search_tool_mode="preloaded",
            agent_management_mode="standard",
        )
        names = [plugin.name for plugin in plugins]
        self.assertIn("sana-cot-steer", names)
        self.assertIn("sana-sprint-steer", names)
        self.assertLess(names.index("sana-cot-steer"), names.index("sana-sprint-steer"))
        self.assertNotIn("sana-cot-post-record", names)

    def test_cot_on_excludes_cot_from_tool_limit(self) -> None:
        agent = _make_agent(cot=True)
        excluded = agent._tool_limit_excluded_tools(
            search_tool_mode="preloaded",
            agent_management_mode="standard",
        )
        self.assertIn("cot", excluded)


if __name__ == "__main__":
    unittest.main()

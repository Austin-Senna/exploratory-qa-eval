"""Tests for SanaDataLakeAgent._decorate_tools — swaps peek_file when results is on."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from sana_evaluation.flags import SanaFlags
from sana_evaluation.sana_bundle import SanaDataLakeAgent
from sana_evaluation.sana_config import SanaRunConfig
from strands_evaluation.config import AgentConfig


def _make_agent(*, results: bool) -> SanaDataLakeAgent:
    flags = SanaFlags(results=results)
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


if __name__ == "__main__":
    unittest.main()

"""Tests for SanaDataLakeAgent._decorate_tools — swaps peek_file when results is on."""

from __future__ import annotations

import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

from strands.vended_plugins.steering import Proceed

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
            plan_mode="standard",
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

    def test_delegation_preloaded_planner_omits_search_subagent(self) -> None:
        agent = _make_agent(delegation=True)
        tools = []
        for name in ["plan", "submit_answer", "peek_file", "query_file"]:
            tool = MagicMock()
            tool.tool_name = name
            tools.append(tool)

        decorated = agent._decorate_tools(
            tools,
            search_tool_mode="preloaded",
            plan_mode="standard",
        )

        decorated_names = [getattr(t, "tool_name", None) for t in decorated]
        self.assertEqual(
            decorated_names,
            ["plan", "submit_answer", "inspect_subagent"],
        )
        self.assertNotIn("search_subagent", decorated_names)

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

def test_build_agent_applies_delegation_plugin_filter(monkeypatch) -> None:
    import strands_evaluation.agent_with_mode as agent_with_mode

    created = {}

    class _FakeStrandsAgent:
        def __init__(self, *args, **kwargs):
            created["plugins"] = kwargs["plugins"]
            created["tools"] = kwargs["tools"]
            created["system_prompt"] = kwargs["system_prompt"]
            self.model = kwargs["model"]

    monkeypatch.setattr(agent_with_mode, "Agent", _FakeStrandsAgent)
    monkeypatch.setattr(
        agent_with_mode,
        "load_ideal_plan_for_context",
        lambda task_context: SimpleNamespace(
            reasoning_chain_text="",
            source_sequence=["datagov/source-a/files/rows.txt"],
        ),
    )

    rc = SanaRunConfig(
        search_tool_mode="naive",
        search_results_mode="naive",
        agent_management_mode="standard",
        plan_skills_enabled=True,
        sana_flags=SanaFlags(delegation=True),
    )
    agent = SanaDataLakeAgent(AgentConfig(model_name="openai/gpt-5.4-nano"), rc)

    agent._build_agent(MagicMock(), task_context={})

    plugin_names = [getattr(plugin, "name", None) for plugin in created["plugins"]]
    assert "agent_skills" not in plugin_names
    assert "## SKILLS" not in created["system_prompt"]
    assert "skills(" not in created["system_prompt"]
    assert "search_subagent" in [getattr(tool, "tool_name", None) for tool in created["tools"]]


def test_build_agent_uses_lean_delegation_prompt(monkeypatch) -> None:
    import strands_evaluation.agent_with_mode as agent_with_mode

    created = {}

    class _FakeStrandsAgent:
        def __init__(self, *args, **kwargs):
            created["tools"] = kwargs["tools"]
            created["system_prompt"] = kwargs["system_prompt"]
            self.model = kwargs["model"]

    monkeypatch.setattr(agent_with_mode, "Agent", _FakeStrandsAgent)
    monkeypatch.setattr(
        agent_with_mode,
        "load_ideal_plan_for_context",
        lambda task_context: SimpleNamespace(
            reasoning_chain_text="",
            source_sequence=["datagov/source-a/files/rows.txt"],
        ),
    )

    rc = SanaRunConfig(
        search_tool_mode="standard",
        search_results_mode="ideal",
        agent_management_mode="standard",
        sana_flags=SanaFlags(delegation=True),
    )
    agent = SanaDataLakeAgent(AgentConfig(model_name="openai/gpt-5.4-nano"), rc)

    agent._build_agent(MagicMock(), task_context={})

    prompt = created["system_prompt"]
    assert "## DELEGATION PLANNER" in prompt
    assert "plan(" in prompt
    assert "search_subagent" in prompt
    assert "inspect_subagent" in prompt
    assert "submit_answer" in prompt
    for direct_tool in (
        "list_files",
        "peek_file",
        "query_file",
        "download",
        "execute_code",
        "get_sandbox_info",
        "cleanup_sandbox",
    ):
        assert direct_tool not in prompt


def test_build_agent_uses_inspect_only_delegation_prompt_for_preloaded(monkeypatch) -> None:
    import strands_evaluation.agent_with_mode as agent_with_mode

    created = {}

    class _FakeStrandsAgent:
        def __init__(self, *args, **kwargs):
            created["tools"] = kwargs["tools"]
            created["system_prompt"] = kwargs["system_prompt"]
            self.model = kwargs["model"]

    monkeypatch.setattr(agent_with_mode, "Agent", _FakeStrandsAgent)
    monkeypatch.setattr(
        agent_with_mode,
        "load_ideal_plan_for_context",
        lambda task_context: SimpleNamespace(
            reasoning_chain_text="",
            source_sequence=["datagov/source-a/files/rows.txt"],
        ),
    )

    rc = SanaRunConfig(
        search_tool_mode="preloaded",
        search_results_mode="ideal",
        agent_management_mode="standard",
        sana_flags=SanaFlags(delegation=True),
    )
    agent = SanaDataLakeAgent(AgentConfig(model_name="openai/gpt-5.4-nano"), rc)

    agent._build_agent(
        MagicMock(),
        task_context={
            "task_id": "task_1",
            "task_path": "tasks_core_quality/k-1-d-1/task_1.json",
        },
    )

    prompt = created["system_prompt"]
    tool_names = [getattr(tool, "tool_name", None) for tool in created["tools"]]
    assert "search_subagent" not in prompt
    assert "search_subagent" not in tool_names
    assert "inspect_subagent" in prompt
    assert "## PRELOADED DATASETS" in prompt


def test_sprint_plugins_inherit_search_free_exclusions() -> None:
    rc = SanaRunConfig(
        search_tool_mode="ideal",
        search_results_mode="ideal",
        agent_management_mode="standard",
        search_free=True,
        max_tool_calls=3,
        sana_flags=SanaFlags(sprint=True),
    )
    agent = SanaDataLakeAgent(AgentConfig(model_name="openai/gpt-5.4-nano"), rc)

    plugins = agent._extra_plugins(
        search_tool_mode="ideal",
        agent_management_mode="standard",
    )
    sprint_plugin = next(plugin for plugin in plugins if plugin.name == "sana-sprint-steer")
    sprint_plugin.on_after_tool(
        SimpleNamespace(tool_use={"name": "search_ideal"}, result=None, cancel_message=None)
    )

    action = asyncio.run(
        sprint_plugin.steer_before_tool(agent=None, tool_use={"name": "query_file"})
    )

    assert isinstance(action, Proceed)


if __name__ == "__main__":
    unittest.main()

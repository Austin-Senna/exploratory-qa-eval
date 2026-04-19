import asyncio
import time
import unittest
from types import SimpleNamespace

from strands_evaluation.config import AgentConfig
from strands_evaluation.instrumentation.agent_plugins import ToolLimitSteeringHandler
from strands_evaluation.tools import agent_tools, agent_tools_v2


class FakeModel:
    def __init__(self, config):
        self._config = config

    def get_config(self):
        return self._config

    def update_config(self, **model_config):
        self._config.update(model_config)


class TestToolLimitSteeringHandler(unittest.TestCase):
    def _make_agent(self, max_tokens=8096):
        return SimpleNamespace(
            model=FakeModel(
                {
                    "model_id": "gpt-5.2",
                    "params": {"max_completion_tokens": max_tokens},
                }
            )
        )

    def test_max_tokens_retry_guidance_lowers_retry_cap(self):
        handler = ToolLimitSteeringHandler(timeout_seconds=9999)
        handler._start_time = time.time()
        agent = self._make_agent()

        action = asyncio.run(
            handler.steer_after_model(
                agent=agent,
                message={"role": "assistant", "content": [{"text": "too long"}]},
                stop_reason="max_tokens",
            )
        )

        self.assertEqual(action.type, "guide")
        self.assertIn("hit the max token limit", action.reason)
        self.assertEqual(agent.model.get_config()["params"]["max_completion_tokens"], 4096)

    def test_repeated_max_tokens_forces_submit_only_cap(self):
        handler = ToolLimitSteeringHandler(timeout_seconds=9999, max_model_guides=2)
        handler._start_time = time.time()
        agent = self._make_agent()

        asyncio.run(
            handler.steer_after_model(
                agent=agent,
                message={"role": "assistant", "content": [{"text": "too long"}]},
                stop_reason="max_tokens",
            )
        )
        action = asyncio.run(
            handler.steer_after_model(
                agent=agent,
                message={"role": "assistant", "content": [{"text": "still too long"}]},
                stop_reason="max_tokens",
            )
        )

        self.assertEqual(action.type, "guide")
        self.assertIn("Call submit_answer NOW", action.reason)
        self.assertEqual(agent.model.get_config()["params"]["max_completion_tokens"], 2048)

    def test_retry_cap_never_increases_a_smaller_user_cap(self):
        handler = ToolLimitSteeringHandler(timeout_seconds=9999)
        handler._start_time = time.time()
        agent = self._make_agent(max_tokens=2048)

        asyncio.run(
            handler.steer_after_model(
                agent=agent,
                message={"role": "assistant", "content": [{"text": "too long"}]},
                stop_reason="max_tokens",
            )
        )

        self.assertEqual(agent.model.get_config()["params"]["max_completion_tokens"], 2048)

    def test_timeout_plain_text_turn_switches_to_submit_only(self):
        handler = ToolLimitSteeringHandler(timeout_seconds=1)
        handler._start_time = time.time() - 5
        agent = self._make_agent()

        action = asyncio.run(
            handler.steer_after_model(
                agent=agent,
                message={"role": "assistant", "content": [{"text": "final answer in prose"}]},
                stop_reason="end_turn",
            )
        )

        self.assertEqual(action.type, "guide")
        self.assertIn("Timeout reached", action.reason)
        self.assertIn("submit_answer NOW", action.reason)
        self.assertEqual(agent.model.get_config()["params"]["max_completion_tokens"], 2048)


class TestTokenBudgetDefaults(unittest.TestCase):
    def test_agent_config_default_max_tokens_is_8096(self):
        self.assertEqual(AgentConfig().max_tokens, 8096)

    def test_tool_result_caps_are_reduced(self):
        self.assertEqual(agent_tools._TOOL_RESULT_CHAR_CAP, 6_000)
        self.assertEqual(agent_tools_v2._TOOL_RESULT_CHAR_CAP, 6_000)


if __name__ == "__main__":
    unittest.main()

import asyncio
import unittest

from strands_evaluation.instrumentation.loop_plugin import CategoryStagnationHandler


class TestCategoryStagnationHandler(unittest.TestCase):
    def test_guide_reports_true_consecutive_count_before_reset(self):
        handler = CategoryStagnationHandler(max_consecutive_category=2)

        asyncio.run(handler.steer_before_tool(agent=None, tool_use={"name": "execute_code"}))
        asyncio.run(handler.steer_before_tool(agent=None, tool_use={"name": "query_file"}))
        action = asyncio.run(handler.steer_before_tool(agent=None, tool_use={"name": "grep_file"}))

        self.assertEqual(action.type, "guide")
        self.assertIn("used 'execute' tools 3 times in a row", action.reason)
        self.assertEqual(handler.consecutive_count, 0)


if __name__ == "__main__":
    unittest.main()

"""Unit tests for model pricing lookup behavior."""

import unittest

from strands_evaluation.helper.result import AgentResult


class _DummyMetrics:
    def __init__(self, input_tokens: int, output_tokens: int) -> None:
        self.accumulated_usage = {
            "inputTokens": input_tokens,
            "outputTokens": output_tokens,
        }
        self.cycle_count = 0
        self.cycle_durations = []
        self.tool_metrics = {}


def _build_result(model_name: str, input_tokens: int, output_tokens: int) -> AgentResult:
    return AgentResult(
        answer="",
        model="",
        model_name=model_name,
        metrics=_DummyMetrics(input_tokens, output_tokens),
    )


class PricingLookupTests(unittest.TestCase):
    def test_openai_prefixed_model_name_has_nonzero_cost(self) -> None:
        result = _build_result("openai/gpt-5.2", input_tokens=23616, output_tokens=285)
        self.assertGreater(result.cost_usd, 0.0)

    def test_openai_prefixed_and_unprefixed_keys_match_cost(self) -> None:
        prefixed = _build_result("openai/gpt-5.2", input_tokens=23616, output_tokens=285)
        unprefixed = _build_result("gpt-5.2", input_tokens=23616, output_tokens=285)
        self.assertAlmostEqual(prefixed.cost_usd, unprefixed.cost_usd, places=12)

    def test_bedrock_key_is_unchanged(self) -> None:
        result = _build_result("bedrock/claude-haiku-4.5", input_tokens=1000, output_tokens=500)
        # 1.00 * 1000/1e6 + 5.00 * 500/1e6
        expected = 0.0035
        self.assertAlmostEqual(result.cost_usd, expected, places=12)

    def test_unknown_model_returns_zero_and_logs_warning(self) -> None:
        result = _build_result("unknown/provider-model", input_tokens=1000, output_tokens=1000)
        with self.assertLogs("strands_evaluation.helper.result", level="WARNING") as captured:
            cost = result.cost_usd
        self.assertEqual(cost, 0.0)
        self.assertTrue(any("No pricing configured for model_name=unknown/provider-model" in m for m in captured.output))


if __name__ == "__main__":
    unittest.main()

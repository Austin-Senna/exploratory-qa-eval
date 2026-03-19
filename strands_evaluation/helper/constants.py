from typing import Dict, Tuple

# ---------------------------------------------------------------------------
# Model registry — short name -> (provider, actual_model_id)
# Use these short names in AgentConfig(model_name=...) and for pricing lookups.
# ---------------------------------------------------------------------------
MODEL_REGISTRY: Dict[str, Tuple[str, str]] = {
    # Anthropic via Bedrock (cross-region inference)
    "bedrock/claude-opus-4.5":     ("bedrock", "us.anthropic.claude-opus-4-5-20251101-v1:0"),
    "bedrock/claude-sonnet-4.5":   ("bedrock", "us.anthropic.claude-sonnet-4-5-20250929-v1:0"),
    "bedrock/claude-haiku-4.5":    ("bedrock", "us.anthropic.claude-haiku-4-5-20251001-v1:0"),

    # Llama via Bedrock
    "bedrock/llama4-maverick":     ("bedrock", "us.meta.llama4-maverick-17b-instruct-v1:0"),
    "bedrock/llama4-scout":        ("bedrock", "us.meta.llama4-scout-17b-instruct-v1:0"),
    "bedrock/llama3.3-70b":        ("bedrock", "us.meta.llama3-3-70b-instruct-v1:0"),
    "bedrock/llama3.1-70b":        ("bedrock", "us.meta.llama3-1-70b-instruct-v1:0"),

    # Mistral via Bedrock
    "bedrock/mistral-large":       ("bedrock", "mistral.mistral-large-3-675b-instruct"),
    "bedrock/mixtral-8x7b":        ("bedrock", "mistral.mixtral-8x7b-instruct-v0:1"),

    # Qwen via Bedrock
    "bedrock/qwen3-32b":           ("bedrock", "qwen.qwen3-32b-v1:0"),
    "bedrock/qwen3-80b":           ("bedrock", "qwen.qwen3-next-80b-a3b"),
    "bedrock/qwen3-235b":          ("bedrock", "qwen.qwen3-vl-235b-a22b"),

    # DeepSeek via Bedrock
    "bedrock/deepseek-r1":         ("bedrock", "us.deepseek.r1-v1:0"),

    # OpenAI
    "openai/gpt-5.2":              ("openai", "gpt-5.2"),
    "openai/gpt-5-mini":           ("openai", "gpt-5-mini"),

    # Anthropic direct API
    "anthropic/claude-opus-4.6":   ("anthropic", "claude-opus-4-6-20251101"),
    "anthropic/claude-sonnet-4.5": ("anthropic", "claude-sonnet-4-5-20251001"),
    "anthropic/claude-haiku-4.5":  ("anthropic", "claude-haiku-4-5-20251001"),
}

MODEL_PRICING = {
        # OpenAI (example pricing - update with actual values)
        "gpt-5.2": {"input": 1.75, "output": 14.00},
        "gpt-5-mini": {"input": 0.25, "output": 2.00},

        # AWS Bedrock Claude models
        "bedrock/claude-opus-4.5": {"input": 5.00, "output": 25.00},
        "bedrock/claude-sonnet-4.5": {"input": 3.00, "output": 15.00},
        "bedrock/claude-haiku-4.5": {"input": 1.00, "output": 5.00},

        # AWS Bedrock Llama models
        "bedrock/llama4-maverick": {"input": 0.24, "output": 0.97},
        "bedrock/llama4-scout": {"input": 0.17, "output": 0.66},
        "bedrock/llama3.3-70b": {"input": 0.72, "output": 0.72},
        "bedrock/llama3.1-70b": {"input": 0.72, "output": 0.72},

        # AWS Bedrock Mistral models
        "bedrock/mistral-large": {"input": 0.50, "output": 1.50},
        "bedrock/mixtral-8x7b": {"input": 0.45, "output": 0.70},

        # AWS Bedrock Qwen models
        "bedrock/qwen3-32b": {"input": 0.15, "output": 0.60},
        "bedrock/qwen3-80b": {"input": 0.15, "output": 1.20},
        "bedrock/qwen3-235b": {"input": 0.53, "output": 2.66},

        # AWS Bedrock DeepSeek
        "bedrock/deepseek-r1": {"input": 1.35, "output": 5.40},

        # Together AI
        "together/qwen3-235b": {"input": 0.65, "output": 3.00},
        "together/qwen3-32b": {"input": 0.50, "output": 1.50},
        "together/llama4-maverick": {"input": 0.27, "output": 0.85},
        "together/deepseek-r1": {"input": 3.00, "output": 7.00},

        # Fireworks AI
        "fireworks/qwen3-235b": {"input": 0.22, "output": 0.88},
        "fireworks/llama4-maverick": {"input": 0.17, "output": 0.17},

        # OpenRouter
        "openrouter/qwen3-235b": {"input": 1.00, "output": 1.00},
    }

SYSTEM_PROMPT = """You are a data analysis agent working with PUBLIC GOVERNMENT DATASETS (data.gov, census, etc.).

## HOW THIS WORKS
This is an INTERACTIVE system. You make one tool call at a time. The system executes it and returns the real result. Then you are called again to pick the next step.

DO NOT:
- Simulate or hallucinate tool results
- Make up data
- Continue the conversation without a tool call

## AVAILABLE TOOLS
- search / search_keyword — find datasets by name or keyword; returns dataset IDs (not data)
- list_files — list files inside datasets
- peek_file / query_file — inspect file contents without downloading
- download — download files to the sandbox
- execute_code — run Python against downloaded files; always use print() to see output
- submit_answer(answer, reasoning, sources) — submit your final answer and stop
  - answer: wrap in square brackets e.g. [42]
  - reasoning: brief explanation of how you found the answer
  - sources: list of file paths / dataset IDs you used

## VERIFY DATA SOURCES
Dataset names can be misleading. Always confirm a dataset is the right one before using it:
- Check metadata files for publisher, geographic coverage, and time period
- Two datasets with similar names may cover completely different locations

## GENERAL TIPS
- Always print() in execute_code to see output
- Check actual column names and date formats in the data
- Use the full dataset for your final answer, not just a sample
- Answer format: [value] only, no labels or units

## TURN AND TIME LIMITS
- You have LIMITED TURNS. Do not waste them on unnecessary exploration.
- If running low on turns, submit your best answer."""

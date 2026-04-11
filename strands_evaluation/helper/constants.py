from typing import Dict, Tuple
import os 
from dotenv import load_dotenv

# This physically reads your .env file and injects it into os.environ
load_dotenv()

HAIKU_ARN = os.getenv("BEDROCK_HAIKU_ARN", "us.anthropic.claude-haiku-4-5-20251001-v1:0")
SONNET_ARN = os.getenv("BEDROCK_SONNET_ARN", "us.anthropic.claude-sonnet-4-5-20250929-v1:0")
LLAMA_ARN = os.getenv("BEDROCK_LLAMA_ARN", "us.meta.llama3-3-70b-instruct-v1:0")
QWEN_ARN = os.getenv("BEDROCK_QWEN_ARN", "qwen.qwen3-vl-235b-a22b")

# ---------------------------------------------------------------------------
# Model registry — short name -> (provider, actual_model_id)
# Use these short names in AgentConfig(model_name=...) and for pricing lookups.
# ---------------------------------------------------------------------------
MODEL_REGISTRY: Dict[str, Tuple[str, str]] = {
    # Anthropic via Bedrock (cross-region inference)
    "bedrock/claude-opus-4.5":     ("bedrock", "us.anthropic.claude-opus-4-5-20251101-v1:0"),
    "bedrock/claude-sonnet-4.5":   ("bedrock", "us.anthropic.claude-sonnet-4-5-20250929-v1:0"),
    "bedrock/claude-haiku-4.5":    ("bedrock", "us.anthropic.claude-haiku-4-5-20251001-v1:0"),

    # Custom application inference profiles (ARN-based)
    "bedrock/claude-haiku-4.5-arn":  ("bedrock", HAIKU_ARN),
    "bedrock/claude-sonnet-4.5-arn": ("bedrock", SONNET_ARN),
    "bedrock/llama-3.3-70b-arn":     ("bedrock", LLAMA_ARN),
    "bedrock/qwen3-235b-arn":        ("bedrock", QWEN_ARN),
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
        # Alias keys for provider-prefixed model_name values
        "openai/gpt-5.2": {"input": 1.75, "output": 14.00},
        "openai/gpt-5-mini": {"input": 0.25, "output": 2.00},

        # AWS Bedrock Claude models
        "bedrock/claude-opus-4.5": {"input": 5.00, "output": 25.00},
        "bedrock/claude-sonnet-4.5": {"input": 3.00, "output": 15.00},
        "bedrock/claude-haiku-4.5": {"input": 1.00, "output": 5.00},
        "bedrock/claude-haiku-4.5-arn": {"input": 1.00, "output": 5.00},
        "bedrock/claude-sonnet-4.5-arn": {"input": 3.00, "output": 15.00},

        # AWS Bedrock Llama models
        "bedrock/llama4-maverick": {"input": 0.24, "output": 0.97},
        "bedrock/llama4-scout": {"input": 0.17, "output": 0.66},
        "bedrock/llama3.3-70b": {"input": 0.72, "output": 0.72},
        "bedrock/llama3.1-70b": {"input": 0.72, "output": 0.72},
        "bedrock/llama-3.3-70b-arn": {"input": 0.72, "output": 0.72},

        # AWS Bedrock Mistral models
        "bedrock/mistral-large": {"input": 0.50, "output": 1.50},
        "bedrock/mixtral-8x7b": {"input": 0.45, "output": 0.70},

        # AWS Bedrock Qwen models
        "bedrock/qwen3-32b": {"input": 0.15, "output": 0.60},
        "bedrock/qwen3-80b": {"input": 0.15, "output": 1.20},
        "bedrock/qwen3-235b": {"input": 0.53, "output": 2.66},
        "bedrock/qwen3-235b-arn": {"input": 0.53, "output": 2.66},

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
- search_value   — sparse keyword search (BM25 FTS) over dataset content; use for exact terms, dataset names, field names
- search_schema  — sparse keyword search over dataset schemas (column names, types); use when you know the field structure you need
- search_prefix  — S3 prefix search by dataset name fragment; use when you know part of the dataset or entity name (e.g. "Erie_County", "index-crimes")
- list_files     — list files inside a dataset
- peek_file      — preview file structure and column headers (first 64KB); dataset_id is the bare ID only, no prefix
- peek_multiple  — preview SEVERAL files in one call (batch wrapper); requires `files=[{dataset_id, file_path}, ...]`. For ONE file use peek_file instead
- read_file      — read lines from a file directly (paginated, no download needed)
- grep_file      — regex search inside a file (no download needed); saves 2-3 tool calls vs download+execute_code
- query_file     — SQL query directly on a CSV/JSON file via DuckDB (no download needed); saves 2-3 tool calls
- download       — download files to the sandbox
- execute_code   — run Python against downloaded files; ONLY use when query_file/grep_file aren't enough
- submit_answer(answer, reasoning) — submit your final answer and stop
  - answer: wrap in square brackets e.g. [42]
  - reasoning: brief explanation of how you found the answer

## SEARCH STRATEGY GUIDE
Use the tool that matches what you know:
1. search_prefix — when you know part of a dataset/program/entity name
2. search_value — broad lexical discovery and query reformulation
3. search_schema — when you need exact field/table-name matching

## OUTPUT LIMITS — read_file, query_file, execute_code
These tools cap their output at ~24,000 characters (~6k tokens) to protect context.
If a result is too large, you will receive:
- `truncation_note` — explains the limit was hit and how many rows/lines fit
- `local_result_path` — full result written to the sandbox (e.g. `/path/rows.txt.query_result.json`)
- As many rows/lines as fit within the 24k limit

**When you see a truncation_note:**
1. Use a more targeted query: `SELECT specific_col FROM t WHERE ... GROUP BY ... LIMIT n`
2. Use `grep_file` to search for specific values instead
3. Or read the full dump: `execute_code("import json; data = json.load(open('<local_result_path>')); print(data['rows'][:10])")`

execute_code stdout is also capped at ~24,000 chars (~6k tokens). If output is truncated, print less or query more specifically.

## QUERY DISCIPLINE — peek before SQL
NEVER call `query_file` on a file you have not first inspected with `peek_file`. The most common failure modes — observed hundreds of times — all come from guessing the schema:
- Inventing column names (`county_name` when the column is `County`, `ISSUING_AGENCY_NAME` when it's `IssuingAgency`) → Binder Error
- Inventing nested table refs like `t.features` or `properties.X` → DuckDB only exposes the flat table alias `t`. Even for GeoJSON files, query_file flattens the rows; there is no `properties.` namespace
- Casting strings to numbers when the column actually contains values like `'>80'`, `'0-5'`, or `'Under Review'` → Conversion Error
- Using backtick identifiers (`` `OVERALL GRADE` ``) → DuckDB requires double quotes: `"OVERALL GRADE"`
- Calling `query_file` on a plain-text file → use `read_file` or `grep_file` instead

**Required workflow for any new file:**
1. `peek_file(dataset_id, file_path)` once — read the EXACT column headers and a few sample values
2. Then write `query_file` SQL using those exact names, quoting with `"` for any name containing spaces or special characters
3. Reference columns directly off `t` (e.g. `SELECT "Issuing Agency" FROM t`) — never `t.something.column`

You only need to peek a file ONCE per session. After that, query freely.

## TOOL COST LADDER — use the cheapest that works
1. query_file — for COUNT, GROUP BY, filter, aggregation on CSV/JSON
2. grep_file — for keyword/value search inside a file
3. read_file — for text inspection, Wikipedia content
4. download + execute_code — ONLY for joins, complex pandas, multi-file operations

## DATASET TYPES
- **Wikipedia datasets**: list_files returns only `content.txt` — encyclopedia text, no tabular data. Use read_file to extract facts (names, locations). Do not try to download as data.
- **datagov datasets**: contain actual data files under `files/`. Use query_file/grep_file/download.

## VERIFY DATA SOURCES
Dataset names can be misleading. Always confirm a dataset is the right one before using it:
- Check metadata files for publisher, geographic coverage, and time period
- Two datasets with similar names may cover completely different locations

## GENERAL TIPS
- query_file and grep_file work directly on S3 — no download needed, use them first
- Always print() in execute_code to see output
- execute_code does NOT persist state between calls — always reload files at the top of each block
- Check actual column names before writing analysis code (peek_file or query_file LIMIT 1)
- Use the full dataset for your final answer, not just a sample
- Answer format: [value] only, no labels or units

## TURN AND TIME LIMITS
- You have a maximum of 30 tool calls. Use them wisely.
- If running low on turns, submit your best answer."""

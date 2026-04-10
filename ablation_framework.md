# Multi-Axis Ablation Framework

## What this adds
The ablation system now runs **three independent axes** instead of one condition-only switch:

- `search_tool`: `naive | standard | ideal`
- `search_results`: `naive | standard | ideal`
- `agent_management`: `naive | standard | ideal`

These are configured in `RunConfig` via:
- `search_tool_mode`
- `search_results_mode`
- `agent_management_mode`

## `strands_evaluation/run_mode_eval.py`
This is the new entrypoint for ablation runs.

### CLI behavior
It keeps the normal eval/search args (`--k`, `--search-calls`, `--task-dir`, `--all-tasks`, model args, etc.) and adds:

- `--search_tool {naive|standard|ideal}`
- `--search_results {naive|standard|ideal}`
- `--agent_management {naive|standard|ideal}`

### Variant labeling and outputs
Variant label is built as:

- `st-{search_tool}_sr-{search_results}_am-{agent_management}`
- optional suffixes: `_k{N}` and `_sc{N}`

Output layout:

- `results/{variant}/{base_condition}/{model}/...`
- `results/traces/{variant}/{base_condition}/{model}/...`

The runner still supports `--task-continue` (resume by skipping already-recorded tasks).

---

## `strands_evaluation/agent_with_mode.py`
Mode composition is inlined in this module.

### Role
It builds a `ModeBundle` containing:

- final `tools`
- final `system_prompt`
- `search_tool_names`
- booleans for `enable_skills` and `enable_stagnation`
- normalized mode values

### Mode normalization
Each axis is normalized and validated to one of:

- `naive`, `standard`, `ideal`

### Search tool mapping (`search_tool`)
- `naive`:
  - uses sparse search tools from `search_b_tools` (`search_value`, `search_schema`)
  - plus `search_prefix`
- `standard`:
  - uses hybrid (BM25 + dense) tools from `search_a_tools` (`search_value`, `search_schema`)
  - **without** cross-encoder reranked tool
  - plus `search_prefix`
- `ideal`:
  - uses `search_ideal.py` tool signatures
  - receives task context via `set_task_context(...)`

### Management mapping (`agent_management`)
- `naive`:
  - base prompt
  - no planning tools
  - no skills/stagnation helper
- `standard`:
  - loads condition B prompt (`prompts/condition_b.txt` fallback to base prompt)
  - adds `[plan, summarize_context]`
  - enables skills + stagnation plugin path
- `ideal`:
  - loads condition B prompt
  - injects task `reasoning_chain` into prompt via `inject_reasoning_chain_prompt(...)`
  - adds `[plan_ideal]`
  - does **not** enable skills/stagnation

---

## `strands_evaluation/tools/external/ideal/search_wrapper.py`
This wraps selected search tools for:

1. fixed-`k` enforcement (`search_k`)
2. result payload shaping (`search_results`)

### Result payload modes (`search_results`)
- `naive`:
  - returns only identifier-level fields (`uri`, inferred `dataset_id`)
- `standard`:
  - returns `uri`, `dataset_id`, and `snippet`
  - `snippet` is capped to **200 words** from available search text (`document/text/content`)
- `ideal`:
  - returns `uri`, `dataset_id`
  - enriches with:
    - `description` from `table_descriptions.jsonl`
    - `schema` text lookup from `lance_table_descriptions/lakeqa_schema`

### Tool wrapping behavior
For query tools and prefix tools, it preserves original signatures but:
- removes caller control over `top_k`/`limit` when fixed `k` is set
- applies payload reshaping on every call

---

## New supporting modules

### `strands_evaluation/tools/external/ideal/search_ideal.py`
Current status: **scaffold**.

- Exposes a single search tool: `search_ideal(query, top_k)`.
- Loads required per-task plans from `plans_mini/` using mirrored paths:
  - task: `tasks_mini/k-*-d-*/task_*.json`
  - plan: `plans_mini/k-*-d-*/task_*.json`
- Enforces strict plan schema:
  - `dataset_sequence` (ordered dataset IDs)
  - `reasoning_chain_text` (canonical long-form reasoning)
- Consumes one dataset from `dataset_sequence` per `search_ideal` call.
- Returns empty results with `plan_exhausted=true` once sequence is exhausted.
- Missing/invalid plan files hard-fail (no fallback to `tasks_mini`).

### `strands_evaluation/tools/external/ideal/plan_ideal.py`
Provides ideal planning utilities:

- `format_reasoning_chain(...)`
- `inject_reasoning_chain_prompt(...)`
- `plan_ideal(...)` tool (file-backed: loads from `plans_mini`, ignores manual plan text)

---

## Agent integration (`strands_evaluation/agent_with_mode.py`)

### Runtime switch
`DataLakeAgent._build_agent(...)` checks whether any ablation mode is set:

- if yes: uses the in-module mode-bundle builder
- if no: falls back to existing condition-based logic (`baseline/a/b`)

### Plugin behavior under modes
- Skills and stagnation plugin are controlled by `ModeBundle` flags.
- Search budget plugin still applies when `search_calls_limit` is set.
- Tool-limit and logging plugins still apply.

### Task context plumbing
Worker builds:
- `task_id`
- `datasets_used`
- `reasoning_chain`

and passes it to `DataLakeAgent.run(..., task_context=...)`.

### Worker search setup optimization (important)
For `naive` mode, worker **does not** call `search_b_tools.setup()` anymore.

- This avoids eager loading of heavy embedding/reranker stack on sparse-only paths.
- `--db-path` override is still honored by calling only `set_db_path(...)`.

---

## Tests added
- `test/test_mode_wrapper.py`
  - verifies mode mapping, file-backed ideal prompt injection, and `search_ideal` selection
- `test/test_search_wrapper.py`
  - verifies `naive` payload, 200-word truncation in `standard`, ideal description enrichment, and `search_ideal` tool-name detection
- `test/test_search_ideal.py`
  - verifies hard-fail on missing plans, strict dataset-sequence iteration, and exhaustion behavior

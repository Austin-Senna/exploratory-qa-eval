# Condition Implementation Reference

This document describes how conditions are implemented in the current codebase.
It is based on the live implementation in:

- `strands_evaluation/agent.py`
- `strands_evaluation/agent_with_mode.py`
- `strands_evaluation/helper/prompting.py`
- `strands_evaluation/run_mode_eval.py`
- `strands_evaluation/tools/external/ideal/*`

Where this differs from `ablation_framework.md`, this file reflects the current code.

## 1. Ideal implementations

The ideal path is now split across all three ablation axes and the dedicated ideal tools.

### `search_tool=ideal`

Implemented by `build_search(...)` in `strands_evaluation/agent_with_mode.py`.

- Exposes only:
  - `search_ideal`
- Passes task context into `search_ideal.set_task_context(...)`
- Uses the mirrored `plans_mini/.../task_*.json` file as the source of truth for dataset order

### `search_results=ideal`

Implemented by `build_results(...)` through `strands_evaluation/tools/external/ideal/search_wrapper.py`.

- Returns:
  - `uri`
  - `dataset_id`
  - `description`
  - `schema`
- `description` comes from `table_descriptions.jsonl`
- `schema` comes from `lance_table_descriptions/lakeqa_schema`
- Fixed `k` is enforced here when `RunConfig.search_k` is set

### `agent_management=ideal`

Implemented by `build_management(...)` in `strands_evaluation/agent_with_mode.py`.

- Prompt:
  - composed from:
    - `prompts/condition_b.txt`
    - `prompts/search_ideal.txt`
- Management tools:
  - `plan_ideal`
  - `summarize_context`
- Skills:
  - enabled
  - uses:
    - `plan-ideal`
    - `discover-data-ideal`
    - `query-data`
- Stagnation plugin:
  - enabled

Current code does not inject the reasoning chain during mode-bundle construction. Instead, `plan_ideal` loads the file-backed reasoning chain when the tool is called.

## 2. Ideal tool implementation

The new ideal behavior lives under `strands_evaluation/tools/external/ideal/`.

### `plan_store.py`

This is the shared loader for ideal-mode plans.

- It resolves task ids like:
  - `tasks_mini/k-2-d-4/task_1.json`
- Into plan paths like:
  - `plans_mini/k-2-d-4/task_1.json`
- Each plan file must contain:
  - `dataset_sequence`
  - `reasoning_chain_text`

Missing or invalid plan files fail fast.

### `search_ideal.py`

This is the ideal search tool.

- The tool surface is:
  - `search_ideal(query, top_k=10)`
- On task setup it loads the plan file and resets an internal cursor.
- In ideal mode this is the only search tool.
- Each call consumes up to five datasets from `dataset_sequence`.
- Search is restricted to those datasets only.
- It should be used until exhaustion; the agent will most likely need all the datasets.
- Returned payload includes:
  - `results`
  - `count`
  - `dataset_id`
  - `dataset_ids`
  - `plan_step_index`
  - `plan_step_number`
  - `plan_step_indexes`
  - `plan_step_numbers`
  - `plan_steps_total`
  - `datasets_per_call`
  - `plan_exhausted`
- Once all datasets are consumed, it returns empty results with `plan_exhausted=true`.

### `plan_ideal.py`

This is the ideal planning tool.

- The tool surface is currently:
  - `plan_ideal(plan_text, tool_context)`
- Manual `plan_text` is ignored.
- The tool loads the current task plan from `plans_mini`.
- It writes a new `## IDEAL PLAN` section into `agent.system_prompt`.
- That section includes:
  - the file-backed `reasoning_chain_text`
  - a directive telling the agent to build a numbered execution plan from that chain
- Current instruction policy:
  - copying the chain is allowed
  - producing a clearer, more executable plan is preferred

## 3. Other ablation implementations

Multi-axis ablations are implemented in `strands_evaluation/agent_with_mode.py` and invoked through `strands_evaluation/run_mode_eval.py`.

Condition B-style prompt and skill composition is centralized in `strands_evaluation/helper/prompting.py`.

- `prompts/condition_b.txt` is now the generic Condition B management/base prompt
- `prompts/baseline.txt` is now the generic baseline/search-only base prompt
- search-specific instructions live in:
  - `prompts/search_naive.txt`
  - `prompts/search_standard.txt`
  - `prompts/search_ideal.txt`
- search-mode-specific discovery skills live in:
  - `strands_evaluation/tools/skills/discover-data-naive`
  - `strands_evaluation/tools/skills/discover-data-standard`
  - `strands_evaluation/tools/skills/discover-data-ideal`
- all three discovery skill variants expose the same skill name to the agent:
  - `discover-data`

The three axes are:

- `search_tool`
- `search_results`
- `agent_management`

`run_mode_eval.py` builds output paths like:

- `results/st-{search_tool}_sr-{search_results}_am-{agent_management}/{base_condition}/{model}/...`

The `base_condition` is still carried for output nesting and compatibility, but the agent behavior comes from the three mode builders.

### `search_tool=standard`

- Uses full Condition A search surface:
  - `search_value`
  - `search_schema`
  - `search_reranked`
  - `search_prefix`

### `search_tool=naive`

- Uses Condition B sparse search tools:
  - `search_value`
  - `search_schema`
  - `search_prefix`

### `search_results=standard`

- Returns:
  - `uri`
  - `dataset_id`
  - `score`
  - `snippet`
- `snippet` is truncated to 200 words

### `search_results=naive`

- Returns only `uri`

### `agent_management=standard`

- Prompt:
  - composed from:
    - `prompts/condition_b.txt`
    - one search overlay chosen by `search_tool`:
      - `prompts/search_naive.txt`
      - `prompts/search_standard.txt`
      - `prompts/search_ideal.txt`
- Management tools:
  - `plan`
  - `summarize_context`
- Skills:
  - enabled
  - uses:
    - `plan-agent`
    - one discovery skill chosen by `search_tool`:
      - `discover-data-naive`
      - `discover-data-standard`
      - `discover-data-ideal`
    - `query-data`
- Stagnation plugin:
  - enabled

### `agent_management=naive`

- Prompt:
  - composed from:
    - `prompts/baseline.txt`
    - one search overlay chosen by `search_tool`:
      - `prompts/search_naive.txt`
      - `prompts/search_standard.txt`
      - `prompts/search_ideal.txt`
- Management tools:
  - none
- Skills:
  - disabled
- Stagnation plugin:
  - disabled

## 4. Legacy condition implementations

These are the original condition paths used when no ablation mode overrides are set.

### `baseline`

Implemented in `strands_evaluation/agent.py`.

- Search tools:
  - `search_value` from `search_b_tools`
  - `search_schema` from `search_b_tools`
  - `search_prefix`
- Prompt:
  - composed from:
    - `prompts/baseline.txt`
    - `prompts/search_naive.txt`
- Management tools:
  - none
- Data tools:
  - standard file/query/download/execute/submit tool set
- Skills:
  - disabled
- Stagnation plugin:
  - disabled

This is effectively "Condition B search stack without planning/context helpers".

### `a`

Implemented in `strands_evaluation/agent.py`.

- Search tools:
  - `search_value` from `search_a_tools`
  - `search_schema` from `search_a_tools`
  - `search_reranked`
  - `search_prefix`
- Prompt:
  - `prompts/condition_a.txt` if present, otherwise base prompt
- Management tools:
  - none
- Data tools:
  - standard file/query/download/execute/submit tool set
- Skills:
  - disabled
- Stagnation plugin:
  - disabled

This is the tools-rich condition.

### `b`

Implemented in `strands_evaluation/agent.py`.

- Search tools:
  - `search_value` from `search_b_tools`
  - `search_schema` from `search_b_tools`
  - `search_prefix`
- Prompt:
  - composed from:
    - `prompts/condition_b.txt`
    - `prompts/search_naive.txt`
- Management tools:
  - `plan`
  - `summarize_context`
- Data tools:
  - standard file/query/download/execute/submit tool set
- Skills:
  - enabled
  - uses:
    - `plan-agent`
    - `discover-data-naive`
    - `query-data`
- Stagnation plugin:
  - enabled

This is the planning-rich condition.

## 5. Runtime behavior notes

### Task context

Worker code builds and passes:

- `task_id`
- `datasets_used`
- `reasoning_chain`

For ideal tools, the actual source of truth is still the mirrored `plans_mini` file, not `task_context["reasoning_chain"]`.

### Search backend initialization

In `agent_with_mode.py` worker setup:

- `search_tool=standard` initializes the Condition A hybrid backend
- `search_tool=naive` avoids calling `search_b_tools.setup()`
  - this prevents loading dense/reranker components on sparse-only runs
- `search_tool=ideal` passes `db_path` through to `search_ideal`

### Shared plugins

Across both legacy and mode-based agents:

- tool-limit steering stays enabled
- logging stays enabled
- search-call budget plugin still applies when configured
- trace/read-trace plugins still apply

## 6. Summary mapping

### Ideal path

- `search_ideal` controls ideal retrieval order through `dataset_sequence`
- `plan_ideal` controls ideal planning context through `reasoning_chain_text`
- `plan-ideal` skill encourages the agent to turn the reasoning chain into a better execution plan

### Legacy conditions

- `baseline` = sparse Condition B search, no planning helpers
- `a` = full Condition A search, no planning helpers
- `b` = sparse Condition B search plus planning/context helpers

### Ablation axes

- `search_tool` controls which search tools exist
- `search_results` controls how much result content is exposed
- `agent_management` controls prompt source, planning tools, skills, and stagnation handling

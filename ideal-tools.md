# Ideal Tools

This note summarizes how `strands_evaluation` implements ideal execution,
ideal planning, and ideal search, and how those tools are added to the
Strands agent.

## Shared Ideal Plan Source

All three ideal features are backed by authored JSON plan files loaded through
`strands_evaluation/tools/external/ideal/plan_store.py`.

Each loaded plan becomes an `IdealTaskPlan` with:

- `dataset_sequence`
- `source_sequence`
- `reasoning_chain_text`
- `ideal_query`
- `ideal_code`

Task ids are mapped from task paths to mirrored plan paths:

- `tasks_mini/...` -> `plans_mini/...`
- `tasks_core/...` -> `plans_mini/tasks_core/...`
- `tasks_core_quality/...` -> `plans_core_quality/...`

The loader validates dataset ids, source paths, reasoning-chain text, and any
authored computation records before returning the plan.

## Ideal Planning

Ideal planning lives in
`strands_evaluation/tools/external/ideal/plan_ideal.py`.

When `agent_management_mode == "ideal"`, `agent_with_mode.py` loads the
ideal plan, injects `reasoning_chain_text` into the system prompt as
`GOLD REASONING CHAIN`, and swaps the normal `plan` tool for `plan_ideal`.

`plan_ideal(plan_text, tool_context)` mutates the live agent's system prompt by
appending or replacing an `IDEAL EXECUTION PLAN` section. This lets the
agent-written plan persist across turns while remaining grounded in the gold
reasoning chain.

## Ideal Search

Ideal search lives in
`strands_evaluation/tools/external/ideal/search_ideal.py`.

When `search_tool_mode == "ideal"`, `build_search()` calls
`search_ideal.set_task_context(task_context)` and returns only the
`search_ideal` tool.

`set_task_context()` loads the active plan and turns `source_sequence` into a
candidate pool of planned S3 URIs. `search_ideal(query)` does not query a real
search index. Instead, it builds a small internal Strands `Agent` with a
`pick` tool and asks a judge model to choose relevant remaining planned sources
from that pool.

Picked URIs are marked used, so later calls search only unused planned sources.
If nothing is close enough, the tool returns an empty result with
`Dataset not found`. If the whole planned pool is exhausted, it also reports
`plan_exhausted` unless `search_lessguide` hides that guidance.

Search result richness is handled separately by
`strands_evaluation/tools/external/ideal/search_wrapper.py`. When
`search_results_mode == "ideal"`, it enriches returned rows with descriptions,
schema fields, and snippets.

## Ideal Execution

Ideal execution is implemented as replacement computation tools in
`strands_evaluation/tools/external/ideal/computation_ideal.py`.

When `computation_tool_mode == "ideal"`, `agent_with_mode.py` walks the normal
data-tool list and replaces:

- `query_file` with `query_ideal`
- `execute_code` with `execute_ideal`

It also injects prompt text telling the agent to use
`query_ideal(..., intent=...)` for SQL-style computation and
`execute_ideal(code, intent)` for Python computation.

`query_ideal` and `execute_ideal` first try to match the agent's SQL or Python
code plus intent against authored `ideal_query` or `ideal_code` records. If a
record matches, they return the stored answer directly with `ideal_oracle: True`.

If no record matches, they run a repair loop using another internal Strands
agent. The repair agent rewrites the SQL or Python code using the authored plan
records and available context, then the ideal tool calls the underlying real
`query_file` or `execute_code`. Repair results are marked with
`ideal_oracle: False` and include repair metadata.

## How The Tools Are Added To The Agent

The central assembler is `build_mode_bundle()` in
`strands_evaluation/agent_with_mode.py`. It normalizes four ablation axes:

- `search_tool_mode`
- `search_results_mode`
- `agent_management_mode`
- `computation_tool_mode`

Then it builds the final tool list:

```python
tools = list(search_tools) + list(management_tools) + list(data_tool_list)
```

That bundle is used when constructing the Strands `Agent`, along with the
composed system prompt, conversation manager, plugins, tool executor, and
tracing/logging plugins.

The CLI exposes these axes in `strands_evaluation/run_mode_eval.py`:

- `--search_tool`
- `--search_results`
- `--agent_management`
- `--computation_tool`

In short:

- ideal planning gives the agent the gold reasoning chain and a persistent
  `plan_ideal` scratch plan;
- ideal search restricts discovery to the authored source pool and uses a
  judge agent to select planned sources;
- ideal execution replaces real SQL/Python execution tools with tools that can
  return authored answers directly or repair and execute the agent's attempt.

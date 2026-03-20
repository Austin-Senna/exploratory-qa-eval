# Sidecar Instrumentation — Design Reference

Removed from the codebase. Preserved here for future re-implementation or analysis.

## Purpose

Per-call trace logging for search and planning tools, written to JSONL files alongside
eval results. Enables post-hoc analysis of retrieval quality at the tool-call level
(MRR, hit@k, latency, gold-rank) without modifying Strands internals.

## How It Worked

### Context injection

Before each `agent.run()`, `set_sidecar_context(task_id, gold_dataset_ids, output_dir)`
was called. This set three module-level globals that all wrapped tools could read:

- `_current_task_id` — used as the JSONL filename and the `task_id` field
- `_current_gold_ids` — list of gold dataset IDs from `task["datasets_used"]`
- `_current_output_dir` — base path for JSONL output

### Decorator pattern

`instrument(tool_name, output_dir)(func)` returned a `functools.wraps` wrapper that:

1. Incremented a per-task turn counter
2. Measured wall-clock latency around `func(*args, **kwargs)`
3. Called `_extract_dataset_ids(result)` on the tool's return value to get which
   dataset IDs appeared in the results
4. Computed `gold_rank` — 1-based rank of the first gold dataset ID in the results,
   or -1 if none appeared
5. Wrote a JSONL record to `{output_dir}/{task_id}.jsonl`

Strands `@tool` metadata attributes (`TOOL_SPEC`, `tool_spec`, `__strands_tool__`,
`__tool_spec__`) were propagated from the original function to the wrapper so the
Strands framework continued to recognise the wrapped tools.

### JSONL record schema

```json
{
  "task_id": "tasks_mini/k-1-d-1/task_001.json",
  "turn": 3,
  "tool": "search_sparse",
  "query": "unemployment county 2019",
  "query_length_tokens": 5,
  "latency_ms": 142,
  "num_results": 10,
  "result_dataset_ids": ["unemployment-county-2019", "bls-laus-2019"],
  "gold_dataset_ids_in_results": ["unemployment-county-2019"],
  "gold_rank": 1,
  "timestamp_ms": 1710000000000
}
```

For planning tools (`generate_plan`, `generate_reflective_plan`) two extra fields
were added when present in the return dict:

```json
{
  "plan_text": "PLAN:\n...",
  "is_replan": false
}
```

### Dataset ID extraction

Tool results were expected to be dicts with a `"results"` list, where each item
had a `"dataset_uri"` or `"uri"` field. The S3 prefix
`s3://lakeqa-yc4103-datalake/` was stripped and the first path component was
taken as the dataset ID (e.g. `unemployment-county-2019`).

## Output location

`results/sidecar/{condition}/{model_id}/{task_id}.jsonl`

The condition and model subdirectory were constructed in `run_eval.py` before
building `ConditionConfig`, then passed as `sidecar_output_dir`.

## Analysis pipeline

The sidecar traces fed into:
- `analysis/discovery_metrics.py` — MRR, hit@1, hit@5 per condition
- `analysis/failure_attribution.py` — correlate gold_rank=-1 with task failure
- `analysis/behavioral.py` — turn-level query drift, plan revision frequency

## Re-implementation notes

- The decorator was applied in `agent.py` inside `_build_agent()`, only when
  `cond.enable_sidecar` was True. The wrapping happened after the tool functions
  were imported, before the `Agent(tools=[...])` call.
- `ConditionConfig` held `enable_sidecar: bool` and `sidecar_output_dir: str`.
- `run_eval.py` exposed `--enable-sidecar` and `--sidecar-output-dir` CLI flags.
- The `set_sidecar_context` call lived in `_run_task_worker` in `agent.py`.

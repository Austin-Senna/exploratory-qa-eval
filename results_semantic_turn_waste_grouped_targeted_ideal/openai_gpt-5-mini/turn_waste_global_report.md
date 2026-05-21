# Turn Waste Global Report

## Scope

- Source root: `results_semantic_turn_waste_grouped_targeted_ideal`
- Output root: `results_semantic_turn_waste_grouped_targeted_ideal`
- Model filter: `openai_gpt-5-mini`
- Processed files: 2
- Total grouped runtime-failure rows: 5
- Evidence mode: row `turn_waste_evidence` plus raw-log turn validation from `logs/modes`

## File Counts

- [openai_gpt-5-mini/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/eval_results.csv](modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/eval_results.csv): 1 grouped runtime-failure rows; failures table: [turn_waste_global_failures.csv](modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/turn_waste_global_failures.csv)
- [openai_gpt-5-mini/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/eval_results.csv](modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/eval_results.csv): 4 grouped runtime-failure rows; failures table: [turn_waste_global_failures.csv](modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/turn_waste_global_failures.csv)

## Counts by Reconciled Global Group

| Reconciled Global Group | Errors | Errors by Model |
| --- | --- | --- |
| Constraint and Format Recovery Thrash | 2 | openai_gpt-5-mini: 2 |
| Mostly On-Path Exhaustion | 2 | openai_gpt-5-mini: 2 |
| Answer-Ready Overshoot | 1 | openai_gpt-5-mini: 1 |

## Counts by Reconciled Global Group and Subtype

| Global Group | Subtype | Errors | Errors by Model | Representative |
| --- | --- | --- | --- | --- |
| Mostly On-Path Exhaustion | late broad probe after progress | 2 | openai_gpt-5-mini: 2 | [task](../../tasks_mini/k-3-d-3/task_6.json) / [plan](../../plans_mini/k-3-d-3/task_6.json) / [log](../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_6.log) |
| Answer-Ready Overshoot | Post-answer cross-checking until timeout | 1 | openai_gpt-5-mini: 1 | [task](../../tasks_mini/k-4-d-3/task_11.json) / [plan](../../plans_mini/k-4-d-3/task_11.json) / [log](../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| Constraint and Format Recovery Thrash | 500 Cities filter and schema thrash | 1 | openai_gpt-5-mini: 1 | [task](../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../plans_mini/k-6-d-2/task_4.json) / [log](../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| Constraint and Format Recovery Thrash | repeated 500 Cities diagnostics | 1 | openai_gpt-5-mini: 1 | [task](../../tasks_mini/k-5-d-4/task_2.json) / [plan](../../plans_mini/k-5-d-4/task_2.json) / [log](../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) |

## Counts by Original Global Group and Subtype

| Original Global Group | Subtype | Errors | Errors by Model | Representative |
| --- | --- | --- | --- | --- |
| Mostly On-Path Exhaustion | late broad probe after progress | 2 | openai_gpt-5-mini: 2 | [task](../../tasks_mini/k-3-d-3/task_6.json) / [plan](../../plans_mini/k-3-d-3/task_6.json) / [log](../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_6.log) |
| Answer-Ready Overshoot | Post-answer cross-checking until timeout | 1 | openai_gpt-5-mini: 1 | [task](../../tasks_mini/k-4-d-3/task_11.json) / [plan](../../plans_mini/k-4-d-3/task_11.json) / [log](../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| Constraint and Format Recovery Thrash | 500 Cities filter and schema thrash | 1 | openai_gpt-5-mini: 1 | [task](../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../plans_mini/k-6-d-2/task_4.json) / [log](../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| Constraint and Format Recovery Thrash | repeated 500 Cities diagnostics | 1 | openai_gpt-5-mini: 1 | [task](../../tasks_mini/k-5-d-4/task_2.json) / [plan](../../plans_mini/k-5-d-4/task_2.json) / [log](../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) |

## Canonical Groups

_Narrative claims below are limited to grouped counts, direct `turn_waste_evidence`, and optional validated log snippets._

### Constraint and Format Recovery Thrash

- Meaning: File size, schema uncertainty, parsing trouble, or query/tool constraints dominate the wasted tail, pulling the run into recovery work instead of task logic.
- Characteristics: large-file inspection loops or repeated schema peeks; parser or format recovery retries after errors; constraint workarounds that never transition into a clean extraction path
- Count: 2
- Subtypes: 500 Cities filter and schema thrash (1); repeated 500 Cities diagnostics (1)
- Representative evidence-backed rows:
  - [task](../../tasks_mini/k-5-d-4/task_2.json) | [plan](../../plans_mini/k-5-d-4/task_2.json) | [log](../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) | `tasks_mini/k-5-d-4/task_2.json` @ `search_p_results_i_plani_computei_k5_skills_off` (estimated wasted turns: 9)
    Evidence: Turn 20 | Executing: query_ideal({"s3_uri": "s3://lakeqa-yc4103-datalake/datagov/500-cities-local-data-for-better-health-2016-release/files/rows.txt"; Turn 21 | Executing: query_ideal({"s3_uri": "s3://lakeqa-yc4103-datalake/datagov/500-c...
    Log check: Turn 20: 2026-05-16 02:24:47 | INFO | strands_evaluation.instrumentation.agent_plugins | Executing: query_ideal({"s3_uri": "s3://lakeqa-yc4103-datalake/datagov/500-cities-local-data-for-...; Turn 21: 2026-05-16 02:25:22 | INFO | strands_evaluation.instrumentation.agent_plugins | Executing: query_ideal({"s3_uri": "s3://lakeqa-yc4103-datalake/datagov/500-cities-local-data-for-...
  - [task](../../tasks_mini/k-6-d-2/task_4.json) | [plan](../../plans_mini/k-6-d-2/task_4.json) | [log](../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) | `tasks_mini/k-6-d-2/task_4.json` @ `search_p_results_i_plani_computei_k5_skills_off` (estimated wasted turns: 9)
    Evidence: Turn 1 | Executing: plan_ideal({"plan_text": "1. Peek both 2016 and 2018 500-cities files; Turn 12 | Executing: query_ideal({"dataset_id": "500-cities-local-data-for-better-health-2016-release"; Turn 15 | Executing: query_ideal({"dataset...
    Log check: Turn 1: 2026-05-16 02:32:50 | INFO | strands_evaluation.instrumentation.agent_plugins | Executing: plan_ideal({"plan_text": "1. Peek both 2016 and 2018 500-cities files (query_ideal) to...; Turn 12: 2026-05-16 02:37:24 | INFO | strands_evaluation.instrumentation.agent_plugins | Executing: query_ideal({"dataset_id": "500-cities-local-data-for-better-health-2016-release", "fi...

### Mostly On-Path Exhaustion

- Meaning: The run remains largely productive and hits the token, time, or tool budget before a distinct wasted-tail pattern clearly emerges.
- Characteristics: the tail is still doing necessary extraction or synthesis work; estimated wasted turns are zero or small relative to the whole run; no single low-yield loop clearly dominates the ending
- Count: 2
- Subtypes: late broad probe after progress (2)
- Representative evidence-backed rows:
  - [task](../../tasks_mini/k-3-d-3/task_6.json) | [plan](../../plans_mini/k-3-d-3/task_6.json) | [log](../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_6.log) | `tasks_mini/k-3-d-3/task_6.json` @ `search_p_results_i_plani_computei_k5_skills_off` (estimated wasted turns: 5)
    Evidence: Turn 8 | Tool result: {"output": "['DEPARTMENT OF PUBLIC WORKS'; Turn 11 | Executing: plan_ideal({"plan_text": "1) Intersect the three top-20 agency lists; Turn 12 | Tool result: {"output": "[]\n"; Turn 14 | Tool result: {"output": "2019...
    Log check: Turn 8: 2026-05-16 00:16:37 | INFO | strands_evaluation.instrumentation.agent_plugins | Executing: execute_ideal({"dataset_id": "parking-violations-issued-in-january-2019", "file_path":...; Turn 11: 2026-05-16 00:16:56 | INFO | strands_evaluation.instrumentation.agent_plugins | Executing: plan_ideal({"plan_text": "1) Intersect the three top-20 agency lists (from earlier run...
  - [task](../../tasks_mini/k-4-d-4/task_6.json) | [plan](../../plans_mini/k-4-d-4/task_6.json) | [log](../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) | `tasks_mini/k-4-d-4/task_6.json` @ `search_p_results_i_plani_computei_k5_skills_off` (estimated wasted turns: 4)
    Evidence: Turn 21 | Executing: query_ideal({"s3_uri": "s3://lakeqa-yc4103-datalake/datagov/texas-state-expenditures-by-county-2018/files/rows.txt"; Turn 25 | Executing: query_ideal({"s3_uri": "s3://lakeqa-yc4103-datalake/datagov/texas-state-expend...
    Log check: Turn 21: 2026-05-16 01:28:17 | INFO | strands_evaluation.instrumentation.agent_plugins | Executing: query_ideal({"s3_uri": "s3://lakeqa-yc4103-datalake/datagov/texas-state-expenditures-b...; Turn 25: 2026-05-16 01:29:41 | INFO | strands_evaluation.instrumentation.agent_plugins | Executing: query_ideal({"s3_uri": "s3://lakeqa-yc4103-datalake/datagov/texas-state-expenditures-b...

### Answer-Ready Overshoot

- Meaning: The answer path is already mostly established, but the run spends its tail on extra checks, nearby-source validation, or one more low-yield action instead of submitting.
- Characteristics: late verification after the decisive clue is already visible; adjacent-source checking that does not materially change the answer; extra turns after a stop warning, timeout warning, or obvious answer-ready point
- Count: 1
- Subtypes: Post-answer cross-checking until timeout (1)
- Representative evidence-backed rows:
  - [task](../../tasks_mini/k-4-d-3/task_11.json) | [plan](../../plans_mini/k-4-d-3/task_11.json) | [log](../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) | `tasks_mini/k-4-d-3/task_11.json` @ `search_i_results_i_plani_computei_k5_skills_off` (estimated wasted turns: 9)
    Evidence: Turn 15 | Tool result: {"dataset_id": "county-population-in-iowa-by-year", "file_path": "files/rows.txt", "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/county-population-in-iowa-by-year/files/rows.txt", "columns": ["answer"], "rows": [[...
    Log check: Turn 15: 2026-05-15 06:49:19 | INFO | strands_evaluation.instrumentation.agent_plugins | Executing: query_ideal({"dataset_id": "county-population-in-iowa-by-year", "file_path": "files/ro...; Turn 16: 2026-05-15 06:49:49 | INFO | strands_evaluation.instrumentation.agent_plugins | Executing: query_ideal({"dataset_id": "county-population-in-iowa-by-year", "file_path": "files/ro...

## Notes

- This report does not restate `turn_waste_summary`, `turn_repeated_behavior`, or group reasons as fact.
- Stronger row-level claims should come from `turn_waste_evidence` or from rerunning with `--logs-dir` for validated turn snippets.
- When present, model-validation statuses other than `pass` or `repaired_pass` suppress row evidence in this report.
- Mixed or unresolved rows visible here: 0

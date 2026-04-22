# Turn Waste Global Report

## Scope

- Source root: `results-ec2_semantic_turn_waste`
- Output root: `results-ec2_semantic_turn_waste_grouped`
- Processed files: 5
- Total audited runtime-failure rows: 221

## File Counts

- [modes/openai_gpt-5.2-xhigh/search_d_results_i_plani_k5/eval_results.csv](modes/openai_gpt-5.2-xhigh/search_d_results_i_plani_k5/eval_results.csv): 30 audited rows, 30 runtime-failure rows; failures table: [turn_waste_global_failures.csv](modes/openai_gpt-5.2-xhigh/search_d_results_i_plani_k5/turn_waste_global_failures.csv)
- [modes/openai_gpt-5.2-xhigh/search_i_results_i_pland_k5/eval_results.csv](modes/openai_gpt-5.2-xhigh/search_i_results_i_pland_k5/eval_results.csv): 46 audited rows, 46 runtime-failure rows; failures table: [turn_waste_global_failures.csv](modes/openai_gpt-5.2-xhigh/search_i_results_i_pland_k5/turn_waste_global_failures.csv)
- [modes/openai_gpt-5.2-xhigh/search_i_results_i_plani_k5/eval_results.csv](modes/openai_gpt-5.2-xhigh/search_i_results_i_plani_k5/eval_results.csv): 37 audited rows, 37 runtime-failure rows; failures table: [turn_waste_global_failures.csv](modes/openai_gpt-5.2-xhigh/search_i_results_i_plani_k5/turn_waste_global_failures.csv)
- [modes/openai_gpt-5.2-xhigh/search_i_results_i_plann_k5/eval_results.csv](modes/openai_gpt-5.2-xhigh/search_i_results_i_plann_k5/eval_results.csv): 47 audited rows, 47 runtime-failure rows; failures table: [turn_waste_global_failures.csv](modes/openai_gpt-5.2-xhigh/search_i_results_i_plann_k5/turn_waste_global_failures.csv)
- [modes/openai_gpt-5.2-xhigh/search_n_results_i_plani_k5/eval_results.csv](modes/openai_gpt-5.2-xhigh/search_n_results_i_plani_k5/eval_results.csv): 61 audited rows, 61 runtime-failure rows; failures table: [turn_waste_global_failures.csv](modes/openai_gpt-5.2-xhigh/search_n_results_i_plani_k5/turn_waste_global_failures.csv)

## Canonical Groups

### endgame overshoot

- Count: 39
- Description: The run had essentially solved the task and then lost budget on one last low-value step.
- Subtypes: late-stage answer overshoot (39)
- Representative tasks: [tasks_mini/k-4-d-4/task_8.json @ search_i_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_plani_k5/k-4-d-4/task_8.log) [plan](../plans_mini/k-4-d-4/task_8.json) (6); [tasks_mini/k-3-d-4/task_3.json @ search_i_results_i_plann_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_plann_k5/k-3-d-4/task_3.log) [plan](../plans_mini/k-3-d-4/task_3.json) (5); [tasks_mini/k-7-d-4/task_6.json @ search_i_results_i_plann_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_plann_k5/k-7-d-4/task_6.log) [plan](../plans_mini/k-7-d-4/task_6.json) (5); [tasks_mini/k-5-d-4/task_10.json @ search_i_results_i_plann_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_plann_k5/k-5-d-4/task_10.log) [plan](../plans_mini/k-5-d-4/task_10.json) (4); [tasks_mini/k-7-d-4/task_8.json @ search_i_results_i_plann_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_plann_k5/k-7-d-4/task_8.log) [plan](../plans_mini/k-7-d-4/task_8.json) (4)

### endgame validation loop

- Count: 23
- Description: The run had narrowed the answer but kept validating alternates, edge cases, or extra corroboration.
- Subtypes: late candidate validation loop (23)
- Representative tasks: [tasks_mini/k-2-d-3/task_8.json @ search_i_results_i_plann_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_plann_k5/k-2-d-3/task_8.log) [plan](../plans_mini/k-2-d-3/task_8.json) (12); [tasks_mini/k-5-d-4/task_1.json @ search_n_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_n_results_i_plani_k5/k-5-d-4/task_1.log) [plan](../plans_mini/k-5-d-4/task_1.json) (10); [tasks_mini/k-3-d-3/task_10.json @ search_i_results_i_plann_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_plann_k5/k-3-d-3/task_10.log) [plan](../plans_mini/k-3-d-3/task_10.json) (6); [tasks_mini/k-2-d-4/task_9.json @ search_i_results_i_pland_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_pland_k5/k-2-d-4/task_9.log) [plan](../plans_mini/k-2-d-4/task_9.json) (5); [tasks_mini/k-2-d-3/task_1.json @ search_i_results_i_plann_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_plann_k5/k-2-d-3/task_1.log) [plan](../plans_mini/k-2-d-3/task_1.json) (5)

### same-source repetition

- Count: 45
- Description: The run stayed on the right source family but kept recomputing or reranking near-duplicate work.
- Subtypes: same-source recompute loop (28); school-report churn (17)
- Representative tasks: [tasks_mini/k-3-d-3/task_10.json @ search_i_results_i_pland_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_pland_k5/k-3-d-3/task_10.log) [plan](../plans_mini/k-3-d-3/task_10.json) (15); [tasks_mini/k-6-d-4/task_2.json @ search_i_results_i_pland_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_pland_k5/k-6-d-4/task_2.log) [plan](../plans_mini/k-6-d-4/task_2.json) (13); [tasks_mini/k-3-d-3/task_10.json @ search_d_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_d_results_i_plani_k5/k-3-d-3/task_10.log) [plan](../plans_mini/k-3-d-3/task_10.json) (8); [tasks_mini/k-6-d-4/task_9.json @ search_i_results_i_plann_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_plann_k5/k-6-d-4/task_9.log) [plan](../plans_mini/k-6-d-4/task_9.json) (8); [tasks_mini/k-3-d-3/task_1.json @ search_i_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_plani_k5/k-3-d-3/task_1.log) [plan](../plans_mini/k-3-d-3/task_1.json) (7)

### search or discovery churn

- Count: 14
- Description: The run kept rephrasing search/discovery steps instead of grounding new evidence.
- Subtypes: search reformulation loop (14)
- Representative tasks: [tasks_mini/k-3-d-4/task_1.json @ search_n_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_n_results_i_plani_k5/k-3-d-4/task_1.log) [plan](../plans_mini/k-3-d-4/task_1.json) (16); [tasks_mini/k-2-d-3/task_8.json @ search_i_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_plani_k5/k-2-d-3/task_8.log) [plan](../plans_mini/k-2-d-3/task_8.json) (8); [tasks_mini/k-4-d-4/task_3.json @ search_n_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_n_results_i_plani_k5/k-4-d-4/task_3.log) [plan](../plans_mini/k-4-d-4/task_3.json) (8); [tasks_mini/k-3-d-4/task_9.json @ search_d_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_d_results_i_plani_k5/k-3-d-4/task_9.log) [plan](../plans_mini/k-3-d-4/task_9.json) (7); [tasks_mini/k-3-d-4/task_7.json @ search_n_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_n_results_i_plani_k5/k-3-d-4/task_7.log) [plan](../plans_mini/k-3-d-4/task_7.json) (7)

### source inspection or schema thrash

- Count: 52
- Description: The run got stuck on file shape, schema, parser, or source-field inspection instead of progressing to synthesis.
- Subtypes: nces school-location spiral (32); problematic-data recovery thrash (20)
- Representative tasks: [tasks_mini/k-6-d-4/task_1.json @ search_i_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_plani_k5/k-6-d-4/task_1.log) [plan](../plans_mini/k-6-d-4/task_1.json) (17); [tasks_mini/k-7-d-3/task_4.json @ search_i_results_i_pland_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_pland_k5/k-7-d-3/task_4.log) [plan](../plans_mini/k-7-d-3/task_4.json) (13); [tasks_mini/k-6-d-4/task_6.json @ search_i_results_i_pland_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_pland_k5/k-6-d-4/task_6.log) [plan](../plans_mini/k-6-d-4/task_6.json) (12); [tasks_mini/k-4-d-3/task_9.json @ search_i_results_i_pland_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_pland_k5/k-4-d-3/task_9.log) [plan](../plans_mini/k-4-d-3/task_9.json) (7); [tasks_mini/k-7-d-4/task_8.json @ search_i_results_i_pland_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_pland_k5/k-7-d-4/task_8.log) [plan](../plans_mini/k-7-d-4/task_8.json) (7)

### source drift or reset

- Count: 35
- Description: The run made progress and then reset into rediscovery or drifted into the wrong adjacent source family.
- Subtypes: source-family drift or rediscovery reset (35)
- Representative tasks: [tasks_mini/k-7-d-4/task_4.json @ search_n_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_n_results_i_plani_k5/k-7-d-4/task_4.log) [plan](../plans_mini/k-7-d-4/task_4.json) (14); [tasks_mini/k-7-d-4/task_5.json @ search_n_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_n_results_i_plani_k5/k-7-d-4/task_5.log) [plan](../plans_mini/k-7-d-4/task_5.json) (11); [tasks_mini/k-4-d-3/task_5.json @ search_d_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_d_results_i_plani_k5/k-4-d-3/task_5.log) [plan](../plans_mini/k-4-d-3/task_5.json) (7); [tasks_mini/k-7-d-4/task_9.json @ search_n_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_n_results_i_plani_k5/k-7-d-4/task_9.log) [plan](../plans_mini/k-7-d-4/task_9.json) (7); [tasks_mini/k-3-d-4/task_7.json @ search_i_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_plani_k5/k-3-d-4/task_7.log) [plan](../plans_mini/k-3-d-4/task_7.json) (6)

### mixed or unclear

- Count: 13
- Description: No single dominant wasted-turn pattern was clear from the available row summary.
- Subtypes: mixed or unclear (13)
- Representative tasks: [tasks_mini/k-3-d-4/task_7.json @ search_d_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_d_results_i_plani_k5/k-3-d-4/task_7.log) [plan](../plans_mini/k-3-d-4/task_7.json) (1); [tasks_mini/k-6-d-4/task_8.json @ search_i_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_plani_k5/k-6-d-4/task_8.log) [plan](../plans_mini/k-6-d-4/task_8.json) (1); [tasks_mini/k-3-d-3/task_1.json @ search_d_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_d_results_i_plani_k5/k-3-d-3/task_1.log) [plan](../plans_mini/k-3-d-3/task_1.json) (0); [tasks_mini/k-3-d-3/task_3.json @ search_d_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_d_results_i_plani_k5/k-3-d-3/task_3.log) [plan](../plans_mini/k-3-d-3/task_3.json) (0); [tasks_mini/k-4-d-4/task_5.json @ search_d_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_d_results_i_plani_k5/k-4-d-4/task_5.log) [plan](../plans_mini/k-4-d-4/task_5.json) (0)

## Mixed Or Unresolved

- Mixed-or-unclear count: 13
- Examples: [tasks_mini/k-3-d-4/task_7.json @ search_d_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_d_results_i_plani_k5/k-3-d-4/task_7.log) [plan](../plans_mini/k-3-d-4/task_7.json); [tasks_mini/k-6-d-4/task_8.json @ search_i_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_plani_k5/k-6-d-4/task_8.log) [plan](../plans_mini/k-6-d-4/task_8.json); [tasks_mini/k-3-d-3/task_1.json @ search_d_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_d_results_i_plani_k5/k-3-d-3/task_1.log) [plan](../plans_mini/k-3-d-3/task_1.json); [tasks_mini/k-3-d-3/task_3.json @ search_d_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_d_results_i_plani_k5/k-3-d-3/task_3.log) [plan](../plans_mini/k-3-d-3/task_3.json); [tasks_mini/k-4-d-4/task_5.json @ search_d_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_d_results_i_plani_k5/k-4-d-4/task_5.log) [plan](../plans_mini/k-4-d-4/task_5.json); [tasks_mini/k-5-d-3/task_7.json @ search_d_results_i_plani_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_d_results_i_plani_k5/k-5-d-3/task_7.log) [plan](../plans_mini/k-5-d-3/task_7.json); [tasks_mini/k-3-d-3/task_2.json @ search_i_results_i_pland_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_pland_k5/k-3-d-3/task_2.log) [plan](../plans_mini/k-3-d-3/task_2.json); [tasks_mini/k-4-d-4/task_4.json @ search_i_results_i_pland_k5](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_pland_k5/k-4-d-4/task_4.log) [plan](../plans_mini/k-4-d-4/task_4.json)

## Notes

- `turn_waste_global_group` is now a broad behavior-first umbrella bucket.
- `turn_waste_global_subtype` preserves the earlier narrower pattern so corpus-specific slices are still available.
- Rows are sorted in failures tables by umbrella group, then descending `estimated_wasted_turns`, then `task_id`.

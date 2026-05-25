# Answer Failure Validation Report

- Source root: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_answer_failures`
- Logs root: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/logs/modes`
- Non-correct rows checked: 943
- Invalid or missing-log rows: 245

## Status Counts

- `invalid`: 245
- `valid`: 698

## Invalid Rows

- `tasks_mini/k-3-d-4/task_6.json` in `openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off`: invalid - event 1: exact evidence snippet for turn 20 does not match the raw log; event 1: exact evidence snippet for turn 19 does not match the raw log
- `tasks_mini/k-3-d-4/task_7.json` in `openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off`: invalid - event 1: exact evidence snippet for turn 11 does not match the raw log
- `tasks_mini/k-4-d-1/task_2.json` in `openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off`: invalid - event 1: exact evidence snippet for turn 10 does not match the raw log; event 2: exact evidence snippet for turn 10 does not match the raw log
- `tasks_mini/k-4-d-2/task_1.json` in `openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off`: invalid - event 2: exact evidence snippet for turn 18 does not match the raw log; event 2: exact evidence snippet for turn 21 does not match the raw log
- `tasks_mini/k-4-d-3/task_1.json` in `openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off`: invalid - event 1: exact evidence snippet for turn 13 does not match the raw log; event 2: exact evidence snippet for turn 32 does not match the raw log
- `tasks_mini/k-4-d-4/task_11.json` in `openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off`: invalid - event 1: exact evidence snippet for turn 1 does not match the raw log; event 1: exact evidence snippet for turn 13 does not match the raw log; event 2: exact evidence snippet for turn 12 does not match the raw log; event 3: exact evidence snippet for turn 31 does not match the raw log
- `tasks_mini/k-4-d-5/task_1.json` in `openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off`: invalid - event 1: exact evidence snippet for turn 26 does not match the raw log
- `tasks_mini/k-5-d-3/task_12.json` in `openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off`: invalid - event 1: exact evidence snippet for turn 30 does not match the raw log
- `tasks_mini/k-5-d-3/task_14.json` in `openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off`: invalid - event 1: exact evidence snippet for turn 30 does not match the raw log
- `tasks_mini/k-3-d-4/task_6.json` in `openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off`: invalid - event 1: invalid failure_stage `reasoning`
- `tasks_mini/k-4-d-1/task_3.json` in `openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off`: invalid - event 1: failure_evidence must start with `Turn N |` for rows with existing raw logs
- `tasks_mini/k-4-d-2/task_1.json` in `openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off`: invalid - event 1: exact evidence snippet for turn 15 does not match the raw log; event 1: exact evidence snippet for turn 17 does not match the raw log
- `tasks_mini/k-4-d-3/task_1.json` in `openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off`: invalid - event 1: exact evidence snippet for turn 31 does not match the raw log; event 1: exact evidence snippet for turn 32 does not match the raw log; event 1: exact evidence snippet for turn 33 does not match the raw log; event 2: exact evidence snippet for turn 21 does not match the raw log
- `tasks_mini/k-4-d-3/task_6.json` in `openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off`: invalid - event 1: invalid failure_stage `answer_selection`; event 1: failure_evidence must start with `Turn N |` for rows with existing raw logs
- `tasks_mini/k-4-d-4/task_11.json` in `openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off`: invalid - event 1: invalid failure_stage `aggregation`; event 1: failure_evidence must start with `Turn N |` for rows with existing raw logs
- `tasks_mini/k-5-d-3/task_14.json` in `openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off`: invalid - event 1: exact evidence snippet for turn 28 does not match the raw log
- `tasks_mini/k-5-d-4/task_5.json` in `openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off`: invalid - event 1: failure_evidence must start with `Turn N |` for rows with existing raw logs
- `tasks_mini/k-6-d-2/task_4.json` in `openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off`: invalid - event 1: missing confidence; event 1: invalid failure_stage `reasoning`; event 1: exact evidence snippet for turn 32 does not match the raw log; event 1: exact evidence snippet for turn 33 does not match the raw log
- `tasks_mini/k-4-d-1/task_2.json` in `openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off`: invalid - event 2: exact evidence snippet for turn 13 does not match the raw log; event 2: exact evidence snippet for turn 16 does not match the raw log; event 3: exact evidence snippet for turn 21 does not match the raw log
- `tasks_mini/k-4-d-3/task_11.json` in `openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off`: invalid - event 1: exact evidence snippet for turn 16 does not match the raw log

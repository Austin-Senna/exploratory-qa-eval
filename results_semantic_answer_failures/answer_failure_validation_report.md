# Answer Failure Validation Report

- Source root: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_answer_failures`
- Logs root: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/logs/modes`
- Non-correct rows checked: 943
- Invalid or missing-log rows: 56

## Status Counts

- `invalid`: 56
- `valid`: 706
- `valid_with_warnings`: 181

## Invalid Rows

- `tasks_mini/k-4-d-2/task_1.json` in `openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off`: invalid - event 1: invalid failure_stage `reasoning`
- `tasks_mini/k-4-d-3/task_1.json` in `openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off`: invalid - event 1: missing confidence; event 1: failure_evidence must start with `Turn N |` for rows with existing raw logs
- `tasks_mini/k-5-d-4/task_1.json` in `openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off`: invalid - event 1: invalid failure_stage `answering`; event 1: failure_evidence must start with `Turn N |` for rows with existing raw logs
- `tasks_mini/k-6-d-2/task_4.json` in `openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off`: invalid - event 1: invalid failure_stage `reasoning`; event 1: exact evidence snippet for turn 32 does not match the raw log; event 1: exact evidence snippet for turn 33 does not match the raw log
- `tasks_mini/k-5-d-3/task_12.json` in `openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off`: invalid - event 1: invalid failure_stage `final_answer`; event 1: failure_evidence must start with `Turn N |` for rows with existing raw logs
- `tasks_mini/k-3-d-4/task_6.json` in `openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off`: invalid - event 1: invalid failure_stage `reasoning`; event 1: failure_evidence must start with `Turn N |` for rows with existing raw logs
- `tasks_mini/k-5-d-3/task_12.json` in `openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off`: invalid - event 1: missing confidence; event 1: exact evidence snippet for turn 26 does not match the raw log
- `tasks_mini/k-6-d-3/task_5.json` in `openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off`: invalid - event 1: missing confidence; event 2: missing confidence; event 1: failure_evidence must start with `Turn N |` for rows with existing raw logs; event 2: failure_evidence must start with `Turn N |` for rows with existing raw logs
- `tasks_mini/k-3-d-4/task_6.json` in `openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off`: invalid - event 1: invalid failure_stage `calculation`
- `tasks_mini/k-4-d-3/task_11.json` in `openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off`: invalid - event 1: invalid failure_stage `final_answer_selection`; event 1: failure_evidence must start with `Turn N |` for rows with existing raw logs
- `tasks_mini/k-5-d-3/task_12.json` in `openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off`: invalid - event 1: invalid failure_stage `answer_generation`; event 1: failure_evidence must start with `Turn N |` for rows with existing raw logs
- `tasks_mini/k-3-d-4/task_7.json` in `openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off`: invalid - event 1: invalid failure_stage `answer_selection`; event 1: failure_evidence must start with `Turn N |` for rows with existing raw logs
- `tasks_mini/k-4-d-4/task_10.json` in `openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off`: invalid - event 1: missing confidence; event 1: failure_evidence must start with `Turn N |` for rows with existing raw logs
- `tasks_mini/k-4-d-4/task_5.json` in `openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off`: invalid - event 3: failure_evidence references turns beyond log max turn 22
- `tasks_mini/k-5-d-2/task_1.json` in `openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off`: invalid - event 1: missing failure_evidence; event 2: missing failure_evidence
- `tasks_mini/k-5-d-2/task_10.json` in `openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off`: invalid - event 2: failure_evidence references turns beyond log max turn 9; event 1: failure_evidence must start with `Turn N |` for rows with existing raw logs; event 2: failure_evidence must start with `Turn N |` for rows with existing raw logs
- `tasks_mini/k-6-d-2/task_1.json` in `openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off`: invalid - event 1: failure_evidence references turns beyond log max turn 27; event 1: failure_evidence must start with `Turn N |` for rows with existing raw logs
- `tasks_mini/k-2-d-3/task_1.json` in `openai_gpt-5.4-nano/search_i_results_i_pland_computei_k5_skills_off`: invalid - event 1: missing confidence; event 1: invalid failure_stage `answer_submission`; event 1: failure_evidence must start with `Turn N |` for rows with existing raw logs
- `tasks_mini/k-3-d-2/task_8.json` in `openai_gpt-5.4-nano/search_i_results_i_pland_computei_k5_skills_off`: invalid - event 1: missing confidence; event 1: failure_evidence must start with `Turn N |` for rows with existing raw logs
- `tasks_mini/k-3-d-3/task_4.json` in `openai_gpt-5.4-nano/search_i_results_i_pland_computei_k5_skills_off`: invalid - event 1: missing confidence

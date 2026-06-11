# Answer Failure Report

- Source root: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_answer_failures`
- Event rows: 71
- Trusted event rows: 59
- Non-correct eval rows: 45
- Events excluded by validation/model-validation: 12

## Counts by Failure Type

| Failure Type | Events |
| --- | --- |
| tool_or_data_blocker | 14 |
| wrong_source_or_scope | 14 |
| evidence_available_answer_error | 11 |
| incomplete_evidence_not_enough_turns | 6 |
| computation_or_aggregation_error | 4 |
| incomplete_evidence_early_answer | 3 |
| planning_decomposition_mismatch | 3 |
| extraction_or_parsing_error | 2 |
| question_or_constraint_misread | 2 |

## Counts by Failure Type and Subtype

| Failure Type | Subtype | Events | Representative |
| --- | --- | --- | --- |
| tool_or_data_blocker | tool_budget_exhausted | 4 | [task](../../../../tasks_mini/k-3-d-4/task_1.json) / [plan](../../../../plans_mini/k-3-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-4/task_1.log) |
| tool_or_data_blocker | unsupported_or_oversized_data_access | 4 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| incomplete_evidence_not_enough_turns | tool_budget_exhausted | 3 | [task](../../../../tasks_mini/k-4-d-4/task_6.json) / [plan](../../../../plans_mini/k-4-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| tool_or_data_blocker | data_source_missing_or_unavailable | 3 | [task](../../../../tasks_mini/k-3-d-4/task_3.json) / [plan](../../../../plans_mini/k-3-d-4/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-4/task_3.log) |
| incomplete_evidence_not_enough_turns | turn_or_time_budget_exhausted | 2 | [task](../../../../tasks_mini/k-5-d-4/task_2.json) / [plan](../../../../plans_mini/k-5-d-4/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) |
| tool_or_data_blocker | runner_or_event_loop_exception | 2 | [task](../../../../tasks_mini/k-5-d-3/task_13.json) / [plan](../../../../plans_mini/k-5-d-3/task_13.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-3/task_13.log) |
| wrong_source_or_scope | omitted authored city-based filter | 2 | [task](../../../../tasks_mini/k-3-d-2/task_10.json) / [plan](../../../../plans_mini/k-3-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| computation_or_aggregation_error | ranked raw rows instead of grouped sum | 1 | [task](../../../../tasks_mini/k-4-d-2/task_14.json) / [plan](../../../../plans_mini/k-4-d-2/task_14.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_14.log) |
| computation_or_aggregation_error | ratio-vs-change-rate mixup | 1 | [task](../../../../tasks_mini/k-3-d-2/task_2.json) / [plan](../../../../plans_mini/k-3-d-2/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_2.log) |
| computation_or_aggregation_error | raw count submitted instead of rounded per-century result | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| computation_or_aggregation_error | wrong postsecondary count in final sum | 1 | [task](../../../../tasks_mini/k-4-d-4/task_10.json) / [plan](../../../../plans_mini/k-4-d-4/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-4/task_10.log) |
| evidence_available_answer_error | final answer used wrong component counts | 1 | [task](../../../../tasks_mini/k-3-d-2/task_10.json) / [plan](../../../../plans_mini/k-3-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| evidence_available_answer_error | selected 1877 instead of 1869 | 1 | [task](../../../../tasks_mini/k-3-d-4/task_7.json) / [plan](../../../../plans_mini/k-3-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-4/task_7.log) |
| evidence_available_answer_error | submitted Loop income 67699 | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| evidence_available_answer_error | submitted bracketed counts instead of required subtraction | 1 | [task](../../../../tasks_mini/k-4-d-2/task_13.json) / [plan](../../../../plans_mini/k-4-d-2/task_13.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_13.log) |
| evidence_available_answer_error | submitted final answer from 817 minus 1 | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| evidence_available_answer_error | submitted the Harbor-based count of 389 from the wrong branch | 1 | [task](../../../../tasks_mini/k-4-d-2/task_8.json) / [plan](../../../../plans_mini/k-4-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_8.log) |
| evidence_available_answer_error | submitted the correct number with extra intermediate values | 1 | [task](../../../../tasks_mini/k-4-d-2/task_6.json) / [plan](../../../../plans_mini/k-4-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_6.log) |
| evidence_available_answer_error | submitted the wrong computed value | 1 | [task](../../../../tasks_mini/k-4-d-2/task_14.json) / [plan](../../../../plans_mini/k-4-d-2/task_14.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_14.log) |
| evidence_available_answer_error | submitted wrong subtraction from incorrect operand counts | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| evidence_available_answer_error | submitted_1992_instead_of_author_target_1936 | 1 | [task](../../../../tasks_mini/k-5-d-3/task_12.json) / [plan](../../../../plans_mini/k-5-d-3/task_12.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-3/task_12.log) |
| evidence_available_answer_error | wrong final answer from parsed grep subset | 1 | [task](../../../../tasks_mini/k-4-d-1/task_2.json) / [plan](../../../../plans_mini/k-4-d-1/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-1/task_2.log) |
| extraction_or_parsing_error | converted OPEN_DATE to MM/DD instead of extracting the required school-day value | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| extraction_or_parsing_error | wrong filter/row selection for private-school count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_6.json) / [plan](../../../../plans_mini/k-3-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| incomplete_evidence_early_answer | did not page past truncated excerpt | 1 | [task](../../../../tasks_mini/k-4-d-5/task_1.json) / [plan](../../../../plans_mini/k-4-d-5/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-5/task_1.log) |
| incomplete_evidence_early_answer | missing APD CAD aggregate | 1 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| incomplete_evidence_early_answer | premature answer with approximate estimate | 1 | [task](../../../../tasks_mini/k-3-d-4/task_3.json) / [plan](../../../../plans_mini/k-3-d-4/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-4/task_3.log) |
| incomplete_evidence_not_enough_turns | tool budget exhausted before locating the 2025 Chicago police salary schedule | 1 | [task](../../../../tasks_mini/k-4-d-4/task_4.json) / [plan](../../../../plans_mini/k-4-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-4/task_4.log) |
| planning_decomposition_mismatch | raw-row ordering instead of grouped SUM branch aggregation | 1 | [task](../../../../tasks_mini/k-5-d-3/task_9.json) / [plan](../../../../plans_mini/k-5-d-3/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-3/task_9.log) |
| planning_decomposition_mismatch | skipped four-year intersection | 1 | [task](../../../../tasks_mini/k-3-d-4/task_3.json) / [plan](../../../../plans_mini/k-3-d-4/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-4/task_3.log) |
| planning_decomposition_mismatch | used CAD sector hop instead of searches-by-type plan | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| question_or_constraint_misread | added spurious ward filter on final 2020 count | 1 | [task](../../../../tasks_mini/k-5-d-1/task_3.json) / [plan](../../../../plans_mini/k-5-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-1/task_3.log) |
| question_or_constraint_misread | used broad drug-keyword filter instead of exact Narcotic Drug Laws criterion | 1 | [task](../../../../tasks_mini/k-4-d-2/task_8.json) / [plan](../../../../plans_mini/k-4-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_8.log) |
| tool_or_data_blocker | ideal_repair_failure | 1 | [task](../../../../tasks_mini/k-7-d-4/task_1.json) / [plan](../../../../plans_mini/k-7-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-7-d-4/task_1.log) |
| wrong_source_or_scope | county-level aggregation ignored city-in-county scope | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| wrong_source_or_scope | county-level count omitted required city filter | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| wrong_source_or_scope | county/geography pivot from Whitman/Pullman to Garfield/Pomeroy | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| wrong_source_or_scope | dataset_mismatch | 1 | [task](../../../../tasks_mini/k-5-d-1/task_4.json) / [plan](../../../../plans_mini/k-5-d-1/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-1/task_4.log) |
| wrong_source_or_scope | dropped district-9 filter and used all-district sector ranking | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| wrong_source_or_scope | non-equivalent NOPD weapon query | 1 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| wrong_source_or_scope | switched to Harold Washington branch | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| wrong_source_or_scope | used Santa Monica instead of Los Angeles in the binge-drinking comparison | 1 | [task](../../../../tasks_mini/k-4-d-4/task_4.json) / [plan](../../../../plans_mini/k-4-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-4/task_4.log) |
| wrong_source_or_scope | used Wayne County-only postsecondary proxy and grep match count instead of Detroit-in-Wayne-County filtered count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_source_or_scope | used Wayne County-wide public-school count instead of Detroit-in-Wayne-County count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_source_or_scope | used county-seat city pages instead of county-level comparison | 1 | [task](../../../../tasks_mini/k-4-d-3/task_11.json) / [plan](../../../../plans_mini/k-4-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| wrong_source_or_scope | wrong year filter on FY2020 intake | 1 | [task](../../../../tasks_mini/k-3-d-3/task_4.json) / [plan](../../../../plans_mini/k-3-d-3/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-3/task_4.log) |

## Co-occurring Failure Types

| Failure Type Set | Rows |
| --- | --- |
| tool_or_data_blocker | 5 |
| evidence_available_answer_error | 4 |
| evidence_available_answer_error; wrong_source_or_scope | 4 |
| incomplete_evidence_not_enough_turns | 3 |
| wrong_source_or_scope | 3 |
| computation_or_aggregation_error | 2 |
| extraction_or_parsing_error | 2 |
| computation_or_aggregation_error; evidence_available_answer_error | 1 |
| computation_or_aggregation_error; planning_decomposition_mismatch; tool_or_data_blocker | 1 |
| evidence_available_answer_error; question_or_constraint_misread | 1 |
| evidence_available_answer_error; tool_or_data_blocker | 1 |
| incomplete_evidence_early_answer | 1 |
| incomplete_evidence_early_answer; planning_decomposition_mismatch; tool_or_data_blocker | 1 |
| incomplete_evidence_early_answer; wrong_source_or_scope | 1 |
| incomplete_evidence_not_enough_turns; tool_or_data_blocker | 1 |
| incomplete_evidence_not_enough_turns; tool_or_data_blocker; wrong_source_or_scope | 1 |
| incomplete_evidence_not_enough_turns; wrong_source_or_scope | 1 |
| planning_decomposition_mismatch; tool_or_data_blocker | 1 |
| question_or_constraint_misread | 1 |
| tool_or_data_blocker; wrong_source_or_scope | 1 |

## Representative Evidence

- `tasks_mini/k-2-d-3/task_1.json` `incomplete_evidence_early_answer`/`missing APD CAD aggregate`: Turn 9 | grep_file on apd-computer-aided-dispatch-incidents for Mental Health Incident returned 20 matches, truncated to 15; no aggregate count was produced.; Turn 34 | submit_answer answer=[1790]; reasoning says APD...
- `tasks_mini/k-2-d-3/task_1.json` `wrong_source_or_scope`/`non-equivalent NOPD weapon query`: Turn 15 | query_ideal semantic judge found no equivalent record for the NOPD weapon query; the submitted SQL filtered Use of Force Type by firearm/weapon/exhibited and was not semantically equivalent, so repair was in...
- `tasks_mini/k-3-d-2/task_1.json` `planning_decomposition_mismatch`/`used CAD sector hop instead of searches-by-type plan`: Turn 2 | Model response #2 [role=assistant block=1 tool_use] pick({"s3_uris": ["s3://lakeqa-yc4103-datalake/datagov/apd-computer-aided-dispatch-incidents/files/rows.txt", "s3://lakeqa-yc4103-datalake/datagov/apd-use-o...
- `tasks_mini/k-3-d-2/task_1.json` `tool_or_data_blocker`/`unsupported_or_oversized_data_access`: Turn 6 | WARNING | strands_evaluation.instrumentation.agent_plugins | Tool logical error (status=error): {"success": false, "error": "Cannot execute SQL: file is too big (1377 MB >= 500 MB limit).", "dataset_id": "apd...
- `tasks_mini/k-3-d-2/task_1.json` `computation_or_aggregation_error`/`raw count submitted instead of rounded per-century result`: Turn 12 | DEBUG | strands_evaluation.instrumentation.agent_plugins | Tool result: {"output": "59", "success": true, "dataset_id": "apd-use-of-force", "file_path": "files/rows.txt"}; Turn 16 | INFO | strands_evaluation...

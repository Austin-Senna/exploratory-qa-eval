# Answer Failure Report

- Source root: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_answer_failures`
- Event rows: 90
- Trusted event rows: 75
- Non-correct eval rows: 50
- Events excluded by validation/model-validation: 15

## Counts by Failure Type

| Failure Type | Events |
| --- | --- |
| wrong_source_or_scope | 21 |
| evidence_available_answer_error | 14 |
| tool_or_data_blocker | 13 |
| incomplete_evidence_not_enough_turns | 10 |
| planning_decomposition_mismatch | 8 |
| extraction_or_parsing_error | 2 |
| incomplete_evidence_early_answer | 2 |
| question_or_constraint_misread | 2 |
| computation_or_aggregation_error | 1 |
| query_execution_error_loop | 1 |
| semantic_or_gold_label_issue | 1 |

## Counts by Failure Type and Subtype

| Failure Type | Subtype | Events | Representative |
| --- | --- | --- | --- |
| tool_or_data_blocker | tool_budget_exhausted | 8 | [task](../../../../tasks_mini/k-4-d-2/task_1.json) / [plan](../../../../plans_mini/k-4-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| incomplete_evidence_not_enough_turns | tool_budget_exhausted | 4 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| tool_or_data_blocker | unsupported_or_oversized_data_access | 3 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| computation_or_aggregation_error | wrong ranking aggregation | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| evidence_available_answer_error | final answer used 1728 instead of 1724 | 1 | [task](../../../../tasks_mini/k-5-d-2/task_10.json) / [plan](../../../../plans_mini/k-5-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_10.log) |
| evidence_available_answer_error | final submission used the wrong school/day | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| evidence_available_answer_error | final_answer_included_intermediate_result | 1 | [task](../../../../tasks_mini/k-3-d-4/task_5.json) / [plan](../../../../plans_mini/k-3-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_5.log) |
| evidence_available_answer_error | incorrect_historical_year_off_by_one | 1 | [task](../../../../tasks_mini/k-4-d-3/task_9.json) / [plan](../../../../plans_mini/k-4-d-3/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_9.log) |
| evidence_available_answer_error | picked_fort_worth_isd_and_1889_instead_of_lake_worth_isd_and_1916 | 1 | [task](../../../../tasks_mini/k-5-d-3/task_3.json) / [plan](../../../../plans_mini/k-5-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| evidence_available_answer_error | selected Davenport city population as the final answer | 1 | [task](../../../../tasks_mini/k-4-d-3/task_11.json) / [plan](../../../../plans_mini/k-4-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| evidence_available_answer_error | submitted -184 instead of -1184 | 1 | [task](../../../../tasks_mini/k-4-d-2/task_13.json) / [plan](../../../../plans_mini/k-4-d-2/task_13.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_13.log) |
| evidence_available_answer_error | submitted 4 instead of the correct 7 | 1 | [task](../../../../tasks_mini/k-5-d-3/task_14.json) / [plan](../../../../plans_mini/k-5-d-3/task_14.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_14.log) |
| evidence_available_answer_error | submitted [30] from the wrong county pair instead of 13 | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| evidence_available_answer_error | submitted wrong final answer | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| evidence_available_answer_error | submitted_wrong_final_year | 1 | [task](../../../../tasks_mini/k-5-d-4/task_3.json) / [plan](../../../../plans_mini/k-5-d-4/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_3.log) |
| evidence_available_answer_error | switched_to_district_3 | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| evidence_available_answer_error | used_estimated_inputs_instead_of_source_counts | 1 | [task](../../../../tasks_mini/k-3-d-4/task_4.json) / [plan](../../../../plans_mini/k-3-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| evidence_available_answer_error | wrong_counts_averaged | 1 | [task](../../../../tasks_mini/k-3-d-3/task_4.json) / [plan](../../../../plans_mini/k-3-d-3/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_4.log) |
| extraction_or_parsing_error | extracted first constable instead of requested first head/superintendent | 1 | [task](../../../../tasks_mini/k-4-d-3/task_6.json) / [plan](../../../../plans_mini/k-4-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| extraction_or_parsing_error | wrong year span from museum page | 1 | [task](../../../../tasks_mini/k-3-d-4/task_7.json) / [plan](../../../../plans_mini/k-3-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_7.log) |
| incomplete_evidence_early_answer | asked for a fallback and submitted unable to determine before deriving the county | 1 | [task](../../../../tasks_mini/k-4-d-3/task_7.json) / [plan](../../../../plans_mini/k-4-d-3/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_7.log) |
| incomplete_evidence_early_answer | truncated_grep_sample_count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| incomplete_evidence_not_enough_turns | 30-call tool limit reached before verification completed | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| incomplete_evidence_not_enough_turns | repair failure plus tool budget exhaustion before correction | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| incomplete_evidence_not_enough_turns | tool budget exhausted before completing the intended comparison | 1 | [task](../../../../tasks_mini/k-4-d-3/task_2.json) / [plan](../../../../plans_mini/k-4-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| incomplete_evidence_not_enough_turns | tool budget exhausted before first hop finished | 1 | [task](../../../../tasks_mini/k-4-d-4/task_5.json) / [plan](../../../../plans_mini/k-4-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_5.log) |
| incomplete_evidence_not_enough_turns | tool budget exhausted before re-checking | 1 | [task](../../../../tasks_mini/k-5-d-3/task_14.json) / [plan](../../../../plans_mini/k-5-d-3/task_14.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_14.log) |
| incomplete_evidence_not_enough_turns | tool limit reached before overtime chain completed | 1 | [task](../../../../tasks_mini/k-4-d-4/task_4.json) / [plan](../../../../plans_mini/k-4-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_4.log) |
| planning_decomposition_mismatch | broader_capital_filter | 1 | [task](../../../../tasks_mini/k-3-d-3/task_4.json) / [plan](../../../../plans_mini/k-3-d-3/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_4.log) |
| planning_decomposition_mismatch | charter-school SQL skipped the required Ward 5 and grades filter | 1 | [task](../../../../tasks_mini/k-4-d-3/task_7.json) / [plan](../../../../plans_mini/k-4-d-3/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_7.log) |
| planning_decomposition_mismatch | consolidated_multi_year_aggregation | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| planning_decomposition_mismatch | pivoted from the Ward 7 result to a different Vincent C. Gray / Thomas Jefferson chain and submitted 1743 instead of 1735 | 1 | [task](../../../../tasks_mini/k-5-d-2/task_6.json) / [plan](../../../../plans_mini/k-5-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_6.log) |
| planning_decomposition_mismatch | sampled_rows_instead_of_district_average | 1 | [task](../../../../tasks_mini/k-5-d-3/task_3.json) / [plan](../../../../plans_mini/k-5-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| planning_decomposition_mismatch | skipped required intersection hop; chose Middlesex instead of Bergen | 1 | [task](../../../../tasks_mini/k-6-d-3/task_5.json) / [plan](../../../../plans_mini/k-6-d-3/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_5.log) |
| planning_decomposition_mismatch | skipped_four_year_intersection_and_final_filters | 1 | [task](../../../../tasks_mini/k-3-d-4/task_3.json) / [plan](../../../../plans_mini/k-3-d-4/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_3.log) |
| planning_decomposition_mismatch | used_non_equivalent_single_year_check_as_proxy | 1 | [task](../../../../tasks_mini/k-3-d-4/task_3.json) / [plan](../../../../plans_mini/k-3-d-4/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_3.log) |
| query_execution_error_loop | semantic no-match and JSONDecodeError repair failures | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| question_or_constraint_misread | used top-5 instead of top-2 | 1 | [task](../../../../tasks_mini/k-4-d-3/task_1.json) / [plan](../../../../plans_mini/k-4-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_1.log) |
| question_or_constraint_misread | wrong city pair and prevalence definition | 1 | [task](../../../../tasks_mini/k-4-d-4/task_5.json) / [plan](../../../../plans_mini/k-4-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_5.log) |
| semantic_or_gold_label_issue | gold answer conflicts with source text | 1 | [task](../../../../tasks_mini/k-4-d-5/task_1.json) / [plan](../../../../plans_mini/k-4-d-5/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_1.log) |
| tool_or_data_blocker | ideal_repair_failure | 1 | [task](../../../../tasks_mini/k-4-d-2/task_1.json) / [plan](../../../../plans_mini/k-4-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| tool_or_data_blocker | malformed_tool_call | 1 | [task](../../../../tasks_mini/k-4-d-2/task_6.json) / [plan](../../../../plans_mini/k-4-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_6.log) |
| wrong_source_or_scope | county lookup over broader city list | 1 | [task](../../../../tasks_mini/k-5-d-2/task_10.json) / [plan](../../../../plans_mini/k-5-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_10.log) |
| wrong_source_or_scope | dataset/year drift | 1 | [task](../../../../tasks_mini/k-4-d-2/task_1.json) / [plan](../../../../plans_mini/k-4-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| wrong_source_or_scope | extra PRECINCT=44 filter narrowed the 2022 count | 1 | [task](../../../../tasks_mini/k-4-d-1/task_3.json) / [plan](../../../../plans_mini/k-4-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_3.log) |
| wrong_source_or_scope | missed Boston-in-Suffolk constraint | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| wrong_source_or_scope | route_66_terminus_shift_to_santa_monica | 1 | [task](../../../../tasks_mini/k-5-d-4/task_3.json) / [plan](../../../../plans_mini/k-5-d-4/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_3.log) |
| wrong_source_or_scope | searched Chicago street-sweeping datasets while needing Washington, DC | 1 | [task](../../../../tasks_mini/k-4-d-3/task_7.json) / [plan](../../../../plans_mini/k-4-d-3/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_7.log) |
| wrong_source_or_scope | state-specific computation drifted to national county-count queries | 1 | [task](../../../../tasks_mini/k-5-d-3/task_14.json) / [plan](../../../../plans_mini/k-5-d-3/task_14.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_14.log) |
| wrong_source_or_scope | switched from VADIR comparison to AvgOfVio school-safety query | 1 | [task](../../../../tasks_mini/k-4-d-3/task_2.json) / [plan](../../../../plans_mini/k-4-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| wrong_source_or_scope | switched to P.S. 172 instead of the P.S. 380 candidate | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| wrong_source_or_scope | used SiteCounty and omitted exact ProgramYear filters | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| wrong_source_or_scope | used apd-searches instead of council-meeting-year source | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| wrong_source_or_scope | used city population dataset instead of county-level population | 1 | [task](../../../../tasks_mini/k-4-d-3/task_11.json) / [plan](../../../../plans_mini/k-4-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| wrong_source_or_scope | used county/state public-school scope instead of the required city-in-county scope | 1 | [task](../../../../tasks_mini/k-3-d-2/task_10.json) / [plan](../../../../plans_mini/k-3-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| wrong_source_or_scope | used current-dataset county counts instead of the task's expected counts | 1 | [task](../../../../tasks_mini/k-3-d-4/task_6.json) / [plan](../../../../plans_mini/k-3-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_6.log) |
| wrong_source_or_scope | used current-year-to-date complaints instead of historic complaints source | 1 | [task](../../../../tasks_mini/k-3-d-1/task_1.json) / [plan](../../../../plans_mini/k-3-d-1/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-1/task_1.log) |
| wrong_source_or_scope | wrong branch/community-area path | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| wrong_source_or_scope | wrong comparison city pair | 1 | [task](../../../../tasks_mini/k-4-d-4/task_4.json) / [plan](../../../../plans_mini/k-4-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_4.log) |
| wrong_source_or_scope | wrong filter branch | 1 | [task](../../../../tasks_mini/k-3-d-2/task_7.json) / [plan](../../../../plans_mini/k-3-d-2/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_7.log) |
| wrong_source_or_scope | wrong parcel candidate | 1 | [task](../../../../tasks_mini/k-4-d-4/task_13.json) / [plan](../../../../plans_mini/k-4-d-4/task_13.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_13.log) |
| wrong_source_or_scope | wrong_county_lookup | 1 | [task](../../../../tasks_mini/k-7-d-4/task_1.json) / [plan](../../../../plans_mini/k-7-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-7-d-4/task_1.log) |
| wrong_source_or_scope | wrong_state_lookup | 1 | [task](../../../../tasks_mini/k-4-d-4/task_11.json) / [plan](../../../../plans_mini/k-4-d-4/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_11.log) |

## Co-occurring Failure Types

| Failure Type Set | Rows |
| --- | --- |
| wrong_source_or_scope | 6 |
| evidence_available_answer_error; wrong_source_or_scope | 4 |
| incomplete_evidence_not_enough_turns; wrong_source_or_scope | 4 |
| tool_or_data_blocker | 4 |
| evidence_available_answer_error | 3 |
| tool_or_data_blocker; wrong_source_or_scope | 3 |
| evidence_available_answer_error; incomplete_evidence_not_enough_turns; wrong_source_or_scope | 2 |
| evidence_available_answer_error; planning_decomposition_mismatch | 2 |
| extraction_or_parsing_error | 2 |
| planning_decomposition_mismatch | 2 |
| planning_decomposition_mismatch; tool_or_data_blocker | 2 |
| computation_or_aggregation_error; wrong_source_or_scope | 1 |
| evidence_available_answer_error; incomplete_evidence_early_answer | 1 |
| evidence_available_answer_error; incomplete_evidence_not_enough_turns | 1 |
| evidence_available_answer_error; tool_or_data_blocker | 1 |
| incomplete_evidence_early_answer; planning_decomposition_mismatch; wrong_source_or_scope | 1 |
| incomplete_evidence_not_enough_turns; query_execution_error_loop | 1 |
| incomplete_evidence_not_enough_turns; question_or_constraint_misread | 1 |
| incomplete_evidence_not_enough_turns; tool_or_data_blocker | 1 |
| question_or_constraint_misread | 1 |
| semantic_or_gold_label_issue | 1 |

## Representative Evidence

- `tasks_mini/k-2-d-3/task_1.json` `tool_or_data_blocker`/`unsupported_or_oversized_data_access`: Turn 15 | WARNING | strands_evaluation.instrumentation.agent_plugins | Tool logical error (status=error): {"success": false, "error": "Cannot execute SQL: file is too big (1377 MB >= 500 MB limit).", "dataset_id": "ap...
- `tasks_mini/k-2-d-3/task_1.json` `incomplete_evidence_not_enough_turns`/`tool_budget_exhausted`: Turn 25 | DEBUG | strands_evaluation.instrumentation.agent_plugins | Model response #25 [role=assistant block=1 tool_use] execute_ideal({"code": "import json, collections, os\np='/home/ec2-user/eval_eqa/exploratory-qa...
- `tasks_mini/k-3-d-1/task_1.json` `wrong_source_or_scope`/`used current-year-to-date complaints instead of historic complaints source`: Turn 15 | execute_ideal({"file_path": "nypd-complaint-data-current-year-to-date/files/rows.txt", "code": "...", "intent": "Compute most common offense in Bronx for 2023 from complaints dataset"}); Turn 17 | Tool resul...
- `tasks_mini/k-3-d-2/task_1.json` `evidence_available_answer_error`/`switched_to_district_3`: Turn 31 | Model response #31 [role=assistant block=1 tool_use] execute_ideal({"code": "import boto3, csv, collections\ns3 = boto3.client('s3')\nbucket = 'lakeqa-yc4103-datalake'\nkey = 'datagov/apd-computer-aided-disp...
- `tasks_mini/k-3-d-2/task_1.json` `incomplete_evidence_early_answer`/`truncated_grep_sample_count`: Turn 24 | Model response #24 [role=assistant block=1 tool_use] grep_file({"dataset_id": "apd-use-of-force", "file_path": "files/rows.txt", "regex_pattern": ",2023,", "context_lines": 0}) ... Tool result: {"dataset_id"...

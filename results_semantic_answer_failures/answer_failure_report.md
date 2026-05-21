# Answer Failure Aggregate Report

- Source root: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_answer_failures`
- Event rows: 165
- Trusted event rows: 143
- Events excluded by validation/model-validation: 22

## Counts by Failure Type

| Failure Type | Events |
| --- | --- |
| wrong_source_or_scope | 38 |
| tool_or_data_blocker | 25 |
| evidence_available_answer_error | 18 |
| incomplete_evidence_early_answer | 11 |
| computation_or_aggregation_error | 9 |
| query_execution_error_loop | 9 |
| question_or_constraint_misread | 7 |
| incomplete_evidence_not_enough_turns | 6 |
| schema_or_shape_inspection_loop | 6 |
| extraction_or_parsing_error | 5 |
| planning_decomposition_mismatch | 5 |
| semantic_or_gold_label_issue | 2 |
| low_yield_search_loop | 1 |
| other_or_unclear | 1 |

## Counts by Failure Type and Subtype

| Failure Type | Subtype | Events | Representative |
| --- | --- | --- | --- |
| tool_or_data_blocker | ideal_repair_failure | 9 | [task](../tasks_mini/k-3-d-2/task_8.json) / [plan](../plans_mini/k-3-d-2/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| tool_or_data_blocker | unsupported_or_oversized_data_access | 6 | [task](../tasks_mini/k-4-d-1/task_1.json) / [plan](../plans_mini/k-4-d-1/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_1.log) |
| incomplete_evidence_not_enough_turns | tool_budget_exhausted | 5 | [task](../tasks_mini/k-4-d-2/task_4.json) / [plan](../plans_mini/k-4-d-2/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| tool_or_data_blocker | data_source_missing_or_unavailable | 4 | [task](../tasks_mini/k-3-d-2/task_11.json) / [plan](../plans_mini/k-3-d-2/task_11.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_11.log) |
| tool_or_data_blocker | tool_budget_exhausted | 3 | [task](../tasks_mini/k-3-d-3/task_4.json) / [plan](../plans_mini/k-3-d-3/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_4.log) |
| evidence_available_answer_error | wrong_final_entity | 2 | [task](../tasks_mini/k-3-d-2/task_12.json) / [plan](../plans_mini/k-3-d-2/task_12.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_12.log) |
| tool_or_data_blocker | tool_status_or_transport_error | 2 | [task](../tasks_mini/k-4-d-2/task_6.json) / [plan](../plans_mini/k-4-d-2/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_6.log) |
| wrong_source_or_scope | wrong_dataset_family | 2 | [task](../tasks_mini/k-4-d-5/task_3.json) / [plan](../plans_mini/k-4-d-5/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_3.log) |
| computation_or_aggregation_error | failed_intersection_minimum | 1 | [task](../tasks_mini/k-5-d-3/task_14.json) / [plan](../plans_mini/k-5-d-3/task_14.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_14.log) |
| computation_or_aggregation_error | inclusive_upper_bound_mismatch | 1 | [task](../tasks_mini/k-3-d-2/task_12.json) / [plan](../plans_mini/k-3-d-2/task_12.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_12.log) |
| computation_or_aggregation_error | incorrect_average | 1 | [task](../tasks_mini/k-3-d-3/task_4.json) / [plan](../plans_mini/k-3-d-3/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_4.log) |
| computation_or_aggregation_error | incorrect_branch_intersection | 1 | [task](../tasks_mini/k-5-d-3/task_9.json) / [plan](../plans_mini/k-5-d-3/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_9.log) |
| computation_or_aggregation_error | rounding_error | 1 | [task](../tasks_mini/k-3-d-4/task_2.json) / [plan](../plans_mini/k-3-d-4/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_2.log) |
| computation_or_aggregation_error | ward_comparison_confusion | 1 | [task](../tasks_mini/k-6-d-2/task_2.json) / [plan](../plans_mini/k-6-d-2/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_2.log) |
| computation_or_aggregation_error | wrong_cv_ranking | 1 | [task](../tasks_mini/k-5-d-4/task_9.json) / [plan](../plans_mini/k-5-d-4/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_9.log) |
| computation_or_aggregation_error | wrong_final_aggregation_scope | 1 | [task](../tasks_mini/k-5-d-1/task_3.json) / [plan](../plans_mini/k-5-d-1/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-1/task_3.log) |
| computation_or_aggregation_error | wrong_metric_and_scope | 1 | [task](../tasks_mini/k-3-d-4/task_3.json) / [plan](../plans_mini/k-3-d-4/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_3.log) |
| evidence_available_answer_error | answer_submission_mismatch | 1 | [task](../tasks_mini/k-4-d-3/task_3.json) / [plan](../plans_mini/k-4-d-3/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_3.log) |
| evidence_available_answer_error | blank_submission_after_giveup | 1 | [task](../tasks_mini/k-5-d-4/task_2.json) / [plan](../plans_mini/k-5-d-4/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) |
| evidence_available_answer_error | correct reasoning, wrong submitted answer | 1 | [task](../tasks_mini/k-3-d-2/task_5.json) / [plan](../plans_mini/k-3-d-2/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| evidence_available_answer_error | final_answer_substitution | 1 | [task](../tasks_mini/k-5-d-3/task_11.json) / [plan](../plans_mini/k-5-d-3/task_11.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_11.log) |
| evidence_available_answer_error | hallucinated_establishment_year | 1 | [task](../tasks_mini/k-5-d-2/task_11.json) / [plan](../plans_mini/k-5-d-2/task_11.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_11.log) |
| evidence_available_answer_error | selected_wrong_city_population | 1 | [task](../tasks_mini/k-4-d-3/task_11.json) / [plan](../plans_mini/k-4-d-3/task_11.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| evidence_available_answer_error | submitted_answer_from_wrong_intermediate_count | 1 | [task](../tasks_mini/k-3-d-2/task_9.json) / [plan](../plans_mini/k-3-d-2/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| evidence_available_answer_error | submitted_error_placeholder | 1 | [task](../tasks_mini/k-3-d-5/task_1.json) / [plan](../plans_mini/k-3-d-5/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-5/task_1.log) |
| evidence_available_answer_error | substituted_county_seat_year_for_school_district_year | 1 | [task](../tasks_mini/k-5-d-3/task_3.json) / [plan](../plans_mini/k-5-d-3/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| evidence_available_answer_error | wrong_department_head | 1 | [task](../tasks_mini/k-4-d-3/task_5.json) / [plan](../plans_mini/k-4-d-3/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_5.log) |
| evidence_available_answer_error | wrong_entity_submitted | 1 | [task](../tasks_mini/k-3-d-3/task_6.json) / [plan](../plans_mini/k-3-d-3/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_6.log) |
| evidence_available_answer_error | wrong_final_entity_chain | 1 | [task](../tasks_mini/k-5-d-4/task_9.json) / [plan](../plans_mini/k-5-d-4/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_9.log) |
| evidence_available_answer_error | wrong_final_submission | 1 | [task](../tasks_mini/k-5-d-2/task_6.json) / [plan](../plans_mini/k-5-d-2/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_6.log) |
| evidence_available_answer_error | wrong_founder_name | 1 | [task](../tasks_mini/k-4-d-3/task_12.json) / [plan](../plans_mini/k-4-d-3/task_12.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_12.log) |
| evidence_available_answer_error | wrong_neighborhood_to_community_area_mapping | 1 | [task](../tasks_mini/k-5-d-3/task_9.json) / [plan](../plans_mini/k-5-d-3/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_9.log) |
| evidence_available_answer_error | wrong_row_selected | 1 | [task](../tasks_mini/k-4-d-2/task_2.json) / [plan](../plans_mini/k-4-d-2/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_2.log) |
| extraction_or_parsing_error | bridge_year_taken_as_land_company_founding_year | 1 | [task](../tasks_mini/k-5-d-4/task_1.json) / [plan](../plans_mini/k-5-d-4/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_1.log) |
| extraction_or_parsing_error | county_fips_instead_of_county_name | 1 | [task](../tasks_mini/k-3-d-4/task_4.json) / [plan](../plans_mini/k-3-d-4/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| extraction_or_parsing_error | selected_opening_year_instead_of_establishment_year | 1 | [task](../tasks_mini/k-3-d-4/task_7.json) / [plan](../plans_mini/k-3-d-4/task_7.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_7.log) |
| extraction_or_parsing_error | sitecounty_instead_of_cecounty | 1 | [task](../tasks_mini/k-4-d-5/task_5.json) / [plan](../plans_mini/k-4-d-5/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| extraction_or_parsing_error | wrong_file_shape | 1 | [task](../tasks_mini/k-4-d-2/task_8.json) / [plan](../plans_mini/k-4-d-2/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_8.log) |
| incomplete_evidence_early_answer | (none) | 1 | [task](../tasks_mini/k-5-d-4/task_4.json) / [plan](../plans_mini/k-5-d-4/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_4.log) |
| incomplete_evidence_early_answer | answered_before_required_final_hop | 1 | [task](../tasks_mini/k-5-d-3/task_2.json) / [plan](../plans_mini/k-5-d-3/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_2.log) |
| incomplete_evidence_early_answer | blank_submission_after_blocker | 1 | [task](../tasks_mini/k-4-d-2/task_10.json) / [plan](../plans_mini/k-4-d-2/task_10.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_10.log) |
| incomplete_evidence_early_answer | gave_up_after_tool_errors | 1 | [task](../tasks_mini/k-3-d-4/task_3.json) / [plan](../plans_mini/k-3-d-4/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_3.log) |
| incomplete_evidence_early_answer | missing_later_hops | 1 | [task](../tasks_mini/k-6-d-2/task_2.json) / [plan](../plans_mini/k-6-d-2/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_2.log) |
| incomplete_evidence_early_answer | placeholder_submission | 1 | [task](../tasks_mini/k-4-d-2/task_13.json) / [plan](../plans_mini/k-4-d-2/task_13.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_13.log) |
| incomplete_evidence_early_answer | placeholder_submission_before_final_hops | 1 | [task](../tasks_mini/k-4-d-4/task_6.json) / [plan](../plans_mini/k-4-d-4/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| incomplete_evidence_early_answer | premature_insufficient_data_submission | 1 | [task](../tasks_mini/k-6-d-2/task_5.json) / [plan](../plans_mini/k-6-d-2/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_5.log) |
| incomplete_evidence_early_answer | premature_submission | 1 | [task](../tasks_mini/k-4-d-4/task_11.json) / [plan](../plans_mini/k-4-d-4/task_11.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_11.log) |
| incomplete_evidence_early_answer | submitted_before_required_later_hops_were_gathered | 1 | [task](../tasks_mini/k-5-d-3/task_15.json) / [plan](../plans_mini/k-5-d-3/task_15.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_15.log) |
| incomplete_evidence_early_answer | truncated_source_not_fully_read | 1 | [task](../tasks_mini/k-3-d-4/task_7.json) / [plan](../plans_mini/k-3-d-4/task_7.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_7.log) |
| incomplete_evidence_not_enough_turns | tool_budget_exhausted_before_final_hop | 1 | [task](../tasks_mini/k-3-d-3/task_2.json) / [plan](../plans_mini/k-3-d-3/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_2.log) |
| low_yield_search_loop | repeated_irrelevant_searches_for_school_evidence | 1 | [task](../tasks_mini/k-5-d-3/task_2.json) / [plan](../plans_mini/k-5-d-3/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_2.log) |
| other_or_unclear | placeholder_submission_after_blocker | 1 | [task](../tasks_mini/k-6-d-3/task_2.json) / [plan](../plans_mini/k-6-d-3/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_2.log) |
| planning_decomposition_mismatch | ad_hoc_candidate_lookup | 1 | [task](../tasks_mini/k-4-d-4/task_13.json) / [plan](../plans_mini/k-4-d-4/task_13.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_13.log) |
| planning_decomposition_mismatch | diverged_from_required_hop_chain | 1 | [task](../tasks_mini/k-4-d-4/task_2.json) / [plan](../plans_mini/k-4-d-4/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_2.log) |
| planning_decomposition_mismatch | divergent_lookup_path | 1 | [task](../tasks_mini/k-4-d-2/task_13.json) / [plan](../plans_mini/k-4-d-2/task_13.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_13.log) |
| planning_decomposition_mismatch | ignored_fixed_target_area | 1 | [task](../tasks_mini/k-4-d-2/task_2.json) / [plan](../plans_mini/k-4-d-2/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_2.log) |
| planning_decomposition_mismatch | skipped_required_hops | 1 | [task](../tasks_mini/k-5-d-3/task_12.json) / [plan](../plans_mini/k-5-d-3/task_12.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_12.log) |
| query_execution_error_loop | binder_error_and_repair_cycle | 1 | [task](../tasks_mini/k-5-d-4/task_2.json) / [plan](../plans_mini/k-5-d-4/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) |
| query_execution_error_loop | ideal_repair_failure | 1 | [task](../tasks_mini/k-5-d-3/task_1.json) / [plan](../plans_mini/k-5-d-3/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_1.log) |
| query_execution_error_loop | malformed_tool_call | 1 | [task](../tasks_mini/k-4-d-3/task_6.json) / [plan](../plans_mini/k-4-d-3/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| query_execution_error_loop | placeholder_sql_and_repair_failures | 1 | [task](../tasks_mini/k-5-d-3/task_12.json) / [plan](../plans_mini/k-5-d-3/task_12.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_12.log) |
| query_execution_error_loop | repair_churn_with_binder_error | 1 | [task](../tasks_mini/k-4-d-4/task_6.json) / [plan](../plans_mini/k-4-d-4/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| query_execution_error_loop | repeated_binder_and_unsupported_json_failures | 1 | [task](../tasks_mini/k-4-d-2/task_1.json) / [plan](../plans_mini/k-4-d-2/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| query_execution_error_loop | repeated_column_resolution_binder_errors | 1 | [task](../tasks_mini/k-6-d-2/task_3.json) / [plan](../plans_mini/k-6-d-2/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_3.log) |
| query_execution_error_loop | repeated_sql_repair_jsondecode | 1 | [task](../tasks_mini/k-4-d-4/task_2.json) / [plan](../plans_mini/k-4-d-4/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_2.log) |
| query_execution_error_loop | unsupported parser/tool choice for file format | 1 | [task](../tasks_mini/k-3-d-2/task_5.json) / [plan](../plans_mini/k-3-d-2/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| question_or_constraint_misread | birthplace_vs_namesake_confusion | 1 | [task](../tasks_mini/k-5-d-2/task_11.json) / [plan](../plans_mini/k-5-d-2/task_11.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_11.log) |
| question_or_constraint_misread | branch_as_neighborhood | 1 | [task](../tasks_mini/k-3-d-3/task_2.json) / [plan](../plans_mini/k-3-d-3/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_2.log) |
| question_or_constraint_misread | final_hop_relation_misread | 1 | [task](../tasks_mini/k-5-d-2/task_1.json) / [plan](../plans_mini/k-5-d-2/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_1.log) |
| question_or_constraint_misread | grouping_key_and_topk_misread | 1 | [task](../tasks_mini/k-5-d-3/task_8.json) / [plan](../plans_mini/k-5-d-3/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_8.log) |
| question_or_constraint_misread | returned_category_instead_of_count | 1 | [task](../tasks_mini/k-4-d-1/task_3.json) / [plan](../plans_mini/k-4-d-1/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_3.log) |
| question_or_constraint_misread | returned_intermediate_metric_instead_of_final_population | 1 | [task](../tasks_mini/k-5-d-3/task_15.json) / [plan](../plans_mini/k-5-d-3/task_15.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_15.log) |
| question_or_constraint_misread | violent_crime_and_founding_year_recast_as_bridge_proxies | 1 | [task](../tasks_mini/k-5-d-4/task_1.json) / [plan](../plans_mini/k-5-d-4/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_1.log) |
| schema_or_shape_inspection_loop | column_or_row_sampling_loop | 1 | [task](../tasks_mini/k-3-d-2/task_11.json) / [plan](../plans_mini/k-3-d-2/task_11.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_11.log) |
| schema_or_shape_inspection_loop | metadata_preview_and_sample_rows | 1 | [task](../tasks_mini/k-5-d-4/task_8.json) / [plan](../plans_mini/k-5-d-4/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_8.log) |
| schema_or_shape_inspection_loop | repeated_metadata_preview | 1 | [task](../tasks_mini/k-3-d-2/task_6.json) / [plan](../plans_mini/k-3-d-2/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| schema_or_shape_inspection_loop | row_count_and_column_check_instead_of_required_aggregation | 1 | [task](../tasks_mini/k-4-d-4/task_9.json) / [plan](../plans_mini/k-4-d-4/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_9.log) |
| schema_or_shape_inspection_loop | sample_row_probe | 1 | [task](../tasks_mini/k-4-d-3/task_2.json) / [plan](../plans_mini/k-4-d-3/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| schema_or_shape_inspection_loop | schema_sampling_over_evidence_extraction | 1 | [task](../tasks_mini/k-6-d-3/task_3.json) / [plan](../plans_mini/k-6-d-3/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| semantic_or_gold_label_issue | benchmark_answer_conflict | 1 | [task](../tasks_mini/k-3-d-2/task_10.json) / [plan](../plans_mini/k-3-d-2/task_10.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| semantic_or_gold_label_issue | task_gold_conflict | 1 | [task](../tasks_mini/k-4-d-5/task_1.json) / [plan](../plans_mini/k-4-d-5/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_1.log) |
| tool_or_data_blocker | malformed_tool_call | 1 | [task](../tasks_mini/k-5-d-3/task_10.json) / [plan](../plans_mini/k-5-d-3/task_10.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_10.log) |
| wrong_source_or_scope | county_scope_mismatch | 1 | [task](../tasks_mini/k-3-d-2/task_7.json) / [plan](../plans_mini/k-3-d-2/task_7.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_7.log) |
| wrong_source_or_scope | dataset_version_mismatch | 1 | [task](../tasks_mini/k-5-d-3/task_14.json) / [plan](../plans_mini/k-5-d-3/task_14.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_14.log) |
| wrong_source_or_scope | dataset_year_mismatch | 1 | [task](../tasks_mini/k-5-d-2/task_8.json) / [plan](../plans_mini/k-5-d-2/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_8.log) |
| wrong_source_or_scope | detoured_to_unrelated_population_dataset | 1 | [task](../tasks_mini/k-4-d-2/task_15.json) / [plan](../plans_mini/k-4-d-2/task_15.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_15.log) |
| wrong_source_or_scope | district_scope_omitted | 1 | [task](../tasks_mini/k-4-d-1/task_5.json) / [plan](../plans_mini/k-4-d-1/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_5.log) |
| wrong_source_or_scope | dropped_city_filter_for_public_school_count | 1 | [task](../tasks_mini/k-3-d-2/task_9.json) / [plan](../plans_mini/k-3-d-2/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_source_or_scope | irrelevant_dataset_search | 1 | [task](../tasks_mini/k-4-d-4/task_1.json) / [plan](../plans_mini/k-4-d-4/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| wrong_source_or_scope | metadata_view_instead_of_rows | 1 | [task](../tasks_mini/k-5-d-4/task_5.json) / [plan](../plans_mini/k-5-d-4/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_5.log) |
| wrong_source_or_scope | missed_required_ami_source | 1 | [task](../tasks_mini/k-6-d-2/task_5.json) / [plan](../plans_mini/k-6-d-2/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_5.log) |
| wrong_source_or_scope | missing_programyear_filter | 1 | [task](../tasks_mini/k-5-d-2/task_3.json) / [plan](../plans_mini/k-5-d-2/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_3.log) |
| wrong_source_or_scope | opened_wrong_dataset_family | 1 | [task](../tasks_mini/k-3-d-3/task_1.json) / [plan](../plans_mini/k-3-d-3/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_1.log) |
| wrong_source_or_scope | picked_houston_instead_of_fort_worth | 1 | [task](../tasks_mini/k-5-d-3/task_3.json) / [plan](../plans_mini/k-5-d-3/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| wrong_source_or_scope | pivoted_to_wrong_dataset_branch | 1 | [task](../tasks_mini/k-4-d-2/task_1.json) / [plan](../plans_mini/k-4-d-2/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| wrong_source_or_scope | scope_drift_to_unrelated_datasets | 1 | [task](../tasks_mini/k-4-d-4/task_4.json) / [plan](../plans_mini/k-4-d-4/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_4.log) |
| wrong_source_or_scope | searched and opened wrong dataset versions | 1 | [task](../tasks_mini/k-5-d-3/task_13.json) / [plan](../plans_mini/k-5-d-3/task_13.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_13.log) |
| wrong_source_or_scope | switched_to_wrong_cpi_dataset_branch | 1 | [task](../tasks_mini/k-5-d-2/task_1.json) / [plan](../plans_mini/k-5-d-2/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_1.log) |
| wrong_source_or_scope | used_arrest_dataset_for_2019_crime_hop | 1 | [task](../tasks_mini/k-4-d-1/task_1.json) / [plan](../plans_mini/k-4-d-1/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_1.log) |
| wrong_source_or_scope | used_complaint_dataset_for_final_count_step | 1 | [task](../tasks_mini/k-4-d-1/task_3.json) / [plan](../plans_mini/k-4-d-1/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_3.log) |
| wrong_source_or_scope | used_income_only_county_set | 1 | [task](../tasks_mini/k-4-d-3/task_11.json) / [plan](../plans_mini/k-4-d-3/task_11.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| wrong_source_or_scope | wrong_500_cities_dataset_variant | 1 | [task](../tasks_mini/k-5-d-4/task_6.json) / [plan](../plans_mini/k-5-d-4/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_6.log) |
| wrong_source_or_scope | wrong_dataset | 1 | [task](../tasks_mini/k-3-d-2/task_1.json) / [plan](../plans_mini/k-3-d-2/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| wrong_source_or_scope | wrong_dataset_branch | 1 | [task](../tasks_mini/k-4-d-3/task_12.json) / [plan](../plans_mini/k-4-d-3/task_12.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_12.log) |
| wrong_source_or_scope | wrong_dataset_variant | 1 | [task](../tasks_mini/k-6-d-3/task_5.json) / [plan](../plans_mini/k-6-d-3/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_5.log) |
| wrong_source_or_scope | wrong_dataset_year_branch | 1 | [task](../tasks_mini/k-6-d-3/task_4.json) / [plan](../plans_mini/k-6-d-3/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_4.log) |
| wrong_source_or_scope | wrong_dataset_year_field | 1 | [task](../tasks_mini/k-4-d-3/task_1.json) / [plan](../plans_mini/k-4-d-3/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_1.log) |
| wrong_source_or_scope | wrong_entity_branch | 1 | [task](../tasks_mini/k-5-d-3/task_1.json) / [plan](../plans_mini/k-5-d-3/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_1.log) |
| wrong_source_or_scope | wrong_file_or_dataset_path | 1 | [task](../tasks_mini/k-6-d-3/task_1.json) / [plan](../plans_mini/k-6-d-3/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_1.log) |
| wrong_source_or_scope | wrong_file_path | 1 | [task](../tasks_mini/k-4-d-2/task_8.json) / [plan](../plans_mini/k-4-d-2/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_8.log) |
| wrong_source_or_scope | wrong_file_shape_or_dataset_branch | 1 | [task](../tasks_mini/k-5-d-4/task_4.json) / [plan](../plans_mini/k-5-d-4/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_4.log) |
| wrong_source_or_scope | wrong_final_county_branch | 1 | [task](../tasks_mini/k-6-d-2/task_3.json) / [plan](../plans_mini/k-6-d-2/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_3.log) |
| wrong_source_or_scope | wrong_measure_and_value_type_filters | 1 | [task](../tasks_mini/k-6-d-2/task_4.json) / [plan](../plans_mini/k-6-d-2/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| wrong_source_or_scope | wrong_nba_branch | 1 | [task](../tasks_mini/k-7-d-4/task_1.json) / [plan](../plans_mini/k-7-d-4/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-7-d-4/task_1.log) |
| wrong_source_or_scope | wrong_public_school_dataset_family | 1 | [task](../tasks_mini/k-4-d-2/task_4.json) / [plan](../plans_mini/k-4-d-2/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| wrong_source_or_scope | wrong_source_branch | 1 | [task](../tasks_mini/k-3-d-4/task_1.json) / [plan](../plans_mini/k-3-d-4/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_1.log) |
| wrong_source_or_scope | wrong_year_and_metric_for_mental_health | 1 | [task](../tasks_mini/k-4-d-3/task_9.json) / [plan](../plans_mini/k-4-d-3/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_9.log) |
| wrong_source_or_scope | wrong_year_and_source_family | 1 | [task](../tasks_mini/k-5-d-2/task_4.json) / [plan](../plans_mini/k-5-d-2/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_4.log) |

## Co-occurring Failure Types

| Failure Type Set | Rows |
| --- | --- |
| wrong_source_or_scope | 19 |
| evidence_available_answer_error | 7 |
| tool_or_data_blocker | 6 |
| schema_or_shape_inspection_loop; tool_or_data_blocker | 5 |
| evidence_available_answer_error; wrong_source_or_scope | 4 |
| tool_or_data_blocker; wrong_source_or_scope | 4 |
| computation_or_aggregation_error; evidence_available_answer_error | 3 |
| computation_or_aggregation_error; tool_or_data_blocker | 3 |
| query_execution_error_loop; wrong_source_or_scope | 3 |
| computation_or_aggregation_error; incomplete_evidence_early_answer | 2 |
| evidence_available_answer_error; query_execution_error_loop | 2 |
| incomplete_evidence_early_answer; tool_or_data_blocker | 2 |
| incomplete_evidence_early_answer; wrong_source_or_scope | 2 |
| incomplete_evidence_not_enough_turns; wrong_source_or_scope | 2 |
| planning_decomposition_mismatch; query_execution_error_loop | 2 |
| question_or_constraint_misread; wrong_source_or_scope | 2 |
| semantic_or_gold_label_issue | 2 |
| computation_or_aggregation_error; wrong_source_or_scope | 1 |
| evidence_available_answer_error; planning_decomposition_mismatch | 1 |
| evidence_available_answer_error; question_or_constraint_misread | 1 |
| extraction_or_parsing_error | 1 |
| extraction_or_parsing_error; incomplete_evidence_early_answer | 1 |
| extraction_or_parsing_error; question_or_constraint_misread | 1 |
| extraction_or_parsing_error; tool_or_data_blocker | 1 |
| extraction_or_parsing_error; wrong_source_or_scope | 1 |
| incomplete_evidence_early_answer; low_yield_search_loop | 1 |
| incomplete_evidence_early_answer; planning_decomposition_mismatch | 1 |
| incomplete_evidence_early_answer; query_execution_error_loop | 1 |
| incomplete_evidence_early_answer; question_or_constraint_misread | 1 |
| incomplete_evidence_not_enough_turns; planning_decomposition_mismatch | 1 |
| incomplete_evidence_not_enough_turns; question_or_constraint_misread | 1 |
| incomplete_evidence_not_enough_turns; schema_or_shape_inspection_loop | 1 |
| incomplete_evidence_not_enough_turns; tool_or_data_blocker | 1 |
| other_or_unclear; tool_or_data_blocker | 1 |
| query_execution_error_loop | 1 |
| question_or_constraint_misread | 1 |

## Representative Evidence

- `tasks_mini/k-3-d-2/task_1.json` `wrong_source_or_scope`/`wrong_dataset`: Turn 6 | The agent sent the sector-search hop to apd-use-of-force instead of apd-searches-
- `tasks_mini/k-3-d-2/task_10.json` `semantic_or_gold_label_issue`/`benchmark_answer_conflict`: Turn 20 | submit_answer({"answer": "[145]", "reasoning": "Orange County Public Schools is based in Orlando, Florida. Using NCES EDGE location datasets: public schools in Orange County (CNTY=12095), 2022-2023 = 288. Pr...
- `tasks_mini/k-3-d-2/task_11.json` `tool_or_data_blocker`/`data_source_missing_or_unavailable`: Turn 8 | Tool logical error (status=error): {"error": "HeadObject failed: An error occurred (404) when calling the HeadObject operation: Not Found"}. Turn 9 | the peeked file only returned header text and a 2-row esti...
- `tasks_mini/k-3-d-2/task_11.json` `schema_or_shape_inspection_loop`/`column_or_row_sampling_loop`: Turn 11 | "Submitted SQL selects a single sample row (SELECT * FROM t LIMIT 1) to inspect columns, which does not correspond to the authored record’s computation filtering Wyoming counties by a recipient count range a...
- `tasks_mini/k-3-d-2/task_12.json` `computation_or_aggregation_error`/`inclusive_upper_bound_mismatch`: Turn 10 | Model response #10 [role=assistant block=1 tool_use] query_ideal({"dataset_id": "fy-2019-disability-pension-recipient-by-county", "file_path": "files/rows.txt", "intent": "Find Montana counties with 2019 tot...

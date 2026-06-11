# Answer Failure Aggregate Report

- Source root: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_answer_failures`
- Event rows: 141
- Trusted event rows: 132
- Events excluded by validation/model-validation: 9

## Counts by Failure Type

| Failure Type | Events |
| --- | --- |
| tool_or_data_blocker | 27 |
| evidence_available_answer_error | 24 |
| wrong_source_or_scope | 21 |
| query_execution_error_loop | 12 |
| question_or_constraint_misread | 10 |
| incomplete_evidence_early_answer | 9 |
| computation_or_aggregation_error | 8 |
| extraction_or_parsing_error | 8 |
| incomplete_evidence_not_enough_turns | 5 |
| planning_decomposition_mismatch | 3 |
| other_or_unclear | 2 |
| schema_or_shape_inspection_loop | 2 |
| semantic_or_gold_label_issue | 1 |

## Counts by Failure Type and Subtype

| Failure Type | Subtype | Events | Representative |
| --- | --- | --- | --- |
| tool_or_data_blocker | ideal_repair_failure | 11 | [task](../tasks_mini/k-3-d-2/task_6.json) / [plan](../plans_mini/k-3-d-2/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| tool_or_data_blocker | unsupported_or_oversized_data_access | 5 | [task](../tasks_mini/k-3-d-4/task_4.json) / [plan](../plans_mini/k-3-d-4/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| query_execution_error_loop | ideal_repair_failure | 4 | [task](../tasks_mini/k-4-d-4/task_2.json) / [plan](../plans_mini/k-4-d-4/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_2.log) |
| evidence_available_answer_error | placeholder_submission | 3 | [task](../tasks_mini/k-5-d-4/task_4.json) / [plan](../plans_mini/k-5-d-4/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_4.log) |
| incomplete_evidence_not_enough_turns | tool_budget_exhausted | 3 | [task](../tasks_mini/k-3-d-4/task_2.json) / [plan](../plans_mini/k-3-d-4/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_2.log) |
| tool_or_data_blocker | tool_budget_exhausted | 3 | [task](../tasks_mini/k-4-d-3/task_6.json) / [plan](../plans_mini/k-4-d-3/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| tool_or_data_blocker | tool_status_or_transport_error | 3 | [task](../tasks_mini/k-4-d-2/task_8.json) / [plan](../plans_mini/k-4-d-2/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_8.log) |
| incomplete_evidence_not_enough_turns | turn_or_time_budget_exhausted | 2 | [task](../tasks_mini/k-3-d-4/task_1.json) / [plan](../plans_mini/k-3-d-4/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_1.log) |
| tool_or_data_blocker | data_source_missing_or_unavailable | 2 | [task](../tasks_mini/k-3-d-2/task_5.json) / [plan](../plans_mini/k-3-d-2/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| wrong_source_or_scope | wrong_county_branch | 2 | [task](../tasks_mini/k-6-d-2/task_3.json) / [plan](../plans_mini/k-6-d-2/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_3.log) |
| computation_or_aggregation_error | bad_cross_year_intersection | 1 | [task](../tasks_mini/k-6-d-3/task_3.json) / [plan](../plans_mini/k-6-d-3/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| computation_or_aggregation_error | century_denominator_and_rounding_error | 1 | [task](../tasks_mini/k-3-d-2/task_1.json) / [plan](../plans_mini/k-3-d-2/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| computation_or_aggregation_error | incorrect_average_ranking | 1 | [task](../tasks_mini/k-3-d-3/task_6.json) / [plan](../plans_mini/k-3-d-3/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_6.log) |
| computation_or_aggregation_error | unnecessary_applied_force_filter | 1 | [task](../tasks_mini/k-3-d-2/task_1.json) / [plan](../plans_mini/k-3-d-2/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| computation_or_aggregation_error | wrong_average_ranking | 1 | [task](../tasks_mini/k-5-d-3/task_7.json) / [plan](../plans_mini/k-5-d-3/task_7.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_7.log) |
| computation_or_aggregation_error | wrong_average_rounding | 1 | [task](../tasks_mini/k-5-d-2/task_7.json) / [plan](../plans_mini/k-5-d-2/task_7.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_7.log) |
| computation_or_aggregation_error | wrong_intersection_set | 1 | [task](../tasks_mini/k-5-d-3/task_13.json) / [plan](../plans_mini/k-5-d-3/task_13.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_13.log) |
| computation_or_aggregation_error | wrong_numerator_used_in_ratio | 1 | [task](../tasks_mini/k-4-d-2/task_5.json) / [plan](../plans_mini/k-4-d-2/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_5.log) |
| evidence_available_answer_error | default_placeholder_submission | 1 | [task](../tasks_mini/k-3-d-2/task_6.json) / [plan](../plans_mini/k-3-d-2/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| evidence_available_answer_error | final_sum_based_on_wrong_postsecondary_count | 1 | [task](../tasks_mini/k-4-d-4/task_10.json) / [plan](../plans_mini/k-4-d-4/task_10.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_10.log) |
| evidence_available_answer_error | hallucinated_founding_year | 1 | [task](../tasks_mini/k-5-d-4/task_3.json) / [plan](../plans_mini/k-5-d-4/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_3.log) |
| evidence_available_answer_error | partial_final_answer | 1 | [task](../tasks_mini/k-5-d-2/task_8.json) / [plan](../plans_mini/k-5-d-2/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_8.log) |
| evidence_available_answer_error | placeholder_fallback | 1 | [task](../tasks_mini/k-4-d-5/task_4.json) / [plan](../plans_mini/k-4-d-5/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_4.log) |
| evidence_available_answer_error | submission_mismatch | 1 | [task](../tasks_mini/k-4-d-5/task_5.json) / [plan](../plans_mini/k-4-d-5/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| evidence_available_answer_error | submitted_wrong_numeric_value | 1 | [task](../tasks_mini/k-3-d-2/task_2.json) / [plan](../plans_mini/k-3-d-2/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_2.log) |
| evidence_available_answer_error | wrong_branch_and_income_lookup | 1 | [task](../tasks_mini/k-6-d-3/task_3.json) / [plan](../plans_mini/k-6-d-3/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| evidence_available_answer_error | wrong_federal_agency_selected | 1 | [task](../tasks_mini/k-3-d-3/task_6.json) / [plan](../plans_mini/k-3-d-3/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_6.log) |
| evidence_available_answer_error | wrong_final_answer | 1 | [task](../tasks_mini/k-4-d-4/task_8.json) / [plan](../plans_mini/k-4-d-4/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_8.log) |
| evidence_available_answer_error | wrong_final_answer_from_wrong_intermediate_count | 1 | [task](../tasks_mini/k-3-d-2/task_8.json) / [plan](../plans_mini/k-3-d-2/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| evidence_available_answer_error | wrong_final_chain | 1 | [task](../tasks_mini/k-5-d-3/task_7.json) / [plan](../plans_mini/k-5-d-3/task_7.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_7.log) |
| evidence_available_answer_error | wrong_final_choice | 1 | [task](../tasks_mini/k-4-d-3/task_11.json) / [plan](../plans_mini/k-4-d-3/task_11.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| evidence_available_answer_error | wrong_final_entity_selected | 1 | [task](../tasks_mini/k-4-d-4/task_6.json) / [plan](../plans_mini/k-4-d-4/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| evidence_available_answer_error | wrong_final_selection | 1 | [task](../tasks_mini/k-5-d-3/task_13.json) / [plan](../plans_mini/k-5-d-3/task_13.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_13.log) |
| evidence_available_answer_error | wrong_final_submission | 1 | [task](../tasks_mini/k-5-d-2/task_7.json) / [plan](../plans_mini/k-5-d-2/task_7.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_7.log) |
| evidence_available_answer_error | wrong_final_synthesis | 1 | [task](../tasks_mini/k-3-d-2/task_10.json) / [plan](../plans_mini/k-3-d-2/task_10.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| evidence_available_answer_error | wrong_final_year | 1 | [task](../tasks_mini/k-3-d-4/task_7.json) / [plan](../plans_mini/k-3-d-4/task_7.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_7.log) |
| evidence_available_answer_error | wrong_value_selected_from_correct_evidence | 1 | [task](../tasks_mini/k-4-d-2/task_1.json) / [plan](../plans_mini/k-4-d-2/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| evidence_available_answer_error | wrong_value_submitted | 1 | [task](../tasks_mini/k-3-d-3/task_4.json) / [plan](../plans_mini/k-3-d-3/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_4.log) |
| evidence_available_answer_error | year_confusion_at_submission | 1 | [task](../tasks_mini/k-5-d-3/task_3.json) / [plan](../plans_mini/k-5-d-3/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| extraction_or_parsing_error | birthplace_taken_as_base_location | 1 | [task](../tasks_mini/k-5-d-2/task_4.json) / [plan](../plans_mini/k-5-d-2/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_4.log) |
| extraction_or_parsing_error | demonym_instead_of_province | 1 | [task](../tasks_mini/k-3-d-5/task_1.json) / [plan](../plans_mini/k-3-d-5/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-5/task_1.log) |
| extraction_or_parsing_error | digit_miscopy | 1 | [task](../tasks_mini/k-4-d-3/task_11.json) / [plan](../plans_mini/k-4-d-3/task_11.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| extraction_or_parsing_error | founding_year_taken_as_birth_year | 1 | [task](../tasks_mini/k-5-d-2/task_6.json) / [plan](../plans_mini/k-5-d-2/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_6.log) |
| extraction_or_parsing_error | school_count_filter_miss | 1 | [task](../tasks_mini/k-4-d-2/task_4.json) / [plan](../plans_mini/k-4-d-2/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| extraction_or_parsing_error | wrong_field_or_tag | 1 | [task](../tasks_mini/k-3-d-4/task_4.json) / [plan](../plans_mini/k-3-d-4/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| extraction_or_parsing_error | wrong_founding_year | 1 | [task](../tasks_mini/k-4-d-2/task_10.json) / [plan](../plans_mini/k-4-d-2/task_10.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_10.log) |
| extraction_or_parsing_error | wrong_year_selected_from_truncated_excerpt | 1 | [task](../tasks_mini/k-3-d-4/task_7.json) / [plan](../plans_mini/k-3-d-4/task_7.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_7.log) |
| incomplete_evidence_early_answer | blocked_partial_chain | 1 | [task](../tasks_mini/k-3-d-4/task_3.json) / [plan](../plans_mini/k-3-d-4/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_3.log) |
| incomplete_evidence_early_answer | gave_up_after_empty_results | 1 | [task](../tasks_mini/k-4-d-4/task_4.json) / [plan](../plans_mini/k-4-d-4/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_4.log) |
| incomplete_evidence_early_answer | missing_birth_year_lookup | 1 | [task](../tasks_mini/k-5-d-2/task_6.json) / [plan](../plans_mini/k-5-d-2/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_6.log) |
| incomplete_evidence_early_answer | placeholder_submission | 1 | [task](../tasks_mini/k-3-d-2/task_7.json) / [plan](../plans_mini/k-3-d-2/task_7.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_7.log) |
| incomplete_evidence_early_answer | premature_submission_after_partial_hop | 1 | [task](../tasks_mini/k-3-d-4/task_5.json) / [plan](../plans_mini/k-3-d-4/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_5.log) |
| incomplete_evidence_early_answer | premature_submission_missing_final_hop | 1 | [task](../tasks_mini/k-4-d-4/task_1.json) / [plan](../plans_mini/k-4-d-4/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| incomplete_evidence_early_answer | premature_submit_after_partial_chain | 1 | [task](../tasks_mini/k-5-d-3/task_12.json) / [plan](../plans_mini/k-5-d-3/task_12.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_12.log) |
| incomplete_evidence_early_answer | submitted before county lookup | 1 | [task](../tasks_mini/k-4-d-3/task_3.json) / [plan](../plans_mini/k-4-d-3/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_3.log) |
| incomplete_evidence_early_answer | submitted_unknown_after_blocker | 1 | [task](../tasks_mini/k-5-d-4/task_5.json) / [plan](../plans_mini/k-5-d-4/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_5.log) |
| other_or_unclear | null_submission_after_failed_extraction | 1 | [task](../tasks_mini/k-3-d-2/task_9.json) / [plan](../plans_mini/k-3-d-2/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| other_or_unclear | placeholder_submission_after_blocker | 1 | [task](../tasks_mini/k-6-d-3/task_5.json) / [plan](../plans_mini/k-6-d-3/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_5.log) |
| planning_decomposition_mismatch | hop_divergence | 1 | [task](../tasks_mini/k-3-d-4/task_2.json) / [plan](../plans_mini/k-3-d-4/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_2.log) |
| planning_decomposition_mismatch | skipped required county hop | 1 | [task](../tasks_mini/k-4-d-3/task_3.json) / [plan](../plans_mini/k-4-d-3/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_3.log) |
| planning_decomposition_mismatch | skipped_required_ripa_mapping_hop | 1 | [task](../tasks_mini/k-4-d-2/task_5.json) / [plan](../plans_mini/k-4-d-2/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_5.log) |
| query_execution_error_loop | ideal_repair_jsondecodeerror | 1 | [task](../tasks_mini/k-5-d-4/task_8.json) / [plan](../plans_mini/k-5-d-4/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_8.log) |
| query_execution_error_loop | jsondecode_repair_error_loop | 1 | [task](../tasks_mini/k-4-d-4/task_9.json) / [plan](../plans_mini/k-4-d-4/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_9.log) |
| query_execution_error_loop | malformed_query_repair | 1 | [task](../tasks_mini/k-4-d-4/task_5.json) / [plan](../plans_mini/k-4-d-4/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_5.log) |
| query_execution_error_loop | oom_and_repair_timeout | 1 | [task](../tasks_mini/k-3-d-4/task_1.json) / [plan](../plans_mini/k-3-d-4/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_1.log) |
| query_execution_error_loop | semantic_mismatch_and_repair_failure | 1 | [task](../tasks_mini/k-3-d-2/task_9.json) / [plan](../plans_mini/k-3-d-2/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| query_execution_error_loop | sql_repair_jsondecodeerror | 1 | [task](../tasks_mini/k-3-d-4/task_5.json) / [plan](../plans_mini/k-3-d-4/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_5.log) |
| query_execution_error_loop | stalled_execute_repair_loop | 1 | [task](../tasks_mini/k-5-d-4/task_2.json) / [plan](../plans_mini/k-5-d-4/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) |
| query_execution_error_loop | xml_json_tool_mismatch | 1 | [task](../tasks_mini/k-3-d-2/task_5.json) / [plan](../plans_mini/k-3-d-2/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| question_or_constraint_misread | based_in_constraint_ignored | 1 | [task](../tasks_mini/k-5-d-2/task_4.json) / [plan](../plans_mini/k-5-d-2/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_4.log) |
| question_or_constraint_misread | coreference_misread | 1 | [task](../tasks_mini/k-4-d-4/task_13.json) / [plan](../plans_mini/k-4-d-4/task_13.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_13.log) |
| question_or_constraint_misread | multi_hop_constraint_misread | 1 | [task](../tasks_mini/k-4-d-4/task_9.json) / [plan](../plans_mini/k-4-d-4/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_9.log) |
| question_or_constraint_misread | original_23_counties_misread | 1 | [task](../tasks_mini/k-4-d-4/task_6.json) / [plan](../plans_mini/k-4-d-4/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| question_or_constraint_misread | percentage_change_instead_of_percentage_of_baseline | 1 | [task](../tasks_mini/k-3-d-2/task_2.json) / [plan](../plans_mini/k-3-d-2/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_2.log) |
| question_or_constraint_misread | returned_person_instead_of_university | 1 | [task](../tasks_mini/k-5-d-3/task_8.json) / [plan](../plans_mini/k-5-d-3/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_8.log) |
| question_or_constraint_misread | reversed_incorporation_comparison | 1 | [task](../tasks_mini/k-6-d-2/task_3.json) / [plan](../plans_mini/k-6-d-2/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_3.log) |
| question_or_constraint_misread | scope_and_filter_misread | 1 | [task](../tasks_mini/k-5-d-4/task_8.json) / [plan](../plans_mini/k-5-d-4/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_8.log) |
| question_or_constraint_misread | state_fips_or_geography_confusion | 1 | [task](../tasks_mini/k-3-d-4/task_6.json) / [plan](../plans_mini/k-3-d-4/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_6.log) |
| question_or_constraint_misread | wrong_city_and_year_constraints | 1 | [task](../tasks_mini/k-4-d-4/task_4.json) / [plan](../plans_mini/k-4-d-4/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_4.log) |
| schema_or_shape_inspection_loop | metadata_only_loop | 1 | [task](../tasks_mini/k-5-d-3/task_10.json) / [plan](../plans_mini/k-5-d-3/task_10.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_10.log) |
| schema_or_shape_inspection_loop | repeated_schema_probe | 1 | [task](../tasks_mini/k-4-d-4/task_5.json) / [plan](../plans_mini/k-4-d-4/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_5.log) |
| semantic_or_gold_label_issue | gold_answer_conflict_with_source | 1 | [task](../tasks_mini/k-4-d-5/task_1.json) / [plan](../plans_mini/k-4-d-5/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_1.log) |
| tool_or_data_blocker | malformed_tool_call | 1 | [task](../tasks_mini/k-4-d-2/task_8.json) / [plan](../plans_mini/k-4-d-2/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_8.log) |
| tool_or_data_blocker | placeholder_submission_after_blockers | 1 | [task](../tasks_mini/k-5-d-4/task_8.json) / [plan](../plans_mini/k-5-d-4/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_8.log) |
| tool_or_data_blocker | xml_query_unsupported | 1 | [task](../tasks_mini/k-3-d-2/task_9.json) / [plan](../plans_mini/k-3-d-2/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_source_or_scope | city_constraint_omitted | 1 | [task](../tasks_mini/k-3-d-2/task_8.json) / [plan](../plans_mini/k-3-d-2/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| wrong_source_or_scope | cook_county_only_scope_instead_of_authorized_chicago_in_cook_county | 1 | [task](../tasks_mini/k-3-d-2/task_7.json) / [plan](../plans_mini/k-3-d-2/task_7.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_7.log) |
| wrong_source_or_scope | county_only_private_school_count | 1 | [task](../tasks_mini/k-3-d-2/task_10.json) / [plan](../plans_mini/k-3-d-2/task_10.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| wrong_source_or_scope | description_branch_instead_of_code_branch | 1 | [task](../tasks_mini/k-5-d-3/task_8.json) / [plan](../plans_mini/k-5-d-3/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_8.log) |
| wrong_source_or_scope | extra_precinct_filter | 1 | [task](../tasks_mini/k-4-d-1/task_3.json) / [plan](../plans_mini/k-4-d-1/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_3.log) |
| wrong_source_or_scope | extra_ward_filter_in_final_count | 1 | [task](../tasks_mini/k-5-d-1/task_3.json) / [plan](../plans_mini/k-5-d-1/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-1/task_3.log) |
| wrong_source_or_scope | final_hop_source_missed | 1 | [task](../tasks_mini/k-4-d-4/task_1.json) / [plan](../plans_mini/k-4-d-4/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| wrong_source_or_scope | final_hop_wrong_source | 1 | [task](../tasks_mini/k-4-d-3/task_6.json) / [plan](../plans_mini/k-4-d-3/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| wrong_source_or_scope | missing_school_year_constraint | 1 | [task](../tasks_mini/k-3-d-2/task_6.json) / [plan](../plans_mini/k-3-d-2/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| wrong_source_or_scope | neighborhood_filter_misread | 1 | [task](../tasks_mini/k-4-d-3/task_2.json) / [plan](../plans_mini/k-4-d-3/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| wrong_source_or_scope | salary_checked_in_wrong_dataset | 1 | [task](../tasks_mini/k-4-d-4/task_4.json) / [plan](../plans_mini/k-4-d-4/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_4.log) |
| wrong_source_or_scope | searched_school_dataset_for_neighborhood_field | 1 | [task](../tasks_mini/k-3-d-5/task_1.json) / [plan](../plans_mini/k-3-d-5/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-5/task_1.log) |
| wrong_source_or_scope | skipped_moses_brown_source | 1 | [task](../tasks_mini/k-4-d-4/task_13.json) / [plan](../plans_mini/k-4-d-4/task_13.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_13.log) |
| wrong_source_or_scope | subset_scope_drop | 1 | [task](../tasks_mini/k-3-d-4/task_2.json) / [plan](../plans_mini/k-3-d-4/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_2.log) |
| wrong_source_or_scope | used_apd_searches_year_instead_of_council_meeting_year | 1 | [task](../tasks_mini/k-4-d-2/task_4.json) / [plan](../plans_mini/k-4-d-2/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| wrong_source_or_scope | wrong_dataset_year_for_postsecondary_count | 1 | [task](../tasks_mini/k-4-d-4/task_10.json) / [plan](../plans_mini/k-4-d-4/task_10.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_10.log) |
| wrong_source_or_scope | wrong_field_and_filter | 1 | [task](../tasks_mini/k-4-d-5/task_4.json) / [plan](../plans_mini/k-4-d-5/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_4.log) |
| wrong_source_or_scope | wrong_file_variant | 1 | [task](../tasks_mini/k-3-d-2/task_5.json) / [plan](../plans_mini/k-3-d-2/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| wrong_source_or_scope | wrong_school_branch | 1 | [task](../tasks_mini/k-4-d-2/task_10.json) / [plan](../plans_mini/k-4-d-2/task_10.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_10.log) |

## Co-occurring Failure Types

| Failure Type Set | Rows |
| --- | --- |
| computation_or_aggregation_error; evidence_available_answer_error | 5 |
| evidence_available_answer_error | 5 |
| tool_or_data_blocker; wrong_source_or_scope | 4 |
| evidence_available_answer_error; tool_or_data_blocker | 3 |
| evidence_available_answer_error; tool_or_data_blocker; wrong_source_or_scope | 3 |
| evidence_available_answer_error; wrong_source_or_scope | 3 |
| incomplete_evidence_early_answer; query_execution_error_loop | 3 |
| evidence_available_answer_error; extraction_or_parsing_error | 2 |
| evidence_available_answer_error; question_or_constraint_misread | 2 |
| extraction_or_parsing_error; wrong_source_or_scope | 2 |
| incomplete_evidence_early_answer; tool_or_data_blocker; wrong_source_or_scope | 2 |
| query_execution_error_loop; question_or_constraint_misread; tool_or_data_blocker | 2 |
| query_execution_error_loop; tool_or_data_blocker | 2 |
| question_or_constraint_misread; wrong_source_or_scope | 2 |
| computation_or_aggregation_error | 1 |
| computation_or_aggregation_error; planning_decomposition_mismatch | 1 |
| evidence_available_answer_error; query_execution_error_loop | 1 |
| extraction_or_parsing_error; incomplete_evidence_early_answer | 1 |
| extraction_or_parsing_error; question_or_constraint_misread | 1 |
| extraction_or_parsing_error; tool_or_data_blocker | 1 |
| extraction_or_parsing_error; tool_or_data_blocker; wrong_source_or_scope | 1 |
| incomplete_evidence_early_answer; planning_decomposition_mismatch | 1 |
| incomplete_evidence_early_answer; question_or_constraint_misread; wrong_source_or_scope | 1 |
| incomplete_evidence_early_answer; tool_or_data_blocker | 1 |
| incomplete_evidence_not_enough_turns; planning_decomposition_mismatch; wrong_source_or_scope | 1 |
| incomplete_evidence_not_enough_turns; query_execution_error_loop | 1 |
| incomplete_evidence_not_enough_turns; query_execution_error_loop; schema_or_shape_inspection_loop | 1 |
| incomplete_evidence_not_enough_turns; question_or_constraint_misread; wrong_source_or_scope | 1 |
| incomplete_evidence_not_enough_turns; schema_or_shape_inspection_loop; tool_or_data_blocker | 1 |
| other_or_unclear; query_execution_error_loop; tool_or_data_blocker | 1 |
| other_or_unclear; tool_or_data_blocker | 1 |
| query_execution_error_loop; tool_or_data_blocker; wrong_source_or_scope | 1 |
| question_or_constraint_misread; tool_or_data_blocker | 1 |
| semantic_or_gold_label_issue | 1 |
| tool_or_data_blocker | 1 |

## Representative Evidence

- `tasks_mini/k-3-d-2/task_1.json` `computation_or_aggregation_error`/`unnecessary_applied_force_filter`: Turn 11 | `Submitted code counts 2023 council district 1 records with Used Taser(s)>0 AND (any other force field >0). The authored computation counts only Used Taser(s)>0 ... Therefore the intent is not followed exact...
- `tasks_mini/k-3-d-2/task_1.json` `computation_or_aggregation_error`/`century_denominator_and_rounding_error`: Turn 16 | `Austin incorporated on 12/27/1839 => centuries=(2023-1839+1)=185... Average per century=59/185≈0.319→rounded to nearest integer=160`
- `tasks_mini/k-3-d-2/task_10.json` `wrong_source_or_scope`/`county_only_private_school_count`: Turn 6 | query_ideal on the private-school dataset was framed as "Count private schools in Orange County for school year 2021-2022." The semantic judge then rejected equivalence because "The authored record counts pri...
- `tasks_mini/k-3-d-2/task_10.json` `evidence_available_answer_error`/`wrong_final_synthesis`: Turn 7 | submit_answer({"answer": "[-202]", "reasoning": "Orange County Public Schools is based in downtown Orlando. Public schools in Orange County (FL) for 2022-2023: 219. Private schools in Orange County for 2021-2...
- `tasks_mini/k-3-d-2/task_2.json` `question_or_constraint_misread`/`percentage_change_instead_of_percentage_of_baseline`: Turn 6 | query_ideal intent: "Compute rounded percentage change from 2020 to 2021 for Ward 4 THEFT F/AUTO incidents." ... tool result: {"output": "-7\n", "success": true}

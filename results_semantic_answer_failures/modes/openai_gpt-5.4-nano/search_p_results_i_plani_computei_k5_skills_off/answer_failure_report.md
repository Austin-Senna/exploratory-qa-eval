# Answer Failure Report

- Source root: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_answer_failures`
- Event rows: 111
- Trusted event rows: 106
- Non-correct eval rows: 65
- Events excluded by validation/model-validation: 5

## Counts by Failure Type

| Failure Type | Events |
| --- | --- |
| wrong_scope_or_filter | 28 |
| tool_or_data_blocker | 20 |
| evidence_available_answer_error | 11 |
| planning_decomposition_mismatch | 11 |
| query_execution_error_loop | 8 |
| extraction_or_parsing_error | 6 |
| computation_or_aggregation_error | 5 |
| wrong_source_or_dataset | 5 |
| incomplete_evidence_budget_exhausted | 3 |
| incomplete_evidence_early_answer | 3 |
| question_or_constraint_misread | 2 |
| low_yield_search_loop | 1 |
| other_or_unclear | 1 |
| schema_or_shape_inspection_loop | 1 |
| semantic_or_gold_label_issue | 1 |

## Counts by Failure Type and Subtype

| Failure Type | Subtype | Events | Representative |
| --- | --- | --- | --- |
| tool_or_data_blocker | unsupported_or_oversized_data_access | 6 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| tool_or_data_blocker | malformed_tool_call | 5 | [task](../../../../tasks_mini/k-3-d-2/task_11.json) / [plan](../../../../plans_mini/k-3-d-2/task_11.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_11.log) |
| tool_or_data_blocker | tool_status_or_transport_error | 3 | [task](../../../../tasks_mini/k-3-d-3/task_6.json) / [plan](../../../../plans_mini/k-3-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_6.log) |
| query_execution_error_loop | repeated SQL repair JSONDecodeError | 2 | [task](../../../../tasks_mini/k-4-d-4/task_9.json) / [plan](../../../../plans_mini/k-4-d-4/task_9.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_9.log) |
| tool_or_data_blocker | data_source_missing_or_unavailable | 2 | [task](../../../../tasks_mini/k-3-d-2/task_11.json) / [plan](../../../../plans_mini/k-3-d-2/task_11.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_11.log) |
| tool_or_data_blocker | ideal_repair_failure | 2 | [task](../../../../tasks_mini/k-3-d-4/task_3.json) / [plan](../../../../plans_mini/k-3-d-4/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_3.log) |
| tool_or_data_blocker | tool_budget_exhausted | 2 | [task](../../../../tasks_mini/k-3-d-4/task_2.json) / [plan](../../../../plans_mini/k-3-d-4/task_2.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_2.log) |
| computation_or_aggregation_error | incorrect per-century arithmetic | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| computation_or_aggregation_error | incorrect_average_and_rounding | 1 | [task](../../../../tasks_mini/k-5-d-2/task_7.json) / [plan](../../../../plans_mini/k-5-d-2/task_7.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_7.log) |
| computation_or_aggregation_error | percent_change_vs_share_of_2020 | 1 | [task](../../../../tasks_mini/k-3-d-2/task_2.json) / [plan](../../../../plans_mini/k-3-d-2/task_2.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_2.log) |
| computation_or_aggregation_error | single_year_result_instead_of_four_year_average | 1 | [task](../../../../tasks_mini/k-5-d-4/task_2.json) / [plan](../../../../plans_mini/k-5-d-4/task_2.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) |
| computation_or_aggregation_error | used_wrong_area_count_branch_for_final_ratio | 1 | [task](../../../../tasks_mini/k-4-d-2/task_5.json) / [plan](../../../../plans_mini/k-4-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_5.log) |
| evidence_available_answer_error | incorrectly placed Wallops Flight Facility in Westmoreland County | 1 | [task](../../../../tasks_mini/k-4-d-3/task_3.json) / [plan](../../../../plans_mini/k-4-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_3.log) |
| evidence_available_answer_error | inverted comparison at submission | 1 | [task](../../../../tasks_mini/k-4-d-3/task_11.json) / [plan](../../../../plans_mini/k-4-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| evidence_available_answer_error | placeholder_final_answer | 1 | [task](../../../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../../../plans_mini/k-6-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| evidence_available_answer_error | stopped_at_employer_name | 1 | [task](../../../../tasks_mini/k-5-d-2/task_8.json) / [plan](../../../../plans_mini/k-5-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_8.log) |
| evidence_available_answer_error | submitted 1907 instead of 1858 | 1 | [task](../../../../tasks_mini/k-5-d-4/task_3.json) / [plan](../../../../plans_mini/k-5-d-4/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_3.log) |
| evidence_available_answer_error | submitted 1959 despite reasoning for 1916 | 1 | [task](../../../../tasks_mini/k-5-d-3/task_3.json) / [plan](../../../../plans_mini/k-5-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| evidence_available_answer_error | submitted school name instead of bridge | 1 | [task](../../../../tasks_mini/k-3-d-4/task_5.json) / [plan](../../../../plans_mini/k-3-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_5.log) |
| evidence_available_answer_error | submitted_8_instead_of_13 | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| evidence_available_answer_error | submitted_count_instead_of_percentage | 1 | [task](../../../../tasks_mini/k-4-d-2/task_1.json) / [plan](../../../../plans_mini/k-4-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| evidence_available_answer_error | submitted_wrong_final_answer | 1 | [task](../../../../tasks_mini/k-3-d-3/task_4.json) / [plan](../../../../plans_mini/k-3-d-3/task_4.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_4.log) |
| evidence_available_answer_error | surface_form_mismatch | 1 | [task](../../../../tasks_mini/k-3-d-5/task_1.json) / [plan](../../../../plans_mini/k-3-d-5/task_1.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-5/task_1.log) |
| extraction_or_parsing_error | confused founding year with birth year | 1 | [task](../../../../tasks_mini/k-5-d-2/task_6.json) / [plan](../../../../plans_mini/k-5-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_6.log) |
| extraction_or_parsing_error | public-school KML filter/path returned zero rows | 1 | [task](../../../../tasks_mini/k-3-d-4/task_4.json) / [plan](../../../../plans_mini/k-3-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| extraction_or_parsing_error | selected birthplace instead of based-in location | 1 | [task](../../../../tasks_mini/k-5-d-2/task_4.json) / [plan](../../../../plans_mini/k-5-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_4.log) |
| extraction_or_parsing_error | wrong person-name lookup | 1 | [task](../../../../tasks_mini/k-4-d-3/task_6.json) / [plan](../../../../plans_mini/k-4-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| extraction_or_parsing_error | wrong_field_model | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| extraction_or_parsing_error | xml filter returned zero rows | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| incomplete_evidence_budget_exhausted | hard_timeout | 1 | [task](../../../../tasks_mini/k-3-d-4/task_1.json) / [plan](../../../../plans_mini/k-3-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_1.log) |
| incomplete_evidence_budget_exhausted | time_budget_exhausted | 1 | [task](../../../../tasks_mini/k-4-d-4/task_5.json) / [plan](../../../../plans_mini/k-4-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_5.log) |
| incomplete_evidence_budget_exhausted | tool_budget_exhausted | 1 | [task](../../../../tasks_mini/k-5-d-3/task_10.json) / [plan](../../../../plans_mini/k-5-d-3/task_10.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_10.log) |
| incomplete_evidence_early_answer | missing firearm-count lookup | 1 | [task](../../../../tasks_mini/k-7-d-4/task_1.json) / [plan](../../../../plans_mini/k-7-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-7-d-4/task_1.log) |
| incomplete_evidence_early_answer | submitted_before_county_and_building_hops | 1 | [task](../../../../tasks_mini/k-5-d-3/task_12.json) / [plan](../../../../plans_mini/k-5-d-3/task_12.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_12.log) |
| incomplete_evidence_early_answer | submitted_intermediate_lookup | 1 | [task](../../../../tasks_mini/k-4-d-4/task_11.json) / [plan](../../../../plans_mini/k-4-d-4/task_11.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_11.log) |
| low_yield_search_loop | empty-result repeat on binge-drinking slice | 1 | [task](../../../../tasks_mini/k-4-d-4/task_4.json) / [plan](../../../../plans_mini/k-4-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_4.log) |
| other_or_unclear | incorrect NYC founding year | 1 | [task](../../../../tasks_mini/k-4-d-2/task_10.json) / [plan](../../../../plans_mini/k-4-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_10.log) |
| planning_decomposition_mismatch | added extra applied_force constraint | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| planning_decomposition_mismatch | mismatched fields/years in CACFP hop | 1 | [task](../../../../tasks_mini/k-5-d-4/task_4.json) / [plan](../../../../plans_mini/k-5-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_4.log) |
| planning_decomposition_mismatch | non-equivalent county-count queries and placeholder intersection query | 1 | [task](../../../../tasks_mini/k-5-d-4/task_8.json) / [plan](../../../../plans_mini/k-5-d-4/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_8.log) |
| planning_decomposition_mismatch | single-year county count instead of planned multi-year intersection | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| planning_decomposition_mismatch | stayed_on_first_hop | 1 | [task](../../../../tasks_mini/k-3-d-4/task_1.json) / [plan](../../../../plans_mini/k-3-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_1.log) |
| planning_decomposition_mismatch | substituted_wrong_interpreter_chain | 1 | [task](../../../../tasks_mini/k-4-d-4/task_8.json) / [plan](../../../../plans_mini/k-4-d-4/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_8.log) |
| planning_decomposition_mismatch | switched_from_central_chain_to_rampart_lookup | 1 | [task](../../../../tasks_mini/k-4-d-2/task_5.json) / [plan](../../../../plans_mini/k-4-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_5.log) |
| planning_decomposition_mismatch | used department-description and single-year queries instead of the authored department-number 2019-2021 intersection path | 1 | [task](../../../../tasks_mini/k-5-d-3/task_8.json) / [plan](../../../../plans_mini/k-5-d-3/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_8.log) |
| planning_decomposition_mismatch | wrong year anchor | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| planning_decomposition_mismatch | wrong_first_hop_schema_and_missing_fy2007_ranking | 1 | [task](../../../../tasks_mini/k-5-d-4/task_2.json) / [plan](../../../../plans_mini/k-5-d-4/task_2.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) |
| planning_decomposition_mismatch | wrong_terminus_branch | 1 | [task](../../../../tasks_mini/k-6-d-2/task_3.json) / [plan](../../../../plans_mini/k-6-d-2/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_3.log) |
| query_execution_error_loop | json_repair_parse_failure | 1 | [task](../../../../tasks_mini/k-6-d-3/task_5.json) / [plan](../../../../plans_mini/k-6-d-3/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_5.log) |
| query_execution_error_loop | jsondecode_error_in_sql_repair | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| query_execution_error_loop | non_equivalent_sql_and_jsondecodeerror | 1 | [task](../../../../tasks_mini/k-5-d-3/task_12.json) / [plan](../../../../plans_mini/k-5-d-3/task_12.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_12.log) |
| query_execution_error_loop | repeated JSONDecodeError in query_ideal repair | 1 | [task](../../../../tasks_mini/k-4-d-4/task_2.json) / [plan](../../../../plans_mini/k-4-d-4/task_2.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_2.log) |
| query_execution_error_loop | sql repair JSONDecodeError | 1 | [task](../../../../tasks_mini/k-7-d-4/task_1.json) / [plan](../../../../plans_mini/k-7-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-7-d-4/task_1.log) |
| query_execution_error_loop | sql_repair_jsondecodeerror | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| question_or_constraint_misread | comparison_reversed | 1 | [task](../../../../tasks_mini/k-6-d-2/task_3.json) / [plan](../../../../plans_mini/k-6-d-2/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_3.log) |
| question_or_constraint_misread | returned a person name instead of the required university answer | 1 | [task](../../../../tasks_mini/k-5-d-3/task_8.json) / [plan](../../../../plans_mini/k-5-d-3/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_8.log) |
| schema_or_shape_inspection_loop | schema probe returned no usable rows | 1 | [task](../../../../tasks_mini/k-4-d-4/task_4.json) / [plan](../../../../plans_mini/k-4-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_4.log) |
| semantic_or_gold_label_issue | expected_answer_conflict | 1 | [task](../../../../tasks_mini/k-4-d-5/task_1.json) / [plan](../../../../plans_mini/k-4-d-5/task_1.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_1.log) |
| wrong_scope_or_filter | NTA_NAME neighborhood matching instead of exact LOCATION_CODE and NTA-code filtering | 1 | [task](../../../../tasks_mini/k-4-d-3/task_2.json) / [plan](../../../../plans_mini/k-4-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| wrong_scope_or_filter | broader two-school scope | 1 | [task](../../../../tasks_mini/k-4-d-2/task_10.json) / [plan](../../../../plans_mini/k-4-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_10.log) |
| wrong_scope_or_filter | county_only_instead_of_chicago_in_county | 1 | [task](../../../../tasks_mini/k-3-d-2/task_7.json) / [plan](../../../../plans_mini/k-3-d-2/task_7.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_7.log) |
| wrong_scope_or_filter | drifted_to_statewide_then_still_missed_city_filter | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_scope_or_filter | extra Ward 2 filter on the 2020 count | 1 | [task](../../../../tasks_mini/k-5-d-1/task_3.json) / [plan](../../../../plans_mini/k-5-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-1/task_3.log) |
| wrong_scope_or_filter | included Orange County outside the required intersection | 1 | [task](../../../../tasks_mini/k-5-d-3/task_13.json) / [plan](../../../../plans_mini/k-5-d-3/task_13.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_13.log) |
| wrong_scope_or_filter | misclassified Harris in the original-23 county filter | 1 | [task](../../../../tasks_mini/k-4-d-4/task_6.json) / [plan](../../../../plans_mini/k-4-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| wrong_scope_or_filter | mismatched_sitecounty_vs_cecounty_scope | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| wrong_scope_or_filter | missing Boston restriction in private-school count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| wrong_scope_or_filter | omitted authored filters in school ranking | 1 | [task](../../../../tasks_mini/k-3-d-4/task_5.json) / [plan](../../../../plans_mini/k-3-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_5.log) |
| wrong_scope_or_filter | omitted_detroit_city_filter | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_scope_or_filter | omitted_required_filter_and_used_proxy_grouping | 1 | [task](../../../../tasks_mini/k-4-d-5/task_4.json) / [plan](../../../../plans_mini/k-4-d-5/task_4.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_4.log) |
| wrong_scope_or_filter | over-restricted to precinct 44 in final count | 1 | [task](../../../../tasks_mini/k-4-d-1/task_3.json) / [plan](../../../../plans_mini/k-4-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_3.log) |
| wrong_scope_or_filter | single-year scope and malformed filter | 1 | [task](../../../../tasks_mini/k-4-d-4/task_9.json) / [plan](../../../../plans_mini/k-4-d-4/task_9.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_9.log) |
| wrong_scope_or_filter | used a generic Lansing CBSA lookup instead of the school-year-specific authored computation | 1 | [task](../../../../tasks_mini/k-3-d-2/task_6.json) / [plan](../../../../plans_mini/k-3-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| wrong_scope_or_filter | used county-only Orange County filter instead of the authored Orlando city-specific filter | 1 | [task](../../../../tasks_mini/k-3-d-2/task_10.json) / [plan](../../../../plans_mini/k-3-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| wrong_scope_or_filter | used max/frequency instead of the elementary-school Level 1 filter | 1 | [task](../../../../tasks_mini/k-4-d-4/task_2.json) / [plan](../../../../plans_mini/k-4-d-4/task_2.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_2.log) |
| wrong_scope_or_filter | wrong city set and year scope | 1 | [task](../../../../tasks_mini/k-4-d-4/task_4.json) / [plan](../../../../plans_mini/k-4-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_4.log) |
| wrong_scope_or_filter | wrong county branch | 1 | [task](../../../../tasks_mini/k-7-d-4/task_1.json) / [plan](../../../../plans_mini/k-7-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-7-d-4/task_1.log) |
| wrong_scope_or_filter | wrong county filters and missing program-year filter | 1 | [task](../../../../tasks_mini/k-5-d-4/task_5.json) / [plan](../../../../plans_mini/k-5-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_5.log) |
| wrong_scope_or_filter | wrong county selected in the release comparison | 1 | [task](../../../../tasks_mini/k-4-d-4/task_6.json) / [plan](../../../../plans_mini/k-4-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| wrong_scope_or_filter | wrong county set and census filter pattern | 1 | [task](../../../../tasks_mini/k-5-d-4/task_8.json) / [plan](../../../../plans_mini/k-5-d-4/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_8.log) |
| wrong_scope_or_filter | wrong founder/county pair | 1 | [task](../../../../tasks_mini/k-4-d-4/task_12.json) / [plan](../../../../plans_mini/k-4-d-4/task_12.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_12.log) |
| wrong_scope_or_filter | wrong honoree branch | 1 | [task](../../../../tasks_mini/k-4-d-4/task_13.json) / [plan](../../../../plans_mini/k-4-d-4/task_13.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_13.log) |
| wrong_scope_or_filter | wrong intermediate branch | 1 | [task](../../../../tasks_mini/k-3-d-3/task_6.json) / [plan](../../../../plans_mini/k-3-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_6.log) |
| wrong_scope_or_filter | wrong_branch_community_area_chain | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| wrong_scope_or_filter | wrong_county_lookup | 1 | [task](../../../../tasks_mini/k-6-d-2/task_3.json) / [plan](../../../../plans_mini/k-6-d-2/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_3.log) |
| wrong_scope_or_filter | wrong_field_threshold | 1 | [task](../../../../tasks_mini/k-5-d-2/task_8.json) / [plan](../../../../plans_mini/k-5-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_8.log) |
| wrong_source_or_dataset | 500-Cities release/version confusion | 1 | [task](../../../../tasks_mini/k-5-d-4/task_3.json) / [plan](../../../../plans_mini/k-5-d-4/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_3.log) |
| wrong_source_or_dataset | 500-cities_vs_city-page | 1 | [task](../../../../tasks_mini/k-5-d-2/task_8.json) / [plan](../../../../plans_mini/k-5-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_8.log) |
| wrong_source_or_dataset | file_format_mismatch | 1 | [task](../../../../tasks_mini/k-6-d-3/task_5.json) / [plan](../../../../plans_mini/k-6-d-3/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_5.log) |
| wrong_source_or_dataset | missing_neighborhood_field | 1 | [task](../../../../tasks_mini/k-3-d-5/task_1.json) / [plan](../../../../plans_mini/k-3-d-5/task_1.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-5/task_1.log) |
| wrong_source_or_dataset | used the 2019-20 postsecondary dataset instead of the task-specified Polk County postsecondary count | 1 | [task](../../../../tasks_mini/k-4-d-4/task_10.json) / [plan](../../../../plans_mini/k-4-d-4/task_10.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_10.log) |

## Co-occurring Failure Types

| Failure Type Set | Rows |
| --- | --- |
| wrong_scope_or_filter | 8 |
| tool_or_data_blocker; wrong_scope_or_filter | 7 |
| evidence_available_answer_error | 6 |
| extraction_or_parsing_error | 4 |
| tool_or_data_blocker | 4 |
| query_execution_error_loop; wrong_scope_or_filter | 3 |
| computation_or_aggregation_error | 2 |
| computation_or_aggregation_error; planning_decomposition_mismatch | 2 |
| evidence_available_answer_error; wrong_scope_or_filter | 2 |
| evidence_available_answer_error; wrong_source_or_dataset | 2 |
| incomplete_evidence_budget_exhausted; tool_or_data_blocker | 2 |
| computation_or_aggregation_error; planning_decomposition_mismatch; tool_or_data_blocker | 1 |
| evidence_available_answer_error; wrong_scope_or_filter; wrong_source_or_dataset | 1 |
| extraction_or_parsing_error; planning_decomposition_mismatch; tool_or_data_blocker | 1 |
| extraction_or_parsing_error; tool_or_data_blocker | 1 |
| incomplete_evidence_budget_exhausted; planning_decomposition_mismatch; tool_or_data_blocker | 1 |
| incomplete_evidence_early_answer | 1 |
| incomplete_evidence_early_answer; query_execution_error_loop | 1 |
| incomplete_evidence_early_answer; query_execution_error_loop; wrong_scope_or_filter | 1 |
| low_yield_search_loop; schema_or_shape_inspection_loop; wrong_scope_or_filter | 1 |
| other_or_unclear; wrong_scope_or_filter | 1 |
| planning_decomposition_mismatch | 1 |
| planning_decomposition_mismatch; query_execution_error_loop | 1 |
| planning_decomposition_mismatch; question_or_constraint_misread | 1 |
| planning_decomposition_mismatch; question_or_constraint_misread; wrong_scope_or_filter | 1 |
| planning_decomposition_mismatch; tool_or_data_blocker | 1 |
| planning_decomposition_mismatch; tool_or_data_blocker; wrong_scope_or_filter | 1 |
| query_execution_error_loop | 1 |
| query_execution_error_loop; wrong_source_or_dataset | 1 |
| semantic_or_gold_label_issue | 1 |
| wrong_source_or_dataset | 1 |

## Representative Evidence

- `tasks_mini/k-3-d-2/task_1.json` `planning_decomposition_mismatch`/`added extra applied_force constraint`: Turn 5 | Tool result: {"success": true, "dataset_id": "apd-searches-by-type", "rows": [["Charlie"]], "row_count": 1}; Turn 7 | Tool result: {"output": "1", "success": true, "dataset_id": "apd-computer-aided-dispatch-i...
- `tasks_mini/k-3-d-2/task_1.json` `computation_or_aggregation_error`/`incorrect per-century arithmetic`: Turn 2 | Tool result: {"dataset_id": "Austin,_Texas", "file_path": "content.txt", "preview_text": "Austin ... Incorporated on December 27, 1839, it has been one of the fastest-growing large cities ..."}; Turn 16 | Mod...
- `tasks_mini/k-3-d-2/task_10.json` `wrong_scope_or_filter`/`used county-only Orange County filter instead of the authored Orlando city-specific filter`: Turn 6 | Model response #1 [role=assistant block=1 tool_use] select_match({"index": 0, "reason": "The authored record counts private schools for school year 2021-2022 in a specific city ('ORLANDO') and uses upper(trim...
- `tasks_mini/k-3-d-2/task_11.json` `tool_or_data_blocker`/`data_source_missing_or_unavailable`: Turn 10 read_file output for Basin,_Wyoming shows the climate sentence with the temperature value blanked out.
- `tasks_mini/k-3-d-2/task_11.json` `tool_or_data_blocker`/`malformed_tool_call`: Turn 11 execute_ideal raised FileNotFoundError for `.../Basin,_Wyoming/content.txt`, and the sandbox listed only `content.txt.read_result.json` for that dataset.

# Answer Failure Report

- Source root: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_answer_failures`
- Event rows: 114
- Trusted event rows: 110
- Non-correct eval rows: 57
- Events excluded by validation/model-validation: 4

## Counts by Failure Type

| Failure Type | Events |
| --- | --- |
| wrong_source_or_scope | 27 |
| tool_or_data_blocker | 15 |
| extraction_or_parsing_error | 14 |
| evidence_available_answer_error | 12 |
| query_execution_error_loop | 12 |
| incomplete_evidence_not_enough_turns | 10 |
| computation_or_aggregation_error | 8 |
| question_or_constraint_misread | 5 |
| planning_decomposition_mismatch | 4 |
| low_yield_search_loop | 2 |
| schema_or_shape_inspection_loop | 1 |

## Counts by Failure Type and Subtype

| Failure Type | Subtype | Events | Representative |
| --- | --- | --- | --- |
| incomplete_evidence_not_enough_turns | tool_budget_exhausted | 9 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| tool_or_data_blocker | tool_budget_exhausted | 9 | [task](../../../../tasks_mini/k-4-d-2/task_1.json) / [plan](../../../../plans_mini/k-4-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| tool_or_data_blocker | unsupported_or_oversized_data_access | 5 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| computation_or_aggregation_error | approximate_final_value | 1 | [task](../../../../tasks_mini/k-4-d-4/task_6.json) / [plan](../../../../plans_mini/k-4-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| computation_or_aggregation_error | binary_counting_instead_of_gt0_filter | 1 | [task](../../../../tasks_mini/k-4-d-1/task_5.json) / [plan](../../../../plans_mini/k-4-d-1/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-1/task_5.log) |
| computation_or_aggregation_error | failed_hop_intersection | 1 | [task](../../../../tasks_mini/k-5-d-3/task_9.json) / [plan](../../../../plans_mini/k-5-d-3/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_9.log) |
| computation_or_aggregation_error | misranked_minimum | 1 | [task](../../../../tasks_mini/k-4-d-3/task_2.json) / [plan](../../../../plans_mini/k-4-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| computation_or_aggregation_error | summed_multiple_rows_instead_of_extracting_single_district_total | 1 | [task](../../../../tasks_mini/k-4-d-2/task_15.json) / [plan](../../../../plans_mini/k-4-d-2/task_15.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_15.log) |
| computation_or_aggregation_error | wrong proxy aggregation for the arrest-area hop | 1 | [task](../../../../tasks_mini/k-4-d-2/task_6.json) / [plan](../../../../plans_mini/k-4-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_6.log) |
| computation_or_aggregation_error | wrong_filter_scope | 1 | [task](../../../../tasks_mini/k-5-d-1/task_3.json) / [plan](../../../../plans_mini/k-5-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-1/task_3.log) |
| computation_or_aggregation_error | wrong_final_arithmetic | 1 | [task](../../../../tasks_mini/k-3-d-4/task_6.json) / [plan](../../../../plans_mini/k-3-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-4/task_6.log) |
| evidence_available_answer_error | extra_intermediate_entity_in_final_answer | 1 | [task](../../../../tasks_mini/k-3-d-4/task_5.json) / [plan](../../../../plans_mini/k-3-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-4/task_5.log) |
| evidence_available_answer_error | selected_wrong_count_after_wrong_intermediate | 1 | [task](../../../../tasks_mini/k-4-d-1/task_1.json) / [plan](../../../../plans_mini/k-4-d-1/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-1/task_1.log) |
| evidence_available_answer_error | submitted wrong final result from incorrect intermediates | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| evidence_available_answer_error | submitted_intermediate_hops_instead_of_final_scalar_answer | 1 | [task](../../../../tasks_mini/k-4-d-2/task_2.json) / [plan](../../../../plans_mini/k-4-d-2/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_2.log) |
| evidence_available_answer_error | submitted_stale_answer_after_self_correction | 1 | [task](../../../../tasks_mini/k-4-d-2/task_5.json) / [plan](../../../../plans_mini/k-4-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_5.log) |
| evidence_available_answer_error | submitted_wrong_final_year | 1 | [task](../../../../tasks_mini/k-5-d-3/task_3.json) / [plan](../../../../plans_mini/k-5-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| evidence_available_answer_error | submitted_wrong_result | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| evidence_available_answer_error | wrong_branch_or_area_selected | 1 | [task](../../../../tasks_mini/k-5-d-3/task_9.json) / [plan](../../../../plans_mini/k-5-d-3/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_9.log) |
| evidence_available_answer_error | wrong_final_year | 1 | [task](../../../../tasks_mini/k-4-d-5/task_1.json) / [plan](../../../../plans_mini/k-4-d-5/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-5/task_1.log) |
| evidence_available_answer_error | wrong_founding_year_selected | 1 | [task](../../../../tasks_mini/k-5-d-4/task_3.json) / [plan](../../../../plans_mini/k-5-d-4/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-4/task_3.log) |
| evidence_available_answer_error | wrong_museum_year_selected | 1 | [task](../../../../tasks_mini/k-3-d-4/task_7.json) / [plan](../../../../plans_mini/k-3-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-4/task_7.log) |
| evidence_available_answer_error | wrong_namesake_pair_finalized | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| extraction_or_parsing_error | district_office_count_from_truncated_grep | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| extraction_or_parsing_error | misread_year_from_history_range | 1 | [task](../../../../tasks_mini/k-5-d-3/task_3.json) / [plan](../../../../plans_mini/k-5-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| extraction_or_parsing_error | overbroad_description_filter | 1 | [task](../../../../tasks_mini/k-4-d-2/task_8.json) / [plan](../../../../plans_mini/k-4-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_8.log) |
| extraction_or_parsing_error | public_school_count_misread | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| extraction_or_parsing_error | sitecounty_instead_of_cecounty | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| extraction_or_parsing_error | truncated_grep_result_misread | 1 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| extraction_or_parsing_error | wrong_column_used_for_shooting_descriptor | 1 | [task](../../../../tasks_mini/k-5-d-1/task_4.json) / [plan](../../../../plans_mini/k-5-d-1/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-1/task_4.log) |
| extraction_or_parsing_error | wrong_column_used_in_complaints | 1 | [task](../../../../tasks_mini/k-5-d-1/task_4.json) / [plan](../../../../plans_mini/k-5-d-1/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-1/task_4.log) |
| extraction_or_parsing_error | wrong_grandfather_name | 1 | [task](../../../../tasks_mini/k-4-d-4/task_13.json) / [plan](../../../../plans_mini/k-4-d-4/task_13.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-4/task_13.log) |
| extraction_or_parsing_error | wrong_historical_entity | 1 | [task](../../../../tasks_mini/k-4-d-4/task_8.json) / [plan](../../../../plans_mini/k-4-d-4/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-4/task_8.log) |
| extraction_or_parsing_error | wrong_person_name_extracted_from_wikipedia | 1 | [task](../../../../tasks_mini/k-4-d-3/task_6.json) / [plan](../../../../plans_mini/k-4-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| extraction_or_parsing_error | wrong_row_selected | 1 | [task](../../../../tasks_mini/k-4-d-4/task_11.json) / [plan](../../../../plans_mini/k-4-d-4/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-4/task_11.log) |
| extraction_or_parsing_error | wrong_xml_field_path | 1 | [task](../../../../tasks_mini/k-6-d-3/task_5.json) / [plan](../../../../plans_mini/k-6-d-3/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-6-d-3/task_5.log) |
| extraction_or_parsing_error | wrong_year_extracted_from_holland_land_company_text | 1 | [task](../../../../tasks_mini/k-5-d-4/task_1.json) / [plan](../../../../plans_mini/k-5-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-4/task_1.log) |
| incomplete_evidence_not_enough_turns | tool_budget_exhausted_before_final_lookup | 1 | [task](../../../../tasks_mini/k-5-d-3/task_8.json) / [plan](../../../../plans_mini/k-5-d-3/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_8.log) |
| low_yield_search_loop | repeated_no_match_searches | 1 | [task](../../../../tasks_mini/k-5-d-3/task_2.json) / [plan](../../../../plans_mini/k-5-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_2.log) |
| low_yield_search_loop | repeated_no_result_searches_for_street_sweeping_source | 1 | [task](../../../../tasks_mini/k-5-d-3/task_11.json) / [plan](../../../../plans_mini/k-5-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_11.log) |
| planning_decomposition_mismatch | omitted_required_final_source_hop | 1 | [task](../../../../tasks_mini/k-5-d-3/task_12.json) / [plan](../../../../plans_mini/k-5-d-3/task_12.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_12.log) |
| planning_decomposition_mismatch | skipped final head/university hop after budget aggregation | 1 | [task](../../../../tasks_mini/k-5-d-3/task_8.json) / [plan](../../../../plans_mini/k-5-d-3/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_8.log) |
| planning_decomposition_mismatch | skipped_area_id_mapping_and_final_area_code_filter | 1 | [task](../../../../tasks_mini/k-4-d-2/task_2.json) / [plan](../../../../plans_mini/k-4-d-2/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_2.log) |
| planning_decomposition_mismatch | skipped_required_intersection_hops | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| query_execution_error_loop | cross_file_sql_binder_error | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| query_execution_error_loop | file_too_large_for_query | 1 | [task](../../../../tasks_mini/k-4-d-2/task_9.json) / [plan](../../../../plans_mini/k-4-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_9.log) |
| query_execution_error_loop | json_shape_mismatch | 1 | [task](../../../../tasks_mini/k-4-d-3/task_7.json) / [plan](../../../../plans_mini/k-4-d-3/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-3/task_7.log) |
| query_execution_error_loop | malformed_sql_and_column_quoting | 1 | [task](../../../../tasks_mini/k-4-d-4/task_13.json) / [plan](../../../../plans_mini/k-4-d-4/task_13.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-4/task_13.log) |
| query_execution_error_loop | malformed_sql_and_table_calls | 1 | [task](../../../../tasks_mini/k-6-d-3/task_5.json) / [plan](../../../../plans_mini/k-6-d-3/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-6-d-3/task_5.log) |
| query_execution_error_loop | malformed_sql_binder_errors | 1 | [task](../../../../tasks_mini/k-4-d-4/task_10.json) / [plan](../../../../plans_mini/k-4-d-4/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-4/task_10.log) |
| query_execution_error_loop | malformed_tool_call | 1 | [task](../../../../tasks_mini/k-5-d-3/task_14.json) / [plan](../../../../plans_mini/k-5-d-3/task_14.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_14.log) |
| query_execution_error_loop | nested_json_schema_mismatch | 1 | [task](../../../../tasks_mini/k-3-d-2/task_6.json) / [plan](../../../../plans_mini/k-3-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| query_execution_error_loop | repeated malformed query calls | 1 | [task](../../../../tasks_mini/k-3-d-4/task_6.json) / [plan](../../../../plans_mini/k-3-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-4/task_6.log) |
| query_execution_error_loop | repeated_duckdb_binder_errors | 1 | [task](../../../../tasks_mini/k-3-d-2/task_10.json) / [plan](../../../../plans_mini/k-3-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| query_execution_error_loop | schema_mismatch_and_near_duplicate_query_failures | 1 | [task](../../../../tasks_mini/k-5-d-3/task_11.json) / [plan](../../../../plans_mini/k-5-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_11.log) |
| query_execution_error_loop | sql_schema_mismatch | 1 | [task](../../../../tasks_mini/k-3-d-2/task_4.json) / [plan](../../../../plans_mini/k-3-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_4.log) |
| question_or_constraint_misread | extra_precinct_filter_in_final_count | 1 | [task](../../../../tasks_mini/k-4-d-1/task_3.json) / [plan](../../../../plans_mini/k-4-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-1/task_3.log) |
| question_or_constraint_misread | ignored_original_23_exclusion | 1 | [task](../../../../tasks_mini/k-4-d-4/task_6.json) / [plan](../../../../plans_mini/k-4-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| question_or_constraint_misread | top-2 rank misread | 1 | [task](../../../../tasks_mini/k-4-d-3/task_1.json) / [plan](../../../../plans_mini/k-4-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-3/task_1.log) |
| question_or_constraint_misread | wrong_status_filter | 1 | [task](../../../../tasks_mini/k-4-d-5/task_1.json) / [plan](../../../../plans_mini/k-4-d-5/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-5/task_1.log) |
| question_or_constraint_misread | wrong_year_filter | 1 | [task](../../../../tasks_mini/k-4-d-5/task_1.json) / [plan](../../../../plans_mini/k-4-d-5/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-5/task_1.log) |
| schema_or_shape_inspection_loop | wrong_parser_for_json | 1 | [task](../../../../tasks_mini/k-4-d-4/task_10.json) / [plan](../../../../plans_mini/k-4-d-4/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-4/task_10.log) |
| tool_or_data_blocker | malformed_tool_call | 1 | [task](../../../../tasks_mini/k-4-d-2/task_2.json) / [plan](../../../../plans_mini/k-4-d-2/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_2.log) |
| wrong_source_or_scope | bid_instead_of_ward | 1 | [task](../../../../tasks_mini/k-3-d-2/task_4.json) / [plan](../../../../plans_mini/k-3-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_4.log) |
| wrong_source_or_scope | carried_sector_filter_into_final_count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| wrong_source_or_scope | county_scope_instead_of_pullman_school_district | 1 | [task](../../../../tasks_mini/k-4-d-2/task_15.json) / [plan](../../../../plans_mini/k-4-d-2/task_15.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_15.log) |
| wrong_source_or_scope | dropped_city_filter | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| wrong_source_or_scope | dropped_city_filter_and_counted_entire_cbsa | 1 | [task](../../../../tasks_mini/k-3-d-2/task_6.json) / [plan](../../../../plans_mini/k-3-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| wrong_source_or_scope | expanded_school_count_to_county | 1 | [task](../../../../tasks_mini/k-4-d-2/task_5.json) / [plan](../../../../plans_mini/k-4-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_5.log) |
| wrong_source_or_scope | extra_council_district_filter | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| wrong_source_or_scope | ignored_remaining-county filter in hop 3 | 1 | [task](../../../../tasks_mini/k-5-d-4/task_5.json) / [plan](../../../../plans_mini/k-5-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-4/task_5.log) |
| wrong_source_or_scope | missing_city_filter | 1 | [task](../../../../tasks_mini/k-3-d-2/task_10.json) / [plan](../../../../plans_mini/k-3-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| wrong_source_or_scope | missouri_branch | 1 | [task](../../../../tasks_mini/k-4-d-4/task_11.json) / [plan](../../../../plans_mini/k-4-d-4/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-4/task_11.log) |
| wrong_source_or_scope | omitted city filter for postsecondary count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_source_or_scope | overbroad_geography_filter | 1 | [task](../../../../tasks_mini/k-3-d-2/task_7.json) / [plan](../../../../plans_mini/k-3-d-2/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_7.log) |
| wrong_source_or_scope | overbroad_row_subset_or_filter | 1 | [task](../../../../tasks_mini/k-4-d-2/task_9.json) / [plan](../../../../plans_mini/k-4-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_9.log) |
| wrong_source_or_scope | spokane_branch_instead_of_whitman_branch | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| wrong_source_or_scope | used county-wide scope for public schools | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_source_or_scope | used crime incidents instead of arrest records | 1 | [task](../../../../tasks_mini/k-4-d-2/task_6.json) / [plan](../../../../plans_mini/k-4-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_6.log) |
| wrong_source_or_scope | used_arrest_dataset_for_crime_lookup | 1 | [task](../../../../tasks_mini/k-4-d-1/task_1.json) / [plan](../../../../plans_mini/k-4-d-1/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-1/task_1.log) |
| wrong_source_or_scope | used_dataset_yearbuilt_instead_of_target_building_page | 1 | [task](../../../../tasks_mini/k-5-d-3/task_12.json) / [plan](../../../../plans_mini/k-5-d-3/task_12.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_12.log) |
| wrong_source_or_scope | wrong dataset family / release confusion | 1 | [task](../../../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../../../plans_mini/k-6-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| wrong_source_or_scope | wrong neighborhood branch | 1 | [task](../../../../tasks_mini/k-4-d-3/task_1.json) / [plan](../../../../plans_mini/k-4-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-3/task_1.log) |
| wrong_source_or_scope | wrong_city_pair | 1 | [task](../../../../tasks_mini/k-4-d-4/task_4.json) / [plan](../../../../plans_mini/k-4-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-4/task_4.log) |
| wrong_source_or_scope | wrong_community_area_lookup | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| wrong_source_or_scope | wrong_dataset_for_2021_count | 1 | [task](../../../../tasks_mini/k-4-d-1/task_2.json) / [plan](../../../../plans_mini/k-4-d-1/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-1/task_2.log) |
| wrong_source_or_scope | wrong_final_hop_source | 1 | [task](../../../../tasks_mini/k-5-d-3/task_7.json) / [plan](../../../../plans_mini/k-5-d-3/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_7.log) |
| wrong_source_or_scope | wrong_geography_or_dataset_family | 1 | [task](../../../../tasks_mini/k-5-d-3/task_2.json) / [plan](../../../../plans_mini/k-5-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_2.log) |
| wrong_source_or_scope | wrong_officeholder_source | 1 | [task](../../../../tasks_mini/k-6-d-3/task_2.json) / [plan](../../../../plans_mini/k-6-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-6-d-3/task_2.log) |
| wrong_source_or_scope | wrong_postsecondary_dataset_year | 1 | [task](../../../../tasks_mini/k-3-d-4/task_6.json) / [plan](../../../../plans_mini/k-3-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-4/task_6.log) |

## Co-occurring Failure Types

| Failure Type Set | Rows |
| --- | --- |
| query_execution_error_loop; wrong_source_or_scope | 5 |
| tool_or_data_blocker; wrong_source_or_scope | 5 |
| evidence_available_answer_error; wrong_source_or_scope | 4 |
| extraction_or_parsing_error | 4 |
| evidence_available_answer_error | 3 |
| wrong_source_or_scope | 3 |
| computation_or_aggregation_error | 2 |
| computation_or_aggregation_error; wrong_source_or_scope | 2 |
| evidence_available_answer_error; extraction_or_parsing_error | 2 |
| extraction_or_parsing_error; query_execution_error_loop; tool_or_data_blocker | 2 |
| incomplete_evidence_not_enough_turns; query_execution_error_loop | 2 |
| planning_decomposition_mismatch; wrong_source_or_scope | 2 |
| tool_or_data_blocker | 2 |
| computation_or_aggregation_error; evidence_available_answer_error | 1 |
| computation_or_aggregation_error; incomplete_evidence_not_enough_turns | 1 |
| computation_or_aggregation_error; query_execution_error_loop; wrong_source_or_scope | 1 |
| computation_or_aggregation_error; question_or_constraint_misread; tool_or_data_blocker | 1 |
| evidence_available_answer_error; planning_decomposition_mismatch; tool_or_data_blocker | 1 |
| evidence_available_answer_error; question_or_constraint_misread | 1 |
| extraction_or_parsing_error; incomplete_evidence_not_enough_turns | 1 |
| extraction_or_parsing_error; incomplete_evidence_not_enough_turns; tool_or_data_blocker | 1 |
| extraction_or_parsing_error; tool_or_data_blocker | 1 |
| extraction_or_parsing_error; tool_or_data_blocker; wrong_source_or_scope | 1 |
| incomplete_evidence_not_enough_turns; low_yield_search_loop; query_execution_error_loop | 1 |
| incomplete_evidence_not_enough_turns; low_yield_search_loop; wrong_source_or_scope | 1 |
| incomplete_evidence_not_enough_turns; planning_decomposition_mismatch | 1 |
| incomplete_evidence_not_enough_turns; query_execution_error_loop; schema_or_shape_inspection_loop | 1 |
| incomplete_evidence_not_enough_turns; wrong_source_or_scope | 1 |
| question_or_constraint_misread | 1 |
| question_or_constraint_misread; wrong_source_or_scope | 1 |

## Representative Evidence

- `tasks_mini/k-2-d-3/task_1.json` `tool_or_data_blocker`/`unsupported_or_oversized_data_access`: Turn 15 | Tool logical error (status=error): {"error": "File too large to query directly (1377 MB). Use download + execute_code only if the source is tabular or JSON."}
- `tasks_mini/k-2-d-3/task_1.json` `extraction_or_parsing_error`/`truncated_grep_result_misread`: Turn 31 | total_matches 20 ... count_found_in_returned_matches 20 ... Full file path: /home/ec2-user/eval_eqa/exploratory-qa-eval/.sandbox_isolated/task_1027100_1778833379891/apd-computer-aided-dispatch-incidents/file...
- `tasks_mini/k-2-d-3/task_1.json` `incomplete_evidence_not_enough_turns`/`tool_budget_exhausted`: Turn 32 | Tool call cancelled. Tool limit reached (30/30 calls used). You must stop using other tools and immediately call submit_answer with your best current answer and reasoning.
- `tasks_mini/k-3-d-2/task_1.json` `tool_or_data_blocker`/`unsupported_or_oversized_data_access`: Turn 6 | query_file({"dataset_id": "apd-computer-aided-dispatch-incidents", "file_path": "files/rows.txt", "sql": "SELECT \"Council District\", COUNT(*) AS cnt\nFROM t\nWHERE \"Response Year\" = 2023 AND \"Sector\" =...
- `tasks_mini/k-3-d-2/task_1.json` `wrong_source_or_scope`/`carried_sector_filter_into_final_count`: Turn 29 | query_file({"dataset_id": "apd-use-of-force", "file_path": "files/rows.txt", "sql": "SELECT COUNT(*)\nFROM t\nWHERE (CAST(strftime('%Y', \"Occurred Date\") AS VARCHAR) = '2023')\nAND \"Council District\" = 1...

# Answer Failure Report

- Source root: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_answer_failures`
- Event rows: 105
- Trusted event rows: 95
- Non-correct eval rows: 50
- Events excluded by validation/model-validation: 10

## Counts by Failure Type

| Failure Type | Events |
| --- | --- |
| wrong_source_or_scope | 26 |
| evidence_available_answer_error | 21 |
| incomplete_evidence_not_enough_turns | 12 |
| tool_or_data_blocker | 12 |
| computation_or_aggregation_error | 9 |
| query_execution_error_loop | 6 |
| extraction_or_parsing_error | 2 |
| planning_decomposition_mismatch | 2 |
| schema_or_shape_inspection_loop | 2 |
| low_yield_search_loop | 1 |
| question_or_constraint_misread | 1 |
| semantic_or_gold_label_issue | 1 |

## Counts by Failure Type and Subtype

| Failure Type | Subtype | Events | Representative |
| --- | --- | --- | --- |
| tool_or_data_blocker | tool_budget_exhausted | 10 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| incomplete_evidence_not_enough_turns | tool_budget_exhausted | 9 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| evidence_available_answer_error | wrong_final_answer | 2 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| tool_or_data_blocker | unsupported_or_oversized_data_access | 2 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| wrong_source_or_scope | wrong_city_branch | 2 | [task](../../../../tasks_mini/k-4-d-4/task_4.json) / [plan](../../../../plans_mini/k-4-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_4.log) |
| computation_or_aggregation_error | averaged_wrong_yearly_counts | 1 | [task](../../../../tasks_mini/k-3-d-3/task_4.json) / [plan](../../../../plans_mini/k-3-d-3/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_4.log) |
| computation_or_aggregation_error | cross_year_candidate_error | 1 | [task](../../../../tasks_mini/k-4-d-4/task_13.json) / [plan](../../../../plans_mini/k-4-d-4/task_13.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_13.log) |
| computation_or_aggregation_error | incorrect_intersection_and_count_selection | 1 | [task](../../../../tasks_mini/k-6-d-3/task_5.json) / [plan](../../../../plans_mini/k-6-d-3/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_5.log) |
| computation_or_aggregation_error | missing_aggregation_and_filters | 1 | [task](../../../../tasks_mini/k-7-d-4/task_1.json) / [plan](../../../../plans_mini/k-7-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-7-d-4/task_1.log) |
| computation_or_aggregation_error | partial_sample_counting | 1 | [task](../../../../tasks_mini/k-5-d-1/task_3.json) / [plan](../../../../plans_mini/k-5-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-1/task_3.log) |
| computation_or_aggregation_error | truncated_final_count | 1 | [task](../../../../tasks_mini/k-5-d-1/task_3.json) / [plan](../../../../plans_mini/k-5-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-1/task_3.log) |
| computation_or_aggregation_error | wrong_counties_and_year_gap | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| computation_or_aggregation_error | wrong_final_count | 1 | [task](../../../../tasks_mini/k-5-d-3/task_14.json) / [plan](../../../../plans_mini/k-5-d-3/task_14.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_14.log) |
| computation_or_aggregation_error | wrong_rank_intersection | 1 | [task](../../../../tasks_mini/k-4-d-3/task_1.json) / [plan](../../../../plans_mini/k-4-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_1.log) |
| evidence_available_answer_error | answer_transcription_error | 1 | [task](../../../../tasks_mini/k-4-d-2/task_13.json) / [plan](../../../../plans_mini/k-4-d-2/task_13.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_13.log) |
| evidence_available_answer_error | extra_intermediate_entity | 1 | [task](../../../../tasks_mini/k-3-d-4/task_5.json) / [plan](../../../../plans_mini/k-3-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_5.log) |
| evidence_available_answer_error | hallucinated_white_share | 1 | [task](../../../../tasks_mini/k-4-d-2/task_1.json) / [plan](../../../../plans_mini/k-4-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| evidence_available_answer_error | intermediate_value_submitted | 1 | [task](../../../../tasks_mini/k-4-d-3/task_11.json) / [plan](../../../../plans_mini/k-4-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| evidence_available_answer_error | submitted wrong final numeric answer | 1 | [task](../../../../tasks_mini/k-3-d-2/task_10.json) / [plan](../../../../plans_mini/k-3-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| evidence_available_answer_error | wrong_birth_year | 1 | [task](../../../../tasks_mini/k-5-d-2/task_10.json) / [plan](../../../../plans_mini/k-5-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_10.log) |
| evidence_available_answer_error | wrong_branch_selected | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| evidence_available_answer_error | wrong_candidate_selected | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| evidence_available_answer_error | wrong_final_answer_after_using_wrong_count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_7.json) / [plan](../../../../plans_mini/k-3-d-2/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_7.log) |
| evidence_available_answer_error | wrong_final_answer_from_wrong_intermediate_count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| evidence_available_answer_error | wrong_final_answer_selected | 1 | [task](../../../../tasks_mini/k-4-d-3/task_6.json) / [plan](../../../../plans_mini/k-4-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| evidence_available_answer_error | wrong_final_answer_submitted | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| evidence_available_answer_error | wrong_final_chain | 1 | [task](../../../../tasks_mini/k-5-d-2/task_6.json) / [plan](../../../../plans_mini/k-5-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_6.log) |
| evidence_available_answer_error | wrong_final_choice | 1 | [task](../../../../tasks_mini/k-4-d-3/task_2.json) / [plan](../../../../plans_mini/k-4-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| evidence_available_answer_error | wrong_final_city_choice | 1 | [task](../../../../tasks_mini/k-4-d-4/task_5.json) / [plan](../../../../plans_mini/k-4-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_5.log) |
| evidence_available_answer_error | wrong_final_year | 1 | [task](../../../../tasks_mini/k-4-d-3/task_9.json) / [plan](../../../../plans_mini/k-4-d-3/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_9.log) |
| evidence_available_answer_error | wrong_intermediate_count_selected | 1 | [task](../../../../tasks_mini/k-3-d-1/task_1.json) / [plan](../../../../plans_mini/k-3-d-1/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-1/task_1.log) |
| evidence_available_answer_error | wrong_school_district_and_year | 1 | [task](../../../../tasks_mini/k-5-d-3/task_3.json) / [plan](../../../../plans_mini/k-5-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| evidence_available_answer_error | wrong_year_selected | 1 | [task](../../../../tasks_mini/k-3-d-4/task_7.json) / [plan](../../../../plans_mini/k-3-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_7.log) |
| extraction_or_parsing_error | approximate_value_substitution | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| extraction_or_parsing_error | wrong_historical_role_extracted | 1 | [task](../../../../tasks_mini/k-4-d-3/task_6.json) / [plan](../../../../plans_mini/k-4-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| incomplete_evidence_not_enough_turns | estimated_answer_after_budget_cutoff | 1 | [task](../../../../tasks_mini/k-4-d-4/task_10.json) / [plan](../../../../plans_mini/k-4-d-4/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_10.log) |
| incomplete_evidence_not_enough_turns | guessed_answer_after_budget_exhaustion | 1 | [task](../../../../tasks_mini/k-4-d-4/task_6.json) / [plan](../../../../plans_mini/k-4-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| incomplete_evidence_not_enough_turns | turn_or_time_budget_exhausted | 1 | [task](../../../../tasks_mini/k-4-d-5/task_3.json) / [plan](../../../../plans_mini/k-4-d-5/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_3.log) |
| low_yield_search_loop | broad_searches_for_identified_student_data | 1 | [task](../../../../tasks_mini/k-5-d-3/task_3.json) / [plan](../../../../plans_mini/k-5-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| planning_decomposition_mismatch | carried_precinct_filter_into_final_hop | 1 | [task](../../../../tasks_mini/k-4-d-1/task_3.json) / [plan](../../../../plans_mini/k-4-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_3.log) |
| planning_decomposition_mismatch | sitecounty_top10_wrong_aggregation | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| query_execution_error_loop | binder_and_catalog_errors | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| query_execution_error_loop | ideal_repair_failure | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| query_execution_error_loop | ideal_repair_jsondecodeerror_loop | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| query_execution_error_loop | repeated_parse_and_repair_failures | 1 | [task](../../../../tasks_mini/k-4-d-5/task_3.json) / [plan](../../../../plans_mini/k-4-d-5/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_3.log) |
| query_execution_error_loop | repeated_parse_xml_on_non_xml_files | 1 | [task](../../../../tasks_mini/k-4-d-4/task_10.json) / [plan](../../../../plans_mini/k-4-d-4/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_10.log) |
| query_execution_error_loop | unsupported_parser_on_json | 1 | [task](../../../../tasks_mini/k-5-d-3/task_14.json) / [plan](../../../../plans_mini/k-5-d-3/task_14.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_14.log) |
| question_or_constraint_misread | dropped city-level constraint on the public-school count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_10.json) / [plan](../../../../plans_mini/k-3-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| schema_or_shape_inspection_loop | metadata_wrapper_confusion | 1 | [task](../../../../tasks_mini/k-4-d-2/task_9.json) / [plan](../../../../plans_mini/k-4-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_9.log) |
| schema_or_shape_inspection_loop | nested_json_shape_probe_loop | 1 | [task](../../../../tasks_mini/k-3-d-4/task_4.json) / [plan](../../../../plans_mini/k-3-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| semantic_or_gold_label_issue | benchmark_label_mismatch | 1 | [task](../../../../tasks_mini/k-4-d-5/task_1.json) / [plan](../../../../plans_mini/k-4-d-5/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_1.log) |
| wrong_source_or_scope | counted_against_wrong_dataset_family_for_2021 | 1 | [task](../../../../tasks_mini/k-4-d-1/task_2.json) / [plan](../../../../plans_mini/k-4-d-1/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_2.log) |
| wrong_source_or_scope | counted_global_top_counties_instead_of_required_hop2_counties | 1 | [task](../../../../tasks_mini/k-3-d-3/task_4.json) / [plan](../../../../plans_mini/k-3-d-3/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_4.log) |
| wrong_source_or_scope | county_only_filter_for_district_offices | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| wrong_source_or_scope | county_only_filter_for_public_schools | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| wrong_source_or_scope | county_only_filter_instead_of_intended_count_scope | 1 | [task](../../../../tasks_mini/k-3-d-2/task_7.json) / [plan](../../../../plans_mini/k-3-d-2/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_7.log) |
| wrong_source_or_scope | county_only_scope_broadening | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| wrong_source_or_scope | current_year_to_date_complaint_source | 1 | [task](../../../../tasks_mini/k-3-d-1/task_1.json) / [plan](../../../../plans_mini/k-3-d-1/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-1/task_1.log) |
| wrong_source_or_scope | dataset_version_drift | 1 | [task](../../../../tasks_mini/k-3-d-4/task_6.json) / [plan](../../../../plans_mini/k-3-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_6.log) |
| wrong_source_or_scope | medicare_datasets_instead_of_state_drug_utilization | 1 | [task](../../../../tasks_mini/k-4-d-5/task_3.json) / [plan](../../../../plans_mini/k-4-d-5/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_3.log) |
| wrong_source_or_scope | outdated_dataset_version_and_field_mismatch | 1 | [task](../../../../tasks_mini/k-3-d-4/task_4.json) / [plan](../../../../plans_mini/k-3-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| wrong_source_or_scope | postsecondary_year_mismatch | 1 | [task](../../../../tasks_mini/k-6-d-3/task_5.json) / [plan](../../../../plans_mini/k-6-d-3/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_5.log) |
| wrong_source_or_scope | state_or_geography_swapped | 1 | [task](../../../../tasks_mini/k-4-d-4/task_11.json) / [plan](../../../../plans_mini/k-4-d-4/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_11.log) |
| wrong_source_or_scope | used_arrest_data_instead_of_2019_crime_data | 1 | [task](../../../../tasks_mini/k-4-d-1/task_2.json) / [plan](../../../../plans_mini/k-4-d-1/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_2.log) |
| wrong_source_or_scope | wrong geography / aggregation scope | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_source_or_scope | wrong_city_or_dataset_family | 1 | [task](../../../../tasks_mini/k-5-d-3/task_11.json) / [plan](../../../../plans_mini/k-5-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_11.log) |
| wrong_source_or_scope | wrong_councilmember_branch | 1 | [task](../../../../tasks_mini/k-5-d-2/task_6.json) / [plan](../../../../plans_mini/k-5-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_6.log) |
| wrong_source_or_scope | wrong_county_branch | 1 | [task](../../../../tasks_mini/k-7-d-4/task_1.json) / [plan](../../../../plans_mini/k-7-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-7-d-4/task_1.log) |
| wrong_source_or_scope | wrong_dataset_version | 1 | [task](../../../../tasks_mini/k-5-d-3/task_14.json) / [plan](../../../../plans_mini/k-5-d-3/task_14.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_14.log) |
| wrong_source_or_scope | wrong_metric_dataset | 1 | [task](../../../../tasks_mini/k-4-d-3/task_2.json) / [plan](../../../../plans_mini/k-4-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| wrong_source_or_scope | wrong_school_branch | 1 | [task](../../../../tasks_mini/k-4-d-3/task_1.json) / [plan](../../../../plans_mini/k-4-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_1.log) |
| wrong_source_or_scope | wrong_ward_branch | 1 | [task](../../../../tasks_mini/k-5-d-1/task_3.json) / [plan](../../../../plans_mini/k-5-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-1/task_3.log) |
| wrong_source_or_scope | wrong_year_source | 1 | [task](../../../../tasks_mini/k-5-d-3/task_12.json) / [plan](../../../../plans_mini/k-5-d-3/task_12.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_12.log) |
| wrong_source_or_scope | wrong_year_subset | 1 | [task](../../../../tasks_mini/k-4-d-2/task_6.json) / [plan](../../../../plans_mini/k-4-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_6.log) |
| wrong_source_or_scope | year_scope_mismatch | 1 | [task](../../../../tasks_mini/k-3-d-4/task_3.json) / [plan](../../../../plans_mini/k-3-d-4/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_3.log) |

## Co-occurring Failure Types

| Failure Type Set | Rows |
| --- | --- |
| evidence_available_answer_error; wrong_source_or_scope | 7 |
| evidence_available_answer_error | 5 |
| incomplete_evidence_not_enough_turns; wrong_source_or_scope | 4 |
| wrong_source_or_scope | 3 |
| computation_or_aggregation_error; tool_or_data_blocker; wrong_source_or_scope | 2 |
| computation_or_aggregation_error; wrong_source_or_scope | 2 |
| evidence_available_answer_error; query_execution_error_loop | 2 |
| evidence_available_answer_error; tool_or_data_blocker | 2 |
| incomplete_evidence_not_enough_turns; tool_or_data_blocker | 2 |
| tool_or_data_blocker; wrong_source_or_scope | 2 |
| computation_or_aggregation_error; incomplete_evidence_not_enough_turns; wrong_source_or_scope | 1 |
| computation_or_aggregation_error; planning_decomposition_mismatch; query_execution_error_loop | 1 |
| computation_or_aggregation_error; query_execution_error_loop; wrong_source_or_scope | 1 |
| computation_or_aggregation_error; tool_or_data_blocker | 1 |
| evidence_available_answer_error; extraction_or_parsing_error | 1 |
| evidence_available_answer_error; incomplete_evidence_not_enough_turns | 1 |
| evidence_available_answer_error; low_yield_search_loop | 1 |
| evidence_available_answer_error; question_or_constraint_misread | 1 |
| extraction_or_parsing_error; tool_or_data_blocker | 1 |
| incomplete_evidence_not_enough_turns; query_execution_error_loop; tool_or_data_blocker | 1 |
| incomplete_evidence_not_enough_turns; query_execution_error_loop; wrong_source_or_scope | 1 |
| incomplete_evidence_not_enough_turns; schema_or_shape_inspection_loop; tool_or_data_blocker | 1 |
| incomplete_evidence_not_enough_turns; schema_or_shape_inspection_loop; wrong_source_or_scope | 1 |
| planning_decomposition_mismatch | 1 |
| semantic_or_gold_label_issue | 1 |

## Representative Evidence

- `tasks_mini/k-2-d-3/task_1.json` `tool_or_data_blocker`/`unsupported_or_oversized_data_access`: Turn 15 | Tool logical error (status=error): {"success": false, "error": "Cannot execute SQL: file is too big (1377 MB >= 500 MB limit).", "dataset_id": "apd-computer-aided-dispatch-incidents"}
- `tasks_mini/k-2-d-3/task_1.json` `incomplete_evidence_not_enough_turns`/`tool_budget_exhausted`: Turn 32 | Tool call cancelled. Tool limit reached (30/30 calls used). You must stop using other tools and immediately call submit_answer with your best current answer and reasoning.
- `tasks_mini/k-3-d-1/task_1.json` `wrong_source_or_scope`/`current_year_to_date_complaint_source`: Turn 13 | `download({"files": [{"s3_uri": "s3://lakeqa-yc4103-datalake/datagov/nypd-complaint-data-current-year-to-date/files/rows.txt"}]})` ... `status": "downloaded"`; Turn 17 | `Tool result: {"output": "('PETIT LAR...
- `tasks_mini/k-3-d-1/task_1.json` `evidence_available_answer_error`/`wrong_intermediate_count_selected`: Turn 16 | `Tool result: {"output": "18613", "success": true, "dataset_id": "nypd-complaint-data-historic", "file_path": "files/rows.txt"}`; Turn 17 | `Tool result: {"output": "('PETIT LARCENY', 517)", "success": true,...
- `tasks_mini/k-3-d-2/task_1.json` `query_execution_error_loop`/`ideal_repair_failure`: Turn 22 | Tool logical error (status=error): {"success": false, "error": "Cannot execute SQL: file is too big (1377 MB >= 500 MB limit).", "dataset_id": "apd-computer-aided-dispatch-incidents", "file_path": "files/row...

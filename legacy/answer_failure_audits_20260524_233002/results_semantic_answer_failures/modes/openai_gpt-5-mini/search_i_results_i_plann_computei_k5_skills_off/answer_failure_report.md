# Answer Failure Report

- Source root: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_answer_failures`
- Event rows: 98
- Trusted event rows: 96
- Non-correct eval rows: 45
- Events excluded by validation/model-validation: 2

## Counts by Failure Type

| Failure Type | Events |
| --- | --- |
| wrong_source_or_scope | 21 |
| evidence_available_answer_error | 19 |
| tool_or_data_blocker | 14 |
| incomplete_evidence_not_enough_turns | 13 |
| computation_or_aggregation_error | 10 |
| question_or_constraint_misread | 5 |
| low_yield_search_loop | 4 |
| query_execution_error_loop | 4 |
| extraction_or_parsing_error | 2 |
| planning_decomposition_mismatch | 2 |
| same_hop_repetition | 1 |
| semantic_or_gold_label_issue | 1 |

## Counts by Failure Type and Subtype

| Failure Type | Subtype | Events | Representative |
| --- | --- | --- | --- |
| incomplete_evidence_not_enough_turns | tool_budget_exhausted | 6 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| incomplete_evidence_not_enough_turns | turn_or_time_budget_exhausted | 6 | [task](../../../../tasks_mini/k-3-d-4/task_4.json) / [plan](../../../../plans_mini/k-3-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| tool_or_data_blocker | tool_budget_exhausted | 6 | [task](../../../../tasks_mini/k-3-d-4/task_6.json) / [plan](../../../../plans_mini/k-3-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-4/task_6.log) |
| tool_or_data_blocker | unsupported_or_oversized_data_access | 4 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| evidence_available_answer_error | wrong_final_answer | 3 | [task](../../../../tasks_mini/k-4-d-3/task_2.json) / [plan](../../../../plans_mini/k-4-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| computation_or_aggregation_error | wrong_postsecondary_count | 2 | [task](../../../../tasks_mini/k-3-d-4/task_6.json) / [plan](../../../../plans_mini/k-3-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-4/task_6.log) |
| query_execution_error_loop | ideal_repair_failure | 2 | [task](../../../../tasks_mini/k-4-d-4/task_9.json) / [plan](../../../../plans_mini/k-4-d-4/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-4/task_9.log) |
| tool_or_data_blocker | turn_or_time_budget_exhausted | 2 | [task](../../../../tasks_mini/k-4-d-3/task_10.json) / [plan](../../../../plans_mini/k-4-d-3/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_10.log) |
| computation_or_aggregation_error | fabricated_final_average | 1 | [task](../../../../tasks_mini/k-4-d-4/task_6.json) / [plan](../../../../plans_mini/k-4-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| computation_or_aggregation_error | incorrect_total_or_input_value | 1 | [task](../../../../tasks_mini/k-4-d-4/task_10.json) / [plan](../../../../plans_mini/k-4-d-4/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-4/task_10.log) |
| computation_or_aggregation_error | omitted_candidate_city_in_average | 1 | [task](../../../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../../../plans_mini/k-6-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| computation_or_aggregation_error | percent_change_instead_of_ratio | 1 | [task](../../../../tasks_mini/k-3-d-2/task_2.json) / [plan](../../../../plans_mini/k-3-d-2/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_2.log) |
| computation_or_aggregation_error | reversed_difference | 1 | [task](../../../../tasks_mini/k-4-d-2/task_13.json) / [plan](../../../../plans_mini/k-4-d-2/task_13.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-2/task_13.log) |
| computation_or_aggregation_error | wrong_metric_and_grouping | 1 | [task](../../../../tasks_mini/k-4-d-3/task_6.json) / [plan](../../../../plans_mini/k-4-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| computation_or_aggregation_error | wrong_minimum_selection | 1 | [task](../../../../tasks_mini/k-4-d-3/task_2.json) / [plan](../../../../plans_mini/k-4-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| computation_or_aggregation_error | wrong_scope_final_count | 1 | [task](../../../../tasks_mini/k-5-d-1/task_3.json) / [plan](../../../../plans_mini/k-5-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-1/task_3.log) |
| evidence_available_answer_error | final_answer_wrong_year | 1 | [task](../../../../tasks_mini/k-5-d-4/task_1.json) / [plan](../../../../plans_mini/k-5-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-4/task_1.log) |
| evidence_available_answer_error | ignored_correct_count | 1 | [task](../../../../tasks_mini/k-4-d-1/task_2.json) / [plan](../../../../plans_mini/k-4-d-1/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-1/task_2.log) |
| evidence_available_answer_error | overrode_exact_result_with_estimate | 1 | [task](../../../../tasks_mini/k-3-d-2/task_7.json) / [plan](../../../../plans_mini/k-3-d-2/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_7.log) |
| evidence_available_answer_error | selected_excluded_county | 1 | [task](../../../../tasks_mini/k-4-d-4/task_6.json) / [plan](../../../../plans_mini/k-4-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| evidence_available_answer_error | submitted_wrong_year | 1 | [task](../../../../tasks_mini/k-5-d-3/task_12.json) / [plan](../../../../plans_mini/k-5-d-3/task_12.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-3/task_12.log) |
| evidence_available_answer_error | wrong_branch_selected | 1 | [task](../../../../tasks_mini/k-5-d-3/task_9.json) / [plan](../../../../plans_mini/k-5-d-3/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-3/task_9.log) |
| evidence_available_answer_error | wrong_entity_and_year | 1 | [task](../../../../tasks_mini/k-5-d-3/task_3.json) / [plan](../../../../plans_mini/k-5-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| evidence_available_answer_error | wrong_entity_selected | 1 | [task](../../../../tasks_mini/k-4-d-4/task_8.json) / [plan](../../../../plans_mini/k-4-d-4/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-4/task_8.log) |
| evidence_available_answer_error | wrong_final_answer_or_format | 1 | [task](../../../../tasks_mini/k-3-d-2/task_2.json) / [plan](../../../../plans_mini/k-3-d-2/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_2.log) |
| evidence_available_answer_error | wrong_final_answer_value_or_format | 1 | [task](../../../../tasks_mini/k-4-d-2/task_13.json) / [plan](../../../../plans_mini/k-4-d-2/task_13.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-2/task_13.log) |
| evidence_available_answer_error | wrong_final_pair_and_birth_year_difference | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| evidence_available_answer_error | wrong_final_synthesis | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| evidence_available_answer_error | wrong_final_value | 1 | [task](../../../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../../../plans_mini/k-6-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| evidence_available_answer_error | wrong_final_year | 1 | [task](../../../../tasks_mini/k-4-d-5/task_1.json) / [plan](../../../../plans_mini/k-4-d-5/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-5/task_1.log) |
| evidence_available_answer_error | wrong_incorporation_year | 1 | [task](../../../../tasks_mini/k-4-d-3/task_9.json) / [plan](../../../../plans_mini/k-4-d-3/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_9.log) |
| evidence_available_answer_error | wrong_school_denominator | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| extraction_or_parsing_error | wrong_famous_person_link | 1 | [task](../../../../tasks_mini/k-5-d-3/task_11.json) / [plan](../../../../plans_mini/k-5-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-3/task_11.log) |
| extraction_or_parsing_error | wrong_year_from_company_source | 1 | [task](../../../../tasks_mini/k-5-d-4/task_1.json) / [plan](../../../../plans_mini/k-5-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-4/task_1.log) |
| incomplete_evidence_not_enough_turns | (none) | 1 | [task](../../../../tasks_mini/k-4-d-2/task_1.json) / [plan](../../../../plans_mini/k-4-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| low_yield_search_loop | dataset_not_found_loop | 1 | [task](../../../../tasks_mini/k-5-d-1/task_4.json) / [plan](../../../../plans_mini/k-5-d-1/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-1/task_4.log) |
| low_yield_search_loop | repeated_dataset_not_found_searches | 1 | [task](../../../../tasks_mini/k-4-d-3/task_7.json) / [plan](../../../../plans_mini/k-4-d-3/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_7.log) |
| low_yield_search_loop | repeated_no_match_searches | 1 | [task](../../../../tasks_mini/k-5-d-4/task_5.json) / [plan](../../../../plans_mini/k-5-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-4/task_5.log) |
| low_yield_search_loop | repeated_salary_searches | 1 | [task](../../../../tasks_mini/k-4-d-4/task_4.json) / [plan](../../../../plans_mini/k-4-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-4/task_4.log) |
| planning_decomposition_mismatch | per_year_top_five_instead_of_cross_year_average | 1 | [task](../../../../tasks_mini/k-4-d-4/task_6.json) / [plan](../../../../plans_mini/k-4-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| planning_decomposition_mismatch | wrong_final_branch | 1 | [task](../../../../tasks_mini/k-5-d-2/task_5.json) / [plan](../../../../plans_mini/k-5-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-2/task_5.log) |
| query_execution_error_loop | unsupported_parse_and_jsondecode_loop | 1 | [task](../../../../tasks_mini/k-3-d-4/task_4.json) / [plan](../../../../plans_mini/k-3-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| query_execution_error_loop | xml_parser_on_json | 1 | [task](../../../../tasks_mini/k-6-d-3/task_4.json) / [plan](../../../../plans_mini/k-6-d-3/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-6-d-3/task_4.log) |
| question_or_constraint_misread | answer_shape_and_intermediate_field | 1 | [task](../../../../tasks_mini/k-4-d-1/task_2.json) / [plan](../../../../plans_mini/k-4-d-1/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-1/task_2.log) |
| question_or_constraint_misread | intersection_requirement_misread | 1 | [task](../../../../tasks_mini/k-4-d-3/task_1.json) / [plan](../../../../plans_mini/k-4-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_1.log) |
| question_or_constraint_misread | treated_open_date_as_school_day | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| question_or_constraint_misread | wrong_comparison_entities | 1 | [task](../../../../tasks_mini/k-4-d-4/task_4.json) / [plan](../../../../plans_mini/k-4-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-4/task_4.log) |
| question_or_constraint_misread | wrong_terminus_city | 1 | [task](../../../../tasks_mini/k-4-d-4/task_5.json) / [plan](../../../../plans_mini/k-4-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-4/task_5.log) |
| same_hop_repetition | redundant_candidate_rechecks | 1 | [task](../../../../tasks_mini/k-4-d-3/task_10.json) / [plan](../../../../plans_mini/k-4-d-3/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_10.log) |
| semantic_or_gold_label_issue | possible_gold_answer_mismatch | 1 | [task](../../../../tasks_mini/k-4-d-3/task_11.json) / [plan](../../../../plans_mini/k-4-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| tool_or_data_blocker | data_source_missing_or_unavailable | 1 | [task](../../../../tasks_mini/k-5-d-4/task_5.json) / [plan](../../../../plans_mini/k-5-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-4/task_5.log) |
| tool_or_data_blocker | runner_or_event_loop_exception | 1 | [task](../../../../tasks_mini/k-4-d-4/task_9.json) / [plan](../../../../plans_mini/k-4-d-4/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-4/task_9.log) |
| wrong_source_or_scope | county_only_district_office_count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| wrong_source_or_scope | county_only_district_office_filter | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| wrong_source_or_scope | county_only_private_school_filter | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| wrong_source_or_scope | county_only_public_school_count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| wrong_source_or_scope | county_wide_private_school_filter | 1 | [task](../../../../tasks_mini/k-3-d-2/task_7.json) / [plan](../../../../plans_mini/k-3-d-2/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_7.log) |
| wrong_source_or_scope | mismatched_source_family | 1 | [task](../../../../tasks_mini/k-5-d-3/task_3.json) / [plan](../../../../plans_mini/k-5-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| wrong_source_or_scope | missing_city_filter | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_source_or_scope | picked_watertown_page_instead_of_paddock_arcade | 1 | [task](../../../../tasks_mini/k-4-d-5/task_1.json) / [plan](../../../../plans_mini/k-4-d-5/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-5/task_1.log) |
| wrong_source_or_scope | searched_unsupported_census_zcta_source | 1 | [task](../../../../tasks_mini/k-4-d-2/task_1.json) / [plan](../../../../plans_mini/k-4-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| wrong_source_or_scope | used_building_energy_yearbuilt_instead_of_required_boeing_plant_2_source | 1 | [task](../../../../tasks_mini/k-5-d-3/task_12.json) / [plan](../../../../plans_mini/k-5-d-3/task_12.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-3/task_12.log) |
| wrong_source_or_scope | used_school_locations_open_date_instead_of_required_school_day_source | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| wrong_source_or_scope | wrong_branch_or_neighborhood | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| wrong_source_or_scope | wrong_city_branch | 1 | [task](../../../../tasks_mini/k-4-d-4/task_5.json) / [plan](../../../../plans_mini/k-4-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-4/task_5.log) |
| wrong_source_or_scope | wrong_county_city_branch | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| wrong_source_or_scope | wrong_county_field_and_year_scope | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| wrong_source_or_scope | wrong_county_set_for_postsecondary_step | 1 | [task](../../../../tasks_mini/k-3-d-4/task_4.json) / [plan](../../../../plans_mini/k-3-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| wrong_source_or_scope | wrong_dataset_and_filter | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| wrong_source_or_scope | wrong_entity_branch | 1 | [task](../../../../tasks_mini/k-4-d-3/task_6.json) / [plan](../../../../plans_mini/k-4-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| wrong_source_or_scope | wrong_neighborhood_lookup | 1 | [task](../../../../tasks_mini/k-5-d-3/task_9.json) / [plan](../../../../plans_mini/k-5-d-3/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-3/task_9.log) |
| wrong_source_or_scope | wrong_neighborhood_or_park_branch | 1 | [task](../../../../tasks_mini/k-4-d-3/task_1.json) / [plan](../../../../plans_mini/k-4-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_1.log) |
| wrong_source_or_scope | wrong_year_and_filter | 1 | [task](../../../../tasks_mini/k-4-d-3/task_9.json) / [plan](../../../../plans_mini/k-4-d-3/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_9.log) |

## Co-occurring Failure Types

| Failure Type Set | Rows |
| --- | --- |
| evidence_available_answer_error; wrong_source_or_scope | 8 |
| computation_or_aggregation_error; evidence_available_answer_error | 4 |
| incomplete_evidence_not_enough_turns; wrong_source_or_scope | 3 |
| computation_or_aggregation_error; tool_or_data_blocker | 2 |
| evidence_available_answer_error; extraction_or_parsing_error | 2 |
| evidence_available_answer_error; tool_or_data_blocker | 2 |
| incomplete_evidence_not_enough_turns; tool_or_data_blocker | 2 |
| question_or_constraint_misread; wrong_source_or_scope | 2 |
| wrong_source_or_scope | 2 |
| computation_or_aggregation_error | 1 |
| computation_or_aggregation_error; evidence_available_answer_error; planning_decomposition_mismatch | 1 |
| computation_or_aggregation_error; incomplete_evidence_not_enough_turns | 1 |
| computation_or_aggregation_error; tool_or_data_blocker; wrong_source_or_scope | 1 |
| evidence_available_answer_error; question_or_constraint_misread | 1 |
| evidence_available_answer_error; tool_or_data_blocker; wrong_source_or_scope | 1 |
| incomplete_evidence_not_enough_turns; low_yield_search_loop | 1 |
| incomplete_evidence_not_enough_turns; low_yield_search_loop; query_execution_error_loop; tool_or_data_blocker | 1 |
| incomplete_evidence_not_enough_turns; low_yield_search_loop; question_or_constraint_misread | 1 |
| incomplete_evidence_not_enough_turns; low_yield_search_loop; tool_or_data_blocker | 1 |
| incomplete_evidence_not_enough_turns; planning_decomposition_mismatch | 1 |
| incomplete_evidence_not_enough_turns; query_execution_error_loop | 1 |
| incomplete_evidence_not_enough_turns; query_execution_error_loop; wrong_source_or_scope | 1 |
| query_execution_error_loop; tool_or_data_blocker | 1 |
| question_or_constraint_misread; tool_or_data_blocker; wrong_source_or_scope | 1 |
| same_hop_repetition; tool_or_data_blocker | 1 |
| semantic_or_gold_label_issue | 1 |

## Representative Evidence

- `tasks_mini/k-2-d-3/task_1.json` `tool_or_data_blocker`/`unsupported_or_oversized_data_access`: Turn 24 | Tool logical error (status=error): {"success": false, "error": "Cannot execute SQL: file is too big (1377 MB >= 500 MB limit).", "dataset_id": "apd-computer-aided-dispatch-incidents", "file_path": "files/row...
- `tasks_mini/k-2-d-3/task_1.json` `incomplete_evidence_not_enough_turns`/`tool_budget_exhausted`: Turn 31 | Tool call cancelled. Tool limit reached (30/30 calls used). You must stop using other tools and immediately call submit_answer with your best current answer and reasoning. Do not call any other tool before s...
- `tasks_mini/k-3-d-2/task_1.json` `wrong_source_or_scope`/`wrong_dataset_and_filter`: Turn 1 | search_ideal({"query": "Austin Police Department 2023 taser use force incident 2023 dispatch system sector council district Austin dataset APD use of force 2023 'taser' 'dispatch' 'sector' 'council'"}) -> pic...
- `tasks_mini/k-3-d-2/task_1.json` `incomplete_evidence_not_enough_turns`/`tool_budget_exhausted`: Turn 31 | "Tool call cancelled. Tool limit reached (30/30 calls used). You must stop using other tools and immediately call submit_answer"; Turn 32 | reasoning: "With incomplete processing, the conservative rounded in...
- `tasks_mini/k-3-d-2/task_2.json` `computation_or_aggregation_error`/`percent_change_instead_of_ratio`: Turn 13 | submit_answer({"answer": "[Ward 4; THEFT F/AUTO; -7%]", "reasoning": "Brightwood is in Ward 4 (Wikipedia). In Ward 4 the most common offense in 2020 was THEFT F/AUTO with 1,070 incidents; in 2021 there were...

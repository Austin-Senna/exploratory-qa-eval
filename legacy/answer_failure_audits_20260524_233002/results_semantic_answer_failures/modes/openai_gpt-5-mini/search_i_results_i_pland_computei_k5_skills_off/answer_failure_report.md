# Answer Failure Report

- Source root: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_answer_failures`
- Event rows: 88
- Trusted event rows: 88
- Non-correct eval rows: 45

## Counts by Failure Type

| Failure Type | Events |
| --- | --- |
| evidence_available_answer_error | 20 |
| wrong_source_or_scope | 18 |
| computation_or_aggregation_error | 13 |
| tool_or_data_blocker | 11 |
| extraction_or_parsing_error | 9 |
| question_or_constraint_misread | 5 |
| planning_decomposition_mismatch | 4 |
| incomplete_evidence_not_enough_turns | 3 |
| query_execution_error_loop | 3 |
| other_or_unclear | 1 |
| semantic_or_gold_label_issue | 1 |

## Counts by Failure Type and Subtype

| Failure Type | Subtype | Events | Representative |
| --- | --- | --- | --- |
| tool_or_data_blocker | tool_budget_exhausted | 6 | [task](../../../../tasks_mini/k-3-d-4/task_1.json) / [plan](../../../../plans_mini/k-3-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-4/task_1.log) |
| query_execution_error_loop | ideal_repair_failure | 2 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| tool_or_data_blocker | runner_or_event_loop_exception | 2 | [task](../../../../tasks_mini/k-5-d-3/task_13.json) / [plan](../../../../plans_mini/k-5-d-3/task_13.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-3/task_13.log) |
| wrong_source_or_scope | countywide_instead_of_city_subset | 2 | [task](../../../../tasks_mini/k-3-d-2/task_10.json) / [plan](../../../../plans_mini/k-3-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| computation_or_aggregation_error | arithmetic_miscalculation | 1 | [task](../../../../tasks_mini/k-3-d-4/task_6.json) / [plan](../../../../plans_mini/k-3-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-4/task_6.log) |
| computation_or_aggregation_error | arithmetic_off_by_100 | 1 | [task](../../../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../../../plans_mini/k-6-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| computation_or_aggregation_error | candidate_set_miscarried | 1 | [task](../../../../tasks_mini/k-3-d-4/task_3.json) / [plan](../../../../plans_mini/k-3-d-4/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-4/task_3.log) |
| computation_or_aggregation_error | counted_wrong_year_and_group_for_final_hop | 1 | [task](../../../../tasks_mini/k-4-d-2/task_2.json) / [plan](../../../../plans_mini/k-4-d-2/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_2.log) |
| computation_or_aggregation_error | omitted_required_value | 1 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| computation_or_aggregation_error | partial_subset_counting | 1 | [task](../../../../tasks_mini/k-4-d-1/task_2.json) / [plan](../../../../plans_mini/k-4-d-1/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-1/task_2.log) |
| computation_or_aggregation_error | reversed_subtraction_order | 1 | [task](../../../../tasks_mini/k-4-d-2/task_13.json) / [plan](../../../../plans_mini/k-4-d-2/task_13.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_13.log) |
| computation_or_aggregation_error | set_intersection_misapplied | 1 | [task](../../../../tasks_mini/k-5-d-3/task_14.json) / [plan](../../../../plans_mini/k-5-d-3/task_14.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-3/task_14.log) |
| computation_or_aggregation_error | topk_intersection_miscomputed | 1 | [task](../../../../tasks_mini/k-4-d-3/task_1.json) / [plan](../../../../plans_mini/k-4-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-3/task_1.log) |
| computation_or_aggregation_error | wrong_aggregation_missing_groupby | 1 | [task](../../../../tasks_mini/k-4-d-2/task_14.json) / [plan](../../../../plans_mini/k-4-d-2/task_14.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_14.log) |
| computation_or_aggregation_error | wrong_average_from_wrong_2020_input | 1 | [task](../../../../tasks_mini/k-3-d-3/task_4.json) / [plan](../../../../plans_mini/k-3-d-3/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-3/task_4.log) |
| computation_or_aggregation_error | wrong_filtered_count | 1 | [task](../../../../tasks_mini/k-5-d-1/task_3.json) / [plan](../../../../plans_mini/k-5-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-1/task_3.log) |
| computation_or_aggregation_error | wrong_percentage_formula | 1 | [task](../../../../tasks_mini/k-3-d-2/task_2.json) / [plan](../../../../plans_mini/k-3-d-2/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_2.log) |
| evidence_available_answer_error | estimated_value_used | 1 | [task](../../../../tasks_mini/k-4-d-4/task_11.json) / [plan](../../../../plans_mini/k-4-d-4/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-4/task_11.log) |
| evidence_available_answer_error | ignored_correct_result_and_submitted_zero | 1 | [task](../../../../tasks_mini/k-5-d-1/task_4.json) / [plan](../../../../plans_mini/k-5-d-1/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-1/task_4.log) |
| evidence_available_answer_error | overinclusive_final_response | 1 | [task](../../../../tasks_mini/k-4-d-2/task_6.json) / [plan](../../../../plans_mini/k-4-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_6.log) |
| evidence_available_answer_error | propagated_wrong_intermediate_answer | 1 | [task](../../../../tasks_mini/k-4-d-2/task_14.json) / [plan](../../../../plans_mini/k-4-d-2/task_14.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_14.log) |
| evidence_available_answer_error | selected_wrong_person | 1 | [task](../../../../tasks_mini/k-4-d-3/task_6.json) / [plan](../../../../plans_mini/k-4-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| evidence_available_answer_error | submitted_intermediate_expression_instead_of_final_integer | 1 | [task](../../../../tasks_mini/k-4-d-2/task_13.json) / [plan](../../../../plans_mini/k-4-d-2/task_13.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_13.log) |
| evidence_available_answer_error | submitted_raw_count_instead_of_normalized_per_century_answer | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| evidence_available_answer_error | submitted_wrong_final_year | 1 | [task](../../../../tasks_mini/k-3-d-4/task_7.json) / [plan](../../../../plans_mini/k-3-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-4/task_7.log) |
| evidence_available_answer_error | unsupported_guess_after_blocker | 1 | [task](../../../../tasks_mini/k-5-d-3/task_3.json) / [plan](../../../../plans_mini/k-5-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| evidence_available_answer_error | wrong final year selected | 1 | [task](../../../../tasks_mini/k-5-d-4/task_1.json) / [plan](../../../../plans_mini/k-5-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-4/task_1.log) |
| evidence_available_answer_error | wrong_final_answer | 1 | [task](../../../../tasks_mini/k-4-d-1/task_2.json) / [plan](../../../../plans_mini/k-4-d-1/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-1/task_2.log) |
| evidence_available_answer_error | wrong_final_answer_format | 1 | [task](../../../../tasks_mini/k-3-d-2/task_2.json) / [plan](../../../../plans_mini/k-3-d-2/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_2.log) |
| evidence_available_answer_error | wrong_final_answer_selection | 1 | [task](../../../../tasks_mini/k-5-d-3/task_14.json) / [plan](../../../../plans_mini/k-5-d-3/task_14.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-3/task_14.log) |
| evidence_available_answer_error | wrong_final_choice | 1 | [task](../../../../tasks_mini/k-3-d-4/task_3.json) / [plan](../../../../plans_mini/k-3-d-4/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-4/task_3.log) |
| evidence_available_answer_error | wrong_final_number | 1 | [task](../../../../tasks_mini/k-6-d-3/task_5.json) / [plan](../../../../plans_mini/k-6-d-3/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-6-d-3/task_5.log) |
| evidence_available_answer_error | wrong_final_rank | 1 | [task](../../../../tasks_mini/k-3-d-4/task_1.json) / [plan](../../../../plans_mini/k-3-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-4/task_1.log) |
| evidence_available_answer_error | wrong_final_school_and_zip | 1 | [task](../../../../tasks_mini/k-4-d-2/task_1.json) / [plan](../../../../plans_mini/k-4-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| evidence_available_answer_error | wrong_final_value | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| evidence_available_answer_error | wrong_final_year | 1 | [task](../../../../tasks_mini/k-5-d-3/task_12.json) / [plan](../../../../plans_mini/k-5-d-3/task_12.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-3/task_12.log) |
| evidence_available_answer_error | wrong_intermediate_value_propagated_to_final_answer | 1 | [task](../../../../tasks_mini/k-3-d-2/task_6.json) / [plan](../../../../plans_mini/k-3-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| extraction_or_parsing_error | county_count_misread | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| extraction_or_parsing_error | empty_saved_artifact | 1 | [task](../../../../tasks_mini/k-6-d-3/task_5.json) / [plan](../../../../plans_mini/k-6-d-3/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-6-d-3/task_5.log) |
| extraction_or_parsing_error | grep_match_count_used_as_count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| extraction_or_parsing_error | sample_biased_location_category | 1 | [task](../../../../tasks_mini/k-4-d-1/task_3.json) / [plan](../../../../plans_mini/k-4-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-1/task_3.log) |
| extraction_or_parsing_error | used_open_date_as_school_day | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| extraction_or_parsing_error | wrong founding year extracted | 1 | [task](../../../../tasks_mini/k-5-d-4/task_1.json) / [plan](../../../../plans_mini/k-5-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-4/task_1.log) |
| extraction_or_parsing_error | wrong_historical_leader_fact | 1 | [task](../../../../tasks_mini/k-4-d-3/task_6.json) / [plan](../../../../plans_mini/k-4-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| extraction_or_parsing_error | wrong_year_extracted | 1 | [task](../../../../tasks_mini/k-4-d-5/task_1.json) / [plan](../../../../plans_mini/k-4-d-5/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-5/task_1.log) |
| extraction_or_parsing_error | wrong_year_from_museum_page | 1 | [task](../../../../tasks_mini/k-3-d-4/task_7.json) / [plan](../../../../plans_mini/k-3-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-4/task_7.log) |
| incomplete_evidence_not_enough_turns | hard_timeout_before_submit | 1 | [task](../../../../tasks_mini/k-5-d-4/task_2.json) / [plan](../../../../plans_mini/k-5-d-4/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) |
| incomplete_evidence_not_enough_turns | tool_budget_exhausted | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| incomplete_evidence_not_enough_turns | turn_or_time_budget_exhausted | 1 | [task](../../../../tasks_mini/k-7-d-4/task_1.json) / [plan](../../../../plans_mini/k-7-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-7-d-4/task_1.log) |
| other_or_unclear | unsupported_hate_crime_estimate | 1 | [task](../../../../tasks_mini/k-7-d-4/task_1.json) / [plan](../../../../plans_mini/k-7-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-7-d-4/task_1.log) |
| planning_decomposition_mismatch | cross_year_average_detour | 1 | [task](../../../../tasks_mini/k-4-d-4/task_6.json) / [plan](../../../../plans_mini/k-4-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| planning_decomposition_mismatch | skipped required county-population comparison | 1 | [task](../../../../tasks_mini/k-4-d-3/task_11.json) / [plan](../../../../plans_mini/k-4-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| planning_decomposition_mismatch | skipped_final_year_lookup | 1 | [task](../../../../tasks_mini/k-5-d-3/task_12.json) / [plan](../../../../plans_mini/k-5-d-3/task_12.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-3/task_12.log) |
| planning_decomposition_mismatch | skipped_intersection_and_used_wrong_branch | 1 | [task](../../../../tasks_mini/k-4-d-2/task_1.json) / [plan](../../../../plans_mini/k-4-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| query_execution_error_loop | xml_json_tool_mismatch | 1 | [task](../../../../tasks_mini/k-6-d-3/task_5.json) / [plan](../../../../plans_mini/k-6-d-3/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-6-d-3/task_5.log) |
| question_or_constraint_misread | broadened narcotic-drug-law filter into generic drug-related arrests | 1 | [task](../../../../tasks_mini/k-4-d-2/task_8.json) / [plan](../../../../plans_mini/k-4-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_8.log) |
| question_or_constraint_misread | carried_forward_intermediate_ward_filter | 1 | [task](../../../../tasks_mini/k-5-d-1/task_3.json) / [plan](../../../../plans_mini/k-5-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-1/task_3.log) |
| question_or_constraint_misread | extra_precinct_filter_and_broadened_location_predicate | 1 | [task](../../../../tasks_mini/k-4-d-1/task_3.json) / [plan](../../../../plans_mini/k-4-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-1/task_3.log) |
| question_or_constraint_misread | fiscal_year_treated_as_calendar_year_and_scope_widened | 1 | [task](../../../../tasks_mini/k-3-d-3/task_4.json) / [plan](../../../../plans_mini/k-3-d-3/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-3/task_4.log) |
| question_or_constraint_misread | used county-seat city population as the final comparator | 1 | [task](../../../../tasks_mini/k-4-d-3/task_11.json) / [plan](../../../../plans_mini/k-4-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| semantic_or_gold_label_issue | expected_answer_conflicts_with_logged_count | 1 | [task](../../../../tasks_mini/k-4-d-4/task_10.json) / [plan](../../../../plans_mini/k-4-d-4/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-4/task_10.log) |
| tool_or_data_blocker | data_source_missing_or_unavailable | 1 | [task](../../../../tasks_mini/k-5-d-4/task_5.json) / [plan](../../../../plans_mini/k-5-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-4/task_5.log) |
| tool_or_data_blocker | oversized_cad_file | 1 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| tool_or_data_blocker | tool_status_or_transport_error | 1 | [task](../../../../tasks_mini/k-5-d-4/task_2.json) / [plan](../../../../plans_mini/k-5-d-4/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) |
| wrong_source_or_scope | county_only_scope | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_source_or_scope | district_office_dataset_misidentified | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| wrong_source_or_scope | dropped_city_filter_for_private_school_count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_6.json) / [plan](../../../../plans_mini/k-3-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| wrong_source_or_scope | final_hop_used_wrong_dataset | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| wrong_source_or_scope | ignored_required_district_filter | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| wrong_source_or_scope | omitted_required_datasets_and_ended_on_area_name_fallback | 1 | [task](../../../../tasks_mini/k-4-d-2/task_2.json) / [plan](../../../../plans_mini/k-4-d-2/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_2.log) |
| wrong_source_or_scope | partial_population_source_set | 1 | [task](../../../../tasks_mini/k-3-d-4/task_3.json) / [plan](../../../../plans_mini/k-3-d-4/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-4/task_3.log) |
| wrong_source_or_scope | truncated_grep_subset | 1 | [task](../../../../tasks_mini/k-4-d-1/task_2.json) / [plan](../../../../plans_mini/k-4-d-1/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-1/task_2.log) |
| wrong_source_or_scope | used wrong area/source branch and skipped the required Central/RIPA path | 1 | [task](../../../../tasks_mini/k-4-d-2/task_8.json) / [plan](../../../../plans_mini/k-4-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-2/task_8.log) |
| wrong_source_or_scope | used_cad_incidents_instead_of_searches_by_type_for_sector_hop | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| wrong_source_or_scope | used_complaint_rows_for_shooting_hop | 1 | [task](../../../../tasks_mini/k-5-d-1/task_4.json) / [plan](../../../../plans_mini/k-5-d-1/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-1/task_4.log) |
| wrong_source_or_scope | wrong_branch_or_geography | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| wrong_source_or_scope | wrong_city_branch | 1 | [task](../../../../tasks_mini/k-4-d-4/task_4.json) / [plan](../../../../plans_mini/k-4-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-4/task_4.log) |
| wrong_source_or_scope | wrong_county_and_city_branch | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| wrong_source_or_scope | wrong_neighborhood_branch | 1 | [task](../../../../tasks_mini/k-4-d-3/task_1.json) / [plan](../../../../plans_mini/k-4-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-4-d-3/task_1.log) |
| wrong_source_or_scope | year_or_dataset_mismatch | 1 | [task](../../../../tasks_mini/k-3-d-4/task_6.json) / [plan](../../../../plans_mini/k-3-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/tasks_mini/k-3-d-4/task_6.log) |

## Co-occurring Failure Types

| Failure Type Set | Rows |
| --- | --- |
| computation_or_aggregation_error; evidence_available_answer_error | 4 |
| computation_or_aggregation_error; wrong_source_or_scope | 3 |
| evidence_available_answer_error; extraction_or_parsing_error | 3 |
| evidence_available_answer_error; tool_or_data_blocker | 3 |
| evidence_available_answer_error; wrong_source_or_scope | 3 |
| extraction_or_parsing_error; wrong_source_or_scope | 3 |
| tool_or_data_blocker | 3 |
| computation_or_aggregation_error; evidence_available_answer_error; wrong_source_or_scope | 2 |
| computation_or_aggregation_error; question_or_constraint_misread | 2 |
| evidence_available_answer_error; planning_decomposition_mismatch | 2 |
| tool_or_data_blocker; wrong_source_or_scope | 2 |
| computation_or_aggregation_error | 1 |
| computation_or_aggregation_error; query_execution_error_loop; tool_or_data_blocker | 1 |
| evidence_available_answer_error | 1 |
| evidence_available_answer_error; extraction_or_parsing_error; query_execution_error_loop | 1 |
| evidence_available_answer_error; query_execution_error_loop; wrong_source_or_scope | 1 |
| extraction_or_parsing_error | 1 |
| extraction_or_parsing_error; question_or_constraint_misread | 1 |
| incomplete_evidence_not_enough_turns; other_or_unclear | 1 |
| incomplete_evidence_not_enough_turns; tool_or_data_blocker | 1 |
| incomplete_evidence_not_enough_turns; wrong_source_or_scope | 1 |
| planning_decomposition_mismatch; question_or_constraint_misread | 1 |
| planning_decomposition_mismatch; tool_or_data_blocker | 1 |
| question_or_constraint_misread; wrong_source_or_scope | 1 |
| semantic_or_gold_label_issue | 1 |
| wrong_source_or_scope | 1 |

## Representative Evidence

- `tasks_mini/k-2-d-3/task_1.json` `tool_or_data_blocker`/`oversized_cad_file`: Turn 8 | The APD computer-aided-dispatch file was about 1.44 GB with an estimated 5.2 million rows, and the agent only saw a small preview rather than a usable full extract.
- `tasks_mini/k-2-d-3/task_1.json` `query_execution_error_loop`/`ideal_repair_failure`: Turn 15 | A query_ideal repair attempt failed with a JSONDecodeError during SQL repair, and similar repair failures kept recurring afterward.
- `tasks_mini/k-2-d-3/task_1.json` `computation_or_aggregation_error`/`omitted_required_value`: Turn 34 | The submitted reasoning only compared 1790 and the APD searches count of 3, and never incorporated the missing 5021 value that should have won the max comparison.
- `tasks_mini/k-3-d-2/task_1.json` `wrong_source_or_scope`/`used_cad_incidents_instead_of_searches_by_type_for_sector_hop`: Turn 2 | "Picked these datasets: - `s3://lakeqa-yc4103-datalake/datagov/apd-computer-aided-dispatch-incidents/files/rows.txt` - `s3://lakeqa-yc4103-datalake/datagov/apd-use-of-force/files/rows.txt`" and Turn 3 | "1) p...
- `tasks_mini/k-3-d-2/task_1.json` `evidence_available_answer_error`/`submitted_raw_count_instead_of_normalized_per_century_answer`: Turn 16 | `submit_answer({"answer": "[59]", "reasoning": "Counted 2023 use-of-force records in the CAD top sector and top council district where 'Used Taser(s)'=1, then divided by (2023-1839)/100 to get per-century av...

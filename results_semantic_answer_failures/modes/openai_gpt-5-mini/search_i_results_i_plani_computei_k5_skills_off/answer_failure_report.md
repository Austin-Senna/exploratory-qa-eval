# Answer Failure Report

- Source root: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_answer_failures`
- Event rows: 69
- Trusted event rows: 69
- Non-correct eval rows: 32

## Counts by Failure Type

| Failure Type | Events |
| --- | --- |
| wrong_source_or_scope | 20 |
| evidence_available_answer_error | 14 |
| tool_or_data_blocker | 10 |
| computation_or_aggregation_error | 7 |
| incomplete_evidence_not_enough_turns | 6 |
| question_or_constraint_misread | 4 |
| query_execution_error_loop | 3 |
| extraction_or_parsing_error | 2 |
| low_yield_search_loop | 1 |
| other_or_unclear | 1 |
| planning_decomposition_mismatch | 1 |

## Counts by Failure Type and Subtype

| Failure Type | Subtype | Events | Representative |
| --- | --- | --- | --- |
| incomplete_evidence_not_enough_turns | tool_budget_exhausted | 4 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| evidence_available_answer_error | wrong_final_answer | 3 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| tool_or_data_blocker | data_source_missing_or_unavailable | 3 | [task](../../../../tasks_mini/k-4-d-4/task_4.json) / [plan](../../../../plans_mini/k-4-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_4.log) |
| tool_or_data_blocker | tool_budget_exhausted | 3 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| wrong_source_or_scope | missing_city_filter | 3 | [task](../../../../tasks_mini/k-3-d-2/task_10.json) / [plan](../../../../plans_mini/k-3-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| query_execution_error_loop | ideal_repair_failure | 2 | [task](../../../../tasks_mini/k-3-d-4/task_4.json) / [plan](../../../../plans_mini/k-3-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| tool_or_data_blocker | ideal_repair_failure | 2 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| tool_or_data_blocker | unsupported_or_oversized_data_access | 2 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| computation_or_aggregation_error | estimated_postsecondary_count | 1 | [task](../../../../tasks_mini/k-3-d-4/task_4.json) / [plan](../../../../plans_mini/k-3-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| computation_or_aggregation_error | missed_all_years_intersection | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| computation_or_aggregation_error | sample_based_counting | 1 | [task](../../../../tasks_mini/k-4-d-1/task_2.json) / [plan](../../../../plans_mini/k-4-d-1/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_2.log) |
| computation_or_aggregation_error | unsupported_percent_guess | 1 | [task](../../../../tasks_mini/k-4-d-2/task_1.json) / [plan](../../../../plans_mini/k-4-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| computation_or_aggregation_error | wrong_final_addend | 1 | [task](../../../../tasks_mini/k-4-d-4/task_10.json) / [plan](../../../../plans_mini/k-4-d-4/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_10.log) |
| computation_or_aggregation_error | wrong_intermediate_precinct_ranking | 1 | [task](../../../../tasks_mini/k-5-d-1/task_4.json) / [plan](../../../../plans_mini/k-5-d-1/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-1/task_4.log) |
| computation_or_aggregation_error | wrong_isd_ranking_and_year | 1 | [task](../../../../tasks_mini/k-5-d-3/task_2.json) / [plan](../../../../plans_mini/k-5-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_2.log) |
| evidence_available_answer_error | extra_unrequested_values_in_final_answer | 1 | [task](../../../../tasks_mini/k-4-d-2/task_6.json) / [plan](../../../../plans_mini/k-4-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_6.log) |
| evidence_available_answer_error | final_answer_mismatch | 1 | [task](../../../../tasks_mini/k-4-d-2/task_5.json) / [plan](../../../../plans_mini/k-4-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_5.log) |
| evidence_available_answer_error | ignored_correct_school_day_evidence | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| evidence_available_answer_error | submitted_dataset_year_as_final_answer | 1 | [task](../../../../tasks_mini/k-5-d-3/task_12.json) / [plan](../../../../plans_mini/k-5-d-3/task_12.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_12.log) |
| evidence_available_answer_error | submitted_wrong_city | 1 | [task](../../../../tasks_mini/k-4-d-4/task_5.json) / [plan](../../../../plans_mini/k-4-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_5.log) |
| evidence_available_answer_error | submitted_wrong_final_answer | 1 | [task](../../../../tasks_mini/k-5-d-1/task_4.json) / [plan](../../../../plans_mini/k-5-d-1/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-1/task_4.log) |
| evidence_available_answer_error | unsupported_estimate_after_tool_limit | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| evidence_available_answer_error | wrong_final_birth_year | 1 | [task](../../../../tasks_mini/k-4-d-4/task_8.json) / [plan](../../../../plans_mini/k-4-d-4/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_8.log) |
| evidence_available_answer_error | wrong_final_value | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| evidence_available_answer_error | wrong_final_year_submitted | 1 | [task](../../../../tasks_mini/k-5-d-4/task_1.json) / [plan](../../../../plans_mini/k-5-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_1.log) |
| evidence_available_answer_error | wrong_year_selected_from_source | 1 | [task](../../../../tasks_mini/k-3-d-4/task_7.json) / [plan](../../../../plans_mini/k-3-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_7.log) |
| extraction_or_parsing_error | wrong_entity_from_source | 1 | [task](../../../../tasks_mini/k-4-d-3/task_6.json) / [plan](../../../../plans_mini/k-4-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| extraction_or_parsing_error | wrong_founding_year_extracted | 1 | [task](../../../../tasks_mini/k-5-d-4/task_1.json) / [plan](../../../../plans_mini/k-5-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_1.log) |
| incomplete_evidence_not_enough_turns | (none) | 1 | [task](../../../../tasks_mini/k-5-d-4/task_5.json) / [plan](../../../../plans_mini/k-5-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_5.log) |
| incomplete_evidence_not_enough_turns | turn_or_time_budget_exhausted | 1 | [task](../../../../tasks_mini/k-4-d-3/task_11.json) / [plan](../../../../plans_mini/k-4-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| low_yield_search_loop | repeated_nonproductive_census_searches | 1 | [task](../../../../tasks_mini/k-4-d-2/task_1.json) / [plan](../../../../plans_mini/k-4-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| other_or_unclear | unsupported_final_year_guess | 1 | [task](../../../../tasks_mini/k-4-d-5/task_1.json) / [plan](../../../../plans_mini/k-4-d-5/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_1.log) |
| planning_decomposition_mismatch | county_only_public_school_scope | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| query_execution_error_loop | malformed_sql_repair | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| question_or_constraint_misread | county_seat_vs_county_population_confusion | 1 | [task](../../../../tasks_mini/k-4-d-3/task_11.json) / [plan](../../../../plans_mini/k-4-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| question_or_constraint_misread | dropped_all_grades_or_exact_subject_constraint | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| question_or_constraint_misread | ignored_exclusion_constraint | 1 | [task](../../../../tasks_mini/k-4-d-4/task_6.json) / [plan](../../../../plans_mini/k-4-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| question_or_constraint_misread | school_day_vs_open_date_misread | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| wrong_source_or_scope | county_instead_of_city_denominator | 1 | [task](../../../../tasks_mini/k-4-d-2/task_5.json) / [plan](../../../../plans_mini/k-4-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_5.log) |
| wrong_source_or_scope | county_only_public_school_count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| wrong_source_or_scope | countywide_public_school_count_instead_of_city_in_county_count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_source_or_scope | final_hop_source_swap | 1 | [task](../../../../tasks_mini/k-4-d-2/task_1.json) / [plan](../../../../plans_mini/k-4-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| wrong_source_or_scope | generic_enrollment_lookup_instead_of_target_row | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| wrong_source_or_scope | irrelevant_budget_dataset | 1 | [task](../../../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../../../plans_mini/k-6-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| wrong_source_or_scope | postsecondary_year_conflation | 1 | [task](../../../../tasks_mini/k-4-d-4/task_10.json) / [plan](../../../../plans_mini/k-4-d-4/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_10.log) |
| wrong_source_or_scope | used_yearbuilt_field_instead_of_building_page | 1 | [task](../../../../tasks_mini/k-5-d-3/task_12.json) / [plan](../../../../plans_mini/k-5-d-3/task_12.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_12.log) |
| wrong_source_or_scope | wrong_branch_or_neighborhood_lookup | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| wrong_source_or_scope | wrong_dataset_version | 1 | [task](../../../../tasks_mini/k-3-d-4/task_6.json) / [plan](../../../../plans_mini/k-3-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_6.log) |
| wrong_source_or_scope | wrong_date_field_and_area_normalization | 1 | [task](../../../../tasks_mini/k-4-d-2/task_5.json) / [plan](../../../../plans_mini/k-4-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_5.log) |
| wrong_source_or_scope | wrong_neighborhood_or_park_branch | 1 | [task](../../../../tasks_mini/k-4-d-3/task_1.json) / [plan](../../../../plans_mini/k-4-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_1.log) |
| wrong_source_or_scope | wrong_school_branch | 1 | [task](../../../../tasks_mini/k-4-d-3/task_1.json) / [plan](../../../../plans_mini/k-4-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_1.log) |
| wrong_source_or_scope | wrong_terminus_city | 1 | [task](../../../../tasks_mini/k-4-d-4/task_4.json) / [plan](../../../../plans_mini/k-4-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_4.log) |
| wrong_source_or_scope | wrong_terminus_city_branch | 1 | [task](../../../../tasks_mini/k-4-d-4/task_5.json) / [plan](../../../../plans_mini/k-4-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_5.log) |
| wrong_source_or_scope | wrong_year_dataset | 1 | [task](../../../../tasks_mini/k-3-d-4/task_6.json) / [plan](../../../../plans_mini/k-3-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_6.log) |
| wrong_source_or_scope | year_mismatch | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |

## Co-occurring Failure Types

| Failure Type Set | Rows |
| --- | --- |
| evidence_available_answer_error; wrong_source_or_scope | 5 |
| computation_or_aggregation_error; tool_or_data_blocker | 2 |
| computation_or_aggregation_error; wrong_source_or_scope | 2 |
| evidence_available_answer_error | 2 |
| incomplete_evidence_not_enough_turns; question_or_constraint_misread | 2 |
| incomplete_evidence_not_enough_turns; tool_or_data_blocker | 2 |
| wrong_source_or_scope | 2 |
| computation_or_aggregation_error; evidence_available_answer_error | 1 |
| computation_or_aggregation_error; low_yield_search_loop; wrong_source_or_scope | 1 |
| computation_or_aggregation_error; query_execution_error_loop | 1 |
| evidence_available_answer_error; extraction_or_parsing_error | 1 |
| evidence_available_answer_error; query_execution_error_loop; wrong_source_or_scope | 1 |
| evidence_available_answer_error; question_or_constraint_misread | 1 |
| evidence_available_answer_error; question_or_constraint_misread; wrong_source_or_scope | 1 |
| evidence_available_answer_error; tool_or_data_blocker | 1 |
| evidence_available_answer_error; tool_or_data_blocker; wrong_source_or_scope | 1 |
| extraction_or_parsing_error | 1 |
| incomplete_evidence_not_enough_turns; query_execution_error_loop | 1 |
| incomplete_evidence_not_enough_turns; tool_or_data_blocker; wrong_source_or_scope | 1 |
| other_or_unclear; tool_or_data_blocker | 1 |
| planning_decomposition_mismatch; wrong_source_or_scope | 1 |
| tool_or_data_blocker; wrong_source_or_scope | 1 |

## Representative Evidence

- `tasks_mini/k-3-d-2/task_1.json` `tool_or_data_blocker`/`unsupported_or_oversized_data_access`: Turn 10 | "Cannot execute SQL: file is too big (1377 MB >= 500 MB limit)." The tool also advised using execute_ideal or a download-style code path.
- `tasks_mini/k-3-d-2/task_1.json` `tool_or_data_blocker`/`ideal_repair_failure`: Turn 13 | "Code repair failed: JSONDecodeError: Unterminated string starting at: line 1 column 9981 (char 9980)"; similar repair failures recur later in the log.
- `tasks_mini/k-3-d-2/task_1.json` `incomplete_evidence_not_enough_turns`/`tool_budget_exhausted`: Turn 32 | "Tool call cancelled. Tool limit reached (30/30 calls used)." Turn 33 | "Due to tool limits I estimated ~10 2023 use-of-force incidents in District 3 ..." and submitted "[5]".
- `tasks_mini/k-3-d-2/task_10.json` `wrong_source_or_scope`/`missing_city_filter`: Turn 7 | `select_match`: 0 - Reason: "The authored record filters CITY='ORLANDO' (via f.properties.CITY) in addition to NMCNTY='ORANGE COUNTY' and SCHOOLYEAR='2022-2023'. Submitted SQL counts Orange County, FL for 202...
- `tasks_mini/k-3-d-2/task_10.json` `wrong_source_or_scope`/`missing_city_filter`: Turn 8 | `select_match`: 0 - Reason: "The authored record counts private schools in city = ORLANDO (while also filtering Orange County and 2021–2022). The submitted SQL counts all private schools in Orange County, FL...

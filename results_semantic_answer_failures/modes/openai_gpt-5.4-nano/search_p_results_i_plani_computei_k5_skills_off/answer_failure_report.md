# Answer Failure Report

- Source root: `results_semantic_answer_failures`
- Event rows: 113
- Trusted event rows: 68
- Non-correct eval rows: 65
- Events excluded by validation/model-validation: 45

## Counts by Failure Type

| Failure Type | Events |
| --- | --- |
| wrong_scope_or_filter | 25 |
| tool_or_data_blocker | 11 |
| evidence_available_answer_error | 6 |
| planning_decomposition_mismatch | 6 |
| query_execution_error_loop | 5 |
| extraction_or_parsing_error | 3 |
| wrong_source_or_dataset | 3 |
| incomplete_evidence_budget_exhausted | 2 |
| incomplete_evidence_early_answer | 2 |
| question_or_constraint_misread | 2 |
| computation_or_aggregation_error | 1 |
| other_or_unclear | 1 |
| same_hop_repetition | 1 |

## Counts by Failure Type and Subtype

| Failure Type | Subtype | Events | Representative |
| --- | --- | --- | --- |
| tool_or_data_blocker | unsupported_or_oversized_data_access | 4 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| tool_or_data_blocker | malformed_tool_call | 3 | [task](../../../../tasks_mini/k-3-d-2/task_6.json) / [plan](../../../../plans_mini/k-3-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| query_execution_error_loop | repeated SQL repair JSONDecodeError | 2 | [task](../../../../tasks_mini/k-4-d-4/task_9.json) / [plan](../../../../plans_mini/k-4-d-4/task_9.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_9.log) |
| tool_or_data_blocker | tool_budget_exhausted | 2 | [task](../../../../tasks_mini/k-4-d-4/task_8.json) / [plan](../../../../plans_mini/k-4-d-4/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_8.log) |
| computation_or_aggregation_error | miscomputed the average and rounded the wrong value | 1 | [task](../../../../tasks_mini/k-5-d-2/task_7.json) / [plan](../../../../plans_mini/k-5-d-2/task_7.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_7.log) |
| evidence_available_answer_error | stopped_at_employer_name | 1 | [task](../../../../tasks_mini/k-5-d-2/task_8.json) / [plan](../../../../plans_mini/k-5-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_8.log) |
| evidence_available_answer_error | submitted 1959 despite reasoning for 1916 | 1 | [task](../../../../tasks_mini/k-5-d-3/task_3.json) / [plan](../../../../plans_mini/k-5-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| evidence_available_answer_error | submitted Westmoreland County instead of Accomack County | 1 | [task](../../../../tasks_mini/k-4-d-3/task_3.json) / [plan](../../../../plans_mini/k-4-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_3.log) |
| evidence_available_answer_error | submitted school name instead of bridge | 1 | [task](../../../../tasks_mini/k-3-d-4/task_5.json) / [plan](../../../../plans_mini/k-3-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_5.log) |
| evidence_available_answer_error | submitted_1907_instead_of_1858 | 1 | [task](../../../../tasks_mini/k-5-d-4/task_3.json) / [plan](../../../../plans_mini/k-5-d-4/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_3.log) |
| evidence_available_answer_error | surface_form_mismatch | 1 | [task](../../../../tasks_mini/k-3-d-5/task_1.json) / [plan](../../../../plans_mini/k-3-d-5/task_1.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-5/task_1.log) |
| extraction_or_parsing_error | public-school KML filter/path returned zero rows | 1 | [task](../../../../tasks_mini/k-3-d-4/task_4.json) / [plan](../../../../plans_mini/k-3-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| extraction_or_parsing_error | selected birthplace instead of based-in location | 1 | [task](../../../../tasks_mini/k-5-d-2/task_4.json) / [plan](../../../../plans_mini/k-5-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_4.log) |
| extraction_or_parsing_error | wrong_field_model | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| incomplete_evidence_budget_exhausted | hard_timeout | 1 | [task](../../../../tasks_mini/k-3-d-4/task_1.json) / [plan](../../../../plans_mini/k-3-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_1.log) |
| incomplete_evidence_budget_exhausted | timeout before downstream verification | 1 | [task](../../../../tasks_mini/k-4-d-4/task_5.json) / [plan](../../../../plans_mini/k-4-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_5.log) |
| incomplete_evidence_early_answer | placeholder_submission | 1 | [task](../../../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../../../plans_mini/k-6-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| incomplete_evidence_early_answer | submitted_intermediate_lookup | 1 | [task](../../../../tasks_mini/k-4-d-4/task_11.json) / [plan](../../../../plans_mini/k-4-d-4/task_11.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_11.log) |
| other_or_unclear | incorrect NYC founding year | 1 | [task](../../../../tasks_mini/k-4-d-2/task_10.json) / [plan](../../../../plans_mini/k-4-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_10.log) |
| planning_decomposition_mismatch | heuristic substring count instead of structured county-intersection computation | 1 | [task](../../../../tasks_mini/k-6-d-3/task_5.json) / [plan](../../../../plans_mini/k-6-d-3/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_5.log) |
| planning_decomposition_mismatch | non-equivalent county-count queries and placeholder intersection query | 1 | [task](../../../../tasks_mini/k-5-d-4/task_8.json) / [plan](../../../../plans_mini/k-5-d-4/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_8.log) |
| planning_decomposition_mismatch | schema probing before planned aggregation | 1 | [task](../../../../tasks_mini/k-4-d-4/task_5.json) / [plan](../../../../plans_mini/k-4-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_5.log) |
| planning_decomposition_mismatch | substituted_wrong_interpreter_chain | 1 | [task](../../../../tasks_mini/k-4-d-4/task_8.json) / [plan](../../../../plans_mini/k-4-d-4/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_8.log) |
| planning_decomposition_mismatch | used department-description and single-year queries instead of the authored department-number 2019-2021 intersection path | 1 | [task](../../../../tasks_mini/k-5-d-3/task_8.json) / [plan](../../../../plans_mini/k-5-d-3/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_8.log) |
| planning_decomposition_mismatch | wrong_terminus_branch | 1 | [task](../../../../tasks_mini/k-6-d-2/task_3.json) / [plan](../../../../plans_mini/k-6-d-2/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_3.log) |
| query_execution_error_loop | jsondecode_error_in_sql_repair | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| query_execution_error_loop | repeated JSONDecodeError in query_ideal repair | 1 | [task](../../../../tasks_mini/k-4-d-4/task_2.json) / [plan](../../../../plans_mini/k-4-d-4/task_2.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_2.log) |
| query_execution_error_loop | sql_repair_failures | 1 | [task](../../../../tasks_mini/k-5-d-3/task_12.json) / [plan](../../../../plans_mini/k-5-d-3/task_12.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_12.log) |
| question_or_constraint_misread | comparison_reversed | 1 | [task](../../../../tasks_mini/k-6-d-2/task_3.json) / [plan](../../../../plans_mini/k-6-d-2/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_3.log) |
| question_or_constraint_misread | returned a person name instead of the required university answer | 1 | [task](../../../../tasks_mini/k-5-d-3/task_8.json) / [plan](../../../../plans_mini/k-5-d-3/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_8.log) |
| same_hop_repetition | repeated_single_year_ward_counts | 1 | [task](../../../../tasks_mini/k-3-d-4/task_1.json) / [plan](../../../../plans_mini/k-3-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_1.log) |
| tool_or_data_blocker | data_source_missing_or_unavailable | 1 | [task](../../../../tasks_mini/k-5-d-4/task_8.json) / [plan](../../../../plans_mini/k-5-d-4/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_8.log) |
| tool_or_data_blocker | ideal_repair_failure | 1 | [task](../../../../tasks_mini/k-4-d-3/task_2.json) / [plan](../../../../plans_mini/k-4-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| wrong_scope_or_filter | 2016_only_obesity_query | 1 | [task](../../../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../../../plans_mini/k-6-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| wrong_scope_or_filter | NTA_NAME neighborhood matching instead of exact LOCATION_CODE and NTA-code filtering | 1 | [task](../../../../tasks_mini/k-4-d-3/task_2.json) / [plan](../../../../plans_mini/k-4-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| wrong_scope_or_filter | broad_keyword_police_filters | 1 | [task](../../../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../../../plans_mini/k-6-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| wrong_scope_or_filter | broader police filter and cost center condition instead of exact department filter | 1 | [task](../../../../tasks_mini/k-5-d-2/task_7.json) / [plan](../../../../plans_mini/k-5-d-2/task_7.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_7.log) |
| wrong_scope_or_filter | broader two-school scope | 1 | [task](../../../../tasks_mini/k-4-d-2/task_10.json) / [plan](../../../../plans_mini/k-4-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_10.log) |
| wrong_scope_or_filter | confused monument county with Wallops Flight Facility county | 1 | [task](../../../../tasks_mini/k-4-d-3/task_3.json) / [plan](../../../../plans_mini/k-4-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_3.log) |
| wrong_scope_or_filter | county_only_instead_of_chicago_in_county | 1 | [task](../../../../tasks_mini/k-3-d-2/task_7.json) / [plan](../../../../plans_mini/k-3-d-2/task_7.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_7.log) |
| wrong_scope_or_filter | drifted_to_statewide_then_still_missed_city_filter | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_scope_or_filter | extra Ward 2 filter on the 2020 count | 1 | [task](../../../../tasks_mini/k-5-d-1/task_3.json) / [plan](../../../../plans_mini/k-5-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-1/task_3.log) |
| wrong_scope_or_filter | missing Boston restriction in private-school count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| wrong_scope_or_filter | omitted authored filters in school ranking | 1 | [task](../../../../tasks_mini/k-3-d-4/task_5.json) / [plan](../../../../plans_mini/k-3-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_5.log) |
| wrong_scope_or_filter | omitted_detroit_city_filter | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_scope_or_filter | omitted_required_filter_and_used_proxy_grouping | 1 | [task](../../../../tasks_mini/k-4-d-5/task_4.json) / [plan](../../../../plans_mini/k-4-d-5/task_4.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_4.log) |
| wrong_scope_or_filter | over-restricted to precinct 44 in final count | 1 | [task](../../../../tasks_mini/k-4-d-1/task_3.json) / [plan](../../../../plans_mini/k-4-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_3.log) |
| wrong_scope_or_filter | single-year scope and malformed filter | 1 | [task](../../../../tasks_mini/k-4-d-4/task_9.json) / [plan](../../../../plans_mini/k-4-d-4/task_9.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_9.log) |
| wrong_scope_or_filter | used a generic Lansing CBSA lookup instead of the school-year-specific authored computation | 1 | [task](../../../../tasks_mini/k-3-d-2/task_6.json) / [plan](../../../../plans_mini/k-3-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| wrong_scope_or_filter | used max/frequency instead of the elementary-school Level 1 filter | 1 | [task](../../../../tasks_mini/k-4-d-4/task_2.json) / [plan](../../../../plans_mini/k-4-d-4/task_2.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_2.log) |
| wrong_scope_or_filter | wrong county filters and missing program-year filter | 1 | [task](../../../../tasks_mini/k-5-d-4/task_5.json) / [plan](../../../../plans_mini/k-5-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_5.log) |
| wrong_scope_or_filter | wrong county set and census filter pattern | 1 | [task](../../../../tasks_mini/k-5-d-4/task_8.json) / [plan](../../../../plans_mini/k-5-d-4/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_8.log) |
| wrong_scope_or_filter | wrong founder/county pair | 1 | [task](../../../../tasks_mini/k-4-d-4/task_12.json) / [plan](../../../../plans_mini/k-4-d-4/task_12.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_12.log) |
| wrong_scope_or_filter | wrong honoree branch | 1 | [task](../../../../tasks_mini/k-4-d-4/task_13.json) / [plan](../../../../plans_mini/k-4-d-4/task_13.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_13.log) |
| wrong_scope_or_filter | wrong_branch_community_area_chain | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| wrong_scope_or_filter | wrong_branch_selection | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| wrong_scope_or_filter | wrong_county_lookup | 1 | [task](../../../../tasks_mini/k-6-d-2/task_3.json) / [plan](../../../../plans_mini/k-6-d-2/task_3.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_3.log) |
| wrong_scope_or_filter | wrong_field_threshold | 1 | [task](../../../../tasks_mini/k-5-d-2/task_8.json) / [plan](../../../../plans_mini/k-5-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_8.log) |
| wrong_source_or_dataset | 500-cities_vs_city-page | 1 | [task](../../../../tasks_mini/k-5-d-2/task_8.json) / [plan](../../../../plans_mini/k-5-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_8.log) |
| wrong_source_or_dataset | missing_neighborhood_field | 1 | [task](../../../../tasks_mini/k-3-d-5/task_1.json) / [plan](../../../../plans_mini/k-3-d-5/task_1.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-5/task_1.log) |
| wrong_source_or_dataset | used the 2019-20 postsecondary dataset instead of the task-specified Polk County postsecondary count | 1 | [task](../../../../tasks_mini/k-4-d-4/task_10.json) / [plan](../../../../plans_mini/k-4-d-4/task_10.json) / [log](../../../../logs/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_10.log) |

## Co-occurring Failure Types

| Failure Type Set | Rows |
| --- | --- |
| tool_or_data_blocker; wrong_scope_or_filter | 6 |
| wrong_scope_or_filter | 5 |
| query_execution_error_loop; wrong_scope_or_filter | 3 |
| evidence_available_answer_error | 2 |
| evidence_available_answer_error; wrong_scope_or_filter | 2 |
| extraction_or_parsing_error | 2 |
| planning_decomposition_mismatch; tool_or_data_blocker | 2 |
| query_execution_error_loop | 2 |
| computation_or_aggregation_error; wrong_scope_or_filter | 1 |
| evidence_available_answer_error; wrong_scope_or_filter; wrong_source_or_dataset | 1 |
| evidence_available_answer_error; wrong_source_or_dataset | 1 |
| extraction_or_parsing_error; tool_or_data_blocker | 1 |
| incomplete_evidence_budget_exhausted; planning_decomposition_mismatch | 1 |
| incomplete_evidence_budget_exhausted; same_hop_repetition | 1 |
| incomplete_evidence_early_answer | 1 |
| incomplete_evidence_early_answer; wrong_scope_or_filter | 1 |
| other_or_unclear; wrong_scope_or_filter | 1 |
| planning_decomposition_mismatch; question_or_constraint_misread | 1 |
| planning_decomposition_mismatch; question_or_constraint_misread; wrong_scope_or_filter | 1 |
| planning_decomposition_mismatch; tool_or_data_blocker; wrong_scope_or_filter | 1 |
| tool_or_data_blocker | 1 |
| wrong_source_or_dataset | 1 |

## Representative Evidence

- `tasks_mini/k-3-d-2/task_5.json` `extraction_or_parsing_error`/`wrong_field_model`: Turn 4 | query_ideal({"dataset_id": "public-school-locations-current-23297", "file_path": "files/data.txt", "sql": "SELECT t.\"County Name\" as county, COUNT(*) as public_school_count FROM t WHERE t.\"School Year\" =...
- `tasks_mini/k-3-d-2/task_5.json` `tool_or_data_blocker`/`unsupported_or_oversized_data_access`: Turn 14 | parse_xml_records({"dataset_id": "school-district-office-locations-current-c8f9d", "file_path": "files/data.txt", "record_tag": "Placemark", "fields": ["SCHOOLYEAR", "CNTY", "NMCNTY"], "group_by": ["NMCNTY"]...
- `tasks_mini/k-3-d-2/task_6.json` `wrong_scope_or_filter`/`used a generic Lansing CBSA lookup instead of the school-year-specific authored computation`: Turn 5 | query_ideal({"dataset_id": "postsecondary-school-locations-current-5a74c", "file_path": "files/Postsecondary_School_Locations_Current_-3631565628879840217.txt", "sql": "SELECT DISTINCT \"CBSA\", \"NMCBSA\" FR...
- `tasks_mini/k-3-d-2/task_6.json` `tool_or_data_blocker`/`malformed_tool_call`: Turn 5 | Tool logical error (status=error): {"success": false, "error": "SQL repair failed: JSONDecodeError: Unterminated string starting at: line 1 column 558 (char 557)"}
- `tasks_mini/k-3-d-2/task_7.json` `wrong_scope_or_filter`/`county_only_instead_of_chicago_in_county`: Turn 3 | Model response #3 [role=assistant block=1 tool_use] query_ideal({"dataset_id": "private-school-locations-current-f7d96", "file_path": "files/data-FGgJBu.txt", "sql": "SELECT \"County\" as county, COUNT(*) as...

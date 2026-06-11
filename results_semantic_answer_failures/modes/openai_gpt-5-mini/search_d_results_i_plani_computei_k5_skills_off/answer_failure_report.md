# Answer Failure Report

- Source root: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_answer_failures`
- Event rows: 88
- Trusted event rows: 88
- Non-correct eval rows: 52

## Counts by Failure Type

| Failure Type | Events |
| --- | --- |
| wrong_scope_or_filter | 33 |
| evidence_available_answer_error | 20 |
| tool_or_data_blocker | 18 |
| incomplete_evidence_budget_exhausted | 7 |
| extraction_or_parsing_error | 3 |
| planning_decomposition_mismatch | 2 |
| computation_or_aggregation_error | 1 |
| incomplete_evidence_early_answer | 1 |
| query_execution_error_loop | 1 |
| schema_or_shape_inspection_loop | 1 |
| semantic_or_gold_label_issue | 1 |

## Counts by Failure Type and Subtype

| Failure Type | Subtype | Events | Representative |
| --- | --- | --- | --- |
| tool_or_data_blocker | tool_budget_exhausted | 9 | [task](../../../../tasks_mini/k-3-d-2/task_7.json) / [plan](../../../../plans_mini/k-3-d-2/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_7.log) |
| tool_or_data_blocker | unsupported_or_oversized_data_access | 7 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| incomplete_evidence_budget_exhausted | tool_budget_exhausted | 3 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| computation_or_aggregation_error | off-by-one threshold selection | 1 | [task](../../../../tasks_mini/k-4-d-1/task_1.json) / [plan](../../../../plans_mini/k-4-d-1/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_1.log) |
| evidence_available_answer_error | 09_08_vs_10_28 | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| evidence_available_answer_error | Dallas used instead of Travis | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| evidence_available_answer_error | answered city instead of county | 1 | [task](../../../../tasks_mini/k-5-d-3/task_11.json) / [plan](../../../../plans_mini/k-5-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_11.log) |
| evidence_available_answer_error | final answer selected wrong value | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| evidence_available_answer_error | picked Adam=40 instead of Edward=52 | 1 | [task](../../../../tasks_mini/k-5-d-1/task_2.json) / [plan](../../../../plans_mini/k-5-d-1/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-1/task_2.log) |
| evidence_available_answer_error | picked_1790_from_partial_comparison | 1 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| evidence_available_answer_error | replaced correct district count 6 with unrelated grep count 20 | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| evidence_available_answer_error | selected 1795 instead of 1789 | 1 | [task](../../../../tasks_mini/k-5-d-4/task_1.json) / [plan](../../../../plans_mini/k-5-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_1.log) |
| evidence_available_answer_error | selected wrong final answer | 1 | [task](../../../../tasks_mini/k-5-d-3/task_14.json) / [plan](../../../../plans_mini/k-5-d-3/task_14.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_14.log) |
| evidence_available_answer_error | selected_davenport_2020_population_instead_of_scott_county_value | 1 | [task](../../../../tasks_mini/k-4-d-3/task_11.json) / [plan](../../../../plans_mini/k-4-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| evidence_available_answer_error | selected_wrong_birth_year | 1 | [task](../../../../tasks_mini/k-5-d-2/task_10.json) / [plan](../../../../plans_mini/k-5-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_10.log) |
| evidence_available_answer_error | submitted 542 instead of 14 | 1 | [task](../../../../tasks_mini/k-5-d-1/task_4.json) / [plan](../../../../plans_mini/k-5-d-1/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-1/task_4.log) |
| evidence_available_answer_error | submitted_zero_after_dead_end | 1 | [task](../../../../tasks_mini/k-4-d-1/task_2.json) / [plan](../../../../plans_mini/k-4-d-1/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_2.log) |
| evidence_available_answer_error | used grep match_count 20 instead of validated private-school count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| evidence_available_answer_error | used truncated grep count instead of earlier correct count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_10.json) / [plan](../../../../plans_mini/k-3-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| evidence_available_answer_error | wrong final county/count | 1 | [task](../../../../tasks_mini/k-6-d-3/task_5.json) / [plan](../../../../plans_mini/k-6-d-3/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_5.log) |
| evidence_available_answer_error | wrong final entity: John Brown instead of James Brown | 1 | [task](../../../../tasks_mini/k-4-d-4/task_13.json) / [plan](../../../../plans_mini/k-4-d-4/task_13.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_13.log) |
| evidence_available_answer_error | wrong_final_park_answer | 1 | [task](../../../../tasks_mini/k-4-d-3/task_1.json) / [plan](../../../../plans_mini/k-4-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_1.log) |
| evidence_available_answer_error | wrong_name_selected_at_submission | 1 | [task](../../../../tasks_mini/k-4-d-3/task_6.json) / [plan](../../../../plans_mini/k-4-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| evidence_available_answer_error | wrong_output_format | 1 | [task](../../../../tasks_mini/k-4-d-2/task_2.json) / [plan](../../../../plans_mini/k-4-d-2/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_2.log) |
| extraction_or_parsing_error | confused museum establishment year with first-purpose-built-structure year | 1 | [task](../../../../tasks_mini/k-3-d-4/task_7.json) / [plan](../../../../plans_mini/k-3-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_7.log) |
| extraction_or_parsing_error | wrong enrollment value from correct Pullman row | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| extraction_or_parsing_error | wrong_year_source | 1 | [task](../../../../tasks_mini/k-5-d-3/task_12.json) / [plan](../../../../plans_mini/k-5-d-3/task_12.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_12.log) |
| incomplete_evidence_budget_exhausted | 30-call tool limit exhausted before district-office verification | 1 | [task](../../../../tasks_mini/k-3-d-2/task_6.json) / [plan](../../../../plans_mini/k-3-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| incomplete_evidence_budget_exhausted | hard timeout | 1 | [task](../../../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../../../plans_mini/k-6-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| incomplete_evidence_budget_exhausted | tool budget exhausted before exact extraction | 1 | [task](../../../../tasks_mini/k-3-d-1/task_1.json) / [plan](../../../../plans_mini/k-3-d-1/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-1/task_1.log) |
| incomplete_evidence_budget_exhausted | turn_or_time_budget_exhausted | 1 | [task](../../../../tasks_mini/k-5-d-4/task_2.json) / [plan](../../../../plans_mini/k-5-d-4/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) |
| incomplete_evidence_early_answer | submitted before comparing the full candidate set | 1 | [task](../../../../tasks_mini/k-4-d-3/task_2.json) / [plan](../../../../plans_mini/k-4-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| planning_decomposition_mismatch | switched_to_arrest_charge_path | 1 | [task](../../../../tasks_mini/k-4-d-1/task_2.json) / [plan](../../../../plans_mini/k-4-d-1/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_2.log) |
| planning_decomposition_mismatch | wrong county-ranking strategy | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| query_execution_error_loop | repeated binder errors on missing columns | 1 | [task](../../../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../../../plans_mini/k-6-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| schema_or_shape_inspection_loop | wrong column/schema | 1 | [task](../../../../tasks_mini/k-4-d-2/task_1.json) / [plan](../../../../plans_mini/k-4-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| semantic_or_gold_label_issue | mixed arcade-year vs city-year fact | 1 | [task](../../../../tasks_mini/k-4-d-5/task_1.json) / [plan](../../../../plans_mini/k-4-d-5/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_1.log) |
| tool_or_data_blocker | ideal_repair_failure | 1 | [task](../../../../tasks_mini/k-4-d-4/task_11.json) / [plan](../../../../plans_mini/k-4-d-4/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_11.log) |
| tool_or_data_blocker | malformed_tool_call | 1 | [task](../../../../tasks_mini/k-4-d-4/task_11.json) / [plan](../../../../plans_mini/k-4-d-4/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_11.log) |
| wrong_scope_or_filter | Bedford Village-only VADIR checks | 1 | [task](../../../../tasks_mini/k-4-d-3/task_2.json) / [plan](../../../../plans_mini/k-4-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| wrong_scope_or_filter | K003-only class-size checks | 1 | [task](../../../../tasks_mini/k-4-d-3/task_2.json) / [plan](../../../../plans_mini/k-4-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| wrong_scope_or_filter | added precinct=44 filter to the final 2022 Bronx INSIDE count | 1 | [task](../../../../tasks_mini/k-4-d-1/task_3.json) / [plan](../../../../plans_mini/k-4-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_3.log) |
| wrong_scope_or_filter | anchored on Harold Washington Library Center and the Loop instead of Sulzer Regional Library and Lincoln Square | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| wrong_scope_or_filter | county_instead_of_city_scope | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| wrong_scope_or_filter | current-year-to-date complaints dataset pivot | 1 | [task](../../../../tasks_mini/k-3-d-1/task_1.json) / [plan](../../../../plans_mini/k-3-d-1/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-1/task_1.log) |
| wrong_scope_or_filter | current_dataset_version | 1 | [task](../../../../tasks_mini/k-4-d-4/task_10.json) / [plan](../../../../plans_mini/k-4-d-4/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_10.log) |
| wrong_scope_or_filter | dataset_drift | 1 | [task](../../../../tasks_mini/k-4-d-4/task_11.json) / [plan](../../../../plans_mini/k-4-d-4/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_11.log) |
| wrong_scope_or_filter | dc street-sweeping lookup drifted to Chicago dataset | 1 | [task](../../../../tasks_mini/k-5-d-3/task_10.json) / [plan](../../../../plans_mini/k-5-d-3/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_10.log) |
| wrong_scope_or_filter | maryland-only income dataset instead of U.S.-wide county ranking source | 1 | [task](../../../../tasks_mini/k-3-d-4/task_1.json) / [plan](../../../../plans_mini/k-3-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_1.log) |
| wrong_scope_or_filter | non_equivalent_query_shape | 1 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| wrong_scope_or_filter | off_plan_2018_2019_locations_file | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| wrong_scope_or_filter | public-school dataset family mismatch | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| wrong_scope_or_filter | searched_wrong_charge_term | 1 | [task](../../../../tasks_mini/k-4-d-1/task_2.json) / [plan](../../../../plans_mini/k-4-d-1/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_2.log) |
| wrong_scope_or_filter | state_level_counts_instead_of_county_level_intersection | 1 | [task](../../../../tasks_mini/k-5-d-3/task_13.json) / [plan](../../../../plans_mini/k-5-d-3/task_13.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_13.log) |
| wrong_scope_or_filter | submitted Santa Monica | 1 | [task](../../../../tasks_mini/k-4-d-4/task_5.json) / [plan](../../../../plans_mini/k-4-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_5.log) |
| wrong_scope_or_filter | switched to Deb Haaland/UNM instead of Doug Burgum/NDSU path | 1 | [task](../../../../tasks_mini/k-6-d-3/task_2.json) / [plan](../../../../plans_mini/k-6-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_2.log) |
| wrong_scope_or_filter | used 2021-22/current private and postsecondary sources | 1 | [task](../../../../tasks_mini/k-3-d-4/task_6.json) / [plan](../../../../plans_mini/k-3-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_6.log) |
| wrong_scope_or_filter | used NMCBSA-based matching instead of CITY+CBSA filters | 1 | [task](../../../../tasks_mini/k-3-d-2/task_6.json) / [plan](../../../../plans_mini/k-3-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| wrong_scope_or_filter | used arrest dataset instead of crime dataset | 1 | [task](../../../../tasks_mini/k-4-d-1/task_1.json) / [plan](../../../../plans_mini/k-4-d-1/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_1.log) |
| wrong_scope_or_filter | used current dataset instead of task-specified 2019-20 source | 1 | [task](../../../../tasks_mini/k-6-d-3/task_4.json) / [plan](../../../../plans_mini/k-6-d-3/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_4.log) |
| wrong_scope_or_filter | used parking-violations instead of moving-violations dataset | 1 | [task](../../../../tasks_mini/k-6-d-3/task_2.json) / [plan](../../../../plans_mini/k-6-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_2.log) |
| wrong_scope_or_filter | used the 2008-2012 socioeconomic indicators dataset instead of the public-health-indicators dataset named in the task plan | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| wrong_scope_or_filter | wrong comparison target and dataset branch | 1 | [task](../../../../tasks_mini/k-5-d-4/task_2.json) / [plan](../../../../plans_mini/k-5-d-4/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) |
| wrong_scope_or_filter | wrong dataset | 1 | [task](../../../../tasks_mini/k-4-d-5/task_3.json) / [plan](../../../../plans_mini/k-4-d-5/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_3.log) |
| wrong_scope_or_filter | wrong district branch / countywide district-average scope | 1 | [task](../../../../tasks_mini/k-5-d-3/task_2.json) / [plan](../../../../plans_mini/k-5-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_2.log) |
| wrong_scope_or_filter | wrong entity branch | 1 | [task](../../../../tasks_mini/k-5-d-3/task_9.json) / [plan](../../../../plans_mini/k-5-d-3/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_9.log) |
| wrong_scope_or_filter | wrong geography/filter combination | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_scope_or_filter | wrong school/person chain led to Baltimore answer | 1 | [task](../../../../tasks_mini/k-5-d-3/task_10.json) / [plan](../../../../plans_mini/k-5-d-3/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_10.log) |
| wrong_scope_or_filter | wrong terminus pair | 1 | [task](../../../../tasks_mini/k-4-d-4/task_5.json) / [plan](../../../../plans_mini/k-4-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_5.log) |
| wrong_scope_or_filter | wrong_council_district_or_scope | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| wrong_scope_or_filter | wrong_school_neighborhood_branch | 1 | [task](../../../../tasks_mini/k-4-d-3/task_1.json) / [plan](../../../../plans_mini/k-4-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_1.log) |
| wrong_scope_or_filter | wrong_year_or_filter | 1 | [task](../../../../tasks_mini/k-4-d-2/task_2.json) / [plan](../../../../plans_mini/k-4-d-2/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_2.log) |

## Co-occurring Failure Types

| Failure Type Set | Rows |
| --- | --- |
| wrong_scope_or_filter | 12 |
| evidence_available_answer_error | 10 |
| tool_or_data_blocker; wrong_scope_or_filter | 4 |
| evidence_available_answer_error; tool_or_data_blocker; wrong_scope_or_filter | 3 |
| tool_or_data_blocker | 3 |
| evidence_available_answer_error; tool_or_data_blocker | 2 |
| evidence_available_answer_error; wrong_scope_or_filter | 2 |
| extraction_or_parsing_error | 2 |
| incomplete_evidence_budget_exhausted; tool_or_data_blocker; wrong_scope_or_filter | 2 |
| incomplete_evidence_budget_exhausted; wrong_scope_or_filter | 2 |
| computation_or_aggregation_error; wrong_scope_or_filter | 1 |
| evidence_available_answer_error; planning_decomposition_mismatch | 1 |
| evidence_available_answer_error; planning_decomposition_mismatch; wrong_scope_or_filter | 1 |
| extraction_or_parsing_error; tool_or_data_blocker | 1 |
| incomplete_evidence_budget_exhausted | 1 |
| incomplete_evidence_budget_exhausted; query_execution_error_loop | 1 |
| incomplete_evidence_budget_exhausted; tool_or_data_blocker | 1 |
| incomplete_evidence_early_answer; wrong_scope_or_filter | 1 |
| schema_or_shape_inspection_loop; tool_or_data_blocker | 1 |
| semantic_or_gold_label_issue | 1 |

## Representative Evidence

- `tasks_mini/k-2-d-3/task_1.json` `wrong_scope_or_filter`/`non_equivalent_query_shape`: Turn 4 | Model response #4 [role=assistant block=1 tool_use] query_ideal({"dataset_id": "nopd-use-of-force-incidents", "file_path": "files/rows.txt", "sql": "SELECT \"Division\", COUNT(*) AS cnt\nFROM t\nWHERE strftim...
- `tasks_mini/k-2-d-3/task_1.json` `tool_or_data_blocker`/`unsupported_or_oversized_data_access`: Turn 15 | Tool result: {"dataset_id": "apd-searches-by-type", "file_path": "files/rows.txt", "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/apd-searches-by-type/files/rows.txt", "columns": ["Sector", "cnt"], "rows": [...
- `tasks_mini/k-2-d-3/task_1.json` `evidence_available_answer_error`/`picked_1790_from_partial_comparison`: Turn 4 | Model response #4 [role=assistant block=1 tool_use] query_ideal({"dataset_id": "nopd-use-of-force-incidents", "file_path": "files/rows.txt", "sql": "SELECT \"Division\", COUNT(*) AS cnt\nFROM t\nWHERE strftim...
- `tasks_mini/k-3-d-1/task_1.json` `tool_or_data_blocker`/`unsupported_or_oversized_data_access`: Turn 12 | Tool logical error (status=error): {"success": false, "error": "Cannot execute SQL: file is too big (2891 MB >= 500 MB limit).", "dataset_id": "nypd-complaint-data-historic", "file_path": "files/rows.txt", "...
- `tasks_mini/k-3-d-1/task_1.json` `wrong_scope_or_filter`/`current-year-to-date complaints dataset pivot`: Turn 27 | Model response #27 [role=assistant block=1 tool_use] query_ideal({"dataset_id": "nypd-complaint-data-current-year-to-date", "file_path": "files/rows.txt", "sql": "SELECT \"OFNS_DESC\" AS offense, COUNT(*) AS...

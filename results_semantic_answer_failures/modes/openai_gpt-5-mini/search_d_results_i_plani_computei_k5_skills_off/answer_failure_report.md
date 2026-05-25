# Answer Failure Report

- Source root: `results_semantic_answer_failures`
- Event rows: 90
- Trusted event rows: 73
- Non-correct eval rows: 52
- Events excluded by validation/model-validation: 17

## Counts by Failure Type

| Failure Type | Events |
| --- | --- |
| wrong_scope_or_filter | 20 |
| evidence_available_answer_error | 17 |
| tool_or_data_blocker | 15 |
| wrong_source_or_dataset | 10 |
| incomplete_evidence_budget_exhausted | 7 |
| extraction_or_parsing_error | 1 |
| incomplete_evidence_early_answer | 1 |
| planning_decomposition_mismatch | 1 |
| query_execution_error_loop | 1 |

## Counts by Failure Type and Subtype

| Failure Type | Subtype | Events | Representative |
| --- | --- | --- | --- |
| tool_or_data_blocker | tool_budget_exhausted | 8 | [task](../../../../tasks_mini/k-3-d-2/task_7.json) / [plan](../../../../plans_mini/k-3-d-2/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_7.log) |
| tool_or_data_blocker | unsupported_or_oversized_data_access | 7 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| incomplete_evidence_budget_exhausted | tool_budget_exhausted | 3 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| evidence_available_answer_error | 09_08_vs_10_28 | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| evidence_available_answer_error | Dallas used instead of Travis | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| evidence_available_answer_error | answered city instead of county | 1 | [task](../../../../tasks_mini/k-5-d-3/task_11.json) / [plan](../../../../plans_mini/k-5-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_11.log) |
| evidence_available_answer_error | final answer selected wrong value | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| evidence_available_answer_error | picked Adam=40 instead of Edward=52 | 1 | [task](../../../../tasks_mini/k-5-d-1/task_2.json) / [plan](../../../../plans_mini/k-5-d-1/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-1/task_2.log) |
| evidence_available_answer_error | picked_1790_from_partial_comparison | 1 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| evidence_available_answer_error | replaced correct district count 6 with unrelated grep count 20 | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| evidence_available_answer_error | selected 1795 instead of 1789 | 1 | [task](../../../../tasks_mini/k-5-d-4/task_1.json) / [plan](../../../../plans_mini/k-5-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_1.log) |
| evidence_available_answer_error | selected_davenport_2020_population_instead_of_scott_county_value | 1 | [task](../../../../tasks_mini/k-4-d-3/task_11.json) / [plan](../../../../plans_mini/k-4-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| evidence_available_answer_error | selected_wrong_birth_year | 1 | [task](../../../../tasks_mini/k-5-d-2/task_10.json) / [plan](../../../../plans_mini/k-5-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_10.log) |
| evidence_available_answer_error | submitted 542 instead of 14 | 1 | [task](../../../../tasks_mini/k-5-d-1/task_4.json) / [plan](../../../../plans_mini/k-5-d-1/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-1/task_4.log) |
| evidence_available_answer_error | used grep match_count 20 instead of validated private-school count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| evidence_available_answer_error | used truncated grep count instead of earlier correct count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_10.json) / [plan](../../../../plans_mini/k-3-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| evidence_available_answer_error | wrong final county/count | 1 | [task](../../../../tasks_mini/k-6-d-3/task_5.json) / [plan](../../../../plans_mini/k-6-d-3/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_5.log) |
| evidence_available_answer_error | wrong final entity: John Brown instead of James Brown | 1 | [task](../../../../tasks_mini/k-4-d-4/task_13.json) / [plan](../../../../plans_mini/k-4-d-4/task_13.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_13.log) |
| evidence_available_answer_error | wrong_name_selected_at_submission | 1 | [task](../../../../tasks_mini/k-4-d-3/task_6.json) / [plan](../../../../plans_mini/k-4-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| evidence_available_answer_error | wrong_output_format | 1 | [task](../../../../tasks_mini/k-4-d-2/task_2.json) / [plan](../../../../plans_mini/k-4-d-2/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_2.log) |
| extraction_or_parsing_error | wrong final enrollment answer | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| incomplete_evidence_budget_exhausted | 30-call tool limit exhausted before district-office verification | 1 | [task](../../../../tasks_mini/k-3-d-2/task_6.json) / [plan](../../../../plans_mini/k-3-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| incomplete_evidence_budget_exhausted | hard timeout | 1 | [task](../../../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../../../plans_mini/k-6-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| incomplete_evidence_budget_exhausted | tool budget exhausted before exact extraction | 1 | [task](../../../../tasks_mini/k-3-d-1/task_1.json) / [plan](../../../../plans_mini/k-3-d-1/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-1/task_1.log) |
| incomplete_evidence_budget_exhausted | turn_or_time_budget_exhausted | 1 | [task](../../../../tasks_mini/k-5-d-4/task_2.json) / [plan](../../../../plans_mini/k-5-d-4/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) |
| incomplete_evidence_early_answer | submitted before comparing the full candidate set | 1 | [task](../../../../tasks_mini/k-4-d-3/task_2.json) / [plan](../../../../plans_mini/k-4-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| planning_decomposition_mismatch | wrong county-ranking strategy | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| query_execution_error_loop | repeated binder errors on missing columns | 1 | [task](../../../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../../../plans_mini/k-6-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| wrong_scope_or_filter | added_precinct_44_filter_to_final_2022_bronx_inside_count | 1 | [task](../../../../tasks_mini/k-4-d-1/task_3.json) / [plan](../../../../plans_mini/k-4-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_3.log) |
| wrong_scope_or_filter | anchored_on_harold_washington_and_loop_instead_of_sulzer_and_lincoln_square | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| wrong_scope_or_filter | bedford_village_only_vadir_checks | 1 | [task](../../../../tasks_mini/k-4-d-3/task_2.json) / [plan](../../../../plans_mini/k-4-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| wrong_scope_or_filter | county_instead_of_city_scope | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| wrong_scope_or_filter | k003_only_class_size_checks | 1 | [task](../../../../tasks_mini/k-4-d-3/task_2.json) / [plan](../../../../plans_mini/k-4-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| wrong_scope_or_filter | nmcbsa_matching_instead_of_city_cbsa_filters | 1 | [task](../../../../tasks_mini/k-3-d-2/task_6.json) / [plan](../../../../plans_mini/k-3-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| wrong_scope_or_filter | non_equivalent_query_shape | 1 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| wrong_scope_or_filter | propagated_wrong_target_into_final_answer | 1 | [task](../../../../tasks_mini/k-4-d-1/task_1.json) / [plan](../../../../plans_mini/k-4-d-1/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_1.log) |
| wrong_scope_or_filter | state_level_counts_instead_of_county_level_intersection | 1 | [task](../../../../tasks_mini/k-5-d-3/task_13.json) / [plan](../../../../plans_mini/k-5-d-3/task_13.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_13.log) |
| wrong_scope_or_filter | submitted_santa_monica | 1 | [task](../../../../tasks_mini/k-4-d-4/task_5.json) / [plan](../../../../plans_mini/k-4-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_5.log) |
| wrong_scope_or_filter | switched_to_deb_haaland_unm_instead_of_doug_burgum_ndsu_path | 1 | [task](../../../../tasks_mini/k-6-d-3/task_2.json) / [plan](../../../../plans_mini/k-6-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_2.log) |
| wrong_scope_or_filter | wrong_comparison_target_and_dataset_branch | 1 | [task](../../../../tasks_mini/k-5-d-4/task_2.json) / [plan](../../../../plans_mini/k-5-d-4/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) |
| wrong_scope_or_filter | wrong_council_district_or_scope | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| wrong_scope_or_filter | wrong_county_pair | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| wrong_scope_or_filter | wrong_district_branch_countywide_district_average_scope | 1 | [task](../../../../tasks_mini/k-5-d-3/task_2.json) / [plan](../../../../plans_mini/k-5-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_2.log) |
| wrong_scope_or_filter | wrong_entity_branch | 1 | [task](../../../../tasks_mini/k-5-d-3/task_9.json) / [plan](../../../../plans_mini/k-5-d-3/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_9.log) |
| wrong_scope_or_filter | wrong_geography_filter_combination | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_scope_or_filter | wrong_school_person_chain_led_to_baltimore_answer | 1 | [task](../../../../tasks_mini/k-5-d-3/task_10.json) / [plan](../../../../plans_mini/k-5-d-3/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_10.log) |
| wrong_scope_or_filter | wrong_terminus_pair | 1 | [task](../../../../tasks_mini/k-4-d-4/task_5.json) / [plan](../../../../plans_mini/k-4-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_5.log) |
| wrong_scope_or_filter | wrong_year_or_filter | 1 | [task](../../../../tasks_mini/k-4-d-2/task_2.json) / [plan](../../../../plans_mini/k-4-d-2/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_2.log) |
| wrong_source_or_dataset | current_dataset_version | 1 | [task](../../../../tasks_mini/k-4-d-4/task_10.json) / [plan](../../../../plans_mini/k-4-d-4/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_10.log) |
| wrong_source_or_dataset | current_year_to_date_complaints_dataset_pivot | 1 | [task](../../../../tasks_mini/k-3-d-1/task_1.json) / [plan](../../../../plans_mini/k-3-d-1/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-1/task_1.log) |
| wrong_source_or_dataset | dc_street_sweeping_lookup_drifted_to_chicago_dataset | 1 | [task](../../../../tasks_mini/k-5-d-3/task_10.json) / [plan](../../../../plans_mini/k-5-d-3/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_10.log) |
| wrong_source_or_dataset | maryland_only_income_dataset_instead_of_us_county_ranking_source | 1 | [task](../../../../tasks_mini/k-3-d-4/task_1.json) / [plan](../../../../plans_mini/k-3-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_1.log) |
| wrong_source_or_dataset | public_school_dataset_family_mismatch | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| wrong_source_or_dataset | used_arrest_dataset_instead_of_crime_dataset | 1 | [task](../../../../tasks_mini/k-4-d-1/task_1.json) / [plan](../../../../plans_mini/k-4-d-1/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_1.log) |
| wrong_source_or_dataset | used_current_dataset_instead_of_task_specified_2019_20_source | 1 | [task](../../../../tasks_mini/k-6-d-3/task_4.json) / [plan](../../../../plans_mini/k-6-d-3/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_4.log) |
| wrong_source_or_dataset | used_parking_violations_instead_of_moving_violations_dataset | 1 | [task](../../../../tasks_mini/k-6-d-3/task_2.json) / [plan](../../../../plans_mini/k-6-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_2.log) |
| wrong_source_or_dataset | used_socioeconomic_indicators_instead_of_public_health_indicators | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| wrong_source_or_dataset | wrong_dataset | 1 | [task](../../../../tasks_mini/k-4-d-5/task_3.json) / [plan](../../../../plans_mini/k-4-d-5/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_3.log) |

## Co-occurring Failure Types

| Failure Type Set | Rows |
| --- | --- |
| evidence_available_answer_error | 10 |
| wrong_scope_or_filter | 5 |
| wrong_scope_or_filter; wrong_source_or_dataset | 4 |
| tool_or_data_blocker | 3 |
| wrong_source_or_dataset | 3 |
| evidence_available_answer_error; tool_or_data_blocker | 2 |
| evidence_available_answer_error; tool_or_data_blocker; wrong_scope_or_filter | 2 |
| incomplete_evidence_budget_exhausted; wrong_scope_or_filter | 2 |
| tool_or_data_blocker; wrong_scope_or_filter | 2 |
| evidence_available_answer_error; planning_decomposition_mismatch; wrong_scope_or_filter | 1 |
| evidence_available_answer_error; tool_or_data_blocker; wrong_source_or_dataset | 1 |
| extraction_or_parsing_error; tool_or_data_blocker | 1 |
| incomplete_evidence_budget_exhausted | 1 |
| incomplete_evidence_budget_exhausted; query_execution_error_loop | 1 |
| incomplete_evidence_budget_exhausted; tool_or_data_blocker | 1 |
| incomplete_evidence_budget_exhausted; tool_or_data_blocker; wrong_scope_or_filter | 1 |
| incomplete_evidence_budget_exhausted; tool_or_data_blocker; wrong_source_or_dataset | 1 |
| incomplete_evidence_early_answer; wrong_scope_or_filter | 1 |
| tool_or_data_blocker; wrong_source_or_dataset | 1 |

## Representative Evidence

- `tasks_mini/k-2-d-3/task_1.json` `wrong_scope_or_filter`/`non_equivalent_query_shape`: Turn 4 | Model response #4 [role=assistant block=1 tool_use] query_ideal({"dataset_id": "nopd-use-of-force-incidents", "file_path": "files/rows.txt", "sql": "SELECT \"Division\", COUNT(*) AS cnt\nFROM t\nWHERE strftim...
- `tasks_mini/k-2-d-3/task_1.json` `tool_or_data_blocker`/`unsupported_or_oversized_data_access`: Turn 15 | Tool result: {"dataset_id": "apd-searches-by-type", "file_path": "files/rows.txt", "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/apd-searches-by-type/files/rows.txt", "columns": ["Sector", "cnt"], "rows": [...
- `tasks_mini/k-2-d-3/task_1.json` `evidence_available_answer_error`/`picked_1790_from_partial_comparison`: Turn 4 | Model response #4 [role=assistant block=1 tool_use] query_ideal({"dataset_id": "nopd-use-of-force-incidents", "file_path": "files/rows.txt", "sql": "SELECT \"Division\", COUNT(*) AS cnt\nFROM t\nWHERE strftim...
- `tasks_mini/k-3-d-1/task_1.json` `tool_or_data_blocker`/`unsupported_or_oversized_data_access`: Turn 12 | Tool logical error (status=error): {"success": false, "error": "Cannot execute SQL: file is too big (2891 MB >= 500 MB limit).", "dataset_id": "nypd-complaint-data-historic", "file_path": "files/rows.txt", "...
- `tasks_mini/k-3-d-1/task_1.json` `wrong_source_or_dataset`/`current_year_to_date_complaints_dataset_pivot`: Turn 27 | Model response #27 [role=assistant block=1 tool_use] query_ideal({"dataset_id": "nypd-complaint-data-current-year-to-date", "file_path": "files/rows.txt", "sql": "SELECT \"OFNS_DESC\" AS offense, COUNT(*) AS...

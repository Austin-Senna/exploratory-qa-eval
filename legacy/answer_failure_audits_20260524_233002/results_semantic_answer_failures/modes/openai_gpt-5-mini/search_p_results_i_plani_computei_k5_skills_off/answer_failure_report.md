# Answer Failure Report

- Source root: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_answer_failures`
- Event rows: 58
- Trusted event rows: 47
- Non-correct eval rows: 31
- Events excluded by validation/model-validation: 11

## Counts by Failure Type

| Failure Type | Events |
| --- | --- |
| evidence_available_answer_error | 13 |
| wrong_source_or_scope | 9 |
| extraction_or_parsing_error | 7 |
| incomplete_evidence_not_enough_turns | 5 |
| computation_or_aggregation_error | 4 |
| query_execution_error_loop | 4 |
| schema_or_shape_inspection_loop | 2 |
| question_or_constraint_misread | 1 |
| semantic_or_gold_label_issue | 1 |
| tool_or_data_blocker | 1 |

## Counts by Failure Type and Subtype

| Failure Type | Subtype | Events | Representative |
| --- | --- | --- | --- |
| incomplete_evidence_not_enough_turns | turn_or_time_budget_exhausted | 3 | [task](../../../../tasks_mini/k-3-d-3/task_6.json) / [plan](../../../../plans_mini/k-3-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_6.log) |
| evidence_available_answer_error | wrong_final_entity | 2 | [task](../../../../tasks_mini/k-4-d-3/task_6.json) / [plan](../../../../plans_mini/k-4-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| wrong_source_or_scope | wrong_dataset_version | 2 | [task](../../../../tasks_mini/k-4-d-4/task_10.json) / [plan](../../../../plans_mini/k-4-d-4/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_10.log) |
| computation_or_aggregation_error | used_unverified_estimate_in_final_math | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| computation_or_aggregation_error | wrong_cross_year_aggregation | 1 | [task](../../../../tasks_mini/k-4-d-4/task_6.json) / [plan](../../../../plans_mini/k-4-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| computation_or_aggregation_error | wrong_hate_crime_total | 1 | [task](../../../../tasks_mini/k-7-d-4/task_1.json) / [plan](../../../../plans_mini/k-7-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-7-d-4/task_1.log) |
| computation_or_aggregation_error | wrong_peak_year_filter | 1 | [task](../../../../tasks_mini/k-4-d-2/task_9.json) / [plan](../../../../plans_mini/k-4-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_9.log) |
| evidence_available_answer_error | ignored_available_count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| evidence_available_answer_error | submitted the wrong final answer after using the inflated public-school count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_10.json) / [plan](../../../../plans_mini/k-3-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| evidence_available_answer_error | submitted_incorrect_year | 1 | [task](../../../../tasks_mini/k-5-d-4/task_1.json) / [plan](../../../../plans_mini/k-5-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_1.log) |
| evidence_available_answer_error | submitted_wrong_downstream_count | 1 | [task](../../../../tasks_mini/k-4-d-2/task_9.json) / [plan](../../../../plans_mini/k-4-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_9.log) |
| evidence_available_answer_error | submitted_wrong_establishment_year_for_wrong_school_district | 1 | [task](../../../../tasks_mini/k-5-d-3/task_3.json) / [plan](../../../../plans_mini/k-5-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| evidence_available_answer_error | submitted_wrong_final_value | 1 | [task](../../../../tasks_mini/k-3-d-2/task_11.json) / [plan](../../../../plans_mini/k-3-d-2/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_11.log) |
| evidence_available_answer_error | wrong_final_answer_submission | 1 | [task](../../../../tasks_mini/k-4-d-5/task_4.json) / [plan](../../../../plans_mini/k-4-d-5/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_4.log) |
| evidence_available_answer_error | wrong_final_submission | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| evidence_available_answer_error | wrong_final_year_submission | 1 | [task](../../../../tasks_mini/k-5-d-3/task_2.json) / [plan](../../../../plans_mini/k-5-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_2.log) |
| evidence_available_answer_error | wrong_numeric_answer | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| evidence_available_answer_error | wrong_rank_selected | 1 | [task](../../../../tasks_mini/k-3-d-4/task_1.json) / [plan](../../../../plans_mini/k-3-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_1.log) |
| extraction_or_parsing_error | ambiguous_final_year_extraction | 1 | [task](../../../../tasks_mini/k-4-d-5/task_1.json) / [plan](../../../../plans_mini/k-4-d-5/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_1.log) |
| extraction_or_parsing_error | first_constable_vs_head_confusion | 1 | [task](../../../../tasks_mini/k-4-d-3/task_6.json) / [plan](../../../../plans_mini/k-4-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| extraction_or_parsing_error | wrong_district_extracted_from_partial_school_nutrition_parse | 1 | [task](../../../../tasks_mini/k-5-d-3/task_3.json) / [plan](../../../../plans_mini/k-5-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| extraction_or_parsing_error | wrong_field_and_truncated_date | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| extraction_or_parsing_error | wrong_founding_year_extracted | 1 | [task](../../../../tasks_mini/k-5-d-4/task_1.json) / [plan](../../../../plans_mini/k-5-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_1.log) |
| extraction_or_parsing_error | wrong_temperature_value_extracted | 1 | [task](../../../../tasks_mini/k-3-d-2/task_11.json) / [plan](../../../../plans_mini/k-3-d-2/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_11.log) |
| extraction_or_parsing_error | wrong_year_from_source | 1 | [task](../../../../tasks_mini/k-3-d-4/task_7.json) / [plan](../../../../plans_mini/k-3-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_7.log) |
| incomplete_evidence_not_enough_turns | hard_timeout | 1 | [task](../../../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../../../plans_mini/k-6-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| incomplete_evidence_not_enough_turns | tool_budget_exhausted | 1 | [task](../../../../tasks_mini/k-4-d-4/task_11.json) / [plan](../../../../plans_mini/k-4-d-4/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_11.log) |
| query_execution_error_loop | malformed_or_incompatible_queries | 1 | [task](../../../../tasks_mini/k-4-d-4/task_11.json) / [plan](../../../../plans_mini/k-4-d-4/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_11.log) |
| query_execution_error_loop | mis_specified_use_of_force_query | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| query_execution_error_loop | repeated_empty_repair_queries | 1 | [task](../../../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../../../plans_mini/k-6-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| query_execution_error_loop | wrong_sql_schema | 1 | [task](../../../../tasks_mini/k-3-d-3/task_6.json) / [plan](../../../../plans_mini/k-3-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_6.log) |
| question_or_constraint_misread | dropped the required city constraint and used county-only scope | 1 | [task](../../../../tasks_mini/k-3-d-2/task_10.json) / [plan](../../../../plans_mini/k-3-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| schema_or_shape_inspection_loop | mixed_schema_probing | 1 | [task](../../../../tasks_mini/k-4-d-4/task_11.json) / [plan](../../../../plans_mini/k-4-d-4/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_11.log) |
| schema_or_shape_inspection_loop | schema_probe_detour | 1 | [task](../../../../tasks_mini/k-3-d-3/task_6.json) / [plan](../../../../plans_mini/k-3-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_6.log) |
| semantic_or_gold_label_issue | inconsistent_gold_answer | 1 | [task](../../../../tasks_mini/k-4-d-3/task_11.json) / [plan](../../../../plans_mini/k-4-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| tool_or_data_blocker | tool_budget_exhausted | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| wrong_source_or_scope | countywide_district_office_count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| wrong_source_or_scope | countywide_public_school_count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| wrong_source_or_scope | missing_city_filter | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_source_or_scope | used_open_date_instead_of_school_day_source | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| wrong_source_or_scope | wrong_city_branch | 1 | [task](../../../../tasks_mini/k-5-d-4/task_2.json) / [plan](../../../../plans_mini/k-5-d-4/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) |
| wrong_source_or_scope | wrong_release_or_dataset_choice | 1 | [task](../../../../tasks_mini/k-5-d-4/task_2.json) / [plan](../../../../plans_mini/k-5-d-4/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) |
| wrong_source_or_scope | wrong_year_branch | 1 | [task](../../../../tasks_mini/k-4-d-2/task_9.json) / [plan](../../../../plans_mini/k-4-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_9.log) |

## Co-occurring Failure Types

| Failure Type Set | Rows |
| --- | --- |
| evidence_available_answer_error | 5 |
| evidence_available_answer_error; extraction_or_parsing_error | 4 |
| extraction_or_parsing_error | 2 |
| incomplete_evidence_not_enough_turns; query_execution_error_loop; schema_or_shape_inspection_loop | 2 |
| wrong_source_or_scope | 2 |
| computation_or_aggregation_error | 1 |
| computation_or_aggregation_error; evidence_available_answer_error; wrong_source_or_scope | 1 |
| computation_or_aggregation_error; incomplete_evidence_not_enough_turns | 1 |
| computation_or_aggregation_error; query_execution_error_loop | 1 |
| evidence_available_answer_error; question_or_constraint_misread | 1 |
| evidence_available_answer_error; tool_or_data_blocker | 1 |
| evidence_available_answer_error; wrong_source_or_scope | 1 |
| extraction_or_parsing_error; wrong_source_or_scope | 1 |
| incomplete_evidence_not_enough_turns; query_execution_error_loop | 1 |
| incomplete_evidence_not_enough_turns; wrong_source_or_scope | 1 |
| semantic_or_gold_label_issue | 1 |

## Representative Evidence

- `tasks_mini/k-3-d-2/task_1.json` `query_execution_error_loop`/`mis_specified_use_of_force_query`: Turn 17 | query_ideal(... SUM("Used Taser(s)") AS taser_sum ... GROUP BY "Council District" ...)
- `tasks_mini/k-3-d-2/task_1.json` `computation_or_aggregation_error`/`used_unverified_estimate_in_final_math`: Turn 35 | submit_answer({"answer": "[2]", "reasoning": "... Estimated number of 2023 use-of-force incidents in District 1 with taser used was about 4; using incorporation year 1839 gives 4*(100/(2023-1839)) ≈ 2 ..."})
- `tasks_mini/k-3-d-2/task_10.json` `question_or_constraint_misread`/`dropped the required city constraint and used county-only scope`: Turn 5 | submit_repaired_sql({"sql": "SELECT COUNT(*) AS public_count\nFROM t, UNNEST(features) AS u(f)\nWHERE upper(trim(f.properties.NMCNTY)) = 'ORANGE COUNTY'\n AND trim(f.properties.SCHOOLYEAR) = '2022-2023'", "re...
- `tasks_mini/k-3-d-2/task_10.json` `evidence_available_answer_error`/`submitted the wrong final answer after using the inflated public-school count`: Turn 7 | submit_answer({"answer": "[1010]", "reasoning": "Public schools in Orange County for 2022-2023 = 1110 (from public-school-locations-current). Private schools in Orange County for 2021-2022 = 100 (from private...
- `tasks_mini/k-3-d-2/task_11.json` `extraction_or_parsing_error`/`wrong_temperature_value_extracted`: Turn 10 | grep_file("wikipedia/Basin,_Wyoming/content.txt", "August 8, 1983", context_lines=2) returned: "The town had the highest temperature ever recorded in Wyoming, , on August 8, 1983, and also holds the state re...

# Answer Failure Report

- Source root: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_answer_failures`
- Event rows: 58
- Trusted event rows: 57
- Non-correct eval rows: 32
- Events excluded by validation/model-validation: 1

## Counts by Failure Type

| Failure Type | Events |
| --- | --- |
| wrong_scope_or_filter | 15 |
| evidence_available_answer_error | 13 |
| tool_or_data_blocker | 12 |
| computation_or_aggregation_error | 7 |
| incomplete_evidence_budget_exhausted | 5 |
| extraction_or_parsing_error | 2 |
| planning_decomposition_mismatch | 2 |
| question_or_constraint_misread | 1 |

## Counts by Failure Type and Subtype

| Failure Type | Subtype | Events | Representative |
| --- | --- | --- | --- |
| tool_or_data_blocker | tool_budget_exhausted | 7 | [task](../../../../tasks_mini/k-4-d-2/task_1.json) / [plan](../../../../plans_mini/k-4-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| incomplete_evidence_budget_exhausted | tool_budget_exhausted | 3 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| tool_or_data_blocker | data_source_missing_or_unavailable | 2 | [task](../../../../tasks_mini/k-4-d-4/task_4.json) / [plan](../../../../plans_mini/k-4-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_4.log) |
| tool_or_data_blocker | unsupported_or_oversized_data_access | 2 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| wrong_scope_or_filter | dropped city filter | 2 | [task](../../../../tasks_mini/k-3-d-2/task_10.json) / [plan](../../../../plans_mini/k-3-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| computation_or_aggregation_error | off-by-one final arithmetic | 1 | [task](../../../../tasks_mini/k-3-d-4/task_6.json) / [plan](../../../../plans_mini/k-3-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_6.log) |
| computation_or_aggregation_error | release_winner_ranking_error | 1 | [task](../../../../tasks_mini/k-4-d-4/task_6.json) / [plan](../../../../plans_mini/k-4-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| computation_or_aggregation_error | sampled grep counts used for final answer | 1 | [task](../../../../tasks_mini/k-4-d-1/task_2.json) / [plan](../../../../plans_mini/k-4-d-1/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-1/task_2.log) |
| computation_or_aggregation_error | subtracted_the_wrong_operands_for_the_final_difference | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| computation_or_aggregation_error | used_2016_only_instead_of_2016_and_2018_average | 1 | [task](../../../../tasks_mini/k-4-d-4/task_5.json) / [plan](../../../../plans_mini/k-4-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_5.log) |
| computation_or_aggregation_error | wrong operands from intermediate queries | 1 | [task](../../../../tasks_mini/k-3-d-4/task_6.json) / [plan](../../../../plans_mini/k-3-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_6.log) |
| computation_or_aggregation_error | wrong_count_in_final_sum | 1 | [task](../../../../tasks_mini/k-4-d-4/task_10.json) / [plan](../../../../plans_mini/k-4-d-4/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_10.log) |
| evidence_available_answer_error | final answer selected the wrong district/year synthesis from off-track SiteISP averages | 1 | [task](../../../../tasks_mini/k-5-d-3/task_2.json) / [plan](../../../../plans_mini/k-5-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_2.log) |
| evidence_available_answer_error | intermediate_values_in_final_answer | 1 | [task](../../../../tasks_mini/k-4-d-2/task_6.json) / [plan](../../../../plans_mini/k-4-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_6.log) |
| evidence_available_answer_error | rough_estimate_submission | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| evidence_available_answer_error | selected_1877_instead_of_target_year | 1 | [task](../../../../tasks_mini/k-3-d-4/task_7.json) / [plan](../../../../plans_mini/k-3-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_7.log) |
| evidence_available_answer_error | submitted 3274 instead of the task answer 2941 | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| evidence_available_answer_error | submitted [4] despite reasoning 1 | 1 | [task](../../../../tasks_mini/k-4-d-2/task_5.json) / [plan](../../../../plans_mini/k-4-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_5.log) |
| evidence_available_answer_error | submitted wrong final lookup result | 1 | [task](../../../../tasks_mini/k-5-d-1/task_4.json) / [plan](../../../../plans_mini/k-5-d-1/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-1/task_4.log) |
| evidence_available_answer_error | submitted_loop_per_capita_income_instead_of_the_intended_branch_result | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| evidence_available_answer_error | substituted location OPEN_DATE for requested school-day fact | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| evidence_available_answer_error | switched_to_joseph_la_flesche_1822 | 1 | [task](../../../../tasks_mini/k-4-d-4/task_8.json) / [plan](../../../../plans_mini/k-4-d-4/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_8.log) |
| evidence_available_answer_error | used estimated count | 1 | [task](../../../../tasks_mini/k-3-d-4/task_4.json) / [plan](../../../../plans_mini/k-3-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| evidence_available_answer_error | wrong_output_shape_scalar_expected | 1 | [task](../../../../tasks_mini/k-4-d-2/task_6.json) / [plan](../../../../plans_mini/k-4-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_6.log) |
| evidence_available_answer_error | wrong_year_selected | 1 | [task](../../../../tasks_mini/k-5-d-4/task_1.json) / [plan](../../../../plans_mini/k-5-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_1.log) |
| extraction_or_parsing_error | precinct/count mix-up | 1 | [task](../../../../tasks_mini/k-5-d-1/task_4.json) / [plan](../../../../plans_mini/k-5-d-1/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-1/task_4.log) |
| extraction_or_parsing_error | wrong historical title/name extracted from Wikipedia snippet | 1 | [task](../../../../tasks_mini/k-4-d-3/task_6.json) / [plan](../../../../plans_mini/k-4-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| incomplete_evidence_budget_exhausted | (none) | 1 | [task](../../../../tasks_mini/k-4-d-2/task_1.json) / [plan](../../../../plans_mini/k-4-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| incomplete_evidence_budget_exhausted | turn_or_time_budget_exhausted | 1 | [task](../../../../tasks_mini/k-4-d-3/task_11.json) / [plan](../../../../plans_mini/k-4-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| planning_decomposition_mismatch | arrest-stage chain divergence | 1 | [task](../../../../tasks_mini/k-4-d-2/task_5.json) / [plan](../../../../plans_mini/k-4-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_5.log) |
| planning_decomposition_mismatch | used DIABETES_AdjPrev multi-year intersection instead of authored DIABETES_CrudePrev per-year path | 1 | [task](../../../../tasks_mini/k-5-d-4/task_6.json) / [plan](../../../../plans_mini/k-5-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_6.log) |
| question_or_constraint_misread | omitted required GradeLevel='All Grades' filter | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| tool_or_data_blocker | malformed_tool_call | 1 | [task](../../../../tasks_mini/k-3-d-4/task_4.json) / [plan](../../../../plans_mini/k-3-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| wrong_scope_or_filter | county instead of city scope | 1 | [task](../../../../tasks_mini/k-4-d-2/task_5.json) / [plan](../../../../plans_mini/k-4-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_5.log) |
| wrong_scope_or_filter | county-level public-school subset instead of city-and-county count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| wrong_scope_or_filter | district_3_instead_of_1 | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| wrong_scope_or_filter | dropped_boston_city_constraint | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| wrong_scope_or_filter | pivoted from Texas identified-student-percentage to Puerto Rico SiteISP/CEP dataset | 1 | [task](../../../../tasks_mini/k-5-d-3/task_2.json) / [plan](../../../../plans_mini/k-5-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_2.log) |
| wrong_scope_or_filter | switched_terminus_city_to_santa_monica | 1 | [task](../../../../tasks_mini/k-4-d-4/task_5.json) / [plan](../../../../plans_mini/k-4-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_5.log) |
| wrong_scope_or_filter | used Wayne County aggregate instead of Detroit-specific school count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_scope_or_filter | used Wikipedia county pages instead of the census-population source | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| wrong_scope_or_filter | wrong date field/filter path | 1 | [task](../../../../tasks_mini/k-4-d-2/task_5.json) / [plan](../../../../plans_mini/k-4-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_5.log) |
| wrong_scope_or_filter | wrong geography/source family | 1 | [task](../../../../tasks_mini/k-5-d-4/task_5.json) / [plan](../../../../plans_mini/k-5-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_5.log) |
| wrong_scope_or_filter | wrong school/location branch | 1 | [task](../../../../tasks_mini/k-4-d-3/task_1.json) / [plan](../../../../plans_mini/k-4-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_1.log) |
| wrong_scope_or_filter | wrong_branch_and_community_area_path | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| wrong_scope_or_filter | wrong_year_filter | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |

## Co-occurring Failure Types

| Failure Type Set | Rows |
| --- | --- |
| evidence_available_answer_error | 4 |
| wrong_scope_or_filter | 3 |
| computation_or_aggregation_error | 2 |
| computation_or_aggregation_error; tool_or_data_blocker | 2 |
| computation_or_aggregation_error; wrong_scope_or_filter | 2 |
| evidence_available_answer_error; tool_or_data_blocker | 2 |
| evidence_available_answer_error; wrong_scope_or_filter | 2 |
| incomplete_evidence_budget_exhausted | 2 |
| incomplete_evidence_budget_exhausted; tool_or_data_blocker; wrong_scope_or_filter | 2 |
| tool_or_data_blocker | 2 |
| evidence_available_answer_error; extraction_or_parsing_error | 1 |
| evidence_available_answer_error; planning_decomposition_mismatch; wrong_scope_or_filter | 1 |
| evidence_available_answer_error; question_or_constraint_misread; wrong_scope_or_filter | 1 |
| evidence_available_answer_error; tool_or_data_blocker; wrong_scope_or_filter | 1 |
| extraction_or_parsing_error | 1 |
| incomplete_evidence_budget_exhausted; tool_or_data_blocker | 1 |
| planning_decomposition_mismatch; tool_or_data_blocker | 1 |
| tool_or_data_blocker; wrong_scope_or_filter | 1 |

## Representative Evidence

- `tasks_mini/k-3-d-2/task_1.json` `tool_or_data_blocker`/`unsupported_or_oversized_data_access`: Turn 10 | Tool logical error (status=error): {"success": false, "error": "Cannot execute SQL: file is too big (1377 MB >= 500 MB limit).", "dataset_id": "apd-computer-aided-dispatch-incidents", "file_path": "files/row...
- `tasks_mini/k-3-d-2/task_1.json` `wrong_scope_or_filter`/`district_3_instead_of_1`: Turn 27 | execute_ideal(...) | Tool result: {"output": "1", "success": true, "dataset_id": "apd-computer-aided-dispatch-incidents", "file_path": "files/rows.txt", "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/apd-com...
- `tasks_mini/k-3-d-2/task_1.json` `incomplete_evidence_budget_exhausted`/`tool_budget_exhausted`: Turn 33 | submit_answer({"answer": "[5]", "reasoning": "Found Sector with most searches in 2023 = Charlie (apd-searches-by-type). Using CAD samples for Sector=Charlie, Council District 3 appears most frequent. Due to...
- `tasks_mini/k-3-d-2/task_10.json` `wrong_scope_or_filter`/`dropped city filter`: Turn 7 | Model response #1 [role=assistant block=1 tool_use] select_match({"index": 0, "reason": "No candidate matches: authored record filters CITY='ORLANDO' (via f.properties.CITY) in addition to NMCNTY='ORANGE COUN...
- `tasks_mini/k-3-d-2/task_10.json` `wrong_scope_or_filter`/`dropped city filter`: Turn 8 | Model response #1 [role=assistant block=1 tool_use] select_match({"index": 0, "reason": "Submitted intent is to count private schools in Orange County, FL for 2021-2022. Authored record counts private schools...

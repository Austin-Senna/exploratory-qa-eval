# Answer Failure Report

- Source root: `results_semantic_answer_failures`
- Event rows: 98
- Trusted event rows: 83
- Non-correct eval rows: 57
- Events excluded by validation/model-validation: 15

## Counts by Failure Type

| Failure Type | Events |
| --- | --- |
| wrong_scope_or_filter | 23 |
| evidence_available_answer_error | 20 |
| tool_or_data_blocker | 12 |
| incomplete_evidence_budget_exhausted | 7 |
| wrong_source_or_dataset | 6 |
| computation_or_aggregation_error | 4 |
| extraction_or_parsing_error | 4 |
| planning_decomposition_mismatch | 4 |
| incomplete_evidence_early_answer | 1 |
| query_execution_error_loop | 1 |
| question_or_constraint_misread | 1 |

## Counts by Failure Type and Subtype

| Failure Type | Subtype | Events | Representative |
| --- | --- | --- | --- |
| tool_or_data_blocker | tool_budget_exhausted | 7 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| incomplete_evidence_budget_exhausted | tool_budget_exhausted | 4 | [task](../../../../tasks_mini/k-4-d-4/task_11.json) / [plan](../../../../plans_mini/k-4-d-4/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-4/task_11.log) |
| tool_or_data_blocker | data_source_missing_or_unavailable | 2 | [task](../../../../tasks_mini/k-5-d-2/task_8.json) / [plan](../../../../plans_mini/k-5-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-2/task_8.log) |
| tool_or_data_blocker | unsupported_or_oversized_data_access | 2 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| wrong_scope_or_filter | Wayne County scope | 2 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| computation_or_aggregation_error | compared an incomplete candidate set and chose the wrong maximum | 1 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| computation_or_aggregation_error | counted an over-broad set of crime codes instead of only the target code | 1 | [task](../../../../tasks_mini/k-4-d-2/task_9.json) / [plan](../../../../plans_mini/k-4-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_9.log) |
| computation_or_aggregation_error | extra sector filter | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| computation_or_aggregation_error | used string whitelist instead of numeric > 0 for Used Taser(s), excluding rows with value 2 | 1 | [task](../../../../tasks_mini/k-4-d-1/task_5.json) / [plan](../../../../plans_mini/k-4-d-1/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-1/task_5.log) |
| evidence_available_answer_error | baltimore_county_chain_instead_of_ulster_county | 1 | [task](../../../../tasks_mini/k-4-d-3/task_7.json) / [plan](../../../../plans_mini/k-4-d-3/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-3/task_7.log) |
| evidence_available_answer_error | final answer included extra intermediate school name instead of only the bridge | 1 | [task](../../../../tasks_mini/k-3-d-4/task_5.json) / [plan](../../../../plans_mini/k-3-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-4/task_5.log) |
| evidence_available_answer_error | final answer used the wrong county pair and returned [4] instead of the task answer | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| evidence_available_answer_error | final_answer_selected_wrong_entity | 1 | [task](../../../../tasks_mini/k-4-d-3/task_6.json) / [plan](../../../../plans_mini/k-4-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| evidence_available_answer_error | ignored_lower_competitor_counts | 1 | [task](../../../../tasks_mini/k-4-d-3/task_2.json) / [plan](../../../../plans_mini/k-4-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| evidence_available_answer_error | selected Chad Brown over James Brown | 1 | [task](../../../../tasks_mini/k-4-d-4/task_13.json) / [plan](../../../../plans_mini/k-4-d-4/task_13.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-4/task_13.log) |
| evidence_available_answer_error | selected Davenport city population instead of Scott County population | 1 | [task](../../../../tasks_mini/k-4-d-3/task_11.json) / [plan](../../../../plans_mini/k-4-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| evidence_available_answer_error | submitted 163 from null-premise/110 path despite available 103/258 evidence | 1 | [task](../../../../tasks_mini/k-5-d-1/task_4.json) / [plan](../../../../plans_mini/k-5-d-1/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-1/task_4.log) |
| evidence_available_answer_error | submitted 1835 from Chicago Fire Department instead of 1858 | 1 | [task](../../../../tasks_mini/k-5-d-4/task_3.json) / [plan](../../../../plans_mini/k-5-d-4/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-4/task_3.log) |
| evidence_available_answer_error | submitted 5882 unchanged from the wrong scoped query result | 1 | [task](../../../../tasks_mini/k-4-d-2/task_15.json) / [plan](../../../../plans_mini/k-4-d-2/task_15.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_15.log) |
| evidence_available_answer_error | submitted University of New Mexico from the wrong person-biography path | 1 | [task](../../../../tasks_mini/k-6-d-3/task_2.json) / [plan](../../../../plans_mini/k-6-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-6-d-3/task_2.log) |
| evidence_available_answer_error | submitted [5] despite own reasoning rounding to 1 | 1 | [task](../../../../tasks_mini/k-4-d-2/task_5.json) / [plan](../../../../plans_mini/k-4-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_5.log) |
| evidence_available_answer_error | submitted bracketed composite answer instead of required single numeric answer | 1 | [task](../../../../tasks_mini/k-4-d-2/task_2.json) / [plan](../../../../plans_mini/k-4-d-2/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_2.log) |
| evidence_available_answer_error | submitted the wrong final tuple after computing 1822 for Southeast | 1 | [task](../../../../tasks_mini/k-4-d-2/task_6.json) / [plan](../../../../plans_mini/k-4-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_6.log) |
| evidence_available_answer_error | used wrong NOPD metric branch | 1 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| evidence_available_answer_error | wrong community area | 1 | [task](../../../../tasks_mini/k-5-d-3/task_9.json) / [plan](../../../../plans_mini/k-5-d-3/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_9.log) |
| evidence_available_answer_error | wrong final district | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| evidence_available_answer_error | wrong final selection | 1 | [task](../../../../tasks_mini/k-4-d-4/task_6.json) / [plan](../../../../plans_mini/k-4-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| evidence_available_answer_error | wrong_final_numeric_answer | 1 | [task](../../../../tasks_mini/k-4-d-2/task_8.json) / [plan](../../../../plans_mini/k-4-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_8.log) |
| evidence_available_answer_error | wrong_year_selected_from_available_source | 1 | [task](../../../../tasks_mini/k-5-d-3/task_3.json) / [plan](../../../../plans_mini/k-5-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| extraction_or_parsing_error | assumed wrong column name in file schema | 1 | [task](../../../../tasks_mini/k-4-d-2/task_9.json) / [plan](../../../../plans_mini/k-4-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_9.log) |
| extraction_or_parsing_error | grep matched negated mental-health rows | 1 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| extraction_or_parsing_error | selected Paddock Arcade's 1850 year instead of Watertown's 1869 city-incorporation year | 1 | [task](../../../../tasks_mini/k-4-d-5/task_1.json) / [plan](../../../../plans_mini/k-4-d-5/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-5/task_1.log) |
| extraction_or_parsing_error | wrong_column_name | 1 | [task](../../../../tasks_mini/k-4-d-2/task_8.json) / [plan](../../../../plans_mini/k-4-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_8.log) |
| incomplete_evidence_budget_exhausted | tool budget exhausted | 1 | [task](../../../../tasks_mini/k-4-d-4/task_6.json) / [plan](../../../../plans_mini/k-4-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| incomplete_evidence_budget_exhausted | tool-call cap reached before extracting both Police Bureau figures | 1 | [task](../../../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../../../plans_mini/k-6-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| incomplete_evidence_budget_exhausted | tool_limit_before_grade_8_9_validation | 1 | [task](../../../../tasks_mini/k-4-d-3/task_7.json) / [plan](../../../../plans_mini/k-4-d-3/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-3/task_7.log) |
| incomplete_evidence_early_answer | unsupported final guess | 1 | [task](../../../../tasks_mini/k-5-d-3/task_2.json) / [plan](../../../../plans_mini/k-5-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_2.log) |
| planning_decomposition_mismatch | diverged to Deb Haaland instead of Doug Burgum at the DOI hop | 1 | [task](../../../../tasks_mini/k-6-d-3/task_2.json) / [plan](../../../../plans_mini/k-6-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-6-d-3/task_2.log) |
| planning_decomposition_mismatch | incomplete_evidence_chain | 1 | [task](../../../../tasks_mini/k-3-d-2/task_6.json) / [plan](../../../../plans_mini/k-3-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| planning_decomposition_mismatch | skipped yearly branch-intersection before lookup | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| planning_decomposition_mismatch | switched the area-hop from the planned arrest dataset to the 2010-2019 crime dataset | 1 | [task](../../../../tasks_mini/k-4-d-2/task_6.json) / [plan](../../../../plans_mini/k-4-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_6.log) |
| query_execution_error_loop | invalid GeoJSON field path | 1 | [task](../../../../tasks_mini/k-3-d-2/task_10.json) / [plan](../../../../plans_mini/k-3-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| question_or_constraint_misread | answered_with_wrong_historical_frame | 1 | [task](../../../../tasks_mini/k-4-d-3/task_6.json) / [plan](../../../../plans_mini/k-4-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| tool_or_data_blocker | malformed_tool_call | 1 | [task](../../../../tasks_mini/k-4-d-4/task_11.json) / [plan](../../../../plans_mini/k-4-d-4/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-4/task_11.log) |
| wrong_scope_or_filter | Texas-wide 2021 ranking instead of intended 2016 rate-category check | 1 | [task](../../../../tasks_mini/k-5-d-4/task_5.json) / [plan](../../../../plans_mini/k-5-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-4/task_5.log) |
| wrong_scope_or_filter | counted_bid_subset_instead_of_ward_1 | 1 | [task](../../../../tasks_mini/k-3-d-2/task_4.json) / [plan](../../../../plans_mini/k-3-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_4.log) |
| wrong_scope_or_filter | county-wide district ranking instead of direct Pullman School District filter | 1 | [task](../../../../tasks_mini/k-4-d-2/task_15.json) / [plan](../../../../plans_mini/k-4-d-2/task_15.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_15.log) |
| wrong_scope_or_filter | county-wide instead of Orlando subset | 1 | [task](../../../../tasks_mini/k-3-d-2/task_10.json) / [plan](../../../../plans_mini/k-3-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| wrong_scope_or_filter | extra Council District=9 filter on sector-wide dispatch count | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| wrong_scope_or_filter | extra Ward 2 filter instead of all-ward total | 1 | [task](../../../../tasks_mini/k-5-d-1/task_3.json) / [plan](../../../../plans_mini/k-5-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-1/task_3.log) |
| wrong_scope_or_filter | extra_precinct_filter | 1 | [task](../../../../tasks_mini/k-4-d-1/task_3.json) / [plan](../../../../plans_mini/k-4-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-1/task_3.log) |
| wrong_scope_or_filter | failed cross-year top-five county shortlist; hand-picked a Dallas-containing list | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| wrong_scope_or_filter | final_answer_based_on_bid_counts | 1 | [task](../../../../tasks_mini/k-3-d-2/task_4.json) / [plan](../../../../plans_mini/k-3-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_4.log) |
| wrong_scope_or_filter | looked up Loop instead of Lincoln Square | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| wrong_scope_or_filter | missing_city_filter | 1 | [task](../../../../tasks_mini/k-3-d-2/task_6.json) / [plan](../../../../plans_mini/k-3-d-2/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| wrong_scope_or_filter | pivoted to Dallas County / George M. Dallas instead of the intended county branch | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| wrong_scope_or_filter | switched_to_bid_subset_after_schema_error | 1 | [task](../../../../tasks_mini/k-3-d-2/task_4.json) / [plan](../../../../plans_mini/k-3-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_4.log) |
| wrong_scope_or_filter | used 2018 release but only 2015-2016 rows appeared; wrong year slice | 1 | [task](../../../../tasks_mini/k-5-d-4/task_3.json) / [plan](../../../../plans_mini/k-5-d-4/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-4/task_3.log) |
| wrong_scope_or_filter | used MA/Suffolk filter instead of Boston-derived county path | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| wrong_scope_or_filter | used `IDENT` text match and `AREA NAME` instead of crime code 354 plus Area ID 9 | 1 | [task](../../../../tasks_mini/k-4-d-2/task_2.json) / [plan](../../../../plans_mini/k-4-d-2/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_2.log) |
| wrong_scope_or_filter | used broad counts instead of intended intersection chain | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| wrong_scope_or_filter | used city-or-county school count instead of Los Angeles city | 1 | [task](../../../../tasks_mini/k-4-d-2/task_5.json) / [plan](../../../../plans_mini/k-4-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_5.log) |
| wrong_scope_or_filter | widened_candidate_pool | 1 | [task](../../../../tasks_mini/k-4-d-3/task_2.json) / [plan](../../../../plans_mini/k-4-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| wrong_scope_or_filter | wrong branch/entity intersection | 1 | [task](../../../../tasks_mini/k-5-d-3/task_9.json) / [plan](../../../../plans_mini/k-5-d-3/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_9.log) |
| wrong_scope_or_filter | wrong county candidate set | 1 | [task](../../../../tasks_mini/k-4-d-4/task_6.json) / [plan](../../../../plans_mini/k-4-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| wrong_source_or_dataset | Puerto Rico school-nutrition detour | 1 | [task](../../../../tasks_mini/k-5-d-3/task_2.json) / [plan](../../../../plans_mini/k-5-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_2.log) |
| wrong_source_or_dataset | chicago_street_sweeping_instead_of_dc | 1 | [task](../../../../tasks_mini/k-4-d-3/task_7.json) / [plan](../../../../plans_mini/k-4-d-3/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-3/task_7.log) |
| wrong_source_or_dataset | public-school county-count source not identified | 1 | [task](../../../../tasks_mini/k-4-d-4/task_10.json) / [plan](../../../../plans_mini/k-4-d-4/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-4/task_10.log) |
| wrong_source_or_dataset | skipped required RIPA area-mapping file | 1 | [task](../../../../tasks_mini/k-4-d-2/task_2.json) / [plan](../../../../plans_mini/k-4-d-2/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-2/task_2.log) |
| wrong_source_or_dataset | used arrest dataset instead of 2019 crime dataset | 1 | [task](../../../../tasks_mini/k-4-d-1/task_1.json) / [plan](../../../../plans_mini/k-4-d-1/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-4-d-1/task_1.log) |
| wrong_source_or_dataset | wrong_geography_source_family | 1 | [task](../../../../tasks_mini/k-5-d-3/task_11.json) / [plan](../../../../plans_mini/k-5-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/tasks_mini/k-5-d-3/task_11.log) |

## Co-occurring Failure Types

| Failure Type Set | Rows |
| --- | --- |
| wrong_scope_or_filter | 6 |
| evidence_available_answer_error; wrong_scope_or_filter | 5 |
| evidence_available_answer_error | 4 |
| incomplete_evidence_budget_exhausted | 3 |
| tool_or_data_blocker | 3 |
| evidence_available_answer_error; planning_decomposition_mismatch | 2 |
| evidence_available_answer_error; tool_or_data_blocker | 2 |
| tool_or_data_blocker; wrong_scope_or_filter | 2 |
| computation_or_aggregation_error | 1 |
| computation_or_aggregation_error; evidence_available_answer_error; extraction_or_parsing_error | 1 |
| computation_or_aggregation_error; extraction_or_parsing_error | 1 |
| computation_or_aggregation_error; tool_or_data_blocker | 1 |
| evidence_available_answer_error; extraction_or_parsing_error | 1 |
| evidence_available_answer_error; incomplete_evidence_budget_exhausted; wrong_scope_or_filter | 1 |
| evidence_available_answer_error; incomplete_evidence_budget_exhausted; wrong_source_or_dataset | 1 |
| evidence_available_answer_error; question_or_constraint_misread | 1 |
| evidence_available_answer_error; tool_or_data_blocker; wrong_scope_or_filter | 1 |
| evidence_available_answer_error; wrong_scope_or_filter; wrong_source_or_dataset | 1 |
| extraction_or_parsing_error | 1 |
| incomplete_evidence_budget_exhausted; tool_or_data_blocker | 1 |
| incomplete_evidence_budget_exhausted; wrong_source_or_dataset | 1 |
| incomplete_evidence_early_answer; wrong_source_or_dataset | 1 |
| planning_decomposition_mismatch; tool_or_data_blocker; wrong_scope_or_filter | 1 |
| planning_decomposition_mismatch; wrong_scope_or_filter | 1 |
| query_execution_error_loop; wrong_scope_or_filter | 1 |
| tool_or_data_blocker; wrong_source_or_dataset | 1 |
| wrong_source_or_dataset | 1 |

## Representative Evidence

- `tasks_mini/k-2-d-3/task_1.json` `evidence_available_answer_error`/`used wrong NOPD metric branch`: Turn 5 | ... query_file({"dataset_id": "nopd-use-of-force-incidents", "file_path": "files/rows.txt", "sql": "SELECT \"Division level\", COUNT(*) AS cnt FROM t WHERE EXTRACT(year FROM \"Date Occurred\") = 2022 GROUP BY...
- `tasks_mini/k-2-d-3/task_1.json` `extraction_or_parsing_error`/`grep matched negated mental-health rows`: Turn 16 | ... query_file({"dataset_id": "apd-computer-aided-dispatch-incidents", "file_path": "files/rows.txt", "sql": "SELECT COUNT(*) FROM t WHERE \"Response Year\" = 2022 AND LOWER(\"Mental Health Flag\") LIKE '%me...
- `tasks_mini/k-2-d-3/task_1.json` `computation_or_aggregation_error`/`compared an incomplete candidate set and chose the wrong maximum`: Turn 33 | ... submit_answer({"answer": "[1790]", "reasoning": "From datasets: NOPD weapon-type incidents by division (2022) max = 41 (7th District). APD searches due to contraband highest sector = Edward (3 searches);...
- `tasks_mini/k-3-d-2/task_1.json` `tool_or_data_blocker`/`unsupported_or_oversized_data_access`: Turn 6 | query_file({"dataset_id": "apd-computer-aided-dispatch-incidents", "file_path": "files/rows.txt", "sql": "SELECT \"Council District\", COUNT(*) AS cnt\nFROM t\nWHERE \"Response Year\" = 2023 AND \"Sector\" =...
- `tasks_mini/k-3-d-2/task_1.json` `computation_or_aggregation_error`/`extra sector filter`: Turn 29 | query_file({"dataset_id": "apd-use-of-force", "file_path": "files/rows.txt", "sql": "SELECT COUNT(*)\nFROM t\nWHERE (CAST(strftime('%Y', \"Occurred Date\") AS VARCHAR) = '2023')\nAND \"Council District\" = 1...

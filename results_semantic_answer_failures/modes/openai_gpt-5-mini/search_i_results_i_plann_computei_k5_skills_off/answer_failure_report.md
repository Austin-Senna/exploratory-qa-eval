# Answer Failure Report

- Source root: `results_semantic_answer_failures`
- Event rows: 82
- Trusted event rows: 68
- Non-correct eval rows: 45
- Events excluded by validation/model-validation: 14

## Counts by Failure Type

| Failure Type | Events |
| --- | --- |
| wrong_scope_or_filter | 19 |
| tool_or_data_blocker | 12 |
| incomplete_evidence_budget_exhausted | 10 |
| evidence_available_answer_error | 8 |
| planning_decomposition_mismatch | 5 |
| wrong_source_or_dataset | 4 |
| computation_or_aggregation_error | 3 |
| extraction_or_parsing_error | 3 |
| low_yield_search_loop | 2 |
| question_or_constraint_misread | 1 |
| same_hop_repetition | 1 |

## Counts by Failure Type and Subtype

| Failure Type | Subtype | Events | Representative |
| --- | --- | --- | --- |
| tool_or_data_blocker | tool_budget_exhausted | 8 | [task](../../../../tasks_mini/k-4-d-2/task_1.json) / [plan](../../../../plans_mini/k-4-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| incomplete_evidence_budget_exhausted | turn_or_time_budget_exhausted | 3 | [task](../../../../tasks_mini/k-3-d-4/task_4.json) / [plan](../../../../plans_mini/k-3-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| incomplete_evidence_budget_exhausted | tool_budget_exhausted | 2 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| tool_or_data_blocker | unsupported_or_oversized_data_access | 2 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| computation_or_aggregation_error | broad ranking instead of specific comparison | 1 | [task](../../../../tasks_mini/k-4-d-3/task_10.json) / [plan](../../../../plans_mini/k-4-d-3/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_10.log) |
| computation_or_aggregation_error | left subtraction as an unevaluated expression | 1 | [task](../../../../tasks_mini/k-4-d-2/task_13.json) / [plan](../../../../plans_mini/k-4-d-2/task_13.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-2/task_13.log) |
| computation_or_aggregation_error | wrong_percentage_basis | 1 | [task](../../../../tasks_mini/k-3-d-2/task_2.json) / [plan](../../../../plans_mini/k-3-d-2/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_2.log) |
| evidence_available_answer_error | final_answer_overwrote_intermediate_result | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| evidence_available_answer_error | final_answer_wrong | 1 | [task](../../../../tasks_mini/k-6-d-3/task_5.json) / [plan](../../../../plans_mini/k-6-d-3/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-6-d-3/task_5.log) |
| evidence_available_answer_error | selected P.S. 011 instead of PS 056 | 1 | [task](../../../../tasks_mini/k-4-d-3/task_2.json) / [plan](../../../../plans_mini/k-4-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| evidence_available_answer_error | speculative wrong river choice | 1 | [task](../../../../tasks_mini/k-5-d-4/task_5.json) / [plan](../../../../plans_mini/k-5-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-4/task_5.log) |
| evidence_available_answer_error | submitted 1992 instead of 1936 | 1 | [task](../../../../tasks_mini/k-5-d-3/task_12.json) / [plan](../../../../plans_mini/k-5-d-3/task_12.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-3/task_12.log) |
| evidence_available_answer_error | submitted the wrong final year (1848 instead of 1847) | 1 | [task](../../../../tasks_mini/k-4-d-3/task_9.json) / [plan](../../../../plans_mini/k-4-d-3/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_9.log) |
| evidence_available_answer_error | used estimate instead of extracted count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_7.json) / [plan](../../../../plans_mini/k-3-d-2/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_7.log) |
| evidence_available_answer_error | wrong_final_entity_lineage | 1 | [task](../../../../tasks_mini/k-5-d-3/task_11.json) / [plan](../../../../plans_mini/k-5-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-3/task_11.log) |
| extraction_or_parsing_error | selected 1877 from the AMNH page instead of the intended 1869 founding year | 1 | [task](../../../../tasks_mini/k-3-d-4/task_7.json) / [plan](../../../../plans_mini/k-3-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-4/task_7.log) |
| extraction_or_parsing_error | wrong row level aggregation | 1 | [task](../../../../tasks_mini/k-4-d-3/task_10.json) / [plan](../../../../plans_mini/k-4-d-3/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_10.log) |
| extraction_or_parsing_error | wrong year extracted from Watertown source | 1 | [task](../../../../tasks_mini/k-4-d-5/task_1.json) / [plan](../../../../plans_mini/k-4-d-5/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-5/task_1.log) |
| incomplete_evidence_budget_exhausted | charter-school hop truncated before downstream county lookup | 1 | [task](../../../../tasks_mini/k-4-d-3/task_7.json) / [plan](../../../../plans_mini/k-4-d-3/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_7.log) |
| incomplete_evidence_budget_exhausted | hard timeout after extra query | 1 | [task](../../../../tasks_mini/k-6-d-3/task_4.json) / [plan](../../../../plans_mini/k-6-d-3/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-6-d-3/task_4.log) |
| incomplete_evidence_budget_exhausted | hard timeout during repair attempts | 1 | [task](../../../../tasks_mini/k-5-d-1/task_4.json) / [plan](../../../../plans_mini/k-5-d-1/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-1/task_4.log) |
| incomplete_evidence_budget_exhausted | tool budget exhausted before third count | 1 | [task](../../../../tasks_mini/k-2-d-3/task_1.json) / [plan](../../../../plans_mini/k-2-d-3/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| incomplete_evidence_budget_exhausted | tool budget exhausted before verification | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| low_yield_search_loop | dataset discovery loop | 1 | [task](../../../../tasks_mini/k-5-d-4/task_5.json) / [plan](../../../../plans_mini/k-5-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-4/task_5.log) |
| low_yield_search_loop | kept re-searching after source set was already identified | 1 | [task](../../../../tasks_mini/k-4-d-3/task_7.json) / [plan](../../../../plans_mini/k-4-d-3/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_7.log) |
| planning_decomposition_mismatch | intermediate SQL scope mismatch | 1 | [task](../../../../tasks_mini/k-6-d-3/task_4.json) / [plan](../../../../plans_mini/k-6-d-3/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-6-d-3/task_4.log) |
| planning_decomposition_mismatch | mismatched 2021 mental-health aggregation path instead of the authored 2015 OMH clinic step | 1 | [task](../../../../tasks_mini/k-4-d-3/task_9.json) / [plan](../../../../plans_mini/k-4-d-3/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_9.log) |
| planning_decomposition_mismatch | replaced the authored four-year district consistency hop with a county-level minimum query | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| planning_decomposition_mismatch | single-year county totals SQL omitted required multi-year low-income filter | 1 | [task](../../../../tasks_mini/k-4-d-4/task_9.json) / [plan](../../../../plans_mini/k-4-d-4/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-4/task_9.log) |
| planning_decomposition_mismatch | submitted code diverged from authored stepwise computation | 1 | [task](../../../../tasks_mini/k-5-d-1/task_4.json) / [plan](../../../../plans_mini/k-5-d-1/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-1/task_4.log) |
| question_or_constraint_misread | used 2019 average instead of December 2019 threshold | 1 | [task](../../../../tasks_mini/k-4-d-3/task_11.json) / [plan](../../../../plans_mini/k-4-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| same_hop_repetition | repeated single-year county low-income percent query without required GradeLevel and 32-40% filters | 1 | [task](../../../../tasks_mini/k-4-d-4/task_9.json) / [plan](../../../../plans_mini/k-4-d-4/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-4/task_9.log) |
| tool_or_data_blocker | malformed_tool_call | 1 | [task](../../../../tasks_mini/k-3-d-4/task_4.json) / [plan](../../../../plans_mini/k-3-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| tool_or_data_blocker | runner_or_event_loop_exception | 1 | [task](../../../../tasks_mini/k-4-d-4/task_9.json) / [plan](../../../../plans_mini/k-4-d-4/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-4/task_9.log) |
| wrong_scope_or_filter | county lookup drifted away from the intended Whitman/Pullman chain | 1 | [task](../../../../tasks_mini/k-5-d-4/task_7.json) / [plan](../../../../plans_mini/k-5-d-4/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| wrong_scope_or_filter | county/year-only filters instead of Boston-specific computation | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| wrong_scope_or_filter | county_only_filter | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| wrong_scope_or_filter | mis-scoped county/year filter | 1 | [task](../../../../tasks_mini/k-3-d-2/task_7.json) / [plan](../../../../plans_mini/k-3-d-2/task_7.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_7.log) |
| wrong_scope_or_filter | missing_detroit_city_filter_in_postsecondary_query | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_scope_or_filter | omitted STATE=TX filter | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| wrong_scope_or_filter | omitted_city_constraint | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| wrong_scope_or_filter | scope_and_output_shape_mismatch | 1 | [task](../../../../tasks_mini/k-3-d-4/task_4.json) / [plan](../../../../plans_mini/k-3-d-4/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| wrong_scope_or_filter | single_year_sitecounty_instead_of_five_year_cecounty_aps_filter | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| wrong_scope_or_filter | switched_from_lincoln_square_to_loop | 1 | [task](../../../../tasks_mini/k-6-d-3/task_3.json) / [plan](../../../../plans_mini/k-6-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| wrong_scope_or_filter | used Chicago/Santa Monica pair instead of Chicago/Los Angeles | 1 | [task](../../../../tasks_mini/k-4-d-4/task_5.json) / [plan](../../../../plans_mini/k-4-d-4/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-4/task_5.log) |
| wrong_scope_or_filter | wayne_county_used_for_public_school_count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_9.json) / [plan](../../../../plans_mini/k-3-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_scope_or_filter | wrong county branch for last lookup | 1 | [task](../../../../tasks_mini/k-4-d-4/task_6.json) / [plan](../../../../plans_mini/k-4-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-4/task_6.log) |
| wrong_scope_or_filter | wrong district/entity selected | 1 | [task](../../../../tasks_mini/k-5-d-3/task_3.json) / [plan](../../../../plans_mini/k-5-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| wrong_scope_or_filter | wrong filter and metric | 1 | [task](../../../../tasks_mini/k-4-d-3/task_10.json) / [plan](../../../../plans_mini/k-4-d-3/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_10.log) |
| wrong_scope_or_filter | wrong neighborhood branch (Loop instead of Lincoln Square) | 1 | [task](../../../../tasks_mini/k-5-d-3/task_9.json) / [plan](../../../../plans_mini/k-5-d-3/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-3/task_9.log) |
| wrong_scope_or_filter | wrong upstream sector metric | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| wrong_scope_or_filter | wrong ward filter for final count | 1 | [task](../../../../tasks_mini/k-5-d-1/task_3.json) / [plan](../../../../plans_mini/k-5-d-1/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-5-d-1/task_3.log) |
| wrong_scope_or_filter | wrong_city_anchor | 1 | [task](../../../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../../../plans_mini/k-6-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| wrong_source_or_dataset | DFSS history instead of Chicago Police Department source | 1 | [task](../../../../tasks_mini/k-4-d-3/task_6.json) / [plan](../../../../plans_mini/k-4-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| wrong_source_or_dataset | used city pages instead of county-population path | 1 | [task](../../../../tasks_mini/k-4-d-3/task_11.json) / [plan](../../../../plans_mini/k-4-d-3/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-3/task_11.log) |
| wrong_source_or_dataset | used locations open date instead of school-day source | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| wrong_source_or_dataset | wrong APD branch | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |

## Co-occurring Failure Types

| Failure Type Set | Rows |
| --- | --- |
| wrong_scope_or_filter | 8 |
| evidence_available_answer_error | 3 |
| computation_or_aggregation_error | 2 |
| extraction_or_parsing_error | 2 |
| tool_or_data_blocker; wrong_scope_or_filter | 2 |
| wrong_source_or_dataset | 2 |
| computation_or_aggregation_error; extraction_or_parsing_error; incomplete_evidence_budget_exhausted; wrong_scope_or_filter | 1 |
| evidence_available_answer_error; low_yield_search_loop; tool_or_data_blocker | 1 |
| evidence_available_answer_error; planning_decomposition_mismatch; tool_or_data_blocker | 1 |
| evidence_available_answer_error; tool_or_data_blocker | 1 |
| evidence_available_answer_error; tool_or_data_blocker; wrong_scope_or_filter | 1 |
| evidence_available_answer_error; wrong_scope_or_filter | 1 |
| incomplete_evidence_budget_exhausted | 1 |
| incomplete_evidence_budget_exhausted; low_yield_search_loop; tool_or_data_blocker | 1 |
| incomplete_evidence_budget_exhausted; planning_decomposition_mismatch | 1 |
| incomplete_evidence_budget_exhausted; planning_decomposition_mismatch; tool_or_data_blocker | 1 |
| incomplete_evidence_budget_exhausted; planning_decomposition_mismatch; wrong_scope_or_filter | 1 |
| incomplete_evidence_budget_exhausted; tool_or_data_blocker | 1 |
| incomplete_evidence_budget_exhausted; tool_or_data_blocker; wrong_scope_or_filter | 1 |
| incomplete_evidence_budget_exhausted; wrong_scope_or_filter | 1 |
| incomplete_evidence_budget_exhausted; wrong_scope_or_filter; wrong_source_or_dataset | 1 |
| planning_decomposition_mismatch; same_hop_repetition; tool_or_data_blocker | 1 |
| question_or_constraint_misread; wrong_source_or_dataset | 1 |
| tool_or_data_blocker | 1 |

## Representative Evidence

- `tasks_mini/k-2-d-3/task_1.json` `tool_or_data_blocker`/`unsupported_or_oversized_data_access`: Turn 24 | Tool logical error (status=error): {"success": false, "error": "Cannot execute SQL: file is too big (1377 MB >= 500 MB limit).", "dataset_id": "apd-computer-aided-dispatch-incidents", "file_path": "files/row...
- `tasks_mini/k-2-d-3/task_1.json` `incomplete_evidence_budget_exhausted`/`tool budget exhausted before third count`: Turn 31 | Tool result: Tool call cancelled. Tool limit reached (30/30 calls used). You must stop using other tools and immediately call submit_answer with your best current answer and reasoning.; Turn 32 | submit_answ...
- `tasks_mini/k-3-d-2/task_1.json` `wrong_source_or_dataset`/`wrong APD branch`: Turn 1 | Model response #1 [role=assistant block=1 tool_use] pick({"s3_uris": ["s3://lakeqa-yc4103-datalake/datagov/apd-use-of-force/files/rows.txt"], "reason": "The query asks for Austin Police Department 2023 use-of...
- `tasks_mini/k-3-d-2/task_1.json` `wrong_scope_or_filter`/`wrong upstream sector metric`: Turn 9 | Model response #9 [role=assistant block=1 tool_use] query_ideal({"dataset_id": "apd-computer-aided-dispatch-incidents", "file_path": "files/rows.txt", "sql": "SELECT \"Sector\", COUNT(*) AS cnt\nFROM r\nWHERE...
- `tasks_mini/k-3-d-2/task_1.json` `incomplete_evidence_budget_exhausted`/`tool_budget_exhausted`: Turn 31 | Tool result: Tool call cancelled. Tool limit reached (30/30 calls used). You must stop using other tools and immediately call submit_answer with your best current answer and reasoning.; Turn 33 | Model respo...

# Answer Failure Aggregate Report

- Source root: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_answer_failures`
- Event rows: 192
- Trusted event rows: 117
- Events excluded by validation/model-validation: 75

## Counts by Failure Type

| Failure Type | Events |
| --- | --- |
| tool_or_data_blocker | 27 |
| wrong_scope_or_filter | 18 |
| wrong_source_or_dataset | 15 |
| evidence_available_answer_error | 13 |
| incomplete_evidence_early_answer | 11 |
| planning_decomposition_mismatch | 11 |
| extraction_or_parsing_error | 4 |
| incomplete_evidence_budget_exhausted | 4 |
| query_execution_error_loop | 4 |
| schema_or_shape_inspection_loop | 3 |
| low_yield_search_loop | 2 |
| other_or_unclear | 2 |
| question_or_constraint_misread | 2 |
| computation_or_aggregation_error | 1 |

## Counts by Failure Type and Subtype

| Failure Type | Subtype | Events | Representative |
| --- | --- | --- | --- |
| tool_or_data_blocker | data_source_missing_or_unavailable | 7 | [task](../tasks_mini/k-3-d-4/task_4.json) / [plan](../plans_mini/k-3-d-4/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| tool_or_data_blocker | unsupported_or_oversized_data_access | 6 | [task](../tasks_mini/k-3-d-2/task_1.json) / [plan](../plans_mini/k-3-d-2/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| tool_or_data_blocker | tool_status_or_transport_error | 5 | [task](../tasks_mini/k-3-d-2/task_10.json) / [plan](../plans_mini/k-3-d-2/task_10.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| tool_or_data_blocker | tool_budget_exhausted | 4 | [task](../tasks_mini/k-3-d-4/task_2.json) / [plan](../plans_mini/k-3-d-4/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_2.log) |
| tool_or_data_blocker | malformed_tool_call | 3 | [task](../tasks_mini/k-3-d-2/task_6.json) / [plan](../plans_mini/k-3-d-2/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| incomplete_evidence_budget_exhausted | tool_budget_exhausted | 2 | [task](../tasks_mini/k-3-d-3/task_4.json) / [plan](../plans_mini/k-3-d-3/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_4.log) |
| computation_or_aggregation_error | counted counties instead of average intake | 1 | [task](../tasks_mini/k-3-d-3/task_4.json) / [plan](../plans_mini/k-3-d-3/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_4.log) |
| evidence_available_answer_error | fallback placeholder submitted | 1 | [task](../tasks_mini/k-3-d-2/task_9.json) / [plan](../plans_mini/k-3-d-2/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| evidence_available_answer_error | final answer contradicted gathered evidence; submitted Lincoln Belmont instead of Lincoln Square | 1 | [task](../tasks_mini/k-3-d-3/task_2.json) / [plan](../plans_mini/k-3-d-3/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_2.log) |
| evidence_available_answer_error | final answer copied the wrong rounded value after computing the correct average | 1 | [task](../tasks_mini/k-5-d-2/task_7.json) / [plan](../plans_mini/k-5-d-2/task_7.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_7.log) |
| evidence_available_answer_error | final answer ignored the common school already present in the run | 1 | [task](../tasks_mini/k-3-d-3/task_1.json) / [plan](../plans_mini/k-3-d-3/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_1.log) |
| evidence_available_answer_error | misattributed Lincoln University founder/year | 1 | [task](../tasks_mini/k-5-d-3/task_5.json) / [plan](../plans_mini/k-5-d-3/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_5.log) |
| evidence_available_answer_error | selected parent department instead of operating agency | 1 | [task](../tasks_mini/k-3-d-3/task_6.json) / [plan](../plans_mini/k-3-d-3/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_6.log) |
| evidence_available_answer_error | submitted 103 instead of 115 | 1 | [task](../tasks_mini/k-3-d-2/task_11.json) / [plan](../plans_mini/k-3-d-2/task_11.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_11.log) |
| evidence_available_answer_error | submitted 2010 instead of 1624 | 1 | [task](../tasks_mini/k-4-d-2/task_10.json) / [plan](../plans_mini/k-4-d-2/task_10.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_10.log) |
| evidence_available_answer_error | submitted Queens instead of Manhattan | 1 | [task](../tasks_mini/k-5-d-4/task_9.json) / [plan](../plans_mini/k-5-d-4/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_9.log) |
| evidence_available_answer_error | submitted answer contradicted stated arithmetic | 1 | [task](../tasks_mini/k-3-d-2/task_5.json) / [plan](../plans_mini/k-3-d-2/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| evidence_available_answer_error | submitted_zero | 1 | [task](../tasks_mini/k-4-d-2/task_8.json) / [plan](../plans_mini/k-4-d-2/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_8.log) |
| evidence_available_answer_error | wrong final entity | 1 | [task](../tasks_mini/k-5-d-2/task_4.json) / [plan](../plans_mini/k-5-d-2/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_4.log) |
| evidence_available_answer_error | wrong_founder_name | 1 | [task](../tasks_mini/k-5-d-3/task_6.json) / [plan](../plans_mini/k-5-d-3/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_6.log) |
| extraction_or_parsing_error | numeric county codes instead of county names | 1 | [task](../tasks_mini/k-4-d-4/task_11.json) / [plan](../plans_mini/k-4-d-4/task_11.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_11.log) |
| extraction_or_parsing_error | progress-grade column/header mismatch | 1 | [task](../tasks_mini/k-4-d-2/task_1.json) / [plan](../plans_mini/k-4-d-2/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| extraction_or_parsing_error | read mismatched year/metric columns in the performance directory | 1 | [task](../tasks_mini/k-6-d-2/task_1.json) / [plan](../plans_mini/k-6-d-2/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_1.log) |
| extraction_or_parsing_error | selected_city_charter_year_instead_of_town_charter_year | 1 | [task](../tasks_mini/k-3-d-4/task_10.json) / [plan](../plans_mini/k-3-d-4/task_10.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_10.log) |
| incomplete_evidence_budget_exhausted | stopped after common-school stage before neighborhood/material/structure/year hops | 1 | [task](../tasks_mini/k-4-d-3/task_8.json) / [plan](../plans_mini/k-4-d-3/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_8.log) |
| incomplete_evidence_budget_exhausted | tool-call limit exhausted before final answer; submitted [null] | 1 | [task](../tasks_mini/k-4-d-3/task_8.json) / [plan](../plans_mini/k-4-d-3/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_8.log) |
| incomplete_evidence_early_answer | blank_submission_after_insufficient_evidence | 1 | [task](../tasks_mini/k-5-d-4/task_3.json) / [plan](../plans_mini/k-5-d-4/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_3.log) |
| incomplete_evidence_early_answer | incorporation year not retrieved | 1 | [task](../tasks_mini/k-3-d-2/task_1.json) / [plan](../plans_mini/k-3-d-2/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| incomplete_evidence_early_answer | missing_2020_counts | 1 | [task](../tasks_mini/k-7-d-4/task_1.json) / [plan](../plans_mini/k-7-d-4/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-7-d-4/task_1.log) |
| incomplete_evidence_early_answer | placeholder execute call followed by submission of [Unknown] before resolving the remaining lookup | 1 | [task](../tasks_mini/k-5-d-2/task_8.json) / [plan](../plans_mini/k-5-d-2/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_8.log) |
| incomplete_evidence_early_answer | placeholder_submitted | 1 | [task](../tasks_mini/k-7-d-4/task_1.json) / [plan](../plans_mini/k-7-d-4/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-7-d-4/task_1.log) |
| incomplete_evidence_early_answer | premature_error_exit | 1 | [task](../tasks_mini/k-4-d-3/task_1.json) / [plan](../plans_mini/k-4-d-3/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_1.log) |
| incomplete_evidence_early_answer | stopped and submitted without extracting the county rankings | 1 | [task](../tasks_mini/k-4-d-5/task_4.json) / [plan](../plans_mini/k-4-d-5/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_4.log) |
| incomplete_evidence_early_answer | submitted [UNKNOWN] before gathering the later-hop evidence needed to identify the department and first head | 1 | [task](../tasks_mini/k-4-d-3/task_6.json) / [plan](../plans_mini/k-4-d-3/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| incomplete_evidence_early_answer | submitted [Unknown] before resolving the required chain | 1 | [task](../tasks_mini/k-6-d-2/task_1.json) / [plan](../plans_mini/k-6-d-2/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_1.log) |
| incomplete_evidence_early_answer | submitted a blank answer before assembling the required year | 1 | [task](../tasks_mini/k-4-d-5/task_1.json) / [plan](../plans_mini/k-4-d-5/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_1.log) |
| incomplete_evidence_early_answer | submitted the county-seat year without verifying the required school-district establishment year | 1 | [task](../tasks_mini/k-5-d-3/task_3.json) / [plan](../plans_mini/k-5-d-3/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| low_yield_search_loop | repeated off-target county-income source searches | 1 | [task](../tasks_mini/k-3-d-4/task_1.json) / [plan](../plans_mini/k-3-d-4/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_1.log) |
| low_yield_search_loop | repeated searches returned unrelated datasets instead of the identified-student source | 1 | [task](../tasks_mini/k-5-d-3/task_3.json) / [plan](../plans_mini/k-5-d-3/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| other_or_unclear | final submission used [202] and 1846 instead of 1850 | 1 | [task](../tasks_mini/k-4-d-4/task_12.json) / [plan](../plans_mini/k-4-d-4/task_12.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_12.log) |
| other_or_unclear | wrong submitted college | 1 | [task](../tasks_mini/k-4-d-4/task_9.json) / [plan](../plans_mini/k-4-d-4/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_9.log) |
| planning_decomposition_mismatch | county-count inspection instead of threshold computation | 1 | [task](../tasks_mini/k-5-d-4/task_7.json) / [plan](../plans_mini/k-5-d-4/task_7.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_7.log) |
| planning_decomposition_mismatch | distinct-employee 2021 count instead of row-count average | 1 | [task](../tasks_mini/k-5-d-3/task_5.json) / [plan](../plans_mini/k-5-d-3/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_5.log) |
| planning_decomposition_mismatch | first reimbursement query diverged from the ideal decrease-comparison hop | 1 | [task](../tasks_mini/k-5-d-2/task_3.json) / [plan](../plans_mini/k-5-d-2/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_3.log) |
| planning_decomposition_mismatch | grade-check hop used wrong table/path | 1 | [task](../tasks_mini/k-4-d-2/task_1.json) / [plan](../plans_mini/k-4-d-2/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_1.log) |
| planning_decomposition_mismatch | off-target county-level aggregation branch | 1 | [task](../tasks_mini/k-4-d-3/task_9.json) / [plan](../plans_mini/k-4-d-3/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_9.log) |
| planning_decomposition_mismatch | placeholder schema probe instead of planned ranking aggregation | 1 | [task](../tasks_mini/k-6-d-3/task_3.json) / [plan](../plans_mini/k-6-d-3/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| planning_decomposition_mismatch | placeholder_sql | 1 | [task](../tasks_mini/k-4-d-4/task_13.json) / [plan](../plans_mini/k-4-d-4/task_13.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_13.log) |
| planning_decomposition_mismatch | schema_discovery_detour | 1 | [task](../tasks_mini/k-5-d-4/task_6.json) / [plan](../plans_mini/k-5-d-4/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_6.log) |
| planning_decomposition_mismatch | simplified raw-list intersection instead of the authored cleaned-and-ranked chain | 1 | [task](../tasks_mini/k-3-d-3/task_1.json) / [plan](../plans_mini/k-3-d-3/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-3/task_1.log) |
| planning_decomposition_mismatch | started on 2012-2013 progress-report path instead of the authored performance-directory chain | 1 | [task](../tasks_mini/k-6-d-2/task_1.json) / [plan](../plans_mini/k-6-d-2/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_1.log) |
| planning_decomposition_mismatch | used per-county max aggregation instead of the required HSA>80 filter hop | 1 | [task](../tasks_mini/k-5-d-2/task_8.json) / [plan](../plans_mini/k-5-d-2/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_8.log) |
| query_execution_error_loop | JSON repair retry loop | 1 | [task](../tasks_mini/k-3-d-2/task_9.json) / [plan](../plans_mini/k-3-d-2/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| query_execution_error_loop | repeated execution-tool cancellations and repair failures | 1 | [task](../tasks_mini/k-5-d-1/task_2.json) / [plan](../plans_mini/k-5-d-1/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-1/task_2.log) |
| query_execution_error_loop | repeated_sql_repair_failures | 1 | [task](../tasks_mini/k-2-d-3/task_1.json) / [plan](../plans_mini/k-2-d-3/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| query_execution_error_loop | sql_repair_jsondecodeerror | 1 | [task](../tasks_mini/k-4-d-3/task_2.json) / [plan](../plans_mini/k-4-d-3/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| question_or_constraint_misread | aggregation_instruction_misread | 1 | [task](../tasks_mini/k-2-d-3/task_1.json) / [plan](../plans_mini/k-2-d-3/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-2-d-3/task_1.log) |
| question_or_constraint_misread | single_year_only_filter | 1 | [task](../tasks_mini/k-6-d-2/task_2.json) / [plan](../plans_mini/k-6-d-2/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_2.log) |
| schema_or_shape_inspection_loop | generic schema probe instead of count query sequence | 1 | [task](../tasks_mini/k-6-d-3/task_4.json) / [plan](../plans_mini/k-6-d-3/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_4.log) |
| schema_or_shape_inspection_loop | repeated inspect calls stalled extraction | 1 | [task](../tasks_mini/k-5-d-4/task_8.json) / [plan](../plans_mini/k-5-d-4/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_8.log) |
| schema_or_shape_inspection_loop | repeated metadata/publisher-view peeks instead of row tables | 1 | [task](../tasks_mini/k-4-d-5/task_4.json) / [plan](../plans_mini/k-4-d-5/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_4.log) |
| tool_or_data_blocker | ideal_repair_failure | 1 | [task](../tasks_mini/k-4-d-4/task_2.json) / [plan](../plans_mini/k-4-d-4/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_2.log) |
| tool_or_data_blocker | runner_or_event_loop_exception | 1 | [task](../tasks_mini/k-3-d-2/task_8.json) / [plan](../plans_mini/k-3-d-2/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| wrong_scope_or_filter | 2016-only city slice | 1 | [task](../tasks_mini/k-5-d-2/task_4.json) / [plan](../plans_mini/k-5-d-2/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_4.log) |
| wrong_scope_or_filter | all counties instead of Los Angeles County | 1 | [task](../tasks_mini/k-3-d-4/task_4.json) / [plan](../plans_mini/k-3-d-4/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_4.log) |
| wrong_scope_or_filter | broad county aggregation instead of Sacramento County-specific filter | 1 | [task](../tasks_mini/k-3-d-2/task_5.json) / [plan](../plans_mini/k-3-d-2/task_5.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| wrong_scope_or_filter | county selection mismatch | 1 | [task](../tasks_mini/k-3-d-2/task_8.json) / [plan](../plans_mini/k-3-d-2/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| wrong_scope_or_filter | district-office query used CBSA 7 instead of Lansing CBSA 29620 | 1 | [task](../tasks_mini/k-3-d-2/task_6.json) / [plan](../plans_mini/k-3-d-2/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_6.log) |
| wrong_scope_or_filter | missed required CPS Performance Policy Level filter | 1 | [task](../tasks_mini/k-4-d-4/task_2.json) / [plan](../plans_mini/k-4-d-4/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_2.log) |
| wrong_scope_or_filter | overbroad candidate set still included HAYS | 1 | [task](../tasks_mini/k-4-d-4/task_12.json) / [plan](../plans_mini/k-4-d-4/task_12.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_12.log) |
| wrong_scope_or_filter | queried ACCESS2_AdjPrev and a broad CT city list instead of New Haven/Bridgeport ACCESS2_CrudePrev | 1 | [task](../tasks_mini/k-5-d-2/task_8.json) / [plan](../plans_mini/k-5-d-2/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_8.log) |
| wrong_scope_or_filter | single-year checks instead of cross-year intersection | 1 | [task](../tasks_mini/k-4-d-4/task_9.json) / [plan](../plans_mini/k-4-d-4/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_9.log) |
| wrong_scope_or_filter | used DEPARTMENT DESCRIPTION instead of DEPARTMENT NUMBER in the first-hop appropriations query | 1 | [task](../tasks_mini/k-4-d-3/task_6.json) / [plan](../plans_mini/k-4-d-3/task_6.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| wrong_scope_or_filter | used Death County with loose 2020 matching instead of Residence County with >200 cutoff | 1 | [task](../tasks_mini/k-5-d-2/task_8.json) / [plan](../plans_mini/k-5-d-2/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_8.log) |
| wrong_scope_or_filter | wrong 4-year August cohort and DBN output instead of 4 Year June school_name | 1 | [task](../tasks_mini/k-4-d-2/task_10.json) / [plan](../plans_mini/k-4-d-2/task_10.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_10.log) |
| wrong_scope_or_filter | wrong Detroit/Wayne slice | 1 | [task](../tasks_mini/k-3-d-2/task_9.json) / [plan](../plans_mini/k-3-d-2/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_9.log) |
| wrong_scope_or_filter | wrong branch/geography endpoint | 1 | [task](../tasks_mini/k-5-d-3/task_9.json) / [plan](../plans_mini/k-5-d-3/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_9.log) |
| wrong_scope_or_filter | wrong city/county branch: Rochester in Monroe County instead of Syracuse/Onondaga County | 1 | [task](../tasks_mini/k-4-d-3/task_9.json) / [plan](../plans_mini/k-4-d-3/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_9.log) |
| wrong_scope_or_filter | wrong file path for header/schema lookup | 1 | [task](../tasks_mini/k-5-d-4/task_8.json) / [plan](../plans_mini/k-5-d-4/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_8.log) |
| wrong_scope_or_filter | wrong university/entity selected | 1 | [task](../tasks_mini/k-3-d-4/task_8.json) / [plan](../plans_mini/k-3-d-4/task_8.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_8.log) |
| wrong_scope_or_filter | wrong_entity_chain | 1 | [task](../tasks_mini/k-5-d-3/task_15.json) / [plan](../plans_mini/k-5-d-3/task_15.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_15.log) |
| wrong_source_or_dataset | ambiguous_dataset_id | 1 | [task](../tasks_mini/k-5-d-3/task_13.json) / [plan](../plans_mini/k-5-d-3/task_13.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_13.log) |
| wrong_source_or_dataset | apd-use-of-force instead of apd-searches-by-type | 1 | [task](../tasks_mini/k-3-d-2/task_1.json) / [plan](../plans_mini/k-3-d-2/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| wrong_source_or_dataset | broad_searches_returned_unrelated_datasets | 1 | [task](../tasks_mini/k-6-d-3/task_1.json) / [plan](../plans_mini/k-6-d-3/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_1.log) |
| wrong_source_or_dataset | catalog metadata file instead of underlying row dataset | 1 | [task](../tasks_mini/k-6-d-3/task_3.json) / [plan](../plans_mini/k-6-d-3/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_3.log) |
| wrong_source_or_dataset | late WSIF drift | 1 | [task](../tasks_mini/k-4-d-4/task_9.json) / [plan](../plans_mini/k-4-d-4/task_9.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_9.log) |
| wrong_source_or_dataset | nibrs_offense_dataset | 1 | [task](../tasks_mini/k-5-d-1/task_1.json) / [plan](../plans_mini/k-5-d-1/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-1/task_1.log) |
| wrong_source_or_dataset | pivoted_to_2010_2016_school_safety_report | 1 | [task](../tasks_mini/k-4-d-3/task_2.json) / [plan](../plans_mini/k-4-d-3/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_2.log) |
| wrong_source_or_dataset | used 2022-23 source instead of current source | 1 | [task](../tasks_mini/k-5-d-3/task_14.json) / [plan](../plans_mini/k-5-d-3/task_14.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_14.log) |
| wrong_source_or_dataset | used CAD incidents instead of apd-use-of-force | 1 | [task](../tasks_mini/k-5-d-1/task_2.json) / [plan](../plans_mini/k-5-d-1/task_2.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-1/task_2.log) |
| wrong_source_or_dataset | used crime-data neighborhood clusters instead of intended Wikipedia neighborhood list | 1 | [task](../tasks_mini/k-3-d-4/task_1.json) / [plan](../plans_mini/k-3-d-4/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_1.log) |
| wrong_source_or_dataset | used current postsecondary dataset for county lookup | 1 | [task](../tasks_mini/k-6-d-3/task_4.json) / [plan](../plans_mini/k-6-d-3/task_4.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-3/task_4.log) |
| wrong_source_or_dataset | used school-neighborhood-poverty-estimates instead of the intended school-locations source | 1 | [task](../tasks_mini/k-3-d-4/task_7.json) / [plan](../plans_mini/k-3-d-4/task_7.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_7.log) |
| wrong_source_or_dataset | wrong biodiversity file path and schema column selection | 1 | [task](../tasks_mini/k-4-d-5/task_1.json) / [plan](../plans_mini/k-4-d-5/task_1.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_1.log) |
| wrong_source_or_dataset | wrong_dataset_version | 1 | [task](../tasks_mini/k-4-d-4/task_13.json) / [plan](../plans_mini/k-4-d-4/task_13.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_13.log) |
| wrong_source_or_dataset | wsif_and_single_year_assessment | 1 | [task](../tasks_mini/k-3-d-4/task_3.json) / [plan](../plans_mini/k-3-d-4/task_3.json) / [log](../logs/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_3.log) |

## Co-occurring Failure Types

| Failure Type Set | Rows |
| --- | --- |
| evidence_available_answer_error | 6 |
| tool_or_data_blocker | 6 |
| tool_or_data_blocker; wrong_source_or_dataset | 5 |
| tool_or_data_blocker; wrong_scope_or_filter | 4 |
| incomplete_evidence_early_answer | 3 |
| evidence_available_answer_error; planning_decomposition_mismatch | 2 |
| evidence_available_answer_error; wrong_scope_or_filter | 2 |
| extraction_or_parsing_error | 2 |
| planning_decomposition_mismatch; tool_or_data_blocker | 2 |
| planning_decomposition_mismatch; wrong_source_or_dataset | 2 |
| wrong_scope_or_filter | 2 |
| computation_or_aggregation_error; incomplete_evidence_budget_exhausted | 1 |
| evidence_available_answer_error; query_execution_error_loop; wrong_scope_or_filter | 1 |
| evidence_available_answer_error; tool_or_data_blocker | 1 |
| evidence_available_answer_error; tool_or_data_blocker; wrong_scope_or_filter | 1 |
| extraction_or_parsing_error; incomplete_evidence_early_answer; planning_decomposition_mismatch | 1 |
| extraction_or_parsing_error; planning_decomposition_mismatch | 1 |
| incomplete_evidence_budget_exhausted | 1 |
| incomplete_evidence_budget_exhausted; tool_or_data_blocker; wrong_scope_or_filter | 1 |
| incomplete_evidence_early_answer; low_yield_search_loop | 1 |
| incomplete_evidence_early_answer; planning_decomposition_mismatch; wrong_scope_or_filter | 1 |
| incomplete_evidence_early_answer; schema_or_shape_inspection_loop | 1 |
| incomplete_evidence_early_answer; tool_or_data_blocker; wrong_source_or_dataset | 1 |
| incomplete_evidence_early_answer; wrong_scope_or_filter | 1 |
| incomplete_evidence_early_answer; wrong_source_or_dataset | 1 |
| low_yield_search_loop; wrong_source_or_dataset | 1 |
| other_or_unclear; wrong_scope_or_filter | 1 |
| other_or_unclear; wrong_scope_or_filter; wrong_source_or_dataset | 1 |
| planning_decomposition_mismatch | 1 |
| planning_decomposition_mismatch; wrong_scope_or_filter | 1 |
| query_execution_error_loop; question_or_constraint_misread | 1 |
| query_execution_error_loop; tool_or_data_blocker; wrong_source_or_dataset | 1 |
| query_execution_error_loop; wrong_source_or_dataset | 1 |
| question_or_constraint_misread; tool_or_data_blocker | 1 |
| schema_or_shape_inspection_loop; tool_or_data_blocker; wrong_source_or_dataset | 1 |
| schema_or_shape_inspection_loop; wrong_scope_or_filter | 1 |
| wrong_source_or_dataset | 1 |

## Representative Evidence

- `tasks_mini/k-2-d-3/task_1.json` `question_or_constraint_misread`/`aggregation_instruction_misread`: Turn 7 | Model response #1 [role=assistant block=1 tool_use] query_ideal({"dataset_id": "nopd-use-of-force-incidents", "file_path": "files/rows.txt", "intent": "Compute, for year 2022, the maximum number of incidents...
- `tasks_mini/k-2-d-3/task_1.json` `query_execution_error_loop`/`repeated_sql_repair_failures`: Turn 7 | WARNING | strands_evaluation.instrumentation.agent_plugins | Tool logical error (status=error): {"success": false, "error": "SQL repair failed: JSONDecodeError: Unterminated string starting at: line 1 column...
- `tasks_mini/k-3-d-2/task_1.json` `tool_or_data_blocker`/`unsupported_or_oversized_data_access`: Turn 6 | query_ideal on apd-computer-aided-dispatch-incidents failed because the file was too big to execute SQL on.; Turn 8 | peek_file showed apd-computer-aided-dispatch-incidents rows.txt is about 1.44 GB and liste...
- `tasks_mini/k-3-d-2/task_1.json` `wrong_source_or_dataset`/`apd-use-of-force instead of apd-searches-by-type`: Turn 20 | execute_ideal used apd-use-of-force to compute the top sector for 2023 excluding Unknown.
- `tasks_mini/k-3-d-2/task_1.json` `incomplete_evidence_early_answer`/`incorporation year not retrieved`: Turn 22 | execute_ideal for Austin incorporation year printed a placeholder instead of computing the year.

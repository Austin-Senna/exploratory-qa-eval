# Answer Failure Report

- Source root: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_answer_failures`
- Event rows: 52
- Trusted event rows: 36
- Non-correct eval rows: 31
- Events excluded by validation/model-validation: 16

## Counts by Failure Type

| Failure Type | Events |
| --- | --- |
| evidence_available_answer_error | 11 |
| wrong_source_or_scope | 9 |
| planning_decomposition_mismatch | 3 |
| tool_or_data_blocker | 3 |
| computation_or_aggregation_error | 2 |
| incomplete_evidence_early_answer | 2 |
| incomplete_evidence_not_enough_turns | 2 |
| question_or_constraint_misread | 2 |
| low_yield_search_loop | 1 |
| same_hop_repetition | 1 |

## Counts by Failure Type and Subtype

| Failure Type | Subtype | Events | Representative |
| --- | --- | --- | --- |
| incomplete_evidence_not_enough_turns | turn_or_time_budget_exhausted | 2 | [task](../../../../tasks_mini/k-5-d-4/task_2.json) / [plan](../../../../plans_mini/k-5-d-4/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) |
| tool_or_data_blocker | tool_budget_exhausted | 2 | [task](../../../../tasks_mini/k-4-d-4/task_11.json) / [plan](../../../../plans_mini/k-4-d-4/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_11.log) |
| computation_or_aggregation_error | computed 279/299 and rounded to 1 instead of the authored ratio | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| computation_or_aggregation_error | partial-count peak-year ranking | 1 | [task](../../../../tasks_mini/k-4-d-2/task_9.json) / [plan](../../../../plans_mini/k-4-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_9.log) |
| evidence_available_answer_error | computed 13 but submitted 30 | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| evidence_available_answer_error | final payload mismatched reasoning | 1 | [task](../../../../tasks_mini/k-4-d-5/task_4.json) / [plan](../../../../plans_mini/k-4-d-5/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_4.log) |
| evidence_available_answer_error | final year mismatch after inconsistent reasoning | 1 | [task](../../../../tasks_mini/k-5-d-3/task_2.json) / [plan](../../../../plans_mini/k-5-d-3/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_2.log) |
| evidence_available_answer_error | selected the first constable name instead of the superintendent/head name | 1 | [task](../../../../tasks_mini/k-4-d-3/task_6.json) / [plan](../../../../plans_mini/k-4-d-3/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-3/task_6.log) |
| evidence_available_answer_error | submitted -7 instead of 10 | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| evidence_available_answer_error | submitted 1889 for Fort Worth ISD instead of the correct 1916 | 1 | [task](../../../../tasks_mini/k-5-d-3/task_3.json) / [plan](../../../../plans_mini/k-5-d-3/task_3.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-3/task_3.log) |
| evidence_available_answer_error | submitted wrong-area count unchanged | 1 | [task](../../../../tasks_mini/k-4-d-2/task_9.json) / [plan](../../../../plans_mini/k-4-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_9.log) |
| evidence_available_answer_error | submitted_value_disagrees_with_last_computation | 1 | [task](../../../../tasks_mini/k-5-d-4/task_6.json) / [plan](../../../../plans_mini/k-5-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_6.log) |
| evidence_available_answer_error | swapped source-backed bay name | 1 | [task](../../../../tasks_mini/k-5-d-2/task_5.json) / [plan](../../../../plans_mini/k-5-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-2/task_5.log) |
| evidence_available_answer_error | wrong final subtraction result | 1 | [task](../../../../tasks_mini/k-7-d-4/task_1.json) / [plan](../../../../plans_mini/k-7-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-7-d-4/task_1.log) |
| evidence_available_answer_error | wrong_public_school_count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_5.json) / [plan](../../../../plans_mini/k-3-d-2/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_5.log) |
| incomplete_evidence_early_answer | (none) | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| incomplete_evidence_early_answer | premature answer before county-income lookup | 1 | [task](../../../../tasks_mini/k-3-d-4/task_1.json) / [plan](../../../../plans_mini/k-3-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_1.log) |
| low_yield_search_loop | zero_row_sql_loop | 1 | [task](../../../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../../../plans_mini/k-6-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |
| planning_decomposition_mismatch | cross_year_averaging_drift | 1 | [task](../../../../tasks_mini/k-5-d-4/task_2.json) / [plan](../../../../plans_mini/k-5-d-4/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) |
| planning_decomposition_mismatch | diverged from authored fixed top-five county set | 1 | [task](../../../../tasks_mini/k-7-d-4/task_1.json) / [plan](../../../../plans_mini/k-7-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-7-d-4/task_1.log) |
| planning_decomposition_mismatch | schema/parsing detour instead of required county-filtering hops | 1 | [task](../../../../tasks_mini/k-4-d-4/task_11.json) / [plan](../../../../plans_mini/k-4-d-4/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_11.log) |
| question_or_constraint_misread | omitted ProgramYear filter and used generic top-N county count | 1 | [task](../../../../tasks_mini/k-4-d-5/task_5.json) / [plan](../../../../plans_mini/k-4-d-5/task_5.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-5/task_5.log) |
| question_or_constraint_misread | used `Used Taser(s) = 1` instead of `Used Taser(s) > 0` | 1 | [task](../../../../tasks_mini/k-3-d-2/task_1.json) / [plan](../../../../plans_mini/k-3-d-2/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_1.log) |
| same_hop_repetition | repeated ward grep extraction | 1 | [task](../../../../tasks_mini/k-3-d-4/task_1.json) / [plan](../../../../plans_mini/k-3-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-4/task_1.log) |
| tool_or_data_blocker | missing_or_malformed_log | 1 | [task](../../../../tasks_mini/k-3-d-2/task_11.json) / [plan](../../../../plans_mini/k-3-d-2/task_11.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_11.log) |
| wrong_source_or_scope | dropped city constraint from public-school count | 1 | [task](../../../../tasks_mini/k-3-d-2/task_10.json) / [plan](../../../../plans_mini/k-3-d-2/task_10.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_10.log) |
| wrong_source_or_scope | missing Boston city constraint | 1 | [task](../../../../tasks_mini/k-3-d-2/task_8.json) / [plan](../../../../plans_mini/k-3-d-2/task_8.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-3-d-2/task_8.log) |
| wrong_source_or_scope | used APD searches table instead of council voting record for earliest year | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| wrong_source_or_scope | used KML data.txt school source/version instead of authored public-school source | 1 | [task](../../../../tasks_mini/k-4-d-2/task_4.json) / [plan](../../../../plans_mini/k-4-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_4.log) |
| wrong_source_or_scope | used OPEN_DATE from locations file instead of school-day source | 1 | [task](../../../../tasks_mini/k-4-d-4/task_1.json) / [plan](../../../../plans_mini/k-4-d-4/task_1.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-4/task_1.log) |
| wrong_source_or_scope | wrong DUI area branch | 1 | [task](../../../../tasks_mini/k-4-d-2/task_9.json) / [plan](../../../../plans_mini/k-4-d-2/task_9.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-4-d-2/task_9.log) |
| wrong_source_or_scope | wrong_city_branch | 1 | [task](../../../../tasks_mini/k-5-d-4/task_2.json) / [plan](../../../../plans_mini/k-5-d-4/task_2.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_2.log) |
| wrong_source_or_scope | wrong_field_and_filter_substitution | 1 | [task](../../../../tasks_mini/k-5-d-4/task_6.json) / [plan](../../../../plans_mini/k-5-d-4/task_6.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-5-d-4/task_6.log) |
| wrong_source_or_scope | wrong_year_branch | 1 | [task](../../../../tasks_mini/k-6-d-2/task_4.json) / [plan](../../../../plans_mini/k-6-d-2/task_4.json) / [log](../../../../logs/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/tasks_mini/k-6-d-2/task_4.log) |

## Co-occurring Failure Types

| Failure Type Set | Rows |
| --- | --- |
| evidence_available_answer_error | 6 |
| evidence_available_answer_error; wrong_source_or_scope | 2 |
| tool_or_data_blocker | 2 |
| wrong_source_or_scope | 2 |
| computation_or_aggregation_error; evidence_available_answer_error; wrong_source_or_scope | 1 |
| computation_or_aggregation_error; wrong_source_or_scope | 1 |
| evidence_available_answer_error; planning_decomposition_mismatch | 1 |
| evidence_available_answer_error; question_or_constraint_misread | 1 |
| incomplete_evidence_early_answer; question_or_constraint_misread | 1 |
| incomplete_evidence_early_answer; same_hop_repetition | 1 |
| incomplete_evidence_not_enough_turns; low_yield_search_loop; wrong_source_or_scope | 1 |
| incomplete_evidence_not_enough_turns; planning_decomposition_mismatch; wrong_source_or_scope | 1 |
| planning_decomposition_mismatch; tool_or_data_blocker | 1 |

## Representative Evidence

- `tasks_mini/k-3-d-2/task_1.json` `question_or_constraint_misread`/`used `Used Taser(s) = 1` instead of `Used Taser(s) > 0``: Turn 20 | query_ideal semantic judge found no equivalent record reason="No authored record matches: the candidate counts incidents in 2023 with Used Taser(s) > 0 in council district 1, while the submitted SQL counts r...
- `tasks_mini/k-3-d-2/task_1.json` `incomplete_evidence_early_answer`/`(none)`: Turn 35 | submit_answer({"answer": "[2]", "reasoning": "Sector = Charlie (from searches dataset). Top council district in Charlie in 2023 was District 1. Estimated number of 2023 use-of-force incidents in District 1 w...
- `tasks_mini/k-3-d-2/task_10.json` `wrong_source_or_scope`/`dropped city constraint from public-school count`: Turn 5 | Model response #5 [role=assistant block=1 tool_use] query_ideal({"dataset_id": "public-school-locations-current-23297", "file_path": "files/data-oyCYxF.txt", "sql": "SELECT COUNT(*) AS public_count FROM t WHE...
- `tasks_mini/k-3-d-2/task_11.json` `tool_or_data_blocker`/`missing_or_malformed_log`: Turn 5 | Model response #5 [role=assistant block=1 tool_use] peek_file({"s3_uri": "wikipedia/Basin,_Wyoming/content.txt"}) [toolUseId=call_igxLTK2c8tOz8Lfd7G203NUY]; Turn 10 | DEBUG | strands_evaluation.instrumentatio...
- `tasks_mini/k-3-d-2/task_5.json` `evidence_available_answer_error`/`wrong_public_school_count`: Turn 8 | Model response #8 [role=assistant block=1 tool_use] parse_xml_records({"dataset_id": "public-school-locations-current-23297", "file_path": "files/data.txt", "record_tag": "Placemark", "fields": ["NMCNTY", "CI...

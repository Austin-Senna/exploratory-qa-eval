# Combined Answer-Failure Report

Source root: `results_semantic_answer_failures`
Combined CSV: `combined_answer_failure_events.csv`
Total answer-failure events: 1828

## Counts by Model

| Model | Events |
| --- | --- |
| gpt-5-mini | 586 |
| gpt-5.4-nano | 1242 |

## Counts by Figure Group

| Figure Group | Events | Events by Model |
| --- | --- | --- |
| Source/scope errors | 396 | gpt-5-mini: 149; gpt-5.4-nano: 247 |
| Answer/finalization failures | 299 | gpt-5-mini: 110; gpt-5.4-nano: 189 |
| Tool/data blockers | 252 | gpt-5-mini: 73; gpt-5.4-nano: 179 |
| Turn-waste loops | 249 | gpt-5-mini: 45; gpt-5.4-nano: 204 |
| Incomplete evidence | 216 | gpt-5-mini: 56; gpt-5.4-nano: 160 |
| Planning/trajectory mismatch | 167 | gpt-5-mini: 35; gpt-5.4-nano: 132 |
| Computation errors | 149 | gpt-5-mini: 72; gpt-5.4-nano: 77 |
| Execution/extraction errors | 86 | gpt-5-mini: 40; gpt-5.4-nano: 46 |
| Other/unclear | 14 | gpt-5-mini: 6; gpt-5.4-nano: 8 |

## Counts by Failure Type

| Figure Group | Failure Type | Events | Events by Model |
| --- | --- | --- | --- |
| Source/scope errors | wrong_source_or_scope | 396 | gpt-5-mini: 149; gpt-5.4-nano: 247 |
| Answer/finalization failures | evidence_available_answer_error | 299 | gpt-5-mini: 110; gpt-5.4-nano: 189 |
| Tool/data blockers | tool_or_data_blocker | 252 | gpt-5-mini: 73; gpt-5.4-nano: 179 |
| Computation errors | computation_or_aggregation_error | 149 | gpt-5-mini: 72; gpt-5.4-nano: 77 |
| Turn-waste loops | query_execution_error_loop | 146 | gpt-5-mini: 32; gpt-5.4-nano: 114 |
| Incomplete evidence | incomplete_evidence_early_answer | 109 | gpt-5-mini: 5; gpt-5.4-nano: 104 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | 107 | gpt-5-mini: 51; gpt-5.4-nano: 56 |
| Planning/trajectory mismatch | question_or_constraint_misread | 93 | gpt-5-mini: 22; gpt-5.4-nano: 71 |
| Execution/extraction errors | extraction_or_parsing_error | 86 | gpt-5-mini: 40; gpt-5.4-nano: 46 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | 74 | gpt-5-mini: 13; gpt-5.4-nano: 61 |
| Turn-waste loops | low_yield_search_loop | 52 | gpt-5-mini: 8; gpt-5.4-nano: 44 |
| Turn-waste loops | schema_or_shape_inspection_loop | 51 | gpt-5-mini: 5; gpt-5.4-nano: 46 |
| Other/unclear | semantic_or_gold_label_issue | 8 | gpt-5-mini: 4; gpt-5.4-nano: 4 |
| Other/unclear | other_or_unclear | 6 | gpt-5-mini: 2; gpt-5.4-nano: 4 |

## Counts by Failure Type and Subtype

| Figure Group | Failure Type | Subtype | Events | Events by Model |
| --- | --- | --- | --- | --- |
| Tool/data blockers | tool_or_data_blocker | unsupported_or_oversized_data_access | 66 | gpt-5-mini: 14; gpt-5.4-nano: 52 |
| Tool/data blockers | tool_or_data_blocker | tool_budget_exhausted | 60 | gpt-5-mini: 36; gpt-5.4-nano: 24 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | tool_budget_exhausted | 53 | gpt-5-mini: 30; gpt-5.4-nano: 23 |
| Tool/data blockers | tool_or_data_blocker | data_source_missing_or_unavailable | 45 | gpt-5-mini: 5; gpt-5.4-nano: 40 |
| Tool/data blockers | tool_or_data_blocker | ideal_repair_failure | 40 | gpt-5-mini: 2; gpt-5.4-nano: 38 |
| Turn-waste loops | query_execution_error_loop | ideal_repair_failure | 34 | gpt-5-mini: 7; gpt-5.4-nano: 27 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | turn_or_time_budget_exhausted | 26 | gpt-5-mini: 13; gpt-5.4-nano: 13 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_answer | 17 | gpt-5-mini: 10; gpt-5.4-nano: 7 |
| Tool/data blockers | tool_or_data_blocker | tool_status_or_transport_error | 13 | gpt-5-mini: 1; gpt-5.4-nano: 12 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_version | 10 | gpt-5-mini: 9; gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | placeholder_submission | 9 | gpt-5.4-nano: 9 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_entity | 9 | gpt-5-mini: 2; gpt-5.4-nano: 7 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_year | 8 | gpt-5-mini: 4; gpt-5.4-nano: 4 |
| Source/scope errors | wrong_source_or_scope | wrong_county_branch | 8 | gpt-5-mini: 1; gpt-5.4-nano: 7 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_submission | 7 | gpt-5-mini: 1; gpt-5.4-nano: 6 |
| Incomplete evidence | incomplete_evidence_early_answer | placeholder_submission | 7 | gpt-5.4-nano: 7 |
| Source/scope errors | wrong_source_or_scope | missing_city_filter | 7 | gpt-5-mini: 6; gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_family | 7 | gpt-5-mini: 1; gpt-5.4-nano: 6 |
| Tool/data blockers | tool_or_data_blocker | malformed_tool_call | 7 | gpt-5-mini: 1; gpt-5.4-nano: 6 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_value | 6 | gpt-5-mini: 3; gpt-5.4-nano: 3 |
| Incomplete evidence | incomplete_evidence_early_answer | (none) | 6 | gpt-5.4-nano: 6 |
| Computation errors | computation_or_aggregation_error | arithmetic_miscalculation | 5 | gpt-5-mini: 1; gpt-5.4-nano: 4 |
| Source/scope errors | wrong_source_or_scope | wrong_city_branch | 5 | gpt-5-mini: 5 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_choice | 4 | gpt-5-mini: 2; gpt-5.4-nano: 2 |
| Source/scope errors | wrong_source_or_scope | wrong_community_area_lookup | 4 | gpt-5-mini: 2; gpt-5.4-nano: 2 |
| Source/scope errors | wrong_source_or_scope | wrong_school_branch | 4 | gpt-5-mini: 2; gpt-5.4-nano: 2 |
| Tool/data blockers | tool_or_data_blocker | runner_or_event_loop_exception | 4 | gpt-5-mini: 4 |
| Answer/finalization failures | evidence_available_answer_error | final_answer_mismatch | 3 | gpt-5-mini: 1; gpt-5.4-nano: 2 |
| Answer/finalization failures | evidence_available_answer_error | submitted_wrong_year | 3 | gpt-5-mini: 1; gpt-5.4-nano: 2 |
| Answer/finalization failures | evidence_available_answer_error | wrong_entity_selected | 3 | gpt-5-mini: 1; gpt-5.4-nano: 2 |
| Answer/finalization failures | evidence_available_answer_error | wrong_year_submitted | 3 | gpt-5.4-nano: 3 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_blank_submission | 3 | gpt-5.4-nano: 3 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_fallback_submission | 3 | gpt-5.4-nano: 3 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_unknown_submission | 3 | gpt-5.4-nano: 3 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | (none) | 3 | gpt-5-mini: 2; gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped_required_final_hop | 3 | gpt-5.4-nano: 3 |
| Source/scope errors | wrong_source_or_scope | dropped_city_filter | 3 | gpt-5-mini: 1; gpt-5.4-nano: 2 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset | 3 | gpt-5-mini: 2; gpt-5.4-nano: 1 |
| Tool/data blockers | tool_or_data_blocker | turn_or_time_budget_exhausted | 3 | gpt-5-mini: 2; gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_no_match_searches | 3 | gpt-5-mini: 2; gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_no_result_searches | 3 | gpt-5.4-nano: 3 |
| Turn-waste loops | query_execution_error_loop | ideal_repair_jsondecodeerror | 3 | gpt-5.4-nano: 3 |
| Turn-waste loops | query_execution_error_loop | sql_repair_jsondecodeerror | 3 | gpt-5.4-nano: 3 |
| Turn-waste loops | query_execution_error_loop | xml_json_tool_mismatch | 3 | gpt-5-mini: 1; gpt-5.4-nano: 2 |
| Answer/finalization failures | evidence_available_answer_error | premature_unable_to_determine | 2 | gpt-5.4-nano: 2 |
| Answer/finalization failures | evidence_available_answer_error | propagated_wrong_intermediate_answer | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_wrong_final_answer | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_wrong_final_year | 2 | gpt-5-mini: 2 |
| Answer/finalization failures | evidence_available_answer_error | wrong_branch_selected | 2 | gpt-5-mini: 2 |
| Answer/finalization failures | evidence_available_answer_error | wrong_department_head | 2 | gpt-5.4-nano: 2 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_answer_from_wrong_intermediate_count | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_answer_selected | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_answer_submission | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_answer_submitted | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_chain | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_selection | 2 | gpt-5.4-nano: 2 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_synthesis | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_year_submitted | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_founder_name | 2 | gpt-5.4-nano: 2 |
| Answer/finalization failures | evidence_available_answer_error | wrong_incorporation_year | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_person_selected | 2 | gpt-5.4-nano: 2 |
| Answer/finalization failures | evidence_available_answer_error | wrong_value_submitted | 2 | gpt-5.4-nano: 2 |
| Answer/finalization failures | evidence_available_answer_error | wrong_year_selected | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_aggregation_shape | 2 | gpt-5.4-nano: 2 |
| Computation errors | computation_or_aggregation_error | wrong_branch_intersection | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_intersection_set | 2 | gpt-5.4-nano: 2 |
| Computation errors | computation_or_aggregation_error | wrong_postsecondary_count | 2 | gpt-5-mini: 2 |
| Execution/extraction errors | extraction_or_parsing_error | county_fips_used_instead_of_county_name | 2 | gpt-5.4-nano: 2 |
| Execution/extraction errors | extraction_or_parsing_error | sitecounty_instead_of_cecounty | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_founding_year_extracted | 2 | gpt-5-mini: 2 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_fallback | 2 | gpt-5.4-nano: 2 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_placeholder_submission | 2 | gpt-5.4-nano: 2 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_submission | 2 | gpt-5.4-nano: 2 |
| Other/unclear | other_or_unclear | placeholder_submission_after_blocker | 2 | gpt-5.4-nano: 2 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | diverged_from_required_hop_chain | 2 | gpt-5.4-nano: 2 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped_required_hops | 2 | gpt-5.4-nano: 2 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | stuck_on_first_hop | 2 | gpt-5.4-nano: 2 |
| Source/scope errors | wrong_source_or_scope | county_mismatch | 2 | gpt-5.4-nano: 2 |
| Source/scope errors | wrong_source_or_scope | county_only_public_school_count | 2 | gpt-5-mini: 2 |
| Source/scope errors | wrong_source_or_scope | countywide_instead_of_city_subset | 2 | gpt-5-mini: 2 |
| Source/scope errors | wrong_source_or_scope | countywide_public_school_count | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | dataset_version_drift | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | irrelevant_dataset_search | 2 | gpt-5.4-nano: 2 |
| Source/scope errors | wrong_source_or_scope | metadata_file_instead_of_rows | 2 | gpt-5.4-nano: 2 |
| Source/scope errors | wrong_source_or_scope | neighborhood_lookup_from_wrong_dataset | 2 | gpt-5.4-nano: 2 |
| Source/scope errors | wrong_source_or_scope | source_selection | 2 | gpt-5.4-nano: 2 |
| Source/scope errors | wrong_source_or_scope | wrong_birthplace_branch | 2 | gpt-5.4-nano: 2 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_branch | 2 | gpt-5.4-nano: 2 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_year | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_year_branch | 2 | gpt-5.4-nano: 2 |
| Source/scope errors | wrong_source_or_scope | wrong_entity_branch | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_file_variant | 2 | gpt-5.4-nano: 2 |
| Source/scope errors | wrong_source_or_scope | wrong_neighborhood_or_park_branch | 2 | gpt-5-mini: 2 |
| Source/scope errors | wrong_source_or_scope | wrong_terminus_city | 2 | gpt-5-mini: 2 |
| Source/scope errors | wrong_source_or_scope | year_scope_mismatch | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | irrelevant_dataset_search | 2 | gpt-5.4-nano: 2 |
| Turn-waste loops | low_yield_search_loop | repeated_dataset_not_found_searches | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | malformed_tool_call | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_binder_errors | 2 | gpt-5.4-nano: 2 |
| Turn-waste loops | query_execution_error_loop | repeated_sql_repair_jsondecode | 2 | gpt-5.4-nano: 2 |
| Turn-waste loops | query_execution_error_loop | semantic_mismatch_and_repair_failure | 2 | gpt-5.4-nano: 2 |
| Turn-waste loops | query_execution_error_loop | semantic_query_repair_loop | 2 | gpt-5.4-nano: 2 |
| Answer/finalization failures | evidence_available_answer_error | aborted_with_unknown_answer | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | accepted_invalid_candidate | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | answer_submission_mismatch | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | answer_transcription_error | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | blank_or_null_submission | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | blank_submission_after_giveup | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | blank_submission_after_relevant_data_found | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | blank_submission_after_relevant_evidence_was_available | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | contradictory_final_submission | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | correct reasoning, wrong submitted answer | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | correct_fact_ignored_at_submission | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | default_placeholder_submission | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | empty_placeholder_submission | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | estimated_answer_after_tool_limit | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | estimated_value_used | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | extra_intermediate_entity | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | extra_intermediate_entity_in_final_answer | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | extra_intermediate_values | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | extra_intermediate_values_in_final_submission | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | extra_unrequested_values_in_final_answer | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | fabricated_numeric_estimate | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | false_empty_answer | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | final_answer_confused_with_branch_candidate | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | final_answer_is_wrong_founder | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | final_answer_selects_1850 | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | final_answer_substitution | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | final_answer_token_mismatch | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | final_answer_wrong_year | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | final_hop_conflation | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | final_sum_based_on_wrong_postsecondary_count | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | hallucinated_community_area_number | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | hallucinated_entity_chain | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | hallucinated_establishment_year | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | hallucinated_founder | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | hallucinated_founding_year | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | hallucinated_white_share | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | ignored_available_count | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | ignored_available_evidence | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | ignored_correct_count | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | ignored_correct_evidence | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | ignored_correct_result_and_submitted_zero | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | ignored_correct_school_day_evidence | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | ignored_found_source | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | ignored_recovered_evidence | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | ignored_returned_shooting_count | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | inconsistent_final_submission | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | incorrect_final_answer | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | intermediate_entity_substitution | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | intermediate_hop_answer_submitted | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | intermediate_result_submitted | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | intermediate_result_substituted_for_final_answer | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | intermediate_value_submitted | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | overinclusive_final_response | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | overrode_exact_result_with_estimate | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | partial_final_answer | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | placeholder fallback after source access | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | placeholder_fallback | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | placeholder_submission_after_evidence | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | placeholder_submitted_instead_of_computed_value | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | premature_natural_language_fallback | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | premature_null_answer | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | propagated_wrong_intermediate_count | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | selected_excluded_county | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | selected_intermediate_fact_instead_of_final_fact | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | selected_mba_school_instead_of_undergrad_school | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | selected_wrong_city_population | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | selected_wrong_count_after_wrong_intermediate | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | selected_wrong_person | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | stale_final_answer | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | stale_or_mismatched_final_answer | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submission_mismatch | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted [0] despite qualifying evidence | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted answer does not match its own computed result | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted the wrong final answer after using the inflated public-school count | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted wrong final city | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted wrong final numeric answer | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted wrong final result from incorrect intermediates | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_answer_from_wrong_intermediate_count | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_composite_answer_instead_of_final_count | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_dataset_year_as_final_answer | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_error_placeholder | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_incorrect_numeric_answer | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_incorrect_year | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_intermediate_answer_instead_of_final_answer | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_intermediate_count | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_intermediate_count_instead_of_difference | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_intermediate_entity_instead_of_final_answer | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_intermediate_expression_instead_of_final_integer | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_intermediate_hops_instead_of_final_scalar_answer | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_invalid_answer_despite_victoria_being_supported_by_available_evidence | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_null_despite_required_chain | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_null_fallback | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_null_instead_of_temperature_answer | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_raw_count_instead_of_normalized_per_century_answer | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_stale_answer_after_self_correction | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_unknown_despite_relevant_sources_found | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_wrong_average | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_wrong_city | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_wrong_count_from_wrong_branch | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_wrong_downstream_count | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_wrong_establishment_year_for_wrong_school_district | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_wrong_final_value | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_wrong_numeric_value | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_wrong_result | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_wrong_value | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | substituted_county_seat_year_for_school_district_year | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | tool_limit_placeholder_answer | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | unsupported final answer after unresolved evidence gap | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | unsupported_estimate | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | unsupported_estimate_after_tool_limit | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | unsupported_final_number | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | unsupported_guess_after_blocker | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | unsupported_numeric_value | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | unused_correct_result | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong county branch / wrong school district selected | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong final answer selected | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong final numeric selection | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong final submission | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong final university attribution | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong final year selected | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_bay_name | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_birth_year | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_branch_and_income_lookup | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_branch_final_answer | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_branch_finalization | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_branch_or_area_selected | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_candidate_selected | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_city_year_answer | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_county_selected | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_department_mapping | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_entity | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_entity_and_year | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_entity_hierarchy | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_entity_submitted | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_federal_agency_selected | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_answer_after_miscomparison | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_answer_after_using_wrong_count | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_answer_format | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_answer_from_wrong_counts | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_answer_or_format | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_answer_selection | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_answer_value_or_format | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_bay | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_birth_year | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_borough | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_branch | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_city_choice | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_city_selection | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_entity_and_birth_year | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_entity_chain | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_entity_selected | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_entity_selection | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_entity_submission | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_location_selected | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_lookup | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_neighborhood_or_area | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_number | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_pair_and_birth_year_difference | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_park_area | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_person_and_malformed_number | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_rank | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_school | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_school_and_zip | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_total | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_university_chain | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_year_submission | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_founder | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_founder_and_death_year | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_founding_year_selected | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_governor_birth_year | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_governor_selection | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_intermediate_count_selected | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_intermediate_value_propagated_to_final_answer | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_medieval_name | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_museum_year_selected | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_namesake_pair_finalized | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_neighborhood_to_community_area_mapping | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_numeric_answer | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_population_value | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_rank_selected | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_row_selected | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_school_denominator | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_school_district_and_year | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_school_zip_and_white_share | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_value_selected_from_correct_evidence | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_year_selected_from_related_fact | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_year_selected_from_source | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_year_selection | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | year_confusion_at_submission | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | approximate_final_value | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | arithmetic_off_by_100 | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | averaged_release_counts_as_intake | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | averaged_single_year_instead_of_two_years | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | averaged_wrong_yearly_counts | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | avg_instead_of_required_sum_then_average | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | bad_average_and_rounding | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | bad_cross_year_intersection | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | bad_intersection | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | bad_subtraction | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | binary_counting_instead_of_gt0_filter | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | candidate_set_miscarried | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | century_denominator_and_rounding_error | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | compounding_wrong_threshold | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | counted wrong area branch | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | counted_distinct_employees_instead_of_rows | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | counted_wrong_year_and_group_for_final_hop | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | county_seat_recency_miscomparison | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | cross_year_candidate_error | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | cv_ranking_query_mismatch | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | cv_scope_mismatch | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | distinct_count_instead_of_row_count | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | estimated_count_used_in_ratio | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | estimated_postsecondary_count | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | fabricated_final_average | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | fabricated_zero_office_count | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | failed_hop_intersection | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | failed_intersection_minimum | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | ignored_required_city_constraint | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | inclusive_upper_bound_mismatch | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | incorrect lowest-average school selection | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | incorrect_average | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | incorrect_average_ranking | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | incorrect_branch_intersection | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | incorrect_final_count | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | incorrect_intermediate_count | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | incorrect_intersection | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | incorrect_intersection_and_count | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | incorrect_intersection_and_count_selection | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | incorrect_total_or_input_value | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | intersection_error | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | inverted city comparison | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | misranked_minimum | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | missed_all_years_intersection | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | missed_set_intersection | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | missing_aggregation_and_filters | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | monthly_max_instead_of_yearly_max | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | omitted_candidate_city_in_average | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | omitted_required_value | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | overfiltered numerator | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | overfiltered_final_count | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | partial_sample_counting | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | partial_subset_counting | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | percent_change_instead_of_ratio | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | proxy_metric_mismatch | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | ratio_direction_inverted | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | reversed_difference | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | reversed_subtraction_order | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | rounding_error | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | sample_based_counting | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | sampled_subset_used_instead_of_full_aggregation | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | search_hit_count_confused_with_record_count | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | set_intersection_misapplied | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | single_year_total_treated_as_average | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | skipped_final_subtraction | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | subtracted_from_wrong_public_school_count | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | summed_multiple_rows_instead_of_extracting_single_district_total | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | topk_intersection_miscomputed | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | truncated_final_count | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | unnecessary_applied_force_filter | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | unsupported_estimate | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | unsupported_factual_claim | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | unsupported_percent_guess | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | unsupported_superlative | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | used annual-average unemployment instead of December threshold | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | used_unverified_estimate_in_final_math | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | used_zero_threshold_from_wrong_intermediate | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | ward_comparison_confusion | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong proxy aggregation for the arrest-area hop | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_absolute_difference | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_agency_ranking | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_aggregation_granularity | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_aggregation_metric | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_aggregation_missing_groupby | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_aggregation_scope | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_average_from_wrong_2020_input | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_average_rank | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_average_ranking | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_average_rounding | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_average_window_or_denominator | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_borough_denominator | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_candidate_set | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_counties_and_year_gap | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_counts_used_for_average | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_cross_year_aggregation | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_cv_inputs | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_cv_ranking | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_dataset_and_field | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_denominator_and_rounding | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_earliest_county_comparison | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_earliest_county_selection | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_filter_and_wrong_maximum | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_filter_fields_and_measure | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_filter_scope | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_filtered_count | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_final_addend | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_final_aggregation_scope | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_final_arithmetic | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_final_branch_and_neighborhood_chain | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_final_count | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_final_hop_source | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_final_subtraction | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_formula_or_denominator | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_grouping_and_filter | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_hate_crime_total | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_incorporation_year_ranking | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_intermediate_precinct_ranking | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_intermediate_year | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_intersection_of_constraints | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_intersection_of_hop1_filters | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_isd_ranking_and_year | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_metric_and_grouping | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_metric_and_scope | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_metric_budgeted_pay_rate | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_minimum_selection | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_numerator_used_in_ratio | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_peak_year_filter | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_percentage_formula | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_person_identification | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_rank_intersection | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_ranking_metric_after_cast_error | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_ratio_from_wrong_denominator | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_salary_average_metric_and_grouping | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_scope_final_count | 1 | gpt-5-mini: 1 |
| Computation errors | computation_or_aggregation_error | wrong_set_intersection | 1 | gpt-5.4-nano: 1 |
| Computation errors | computation_or_aggregation_error | wrong_taser_value_interpretation | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | ambiguous_final_year_extraction | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | approximate_value_substitution | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | birthplace_taken_as_base_location | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | bridge_year_taken_as_land_company_founding_year | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | broad_department_filter | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | county_count_misread | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | county_fips_instead_of_county_name | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | demonym_instead_of_province | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | digit_miscopy | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | district_office_count_from_truncated_grep | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | empty_saved_artifact | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | extracted population year 2022 instead of establishment year 1683 | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | first_constable_vs_head_confusion | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | founded_year_confused_with_charter_year | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | founding_year_taken_as_birth_year | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | grandparent_role_confusion | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | grep_match_count_used_as_count | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | json_source_treated_as_xml | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | json_string_quoting_misread | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | looked_for_adams_morgan_in_neighborhood_cluster | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | misread founding year as acquisition year | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | misread_family_relation | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | misread_temperature_value | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | misread_year_from_history_range | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | neighborhood_misparsed_from_location_row | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | nested_geojson_shape | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | opening_date_instead_of_foundation_date | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | overbroad_description_filter | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | parent_agency_confusion | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | private_school_count_not_extracted | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | public_school_count_misread | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | sample_biased_location_category | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | school_count_filter_miss | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | selected_opening_year_instead_of_establishment_year | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | selected_wrong_row_from_final_table | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | truncated_grep_result_misread | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | used_open_date_as_school_day | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong founding year extracted | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_birth_year | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_charter_year_extracted | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_column_used_for_shooting_descriptor | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_column_used_in_complaints | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_district_extracted_from_partial_school_nutrition_parse | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_entity_from_source | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_famous_person_link | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_field_and_truncated_date | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_field_filter | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_field_for_fips | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_field_for_location_lookup | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_field_or_schema | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_field_or_tag | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_field_selected | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_file_shape | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_founding_year | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_grandfather_name | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_grandfather_relation | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_historical_entity | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_historical_leader_fact | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_historical_role_extracted | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_json_access_path | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_location_field_and_category | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_measure_and_city_subset | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_person_name_extracted_from_wikipedia | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_population_field_and_join_key | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_row_selected | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_row_selected_from_ranked_result | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_temperature_value_extracted | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_turing_recipient_extracted | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_university_extracted | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_xml_field_path | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_year_extracted | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_year_extracted_from_holland_land_company_text | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_year_extracted_from_museum_text | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_year_from_company_source | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_year_from_museum_page | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_year_from_source | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_year_selected_from_truncated_excerpt | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_year_source | 1 | gpt-5-mini: 1 |
| Execution/extraction errors | extraction_or_parsing_error | wrong_year_span | 1 | gpt-5.4-nano: 1 |
| Execution/extraction errors | extraction_or_parsing_error | xml_json_parse_confusion | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | abstained_after_search_retry | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | answered_before_required_final_hop | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | blank submission after partial evidence | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | blank_placeholder_submission | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | blank_submission_after_blocker | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | blank_submission_after_failed_recovery | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | blank_submission_after_failed_search | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | blank_submission_after_search_dead_end | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | blocked_partial_chain | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | fallback_answer_without_required_count | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | false_insufficient_data_bailout | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | gave_up_after_empty_results | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | gave_up_after_failed_search | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | gave_up_after_tool_errors | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | gave_up_after_tool_failures | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | gave_up_before_honoree_chain | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | gave_up_before_neighborhood_lookup | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | gave_up_before_parsing_nested_json | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | gave_up_without_extraction | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | generic_placeholder_submission | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | guessed_after_blocker | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | irrelevant_search_drift | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | missed_critical_fact | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | missing_birth_year_lookup | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | missing_city_filter_public | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | missing_later_hops | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | partial_chain_submission | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | partial_or_empty_intermediate_counts | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | placeholder_answer_after_unresolved_chain | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | placeholder_submission_after_blocker | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | placeholder_submission_after_failed_queries | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | placeholder_submission_after_insufficient_extraction | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | placeholder_submission_after_tool_failures | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | placeholder_submission_before_final_hops | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | placeholder_submission_without_phd_grounding | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature insufficient-data submission | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_abandonment | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_fallback_after_tool_failure | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_final_submission | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_insufficient_answer | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_insufficient_data_submission | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_none_submission | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_null_submission | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_placeholder_answer | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_submission_after_partial_hop | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_submission_after_partial_results | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_submission_missing_final_hop | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_submit | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_submit_after_partial_chain | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_unable_to_determine_submission | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | skipped_final_bridge_hop | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | skipped_final_hop | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | skipped_remaining_hops | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | skipped_required_final_lookup | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | skipped_required_hops | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | stopped after selecting the university page without extracting the enrollment figure | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | stopped_after_hop1 | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | stopped_after_intermediate_bridge_fact | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | stopped_before_required_seat_and_statue_hops | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted before county lookup | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted fallback answer without computation | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_after_partial_range_check | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_before_required_final_hops | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_before_required_later_hops_were_gathered | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_blank_without_required_hops | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_empty_answer_after_partial_research | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_null_without_income_rank_evidence | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_placeholder_after_stalled_searching | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_placeholder_after_tool_failures | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_placeholder_after_unresolved_tool_errors | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_unknown_after_blocker | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_unknown_before_required_hops | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_unknown_without_required_verification | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_without_final_hop_evidence | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_without_required_source | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_without_required_subtraction | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_without_supporting_evidence | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_wrong_rate_without_required_final_lookup | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | tool_budget_exhaustion | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | truncated_source_not_fully_read | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | unsupported_final_guess | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | budget_exhausted_before_final_resolution | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | estimated_answer_after_budget_cutoff | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | forced_submission_after_budget_exhaustion | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | guessed_answer_after_budget_exhaustion | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | hard_timeout | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | hard_timeout_before_submit | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | never_reached_final_hops | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | partial_chain_at_submit | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | premature_submission_after_cancellation | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | stalled_before_required_count | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | stopped_before_final_aggregation | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | submitted_after_partial_evidence | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | submitted_before_chain_complete | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | submitted_placeholder_before_resolving_required_hops | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | submitted_unknown_after_cap | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | time_budget_exhausted | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | timeout_before_final_hop | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | tool budget exhausted before math and population comparison were completed | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | tool_budget_exhausted_before_final_hop | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | tool_budget_exhausted_before_final_lookup | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | tool_budget_exhausted_before_final_submission | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | tool_budget_exhausted_before_required_sources | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | tool_budget_exhausted_before_wikipedia_hops | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | tool_limit_exhaustion | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_not_enough_turns | turn_budget_exhausted_before_final_year | 1 | gpt-5.4-nano: 1 |
| Other/unclear | other_or_unclear | hallucinated_final_chain | 1 | gpt-5.4-nano: 1 |
| Other/unclear | other_or_unclear | null_submission_after_failed_extraction | 1 | gpt-5.4-nano: 1 |
| Other/unclear | other_or_unclear | unsupported_final_year_guess | 1 | gpt-5-mini: 1 |
| Other/unclear | other_or_unclear | unsupported_hate_crime_estimate | 1 | gpt-5-mini: 1 |
| Other/unclear | semantic_or_gold_label_issue | benchmark_answer_conflict | 1 | gpt-5.4-nano: 1 |
| Other/unclear | semantic_or_gold_label_issue | benchmark_label_mismatch | 1 | gpt-5-mini: 1 |
| Other/unclear | semantic_or_gold_label_issue | expected_answer_conflicts_with_logged_count | 1 | gpt-5-mini: 1 |
| Other/unclear | semantic_or_gold_label_issue | gold_answer_conflict_with_source | 1 | gpt-5.4-nano: 1 |
| Other/unclear | semantic_or_gold_label_issue | inconsistent_gold_answer | 1 | gpt-5-mini: 1 |
| Other/unclear | semantic_or_gold_label_issue | possible_benchmark_task_mismatch | 1 | gpt-5.4-nano: 1 |
| Other/unclear | semantic_or_gold_label_issue | possible_gold_answer_mismatch | 1 | gpt-5-mini: 1 |
| Other/unclear | semantic_or_gold_label_issue | task_gold_conflict | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | ad_hoc_candidate_lookup | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | carried_precinct_filter_into_final_hop | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | collapsed_to_single_school_branch | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | county_fips_detour | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | county_only_public_school_scope | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | county_scope_broadening | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | county_wide_count_instead_of_city_in_county | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | cross_year_average_detour | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | deviated_from_required_hops | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | diverged_from_planned_hops | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | diverged_from_provided_hop_chain | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | diverged_into_unrelated_opstfips_sanity_checks | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | divergent_lookup_path | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | expanded_cv_scope_to_top_10_instead_of_top_5 | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | geometry_detour | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | hop_2_scope_drift | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | hop_divergence | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | ignored_fixed_target_area | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | ignored_required_hops | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | misordered_hop_branch | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | missed highway terminus extraction | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | missing_final_hop | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | never_advanced_past_hop_1 | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | off_path_branching | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | off_target_exploration_instead_of_required_hops | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | omitted_required_final_source_hop | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | overexpanded_assessment_scope | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | per_year_top_five_instead_of_cross_year_average | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | planned_multi_part_final_output | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | post_plan_search_drift | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | search_only_deviation | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | searched_for_statewide_population_dataset_instead_of_using_planned_county_pages | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | single_year_query_instead_of_required_multi_year_aggregation | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | sitecounty_top10_wrong_aggregation | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped final head/university hop after budget aggregation | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped hop 5 county lookup | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped required county hop | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped required county-population comparison | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped_area_id_mapping_and_final_area_code_filter | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped_bedford_and_day_hops | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped_final_year_lookup | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped_follow_on_hops_after_first_aggregation | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped_intersection_and_used_wrong_branch | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped_king_birthyear_hop | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped_overtime_and_salary_hops | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped_remaining_chain_hops | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped_required_biographical_hops | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped_required_hop_4 | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped_required_hop_chain | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped_required_intersection_hops | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped_required_multi_hop_chain | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped_required_neighborhood_lookup | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped_required_ripa_mapping_hop | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped_required_year_intersection | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | skipped_wikipedia_hops | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | stalled_after_first_hop | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | stalled_before_zip_and_census_hops | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | stayed_on_overtime_hop_instead_of_advancing | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | stuck_on_hop_1 | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | turned hop 3 into a Moving Traffic Violations charge-description query | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | used_all_five_counties_instead_of_remaining_counties_for_age_ranking | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | wrong_branch_chain | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | wrong_entity_chain | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | wrong_final_branch | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | planning_decomposition_mismatch | year_window_and_aggregation_scope_confusion | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | annual_filter_scope_misread | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | answer_shape_and_intermediate_field | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | answer_target_inversion | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | answered_bachelors_degree_year_instead_of_university_founding_year | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | answered_degree_year_instead_of_foundation_year | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | at_least_three_years_treated_as_all_four_years | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | based_in_constraint_ignored | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | based_in_vs_birthplace_confusion | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | birthplace county/state misread | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | birthplace_vs_namesake_confusion | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | borough_misidentified | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | branch_as_neighborhood | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | broadened narcotic-drug-law filter into generic drug-related arrests | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | carried_forward_intermediate_ward_filter | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | chased_wrong_entity_chain | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | city_referent_misread | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | cohort_category_confusion | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | comparison_ratio_misread | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | conflated_target_person_with_first_officeholder | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | constraint_ignored | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | coreference_misread | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | county_seat_condition_misread | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | county_seat_vs_county_population_confusion | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | county_year_confused | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | dropped city-level constraint on the public-school count | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | dropped district/member filter | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | dropped the required city constraint and used county-only scope | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | dropped_all_grades_or_exact_subject_constraint | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | extra_precinct_filter_and_broadened_location_predicate | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | extra_precinct_filter_in_final_count | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | final_hop_relation_misread | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | fiscal_year_treated_as_calendar_year_and_scope_widened | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | grouping_key_and_topk_misread | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | historical_year_confusion | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | ignored the intended top-five-average scope for the CV comparison | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | ignored_exclusion_constraint | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | ignored_original_23_exclusion | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | ignored_single_answer_format | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | incorrect set-intersection across hops | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | incorrect_entity_classification_and_comparison | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | intersection_constraint_misread | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | intersection_requirement_misread | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | location clue treated as school-name clue | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | misidentified_named_king | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | missed_original_23_exclusion | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | multi_hop_constraint_misread | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | omitted_required_filter_and_cross_cycle_intersection | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | original_23_counties_misread | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | output_format_and_answer_scope | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | percentage_change_instead_of_percentage_of_baseline | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | percentage_of_incidents_interpreted_as_percent_change | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | picked highest-release county instead of newest county-seat county | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | province_neighborhood_confusion | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | release_year_confusion | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | release_year_semantics | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | release_year_vs_data_year | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | returned_category_instead_of_count | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | returned_intermediate_metric_instead_of_final_population | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | returned_person_instead_of_university | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | reversed_incorporation_comparison | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | school_day_vs_open_date_misread | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | scientist_chain_misread | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | scope_and_filter_misread | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | state_fips_misread | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | state_fips_or_geography_confusion | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | state_year_mixup | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | target_person_misidentified | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | top-2 rank misread | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | treated_2006_as_noncomparable | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | treated_open_date_as_school_day | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | treated_shooting_location_desc_as_requested_location_position_category | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | used county-seat city population as the final comparator | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | violent_crime_and_founding_year_recast_as_bridge_proxies | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | ward_misread | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | weapon_filtered_use_of_force_subset | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | wrong_branch_identity | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | wrong_city_and_year_constraints | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | wrong_city_pair_and_metric | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | wrong_comparison_city_set | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | wrong_comparison_entities | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | wrong_county_seat_branch | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | wrong_district_propagation_and_estimate | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | wrong_entity_chain | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | wrong_final_county | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | wrong_metric | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | wrong_person_identity | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | wrong_quantity_scope | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | wrong_status_filter | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | wrong_terminus_city | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | wrong_year_filter | 1 | gpt-5-mini: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | wrong_year_window_and_top5_set | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | year_and_field_proxy_mismatch | 1 | gpt-5.4-nano: 1 |
| Planning/trajectory mismatch | question_or_constraint_misread | year_field_mismatch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | aggregate source instead of drug-level source | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | ambiguous_or_missing_dataset_lookup | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | arrest_vs_crime_dataset_confusion | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | bid_instead_of_ward | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | broad search drifted into unrelated Washington education sources | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | carried_sector_filter_into_final_count | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | census_zip_source_search | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | circulation_datasets_not_selected | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | city_constraint_omitted | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | city_lookup_detour | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | city_population_dataset_detour | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | city_scope_swapped_to_gary_indiana | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | collapsed multi-hop chain to final dataset only | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | collapsed the multi-hop county-seat chain into a direct UT enrollment lookup | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | collapsed_multi_year_scope | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | cook_county_only_scope_instead_of_authorized_chicago_in_cook_county | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | counted_against_wrong_dataset_family_for_2021 | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | counted_global_top_counties_instead_of_required_hop2_counties | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | county-wide aggregation instead of Detroit/Wayne | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | county_chain_sought_in_health_dataset | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | county_instead_of_city_denominator | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | county_only_district_office_count | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | county_only_district_office_filter | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | county_only_filter_for_district_offices | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | county_only_filter_for_public_schools | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | county_only_filter_instead_of_intended_count_scope | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | county_only_private_school_count | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | county_only_private_school_filter | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | county_only_scope | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | county_only_scope_broadening | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | county_scope_instead_of_pullman_school_district | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | county_scope_mismatch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | county_vs_city_subset_mismatch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | county_wide_private_school_filter | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | countywide_district_office_count | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | countywide_instead_of_city_specific | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | countywide_public_school_count_instead_of_city_in_county_count | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | cross-year query against a single-year enrollment file | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | cross_dataset_family_misroute | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | ctt_proxy_instead_of_spec_ed_target_list | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | current_year_to_date_complaint_source | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | dataset_version_mismatch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | dataset_year_mismatch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | dc_vs_chicago_dataset_confusion | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | dc_vs_chicago_dataset_mismatch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | department_description_and_2019_only | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | description_branch_instead_of_code_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | detoured_to_unrelated_population_dataset | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | district_office_dataset_misidentified | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | district_scope_omitted | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | dropped_city_filter_and_counted_entire_cbsa | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | dropped_city_filter_for_private_school_count | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | dropped_city_filter_for_public_school_count | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | dropped_lansing_city_filter_on_private_school_count | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | dropped_required_city_filter | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | expanded_candidate_set | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | expanded_school_count_to_county | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | extra agency filter on capital outlay query | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | extra_council_district_filter | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | extra_county_in_scope | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | extra_precinct_filter | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | extra_ward_filter_in_final_count | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | final_geography_misframed_as_texas | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | final_hop_misdirected | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | final_hop_source_missed | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | final_hop_source_swap | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | final_hop_used_wrong_dataset | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | final_hop_wrong_source | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | followed an unavailable Concho County entity branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | followed_wrong_county_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | generic_enrollment_lookup_instead_of_target_row | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | global_count_instead_of_la_subset | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | head_lookup_wrong_dataset | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | historic_dataset_scope | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | historic_metadata_instead_of_2023_rows | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | ignored_remaining-county filter in hop 3 | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | ignored_required_district_filter | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | included_office_of_administration_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | incorrect_filter_values | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | incorrect_fiscal_year_or_filter | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | initial_wrong_dataset_family | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | irrelevant_budget_dataset | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | irrelevant_source_family | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | medicare_datasets_instead_of_state_drug_utilization | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | metadata_catalog_instead_of_rows | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | metadata_file_instead_of_tabular_rows | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | metadata_view_instead_of_rows | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | mismatched_source_family | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | missed_city_constraint | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | missed_required_ami_source | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | missed_required_county_source | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | missed_street_sweeping_source | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | misselected_dataset | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | missing_census_population_source | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | missing_programyear_filter | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | missing_required_borough_source | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | missing_school_year_constraint | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | missouri_branch | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | mixed_grade_scope | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | monument_county_instead_of_facility_county | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | neighborhood_cluster_instead_of_ward1 | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | neighborhood_filter_misread | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | omitted city filter for postsecondary count | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | omitted_parking_dataset_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | omitted_required_adams_morgan_source | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | omitted_required_datasets_and_ended_on_area_name_fallback | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | omitted_required_starting_source | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | opened_wrong_dataset_family | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | out_of_scope_university | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | outdated_dataset_version_and_field_mismatch | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | overbroad_geography_filter | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | overbroad_row_subset_or_filter | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | parking_fines_misread_as_moving_violations | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | partial_dataset_selection | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | partial_population_source_set | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | partial_source_coverage | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | picked the 2013-2014 performance directory as the main source branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | picked_benefactor_biography_instead_of_honoree_biography | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | picked_houston_instead_of_fort_worth | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | picked_moving_datasets_instead_of_parking_datasets | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | picked_watertown_page_instead_of_paddock_arcade | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | pivoted_to_gary_indiana_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | pivoted_to_wrong_dataset_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | postsecondary_wrong_dataset_version | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | postsecondary_year_conflation | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | postsecondary_year_mismatch | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | private_school_count_scope | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | private_school_scope_mismatch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | private_schools_wrong_dataset_version | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | public_school_count_scope | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | release_year_vs_row_year_misread | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | releases_instead_of_receives | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | releases_vs_receives_confusion | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | route66_source_misselection | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | salary_checked_in_wrong_dataset | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | school_day_source_not_used | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | scope_drift_to_unrelated_datasets | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | searched and opened wrong dataset versions | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | searched_for_unavailable_climate_dataset | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | searched_irrelevant_datasets_instead_of_required_school_day_source | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | searched_irrelevant_school_sources_after_wrong_branch_choice | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | searched_nonexistent_mapping_source | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | searched_nonexistent_salary_dataset_instead_of_source_page | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | searched_nonexistent_school_location_dataset | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | searched_school_dataset_for_neighborhood_field | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | searched_unrelated_chicago_source | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | searched_unsupported_census_zcta_source | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | searched_wrong_dataset_family | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | selected_moving_violations_instead_of_parking_violations | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | single_year_file_used_for_multi_year_aggregation | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | single_year_proxy_for_two_year_average | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | sitecounty_instead_of_cecounty | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | skipped_corpus_christi_source | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | skipped_moses_brown_source | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | skipped_required_wikipedia_ward_lookup | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | source_confusion | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | source_family_mismatch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | spokane_branch_instead_of_whitman_branch | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | springfield_missouri_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | state_or_geography_swapped | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | statewide_county_scope_instead_of_detroit_wayne | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | stopped_at_benefactor_page_instead_of_honoree_page | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | street_sweeping_chicago_vs_dc | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | subset_scope_drop | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | substituted_bexar_for_dallas | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | switched to Monroe County, NY instead of Westmoreland County, VA | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | switched_from_iowa_to_alabama | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | switched_to_wrong_cpi_dataset_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | texas_vs_puerto_rico_confusion | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | truncated_grep_subset | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | union_instead_of_required_intersection | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | unrelated_dataset_selection | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | used county-wide scope for public schools | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | used crime dataset for arrest hop | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | used crime incidents instead of arrest records | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | used the wrong crime-description branch in the 2020-present lookup | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | used wrong area/source branch and skipped the required Central/RIPA path | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | used_2010_population_from_500_cities_instead_of_2020_census | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | used_apd_searches_year_instead_of_council_meeting_year | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | used_arrest_data_instead_of_2019_crime_data | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | used_arrest_dataset_for_2019_crime_hop | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | used_arrest_dataset_for_crime_description_hop | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | used_arrest_dataset_for_crime_lookup | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | used_building_energy_yearbuilt_instead_of_required_boeing_plant_2_source | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | used_cad_incidents_instead_of_searches_by_type_for_sector_hop | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | used_complaint_dataset_for_final_count_step | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | used_complaint_rows_for_shooting_hop | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | used_crime_dataset_to_infer_no_ma_ward | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | used_dataset_yearbuilt_instead_of_target_building_page | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | used_income_only_county_set | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | used_open_date_instead_of_school_day_source | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | used_school_locations_open_date_instead_of_required_school_day_source | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | used_shooting_dataset_for_complaint_category | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | used_shooting_dataset_for_complaints_hop | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | used_yearbuilt_field_instead_of_building_page | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | ward_inference_from_wrong_dataset | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | ward_mapping_not_grounded | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong dataset family / release confusion | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong geography / aggregation scope | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong neighborhood branch | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_2022_metrics_dataset | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_500_cities_dataset_variant | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_500_cities_release_family | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_birthplace_geography | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_borough_filter | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_branch_lookup | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_branch_or_geography | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_branch_or_neighborhood | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_branch_or_neighborhood_lookup | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_cbsa_scope | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_city_branch_for_binge_drinking | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_city_budget_files | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_city_or_dataset_family | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_city_pair | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_city_pair_and_release | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_councilmember_branch | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_county | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_county_and_city_branch | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_county_and_district_scope | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_county_city_branch | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_county_field | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_county_field_and_threshold_scope | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_county_field_and_year_scope | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_county_lookup | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_county_seat_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_county_seat_branch_for_final_lookup | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_county_set_for_postsecondary_step | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_and_filter | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_chain | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_fallback | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_family_and_fields | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_family_for_daycare_counts | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_family_for_node_3 | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_file | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_files | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_for_2019_crime_hop | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_for_2021_count | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_for_downstream_hop | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_for_dui_area | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_for_first_hop | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_for_hop | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_for_required_hop | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_or_field | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_or_query_shape | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_or_year | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_pivot | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_schema | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_selected | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_variant | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_version_and_schema | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_year_field | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_year_for_postsecondary_count | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_dataset_year_or_family | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_date_field_and_area_normalization | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_department_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_district_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_field_and_filter | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_field_and_year_scope | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_file_or_dataset_path | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_file_path | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_file_shape_or_dataset_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_filter_criterion | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_filter_for_search_sector | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_final_county_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_final_county_lookup | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_final_filter | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_final_hop_source | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_final_source_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_followup_entity | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_geography_or_dataset_family | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_hbcu_entity_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_historically_black_university_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_location_dataset_scope | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_measure_and_value_type_filters | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_metric_and_candidate_set | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_metric_dataset | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_nba_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_neighborhood_branch | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_neighborhood_lookup | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_officeholder_source | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_postsecondary_dataset_year | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_postsecondary_year_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_program_year_and_field | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_public_school_dataset_family | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_release_or_dataset_choice | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_release_year_scope | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_school_and_district | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_school_dataset_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_scope_income_source | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_source_branch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_target_entity_chain | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_terminus_city_branch | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_tool_or_query_shape | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_ward_branch | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_year_and_field | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_year_and_filter | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_year_and_filter_scope | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_year_and_grouping | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_year_and_metric_for_mental_health | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_year_and_source_family | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_year_branch | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_year_dataset | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_year_scope | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_year_source | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | wrong_year_subset | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | year_and_filter_mismatch | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | year_mismatch | 1 | gpt-5-mini: 1 |
| Source/scope errors | wrong_source_or_scope | year_mismatch_closest_dataset | 1 | gpt-5.4-nano: 1 |
| Source/scope errors | wrong_source_or_scope | year_or_dataset_mismatch | 1 | gpt-5-mini: 1 |
| Tool/data blockers | tool_or_data_blocker | file_too_big_for_query_ideal | 1 | gpt-5-mini: 1 |
| Tool/data blockers | tool_or_data_blocker | historic_complaint_file_query_failed_then_source_pivot | 1 | gpt-5-mini: 1 |
| Tool/data blockers | tool_or_data_blocker | large_file_query_blocked | 1 | gpt-5-mini: 1 |
| Tool/data blockers | tool_or_data_blocker | oversized_cad_file | 1 | gpt-5-mini: 1 |
| Tool/data blockers | tool_or_data_blocker | placeholder_submission | 1 | gpt-5.4-nano: 1 |
| Tool/data blockers | tool_or_data_blocker | placeholder_submission_after_blocker | 1 | gpt-5.4-nano: 1 |
| Tool/data blockers | tool_or_data_blocker | placeholder_submission_after_blockers | 1 | gpt-5.4-nano: 1 |
| Tool/data blockers | tool_or_data_blocker | tool_budget_exhaustion | 1 | gpt-5-mini: 1 |
| Tool/data blockers | tool_or_data_blocker | tool_limit_exhaustion | 1 | gpt-5-mini: 1 |
| Tool/data blockers | tool_or_data_blocker | unsupported_geojson_query | 1 | gpt-5.4-nano: 1 |
| Tool/data blockers | tool_or_data_blocker | unsupported_source_tool_choice | 1 | gpt-5-mini: 1 |
| Tool/data blockers | tool_or_data_blocker | unsupported_xml_query | 1 | gpt-5-mini: 1 |
| Tool/data blockers | tool_or_data_blocker | wrong_source_selection | 1 | gpt-5.4-nano: 1 |
| Tool/data blockers | tool_or_data_blocker | xml_query_unsupported | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | broad_irrelevant_searches | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | broad_prefix_search_no_progress | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | broad_searches_for_identified_student_data | 1 | gpt-5-mini: 1 |
| Turn-waste loops | low_yield_search_loop | dataset_not_found_loop | 1 | gpt-5-mini: 1 |
| Turn-waste loops | low_yield_search_loop | generic_irrelevant_searches | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | generic_searches_before_right_dataset | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | irrelevant dataset discovery | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | irrelevant_dataset_hunting | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | irrelevant_search_branch | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | postsecondary_dataset_search_dead_end | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | regulators_biography_search | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated no-hit search queries | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_dataset_discovery_queries | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_dataset_discovery_without_extraction | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_dataset_not_found_on_corporate_history | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_dataset_search | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_dataset_search_no_match | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_dataset_search_no_progress | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_dataset_searches_returned_nothing | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_empty_dataset_searches | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_empty_queries | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_empty_searches | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_empty_searches_for_computer_sessions | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_failed_dataset_discovery | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_failed_office_source_search | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_generic_income_searches | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_irrelevant_searches | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_irrelevant_searches_for_school_evidence | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_no_dataset_climate_searches | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_no_new_dataset_searches | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_no_result_school_day_searches | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_no_result_searches_for_street_sweeping_source | 1 | gpt-5-mini: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_noisy_dataset_search | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_nonproductive_census_searches | 1 | gpt-5-mini: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_salary_searches | 1 | gpt-5-mini: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_searches_after_wrong_pivot | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_searches_no_new_evidence | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_source_search_without_data_extraction | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_spurs_source_searches | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_syracuse_searches_returned_nothing | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_unhelpful_school_district_searches | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_unsuccessful_generic_searches | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | bad casts and mis-filtered math queries | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | bad_json_unnest_attempts | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | binder_and_catalog_errors | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | binder_and_repair_churn | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | binder_error_and_parameter_misuse | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | binder_error_and_repair_cycle | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | binder_error_and_shape_mismatch | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | binder_error_on_missing_column | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | binder_error_on_wrong_source | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | binder_error_wrong_column_names | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | binder_error_wrong_columns | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | cross_file_sql_binder_error | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | district_office_query_schema_mismatch_and_binder_errors | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | duckdb_json_binder_errors | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | duckdb_stddev_array_binder_error | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | file_too_large_for_query | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | flat_sql_against_nested_json | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | ideal_query_repair_failure | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | ideal_repair_json_decode_error | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | ideal_repair_jsondecode | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | ideal_repair_jsondecode_failure | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | ideal_repair_jsondecodeerror_loop | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | json_schema_query_mismatch | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | json_shape_mismatch | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | jsondecode_repair_error_loop | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | jsondecodeerror_during_repair | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | malformed_numeric_aggregation_sql | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | malformed_or_incompatible_queries | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | malformed_qualify_query | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | malformed_query_repair | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | malformed_sql_and_cancellation | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | malformed_sql_and_column_mismatch | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | malformed_sql_and_column_quoting | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | malformed_sql_and_table_calls | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | malformed_sql_binder_errors | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | malformed_sql_column_reference | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | malformed_sql_or_query_shape | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | malformed_sql_repair | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | mis_specified_use_of_force_query | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | mixed_execution_and_repair_failures | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | nested_geojson_sql_shape_mismatch | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | nested_json_schema_mismatch | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | oom_and_repair_timeout | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | placeholder_or_non_substantive_execution | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | placeholder_sql_and_repair_failures | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | placeholder_sql_then_binder_error | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repair_churn_with_binder_error | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repair_failure_jsondecodeerror | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated malformed query calls | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | repeated schema mismatch on JSON feature collection | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_311_query_failures | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_binder_and_repair_failures | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_binder_and_unsupported_json_failures | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_binder_error_on_json_featurecollection | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_binder_error_on_wrong_shape | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_binder_errors_on_geojson_queries | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_binder_errors_on_geojson_query | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_cast_and_regex_sql_errors | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_column_resolution_binder_errors | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_duckdb_binder_errors | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_empty_repair_queries | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_execute_ideal_path_errors | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_flat_sql_binder_errors_on_nested_geojson | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_parse_and_repair_failures | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_parse_xml_on_non_xml_files | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_query_and_repair_failures | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_query_ideal_repair_failures | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_sql_binder_errors | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_sql_repair_failures | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_zero_row_queries | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | schema_mismatch_and_near_duplicate_query_failures | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | sql_repair_jsondecode_error | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | sql_repair_jsondecode_loop | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | sql_schema_mismatch | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | stalled_execute_repair_loop | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | unsupported parser/tool choice for file format | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | unsupported_nested_geojson_query | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | unsupported_parse_and_jsondecode_loop | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | unsupported_parser_on_json | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | unsupported_xml_json_query_mismatch | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | wrong_column_and_type_assumptions | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | wrong_columns_in_sql | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | wrong_dataset_empty_result_loop | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | wrong_field_access | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | wrong_query_tool_for_json_source | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | wrong_sql_schema | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | wrong_tool_for_json | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | wrong_top_level_column | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | wrong_year_and_type_handling | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | xml_json_query_tool_mismatch | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | xml_parser_on_json | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | xml_query_file_unsupported | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | zero_row_filter_mismatch | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | broad_shape_peeking_without_extraction | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | catalog and header inspection | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | catalog_metadata_grep_loop | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | catalog_preview_without_followthrough | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | column_and_preview_probing | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | column_and_row_probing | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | column_or_row_sampling_loop | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | district_column_probe | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | file_preview_spiral | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | generic_schema_probe_without_computation | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | geojson_featurecollection_not_flat_table | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | header_preview_only | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | header_preview_over_computation | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | header_preview_retry_loop | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | measure_key_discovery_loop | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | metadata_and_header_peeking | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | metadata_descriptor_confused_for_data_table | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | metadata_file_shape_mismatch | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | metadata_only_loop | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | metadata_preview_and_sample_rows | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | metadata_wrapper_confusion | 1 | gpt-5-mini: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | mixed_schema_probing | 1 | gpt-5-mini: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | nested_geojson_shape_not_unpacked | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | nested_json_shape_probe_loop | 1 | gpt-5-mini: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | preview_and_schema_overuse | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | repeated file-shape probing | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | repeated_file_shape_inspection | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | repeated_file_shape_probe | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | repeated_header_probe | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | repeated_metadata_peek | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | repeated_metadata_peeks | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | repeated_metadata_preview | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | repeated_peek_read_grep_after_query_failures | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | repeated_preview_and_header_probing | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | repeated_preview_and_schema_probing | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | repeated_schema_peeking | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | repeated_schema_probe | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | repeated_schema_sanity_checks | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | repeated_zero_row_recovery_loop | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | row_count_and_column_check_instead_of_required_aggregation | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | row_shape_probe | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | sample_and_count_probe_loop | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | sample_row_probe | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | schema_and_sample_row_chasing | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | schema_peek_drift | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | schema_probe_detour | 1 | gpt-5-mini: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | schema_sampling_over_evidence_extraction | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | wrong_file_preview_loop | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | wrong_parser_for_json | 1 | gpt-5-mini: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | xml_shape_detour | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | year_and_measure_probe_loop | 1 | gpt-5.4-nano: 1 |

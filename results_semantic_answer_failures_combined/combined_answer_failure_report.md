# Combined Answer-Failure Report

Source root: `results_semantic_answer_failures`
Combined CSV: `combined_answer_failure_events.csv`
Total answer-failure events: 746

## Counts by Model

| Model | Events |
| --- | --- |
| gpt-5-mini | 439 |
| gpt-5.4-nano | 307 |

## Counts by Figure Group

| Figure Group | Events | Events by Model |
| --- | --- | --- |
| Scope/filter errors | 172 | gpt-5-mini: 106; gpt-5.4-nano: 66 |
| Answer/finalization failures | 141 | gpt-5-mini: 93; gpt-5.4-nano: 48 |
| Tool/data blockers | 140 | gpt-5-mini: 78; gpt-5.4-nano: 62 |
| Incomplete evidence | 95 | gpt-5-mini: 55; gpt-5.4-nano: 40 |
| Source/dataset errors | 57 | gpt-5-mini: 33; gpt-5.4-nano: 24 |
| Task interpretation / planning | 55 | gpt-5-mini: 35; gpt-5.4-nano: 20 |
| Turn-waste loops | 32 | gpt-5-mini: 6; gpt-5.4-nano: 26 |
| Computation/aggregation errors | 26 | gpt-5-mini: 19; gpt-5.4-nano: 7 |
| Extraction/parsing errors | 25 | gpt-5-mini: 13; gpt-5.4-nano: 12 |
| Evaluation/gold issues | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Other/unclear | 1 | gpt-5.4-nano: 1 |

## Counts by Failure Type

| Figure Group | Failure Type | Events | Events by Model |
| --- | --- | --- | --- |
| Scope/filter errors | wrong_scope_or_filter | 172 | gpt-5-mini: 106; gpt-5.4-nano: 66 |
| Answer/finalization failures | evidence_available_answer_error | 141 | gpt-5-mini: 93; gpt-5.4-nano: 48 |
| Tool/data blockers | tool_or_data_blocker | 140 | gpt-5-mini: 78; gpt-5.4-nano: 62 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | 61 | gpt-5-mini: 46; gpt-5.4-nano: 15 |
| Source/dataset errors | wrong_source_or_dataset | 57 | gpt-5-mini: 33; gpt-5.4-nano: 24 |
| Task interpretation / planning | planning_decomposition_mismatch | 43 | gpt-5-mini: 26; gpt-5.4-nano: 17 |
| Incomplete evidence | incomplete_evidence_early_answer | 34 | gpt-5-mini: 9; gpt-5.4-nano: 25 |
| Computation/aggregation errors | computation_or_aggregation_error | 26 | gpt-5-mini: 19; gpt-5.4-nano: 7 |
| Extraction/parsing errors | extraction_or_parsing_error | 25 | gpt-5-mini: 13; gpt-5.4-nano: 12 |
| Turn-waste loops | query_execution_error_loop | 23 | gpt-5-mini: 3; gpt-5.4-nano: 20 |
| Task interpretation / planning | question_or_constraint_misread | 12 | gpt-5-mini: 9; gpt-5.4-nano: 3 |
| Turn-waste loops | low_yield_search_loop | 8 | gpt-5-mini: 3; gpt-5.4-nano: 5 |
| Evaluation/gold issues | semantic_or_gold_label_issue | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Other/unclear | other_or_unclear | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | 1 | gpt-5.4-nano: 1 |

## Counts by Failure Type and Subtype

| Figure Group | Failure Type | Subtype | Events | Events by Model |
| --- | --- | --- | --- | --- |
| Tool/data blockers | tool_or_data_blocker | tool_budget_exhausted | 58 | gpt-5-mini: 43; gpt-5.4-nano: 15 |
| Tool/data blockers | tool_or_data_blocker | unsupported_or_oversized_data_access | 33 | gpt-5-mini: 19; gpt-5.4-nano: 14 |
| Tool/data blockers | tool_or_data_blocker | data_source_missing_or_unavailable | 26 | gpt-5-mini: 6; gpt-5.4-nano: 20 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | tool_budget_exhausted | 24 | gpt-5-mini: 19; gpt-5.4-nano: 5 |
| Tool/data blockers | tool_or_data_blocker | malformed_tool_call | 12 | gpt-5-mini: 4; gpt-5.4-nano: 8 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | turn_or_time_budget_exhausted | 9 | gpt-5-mini: 8; gpt-5.4-nano: 1 |
| Tool/data blockers | tool_or_data_blocker | ideal_repair_failure | 5 | gpt-5-mini: 2; gpt-5.4-nano: 3 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | (none) | 3 | gpt-5-mini: 1; gpt-5.4-nano: 2 |
| Tool/data blockers | tool_or_data_blocker | runner_or_event_loop_exception | 3 | gpt-5-mini: 3 |
| Incomplete evidence | incomplete_evidence_early_answer | (none) | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | Wayne County scope | 2 | gpt-5-mini: 2 |
| Scope/filter errors | wrong_scope_or_filter | dropped city filter | 2 | gpt-5-mini: 2 |
| Scope/filter errors | wrong_scope_or_filter | omitted_authored_city_based_filter | 2 | gpt-5-mini: 2 |
| Scope/filter errors | wrong_scope_or_filter | wrong_county_lookup | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Tool/data blockers | tool_or_data_blocker | tool_status_or_transport_error | 2 | gpt-5.4-nano: 2 |
| Turn-waste loops | query_execution_error_loop | repeated SQL repair JSONDecodeError | 2 | gpt-5.4-nano: 2 |
| Turn-waste loops | query_execution_error_loop | sql_repair_jsondecodeerror | 2 | gpt-5.4-nano: 2 |
| Answer/finalization failures | evidence_available_answer_error | 09_08_vs_10_28 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | Dallas used instead of Travis | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | answered city instead of county | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | baltimore_county_chain_instead_of_ulster_county | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | computed 13 but submitted 30 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | district_3_instead_of_1 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | final answer contradicted reasoning | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | final answer included extra intermediate school name instead of only the bridge | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | final answer selected the wrong district/year synthesis from off-track SiteISP averages | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | final answer selected wrong value | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | final answer used 1728 instead of 1724 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | final answer used the wrong county pair and returned [4] instead of the task answer | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | final answer used wrong component counts | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | final payload mismatched reasoning | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | final submission chose 6 instead of the required 25 | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | final submission used the wrong school/day | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | final year mismatch | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | final year mismatch after inconsistent reasoning | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | final_answer_included_intermediate_result | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | final_answer_overwrote_intermediate_result | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | final_answer_selected_wrong_entity | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | final_answer_wrong | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | final_submission_included_extra_intermediate_values | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | ignored_lower_competitor_counts | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | incorrect founding year selected from NYC source | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | incorrect_historical_year_off_by_one | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | intermediate_values_in_final_answer | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | misselected Queens instead of Manhattan | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | picked Adam=40 instead of Edward=52 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | picked_1790_from_partial_comparison | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | picked_fort_worth_isd_and_1889_instead_of_lake_worth_isd_and_1916 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | placeholder submission | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | placeholder submitted after finding budget files | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | replaced correct district count 6 with unrelated grep count 20 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | returned school instead of suspension bridge | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | reused top-5 county value | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | rough_estimate_submission | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | selected 1795 instead of 1789 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | selected 1877 instead of 1869 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | selected Chad Brown over James Brown | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | selected Davenport city population as the final answer | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | selected Davenport city population instead of Scott County population | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | selected P.S. 011 instead of PS 056 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | selected the first constable name instead of the superintendent/head name | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | selected the zero Ward 5 result instead of the relevant Ward 1 counts | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | selected_1877_instead_of_target_year | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | selected_broader_parent_department | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | selected_davenport_2020_population_instead_of_scott_county_value | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | selected_wrong_birth_year | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | speculative wrong river choice | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | stopped_at_employer_name | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted -184 instead of -1184 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted -7 instead of 10 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted 108 instead of authoritative 115 | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted 1167 instead of 1650 | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted 163 from null-premise/110 path despite available 103/258 evidence | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted 1835 from Chicago Fire Department instead of 1858 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted 1889 for Fort Worth ISD instead of the correct 1916 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted 1959 despite reasoning for 1916 | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted 1992 instead of 1936 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted 3274 instead of the task answer 2941 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted 35 instead of 4 | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted 380 instead of expected 1220 | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted 4 instead of the correct 7 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted 4369 despite unsupported computation and expected 5021 | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted 542 instead of 14 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted 5882 unchanged from the wrong scoped query result | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted Gerri A. Willis instead of the gold answer O. W. Wilson | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted Loop income 67699 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted University of New Mexico from the wrong person-biography path | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted Uptown/19 instead of Lincoln Square/4 | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted Westmoreland County instead of Accomack County | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted [0] despite computing an internal 4-year difference | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted [30] from the wrong county pair instead of 13 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted [4] despite reasoning 1 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted [5] despite own reasoning rounding to 1 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted answer 1 instead of 113 after downstream calculation | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted answer mismatched own arithmetic | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted bracketed composite answer instead of required single numeric answer | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted bracketed counts instead of required subtraction | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted final answer from 817 minus 1 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted school name instead of bridge | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted the Harbor-based count of 389 from the wrong branch | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted the correct number with extra intermediate values | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted the wrong computed value | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted the wrong final tuple after computing 1822 for Southeast | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted the wrong final year (1848 instead of 1847) | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted wrong final answer | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted wrong final answer [1907] | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted wrong final answer despite correct computed chain | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted wrong final county | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted wrong subtraction from incorrect operand counts | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted wrong value despite correct result in reasoning | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted wrong year despite visible source text | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted wrong-area count unchanged | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_1907_instead_of_1858 | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_1992_instead_of_author_target_1936 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_5_instead_of_9 | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_blank_answer | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_loop_per_capita_income_instead_of_the_intended_branch_result | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_placeholder_instead_of_retrieved_answer | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_value_disagrees_with_last_computation | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | submitted_wrong_final_year | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | substituted location OPEN_DATE for requested school-day fact | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | surface_form_mismatch | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | swapped source-backed bay name | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | switched to P.S. 172 instead of the P.S. 380 candidate | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | switched_to_district_3 | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | used estimate instead of extracted count | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | used estimated count | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | used grep match_count 20 instead of validated private-school count | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | used truncated grep count instead of earlier correct count | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | used wrong NOPD metric branch | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | used_estimated_inputs_instead_of_source_counts | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong community area | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong county attribution | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong final answer from parsed grep subset | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong final answer selection | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong final community area | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong final county/count | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong final district | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong final entity | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong final entity selection | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong final entity: John Brown instead of James Brown | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong final selection | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong final subtraction result | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong founder in final submission | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong founder/university chain | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong founder/year chain | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong school identity | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong university selected from available evidence | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_birth_year_selected | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_branch_and_community_area | 1 | gpt-5.4-nano: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_counts_averaged | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_entity_lineage | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_final_numeric_answer | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_name_selected_at_submission | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_output_format | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_output_shape_scalar_expected | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_public_school_count | 1 | gpt-5-mini: 1 |
| Answer/finalization failures | evidence_available_answer_error | wrong_year_selected_from_available_source | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | broad ranking instead of specific comparison | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | compared an incomplete candidate set and chose the wrong maximum | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | computed 279/299 and rounded to 1 instead of the authored ratio | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | counted an over-broad set of crime codes instead of only the target code | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | extra sector filter | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | invalid_candidate_pair_from_incomplete_intersection | 1 | gpt-5.4-nano: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | left subtraction as an unevaluated expression | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | miscomputed the average and rounded the wrong value | 1 | gpt-5.4-nano: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | off-by-one final arithmetic | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | partial-count peak-year ranking | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | ranked raw rows instead of grouped sum | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | ratio-vs-change-rate mixup | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | raw count submitted instead of rounded per-century result | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | release_winner_ranking_error | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | single-year proxy instead of 2018-2022 average | 1 | gpt-5.4-nano: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | subtracted_the_wrong_operands_for_the_final_difference | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | used AVG instead of SUM | 1 | gpt-5.4-nano: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | used string whitelist instead of numeric > 0 for Used Taser(s), excluding rows with value 2 | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | used_2016_only_instead_of_2016_and_2018_average | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | wrong aggregation grain | 1 | gpt-5.4-nano: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | wrong highest-average agency | 1 | gpt-5.4-nano: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | wrong operands from intermediate queries | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | wrong postsecondary count in final sum | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | wrong ranking aggregation | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | wrong_percentage_basis | 1 | gpt-5-mini: 1 |
| Computation/aggregation errors | computation_or_aggregation_error | zero denominator from parsed Austin school count | 1 | gpt-5.4-nano: 1 |
| Evaluation/gold issues | semantic_or_gold_label_issue | expected answer key conflicts with logged comparison | 1 | gpt-5.4-nano: 1 |
| Evaluation/gold issues | semantic_or_gold_label_issue | gold answer conflicts with source text | 1 | gpt-5-mini: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | assumed wrong column name in file schema | 1 | gpt-5-mini: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | converted OPEN_DATE to MM/DD instead of extracting the required school-day value | 1 | gpt-5-mini: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | extracted first constable instead of requested first head/superintendent | 1 | gpt-5-mini: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | grep matched negated mental-health rows | 1 | gpt-5-mini: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | json wrapper / missing expected columns | 1 | gpt-5.4-nano: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | nested offense field returned null | 1 | gpt-5.4-nano: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | public-school KML filter/path returned zero rows | 1 | gpt-5.4-nano: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | selected 1877 from the AMNH page instead of the intended 1869 founding year | 1 | gpt-5-mini: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | selected Paddock Arcade's 1850 year instead of Watertown's 1869 city-incorporation year | 1 | gpt-5-mini: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | selected birthplace instead of based-in location | 1 | gpt-5.4-nano: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | suppression_regex_cast_zero_rows | 1 | gpt-5.4-nano: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | treated nested GeoJSON as flat table columns | 1 | gpt-5.4-nano: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | treated_geojson_as_flat_table | 1 | gpt-5.4-nano: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | truncated_read_wrong_temperature_value | 1 | gpt-5.4-nano: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | used xml parser on json, then queried fields not exposed by the schema | 1 | gpt-5.4-nano: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | ward field treated as flat column | 1 | gpt-5.4-nano: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | wrong filter/row selection for private-school count | 1 | gpt-5-mini: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | wrong final enrollment answer | 1 | gpt-5-mini: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | wrong historical title/name extracted from Wikipedia snippet | 1 | gpt-5-mini: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | wrong row level aggregation | 1 | gpt-5-mini: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | wrong year extracted from Watertown source | 1 | gpt-5-mini: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | wrong year span from museum page | 1 | gpt-5-mini: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | wrong_column_name | 1 | gpt-5-mini: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | wrong_field_model | 1 | gpt-5.4-nano: 1 |
| Extraction/parsing errors | extraction_or_parsing_error | year_literal_mismatch | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | 30-call tool limit exhausted before district-office verification | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | 30-call tool limit reached before verification completed | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | charter-school hop truncated before downstream county lookup | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | execute-tool budget exhausted | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | hard timeout | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | hard timeout after extra query | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | hard timeout during repair attempts | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | hard_timeout | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | placeholder answer after unresolved area lookup and remaining budget pressure | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | postsecondary_count_still_unresolved | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | repair failure plus tool budget exhaustion before correction | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | timeout before downstream verification | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | tool budget exhausted | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | tool budget exhausted before completing the intended comparison | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | tool budget exhausted before exact extraction | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | tool budget exhausted before first hop finished | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | tool budget exhausted before locating the 2025 Chicago police salary schedule | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | tool budget exhausted before re-checking | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | tool budget exhausted before the adjacency and county hops could be completed | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | tool budget exhausted before third count | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | tool budget exhausted before verification | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | tool limit reached before overtime chain completed | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | tool-call cap reached before extracting both Police Bureau figures | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | tool_budget_exhausted_before_validation | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_budget_exhausted | tool_limit_before_grade_8_9_validation | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | asked for a fallback and submitted unable to determine before deriving the county | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | blank submission before required district evidence was gathered | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | did not page past truncated excerpt | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | empty intermediate result treated as final | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | fallback submission after unresolved query failures | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | insufficient_tool_results | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | missing APD CAD aggregate | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | missing March 2019 traffic-report extraction | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | missing_alumni_and_phd_lookup_before_submit | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | null_submission_after_unproductive_search | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | placeholder_submission | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature answer before county-income lookup | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature answer with approximate estimate | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature unable-to-determine submission | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_submission_after_zero_result_query | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | premature_unable_to_determine | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | stopped after only the 2019 top-five subtask | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | stopped after the first-hop FIPS result and submitted a placeholder | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | stopped with [Unable to determine] after failing to locate required CACFP datasets | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted NaN placeholder before the required subtraction was computed | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted after failed recovery of 2010-2019 crime data | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted before 2018-2020 counts were gathered | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted before CV and downstream hops were finished | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted before comparing the full candidate set | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted before nested feature extraction | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted fallback without ward evidence | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted placeholder answer before completing remaining hops | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_before_full_intersection | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_intermediate_lookup | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | submitted_placeholder_without_required_counts | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | truncated_grep_sample_count | 1 | gpt-5-mini: 1 |
| Incomplete evidence | incomplete_evidence_early_answer | unsupported final guess | 1 | gpt-5-mini: 1 |
| Other/unclear | other_or_unclear | incorrect NYC founding year | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | 2016_only_obesity_query | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | NTA_NAME neighborhood matching instead of exact LOCATION_CODE and NTA-code filtering | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | Texas-wide 2021 ranking instead of intended 2016 rate-category check | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | added_precinct_44_filter_to_final_2022_bronx_inside_count | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | anchored_on_harold_washington_and_loop_instead_of_sulzer_and_lincoln_square | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | bedford_village_only_vadir_checks | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | broad weapon filter instead of target NOPD component | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | broad_keyword_police_filters | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | broader police filter and cost center condition instead of exact department filter | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | broader two-school scope | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | carried the wrong county set into the APS filter | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | confused monument county with Wallops Flight Facility county | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | counted_bid_subset_instead_of_ward_1 | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | county instead of city scope | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | county lookup drifted away from the intended Whitman/Pullman chain | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | county lookup over broader city list | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | county scope drift | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | county substitution | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | county-level public-school subset instead of city-and-county count | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | county-set drift in intake-count query | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | county-wide district ranking instead of direct Pullman School District filter | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | county-wide instead of Orlando subset | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | county/geography pivot from Whitman/Pullman to Garfield/Pomeroy | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | county/year-only filters instead of Boston-specific computation | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | county_instead_of_city_scope | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | county_level_aggregation_ignored_city_in_county_scope | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | county_level_count_omitted_required_city_filter | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | county_level_scope_mismatch | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | county_only_filter | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | county_only_instead_of_chicago_in_county | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | cross_year_filter_applied_to_single_year_file | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | district-office lookup used 0 Massachusetts matches | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | drifted_to_statewide_then_still_missed_city_filter | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | dropped city constraint from public-school count | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | dropped district-9 filter and used all-district sector ranking | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | dropped_boston_city_constraint | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | empty Columbia Heights lookup | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | expanded comparison set | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | expanded county set beyond hop-2 scope | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | extra Council District=9 filter on sector-wide dispatch count | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | extra PRECINCT=44 filter narrowed the 2022 count | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | extra Ward 2 filter instead of all-ward total | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | extra Ward 2 filter on the 2020 count | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | extra agency-name filter on capital-outlay ranking | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | extra_precinct_filter | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | failed cross-year top-five county shortlist; hand-picked a Dallas-containing list | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | filtered Missouri instead of Chicago/Los Angeles | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | final_answer_based_on_bid_counts | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | k003_only_class_size_checks | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | looked up Loop instead of Lincoln Square | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | mis-scoped county/year filter | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | missed Boston-in-Suffolk constraint | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | missing Boston city constraint | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | missing Boston restriction in private-school count | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | missing Chicago-only constraints | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | missing Iowa county filter; schema-mismatched columns | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | missing Lansing city filter on office-count query | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | missing county filter | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | missing_city_filter | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | missing_detroit_city_filter_in_postsecondary_query | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | nmcbsa_matching_instead_of_city_cbsa_filters | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | non_equivalent_nopd_weapon_query | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | non_equivalent_query_shape | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | omitted STATE=TX filter | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | omitted authored filters in school ranking | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | omitted_city_constraint | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | omitted_detroit_city_filter | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | omitted_required_filter_and_used_proxy_grouping | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | over-restricted to precinct 44 in final count | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | overall-offense placeholder before ward anchor | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | pivoted from Pittsburgh to Gary, Indiana after finding the needed budget files | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | pivoted to Dallas County / George M. Dallas instead of the intended county branch | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | population_filter_mis_scoped | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | propagated drifted Charlie sector into the mental-health count | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | propagated_wrong_target_into_final_answer | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | route_66_terminus_shift_to_santa_monica | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | scope_and_output_shape_mismatch | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | searched Chicago street-sweeping datasets while needing Washington, DC | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | single-year scope and malformed filter | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | single_year_sitecounty_instead_of_five_year_cecounty_aps_filter | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | state-specific computation drifted to national county-count queries | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | state_level_counts_instead_of_county_level_intersection | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | submitted_santa_monica | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | switched to Harold Washington branch | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | switched_from_lincoln_square_to_loop | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | switched_terminus_city_to_santa_monica | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | switched_to_bid_subset_after_schema_error | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | switched_to_deb_haaland_unm_instead_of_doug_burgum_ndsu_path | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | texas_vs_puerto_rico_scope_mismatch | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | used 2018 release but only 2015-2016 rows appeared; wrong year slice | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | used AREA 5 instead of AREA 1 | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | used BEDS NUMBER probe instead of name-based location lookup | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | used Chicago/Santa Monica pair instead of Chicago/Los Angeles | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | used MA/Suffolk filter instead of Boston-derived county path | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | used Nueces County instead of the county named after Henry Lawrence Kinney | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | used Santa Monica instead of Los Angeles in the binge-drinking comparison | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | used SiteCounty and omitted exact ProgramYear filters | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | used SiteCounty totals instead of intended county derivation | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | used Suffolk County-wide count instead of Boston-in-Suffolk subset | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | used Wayne County aggregate instead of Detroit-specific school count | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | used `IDENT` text match and `AREA NAME` instead of crime code 354 plus Area ID 9 | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | used a generic Lansing CBSA lookup instead of the school-year-specific authored computation | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | used apd-searches 2021 instead of council-meeting year dependency | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | used broad counts instead of intended intersection chain | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | used city-or-county school count instead of Los Angeles city | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | used county-seat city pages instead of county-level comparison | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | used county/state public-school scope instead of the required city-in-county scope | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | used incidental-to-arrest/probable-cause search filter instead of illegal-items/plain-view | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | used max/frequency instead of the elementary-school Level 1 filter | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | used_wayne_county_only_postsecondary_proxy_and_grep_match_count | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | used_wayne_county_wide_public_school_count_instead_of_detroit_in_wayne_county_count | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wayne_county_used_for_public_school_count | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | widened_candidate_pool | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong DUI area branch | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong birthplace target | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong branch/community-area path | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong branch/entity intersection | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong comparison city pair | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong county branch | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong county branch for last lookup | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong county candidate set | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong county filters and missing program-year filter | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong county path | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong county selected | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong county set and census filter pattern | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong date field/filter path | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong district/entity selected | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong entity branch to Mayorkas/Doug Burgum | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong filter and metric | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong filter branch | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong founder/county pair | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong honoree branch | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong level filter | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong neighborhood branch (Loop instead of Lincoln Square) | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong parcel candidate | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong school/location branch | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong upstream sector metric | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong ward filter for final count | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong year/filter | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_borough_scope | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_branch_and_community_area_path | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_branch_community_area_chain | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_branch_selection | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_city_anchor | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_city_branch | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_comparison_target_and_dataset_branch | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_council_district_or_scope | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_county_branch | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_county_pair | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_district_branch_countywide_district_average_scope | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_entity_branch | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_field_and_filter_substitution | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_field_threshold | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_geography_filter_combination | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_person_or_geography_branch | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_school_person_chain_led_to_baltimore_answer | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_state_lookup | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_terminus_pair | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_year_and_field | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_year_and_filter | 1 | gpt-5.4-nano: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_year_branch | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_year_filter | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_year_filter_on_fy2020_intake | 1 | gpt-5-mini: 1 |
| Scope/filter errors | wrong_scope_or_filter | wrong_year_or_filter | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | 500-cities_vs_city-page | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | DFSS history instead of Chicago Police Department source | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | Puerto Rico school-nutrition detour | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | chicago_street_sweeping_instead_of_dc | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | current_dataset_version | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | current_year_to_date_complaints_dataset_pivot | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | dataset/year drift | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | dataset_mismatch | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | dc_street_sweeping_lookup_drifted_to_chicago_dataset | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | dc_vs_chicago_source_mismatch | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | final head lookup used budget ordinance positions-and-salaries datasets instead of the Chicago Police Department history source | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | maryland_only_income_dataset_instead_of_us_county_ranking_source | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | metadata_like_data_txt_candidate | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | missing_neighborhood_field | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | omitted_circulation_datasets | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | pivoted from Texas identified-student-percentage to Puerto Rico SiteISP/CEP dataset | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | public-school county-count source not identified | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | public_school_dataset_family_mismatch | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | queried adjusted diabetes prevalence and 2010 population instead of the requested crude prevalence and 2020 Census place data | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | release-record counts used instead of intake counts | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | selected day-care-homes 2018 file instead of child-center reimbursement/enrollment datasets | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | selected_postsecondary_dataset_for_district_office_lookup | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | skipped required RIPA area-mapping file | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | stalled in progress-report source family instead of ZIP/census lookup | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | street-sweeping catalog metadata | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | switched from VADIR comparison to AvgOfVio school-safety query | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | used 2020-present crime dataset for 2019 step | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | used APD searches table instead of council voting record for earliest year | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | used CAD file for use-of-force hop | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | used KML data.txt school source/version instead of authored public-school source | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | used OPEN_DATE from locations file instead of school-day source | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | used Wikipedia county pages instead of the census-population source | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | used apd-searches instead of council-meeting-year source | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | used arrest dataset instead of 2019 crime dataset | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | used city pages instead of county-population path | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | used city population dataset instead of county-level population | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | used crime dataset before Brightwood source | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | used crime-data ward inference instead of Adams Morgan source | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | used current-dataset county counts instead of the task's expected counts | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | used current-year-to-date complaints instead of historic complaints source | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | used locations open date instead of school-day source | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | used shooting LOCATION_DESC instead of complaint LOC_OF_OCCUR_DESC | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | used stop-incident dataset instead of the arrest dataset for the DUI-area step | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | used the 2019-20 postsecondary dataset instead of the task-specified Polk County postsecondary count | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | used_arrest_dataset_instead_of_crime_dataset | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | used_current_dataset_instead_of_task_specified_2019_20_source | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | used_parking_violations_instead_of_moving_violations_dataset | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | used_socioeconomic_indicators_instead_of_public_health_indicators | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | wrong APD branch | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | wrong dataset and field for category lookup | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | wrong geography/source family | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | wrong release/year for obesity lookup | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | wrong-year dataset chosen for 2020 county death lookup | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | wrong_dataset | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | wrong_dataset_family | 1 | gpt-5.4-nano: 1 |
| Source/dataset errors | wrong_source_or_dataset | wrong_geography_source_family | 1 | gpt-5-mini: 1 |
| Source/dataset errors | wrong_source_or_dataset | yearly_files_only_missing_adams_morgan_anchor | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | arrest-stage chain divergence | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | broad city lookup and county-count detour instead of the required intersection/count steps | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | broader_capital_filter | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | charter-school SQL skipped the required Ward 5 and grades filter | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | consolidated_multi_year_aggregation | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | council-voting-record year hop replaced by APD search | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | count-only_sql_instead_of_required_top3_intersection_pipeline | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | cross-year_aggregation_repaired_to_year_only_query | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | cross_year_averaging_drift | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | diverged from authored fixed top-five county set | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | diverged from the authored five-step chain by omitting ProgramYear and SiteCounty logic | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | diverged to Deb Haaland instead of Doug Burgum at the DOI hop | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | hardcoded agency list instead of computing the intersection | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | hardcoded counties and wrong output shape for CV step | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | heuristic substring count instead of structured county-intersection computation | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | incomplete_evidence_chain | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | intermediate SQL scope mismatch | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | mismatched 2021 mental-health aggregation path instead of the authored 2015 OMH clinic step | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | non-equivalent county-count queries and placeholder intersection query | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | pivoted from the Ward 7 result to a different Vincent C. Gray / Thomas Jefferson chain and submitted 1743 instead of 1735 | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | raw-row ordering instead of grouped SUM branch aggregation | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | replaced the authored four-year district consistency hop with a county-level minimum query | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | row-count detour instead of county-level ranking | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | sampled_rows_instead_of_district_average | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | schema probing before planned aggregation | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | schema/parsing detour instead of required county-filtering hops | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | single-year county totals SQL omitted required multi-year low-income filter | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | skipped four-year intersection | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | skipped required intersection hop; chose Middlesex instead of Bergen | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | skipped upstream derivation hops | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | skipped yearly branch-intersection before lookup | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | skipped_four_year_intersection_and_final_filters | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | submitted code diverged from authored stepwise computation | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | substituted_wrong_interpreter_chain | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | switched the area-hop from the planned arrest dataset to the 2010-2019 crime dataset | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | used CAD sector hop instead of searches-by-type plan | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | used DIABETES_AdjPrev multi-year intersection instead of authored DIABETES_CrudePrev per-year path | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | used department-description and single-year queries instead of the authored department-number 2019-2021 intersection path | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | used_non_equivalent_single_year_check_as_proxy | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | wrong county-ranking strategy | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | wrong factual chain / wrong entity branch | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | wrong first-hop grouping/filter in SQL | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | planning_decomposition_mismatch | wrong_terminus_branch | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | question_or_constraint_misread | added spurious ward filter on final 2020 count | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | question_or_constraint_misread | answered_with_wrong_historical_frame | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | question_or_constraint_misread | comparison_reversed | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | question_or_constraint_misread | county_fips_query_instead_of_public_school_count | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | question_or_constraint_misread | omitted ProgramYear filter and used generic top-N county count | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | question_or_constraint_misread | omitted required GradeLevel='All Grades' filter | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | question_or_constraint_misread | returned a person name instead of the required university answer | 1 | gpt-5.4-nano: 1 |
| Task interpretation / planning | question_or_constraint_misread | used 2019 average instead of December 2019 threshold | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | question_or_constraint_misread | used `Used Taser(s) = 1` instead of `Used Taser(s) > 0` | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | question_or_constraint_misread | used broad drug-keyword filter instead of exact Narcotic Drug Laws criterion | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | question_or_constraint_misread | used top-5 instead of top-2 | 1 | gpt-5-mini: 1 |
| Task interpretation / planning | question_or_constraint_misread | wrong city pair and prevalence definition | 1 | gpt-5-mini: 1 |
| Tool/data blockers | tool_or_data_blocker | missing_or_malformed_log | 1 | gpt-5-mini: 1 |
| Turn-waste loops | low_yield_search_loop | county-resolution population/adjacency search stalled | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | dataset discovery loop | 1 | gpt-5-mini: 1 |
| Turn-waste loops | low_yield_search_loop | kept re-searching after source set was already identified | 1 | gpt-5-mini: 1 |
| Turn-waste loops | low_yield_search_loop | repeated employer/namesake source discovery yielded no verified fact chain | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated generic searches returned no dataset | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated zero-match Brightwood field probes | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | repeated_searches_no_new_evidence | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | low_yield_search_loop | zero_row_sql_loop | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | code repair failure | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | duckdb UNNEST binder error during aggregation | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | empty_recovery_search_and_bad_sandbox_path | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | flat_sql_and_parser_mismatch_on_nested_json | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | invalid GeoJSON field path | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | jsondecode_error_in_sql_repair | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | nonexistent_column_name | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | placeholder code and generic COUNT(*) query rejected | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | placeholder queries plus SQL repair JSONDecodeError | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repair_cycle | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated JSONDecodeError in query_ideal repair | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated binder errors on GeoJSON SQL | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated binder errors on missing columns | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_jsondecode_repair | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | repeated_malformed_json_extraction_attempts | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | semantic no-match and JSONDecodeError repair failures | 1 | gpt-5-mini: 1 |
| Turn-waste loops | query_execution_error_loop | sql_binder_error | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | sql_binder_errors | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | query_execution_error_loop | sql_repair_failures | 1 | gpt-5.4-nano: 1 |
| Turn-waste loops | schema_or_shape_inspection_loop | repeated schema/shape probing on nested school datasets | 1 | gpt-5.4-nano: 1 |

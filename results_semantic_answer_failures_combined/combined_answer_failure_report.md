# Combined Answer-Failure Report

Source root: `results_semantic_answer_failures`
Combined CSV: `combined_answer_failure_events.csv`
Total answer-failure events: 1533

## Counts by Model

| Model | Events |
| --- | --- |
| gpt-5-mini | 515 |
| gpt-5.4-nano | 1018 |

## Counts by Figure Group

| Figure Group | Events | Events by Model |
| --- | --- | --- |
| Execution/computation failures | 471 | gpt-5-mini: 204; gpt-5.4-nano: 267 |
| Tool blocker failures | 301 | gpt-5-mini: 91; gpt-5.4-nano: 210 |
| Finalization failures | 242 | gpt-5-mini: 108; gpt-5.4-nano: 134 |
| Incomplete evidence failures | 188 | gpt-5-mini: 63; gpt-5.4-nano: 125 |
| Task/planning failures | 153 | gpt-5-mini: 38; gpt-5.4-nano: 115 |
| Turn-waste failures | 101 | gpt-5-mini: 11; gpt-5.4-nano: 90 |
| Wrong source target failures | 77 | gpt-5.4-nano: 77 |

## Counts by Failure Type

| Figure Group | Failure Type | Events | Events by Model |
| --- | --- | --- | --- |
| Execution/computation failures | wrong_scope_or_filter | 364 | gpt-5-mini: 159; gpt-5.4-nano: 205 |
| Tool blocker failures | tool_or_data_blocker | 301 | gpt-5-mini: 91; gpt-5.4-nano: 210 |
| Finalization failures | evidence_available_answer_error | 242 | gpt-5-mini: 108; gpt-5.4-nano: 134 |
| Task/planning failures | planning_decomposition_mismatch | 117 | gpt-5-mini: 28; gpt-5.4-nano: 89 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | 104 | gpt-5-mini: 53; gpt-5.4-nano: 51 |
| Incomplete evidence failures | incomplete_evidence_early_answer | 84 | gpt-5-mini: 10; gpt-5.4-nano: 74 |
| Wrong source target failures | wrong_source_or_dataset | 77 | gpt-5.4-nano: 77 |
| Turn-waste failures | query_execution_error_loop | 60 | gpt-5-mini: 4; gpt-5.4-nano: 56 |
| Execution/computation failures | computation_or_aggregation_error | 54 | gpt-5-mini: 25; gpt-5.4-nano: 29 |
| Execution/computation failures | extraction_or_parsing_error | 53 | gpt-5-mini: 20; gpt-5.4-nano: 33 |
| Task/planning failures | question_or_constraint_misread | 36 | gpt-5-mini: 10; gpt-5.4-nano: 26 |
| Turn-waste failures | schema_or_shape_inspection_loop | 19 | gpt-5-mini: 1; gpt-5.4-nano: 18 |
| Turn-waste failures | low_yield_search_loop | 17 | gpt-5-mini: 3; gpt-5.4-nano: 14 |
| Turn-waste failures | same_hop_repetition | 5 | gpt-5-mini: 3; gpt-5.4-nano: 2 |

## Counts by Failure Type and Subtype

| Figure Group | Failure Type | Subtype | Events | Events by Model |
| --- | --- | --- | --- | --- |
| Tool blocker failures | tool_or_data_blocker | tool_budget_exhausted | 76 | gpt-5-mini: 47; gpt-5.4-nano: 29 |
| Tool blocker failures | tool_or_data_blocker | data_source_missing_or_unavailable | 75 | gpt-5-mini: 10; gpt-5.4-nano: 65 |
| Tool blocker failures | tool_or_data_blocker | unsupported_or_oversized_data_access | 70 | gpt-5-mini: 21; gpt-5.4-nano: 49 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | tool_budget_exhausted | 36 | gpt-5-mini: 19; gpt-5.4-nano: 17 |
| Tool blocker failures | tool_or_data_blocker | malformed_tool_call | 29 | gpt-5-mini: 5; gpt-5.4-nano: 24 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | turn_or_time_budget_exhausted | 20 | gpt-5-mini: 11; gpt-5.4-nano: 9 |
| Tool blocker failures | tool_or_data_blocker | ideal_repair_failure | 20 | gpt-5-mini: 3; gpt-5.4-nano: 17 |
| Tool blocker failures | tool_or_data_blocker | tool_status_or_transport_error | 16 | gpt-5.4-nano: 16 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | (none) | 9 | gpt-5-mini: 1; gpt-5.4-nano: 8 |
| Tool blocker failures | tool_or_data_blocker | runner_or_event_loop_exception | 8 | gpt-5-mini: 3; gpt-5.4-nano: 5 |
| Incomplete evidence failures | incomplete_evidence_early_answer | (none) | 7 | gpt-5-mini: 1; gpt-5.4-nano: 6 |
| Turn-waste failures | query_execution_error_loop | sql_repair_jsondecodeerror | 7 | gpt-5.4-nano: 7 |
| Execution/computation failures | wrong_scope_or_filter | wrong county branch | 4 | gpt-5.4-nano: 4 |
| Finalization failures | evidence_available_answer_error | final_answer_mismatch | 3 | gpt-5.4-nano: 3 |
| Incomplete evidence failures | incomplete_evidence_early_answer | placeholder_submission | 3 | gpt-5.4-nano: 3 |
| Turn-waste failures | query_execution_error_loop | repeated SQL repair JSONDecodeError | 3 | gpt-5.4-nano: 3 |
| Execution/computation failures | computation_or_aggregation_error | off-by-one final arithmetic | 2 | gpt-5-mini: 2 |
| Execution/computation failures | wrong_scope_or_filter | Wayne County scope | 2 | gpt-5-mini: 2 |
| Execution/computation failures | wrong_scope_or_filter | dropped city filter | 2 | gpt-5-mini: 2 |
| Execution/computation failures | wrong_scope_or_filter | omitted authored city-based filter | 2 | gpt-5-mini: 2 |
| Execution/computation failures | wrong_scope_or_filter | wrong county selected | 2 | gpt-5.4-nano: 2 |
| Execution/computation failures | wrong_scope_or_filter | wrong_county_lookup | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | final answer contradicted reasoning | 2 | gpt-5.4-nano: 2 |
| Finalization failures | evidence_available_answer_error | final_answer_mismatch_after_correct_reasoning | 2 | gpt-5.4-nano: 2 |
| Finalization failures | evidence_available_answer_error | submitted wrong final answer | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted_wrong_final_answer | 2 | gpt-5.4-nano: 2 |
| Finalization failures | evidence_available_answer_error | wrong final entity | 2 | gpt-5.4-nano: 2 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | hard timeout | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | hard_timeout | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | tool budget exhausted | 2 | gpt-5-mini: 2 |
| Turn-waste failures | query_execution_error_loop | jsondecodeerror_repair_failure | 2 | gpt-5.4-nano: 2 |
| Turn-waste failures | query_execution_error_loop | repeated binder errors on missing columns | 2 | gpt-5-mini: 1; gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | repeated_sql_repair_failures | 2 | gpt-5.4-nano: 2 |
| Execution/computation failures | computation_or_aggregation_error | arithmetic_error | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | arithmetic_miscalculation | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | bad average | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | broad ranking instead of specific comparison | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | compared an incomplete candidate set and chose the wrong maximum | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | computed 279/299 and rounded to 1 instead of the authored ratio | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | conflicting 2021 ratio computation after switching to 77th Street | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | contradictory final arithmetic leading to unsupported total | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | counted an over-broad set of crime codes instead of only the target code | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | counted counties instead of average intake | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | excluded 2006 from the ranking by filtering out rows with NULL prior-year values | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | extra sector filter | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | fallback_count_off_by_two | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | final sum reported as 380 instead of 369 | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | incorrect per-century arithmetic | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | incorrect_average_and_rounding | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | inverse ratio used | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | left subtraction as an unevaluated expression | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | off-by-one threshold selection | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | partial-count peak-year ranking | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | percent_change_vs_share_of_2020 | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | proxy metric instead of authored total_incidents/top-3 computation | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | ranked raw rows instead of grouped sum | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | ratio-vs-change-rate mixup | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | raw count submitted instead of rounded per-century result | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | release_winner_ranking_error | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | sampled grep count for 2017 Ward 1 | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | sampled grep counts used for final answer | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | single-year proxy instead of 2018-2022 average | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | single_year_result_instead_of_four_year_average | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | submitted the retrieved postsecondary count as the final answer | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | subtracted_the_wrong_operands_for_the_final_difference | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | switched to weighted-average budget ratios and the wrong department-number set | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | used 2017 total instead of the two-year average | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | used AVG instead of SUM | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | used only 2019 counts divided by 3 instead of a real 2019-2021 average | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | used string whitelist instead of numeric > 0 for Used Taser(s), excluding rows with value 2 | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | used_2016_only_instead_of_2016_and_2018_average | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | used_2018_only_intermediate_average | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | used_whole_nj_row_count_instead_of_required_county_logic | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | used_wrong_area_count_branch_for_final_ratio | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | wrong aggregation field and scope | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | wrong aggregation grain | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | wrong denominator / used within-year share instead of 2021-to-2020 count ratio | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | wrong highest-average agency | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | wrong operands from intermediate queries | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | wrong postsecondary count in final sum | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | wrong ranking aggregation | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | wrong_aggregation_shape | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | computation_or_aggregation_error | wrong_count_in_final_sum | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | wrong_percentage_basis | 1 | gpt-5-mini: 1 |
| Execution/computation failures | computation_or_aggregation_error | zero denominator from parsed Austin school count | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | DuckDB queries referenced nonexistent bound-table columns t.json and t.data | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | assumed flat ISSUING_AGENCY_NAME field | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | assumed wrong column name in file schema | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | assumed_flat_table | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | confused founding year with birth year | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | confused museum establishment year with first-purpose-built-structure year | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | converted OPEN_DATE to MM/DD instead of extracting the required school-day value | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | count step returned location string | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | extracted first constable instead of requested first head/superintendent | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | first constable instead of first head | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | grep matched negated mental-health rows | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | misread founding year | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | missing_numeric_value | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | nested offense field returned null | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | null_rows_returned | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | numeric county codes instead of county names | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | precinct/count mix-up | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | public-school KML filter/path returned zero rows | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | queried unsupported School Name/2013 columns in the performance directory | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | read mismatched year/metric columns in the performance directory | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | referenced nonexistent CITY column | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | selected 1877 from the AMNH page instead of the intended 1869 founding year | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | selected Paddock Arcade's 1850 year instead of Watertown's 1869 city-incorporation year | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | selected birthplace instead of based-in location | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | selected_city_charter_year_instead_of_town_charter_year | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | submitted 1877 from the structure date instead of 1869 | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | suppression_regex_cast_zero_rows | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | treated nested GeoJSON as a flat table | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | treated nested GeoJSON as flat table columns | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | treated ward-count list as averages | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | treated_geojson_as_flat_table | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | truncated_read_wrong_temperature_value | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | used CITY/STATE instead of borough | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | used museum opening/structure-year fact instead of founding year | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | used the museum opening/building date instead of the founding year | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | used xml parser on json, then queried fields not exposed by the schema | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | wrong enrollment value from correct Pullman row | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | wrong field name: Conservation_Status vs NY Listing Status | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | wrong filter/row selection for private-school count | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | wrong historical title/name extracted from Wikipedia snippet | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | wrong intermediate counts for Polk County | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | wrong person-name lookup | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | wrong postsecondary count extracted | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | wrong row level aggregation | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | wrong year extracted from Watertown source | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | wrong year span from museum page | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | wrong_column_name | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | wrong_field_and_parser | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | wrong_field_for_state_code_lookup | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | wrong_field_model | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | wrong_year_source | 1 | gpt-5-mini: 1 |
| Execution/computation failures | extraction_or_parsing_error | xml filter returned zero rows | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | extraction_or_parsing_error | xml_kml_file_misparsed_or_handled_as_json | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | 2016-only city slice | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | 2018_only_fallback | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | 2023 query returned top-5 county slice instead of target counties | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | Bedford Village-only VADIR checks | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | DFSS history instead of Chicago Police Department source | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | Illinois county-wide slice instead of Chicago/Cook County | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | K003-only class-size checks | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | NTA_NAME neighborhood matching instead of exact LOCATION_CODE and NTA-code filtering | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | Puerto Rico school-nutrition detour | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | SiteCounty_vs_CECounty | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | Texas-wide 2021 ranking instead of intended 2016 rate-category check | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | added precinct=44 filter to the final 2022 Bronx INSIDE count | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | all counties instead of Los Angeles County | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | anchored on Harold Washington Library Center and the Loop instead of Sulzer Regional Library and Lincoln Square | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | approximate_crime_description_filter | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | broad county aggregation instead of Sacramento County-specific filter | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | broad department matching | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | broad services substring filter | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | broad weapon filter instead of target NOPD component | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | broad_statewide_query_instead_of_restricted_intersection | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | broadened county scope without Chicago filter | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | broader county shortlist than intended comparison | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | broader two-school scope | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | carried the wrong county set into the APS filter | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | chicago_street_sweeping_instead_of_dc | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | chose Austin/Travis instead of Houston/Harris | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | city_scope_mismatch | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | collapsed the county intersection to Eastland only | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | collapsed the first hop into a single-year FY2007 query; later binder error on quoted column names | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | counted_bid_subset_instead_of_ward_1 | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | county filter mismatch across FY2019 vs specific counties | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | county instead of city scope | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | county lookup over broader city list | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | county selection mismatch | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | county substitution | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | county-level aggregation ignored city-in-county scope | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | county-level count omitted required city filter | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | county-level public-school subset instead of city-and-county count | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | county-set drift in intake-count query | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | county-wide district ranking instead of direct Pullman School District filter | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | county-wide instead of Orlando subset | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | county-wide instead of chicago-in-cook-county | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | county/geography pivot from Whitman/Pullman to Garfield/Pomeroy | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | county/year-only filters instead of Boston-specific computation | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | county_count_used_instead_of_city_count | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | county_fips_query_instead_of_public_school_count | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | county_instead_of_city | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | county_instead_of_city_scope | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | county_intersection_misapplied | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | county_level_scope_mismatch | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | county_only_filter | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | county_only_instead_of_chicago_in_county | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | cross_year_filter_applied_to_single_year_file | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | current-year-to-date complaints dataset pivot | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | current_dataset_version | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | dataset/year drift | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | dataset_drift | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | dataset_mismatch | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | dataset_version_mismatch | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | dc street-sweeping lookup drifted to Chicago dataset | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | dc_vs_chicago_source_mismatch | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | district-office lookup used 0 Massachusetts matches | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | district-office query used CBSA 7 instead of Lansing CBSA 29620 | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | district_15_school_set_mismatch | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | district_3_instead_of_1 | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | drifted_to_statewide_then_still_missed_city_filter | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | dropped city constraint from public-school count | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | dropped district-9 filter and used all-district sector ranking | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | dropped_boston_city_constraint | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | empty Columbia Heights lookup | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | expanded agency set for employee counts | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | expanded county set beyond hop-2 scope | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | extra Council District=9 filter on sector-wide dispatch count | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | extra PRECINCT=44 filter narrowed the 2022 count | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | extra Ward 2 filter instead of all-ward total | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | extra Ward 2 filter on the 2020 count | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | extra agency-name filter on capital-outlay ranking | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | failed cross-year top-five county shortlist; hand-picked a Dallas-containing list | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | filtered Columbia Heights neighborhood-cluster text instead of Ward 1 offense counts | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | final head lookup used budget ordinance positions-and-salaries datasets instead of the Chicago Police Department history source | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | final_answer_based_on_bid_counts | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | five_cycle_intersection_instead_of_single_record | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | fixed-county subset instead of threshold filters | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | geography_file_pivot | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | graduation_rate_cohort_filter_mismatch | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | guessed Route 66 city list | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | historical_year_mismatch | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | illinois-wide county scope instead of chicago-in-cook-county | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | included Orange County outside the required intersection | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | included_2015_value_below_6_9m_floor | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | income threshold not applied | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | incomplete_evidence_chain | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | incorrect FY2019 contractor filter and grouping | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | incorrect county-seat selection | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | kept Monroe in candidate set | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | looked up Community Area 52 / West Loop instead of the target area | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | looked up Loop instead of Lincoln Square | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | maryland-only income dataset instead of U.S.-wide county ranking source | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | metadata_like_data_txt_candidate | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | mis-scoped county/year filter | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | misclassified Harris in the original-23 county filter | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | mismatched_sitecounty_vs_cecounty_scope | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | missed Boston-in-Suffolk constraint | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | missed required CPS Performance Policy Level filter | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | missing Boston city constraint | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | missing Boston city filter on office query | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | missing Boston restriction in private-school count | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | missing Chicago-only constraints | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | missing Iowa county filter; schema-mismatched columns | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | missing Lansing city filter on office-count query | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | missing_city_filter | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | missing_detroit_city_filter_in_postsecondary_query | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | missing_required_filters_and_normalization | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | missouri_only_filter | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | mixed county candidate set with Kings | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | monthly-max aggregation on ward 2 instead of requested year comparison | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | neighborhood_cluster_guess_instead_of_ward_based_offense_counts | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | nibrs_offense_dataset | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | no Adams Morgan matches in 2017 lookup | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | non-equivalent NOPD weapon query | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | non_equivalent_query_shape | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | off-target Springfield, Missouri binge-drinking lookup instead of the required comparison | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | off_plan_2018_2019_locations_file | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | omitted STATE=TX filter | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | omitted authored filters in school ranking | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | omitted_circulation_datasets | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | omitted_city_constraint | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | omitted_detroit_city_filter | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | omitted_required_filter_and_used_proxy_grouping | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | opened Monroe County, New York instead of Westmoreland County, Virginia | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | original Texas counties were not excluded from the release comparison | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | over-restricted to precinct 44 in final count | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | overall-offense placeholder before ward anchor | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | overbroad candidate set still included HAYS | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | overfiltered_query_or_wrong_filter | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | percentile-rank substitution | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | picked a misaligned CACFP year-file source set | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | pivoted from Pittsburgh to Gary, Indiana after finding the needed budget files | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | pivoted from Texas identified-student-percentage to Puerto Rico SiteISP/CEP dataset | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | pivoted to Dallas County / George M. Dallas instead of the intended county branch | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | pivoted to FBI and broad candidate-agency queries | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | pivoted to unrelated 311 data after street-sweeping source mismatch | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | population_filter_mis_scoped | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | propagated drifted Charlie sector into the mental-health count | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | public-school county-count source not identified | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | public-school dataset family mismatch | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | queried ACCESS2_AdjPrev and a broad CT city list instead of New Haven/Bridgeport ACCESS2_CrudePrev | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | queried adjusted diabetes prevalence and 2010 population instead of the requested crude prevalence and 2020 Census place data | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | queried only 2018-19 instead of the required 2018-19..2021-22 intersection | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | region label mismatch | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | release-record counts used instead of intake counts | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | row-count probe instead of county-filtered reimbursement aggregation | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | scope_and_output_shape_mismatch | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | searched Chicago street-sweeping datasets while needing Washington, DC | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | searched for unnecessary earlier assessment years | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | searched_wrong_charge_term | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | searched_wrong_city_or_dataset | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | selected Monroe County instead of James Monroe's birth county | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | selected day-care-homes 2018 file instead of child-center reimbursement/enrollment datasets | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | selected metadata wrapper instead of rows file | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | selected moving-violations instead of parking-violations | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | single-year checks instead of cross-year intersection | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | single-year scope and malformed filter | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | single_cycle_only_instead_of_five_cycle_intersection | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | single_year_approximation_instead_of_two_year_intersection | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | single_year_sitecounty_instead_of_five_year_cecounty_aps_filter | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | skipped required RIPA area-mapping file | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | stalled in progress-report source family instead of ZIP/census lookup | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | state-specific computation drifted to national county-count queries | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | state_level_counts_instead_of_county_level_intersection | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | statewide_county_fips_instead_of_detroit_wayne_county | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | stfip_state_mismatch | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | street-sweeping catalog metadata | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | submitted Santa Monica | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | switched from VADIR comparison to AvgOfVio school-safety query | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | switched from the PS 321 intersection to P.S. 172 Beacon School of Excellence | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | switched to Deb Haaland/UNM instead of Doug Burgum/NDSU path | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | switched to Harold Washington branch | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | switched to P.S. 172 instead of the P.S. 380 candidate | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | switched_from_lincoln_square_to_loop | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | switched_terminus_city_to_santa_monica | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | switched_to_bid_subset_after_schema_error | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | switched_to_county_code_filters | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | texas_vs_puerto_rico_scope_mismatch | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | truncated grep sample instead of full 2018 dataset | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used 2018 release but only 2015-2016 rows appeared; wrong year slice | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used 2019-only county ranking instead of four-year CV scope | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used 2020-present crime dataset for 2019 step | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used 2021-22/current private and postsecondary sources | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used APD searches table instead of council voting record for earliest year | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used AREA 5 instead of AREA 1 | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used BEDS NUMBER probe instead of name-based location lookup | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used BLOCK/NEIGHBORHOOD_CLUSTER string matching instead of the planned ward/offense chain | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used CAD file for use-of-force hop | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used Chicago/Santa Monica pair instead of Chicago/Los Angeles | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used DEPARTMENT DESCRIPTION instead of DEPARTMENT NUMBER in the first-hop appropriations query | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used Death County with loose 2020 matching instead of Residence County with >200 cutoff | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used KML data.txt school source/version instead of authored public-school source | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used MA/Suffolk filter instead of Boston-derived county path | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used Missouri city filters instead of Chicago/Los Angeles | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used NMCBSA-based matching instead of CITY+CBSA filters | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used Nueces County instead of the county named after Henry Lawrence Kinney | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used OPEN_DATE from locations file instead of school-day source | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used Rochester history and submitted 1834 | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used Santa Monica instead of Los Angeles in the binge-drinking comparison | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used SiteCounty and omitted exact ProgramYear filters | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used SiteCounty totals instead of intended county derivation | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used Suffolk County-wide count instead of Boston-in-Suffolk subset | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used Wayne County aggregate instead of Detroit-specific school count | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used Wayne County-only postsecondary proxy and grep match count instead of Detroit-in-Wayne-County filtered count | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used Wayne County-wide public-school count instead of Detroit-in-Wayne-County count | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used Westmoreland County instead of Accomack County | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used Wikipedia county pages instead of the census-population source | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used `IDENT` text match and `AREA NAME` instead of crime code 354 plus Area ID 9 | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used a generic Lansing CBSA lookup instead of the school-year-specific authored computation | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used apd-searches 2021 instead of council-meeting year dependency | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used apd-searches instead of council-meeting-year source | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used arrest dataset for crime-code lookup | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used arrest dataset instead of 2019 crime dataset | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used arrest dataset instead of crime dataset | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used arrest-data source for the 2019 description lookup | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used arrest-side result as the 2019 crime description | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used broad counts instead of intended intersection chain | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used city population dataset instead of county-level population | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used city-or-county school count instead of Los Angeles city | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used county-mental-health-profiles-2006-2016 instead of county-mental-health-profiles-phase-2-beginning-2014 | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used county-only Orange County filter instead of the authored Orlando city-specific filter | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used county-seat city pages instead of county pages | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used county-seat city pages instead of county-level comparison | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used county-seat city population instead of county population | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used county/state public-school scope instead of the required city-in-county scope | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used crime dataset before Brightwood source | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used crime-data ward inference instead of Adams Morgan source | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used current dataset instead of task-specified 2019-20 source | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used current-dataset county counts instead of the task's expected counts | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used current-year-to-date complaints instead of historic complaints source | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used full original county set instead of post-hop-1 remainder | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used incidental-to-arrest/probable-cause search filter instead of illegal-items/plain-view | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used locations open date instead of school-day source | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used max/frequency instead of the elementary-school Level 1 filter | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used parking-violations instead of moving-violations dataset | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used shooting LOCATION_DESC instead of complaint LOC_OF_OCCUR_DESC | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used stop-incident dataset instead of the arrest dataset for the DUI-area step | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used the 2008-2012 socioeconomic indicators dataset instead of the public-health-indicators dataset named in the task plan | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used the 2010-2019 crime dataset instead of the needed arrest dataset family | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used wrong NOPD metric branch | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used wrong crime description in the 2020-present computation | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used_2010_to_2019_crime_file_for_2021_count_instead_of_2020_to_present | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | used_address_instead_of_neighborhood_mapping | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | used_global_school_count_instead_of_los_angeles_only | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | ward-2 assumption instead of ward-1 path | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wayne-county-mi-query-instead-of-authored-detroit-path | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wayne-county-wide-count-instead-of-target-city | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wayne_county_used_for_public_school_count | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | widened_candidate_pool | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong 4-year August cohort and DBN output instead of 4 Year June school_name | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong APD branch | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong Detroit slice | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong area branch: Area 15 / N Hollywood instead of Area 9 / Van Nuys | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong birthplace target | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong branch/community-area path | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong branch/entity intersection | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong branch/geography endpoint | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong candidate pair | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong city comparison | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong city pair / loose binge filter | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong city set and year scope | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong city/county branch: Rochester in Monroe County instead of Syracuse/Onondaga County | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong class-size predicate | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong comparison city pair | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong comparison target and dataset branch | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong county branch for last lookup | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong county candidate set | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong county filters and missing program-year filter | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong county path | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong county path (Essex instead of Bergen) | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong county selected in the release comparison | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong county set and census filter pattern | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong dataset | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong dataset and field for category lookup | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong date field/filter path | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong district branch / countywide district-average scope | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong district/entity selected | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong entity branch | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong entity branch to Mayorkas/Doug Burgum | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong factual chain / wrong entity branch | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong file path for header/schema lookup | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong filter and metric | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong filter branch | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong founder/county pair | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong geography (Chicago instead of Washington, DC) | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong geography/filter combination | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong geography/source family | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong geography; Chicago street-sweeping instead of DC | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong historical figure | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong honoree branch | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong intermediate branch | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong neighborhood branch (Loop instead of Lincoln Square) | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong offense category | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong parcel candidate | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong person in namesake chain | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong release/year for obesity lookup | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong school branch | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong school/location branch | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong school/person chain led to Baltimore answer | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong terminus pair | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong university/entity selected | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong upstream sector metric | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong ward | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong ward filter for final count | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong ward/offense chain | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong year / nonexistent location dataset | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong year filter on FY2020 intake | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong year/filter | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong-year dataset chosen for 2020 county death lookup | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_borough_scope | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_branch_and_community_area_path | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_branch_community_area_chain | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_branch_selected | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_chained_ward_offense_path | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_city_anchor | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_city_and_ward_scope | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_city_branch | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_city_lookup | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_city_selection | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_council_district_or_scope | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_county_branch | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_county_pair | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_county_selection | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_crime_descriptor | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_entity_chain | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_field_and_filter_substitution | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_field_threshold | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_geography_source_family | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_king_entity | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_medicare_part_d_family | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_person_or_geography_branch | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_school_dbn | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_school_neighborhood_branch | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_state_filter | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_state_lookup | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_year_and_field | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_year_and_filter | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_year_branch | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_year_filter | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_year_or_filter | 1 | gpt-5-mini: 1 |
| Execution/computation failures | wrong_scope_or_filter | wrong_year_or_source_slice | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | year_literal_mismatch | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | year_release_filter | 1 | gpt-5.4-nano: 1 |
| Execution/computation failures | wrong_scope_or_filter | yearly_files_only_missing_adams_morgan_anchor | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | (none) | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | 09_08_vs_10_28 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | Dallas used instead of Travis | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | answer-text contradicts reasoning | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | answered city instead of county | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | answered with paternal grandmother instead of the requested grandfather | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | baltimore_county_chain_instead_of_ulster_county | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | bay_name_mismatch | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | blank_final_submission | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | city population substituted for county value | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | claimed empty intersection despite PS 321 appearing in all three yearly top-2 lists | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | computed 13 but submitted 30 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | contradictory evidence ignored in final synthesis | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | county/statue name mix-up | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | fallback answer [0] | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | fallback placeholder submitted | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | final answer changed 1735 to 1734 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | final answer contradicted gathered evidence; submitted Lincoln Belmont instead of Lincoln Square | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | final answer contradicted retrieved evidence | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | final answer contradicted the common school already visible in prior outputs | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | final answer contradicted the correct Interior-chain reasoning | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | final answer included extra intermediate school name instead of only the bridge | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | final answer selected the wrong district/year synthesis from off-track SiteISP averages | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | final answer selected wrong value | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | final answer used 1728 instead of 1724 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | final answer used branch name instead of neighborhood name | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | final answer used the wrong county pair and returned [4] instead of the task answer | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | final answer used wrong component counts | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | final entity answer is wrong after the correct agency was identified | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | final payload mismatched reasoning | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | final submission chose 6 instead of the required 25 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | final submission used the wrong school/day | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | final year mismatch | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | final year mismatch after inconsistent reasoning | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | final-hop wrong interpreter/year selected | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | final_answer_disagrees_with_computed_result | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | final_answer_does_not_match_stated_calculation | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | final_answer_included_intermediate_result | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | final_answer_overwrote_intermediate_result | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | final_answer_selected_wrong_entity | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | final_answer_wrong | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | final_submission_included_extra_intermediate_values | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | ignored correct 1740 result | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | ignored the Doc Scurlock to Tallapoosa County to Dadeville chain | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | ignored_lower_competitor_counts | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | incorrect founder selection | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | incorrect founder-year chain | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | incorrect founding year selected from NYC source | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | incorrect_historical_year_off_by_one | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | incorrectly placed Wallops Flight Facility in Westmoreland County | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | intermediate_values_in_final_answer | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | inverted comparison at submission | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | late answer substitution to Pottawattamie County count 1 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | misattributed Lincoln University founder/year | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | misselected Queens instead of Manhattan | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | picked Adam=40 instead of Edward=52 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | picked_1790_from_partial_comparison | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | picked_fort_worth_isd_and_1889_instead_of_lake_worth_isd_and_1916 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | placeholder submission | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | placeholder submitted after finding budget files | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | placeholder submitted instead of county-seat name | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | placeholder_final_answer | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | replaced correct district count 6 with unrelated grep count 20 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | returned school instead of suspension bridge | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | returned_intermediate_entity_instead_of_operating_agency | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | rough_estimate_submission | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | selected 1795 despite retrieved evidence showing 1789 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | selected 1795 instead of 1789 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | selected 1850 despite source excerpt showing 1869 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | selected 1877 instead of 1869 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | selected Chad Brown over James Brown | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | selected Davenport city population as the final answer | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | selected Davenport city population instead of Scott County population | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | selected Dunfermline instead of Pittsburgh | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | selected P.S. 011 instead of PS 056 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | selected charter year instead of origin year | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | selected parent department instead of operating agency | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | selected the Monroe/Rochester path instead of the Onondaga/Syracuse path | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | selected the first constable name instead of the superintendent/head name | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | selected the wrong year after the correct page evidence was available | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | selected the zero Ward 5 result instead of the relevant Ward 1 counts | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | selected wrong final answer | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | selected_1795_instead_of_1789 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | selected_1877_instead_of_target_year | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | selected_broader_parent_department | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | selected_davenport_2020_population_instead_of_scott_county_value | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | selected_wrong_birth_year | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | speculative wrong river choice | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | stopped_at_employer_name | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted -184 instead of -1184 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted -7 instead of 10 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted 103 instead of 115 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted 108 instead of authoritative 115 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted 1167 instead of 1650 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted 12 instead of 64 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted 163 from null-premise/110 path despite available 103/258 evidence | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted 1779 despite reasoning citing 1799 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted 1835 from Chicago Fire Department instead of 1858 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted 1889 for Fort Worth ISD instead of Lake Worth ISD 1916 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted 1907 instead of 1858 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted 1959 despite reasoning for 1916 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted 1965 after following the wrong Baruch-based branch | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted 1983 unchanged from the wrong area count | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted 1992 instead of 1936 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted 2010 instead of 1624 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted 2022 instead of 1653 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted 3274 instead of the task answer 2941 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted 35 instead of 4 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted 380 instead of expected 1220 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted 4 instead of the correct 7 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted 4369 despite unsupported computation and expected 5021 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted 501 instead of 26010.5 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted 542 instead of 14 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted 5882 unchanged from the wrong scoped query result | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted Baltimore County/Banneker instead of Sojourner Truth PCS/Ulster County | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted Cook County instead of Sedgwick County | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted Davenport city population instead of county population | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted Devonshire 1228 instead of Van Nuys 761 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted Gerri A. Willis instead of the gold answer O. W. Wilson | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted Loop income 67699 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted Queens instead of Manhattan | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted University of New Mexico from the wrong person-biography path | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted Uptown/19 instead of Lincoln Square/4 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted [0] despite computing an internal 4-year difference | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted [15672] despite reasoning that the result was 176 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted [1834] instead of the correct [1832] branch | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted [1] despite reasoning that result was 3 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted [30] from the wrong county pair instead of 13 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted [4] despite reasoning 1 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted [5] despite own reasoning rounding to 1 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted answer 1 instead of 113 after downstream calculation | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted answer contradicted stated arithmetic | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted answer contradicts reasoning | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted answer mismatched own arithmetic | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted blank answer | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted bracketed composite answer instead of required single numeric answer | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted bracketed counts instead of required subtraction | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted fallback 2020 count instead of the required 2020-minus-2019 difference | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted final answer from 817 minus 1 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted invalid placeholder instead of bay name | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted over-restricted count | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted school name instead of bridge | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted the Harbor-based count of 389 from the wrong branch | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted the correct number with extra intermediate hop values instead of the required single value | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted the wrong computed answer | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted the wrong computed value | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted the wrong final tuple after computing 1822 for Southeast | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted the wrong final year (1848 instead of 1847) | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted wrong final answer [1907] | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted wrong final answer despite correct computed chain | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted wrong final county | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted wrong final lookup result | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted wrong subtraction from incorrect operand counts | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted wrong value despite correct result in reasoning | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted zero-count answer | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted-answer-used-unsupported-postsecondary-count | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted_1850_instead_of_1869 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted_1992_instead_of_author_target_1936 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted_324_despite_reasoning_110 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted_35_instead_of_71 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted_5_instead_of_9 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted_8_instead_of_13 | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted_count_instead_of_percentage | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted_intermediate_year_instead_of_final_count | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted_loop_per_capita_income_instead_of_the_intended_branch_result | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted_placeholder_instead_of_retrieved_answer | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted_unable_to_determine_placeholder_instead_of_numeric_answer | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted_unknown_after_partial_progress | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted_value_disagrees_with_last_computation | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted_wrong_final_year | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | submitted_wrong_founder_name | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted_zero | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | submitted_zero_after_dead_end | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | substituted location OPEN_DATE for requested school-day fact | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | surface_form_mismatch | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | swapped source-backed bay name | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | switched_to_district_3 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | switched_to_joseph_la_flesche_1822 | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | unsupported county-to-town inference; wrong largest town | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | unsupported final arithmetic and wrong synthesized answer | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | used estimate instead of extracted count | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | used estimated count | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | used grep match_count 20 instead of validated private-school count | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | used the wrong state-admission lookup in the final answer | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | used truncated grep count instead of earlier correct count | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | used_estimated_inputs_instead_of_source_counts | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | wrong Chicago population value | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong acreage value | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong bay from river-mouth linkage | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong city pair led to wrong final county value | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong community area | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | wrong county attribution | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong county pair in final computation | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong county/district path used in final synthesis | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong county/year path | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong downstream entity selection | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong downstream university/founder pair | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong final answer from parsed grep subset | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | wrong final answer selection | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong final community area | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong final county-seat hop | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong final county/count | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | wrong final district | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | wrong final entity selection | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong final entity: John Brown instead of James Brown | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | wrong final location lookup used Loop instead of Lincoln Square | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong final selection | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | wrong final subtraction result | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | wrong founder in final submission | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong founder/university chain | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong school identity | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong_birthplace_population | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong_branch_and_community_area | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong_counts_averaged | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | wrong_final_answer | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong_final_entity_lineage | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | wrong_final_numeric_answer | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | wrong_final_park_answer | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | wrong_final_total | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | wrong_final_year | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong_founder_name | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong_incorporation_year | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong_name_selected_at_submission | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | wrong_output_format | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | wrong_output_shape_scalar_expected | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | wrong_public_school_count | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | wrong_rounding_or_transcription | 1 | gpt-5.4-nano: 1 |
| Finalization failures | evidence_available_answer_error | wrong_year_selected | 1 | gpt-5-mini: 1 |
| Finalization failures | evidence_available_answer_error | wrong_year_selected_from_available_source | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | 30-call tool limit exhausted before district-office verification | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | 30-call tool limit reached before verification completed | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | allotted_calls_exhausted_before_completion | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | charter-school hop truncated before downstream county lookup | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | execute-tool budget exhausted | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | hard timeout after extra query | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | hard timeout before averaging and federal-agency lookup | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | hard timeout during repair attempts | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | hard timeout exhausted before a valid answer was submitted | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | hard_timeout_before_submission | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | placeholder answer after unresolved area lookup and remaining budget pressure | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | postsecondary_count_still_unresolved | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | repair failure plus tool budget exhaustion before correction | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | stopped after common-school stage before neighborhood/material/structure/year hops | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | time_budget_exhausted | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | timeout before completing the remaining reasoning chain | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | tool budget exhausted before completing the intended comparison | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | tool budget exhausted before downstream hops | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | tool budget exhausted before exact extraction | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | tool budget exhausted before locating the 2025 Chicago police salary schedule | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | tool budget exhausted before re-checking | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | tool budget exhausted before the adjacency and county hops could be completed | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | tool budget exhausted before third count | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | tool budget exhausted before verification | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | tool execution errors/time prevented completion | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | tool limit reached before overtime chain completed | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | tool-call cap reached before extracting both Police Bureau figures | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | tool-call limit exhausted before final answer; submitted [null] | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | tool_budget_exhausted_before_submission | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | tool_budget_exhausted_before_validation | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | tool_call_limit_reached | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | tool_limit_before_grade_8_9_validation | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_budget_exhausted | tool_limit_reached_before_park_lookup | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | answered [0] after a schema/preview-only postsecondary step | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | answered with a placeholder before deriving the required result | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | asked for a fallback and submitted unable to determine before deriving the county | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | blank submission before required district evidence was gathered | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | blank_answer_after_failed_searches | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | county-seat lookup omitted | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | did not page past truncated excerpt | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | fallback submission after unresolved query failures | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | fallback submission before completing required lookups | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | incorporation year not retrieved | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | insufficient_tool_results | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | missing APD CAD aggregate | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | missing March 2019 traffic-report extraction | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | missing firearm-count lookup | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | missing_alumni_and_phd_lookup_before_submit | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | missing_wikipedia_birth_year_hop | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | no acreage lookup | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | null_submission_after_unproductive_search | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | placeholder execute call followed by submission of [Unknown] before resolving the remaining lookup | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | placeholder submitted before year lookup | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | premature answer before county-income lookup | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | premature answer with approximate estimate | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | premature placeholder submission | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | premature submission without required evidence | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | premature_submission | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | premature_submission_after_empty_intersection | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | premature_submission_after_zero_result_query | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | premature_unable_to_determine | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | skipped king/birth-year lookup | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | stopped after GeoJSON shape discovery | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | stopped after intermediate pay analysis | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | stopped after only the 2019 top-five subtask | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | stopped after the first-hop FIPS result and submitted a placeholder | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | stopped and submitted without extracting the county rankings | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | stopped with [Unable to determine] after failing to locate required CACFP datasets | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted NaN placeholder before the required subtraction was computed | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted [N/A] without isolating the firm | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted [UNKNOWN] before gathering the later-hop evidence needed to identify the department and first head | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted [Unable to determine] before extracting or computing from the selected datasets | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted [Unknown] before resolving the required chain | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted after failed recovery of 2010-2019 crime data | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted after first-hop ward result | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted after intermediate Springfield hop | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted after partial evidence without completing the required violent-incident comparison | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted before 2018-2020 counts were gathered | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted before CV and downstream hops were finished | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted before comparing the full candidate set | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted before computing final formula | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted before remaining required evidence | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted blank answer after stopping early | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted fallback without ward evidence | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted insufficient data after the schema dead-end instead of continuing the DBN-to-school chain | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted no-school answer before Bedford NTA lookup | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted null without later datasets | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted placeholder [0] before ranking/counting | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted placeholder after unresolved query errors | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted placeholder answer before completing remaining hops | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted the county-seat year without verifying the required school-district establishment year | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted unable to determine before aggregating | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted_before_county_and_building_hops | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted_before_county_counts | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted_before_full_intersection | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted_before_required_total_was_computed | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted_before_violent_incidents_comparison | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted_empty_list_without_substantive_answer | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted_intermediate_lookup | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted_placeholder_before_ratio_resolved | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted_placeholder_before_totals_complete | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted_placeholder_without_required_counts | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted_unable_to_determine_before_required_analysis | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | submitted_unrelated_token_before_grounding_phd_answer | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | truncated_grep_sample_count | 1 | gpt-5-mini: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | unable to determine after blocker | 1 | gpt-5.4-nano: 1 |
| Incomplete evidence failures | incomplete_evidence_early_answer | unsupported final guess | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | (none) | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | added extra applied_force constraint | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | arrest hop used Rampart/Miscellaneous Other Violations instead of Central | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | arrest-stage chain divergence | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | avg_top_10_instead_of_yearwise_sum_top_5 | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | borough-fact-detour | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | broad city lookup and county-count detour instead of the required intersection/count steps | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | broad_search_detour | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | broader_capital_filter | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | charter-school SQL skipped the required Ward 5 and grades filter | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | checked ProgramYear/report-type presence instead of the authored county-count computation | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | collapsed required six-dataset chain; used 2009+2010 instead of 2010-only | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | consolidated_multi_year_aggregation | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | council-voting-record year hop replaced by APD search | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | county-count inspection instead of threshold computation | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | county_chain_drift | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | county_fips_vs_county_name_logic | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | cross-year_aggregation_repaired_to_year_only_query | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | cross_year_averaging_drift | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | detour from required county-link hop | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | deviated from required Chicago/Los Angeles comparison hop | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | distinct-employee 2021 count instead of row-count average | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | diverged from authored fixed top-five county set | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | diverged from the authored five-step chain by omitting ProgramYear and SiteCounty logic | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | diverged to Deb Haaland instead of Doug Burgum at the DOI hop | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | diverted from the required node-derived candidate set to a P.S. 020 Clinton Hill lookup | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | diverted to Smith County / Houston Rockets branch | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | employee_pay_top10_drift | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | exploratory_aggregation_and_schema_sampling | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | filters and grouping logic diverged from authored computation | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | first reimbursement query diverged from the authored decrease-comparison hop | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | hardcoded agency list instead of computing the intersection | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | hardcoded counties and wrong output shape for CV step | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | inspection_query_instead_of_county_math_aggregation | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | intermediate SQL scope mismatch | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | intermediate_sql_and_search_detour | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | introduced shooting-related descriptor path instead of fixed descriptor step | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | mismatched 2021 mental-health aggregation path instead of the authored 2015 OMH clinic step | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | mismatched fields/years in CACFP hop | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | mismatched query shape diverged from authored hop chain | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | missed_required_comparison_step | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | multi-county minimum query instead of authored single-county lookup | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | multi-dataset threshold intersection drift | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | non-equivalent county-count queries and placeholder intersection query | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | off-plan ward/offense path | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | pivoted from the Ward 7 result to a Vincent C. Gray chain and submitted 1743 instead of 1735 | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | placeholder SQL instead of real computation | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | placeholder schema probe instead of planned ranking aggregation | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | placeholder_first_hop_instead_of_ward_lookup | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | placeholder_sql | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | placeholder_sql_skipped_required_top7_intersection | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | probe/placeholder queries instead of county aggregation | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | ps_172_branch_divergence | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | raw-row ordering instead of grouped SUM branch aggregation | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | replaced the authored four-year district consistency hop with a county-level minimum query | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | row-count detour instead of county-level ranking | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | sampled_rows_instead_of_district_average | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | schema checks and row counts instead of required county-level aggregations and joins; SQL repair repeatedly failed with JSONDecodeError | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | schema-check detour | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | schema/parsing detour instead of required county-filtering hops | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | schema_discovery_detour | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | shifted to 2016/2021 intersection | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | single-year counts instead of required 2019-2021 chain | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | single-year county count instead of planned multi-year intersection | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | single-year county totals SQL omitted required multi-year low-income filter | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | skipped county-seat lookup and population comparison | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | skipped county-seat/statue lookup after filtering | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | skipped four-year intersection | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | skipped required Ward 1 offense lookup | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | skipped required city-in-county hop | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | skipped required intersection hop; chose Middlesex instead of Bergen | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | skipped upstream derivation hops | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | skipped yearly branch-intersection before lookup | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | skipped_four_year_intersection_and_final_filters | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | skipped_intersection_stage | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | skipped_required_intersection_step | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | started on 2012-2013 progress-report path instead of the authored performance-directory chain | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | started with one-year query; skipped planned elementary-school hop | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | stayed on contractor-ranking stage instead of later hops | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | stayed on school-level checks instead of neighborhood-to-namesake hop | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | stayed_on_first_hop | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | stuck in property-tax-roll branch instead of biography hop | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | substituted_wrong_interpreter_chain | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | switched from area/code count to boolean identity-theft existence check | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | switched the area-hop from the planned arrest dataset to the 2010-2019 crime dataset | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | switched to borough-geometry side path | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | switched_from_central_chain_to_rampart_lookup | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | switched_to_arrest_charge_path | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | trivial_schema_check_instead_of_required_aggregation | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | used 2012-13 top-3 DBNs for the 2011-12 A-grade check | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | used AREA NAME/Date Rptd instead of AREA=2/DATE OCC | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | used CAD sector hop instead of searches-by-type plan | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | used DIABETES_AdjPrev multi-year intersection instead of authored DIABETES_CrudePrev per-year path | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | used LAPD NIBRS path instead of the crime->arrest->RIPA chain | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | used Washington-filtered contractor queries instead of authored top-20 ranking hops | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | used a 2016-only query and dictionary lookup instead of the required 2016+2018 city-average chain | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | used a Whitman County ranking query instead of the Pullman School District lookup | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | used a county-wide PercentMetStandard average instead of the authored count-based county subset query | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | used age-adjusted prevalence plus population cutoff instead of crude-prevalence path | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | used crime-file cluster extraction instead of the neighborhoods-article bridge | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | used department-description and single-year queries instead of the authored department-number 2019-2021 intersection path | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | used per-county max aggregation instead of the required HSA>80 filter hop | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | used score ranking and name search instead of year-by-year intersection logic | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | used total admissions and an overbroad NYC exclusion instead of the authored Secure/Mixed Admissions > 90 and NYC-only filter | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | used wrong query shape for the first hop | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | used_ctt_class-size_path_instead_of_spec_ed | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | used_non_equivalent_single_year_check_as_proxy | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | widened 2019 filter | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | wrong Ward 5 branch | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | wrong county-ranking strategy | 1 | gpt-5-mini: 1 |
| Task/planning failures | planning_decomposition_mismatch | wrong first-hop grouping/filter in SQL | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | wrong first-hop source path | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | wrong initial dataset sequence | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | wrong year anchor | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | wrong_county_chain | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | wrong_first_hop_schema_and_missing_fy2007_ranking | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | planning_decomposition_mismatch | wrong_terminus_branch | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | added spurious ward filter on final 2020 count | 1 | gpt-5-mini: 1 |
| Task/planning failures | question_or_constraint_misread | aggregation_instruction_misread | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | answered_bachelors_degree_year_instead_of_university_founding_year | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | broadened the county set beyond the hop-2 counties | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | bronx-specific shooting denominator omitted | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | comparison_reversed | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | county-seat filter misread | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | dropped city constraint for private count | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | geography_scope_misread | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | missed_required_filters_and_aggregation | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | omitted ProgramYear filter and used generic top-N county count | 1 | gpt-5-mini: 1 |
| Task/planning failures | question_or_constraint_misread | omitted required GradeLevel='All Grades' filter | 1 | gpt-5-mini: 1 |
| Task/planning failures | question_or_constraint_misread | retained precinct 44 and OR on LOCATION_DESC | 1 | gpt-5-mini: 1 |
| Task/planning failures | question_or_constraint_misread | returned a person name instead of the required university answer | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | returned_body_name_instead_of_operating_agency | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | returned_triple_instead_of_single_answer | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | reversed ratio direction | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | single_year_only_filter | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | treated a Community School District 02 school as if it satisfied the Queens District 26 constraint | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | used OUTSIDE instead of INSIDE | 1 | gpt-5-mini: 1 |
| Task/planning failures | question_or_constraint_misread | used `Used Taser(s) = 1` instead of `Used Taser(s) > 0` | 1 | gpt-5-mini: 1 |
| Task/planning failures | question_or_constraint_misread | used all-four-year intersection instead of >=3-year threshold | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | used broad drug-keyword filter instead of exact Narcotic Drug Laws criterion | 1 | gpt-5-mini: 1 |
| Task/planning failures | question_or_constraint_misread | used department description and wrong top-K/year scope instead of department code/number sums | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | used offense-share percent change instead of incident-count percentage | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | used top-5 instead of top-2 | 1 | gpt-5-mini: 1 |
| Task/planning failures | question_or_constraint_misread | wrong Interior secretary branch (Deb Haaland instead of Doug Burgum) | 1 | gpt-5-mini: 1 |
| Task/planning failures | question_or_constraint_misread | wrong answer format | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | wrong county-town branch (Bury St Edmunds instead of Ipswich) | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | wrong geographic scope | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | wrong geographic scope; statewide county aggregation | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | wrong namesake and birth year | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | wrong terminus city pair and prevalence definition | 1 | gpt-5-mini: 1 |
| Task/planning failures | question_or_constraint_misread | wrong_answer_format_tuple_instead_of_single_answer | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | wrong_metric_and_time_window | 1 | gpt-5.4-nano: 1 |
| Task/planning failures | question_or_constraint_misread | year window and county aggregation mismatch | 1 | gpt-5.4-nano: 1 |
| Tool blocker failures | tool_or_data_blocker | file_not_found | 1 | gpt-5.4-nano: 1 |
| Tool blocker failures | tool_or_data_blocker | missing_county_mapping_and_formation_year_data | 1 | gpt-5.4-nano: 1 |
| Tool blocker failures | tool_or_data_blocker | missing_or_malformed_log | 1 | gpt-5-mini: 1 |
| Tool blocker failures | tool_or_data_blocker | no_matching_rows_for_requested_filter | 1 | gpt-5.4-nano: 1 |
| Tool blocker failures | tool_or_data_blocker | schema_mismatch_or_wrong_file | 1 | gpt-5-mini: 1 |
| Tool blocker failures | tool_or_data_blocker | submitted_placeholder_answer | 1 | gpt-5.4-nano: 1 |
| Tool blocker failures | tool_or_data_blocker | unsupported_kml_xml_source | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | low_yield_search_loop | (none) | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | low_yield_search_loop | county-resolution population/adjacency search stalled | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | low_yield_search_loop | dataset discovery loop | 1 | gpt-5-mini: 1 |
| Turn-waste failures | low_yield_search_loop | empty-result repeat on binge-drinking slice | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | low_yield_search_loop | irrelevant dataset drift in school-district search | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | low_yield_search_loop | kept re-searching after source set was already identified | 1 | gpt-5-mini: 1 |
| Turn-waste failures | low_yield_search_loop | repeated broad searches without anchoring county pair | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | low_yield_search_loop | repeated dataset searches for a more explicit county/community-college dataset without new evidence | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | low_yield_search_loop | repeated employer/namesake source discovery yielded no verified fact chain | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | low_yield_search_loop | repeated generic searches returned no dataset | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | low_yield_search_loop | repeated search loop on school-district data | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | low_yield_search_loop | repeated searches returned unrelated datasets instead of the identified-student source | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | low_yield_search_loop | repeated zero-match Brightwood field probes | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | low_yield_search_loop | repeated_search_calls | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | low_yield_search_loop | repeated_searches_found_no_2020_source | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | low_yield_search_loop | repeated_searches_no_new_evidence | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | low_yield_search_loop | zero_row_sql_loop | 1 | gpt-5-mini: 1 |
| Turn-waste failures | query_execution_error_loop | JSON repair retry loop | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | SQL repair JSONDecodeError blocked VADIR computation | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | SQL_repair_JSONDecodeError | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | binder error from flat WARD reference | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | binder error: missing ProgramYear | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | binder_error_missing_year_column | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | code repair failure | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | duckdb UNNEST binder error during aggregation | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | empty_recovery_search_and_bad_sandbox_path | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | execute_ideal repair JSONDecodeError | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | flat_sql_and_parser_mismatch_on_nested_json | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | invalid GeoJSON field path | 1 | gpt-5-mini: 1 |
| Turn-waste failures | query_execution_error_loop | json_decode_error_repair_failure | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | json_repair_parse_failure | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | jsondecode_error_in_sql_repair | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | jsondecodeerror_during_repair_loop | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | malformed_json_extraction_attempt | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | non_equivalent_sql_and_jsondecodeerror | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | placeholder code and generic COUNT(*) query rejected | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | placeholder queries plus SQL repair JSONDecodeError | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | placeholder_sql_then_nonmatching_schema_query | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | repair_cycle | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | repeated DuckDB SQL repair JSONDecodeError | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | repeated JSONDecodeError in query_ideal repair | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | repeated JSONDecodeError in repair | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | repeated WARD SQL binder errors | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | repeated binder errors on GeoJSON SQL | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | repeated execution-tool cancellations and repair failures | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | repeated malformed JSON/GeoJSON and download tool calls blocked the exact aggregations | 1 | gpt-5-mini: 1 |
| Turn-waste failures | query_execution_error_loop | repeated missing-column repair queries against incompatible dictionary schema | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | repeated progress-grade column binder errors | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | repeated sql repair JSONDecodeError | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | repeated sql/json parse repair failures | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | repeated_jsondecode_repair | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | repeated_jsondecodeerror_in_sql_repair | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | repeated_jsondecodeerror_repairs | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | repeated_sql_repair_jsondecode_error | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | repeated_sql_repair_jsondecodeerror | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | schema/column mismatch repair loop | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | semantic no-match and JSONDecodeError repair failures | 1 | gpt-5-mini: 1 |
| Turn-waste failures | query_execution_error_loop | semantic_match_repair_failure | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | sql repair JSONDecodeError | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | sql_binder_error | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | query_execution_error_loop | sql_binder_errors | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | same_hop_repetition | conflicting peak-year recomputation | 1 | gpt-5-mini: 1 |
| Turn-waste failures | same_hop_repetition | police_title_and_title_distribution_loop | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | same_hop_repetition | programyear_inspection_loop | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | same_hop_repetition | repeated single-year county low-income percent query without required GradeLevel and 32-40% filters | 1 | gpt-5-mini: 1 |
| Turn-waste failures | same_hop_repetition | repeated ward grep extraction | 1 | gpt-5-mini: 1 |
| Turn-waste failures | schema_or_shape_inspection_loop | LIMIT 5 schema probe replaced district filtering | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | schema_or_shape_inspection_loop | csv_queryability_and_schema_probe | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | schema_or_shape_inspection_loop | generic schema probe instead of count query sequence | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | schema_or_shape_inspection_loop | metadata-backed schema inspection | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | schema_or_shape_inspection_loop | off_target_sql | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | schema_or_shape_inspection_loop | repeated inspect calls stalled extraction | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | schema_or_shape_inspection_loop | repeated inspection/count queries instead of filters | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | schema_or_shape_inspection_loop | repeated metadata/publisher-view peeks instead of row tables | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | schema_or_shape_inspection_loop | repeated sample-row/schema probing on bridge dataset | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | schema_or_shape_inspection_loop | repeated schema probing on fire-department dataset | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | schema_or_shape_inspection_loop | repeated schema/count probes on 2010-2011 file | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | schema_or_shape_inspection_loop | repeated schema/shape probing on nested school datasets | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | schema_or_shape_inspection_loop | sample-row/schema inspection instead of year-specific class-size filter | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | schema_or_shape_inspection_loop | sample_row_probe | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | schema_or_shape_inspection_loop | schema checks delayed evidence extraction | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | schema_or_shape_inspection_loop | schema probe instead of ranking computation | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | schema_or_shape_inspection_loop | schema probe returned no usable rows | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | schema_or_shape_inspection_loop | schema/sample inspection and binder repair loop | 1 | gpt-5.4-nano: 1 |
| Turn-waste failures | schema_or_shape_inspection_loop | wrong column/schema | 1 | gpt-5-mini: 1 |
| Wrong source target failures | wrong_source_or_dataset | 500-Cities release/version confusion | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | 500-cities_vs_city-page | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | Wikipedia fallback | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | alternate current dataset variants instead of historical source set | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | ambiguous_dataset_id | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | apd-use-of-force instead of apd-searches-by-type | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | apd-use-of-force instead of required APD searches source | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | bridge dataset used for violent-crime and founding-year evidence | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | broad_searches_returned_unrelated_datasets | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | catalog metadata file instead of underlying row dataset | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | catalog_metadata_instead_of_row_data | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | city-population lookup used instead of the task's county-level answer path | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | complaint data only through 2019 | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | county FIPS/geography mismatch | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | county pages instead of city pages | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | county-population dataset | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | current_vs_planned_source_version_mismatch | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | dataset_id_mismatch | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | dataset_id_not_found_or_ambiguous | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | dataset_version_mismatch | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | different dataset/year/schema | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | district_source_mismatch | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | drifted to an unrelated employee-overtime dataset while searching for binge-drinking data | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | file_format_mismatch | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | historic_through_2019 | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | irrelevant_or_new_york_based_datasets | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | late WSIF drift | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | metadata-json instead of rows table | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | metadata/page-shell/catalog files instead of underlying overtime rows | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | metadata_catalog_instead_of_table | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | metadata_descriptor_artifacts_instead_of_row_files | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | metadata_file_used_instead_of_rows_file | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | missing_expected_state_column | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | missing_neighborhood_field | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | mixed_arrest_and_crime_sources | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | mixed_dataset_on_third_hop | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | obesity filters and schema assumptions yielded zero rows in the 2016 500 Cities release, so the opening hop had no city value | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | off-task dataset detour | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | older_school_dataset_version | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | omitted neighborhood source needed to ground Columbia Heights | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | opened metadata JSON instead of rows file | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | pharmacy_snapshot_instead_of_state_drug_utilization | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | pivoted to neighborhoods page instead of university/birth-year sources | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | pivoted_to_2010_2016_school_safety_report | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | private_school_step_drifted_to_postsecondary_dataset | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | publisher-view JSON instead of tabular rows | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | searched_missing_ye_2019_dataset | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | selected a release file that did not contain the needed year rows | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | selected budget-recommendations datasets instead of the ordinance-appropriations branch | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | single-source selection instead of the required multi-dataset chain | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | stayed_on_use_of_force_dataset | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | switched to 2018-2019 school-locations / P.S. 254 instead of Bedford NTA check | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | unrelated_search_hits | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | used 2022-23 source instead of current source | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | used CAD incidents instead of apd-use-of-force | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | used current postsecondary dataset for county lookup | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | used metadata/catalog file instead of queryable office table | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | used only the annual crime datasets and missed the neighborhood source | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | used postsecondary dataset for district offices | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | used school-neighborhood-poverty-estimates instead of the intended school-locations source | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | used the 2019-20 postsecondary dataset instead of the task-specified Polk County postsecondary count | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | used the jail-population dataset for the violent-crime comparison and mapped census values into the wrong metric | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | used_2012_2018_proxy_instead_of_2020_source | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | used_2013_2014_directory_instead_of_required_progress_reports | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | used_combined_current_year_file_instead_of_year_specific_datasets | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | used_current_private_school_dataset_instead_of_authored_version | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | used_namesake_biography_instead_of_university_history | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | violent-crime lookup drifted to the wrong dataset/schema and county target | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | wiki_page_instead_of_salary_dataset | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | wrong dataset family | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | wrong dataset family (NYC DOE report instead of DC charter-school data) | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | wrong_dataset_for_aggregation | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | wrong_dataset_version | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | wrong_file_read | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | wrong_filter_or_scope_missing_city_restriction | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | wrong_source_or_scope | 1 | gpt-5.4-nano: 1 |
| Wrong source target failures | wrong_source_or_dataset | wsif_and_single_year_assessment | 1 | gpt-5.4-nano: 1 |

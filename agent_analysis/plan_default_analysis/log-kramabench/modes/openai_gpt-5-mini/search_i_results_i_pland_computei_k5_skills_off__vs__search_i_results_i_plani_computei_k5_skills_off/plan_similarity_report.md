# Plan Similarity Report: openai_gpt-5-mini

- Log root: `log-kramabench`
- Model variant: `openai_gpt-5-mini`
- Runner model: `gpt-5-mini`
- Plan D mode: `search_i_results_i_pland_computei_k5_skills_off`
- Plan I mode: `search_i_results_i_plani_computei_k5_skills_off`
- Rows: 83

## Counts by plan_similarity
- `similar`: 43
- `not_comparable`: 28
- `operation_mismatch`: 9
- `missing_details`: 3

## Missing-plan rates
- `none`: 55
- `missing_plan_d`: 19
- `missing_plan_i`: 7
- `missing_both`: 2

## Divergence types
- `missing_plan_d`: 19
- `missing_plan_i`: 7
- `missing_both`: 2
- `bibliography_normalization_detail`: 1
- `beach_name_normalization_missing`: 1
- `aggregate_count_vs_average_annual_rate`: 1
- `interval_denominator_mismatch`: 1
- `conflict_window_definition_mismatch`: 1
- `hardcoded_party_mapping_vs_vote_file`: 1
- `monthly_stacked_vs_summer_total_correlation`: 1
- `cycle_period_extrema_mismatch`: 1
- `day_of_year_vs_month_trend_and_significance`: 1
- `missing_logscale_conversion`: 1
- `missing_identity_theft_category_share`: 1
- `included_case_filter_missing`: 1

## Notes
- Judgments compare only explicit `plan(...)` and `plan_ideal(...)` text, not later execution success or final answers.
- Missing explicit plans are copied as mechanical `not_comparable` rows from the helper output.
- Default plans are allowed to be less specific; harmless source-discovery or column-name abstraction is marked `similar`.

# Plan Similarity Report: openai_gpt-5-mini

- Log root: `log-kramabench`
- Model variant: `openai_gpt-5-mini`
- Runner model: `gpt-5-mini`
- Plan D mode: `search_d_results_i_pland_k5_skills_off`
- Plan I mode: `search_i_results_i_plani_computei_k5_skills_off`
- Rows: 83

## Counts by plan_similarity
- `not_comparable`: 65
- `similar`: 13
- `operation_mismatch`: 4
- `missing_details`: 1

## Missing-plan rates
- `missing_plan_d`: 56
- `none`: 18
- `missing_both`: 9

## Divergence types
- `missing_plan_d`: 56
- `missing_both`: 9
- `beach_name_normalization_missing`: 1
- `interval_denominator_mismatch`: 1
- `monthly_stacked_vs_summer_total_correlation`: 1
- `cycle_period_extrema_mismatch`: 1
- `endpoint_average_vs_span_average`: 1

## Notes
- Judgments compare only explicit `plan(...)` and `plan_ideal(...)` text, not later execution success or final answers.
- Missing explicit plans are copied as mechanical `not_comparable` rows from the helper output.
- Default plans are allowed to be less specific; harmless source-discovery or column-name abstraction is marked `similar`.

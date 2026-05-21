# Plan Default Similarity: openai_gpt-5.4-nano

- log root: `log-kramabench`
- model_variant: `openai_gpt-5.4-nano`
- runner_model: `gpt-5.4-nano`
- plan_d_mode: `search_i_results_i_pland_computei_k5_skills_off`
- plan_i_mode: `search_i_results_i_plani_computei_k5_skills_off`
- rows: 83

## Counts by plan_similarity
- `similar`: 70
- `operation_mismatch`: 10
- `incomplete_plan`: 1
- `missing_details`: 1
- `not_comparable`: 1

## Missing-plan counts
- `none`: 82
- `missing_plan_d`: 1

## Divergence counts
- `source_parsing_mismatch`: 1
- `missing_state_vs_national_msa_comparison`: 1
- `missing_human_lightning_combination`: 1
- `aggregate_rate_vs_yearly_average`: 1
- `interval_denominator_mismatch`: 1
- `conflict_counting_granularity_mismatch`: 1
- `population_value_vs_population_rank`: 1
- `wrong_denominator_total_reports`: 1
- `missing_plan_d`: 1
- `monthly_stacked_vs_summer_total_correlation`: 1
- `cycle_period_extrema_mismatch`: 1
- `endpoint_average_vs_span_average`: 1
- `missing_logscale_conversion`: 1

## Notes
- Judgments compare only explicit `plan(...)` vs `plan_ideal(...)` text.
- `not_comparable` rows are mechanical prefill rows from missing explicit planning calls.
- Kramabench default plans often differ only by discovery/tool naming; those are marked `similar` when the source family, computation, and final target remain answer-preserving.

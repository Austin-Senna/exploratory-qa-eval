# Plan Default Similarity: openai_gpt-5.4-nano

- log root: `log-kramabench`
- model_variant: `openai_gpt-5.4-nano`
- runner_model: `gpt-5.4-nano`
- plan_d_mode: `search_d_results_i_pland_k5_skills_off`
- plan_i_mode: `search_i_results_i_plani_computei_k5_skills_off`
- rows: 83

## Counts by plan_similarity
- `similar`: 41
- `not_comparable`: 37
- `operation_mismatch`: 4
- `missing_details`: 1

## Missing-plan counts
- `none`: 46
- `missing_plan_d`: 37

## Divergence counts
- `missing_plan_d`: 37
- `missing_human_lightning_combination`: 1
- `aggregate_rate_vs_yearly_average`: 1
- `population_value_vs_population_rank`: 1
- `wrong_denominator_total_reports`: 1
- `monthly_stacked_vs_summer_total_correlation`: 1

## Notes
- Judgments compare only explicit `plan(...)` vs `plan_ideal(...)` text.
- `not_comparable` rows are mechanical prefill rows from missing explicit planning calls.
- Kramabench default plans often differ only by discovery/tool naming; those are marked `similar` when the source family, computation, and final target remain answer-preserving.

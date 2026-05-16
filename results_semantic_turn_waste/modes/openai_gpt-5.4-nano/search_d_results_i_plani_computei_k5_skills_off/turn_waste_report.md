# Turn Waste Report

- Source file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/eval_results.csv`
- Mirrored eval file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_turn_waste/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/eval_results.csv`
- Audited row count: 1
- Total estimated wasted turns: 7
- Average estimated wasted turns: 7.0
- Deterministic validation: 1 valid, 0 invalid
- Model validation: 1 pass, 0 repaired_pass, 0 untrusted

## Discovered File-Local Groups

### Repeated Dataset Probing After Useful Retrieval
- Count: 1
- Estimated wasted turns: 7
- Description: The run spent its wasted turns re-querying and grepping the already-located population dataset instead of advancing to the next required lookup.
- Distinguishing signals: repeated query_ideal calls against the same population dataset after no authored match; repeated grep_file regex attempts over the same file; useful county rows had already been retrieved; hard timeout occurred before the school-enrollment step.
- Representative task ids: tasks_mini/k-4-d-2/task_15.json

## Global Summary

One accepted failed row was grouped. Its wasted-turn pattern was repeated probing of a located population dataset after partial progress, exhausting the budget before the city/enrollment lookup.

## Global Findings

- The main waste was staying too long on an already-identified source, not broad exploration.
- The run had meaningful progress by locating the Washington population dataset and target county rows.
- The final failure point was an over-specific Clark County grep that ran until hard timeout.

## Unresolved Or Mixed Cases

- None. The audited row passed deterministic validation and model validation.

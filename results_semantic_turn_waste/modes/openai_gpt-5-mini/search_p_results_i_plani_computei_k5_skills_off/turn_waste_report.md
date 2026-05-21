# Turn Waste Report

Source file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/eval_results.csv`
Output file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_turn_waste/modes/openai_gpt-5-mini/search_p_results_i_plani_computei_k5_skills_off/eval_results.csv`

## Summary

- Audited runtime-failure rows: 4
- Accepted model-validated rows: 4
- Total estimated wasted turns: 27
- Average estimated wasted turns: 6.75
- Global summary: All accepted rows are hard timeout failures where the agent had a plausible path but spent the tail budget on repeated or over-broad data access work.

## Discovered File-Local Groups

### `repeated_dataset_diagnostics` (2 rows, 18 wasted turns)

Runs burned the remaining budget on repeated schema/sample/count/grep/query attempts against a difficult dataset after the next hop depended on extracting one specific value or comparison.

Representative task ids: tasks_mini/k-5-d-4/task_2.json, tasks_mini/k-6-d-2/task_4.json

Distinguishing signals:
- near-duplicate queries against the same dataset
- schema/sample/count diagnostics repeated after empty or mismatched results
- timeout before downstream hops or final calculation

### `late_broad_probe_after_progress` (2 rows, 9 wasted turns)

Runs made substantial progress but spent late turns on broad or low-yield discovery/probing instead of executing the narrowed final computation and submission path.

Representative task ids: tasks_mini/k-3-d-3/task_6.json, tasks_mini/k-4-d-4/task_6.json

Distinguishing signals:
- correct or likely intermediate target already identified
- late broad sanity/sample/discovery queries
- timeout immediately before final averaging, lookup, or submission

## Row Assignments

- `tasks_mini/k-3-d-3/task_6.json` -> `late_broad_probe_after_progress`; wasted turns: 5. After obtaining parking lists and moving counts, it lost budget to redundant list debugging and a low-yield agency-name discovery query before final averaging/operator lookup.
- `tasks_mini/k-4-d-4/task_6.json` -> `late_broad_probe_after_progress`; wasted turns: 4. After release totals made Dallas the likely target, final turns used broad VA disability probes and duplicate aggregation attempts instead of Dallas-specific 2020/2023 recipient values.
- `tasks_mini/k-5-d-4/task_2.json` -> `repeated_dataset_diagnostics`; wasted turns: 9. The run repeatedly reformulated 500 Cities binge-drinking lookups and greps after empty or mismatched results, exhausting budget before the overtime hop.
- `tasks_mini/k-6-d-2/task_4.json` -> `repeated_dataset_diagnostics`; wasted turns: 9. The run stayed stuck on repeated 500 Cities obesity diagnostics and repaired queries, never reaching downstream corporation, founder, city, or budget hops.

## Findings

- The strongest shared pattern is failure to switch from exploration to targeted computation before timeout.
- 500 Cities lookups produced the highest wasted-turn estimates because repeated empty or mismatched results triggered multiple diagnostic loops.
- Late-stage broad probes were costly when only a final aggregation, lookup, or submission remained.

## Unresolved Or Mixed Cases

- None. All audited rows passed deterministic validation and model validation.

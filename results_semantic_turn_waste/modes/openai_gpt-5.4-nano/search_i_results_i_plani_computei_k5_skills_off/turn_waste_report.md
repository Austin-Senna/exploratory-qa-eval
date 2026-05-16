# Turn Waste Report

- Source file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic/modes/openai_gpt-5.4-nano/search_i_results_i_plani_computei_k5_skills_off/eval_results.csv`
- Mirrored eval file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_turn_waste/modes/openai_gpt-5.4-nano/search_i_results_i_plani_computei_k5_skills_off/eval_results.csv`
- Audited row count: 13
- Trusted grouped rows: 13
- Total estimated wasted turns: 138
- Average estimated wasted turns: 10.6
- Deterministic validation: 13 valid, 0 valid_with_warnings, 0 invalid, 0 missing_log
- Model validation: 8 pass, 5 repaired_pass, 0 invalid_untrusted

## Discovered File-Local Groups

### Duplicate quantitative reruns
- Count: 7
- Estimated wasted turns: 81
- Description: Runs repeatedly reissued count, ranking, average, or top-N queries after enough quantitative evidence was already available, delaying later hops.
- Distinguishing signals: near-duplicate query_ideal aggregations; same datasets, years, agencies, wards, schools, or metrics rechecked; later non-aggregate lookup steps were not reached before tool limit
- Representative task ids: tasks_mini/k-4-d-3/task_12.json; tasks_mini/k-4-d-3/task_2.json; tasks_mini/k-5-d-3/task_10.json; tasks_mini/k-5-d-3/task_9.json; tasks_mini/k-6-d-3/task_1.json

### Candidate confirmation loops
- Count: 4
- Estimated wasted turns: 33
- Description: Runs had narrowed to plausible candidates but spent the remaining budget confirming names, mappings, filters, or component counts instead of executing the final lookup chain.
- Distinguishing signals: candidate set already visible; repeated narrowing or name/mapping checks; final birthplace, founding-year, department-head, or component-count step was skipped or unsupported
- Representative task ids: tasks_mini/k-4-d-2/task_10.json; tasks_mini/k-4-d-3/task_6.json; tasks_mini/k-4-d-4/task_3.json; tasks_mini/k-4-d-5/task_4.json

### Low-yield repair detours
- Count: 2
- Estimated wasted turns: 24
- Description: Runs burned calls on broad reruns, format repairs, empty schema probes, or mis-targeted diagnostics after the main path should have shifted to final targeted queries.
- Distinguishing signals: XML/JSON handling or query repair loops; empty or mis-targeted schema/value probes; broad reruns consumed budget needed for final specific computation
- Representative task ids: tasks_mini/k-4-d-4/task_10.json; tasks_mini/k-5-d-4/task_3.json

## Global Summary

Most failures were caused by repeatedly re-querying already useful intermediate evidence, especially quantitative rankings or candidate confirmations, until the tool limit blocked downstream lookup steps.

## Global Findings

- Duplicate quantitative reruns are the dominant local pattern, covering 7 of 13 rows.
- Several runs had already narrowed the candidate set but spent final calls confirming intermediate candidates rather than performing final entity lookups.
- A smaller pattern involved low-yield repair or schema detours that consumed the budget before final targeted queries.
- Across groups, the common failure mode was not absence of an initial path but failure to stop querying an intermediate hop once it was good enough.

## Unresolved Or Mixed Cases

- None. All audited rows passed deterministic validation and model validation after conservative repairs where needed.

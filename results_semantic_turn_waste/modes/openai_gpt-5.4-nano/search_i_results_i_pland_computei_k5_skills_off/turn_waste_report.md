# Turn Waste Report

- Source file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic/modes/openai_gpt-5.4-nano/search_i_results_i_pland_computei_k5_skills_off/eval_results.csv`
- Mirrored eval file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_turn_waste/modes/openai_gpt-5.4-nano/search_i_results_i_pland_computei_k5_skills_off/eval_results.csv`
- Audited row count: 4
- Total estimated wasted turns: 48
- Average estimated wasted turns: 12.0
- Deterministic validation: 4 valid, 0 invalid
- Model validation: 3 pass, 1 repaired_pass, 0 untrusted

## Discovered File-Local Groups

### Upstream rework crowded out downstream completion
- Count: 3
- Estimated wasted turns: 44
- Description: Runs made a meaningful upstream discovery, then spent the remaining budget repeating or repairing earlier-hop work instead of advancing to the later required counts or lookups.
- Distinguishing signals: A usable intermediate answer was already found or nearly settled; Later turns repeated schema checks, count queries, parsing, or candidate-selection work around the same upstream target; The final required hops or terminal counts were not completed before timeout or tool exhaustion
- Representative task ids: tasks_mini/k-4-d-2/task_7.json; tasks_mini/k-4-d-4/task_10.json; tasks_mini/k-5-d-3/task_5.json

### Blocked query path retry loop
- Count: 1
- Estimated wasted turns: 4
- Description: The run discovered that its chosen ideal-query route could not handle the target file, but continued spending turns on failed or placeholder ideal computations instead of switching to a workable data-reduction path.
- Distinguishing signals: The tool path was visibly failing or unsupported; Repeated execute_ideal/query_ideal attempts stayed close to the same blocked approach; The run did not reach a usable subset, alternative workflow, or final count
- Representative task ids: tasks_mini/k-4-d-1/task_3.json

## Global Summary
Across the accepted summaries, wasted turns mostly came from staying on an already-solved or already-blocked intermediate step. Three of four rows show upstream rework crowding out downstream completion; one row shows a blocked large-file ideal-query path being retried instead of replaced.

## Global Findings
- The dominant local pattern is failure to transition from intermediate evidence to the next required hop.
- Repeated count/query reformulations were especially costly when the run already had enough information to advance.
- The most distinct outlier is the large-file case, where the wasted tail was persistence with a visibly unsupported execution path.
- Estimated wasted turns are concentrated in the upstream-rework group: 44 of 48 total estimated wasted turns.

## Unresolved Or Mixed Cases
- None. All audited rows passed deterministic validation and model validation after one conservative repair.

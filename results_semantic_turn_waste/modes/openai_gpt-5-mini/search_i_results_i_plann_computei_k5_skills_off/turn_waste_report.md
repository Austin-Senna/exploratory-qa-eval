# Turn Waste Report

Source file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off/eval_results.csv`
Output directory: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_turn_waste/modes/openai_gpt-5-mini/search_i_results_i_plann_computei_k5_skills_off`

## Summary

- Audited failed rows: 10
- Deterministic validation: 10 valid, 0 valid_with_warnings, 0 invalid, 0 missing_log
- Model validation: 10 pass, 0 repaired_pass, 0 invalid_untrusted
- Total estimated wasted turns: 93
- Average estimated wasted turns per audited row: 9.3

## Discovered File-Local Groups

### Repeated final-source search

- Count: 4
- Estimated wasted turns: 42 total, 10.5 average
- Description: Runs made substantial progress, then spent the tail reformulating near-duplicate searches for a missing final source or fact until tool/turn exhaustion.
- Representative task ids: tasks_mini/k-4-d-3/task_7.json, tasks_mini/k-4-d-2/task_1.json, tasks_mini/k-4-d-3/task_6.json
- Signals: Multiple late search_ideal calls with similar terms; Earlier task components were already located or computed; Stop condition occurred before switching strategy or submitting a best-effort answer

### Dataset extraction thrash

- Count: 2
- Estimated wasted turns: 25 total, 12.5 average
- Description: Runs had relevant datasets in hand but lost time on repeated, failing, or overly broad extraction attempts instead of completing a clean computation.
- Representative task ids: tasks_mini/k-5-d-1/task_4.json, tasks_mini/k-3-d-4/task_4.json
- Signals: Repeated query_ideal, grep_file, read_file, or execute workarounds against located datasets; Tool errors or mismatched query shapes recur; Progress stopped at extracting a count or filtered subset from structured data

### Answer-path overchecking

- Count: 3
- Estimated wasted turns: 25 total, 8.3 average
- Description: Runs reached a strong candidate, ranking, or answer-bearing result, then spent remaining turns rechecking criteria or recomputing nearby results rather than finishing the final step and submitting.
- Representative task ids: tasks_mini/k-4-d-3/task_10.json, tasks_mini/k-5-d-2/task_5.json, tasks_mini/k-6-d-3/task_4.json
- Signals: Late turns repeat already explored filters or rankings; A useful candidate set or answer-bearing value appears before the wasted range; Failure comes from not moving to the final lookup or submit action

### Runtime crash after early query failure

- Count: 1
- Estimated wasted turns: 1 total, 1.0 average
- Description: The run ended because of an event-loop ReadError after only a short trace, with little observable repeated turn waste.
- Representative task ids: tasks_mini/k-4-d-4/task_9.json
- Signals: EventLoopException or ReadError is the actual stop condition; Only one low-yield retry is visible before the crash; No extended budget-draining tail exists

## Global Findings

Across 10 accepted rows, the dominant local pattern is late-stage stagnation after partial success: four rows repeatedly searched for a missing final source, three rows overchecked or recomputed after an answer path was clear, two rows thrashed on extracting data from located datasets, and one row was mainly a runtime crash with minimal observable waste.

- Most wasted turns occurred after the run had already found major intermediate evidence, not at initial discovery.
- Repeated search_ideal reformulations are the most common visible tail behavior, especially for final facts outside the already-located datasets.
- Structured-data failures often came from changing query shapes or falling back to grep/read instead of simplifying the computation around known schemas.
- Several runs failed to submit after receiving answer-bearing or strong candidate results, suggesting final-step discipline was a larger issue than pure data availability.
- The event-loop row should be treated separately from budget-waste rows because the crash, not sustained repeated behavior, caused the failure.

## Accepted Rows

- `tasks_mini/k-4-d-3/task_10.json`: Answer-path overchecking | wasted turns `13` | Found the relevant detention, jail, STAR, and violent-crime datasets, but never moved from Erie/Monroe violent-crime ranking to county-seat incorporation before timeout.
- `tasks_mini/k-5-d-2/task_5.json`: Answer-path overchecking | wasted turns `10` | Found the fatality-filtered counties and later the 2021 model-based top-two subset, but timed out before submitting the bay answer.
- `tasks_mini/k-6-d-3/task_4.json`: Answer-path overchecking | wasted turns `2` | The agent found the ACT/Iowa path, gathered the needed school datasets, reached an answer-bearing postsecondary count, but did not submit before timeout.
- `tasks_mini/k-5-d-1/task_4.json`: Dataset extraction thrash | wasted turns `15` | Found the main NYPD datasets and schemas, but never completed the stepwise computation before timeout.
- `tasks_mini/k-3-d-4/task_4.json`: Dataset extraction thrash | wasted turns `10` | The agent found the relevant school-location datasets and obtained public, private, and district-office counts, but never cleanly extracted the needed postsecondary count before timeout.
- `tasks_mini/k-4-d-3/task_7.json`: Repeated final-source search | wasted turns `18` | Searched for DC street-sweeping schedules, found charter-school data, inspected Ward 2 school records, but never resolved the Ward 2 vs Ward 5 sweeping comparison.
- `tasks_mini/k-4-d-2/task_1.json`: Repeated final-source search | wasted turns `10` | Located the progress-report, grade, and school-location facts, then stalled on the final demographic source.
- `tasks_mini/k-4-d-3/task_6.json`: Repeated final-source search | wasted turns `8` | Computed budget/salary evidence for Chicago departments, then repeatedly searched for DFSS first-head history and timed out before submitting.
- `tasks_mini/k-4-d-4/task_4.json`: Repeated final-source search | wasted turns `6` | Found the health and overtime evidence and reached the Chicago Police salary step, then timed out without submitting.
- `tasks_mini/k-4-d-4/task_9.json`: Runtime crash after early query failure | wasted turns `1` | Found the relevant Washington enrollment and assessment datasets, inspected schemas, then crashed before reaching census or college-location work.

## Unresolved Or Mixed Cases

- None. All audited rows passed deterministic and model validation. The event-loop row is grouped separately because its visible waste was minimal and the crash was the primary stop condition.

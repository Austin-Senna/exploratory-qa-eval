# Turn Waste Report

- Source file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results-ec2_semantic/modes/openai_gpt-5.2-xhigh/search_d_results_i_plani_k5/eval_results.csv`
- Audited row count: 30
- Total estimated wasted turns: 69
- Average estimated wasted turns: 2.30

## Global Summary

Across this file, the dominant waste pattern is short terminal overshoot: many runs had already found the needed source path or candidate answer and then spent only one last turn on a support query that timed out or hit the tool cap. The next most common patterns are recovery loops after large-file or parsing failures and a smaller set of genuine search-drift cases where the agent kept broadening or rephrasing the same clue family instead of converging.

## Discovered Local Groups

### Final-Query Overshoots (13)

The solve path was already mostly complete, but the run spent its tail on one last validation/search/peek turn that then timed out, hit the tool cap, or crashed before submit.

- Distinguishing signals: answer path already clear; last turn is a single supporting query or file peek; stop condition occurs immediately after the extra turn
- Representative task ids: tasks_mini/k-2-d-3/task_2.json, tasks_mini/k-2-d-3/task_9.json, tasks_mini/k-2-d-4/task_1.json

### No Clear Wasted Tail (5)

The log ends in a max-token or stop condition without enough visible repetition to confidently call a wasted-turn loop.

- Distinguishing signals: max-tokens crash; no sustained repetition; waste estimate is zero or near-zero
- Representative task ids: tasks_mini/k-3-d-3/task_1.json, tasks_mini/k-3-d-3/task_3.json, tasks_mini/k-3-d-4/task_7.json

### Large-File Recovery Loops (3)

An oversized or malformed data query triggered recovery behavior, followed by repeated searches and peeks in the same dataset family instead of converging.

- Distinguishing signals: initial query error on a large CSV or JSON; repeat search/list/peek over the same source set; tail spent rediscovering the same dataset family
- Representative task ids: tasks_mini/k-2-d-3/task_6.json, tasks_mini/k-2-d-4/task_2.json, tasks_mini/k-2-d-4/task_4.json

### Adjacent Program Expansion (2)

County-level meal and reimbursement searches kept expanding into neighboring Texas education datasets instead of closing the comparison.

- Distinguishing signals: same county comparison; repeated reimbursement or lunch searches; pivot to child-center discovery before answering
- Representative task ids: tasks_mini/k-3-d-3/task_2.json, tasks_mini/k-3-d-4/task_10.json

### Broad Texas Education Drift (2)

The agent broadened Texas school-dataset searches and reset the plan instead of locking onto the district-level lookup once the county-seat path was known.

- Distinguishing signals: Texas school-dataset broadening; identified-student-percentage search family; plan reset or replan loop
- Representative task ids: tasks_mini/k-5-d-3/task_4.json, tasks_mini/k-5-d-3/task_5.json

### School Location Churn (2)

Repeated school-progress and school-location or neighborhood lookups continued after the key school was identified, producing little forward progress.

- Distinguishing signals: school-progress reports already narrowed the candidate; alternates between location and neighborhood pages; reformulates the same clue family
- Representative task ids: tasks_mini/k-3-d-3/task_10.json, tasks_mini/k-3-d-3/task_4.json

### Texas County Detour (2)

After the main comparison was available, the run drifted into a repeated Texas original-counties search loop with small wording changes.

- Distinguishing signals: post-solve detour; rephrased historical county search; no new source family introduced
- Representative task ids: tasks_mini/k-3-d-4/task_9.json, tasks_mini/k-4-d-3/task_5.json

### APD Count Refinement (1)

The run kept re-querying the same APD use-of-force filters after the needed count was already close, with little new information gained.

- Distinguishing signals: same APD dataset; near-identical filters; repeated count refinement
- Representative task ids: tasks_mini/k-3-d-1/task_1.json

## Global Findings

- Most rows have low wasted-turn counts, so the file is dominated by one-turn or near-one-turn tails rather than long spirals.
- The clearest repeated-behavior clusters are APD same-dataset refinement, school/location clue churn, Texas historical-county detours, and Texas education broad-search drift.
- Several rows are better described as terminal crashes with no clear repetitive waste, so they belong in an unclear group rather than being forced into a false loop taxonomy.

## Unresolved Or Mixed Cases

Rows without a confident repeated-waste loop:

- `tasks_mini/k-3-d-3/task_1.json`: estimated_wasted_turns=0; The log ends with a max-tokens crash, but no clearly repetitive wasted tail is visible before it.
- `tasks_mini/k-3-d-3/task_3.json`: estimated_wasted_turns=0; The run exhausted tokens while still exploring supporting pages, but the visible tail is not clearly repetitive enough to count waste confidently.
- `tasks_mini/k-3-d-4/task_7.json`: estimated_wasted_turns=1; The run hit the max-tokens crash before it could combine the year lists and finish the location/date lookup.
- `tasks_mini/k-4-d-4/task_5.json`: estimated_wasted_turns=0; The run exhausted tokens before it could move past the first dataset inspection.
- `tasks_mini/k-5-d-3/task_7.json`: estimated_wasted_turns=0; It reached the token cap before the final answer submission, not because it re-tried a dead end.

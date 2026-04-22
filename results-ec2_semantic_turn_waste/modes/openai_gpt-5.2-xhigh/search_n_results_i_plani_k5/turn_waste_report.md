# Turn Waste Report

- Source file: `results-ec2_semantic/modes/openai_gpt-5.2-xhigh/search_n_results_i_plani_k5/eval_results.csv`
- Audited row count: 61
- Total estimated wasted turns: 173
- Average estimated wasted turns: 2.84

## File-Local Groups

### Auxiliary evidence chase after narrowing the answer (10)
The run had the main candidate set, ranking, or answer path in hand, but spent its remaining budget chasing supporting geography or entity facts such as county seats, population, district datasets, income ranks, or biography pages instead of closing.

Representative task ids:
- `tasks_mini/k-2-d-4/task_1.json`
- `tasks_mini/k-2-d-4/task_8.json`
- `tasks_mini/k-3-d-4/task_1.json`
- `tasks_mini/k-3-d-4/task_7.json`

Distinguishing signals:
- Core counties, cities, properties, or institutions were already narrowed
- Late turns revisit county-seat, population, district, income, or biography lookups
- The wasted tail is usually a multi-turn confirmation hunt rather than a brand-new plan

### Off-path detours and rediscovery resets (8)
The run stepped away from the main answer path and reopened broad discovery, or wandered into unrelated entities and source families, burning budget before it returned to the real task.

Representative task ids:
- `tasks_mini/k-2-d-3/task_8.json`
- `tasks_mini/k-4-d-4/task_1.json`
- `tasks_mini/k-7-d-4/task_2.json`
- `tasks_mini/k-7-d-4/task_4.json`

Distinguishing signals:
- Broad discover-data or source-finding restarts after the needed family was already found
- Unrelated entities or topic pivots consume multiple late turns
- The tail looks like a reset, not a refinement of the existing extraction path

### Same-source rediscovery and file/schema poking (11)
The correct dataset family was basically identified, but the run kept re-searching nearby sources, re-peeking files, or rechecking schemas instead of committing to one extraction path.

Representative task ids:
- `tasks_mini/k-3-d-3/task_2.json`
- `tasks_mini/k-3-d-3/task_3.json`
- `tasks_mini/k-4-d-3/task_3.json`
- `tasks_mini/k-4-d-4/task_2.json`

Distinguishing signals:
- Repeated search_prefix, search_schema, list_files, grep_file, or peek_file calls on the same source family
- The late turns focus on source naming or file structure rather than answer extraction
- Many cases involve school-location, NCES, or nearby dataset-family retries

### Problematic-data recovery loops (8)
A malformed file, oversized file, parse failure, or bad query derailed the run, and the remaining turns were spent on retries or low-yield inspections around the same problem source.

Representative task ids:
- `tasks_mini/k-2-d-3/task_3.json`
- `tasks_mini/k-2-d-3/task_9.json`
- `tasks_mini/k-2-d-4/task_2.json`
- `tasks_mini/k-5-d-4/task_10.json`

Distinguishing signals:
- Oversized JSON, malformed CSV, parse/type errors, or failed queries appear near the stop point
- The tail retries the same source family instead of pivoting to a new extraction strategy
- Evidence often mentions repeated peeks, metadata checks, or alternate reads after the failure

### Stop-warning overruns (8)
The run received an explicit timeout or stop-and-submit style signal, but still spent one more turn or short tail repeating the same aggregation or verification before submitting or crashing.

Representative task ids:
- `tasks_mini/k-2-d-3/task_2.json`
- `tasks_mini/k-3-d-3/task_9.json`
- `tasks_mini/k-3-d-4/task_10.json`
- `tasks_mini/k-3-d-4/task_8.json`

Distinguishing signals:
- A warning to submit appears in the row summary or evidence
- The follow-up turn is still on the same dataset family or same aggregation
- Estimated wasted turns are usually low because the run was already near completion

### Budget-edge finishers (16)
The run stayed mostly on the intended path and lost only the last lookup, aggregation, read, or plan step to the budget limit, with little or no visible wasted tail.

Representative task ids:
- `tasks_mini/k-3-d-1/task_1.json`
- `tasks_mini/k-3-d-3/task_1.json`
- `tasks_mini/k-3-d-3/task_10.json`
- `tasks_mini/k-4-d-4/task_7.json`

Distinguishing signals:
- Most work remains productive through the final turns
- The stop condition cuts off the last needed query, read, or synthesis step
- Estimated wasted turns are often 0 or 1

## Highest Wasted-Turn Cases

- `tasks_mini/k-3-d-4/task_1.json`: 16 estimated wasted turns. Solved the crime-incidents and county-income path up to a best-effort answer, then kept reformulating household-income rank searches until timeout.
- `tasks_mini/k-7-d-4/task_4.json`: 14 estimated wasted turns. It chased the Duolingo and Pittsburgh path, then reopened school-dataset discovery instead of finishing the county math.
- `tasks_mini/k-7-d-4/task_5.json`: 11 estimated wasted turns. It tried to answer via Ali Partovi and Code.org, then wandered into Pittsburgh and Duolingo before returning to school datasets.
- `tasks_mini/k-5-d-4/task_1.json`: 10 estimated wasted turns. Searched Washington contract datasets, identified the likely college set, and then branched into county-seat and building-year lookups.
- `tasks_mini/k-4-d-4/task_3.json`: 8 estimated wasted turns. Computed Texas county expenditure averages, then chased county-seat and student-percentage data for the top counties.

## Unresolved Or Mixed Cases

- No synthetic mixed catch-all group was needed; every audited row fit a recurring local pattern.
- Duplicate resolution applied to `tasks_mini/k-7-d-3/task_9.json`: kept the manual-check version with the date-query error, oversized-table peek, and 3 estimated wasted turns.
- Near-complete rows with no clear wasted tail (`estimated_wasted_turns = 0`): `tasks_mini/k-6-d-4/task_1.json`, `tasks_mini/k-6-d-4/task_9.json`, `tasks_mini/k-7-d-3/task_5.json`

## Global Findings

- Duplicate resolution was applied: tasks_mini/k-7-d-3/task_9.json uses the manual-check version with repeated_behavior 'One bad date query, one oversized table peek, then the final parking aggregate timed out.' and estimated_wasted_turns 3.
- The highest-cost clusters are auxiliary evidence chase after narrowing the answer (10 rows, 60 estimated wasted turns) and off-path detours and rediscovery resets (8 rows, 47 estimated wasted turns).
- The worst individual tails are tasks_mini/k-3-d-4/task_1.json (16), tasks_mini/k-7-d-4/task_4.json (14), tasks_mini/k-7-d-4/task_5.json (11), and tasks_mini/k-5-d-4/task_1.json (10).
- Stop-warning overruns plus budget-edge finishers account for 24 of 61 rows, showing that many failures were close to completion and usually lost only 0 to 1 turns at the end.
- School-location and NCES-style tasks are overrepresented in same-source rediscovery and file/schema poking, while Texas county and county-seat style tasks cluster in auxiliary evidence chase after narrowing the answer.
- No mixed catch-all group was needed; every row fit a recurring local pattern without forcing a synthetic leftover bucket.

## Group Assignments

### Auxiliary evidence chase after narrowing the answer
- `tasks_mini/k-2-d-4/task_1.json`
- `tasks_mini/k-2-d-4/task_8.json`
- `tasks_mini/k-3-d-4/task_1.json`
- `tasks_mini/k-3-d-4/task_7.json`
- `tasks_mini/k-4-d-4/task_3.json`
- `tasks_mini/k-4-d-4/task_4.json`
- `tasks_mini/k-5-d-3/task_1.json`
- `tasks_mini/k-5-d-3/task_3.json`
- `tasks_mini/k-5-d-3/task_4.json`
- `tasks_mini/k-5-d-4/task_1.json`

### Off-path detours and rediscovery resets
- `tasks_mini/k-2-d-3/task_8.json`
- `tasks_mini/k-4-d-4/task_1.json`
- `tasks_mini/k-7-d-4/task_2.json`
- `tasks_mini/k-7-d-4/task_4.json`
- `tasks_mini/k-7-d-4/task_5.json`
- `tasks_mini/k-7-d-4/task_7.json`
- `tasks_mini/k-7-d-4/task_8.json`
- `tasks_mini/k-7-d-4/task_9.json`

### Same-source rediscovery and file/schema poking
- `tasks_mini/k-3-d-3/task_2.json`
- `tasks_mini/k-3-d-3/task_3.json`
- `tasks_mini/k-4-d-3/task_3.json`
- `tasks_mini/k-4-d-4/task_2.json`
- `tasks_mini/k-6-d-3/task_4.json`
- `tasks_mini/k-6-d-3/task_6.json`
- `tasks_mini/k-6-d-4/task_5.json`
- `tasks_mini/k-6-d-4/task_6.json`
- `tasks_mini/k-6-d-4/task_7.json`
- `tasks_mini/k-6-d-4/task_8.json`
- `tasks_mini/k-7-d-4/task_1.json`

### Problematic-data recovery loops
- `tasks_mini/k-2-d-3/task_3.json`
- `tasks_mini/k-2-d-3/task_9.json`
- `tasks_mini/k-2-d-4/task_2.json`
- `tasks_mini/k-5-d-4/task_10.json`
- `tasks_mini/k-5-d-4/task_4.json`
- `tasks_mini/k-5-d-4/task_9.json`
- `tasks_mini/k-6-d-3/task_3.json`
- `tasks_mini/k-7-d-3/task_9.json`

### Stop-warning overruns
- `tasks_mini/k-2-d-3/task_2.json`
- `tasks_mini/k-3-d-3/task_9.json`
- `tasks_mini/k-3-d-4/task_10.json`
- `tasks_mini/k-3-d-4/task_8.json`
- `tasks_mini/k-3-d-4/task_9.json`
- `tasks_mini/k-5-d-4/task_2.json`
- `tasks_mini/k-5-d-4/task_5.json`
- `tasks_mini/k-6-d-3/task_5.json`

### Budget-edge finishers
- `tasks_mini/k-3-d-1/task_1.json`
- `tasks_mini/k-3-d-3/task_1.json`
- `tasks_mini/k-3-d-3/task_10.json`
- `tasks_mini/k-4-d-4/task_7.json`
- `tasks_mini/k-4-d-4/task_8.json`
- `tasks_mini/k-5-d-3/task_5.json`
- `tasks_mini/k-5-d-4/task_8.json`
- `tasks_mini/k-6-d-4/task_1.json`
- `tasks_mini/k-6-d-4/task_9.json`
- `tasks_mini/k-7-d-3/task_10.json`
- `tasks_mini/k-7-d-3/task_5.json`
- `tasks_mini/k-7-d-3/task_6.json`
- `tasks_mini/k-7-d-3/task_7.json`
- `tasks_mini/k-7-d-3/task_8.json`
- `tasks_mini/k-7-d-4/task_10.json`
- `tasks_mini/k-7-d-4/task_6.json`


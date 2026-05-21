# Turn Waste Report

- Source file: `results_semantic/modes/openai_gpt-5-mini/search_d_results_i_plani_computei_k5_skills_off/eval_results.csv`
- Audited rows: 9
- Deterministic validation: 9 valid, 0 invalid, 0 missing-log
- Model validation: 7 pass, 2 repaired_pass, 0 invalid_untrusted
- Estimated wasted turns: total 93, average 10.3

## File-Local Groups

### Repeated extraction repairs for a remaining unresolved count (5 rows)

Runs that had the relevant source or partial answer in hand, then spent the tail on near-duplicate queries, greps, schema probes, repair attempts, or wrong-file inspections for one still-missing count.

- Distinguishing signals: Relevant datasets were already located; at least one intermediate count or source was known; wasted turns concentrate on repeated low-yield extraction attempts for the unresolved field.
- Estimated wasted turns: total 59, average 11.8
- Representative task ids: tasks_mini/k-3-d-1/task_1.json, tasks_mini/k-3-d-2/task_1.json, tasks_mini/k-3-d-2/task_6.json

### Context rechecks and broad searches after the target path was known (2 rows)

Runs that continued revisiting already-established context or broad clue searches instead of retrieving the exact remaining table/value or completing the next concrete computation.

- Distinguishing signals: Late wasted turns are described as rechecking known facts, broad searches, or clue re-searches rather than focused extraction from the needed source.
- Estimated wasted turns: total 11, average 5.5
- Representative task ids: tasks_mini/k-4-d-2/task_1.json, tasks_mini/k-5-d-4/task_2.json

### Stalled on an early hop instead of advancing through a multi-hop chain (2 rows)

Runs that became stuck on an early dataset or partial context and did not proceed to later required hops or aggregations before the budget expired.

- Distinguishing signals: The summaries explicitly say later chain steps were never reached or completed; repeated work stayed around the first or partial computation instead of moving forward.
- Estimated wasted turns: total 23, average 11.5
- Representative task ids: tasks_mini/k-5-d-1/task_3.json, tasks_mini/k-6-d-2/task_4.json

## Global Summary

Across 9 failed rows, the dominant local pattern is repeated extraction repair around a single unresolved count after relevant sources or partial answers were already found. A secondary pattern is losing budget to context rechecks or broad searches after the next needed target was clear. The remaining rows show multi-hop chains stalling on an early hop, preventing later computations from ever being attempted.

## Global Findings

Most wasted turns were not from initial discovery but from late-stage execution discipline: repeated query reformulations, schema probes, grep/read detours, and revisiting known context. The largest waste estimates appear where one unresolved count or early-hop extraction trapped the run until tool or turn exhaustion. Several tasks had usable intermediate progress, but the agent failed to switch from exploration to exact extraction, aggregation, or timely submission.

## Unresolved Or Mixed Cases

None. All audited rows passed deterministic validation and model grounding after two conservative repairs.

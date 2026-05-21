# Turn Waste Report

- Source file: `results_semantic/modes/openai_gpt-5-mini/search_n_results_i_plani_computei_k5_skills_off/eval_results.csv`
- Audited row count: 9
- Total estimated wasted turns: 120
- Average estimated wasted turns: 13.3

## Discovered File-Local Groups

### Wrong-source or wrong-file computation loops

- Rows: 4
- Estimated wasted turns: 51
- Description: Runs spent their remaining budget querying, repairing, or inspecting an incorrect source, metadata file, sample path, or incompatible file representation instead of executing the needed final computation.
- Distinguishing signals: Repeated query/execute attempts against metadata or the wrong dataset; repair attempts preserve the same bad source choice; final needed count or aggregation is delayed until cancellation or timeout.
- Representative task ids: tasks_mini/k-4-d-2/task_6.json, tasks_mini/k-4-d-2/task_9.json, tasks_mini/k-4-d-4/task_10.json, tasks_mini/k-4-d-5/task_3.json

### Redundant discovery and reconfirmation after enough evidence

- Rows: 4
- Estimated wasted turns: 56
- Description: Runs had already identified key entities, areas, datasets, or candidate sources, but kept re-searching or rechecking them instead of advancing to the missing downstream computation.
- Distinguishing signals: Near-duplicate searches for already-located entities or datasets; repeated confirmation of the same geographic or source evidence; progress stalls before final counts even though the next target is known.
- Representative task ids: tasks_mini/k-3-d-2/task_9.json, tasks_mini/k-4-d-2/task_4.json, tasks_mini/k-4-d-4/task_13.json, tasks_mini/k-4-d-4/task_6.json

### Tool-friction repair loop on oversized or brittle data

- Rows: 1
- Estimated wasted turns: 13
- Description: The run encountered tooling friction on a large or difficult file, then spent many turns on duplicate searches, malformed repairs, or placeholder fixes without establishing the remaining required computations.
- Distinguishing signals: Large-file query failure became the dominant obstacle; repeated low-yield grep/query attempts followed the known blocker; repair attempts were malformed or did not resolve the computation path.
- Representative task ids: tasks_mini/k-2-d-3/task_1.json

## Global Summary

Across the 9 accepted failed rows, the dominant waste pattern is budget spent after useful intermediate progress: either re-confirming already-known evidence or looping on the wrong computational substrate. Wrong-source/wrong-file computation loops and redundant discovery/reconfirmation each cover 4 rows. One row is separate because large-file/tool friction plus malformed repair attempts dominated the failure.

## Global Findings

- Most failures were not early dead ends; they had located important entities, datasets, counties, sectors, or schemas before wasting the tail of the run.
- A common transition point was failure to move from discovery into the final constrained aggregation or count.
- Wrong-file and metadata loops were especially costly because repair attempts tended to preserve the bad target instead of reconsidering the data source.
- Redundant reconfirmation often consumed the final turns after enough evidence existed to continue, leaving the terminal computation incomplete.

## Unresolved Or Mixed Cases

- None. All audited rows are deterministic-valid and model-validated as `pass` or `repaired_pass`.

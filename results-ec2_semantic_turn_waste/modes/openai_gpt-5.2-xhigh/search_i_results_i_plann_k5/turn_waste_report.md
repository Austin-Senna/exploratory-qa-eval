# Turn Waste Report

Source file: `results-ec2_semantic/modes/openai_gpt-5.2-xhigh/search_i_results_i_plann_k5/eval_results.csv`

Audited row count: 47

Total estimated wasted turns: 148

Average estimated wasted turns: 3.22 across 46 estimable rows

Rows with unresolved estimate: 1

## Global Summary

This file clusters into six moderate-granularity patterns. Schema and file-shape thrash is the largest cluster, followed by late candidate rechecks and ranking reruns; smaller groups cover search reformulation, off-path drift, and a few low-signal or mismatched traces.

## Global Findings

- The strongest recurring waste mode is schema/file thrash, especially in rows that keep opening headers, columns, raw files, redirects, or sandbox paths instead of reaching the substantive query.
- A large second pattern is late-stage reconfirmation: the agent often had the right candidate or evidence but spent the tail checking totals, alternate pages, or nearby records instead of submitting.
- Ranking and aggregation reruns recur across several rows, usually as repeated top-k or year-by-year queries after the relevant candidate set was already visible.
- Search reformulation loops and off-path drift are smaller but real: some runs keep rewording the same search, while others wander into side investigations or wrong metrics.
- The mixed group is intentionally conservative and includes the trace/eval mismatch plus the few summaries that do not expose a clear repeat loop.

## Discovered Groups

## late_candidate_rechecks (11)
Rows where the agent already had the key candidate or evidence, then spent the tail reconfirming rows, totals, alternate pages, or nearby entities instead of submitting.

Signals: re-reading already-found source pages; checking alternate candidates or nearby records after the answer path was clear; post-answer totals, null-row, or row-level validation

Representative task ids: tasks_mini/k-2-d-3/task_1.json, tasks_mini/k-2-d-3/task_8.json, tasks_mini/k-2-d-4/task_8.json

## search_reformulation_loops (6)
Rows where the run kept rephrasing or reissuing the same search/query family instead of changing strategy.

Signals: near-duplicate search queries; exact-match or continuation searches on the same target; search or setup churn after an unhelpful result or timeout

Representative task ids: tasks_mini/k-2-d-3/task_2.json, tasks_mini/k-4-d-4/task_3.json, tasks_mini/k-5-d-4/task_10.json

## schema_file_thrash (13)
Rows dominated by metadata, schema, header, parser, raw-file, or sandbox inspection instead of the substantive counting step.

Signals: header, column, catalog, or type peeks; parser or read_csv workarounds; raw file preview, grep, or sandbox-path inspection

Representative task ids: tasks_mini/k-2-d-4/task_4.json, tasks_mini/k-4-d-3/task_3.json, tasks_mini/k-4-d-3/task_5.json

## ranking_aggregation_reruns (8)
Rows that kept rerunning top-k, per-year, or aggregate queries on already-seen datasets rather than collapsing them into the final comparison.

Signals: repeating rank lists or per-year aggregates; slight metric variations over the same dataset; restarting a comparison after the key candidate was already visible

Representative task ids: tasks_mini/k-2-d-4/task_3.json, tasks_mini/k-3-d-3/task_1.json, tasks_mini/k-3-d-4/task_9.json

## off_path_drift (5)
Rows that visibly drifted into a different subproblem, wrong metric, or unrelated background lookup before returning to the main task.

Signals: biography, county, or other side-quest detours; wrong-metric or wrong-source digressions; downstream work started before the target entity was established

Representative task ids: tasks_mini/k-3-d-4/task_10.json, tasks_mini/k-5-d-4/task_3.json, tasks_mini/k-5-d-4/task_6.json

## mixed_low_signal (4)
Rows where the visible summary is ambiguous, mostly one-pass, or the trace and eval row do not line up cleanly enough for a confident waste pattern.

Signals: no clear repeat loop in the visible summary; log/result mismatch; mostly one-pass work with only weak late waste signals

Representative task ids: tasks_mini/k-2-d-4/task_5.json, tasks_mini/k-4-d-3/task_4.json, tasks_mini/k-5-d-3/task_7.json

## Unresolved or Mixed Cases

- tasks_mini/k-4-d-3/task_4.json: The serial county-by-county queries added new evidence, so there is no clear repeat loop to bucket.
- tasks_mini/k-5-d-3/task_7.json: The visible summary does not show a strong repeat loop, so the waste pattern stays low-signal.
- tasks_mini/k-6-d-4/task_8.json: The visible trace never got past broad previews, so the repeat pattern is not clear.
- tasks_mini/k-2-d-4/task_5.json: The matched log and eval row conflict, so the waste pattern cannot be recovered confidently.

# Turn Waste Report

- Source file path: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/eval_results.csv`
- Audited row count: 17
- Total estimated wasted turns: 128
- Average estimated wasted turns: 7.53
- Invalid, missing-log, or untrusted audited rows: 0

## Discovered File-Local Groups

### Redundant ranking rechecks after candidate sets were known

- Count: 8
- Description: Runs repeatedly recomputed top-N lists, rankings, or membership filters after the relevant candidate set or yearly lists had already been recovered.
- Distinguishing signals: Near-duplicate query_ideal calls over the same ranking files; repeated year-by-year top-list repair loops; stagnation warnings after execute-heavy runs; downstream hops left unfinished.
- Representative task ids: `tasks_mini/k-3-d-3/task_4.json`, `tasks_mini/k-3-d-3/task_5.json`, `tasks_mini/k-3-d-4/task_2.json`

### Schema, file-path, and dataset recovery churn

- Count: 5
- Description: Runs lost budget probing schemas, alternate file paths, metadata, or ambiguous dataset ids instead of advancing from already available intermediate facts.
- Distinguishing signals: Schema/sample inspection, list_files/read_file/grep_file recovery, 404 or ambiguous dataset errors, binder/column repair loops, and cancelled final lookup attempts.
- Representative task ids: `tasks_mini/k-3-d-3/task_2.json`, `tasks_mini/k-3-d-5/task_1.json`, `tasks_mini/k-4-d-2/task_10.json`

### Redundant verification after answer-relevant values were available

- Count: 3
- Description: Runs had enough key numeric or entity evidence to finish, but continued making confirmation, recalculation, or parsing calls that added little new information.
- Distinguishing signals: Post-result validation queries, hardcoded arithmetic through tools, repeated count checks, or extra parse calls after the needed comparison value was visible.
- Representative task ids: `tasks_mini/k-4-d-2/task_5.json`, `tasks_mini/k-5-d-3/task_6.json`, `tasks_mini/k-5-d-3/task_7.json`

### Late detours on low-yield downstream side quests

- Count: 1
- Description: Runs reached useful intermediate progress, then spent the remaining calls on side-source probes or tangential follow-up checks before reaching the final required hop.
- Distinguishing signals: Intermediate result available, followed by broad or misdirected downstream source queries; final required computation or lookup never reached.
- Representative task ids: `tasks_mini/k-5-d-4/task_2.json`

## Global Summary

Across 17 accepted rows, the dominant wasted-turn pattern was continuing to query or repair already-solved ranking and candidate-selection steps instead of moving to downstream hops. A second major pattern was schema, file-path, and dataset recovery churn, especially after partial progress had already narrowed the answer path. Smaller but recurring failures involved unnecessary post-result verification and final low-yield side detours.

## Global Findings

- The largest group is redundant ranking rechecks, covering 8 of 17 rows; these runs repeatedly recomputed top-N lists, yearly rankings, or membership filters after useful candidate sets were already available.
- Schema and dataset recovery churn accounts for 5 rows; these failures show budget loss through file probes, schema/sample inspection, 404s, ambiguous dataset ids, or column-repair loops.
- Three rows had answer-relevant values available but kept using tools for confirmation or arithmetic that could have been performed directly.
- Most failures were not caused by lack of initial progress; they came from failure to recognize a sufficient intermediate result and pivot to the next hop under a fixed 30-tool budget.
- Stagnation and tool-limit warnings often appeared after execute-heavy repeated calls, but the runs still attempted one more confirmation, parse, or lookup before submission.

## Unresolved Or Mixed Cases

- None. All audited rows are trusted after deterministic and model validation.

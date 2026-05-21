# Turn Waste Report

- Source file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic/modes/openai_gpt-5.4-nano/search_i_results_i_pland_computei_k5_skills_off/eval_results.csv`
- Mirrored file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_turn_waste/modes/openai_gpt-5.4-nano/search_i_results_i_pland_computei_k5_skills_off/eval_results.csv`
- Audited rows: 29
- Deterministic validation: 29 valid, 0 valid_with_warnings, 0 invalid/missing-log
- Model validation: 26 pass, 3 repaired_pass, 0 invalid_untrusted
- Estimated wasted turns: total 172, average 5.9

## Discovered File-Local Groups

### Repair-loop placeholders (11 rows)

Runs kept retrying near-duplicate query_ideal or execute_ideal computations after repair/status failures, then submitted null, zero, blank, unknown, or unable-to-determine answers.

- Estimated wasted turns: total 50, average 4.5
- Distinguishing signals: SQL repair JSONDecodeError or status/path errors; progress stopped on one dataset or subproblem; final placeholder-style submission after repeated failed computations
- Representative task ids: `tasks_mini/k-3-d-4/task_5.json`, `tasks_mini/k-5-d-4/task_7.json`, `tasks_mini/k-3-d-2/task_9.json`

### Missing-data schema loops (3 rows)

Runs found candidate sources but got stuck rechecking schema, catalog files, or missing data instead of finding a usable data path.

- Estimated wasted turns: total 17, average 5.7
- Distinguishing signals: repeated schema/count/catalog probes; same missing or unusable dataset revisited; placeholder answer after unresolved data access
- Representative task ids: `tasks_mini/k-3-d-2/task_8.json`, `tasks_mini/k-3-d-2/task_6.json`, `tasks_mini/k-4-d-4/task_11.json`

### Overworked first hop (10 rows)

Runs kept recomputing first-hop rankings, filters, or counts after enough evidence existed, leaving downstream hops unfinished.

- Estimated wasted turns: total 80, average 8.0
- Distinguishing signals: duplicate ranking or count queries; known first-hop result not converted into next-hop work; downstream bridge, biography, location, or final-count hops never reached
- Representative task ids: `tasks_mini/k-5-d-3/task_5.json`, `tasks_mini/k-3-d-4/task_3.json`, `tasks_mini/k-5-d-4/task_1.json`

### Format workaround churn (4 rows)

Runs stalled on large, GeoJSON, XML, KML, or otherwise awkward file access patterns and spent turns on mismatched parsing workarounds.

- Estimated wasted turns: total 21, average 5.2
- Distinguishing signals: large-file, GeoJSON, XML, or KML access issues; Binder errors or incompatible field extraction; repeated low-yield parsing/query variations
- Representative task ids: `tasks_mini/k-4-d-4/task_10.json`, `tasks_mini/k-3-d-4/task_6.json`, `tasks_mini/k-4-d-1/task_3.json`

### Unresolved mapping searches (1 rows)

Runs completed a numeric or dataset subproblem but then wasted turns on repeated search or lookup attempts for an entity mapping needed for the next hop.

- Estimated wasted turns: total 4, average 4.0
- Distinguishing signals: repeated search_ideal reformulations; mapping target remained unresolved; null submission after empty or failed lookup attempts
- Representative task ids: `tasks_mini/k-7-d-4/task_1.json`

## Global Findings

- 11 of 29 rows primarily wasted turns retrying failed ideal computations or repair paths on the same subproblem.
- 10 of 29 rows over-invested in first-hop rankings, counts, or filters and did not pivot to downstream reasoning hops.
- Format-specific access problems involving large files, GeoJSON, XML, or KML caused a smaller but distinct cluster of wasted workaround turns.
- Many error_unknown rows hide concrete patterns: placeholder submission after known missing data, repair-loop stagnation, or budget exhaustion after repeated low-yield tool use.

## Unresolved Or Mixed Cases

- No invalid, missing-log, or untrusted model-validation rows remain.
- Singleton unresolved mapping pattern retained as its own local group: `tasks_mini/k-7-d-4/task_1.json`.

## Notes

- The previous usage-limit model-validation blocker has been cleared for this file; all accepted rows now have `pass` or `repaired_pass` model-validation status.

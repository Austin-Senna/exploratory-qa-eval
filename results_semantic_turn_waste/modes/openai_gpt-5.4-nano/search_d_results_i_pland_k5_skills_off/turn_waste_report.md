# Turn Waste Report

- Source file: `results_semantic/modes/openai_gpt-5.4-nano/search_d_results_i_pland_k5_skills_off/eval_results.csv`
- Mirrored file: `results_semantic_turn_waste/modes/openai_gpt-5.4-nano/search_d_results_i_pland_k5_skills_off/eval_results.csv`
- Audited runtime-failure rows: 17
- Deterministic validation: 0 invalid/missing rows; 1 valid-with-warnings
- Model validation: 14 pass; 3 repaired_pass
- Total estimated wasted turns: 89
- Average estimated wasted turns: 5.2

## File-local Groups

### File access and data-shape mismatch loops (6)
Runs repeatedly used low-yield query/read/download patterns against files whose shape was already known to be unsuitable, such as metadata-like files, oversized CSVs, GeoJSON FeatureCollections, or top-level JSON wrappers.

Representative task ids: `tasks_mini/k-3-d-3/task_2.json`, `tasks_mini/k-4-d-2/task_6.json`, `tasks_mini/k-4-d-3/task_5.json`

### Repeated tabular parsing or filter refinement (5)
Runs stayed on the same tabular or semi-tabular computation with repeated malformed SQL, parsing errors, empty filters, or narrow rechecks after enough evidence existed to change strategy.

Representative task ids: `tasks_mini/k-4-d-1/task_1.json`, `tasks_mini/k-4-d-2/task_8.json`, `tasks_mini/k-4-d-3/task_7.json`

### Redundant validation or detours after useful candidate evidence (4)
Runs had already found useful candidate values, rankings, or identifiers, but spent late turns rechecking the same evidence or exploring a detour instead of advancing to the remaining hops.

Representative task ids: `tasks_mini/k-4-d-3/task_2.json`, `tasks_mini/k-4-d-3/task_6.json`, `tasks_mini/k-4-d-4/task_2.json`

### Premature submission after recoverable blocker (2)
Runs encountered a recoverable failed query, cancellation, or unresolved denominator lookup and then submitted a non-answer or placeholder rather than repairing the immediate blocker.

Representative task ids: `tasks_mini/k-3-d-4/task_5.json`, `tasks_mini/k-4-d-2/task_5.json`

## Global Findings

Across 17 accepted rows, the dominant wasted-turn pattern was repeated low-yield data access or parsing after the file shape, schema, or candidate evidence was already visible. The rows account for 89 estimated wasted turns in total, averaging about 5.2 wasted turns per failed run. Most failures were not pure reasoning failures; they were execution-path failures where the agent did not pivot after tool feedback, duplicate evidence, empty filters, or known missing downstream hops.

- The largest umbrella group is file access and data-shape mismatch loops, covering 6 rows where metadata-like files, oversized files, GeoJSON, or FeatureCollection structures were handled with unsuitable repeated reads or queries.
- A second recurring pattern is repeated tabular parsing or filter refinement, covering 5 rows where malformed SQL, parsing assumptions, or overly narrow filters consumed turns without unlocking the next hop.
- Four rows show redundant validation or detours after useful candidate evidence was already available; these failures left later hops unfinished despite partial progress.
- Two rows had short wasted tails but failed by prematurely submitting after a recoverable blocker, cancellation, or unresolved denominator lookup.
- High-waste examples often combine a local data-access problem with failure to advance the multi-hop chain, so the wasted turns are concentrated around one stuck intermediate hop rather than spread evenly across the whole task.

## Unresolved Or Mixed Cases

- None. All audited rows passed deterministic validation and model validation after repairs.

## Validation Notes

- `tasks_mini/k-4-d-1/task_1.json`: deterministic `valid_with_warnings` (estimated_wasted_turns=10 but wasted_turn_ranges covers 13 turns); model `pass` (The log shows the run located the arrest-data-from-2010-to-2019 and crime-data-from-2020-to-present datasets.; Turn 21 read the arrest rows header with Arrest Date, Area ID, Area Name, and Charge Group Description.; Turn 30 grep found rows containing Moving Traffic Violations in the arrest dataset.)
- `tasks_mini/k-4-d-3/task_2.json`: deterministic `valid` (no notes); model `repaired_pass` (Repaired: Turn 31 evidence truncates and misquotes the submitted reasoning instead of using an exact log fragment.; Productive ranges over-include Turn 31, which is the forced final submission after the tool-limit stop.)
- `tasks_mini/k-4-d-3/task_6.json`: deterministic `valid` (no notes); model `repaired_pass` (Repaired: Some evidence strings add quote wrappers around Executing fragments that are not exact log text.; extracted_error_evidence is grounded but should use the Turn 22 tool-limit fragment.)
- `tasks_mini/k-4-d-3/task_7.json`: deterministic `valid` (no notes); model `repaired_pass` (Repaired: Original row overstates a hard tool-call limit; the log shows final submission after missing data, with execute-stagnation cancellation and parse/query errors rather than a visible hard tool-limit stop.)

# Turn Waste Report

Source file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic/modes/openai_gpt-5.4-nano/search_n_results_i_plann_k5_skills_off/eval_results.csv`

Audited trusted row count: 19
Total estimated wasted turns: 105
Average estimated wasted turns: 5.53

## Discovered File-Local Groups

### Nested or unsupported file formats handled as flat tables (7 rows)
Runs reached relevant GeoJSON, XML/KML, or FeatureCollection-style data but kept using flat SQL/query_file patterns after the tool exposed only top-level or incompatible structure.
Estimated wasted turns: 27
Representative task ids: tasks_mini/k-3-d-2/task_10.json; tasks_mini/k-3-d-2/task_6.json; tasks_mini/k-4-d-2/task_7.json; tasks_mini/k-5-d-3/task_10.json

### Metadata or catalog files mistaken for usable row data (4 rows)
Runs found plausible sources but spent their wasted tail inspecting catalog metadata, metadata-only downloads, or the wrong data.txt/header path instead of recovering actual row-level data.
Estimated wasted turns: 17
Representative task ids: tasks_mini/k-5-d-4/task_5.json; tasks_mini/k-5-d-2/task_3.json; tasks_mini/k-3-d-1/task_1.json; tasks_mini/k-6-d-3/task_3.json

### Tool budget consumed by duplicate or wrong-scope detours (4 rows)
Runs made real partial progress, but then burned many late turns on already-solved steps, wrong time ranges, wrong geography, duplicate filters, or irrelevant nearby datasets until the final required computation could not be completed.
Estimated wasted turns: 41
Representative task ids: tasks_mini/k-4-d-2/task_5.json; tasks_mini/k-4-d-1/task_2.json; tasks_mini/k-4-d-3/task_7.json; tasks_mini/k-5-d-2/task_5.json

### Narrow single-source fixation after schema mismatch (3 rows)
Runs stayed on one mismatched or insufficient dataset after the available schema showed it could not support the required field or remaining hop.
Estimated wasted turns: 10
Representative task ids: tasks_mini/k-5-d-4/task_6.json; tasks_mini/k-3-d-4/task_5.json; tasks_mini/k-6-d-2/task_1.json

### Incomplete multi-hop exploration after unresolved filter or lookup (1 rows)
A run located relevant datasets and some row-level evidence but stopped after low-yield county/enrollment-style probes without resolving the needed intermediate target or final lookup.
Estimated wasted turns: 10
Representative task ids: tasks_mini/k-5-d-4/task_7.json

## Global Summary

Across the accepted rows, wasted turns mostly came from agents failing to change data-access strategy after clear evidence that the current file or query shape was wrong. The largest recurring pattern was treating nested or unsupported geospatial/JSON formats as flat tables. The costliest failures were budget-burn cases where partial progress was real but repeated wrong-scope detours displaced the remaining required hops.

## Global Findings

The dominant fix target is recovery behavior after schema or format mismatch: agents should pivot from query_file to explicit parsing/flattening when GeoJSON or FeatureCollection structure is exposed, and should stop re-querying metadata/catalog files once outputs show non-row-level data. A second major target is budget discipline: after a hop is solved or a likely dataset is surfaced, repeated confirmation queries and nearby wrong-dataset probes frequently consume the final tool budget before the actual answer computation.

## Unresolved Or Mixed Cases

No invalid, missing-log, or untrusted audited rows remain in this file.

# Turn Waste Report

- Source file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic/modes/openai_gpt-5-mini/search_d_results_i_pland_k5_skills_off/eval_results.csv`
- Audited rows: 3
- Deterministic validation: 3 valid, 0 invalid, 0 missing-log
- Model validation: 3 pass, 0 repaired, 0 invalid
- Total estimated wasted turns: 24
- Average estimated wasted turns: 8.00

## Discovered File-Local Groups

### Post-discovery extraction thrash

- Count: 2
- Description: The agent found relevant datasets or sources, then spent the failure tail repeatedly trying to extract or aggregate needed values with invalid, stale, or overly broad queries before a hard stop.
- Representative task ids: `tasks_mini/k-3-d-4/task_3.json`, `tasks_mini/k-4-d-2/task_7.json`
- Signals: relevant source already located; repeated extraction/parsing attempts; schema mismatch, JSON extraction, cancelled aggregate, or broad scan; downstream comparison or submission not completed.

### Redundant rediscovery and rework before later-hop completion

- Count: 1
- Description: The agent made partial progress, but wasted calls on repeated searches, repeated query formulations, and redoing already retrieved intermediate results, leaving no budget for the remaining source/year lookup and final bridge step.
- Representative task ids: `tasks_mini/k-3-d-5/task_1.json`
- Signals: intermediate results already available; near-duplicate searches/query attempts; re-running known top-list work; later-hop lookup not reached.

## Row Notes

- `tasks_mini/k-4-d-2/task_7.json`: 9 wasted turns, group `Post-discovery extraction thrash`. Found NoMa/Ward 6 and the DC crime GeoJSON datasets, but failed to aggregate offense counts before the tool limit.
- `tasks_mini/k-3-d-4/task_3.json`: 6 wasted turns, group `Post-discovery extraction thrash`. Found the Washington report-card enrollment and assessment datasets, computed low-income county lists, then stalled extracting 2021-22 math proficiency and never reached population lookup or submission.
- `tasks_mini/k-3-d-5/task_1.json`: 9 wasted turns, group `Redundant rediscovery and rework before later-hop completion`. Found the school progress report datasets and top lists for 2006-2009, but exhausted tools before retrieving 2010-2011 and before the bridge-builder province lookup.

## Global Findings

- All three rows show meaningful early progress before waste began.
- The largest shared failure mode is repeated low-yield tool use after the path was partially known.
- Structured data extraction was the most common bottleneck, especially where JSON/schema handling or cross-year filtering was required.
- Tool budget failures were driven less by initial source discovery and more by unresolved extraction strategy once the relevant source was already found.

## Unresolved Or Mixed Cases

- None among the validated audited rows.

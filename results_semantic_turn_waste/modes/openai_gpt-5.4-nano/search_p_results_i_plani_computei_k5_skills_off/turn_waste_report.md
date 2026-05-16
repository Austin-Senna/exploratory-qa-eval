# Turn Waste Report

- Source file: `results_semantic/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/eval_results.csv`
- Audited row count: 3
- Trusted audited rows summarized: 3
- Invalid, missing, or untrusted rows: 0
- Total estimated wasted turns: 27
- Average estimated wasted turns: 9.00

## Discovered File-Local Groups

### Repeated dataset-query loops before downstream hops (3)

Runs made some early progress, then spent the remaining turn or tool budget re-querying, repairing, or re-inspecting the same dataset/hop instead of advancing through the remaining reasoning chain.

Distinguishing signals:
- Repeated calls against the same dataset or same family of near-duplicate aggregation/schema queries
- Progress stopped at an early or middle hop while later source lookups were never reached
- Timeout or tool-limit warnings occurred after redundant query attempts

Representative task ids:
- `tasks_mini/k-3-d-4/task_1.json`
- `tasks_mini/k-4-d-4/task_5.json`
- `tasks_mini/k-5-d-3/task_10.json`

## Row Assignments

- `tasks_mini/k-3-d-4/task_1.json` -> **Repeated dataset-query loops before downstream hops** (6 estimated wasted turns): The run stayed on repeated ward crime-count and lowest-average crime aggregations after the first hop, preventing neighborhood, county, and income-rank lookup steps.
- `tasks_mini/k-4-d-4/task_5.json` -> **Repeated dataset-query loops before downstream hops** (17 estimated wasted turns): The run repeatedly probed state-expenditure schema and spending-rank queries, especially for 2007-state-expenditures, instead of moving to district, highway, and 500 Cities steps.
- `tasks_mini/k-5-d-3/task_10.json` -> **Repeated dataset-query loops before downstream hops** (4 estimated wasted turns): The run kept inspecting and retrying the 2022 street-sweeping schedule after obtaining partial ward counts, exhausting the tool budget before later sweeping-year, charter-school, and birthplace hops.

## Global Summary

All accepted rows show the same broad wasted-turn pattern: after planning and partial progress, the agent became anchored on one dataset or reasoning hop and spent remaining budget on near-duplicate queries, repairs, or schema probes. The failures were not caused by complete lack of direction; they were caused by failure to transition from a solved or partially solved hop to the next required source lookup.

## Global Findings

- The dominant issue is chain-advancement failure after partial progress.
- Repeated query repair and schema inspection consumed the largest waste tail in tasks_mini/k-4-d-4/task_5.json.
- The same pattern appears both early in the chain, as in ward crime and state-expenditure loops, and mid-chain, as in the street-sweeping loop.
- Stop or stagnation warnings did not reliably trigger replanning or immediate best-effort submission.

## Unresolved Or Mixed Cases

- None.

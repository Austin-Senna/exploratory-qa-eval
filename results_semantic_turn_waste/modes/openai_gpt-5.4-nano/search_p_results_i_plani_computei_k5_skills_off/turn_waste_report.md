# Turn Waste Report

- Source file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic/modes/openai_gpt-5.4-nano/search_p_results_i_plani_computei_k5_skills_off/eval_results.csv`
- Audited row count: 33
- Trusted audited rows summarized: 33
- Invalid, missing, or untrusted rows: 0
- Total estimated wasted turns: 204
- Average estimated wasted turns: 6.18

## Discovered File-Local Groups

### Ideal repair/status-error loops (16)

Runs repeatedly hit query_ideal/execute_ideal repair failures, JSONDecodeError/status-error paths, or semantically rejected repair loops.

Distinguishing signals:
- Repeated query_ideal/execute_ideal repair attempts
- JSONDecodeError, status-error, or semantic-repair rejection evidence
- Submission after failing to recover from the tool/repair loop

Representative task ids:
- `tasks_mini/k-4-d-2/task_4.json` (14 estimated wasted turns)
- `tasks_mini/k-3-d-4/task_3.json` (10 estimated wasted turns)
- `tasks_mini/k-4-d-1/task_3.json` (8 estimated wasted turns)
- `tasks_mini/k-4-d-3/task_2.json` (8 estimated wasted turns)

### Budget exhausted after repeated same-hop work (7)

Runs made partial progress, then spent late turns repeating or repairing one hop until timeout/tool budget stopped further work.

Distinguishing signals:
- Tool-limit, hard-timeout, or timeout evidence in the tail
- Repeated work on the same dataset/hop after partial progress
- Downstream hops left unreached

Representative task ids:
- `tasks_mini/k-4-d-4/task_5.json` (14 estimated wasted turns)
- `tasks_mini/k-5-d-3/task_8.json` (12 estimated wasted turns)
- `tasks_mini/k-5-d-4/task_3.json` (12 estimated wasted turns)
- `tasks_mini/k-6-d-3/task_3.json` (12 estimated wasted turns)

### Known-missing-data final submissions (6)

Runs reached a known evidence gap and submitted null, unknown, placeholder, or incomplete answers without a hard budget stop.

Distinguishing signals:
- Final answer explicitly null, unknown, placeholder, or unable-to-determine
- Reasoning or behavior shows unresolved/missing final evidence
- Little or no hard-stop evidence at the final turn

Representative task ids:
- `tasks_mini/k-3-d-2/task_9.json` (8 estimated wasted turns)
- `tasks_mini/k-3-d-2/task_5.json` (5 estimated wasted turns)
- `tasks_mini/k-3-d-4/task_4.json` (5 estimated wasted turns)
- `tasks_mini/k-4-d-4/task_4.json` (4 estimated wasted turns)

### Sandbox or source-access failures followed by fallback (4)

Runs were derailed by file-path, sandbox, parsing, or source-access failures and ended with fallback submissions.

Distinguishing signals:
- FileNotFoundError, disabled network, XML/KML, or parsing failures
- Fallback query attempts after source-access failure
- Final answer made without resolving the source failure

Representative task ids:
- `tasks_mini/k-3-d-4/task_6.json` (5 estimated wasted turns)
- `tasks_mini/k-5-d-4/task_2.json` (5 estimated wasted turns)
- `tasks_mini/k-3-d-2/task_11.json` (3 estimated wasted turns)
- `tasks_mini/k-4-d-2/task_8.json` (3 estimated wasted turns)

## Row Assignments

- `tasks_mini/k-4-d-2/task_4.json` -> **Ideal repair/status-error loops** (14 estimated wasted turns): The run repeatedly hit query_ideal/execute_ideal repair or status-error paths and did not recover cleanly.
- `tasks_mini/k-3-d-4/task_3.json` -> **Ideal repair/status-error loops** (10 estimated wasted turns): The run repeatedly hit query_ideal/execute_ideal repair or status-error paths and did not recover cleanly.
- `tasks_mini/k-4-d-1/task_3.json` -> **Ideal repair/status-error loops** (8 estimated wasted turns): The run repeatedly hit query_ideal/execute_ideal repair or status-error paths and did not recover cleanly.
- `tasks_mini/k-4-d-3/task_2.json` -> **Ideal repair/status-error loops** (8 estimated wasted turns): The run repeatedly hit query_ideal/execute_ideal repair or status-error paths and did not recover cleanly.
- `tasks_mini/k-5-d-4/task_8.json` -> **Ideal repair/status-error loops** (8 estimated wasted turns): The run repeatedly hit query_ideal/execute_ideal repair or status-error paths and did not recover cleanly.
- `tasks_mini/k-3-d-2/task_7.json` -> **Ideal repair/status-error loops** (6 estimated wasted turns): The run repeatedly hit query_ideal/execute_ideal repair or status-error paths and did not recover cleanly.
- `tasks_mini/k-5-d-3/task_12.json` -> **Ideal repair/status-error loops** (6 estimated wasted turns): The run repeatedly hit query_ideal/execute_ideal repair or status-error paths and did not recover cleanly.
- `tasks_mini/k-5-d-4/task_4.json` -> **Ideal repair/status-error loops** (6 estimated wasted turns): The run repeatedly hit query_ideal/execute_ideal repair or status-error paths and did not recover cleanly.
- `tasks_mini/k-4-d-4/task_1.json` -> **Ideal repair/status-error loops** (5 estimated wasted turns): The run repeatedly hit query_ideal/execute_ideal repair or status-error paths and did not recover cleanly.
- `tasks_mini/k-6-d-3/task_5.json` -> **Ideal repair/status-error loops** (5 estimated wasted turns): The run repeatedly hit query_ideal/execute_ideal repair or status-error paths and did not recover cleanly.
- `tasks_mini/k-3-d-2/task_6.json` -> **Ideal repair/status-error loops** (4 estimated wasted turns): The run repeatedly hit query_ideal/execute_ideal repair or status-error paths and did not recover cleanly.
- `tasks_mini/k-5-d-4/task_7.json` -> **Ideal repair/status-error loops** (4 estimated wasted turns): The run repeatedly hit query_ideal/execute_ideal repair or status-error paths and did not recover cleanly.
- `tasks_mini/k-7-d-4/task_1.json` -> **Ideal repair/status-error loops** (4 estimated wasted turns): The run repeatedly hit query_ideal/execute_ideal repair or status-error paths and did not recover cleanly.
- `tasks_mini/k-5-d-4/task_5.json` -> **Ideal repair/status-error loops** (3 estimated wasted turns): The run repeatedly hit query_ideal/execute_ideal repair or status-error paths and did not recover cleanly.
- `tasks_mini/k-4-d-4/task_2.json` -> **Ideal repair/status-error loops** (2 estimated wasted turns): The run repeatedly hit query_ideal/execute_ideal repair or status-error paths and did not recover cleanly.
- `tasks_mini/k-4-d-4/task_9.json` -> **Ideal repair/status-error loops** (1 estimated wasted turns): The run repeatedly hit query_ideal/execute_ideal repair or status-error paths and did not recover cleanly.
- `tasks_mini/k-4-d-4/task_5.json` -> **Budget exhausted after repeated same-hop work** (14 estimated wasted turns): The run spent late turns repeating, repairing, or re-querying one hop until timeout/tool budget stopped it.
- `tasks_mini/k-5-d-3/task_8.json` -> **Budget exhausted after repeated same-hop work** (12 estimated wasted turns): The run spent late turns repeating, repairing, or re-querying one hop until timeout/tool budget stopped it.
- `tasks_mini/k-5-d-4/task_3.json` -> **Budget exhausted after repeated same-hop work** (12 estimated wasted turns): The run spent late turns repeating, repairing, or re-querying one hop until timeout/tool budget stopped it.
- `tasks_mini/k-6-d-3/task_3.json` -> **Budget exhausted after repeated same-hop work** (12 estimated wasted turns): The run spent late turns repeating, repairing, or re-querying one hop until timeout/tool budget stopped it.
- `tasks_mini/k-5-d-3/task_7.json` -> **Budget exhausted after repeated same-hop work** (11 estimated wasted turns): The run spent late turns repeating, repairing, or re-querying one hop until timeout/tool budget stopped it.
- `tasks_mini/k-3-d-4/task_1.json` -> **Budget exhausted after repeated same-hop work** (4 estimated wasted turns): The run spent late turns repeating, repairing, or re-querying one hop until timeout/tool budget stopped it.
- `tasks_mini/k-5-d-3/task_10.json` -> **Budget exhausted after repeated same-hop work** (3 estimated wasted turns): The run spent late turns repeating, repairing, or re-querying one hop until timeout/tool budget stopped it.
- `tasks_mini/k-3-d-2/task_9.json` -> **Known-missing-data final submissions** (8 estimated wasted turns): The run recognized unresolved evidence gaps and submitted null, unknown, placeholder, or otherwise incomplete output.
- `tasks_mini/k-3-d-2/task_5.json` -> **Known-missing-data final submissions** (5 estimated wasted turns): The run recognized unresolved evidence gaps and submitted null, unknown, placeholder, or otherwise incomplete output.
- `tasks_mini/k-3-d-4/task_4.json` -> **Known-missing-data final submissions** (5 estimated wasted turns): The run recognized unresolved evidence gaps and submitted null, unknown, placeholder, or otherwise incomplete output.
- `tasks_mini/k-4-d-4/task_4.json` -> **Known-missing-data final submissions** (4 estimated wasted turns): The run recognized unresolved evidence gaps and submitted null, unknown, placeholder, or otherwise incomplete output.
- `tasks_mini/k-6-d-2/task_4.json` -> **Known-missing-data final submissions** (4 estimated wasted turns): Closest fit: the run had no hard budget stop and ended with an incomplete placeholder submission despite the needed totals being available.
- `tasks_mini/k-4-d-5/task_4.json` -> **Known-missing-data final submissions** (0 estimated wasted turns): The run recognized unresolved evidence gaps and submitted null, unknown, placeholder, or otherwise incomplete output.
- `tasks_mini/k-3-d-4/task_6.json` -> **Sandbox or source-access failures followed by fallback** (5 estimated wasted turns): The visible tail was dominated by file, sandbox, parsing, or source-access failures before a fallback answer.
- `tasks_mini/k-5-d-4/task_2.json` -> **Sandbox or source-access failures followed by fallback** (5 estimated wasted turns): The visible tail was dominated by file, sandbox, parsing, or source-access failures before a fallback answer.
- `tasks_mini/k-3-d-2/task_11.json` -> **Sandbox or source-access failures followed by fallback** (3 estimated wasted turns): The visible tail was dominated by file, sandbox, parsing, or source-access failures before a fallback answer.
- `tasks_mini/k-4-d-2/task_8.json` -> **Sandbox or source-access failures followed by fallback** (3 estimated wasted turns): The visible tail was dominated by file, sandbox, parsing, or source-access failures before a fallback answer.

## Global Summary

The dominant file-local pattern is not complete absence of planning. Most runs made early progress, then failed to transition cleanly after a difficult hop: either the agent stayed in ideal-tool repair/status-error loops, repeated one dataset until timeout/tool exhaustion, or submitted a known-incomplete answer after source/tool failures.

## Global Findings

- `Ideal repair/status-error loops` accounts for 16 trusted rows and 94 estimated wasted turns.
- `Budget exhausted after repeated same-hop work` accounts for 7 trusted rows and 68 estimated wasted turns.
- `Known-missing-data final submissions` accounts for 6 trusted rows and 26 estimated wasted turns.
- `Sandbox or source-access failures followed by fallback` accounts for 4 trusted rows and 16 estimated wasted turns.

## Unresolved Or Mixed Cases

- None.

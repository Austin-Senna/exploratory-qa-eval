# Ideal Maker

This note summarizes how the repo-local agent skills work together to create and validate ideal-mode artifacts:

- `$author-ideal-plans` builds the mirrored planning files used by `plan_ideal` and `search_ideal`.
- `$author-ideal-computations` adds executable/queryable computation records used by `execute_ideal` and `query_ideal`.
- `$plan-verifier` gates a finished plan against the original task reasoning so the ideal plan stays faithful without leaking answers.

The basic flow is:

1. Start from a source task under `tasks_mini`, `tasks_core`, or `tasks_core_quality`.
2. Create or repair the mirrored plan file under the matching `plans_mini` or `plans_core_quality` path.
3. Resolve `dataset_sequence`, `source_sequence`, and clean `reasoning_chain_text` for ideal planning/search.
4. Add `ideal_code` and `ideal_query` records only for executable computation nodes.
5. Run deterministic validators plus fresh semantic review subagents before accepting the artifact.

## Ideal Planning and Searching

Use `$author-ideal-plans` when a mirrored plan file needs to be created, rewritten, cleaned, or prepared for `plan_ideal` / `search_ideal`.

The skill always starts from the mirrored source task:

- `tasks_mini/.../task_*.json` -> `plans_mini/.../task_*.json`
- `tasks_core/.../task_*.json` -> `plans_mini/tasks_core/.../task_*.json`
- `tasks_core_quality/.../task_*.json` -> `plans_core_quality/.../task_*.json`

If the plan does not exist, initialize it with:

```bash
python .agents/skills/author-ideal-plans/scripts/init_plan_file.py tasks_mini/.../task_X.json
```

The initialized plan contains:

- `dataset_sequence`: unique datasets from task nodes in first-use order.
- `source_sequence`: one concrete source file per node/use, preserving repeated source uses.
- `reasoning_chain_text`: numbered scaffold steps for `plan_ideal`.
- `original_final_question`.
- `original_reasoning_chain`.

`dataset_sequence` drives the ideal plan's dataset order. It should contain each dataset once, in first-appearance node order. `datasets_used` is only a coverage check, not the ordering source of truth.

`source_sequence` is the retrieval source of truth for `search_ideal`. It should contain concrete dataset-relative file paths, one per node/source use, and repeated sources should stay repeated. The plan is unresolved if a source remains a bare dataset ID, cannot be verified, or is not indexed in `table_descriptions.jsonl`.

Source resolution should prefer, in order:

1. The node's `source` with a `.txt` version.
2. The original node `source`.
3. The `.json` version.
4. Normalized variants replacing `/v1/files/` with `/files/`.
5. Indexed paths in `table_descriptions.jsonl`.
6. Actual data-body files such as `files/data.txt`, when metadata is missing or ambiguous.

If a source cannot be verified, add `source_resolution_notes` and treat the plan as blocked until the choice is resolved.

`reasoning_chain_text` is prompt scaffolding, not a solved trace. It should tell `plan_ideal` what to retrieve, compare, filter, aggregate, or carry forward, while avoiding final answers and hidden intermediate discoveries. New or rewritten plans should store it as a JSON list of numbered strings.

Good reasoning-chain text:

- Preserves dataset order.
- Groups adjacent datasets when they support the same logical operation.
- Uses carry-forward wording such as "from the remaining counties" or "using the city identified earlier."
- Names places, entity types, years, or periods only when those details are already in the question or needed for clarity.
- Avoids raw paths, dataset slots, node IDs, hidden page titles, final answers, and solved intermediate entities.

Validate the plan with:

```bash
python .agents/skills/author-ideal-plans/scripts/check_plan_cleanliness.py plans_mini/.../task_X.json
```

The validator must return `clean`, and a fresh review subagent must also return `clean`, before the plan is ready for ideal planning/search.

## Ideal Query and Execution

Use `$author-ideal-computations` after the mirrored plan exists and its planning/search fields are clean. This skill only works on computation records; it does not rewrite `dataset_sequence`, `source_sequence`, or `reasoning_chain_text`.

Seed computation records from executable task-node facts:

```bash
.venv/bin/python .agents/skills/author-ideal-computations/scripts/seed_ideal_computation_records.py tasks_core/.../task_X.json --write
```

The seed script writes `ideal_code` records only for nodes whose `fact` parses as executable Python. It skips prose facts, including narrative Wikipedia hops.

For every executable computation node, the plan should eventually contain both:

- `ideal_code`: exact executable Python copied from the task node's `fact`.
- `ideal_query`: DuckDB SQL, or an explicit blocker record if SQL cannot run for that source.

The record contract is strict:

- `node_id` is the task node map key as a string.
- `dataset_id` is derived from the node source.
- `source` exactly matches the node source.
- `intent` exactly matches the node subquestion.
- `ideal_code.code` exactly preserves the node `fact`; do not normalize, add `print`, or rewrite imports.
- `ideal_query.sql` should be authored DuckDB SQL against table alias `t`.
- `answer` should match the node answer for runnable records.

Prose nodes must not receive computation records. If an executable node cannot receive runnable SQL because the source is unsupported by `query_file`, add a blocker `ideal_query` record. Blocker records omit `sql` and use an `answer` string that explains the execution blocker, for example a file-size guard or unsupported source type.

Before authoring SQL, read:

```text
.agents/skills/author-ideal-computations/references/sql-authoring-rubric.md
```

SQL should normally return one row with one column named `answer`, for example:

```sql
SELECT CAST(year AS VARCHAR) AS answer
FROM t
WHERE ...
```

Validate computation records with:

```bash
.venv/bin/python .agents/skills/author-ideal-computations/scripts/check_ideal_computation_records.py plans_mini/.../task_X.json
```

After SQL is authored, execute it live against the source:

```bash
.venv/bin/python .agents/skills/author-ideal-computations/scripts/check_ideal_computation_records.py plans_mini/.../task_X.json --execute-sql
```

The checker must return `clean` before the plan is ready for `computation_tool_mode=ideal`. If blocker records are intentional, the plan remains explicitly blocked until the query path supports that source or another handling path exists.

After local checks pass, run a fresh review subagent focused only on computation-record correctness: executable nodes have both record types, prose nodes have none, code is exact, SQL uses alias `t`, answers match, and blockers omit SQL.

## Plan Verification

Use `$plan-verifier` when a proposed ideal plan needs to be accepted, especially after rewriting `reasoning_chain_text` or changing `dataset_sequence` / `source_sequence`.

The verifier always checks a plan against its mirrored source task. It does not judge the plan in isolation.

Targets can be a single plan file or a directory/subtree:

```bash
python .agents/skills/plan-verifier/scripts/resolve_plan_targets.py plans_mini/.../task_X.json
python .agents/skills/plan-verifier/scripts/resolve_plan_targets.py plans_mini/k-2-d-4
```

For each target, run the objective verifier:

```bash
python .agents/skills/plan-verifier/scripts/verify_plan.py plans_mini/.../task_X.json
```

This gate checks:

- Author-plan cleanliness.
- Dataset coverage against the mirrored task.
- Whether the plan still expresses the same operation families as the original reasoning chain.

Then run a mandatory fresh semantic review subagent, even if the objective script fails. The reviewer should receive only sanitized context:

- Task question.
- Original reasoning chain with final-answer lines removed.
- Plan `dataset_sequence`.
- Plan `source_sequence`.
- Plan `reasoning_chain_text`.
- Verification rubric.

Do not give the reviewer the task final answer, task nodes, or solved-answer lines.

The semantic review rejects plans that:

- Leak the final answer.
- Leak intermediate discovered entity names.
- Leak computed numeric values.
- Reveal hidden dataset titles or page titles.
- Reveal downstream entities before they are retrieved.
- Collapse necessary narrowing, ranking, aggregation, comparison, or lookup steps.
- Let the agent skip a required retrieval step.

A plan is `clean` only when both gates are clean:

1. `verify_plan.py` returns clean.
2. The semantic reviewer returns clean.

Otherwise the verdict is `needs_revision`, with objective issues and semantic issues reported separately.

## How the Pieces Fit Together

`plan_ideal` depends on the clean plan scaffold:

- It uses `dataset_sequence` as the ordered list of datasets the agent is allowed to plan over.
- It uses `reasoning_chain_text` as safe, non-solved guidance for the retrieval/computation path.
- It should not receive leaked answers or hidden dataset/page titles.

`search_ideal` depends on source resolution:

- It uses `source_sequence` as the aligned retrieval source list.
- Repeated node uses stay repeated so retrieval remains aligned with the original task structure.
- Every source must resolve to a concrete indexed file path or the plan is blocked.

`execute_ideal` depends on `ideal_code`:

- It executes exact Python facts from executable task nodes.
- Exact preservation matters because the ideal record is meant to mirror the original task-node computation, not a cleaned-up replacement.

`query_ideal` depends on `ideal_query`:

- It executes authored DuckDB SQL against the same source file through table alias `t`.
- SQL records must produce the recorded answer under live execution.
- Unsupported query sources are represented as explicit blockers, not fake SQL.

The safe production order is:

1. Use `$author-ideal-plans` to create or repair the mirrored plan.
2. Validate planning/search fields with `check_plan_cleanliness.py`.
3. Use `$plan-verifier` to confirm the cleaned plan still matches the original task without leaks.
4. Use `$author-ideal-computations` to seed and author `ideal_code` / `ideal_query` records for executable nodes.
5. Validate computation records locally, execute SQL when present, and run independent computation review.
6. Accept the plan only when all required checks are clean, or mark it explicitly blocked with narrow blocker records/notes.


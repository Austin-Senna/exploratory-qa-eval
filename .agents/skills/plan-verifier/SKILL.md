---
name: plan-verifier
description: Verify whether a `plans_mini/.../task_*.json` plan still matches the original task reasoning chain without leaking answers or leaking enough intermediate information for the agent to skip steps. Use when Codex needs to review a proposed ideal-mode plan, gate a rewrite, or check that `dataset_sequence` and `reasoning_chain_text` remain faithful to the source task.
---

# Plan Verifier

## Rule #1: Verify Against the Mirrored Task

Review a plan file under `plans_mini/.../task_*.json` against the mirrored source task under `tasks_mini/.../task_*.json`.

`reasoning_chain_text` may appear either as:
- a legacy newline-delimited string
- a JSON list of numbered step strings

Normalize it before judging cleanliness or fidelity.

Do not verify the plan in isolation.

Read:
- the plan's `dataset_sequence`
- the plan's `reasoning_chain_text`
- the task's `question`
- the task's `reasoning_chain`
- the task's `datasets_used`
- the task's `nodes`

## Run the Objective Checks First

Run:

```bash
python .agents/skills/plan-verifier/scripts/verify_plan.py plans_mini/.../task_X.json
```

The script checks:
- plan cleanliness using the `author-ideal-plans` checker
- dataset coverage against the mirrored task
- whether the plan still expresses the same operation families as the original reasoning chain

Treat a nonzero exit status as a failed verification.

## Verify Fidelity To the Original Reasoning Chain

After the script, compare the plan to the original `reasoning_chain`.

Confirm all of the following:
1. The plan preserves the same overall retrieval path.
2. The plan does not remove an intermediate narrowing, intersection, ranking, aggregation, comparison, or lookup step that the original chain required.
3. The plan does not compress multiple source steps into wording that lets the agent jump directly to a downstream entity or final lookup.
4. The plan stays in the retrieval order required by `dataset_sequence`.

The plan may be cleaner than the original chain, but it must not become easier by revealing results the agent was supposed to derive.

## Reject Leak-Prone Plans

Reject the plan if it includes:
- the final answer
- intermediate discovered entity names that are not already in the question
- computed numeric values that the agent was supposed to derive
- solved intersections or comparisons
- wording that reveals the downstream entity before its retrieval step

Also reject plans that effectively skip steps, such as:
- jumping from an early filter directly to a final lookup
- naming the surviving city/county/person before the corresponding retrieval step
- collapsing year-by-year evidence gathering into one vague step when the original chain required multiple dataset-specific checks

## Use an Independent Review When Needed

If the plan is borderline, launch a fresh subagent and give it:
- the task question
- the original reasoning chain
- the plan's `dataset_sequence`
- the plan's `reasoning_chain_text`

Do not give it the final answer.

Use a prompt shaped like this:

```text
Use $plan-verifier at /absolute/path/to/plan-verifier to verify whether /absolute/path/to/plans_mini/.../task_X.json still matches the original reasoning chain without leaking answers or skip-step hints.

Return JSON only with:
- status: clean | needs_revision
- issues: [short strings]
- revision_notes: [short strings]

Check:
- fidelity to the original reasoning chain
- answer leakage
- intermediate-result leakage
- whether the plan wording lets the agent skip required steps

Do not solve the task.
Do not infer the final answer.
```

## Workflow Summary

1. Read the mirrored task and plan together.
2. Run `scripts/verify_plan.py`.
3. Compare the plan to the original `reasoning_chain` for skipped or collapsed logic.
4. Reject any plan that leaks answers or downstream entities.
5. Use an independent review subagent when the semantic match is unclear.

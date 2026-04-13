# Verification Rubric

## What This Skill Verifies

A plan passes only if all three are true:

1. It is faithful to the original task reasoning chain.
2. It does not leak answers or intermediate discovered results.
3. It does not make the task easier by allowing the agent to skip required steps.

## Objective Checks

`scripts/verify_plan.py` must pass.

It enforces:
- mirrored task lookup
- valid `dataset_sequence`
- plan cleanliness via `author-ideal-plans`
- same dataset coverage as the task, allowing reordering
- operation-family preservation checks

## Semantic Fidelity Checklist

Read the original `reasoning_chain` and ask:

- Does the plan preserve the same sequence of evidence gathering?
- Does the plan preserve the same narrowing logic?
- Does the plan preserve the same comparison or ranking logic?
- Does the plan preserve any required intermediate lookup before the final lookup?
- Does the final step still depend on the earlier steps, or has the dependency been leaked away?

## Leak Checklist

Reject the plan if it reveals:
- the final answer
- the intermediate surviving entity from a filter or intersection
- a computed count, average, sum, or comparison result
- a named downstream lookup target before its retrieval step

Examples:
- bad: `Find the capital of Vermont, then return the year Montpelier was chartered.`
- good: `Find the capital of the state that remains after intersecting the qualifying sets. Then return the year that capital city was chartered.`

## Skip-Step Hints

Reject the plan if it allows the agent to bypass retrieval:
- `Use the remaining county, Erie County, ...`
- `For the museum American Museum of Natural History, ...`
- `Compare Erie County and Westchester County and return the higher one.`

These leak intermediate results even if they are not the final answer.

## Operation Families

The verifier tracks these reasoning families:
- `filter_or_lookup`
- `intersection_or_narrowing`
- `comparison_or_ranking`
- `aggregation`

The cleaned plan may rewrite the wording, but it should still preserve the same operation families required by the original reasoning chain.

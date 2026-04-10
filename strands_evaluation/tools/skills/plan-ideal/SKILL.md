---
name: plan-ideal
description: Ideal-mode planning workflow using file-backed reasoning-chain context. Call `plan_ideal()` first, then produce a numbered execution plan. Copying chain steps is allowed, but improving clarity and executability is preferred.
---

## Rule #1: Call `plan_ideal` First

In ideal management mode, call `plan_ideal` as your first planning action.

It loads canonical planning context from `plans_mini` for the active task:
- `reasoning_chain_text`
- `dataset_sequence`

Do not skip this step.

## Build an Execution Plan From the Reasoning Chain

After `plan_ideal`, write a numbered execution plan.

Copying chain steps is allowed if they are already accurate.
Prefer improving each step with:
- concrete execution actions
- explicit verification/computation goals
- expected intermediate outputs

Keep the plan aligned with `dataset_sequence` order.

## Execution Expectations

For each step:
1. State what must be verified or computed.
2. Name the concrete tool/action type you will use.
3. Record the result needed to move to the next step.

If evidence conflicts with the chain assumptions, replan explicitly before continuing.

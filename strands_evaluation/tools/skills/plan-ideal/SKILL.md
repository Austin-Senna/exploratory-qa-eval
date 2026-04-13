---
name: plan-ideal
description: Ideal-mode planning workflow with the gold reasoning chain already loaded in the system prompt. Call `plan_ideal()` first to save a concise execution plan grounded in that chain.
---

## Rule #1: Call `plan_ideal` First

In ideal management mode, call `plan_ideal` as your first planning action.

The gold reasoning chain is already loaded in the system prompt at startup.
Use `plan_ideal()` to save your working execution plan before broad retrieval.

## Build an Execution Plan From the Reasoning Chain

Base the plan on the gold reasoning chain and keep its order intact.
Copy a chain step only when it is already the clearest wording.

## Execution Expectations

Prefer 4-8 short numbered steps.
Each step should name:
- what to verify or compute
- the main tool family
- the result needed to move on

Avoid long narrative, restating the whole question, or expanded prose about intermediate outputs.
If evidence conflicts with the chain assumptions, call `plan_ideal()` again with a short revised plan.

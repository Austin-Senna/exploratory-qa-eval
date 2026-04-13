---
name: plan-agent
description: Planning framework for compact execution plans on multi-hop data lake questions. ALWAYS load this skill before calling `plan()` or searching.
---

## Rule #1: Plan Before You Search

Call `plan()` as your **first action** on every new question. Do NOT call search tools until you have a saved plan.

A saved plan keeps search focused and reduces wasted tool calls.

## How to Decompose a Question

Make sure the plan covers the right reasoning phases when they matter. A compact plan can combine adjacent phases into one step.

1. **Entity resolution** — Translate question wording into official agency, program, geography, or person names.
   - "food stamps" -> SNAP
   - "unemployment" -> ETA / UI beneficiaries
   - city/state references may need a FIPS or official jurisdiction mapping

2. **Dataset discovery** — Say what dataset shape you need and how you will search for it.
   - Shape search queries as: `source/program + grain + metric + time`
   - Better: `Texas county prison admissions fiscal year`
   - Worse: `people entering prison system county`

Do not hallucinate dataset names.

### Plan Format

Write 4-8 short numbered steps.
Not every task needs all four reasoning phases as separate steps, but the plan should still account for them when relevant.
Each step should include:
- the goal
- the main tool family
- a concrete action or check

```
1. Find Khan Academy HQ city/state | use the available search tool for entity lookup
   -> else: reformulate with the official organization name or likely dataset title
2. Resolve state to FIPS code | grep_file on a lookup dataset
   -> else: use the available search tool to find a state FIPS lookup table
3. Count public schools by county in that state | query_file GROUP BY
4. If county-level data is missing, get the state total | query_file WHERE STFIP=...
   -> else: search for an alternative school dataset using the available search tools
```

For risky discovery steps, an inline fallback with `-> else:` is fine.
Avoid long narrative, restating the full question, or writing essay-style plans.
Do not write vague steps like "find relevant data" or "analyze the dataset."

---

## When to Replan

Call `plan()` again in any of these situations:

1. **Plan completed, answer not found** — You finished all sub-tasks (including fallbacks) but still can't answer the question. Summarize what you found, identify what's missing, and write a new plan targeting the gap.

2. **Before final extraction** — Once you've found the datasets and confirmed columns, save a focused 1-3 step plan for the exact query or read that yields the answer.

3. **Dead end — pivot to alternative info** — If the expected dataset does not exist, write a short replacement plan around a viable proxy or alternate source.

When replanning, focus only on the remaining gap.

---

## Search Reformulation (When Stuck)

Try these pivots in order:

1. **Lexical pivot** — Swap broad terms for agency/program names (e.g. "school count" -> "NCES public school locations")
2. **Granularity pivot** — Search state-level if county-level returns nothing; filter down in code
3. **Proxy pivot** — If the exact metric does not exist, find a standard proxy (e.g. "median income" for "poverty level")

---

## Context Cleanup

If you've made 10+ tool calls, call `summarize_context` before continuing. Write all findings into the summary — dataset IDs, column names, computed values, remaining gaps. This becomes your permanent memory after old messages are dropped.

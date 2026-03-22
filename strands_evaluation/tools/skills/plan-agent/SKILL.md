---
name: plan-agent
description: Planning framework for decomposing multi-hop data lake questions into ordered sub-tasks with search strategies
---

## When to Use This Skill

Activate this skill at the start of a complex multi-hop question before searching. Use it to decompose the question into concrete steps so you don't waste tool calls on dead ends.

---

## 4-Step Decomposition

Break the question into these phases:

1. **Entity resolution** — what government terms, program names, or geographic IDs are involved?
   - Example: "food stamps" → "SNAP"; "unemployment benefits" → "ETA / UI beneficiaries"; city name → look up county and state FIPS code
2. **Dataset discovery** — what distinct datasets are needed? For each, write a specific search query.
   - Example: "public school counts by county" → `search_sparse("public school locations NCES")`
3. **Relational mapping** — if combining datasets, identify the join key and confirm it exists in both
   - Example: "join on STFIP (state FIPS) and NMCNTY (county name)"
4. **Execution plan** — what specific operations yield the final answer?
   - Example: "GROUP BY county, COUNT(*), filter WHERE STFIP='06', take top 3"

Write out your plan as numbered sub-tasks before taking any search actions.

---

## Sub-Task Format

For each sub-task, specify:
- What information is needed
- Suggested search query or tool call
- Expected dataset type (Wikipedia article, NCES school data, census, economic, etc.)

Example:
```
1. Find the city/state of Khan Academy headquarters | search_sparse("Khan Academy") | Wikipedia
2. Look up the state FIPS code for California | grep_file on school district dataset | datagov NCES
3. Get top-3 counties by public school count in STFIP=06 | query_file GROUP BY county | datagov NCES
```

Keep plans to 3-5 sub-tasks. Do not hallucinate dataset names.

---

## When to Replan

Revise your plan when:
- You have completed 3+ sub-tasks and still haven't found a key dataset
- Search results don't match what you expected
- You have partial information and need to refocus on what's still missing

When replanning, summarize what you've found so far and identify the specific gap, then reformulate your remaining sub-tasks.

---

## Search Reformulation When Stuck

If a search returns poor results, try in order:
1. **Lexical pivot**: swap broad concept for agency/program term (e.g. "school count" → "NCES public school locations")
2. **Granularity pivot**: search state-level if county-level fails; filter in code
3. **Proxy pivot**: find a standard proxy metric if exact one is unavailable

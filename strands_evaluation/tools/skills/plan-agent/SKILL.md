---
name: plan-agent
description: Planning framework for decomposing multi-hop data lake questions into ordered sub-tasks with search strategies. ALWAYS load this skill first before calling plan() or any search tool. If you skip planning, you will waste tool calls on dead ends.
---

## Rule #1: Plan Before You Search

Call `plan()` as your **first action** on every new question. Do NOT call `search_value`, `search_schema`, or `search_prefix` until you have a saved plan.

A plan forces you to think about what you actually need before burning tool calls. Without one, you'll chase irrelevant datasets.

---

## How to Decompose a Question

Break it into 3-7 numbered sub-tasks across four phases:

1. **Entity resolution** — Translate the question's terms into government vocabulary.
   - "food stamps" -> SNAP; "unemployment" -> ETA / UI beneficiaries
   - City names -> county + state FIPS codes
   - If you don't know the official term, your first sub-task is a Wikipedia or search lookup.

2. **Dataset discovery** — For each dataset you need, write a specific search query.
   - Shape queries as: `source/program + grain + metric + time`
   - Better: `Texas county prison admissions fiscal year`
   - Worse: `people entering prison system county`

3. **Join mapping** — If combining datasets, name the join key and confirm it exists in both before querying.

4. **Extraction** — What SQL or code produces the final number?
   - Be specific: `GROUP BY county, COUNT(*), WHERE STFIP='06', top 3`

Keep plans to 3-7 sub-tasks. Do not hallucinate dataset names.

### Plan Format

Every sub-task MUST have a **goal** and a **tool**. For risky steps, add an inline fallback with `-> else:`.

```
1. Find Khan Academy HQ city/state | search_value("Khan Academy")
     -> else: search_prefix("khan-academy")
2. Resolve state to FIPS code | grep_file on NCES dataset
     -> else: search_value("state FIPS codes") for a lookup table
3. Count public schools by county in that state | query_file GROUP BY
4. If county-level data missing, get state total | query_file WHERE STFIP=...
     -> else: search for alternative school dataset via search_schema("school")
```

Do not write vague sub-tasks like "find relevant data" — name what you're looking for and which tool gets it. Fallbacks are optional but recommended for discovery steps where the first search may miss.

---

## When to Replan

Call `plan()` again in any of these situations:

1. **Plan completed, answer not found** — You finished all sub-tasks (including fallbacks) but still can't answer the question. Summarize what you found, identify what's missing, and write a new plan targeting the gap.

2. **Before final extraction** — Once you've found your datasets and confirmed columns, replan as a sanity check. Write a focused 1-2 step plan for the exact query/code that produces the final answer. This catches misaligned assumptions before you burn your last tool calls.

3. **Dead end — pivot to alternative info** — The dataset you need doesn't seem to exist and your inline fallbacks are exhausted. Instead of repeating failed searches, replan around alternative information. Ask: "What *other* data could answer this question indirectly?" Then write sub-tasks to find that instead.

When replanning: summarize what you've found so far, name the specific gap, then write new sub-tasks for the gap only.

---

## Search Reformulation (When Stuck)

Try these pivots in order:

1. **Lexical pivot** — Swap broad terms for agency/program names (e.g. "school count" -> "NCES public school locations")
2. **Granularity pivot** — Search state-level if county-level returns nothing; filter down in code
3. **Proxy pivot** — If the exact metric doesn't exist, find a standard proxy (e.g. "median income" for "poverty level")

---

## Context Cleanup

If you've made 10+ tool calls, call `summarize_context` before continuing. Write all findings into the summary — dataset IDs, column names, computed values, remaining gaps. This becomes your permanent memory after old messages are dropped.

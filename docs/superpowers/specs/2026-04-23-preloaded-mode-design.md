# Preloaded-Sources Mode Design

**Date:** 2026-04-23
**Context:** Supporting the revised paper framing: *given that the agent is told exactly which datasets are needed, where does it still fail?*

---

## 1. Motivation

Prior LAKEQA analysis established search as the dominant bottleneck for exploratory QA agents. Rather than comparing alternative search or planning interventions, the revised paper asks a cleaner question: **if retrieval is solved, what remains?**

The cleanest experimental realization of "retrieval is solved" is not a better search tool, but no search at all: the agent is handed the gold `source_sequence` (URIs + `dataset_id`) directly in its system prompt, told the list is authoritative, and given no search tools. Any remaining failures are then unambiguously downstream of retrieval — file-reading, query construction, code execution, or final-answer reasoning.

The existing `search_ideal` mode does not serve this thesis. It still forces the agent through a search loop (pick query, pick `top_k`, decide when to stop), reintroducing the variable we intend to factor out. A new mode — `preloaded` — is needed.

## 2. Scope

**In scope:**
- A new value `preloaded` on the `search_tool` axis of the existing mode system.
- Injection of `source_sequence` into the system prompt as a `## PRELOADED DATASETS` block containing `dataset_id` and URI only.
- An authoritative-list instruction telling the agent it has the complete set and should not search.
- A new `prompts/search_preloaded.txt` overlay describing the no-search regime.
- Skills selection that omits `discover-data` when `search_tool=preloaded` (keeps `plan-*` and `query-data`).
- `submit_answer` tracing in `TracePlugin` (the one instrumentation gap — everything else for failure attribution is already captured).
- An analysis helper that classifies task failures into four categories using existing trace + `agent_results.jsonl` data.

**Out of scope:**
- Removing the existing `search_ideal` implementation (unused by this paper but not hurting anything; separate cleanup).
- Changes to `search_results` semantics — it becomes a no-op when `search_tool=preloaded`.
- Prompt optimization (hand-written, structure-matched prompts remain acceptable; noted in paper limitations).
- New analysis plots; existing analysis scripts key off variant labels and will pick up the new variant automatically.

## 3. Experimental design (paper Section 2.3, revised)

The paper runs two conditions, both using the `preloaded` source mode:

| Condition | Preloaded URIs | Planning toolkit |
|---|---|---|
| **Oracle-Sources** | ✅ | ❌ (basic prompting) |
| **Oracle-Sources + Planning** | ✅ | ✅ (plan tool, skills plugin, summarize_context, loop nudge) |

**Oracle-Sources** isolates downstream reasoning capability. **Oracle-Sources + Planning** tests whether planning scaffolding recovers failures from the first condition or whether those failures are intrinsic to tabular reasoning.

The published LAKEQA baseline (ontology keyword search, basic prompting) is reported for reference, not rerun.

## 4. Failure attribution

All inputs required for failure attribution are already captured by existing instrumentation:

- `ReadTracePlugin` sidecar → per-task `read_dataset_ids` and `gold_dataset_ids_read`
- Strands `AgentResult.tool_metrics` → per-tool `call_count` and `success_count` (written to `agent_results.jsonl` as `tool_counts` and aggregated by `analysis/tool_error_analysis.py`)
- Task result → final `submit_answer` text (compared to gold in EM evaluation)

Under the preloaded mode, failure attribution uses four mutually exclusive, exhaustive categories ordered by first-matching-wins:

| Category | Detection |
|---|---|
| didn't-open | Any gold URI absent from the union of `read_dataset_ids` across the task |
| read-tool-error | All gold URIs opened, but any read tool (`peek_file`, `query_file`, `read_file`, `grep_file`) has `success_count < call_count` for this task |
| execute-error | All read tools clean, but `execute_code` has `success_count < call_count` for this task |
| wrong-answer | All tools clean, but the `submit_answer` text does not match the gold answer |

`read-tool-error` intentionally does not split into wrong-format vs. wrong-query — that split would require per-call error-text capture the current instrumentation does not provide. If the aggregate rate of read errors is high enough to matter, the split can be added in a follow-up; for now the aggregate is sufficient to answer the paper's question.

The only instrumentation change required to make all four derivable is ensuring `submit_answer` is wired into the trace (see §5.4) — everything else is already recorded.

## 5. Architecture

### 5.1 Mode-system extension (`agent_with_mode.py`, `helper/prompting.py`)

- Add `preloaded` to `_MODES` in both `agent_with_mode.py` and `helper/prompting.py`.
- In `_build_search_tools`, `search_mode == "preloaded"` returns `[]`.
- In `_build_management`, after composing the base prompt, if `search_tool_mode == "preloaded"`:
  - Load the task's plan via the existing `plan_store.load_plan_for_context` helper.
  - Hard-fail if the plan is missing or lacks a non-empty `source_sequence`.
  - Append the `## PRELOADED DATASETS` block to the prompt.
- `search_results` mode is ignored when `search_tool=preloaded` (the payload wrapper has no search tools to wrap).

### 5.2 Skills selection (`helper/prompting.py`)

Skills are currently selected via `skill_paths_for_modes(search_tool_mode, agent_management_mode)` which returns three paths: `plan-*`, `discover-data-*`, and `query-data`.

For `search_tool_mode == "preloaded"`:
- Omit the `discover-data-*` skill entirely. There are no datasets to discover; the URIs are preloaded. Carrying a discover-data skill would only inject obsolete search-tool guidance.
- Keep `query-data` (the agent still queries files).
- Keep the `plan-*` skill selection as-is (controlled by `agent_management_mode`; under `preloaded × naive` it is omitted because skills are disabled, under `preloaded × standard` it is included).

Implementation: `skill_paths_for_modes` branches on `search_tool_mode == "preloaded"` and returns `[planning_skill_path(...), _QUERY_DATA_SKILL]` — dropping the discover entry.

### 5.3 Prompt overlay

The existing pattern uses `prompts/search_{mode}.txt` overlays loaded by `_compose_search_overlay_prompt`. Add `prompts/search_preloaded.txt` with content describing the preloaded regime: no search tools exist, a `## PRELOADED DATASETS` block at the top of the prompt lists all required URIs, and the agent should proceed directly to `peek_file` / `query_file` on those URIs. The per-task URI block itself is injected separately (§5.4) because URIs are task-specific, not prompt-template-level.

### 5.4 Per-task URI injection

A new helper `compose_preloaded_prompt(source_sequence)` emits:

```
## PRELOADED DATASETS

You have been given the complete set of datasets required to answer this
task. Do not search. Proceed directly to inspect and query the files
listed below using the available data tools.

- dataset_id: <id_0> | uri: <source_0>
- dataset_id: <id_1> | uri: <source_1>
...
```

The block is appended to whatever base prompt `_build_management` has already produced. Each line in the block is derived from one URI in `source_sequence`. The `dataset_id` is extracted from the URI path (for Data.gov URIs of shape `datagov/<slug>/files/<name>`, the slug is the `dataset_id`; extraction is delegated to the existing `_normalize_dataset_id` helper in `trace_plugin.py` to keep canonical form consistent with the trace fields). This makes the composer robust to any length mismatch between `dataset_sequence` and `source_sequence` — only `source_sequence` is required.

Inside `_build_management`, when `search_tool_mode == "preloaded"`, a helper `compose_preloaded_block(source_sequence) -> str` produces the `## PRELOADED DATASETS` block and is appended to whatever base prompt was produced. See §5.6 for the exact block format.

### 5.5 CLI surface (`run_mode_eval.py`)

- `--search_tool preloaded` becomes a valid value.
- Variant label format gains `p` as a `search_tool` slot character: `search_p_results_{n|i}_plan_{n|d|i}`.
- Because `search_results` is inert under `preloaded`, the label still reflects the configured value for traceability.

### 5.6 Preloaded-block format

```
## PRELOADED DATASETS

You have been given the complete set of datasets required to answer this
task. Do not search. Proceed directly to inspect and query the files
listed below using the available data tools.

- dataset_id: <id_0> | uri: <source_0>
- dataset_id: <id_1> | uri: <source_1>
...
```

Each line in the block is derived from one URI in `source_sequence`. The `dataset_id` is extracted from the URI path (for Data.gov URIs of shape `datagov/<slug>/files/<name>`, the slug is the `dataset_id`; extraction is delegated to the existing `_normalize_dataset_id` helper in `trace_plugin.py` to keep canonical form consistent with the trace fields). This makes the composer robust to any length mismatch between `dataset_sequence` and `source_sequence` — only `source_sequence` is required.

### 5.7 Instrumentation extension (`trace_plugin.py`)

The only gap in existing instrumentation is `submit_answer` tracing. The class docstring claims it is supported, but `on_after_tool` has no branch for it.

Extend `TracePlugin.on_after_tool` with a `submit_answer` branch that writes:

```
{
  "task_id": ...,
  "tool": "submit_answer",
  "answer_text": <input answer>,
  "timestamp_ms": ...
}
```

Consumers distinguish by `tool` field — no schema change for existing records. All other data required for failure attribution (per-tool error counts, read dataset IDs) is already recorded.

### 5.8 Analysis helper (`analysis/failure_attribution.py`)

A new module that takes, for a task:

- the per-task read-trace sidecar
- the per-task row from `agent_results.jsonl` (for `tool_counts`)
- the gold task (for URIs and gold answer)

Returns a single category label per task by applying the four rules in §4 first-matching-wins. Exposes `classify_task(...) -> str` and `summarize_run(results_dir, tasks_dir) -> dict` returning category counts per condition × model.

## 6. Data flow

```
plans_mini/k-*-d-*/task_*.json
        │
        ▼ load_plan_for_context
source_sequence
        │
        ▼ compose_preloaded_block + prompts/search_preloaded.txt overlay
system prompt with no search tools + ## PRELOADED DATASETS block
        │
        ▼ skill_paths_for_modes → [plan-*, query-data]  (discover-data omitted)
        │
        ▼ agent.run(prompt, tools=[data_tools + management_tools])
agent uses peek_file / query_file / execute_code / submit_answer
        │
        ▼ ReadTracePlugin + TracePlugin (extended with submit_answer)
        │   + agent_results.jsonl (tool_counts per task)
        │
        ▼ analysis/failure_attribution.py
{didn't-open | read-tool-error | execute-error | wrong-answer}
```

## 7. Testing

- **Unit:** `search_tool=preloaded` returns empty search-tool list; prompt contains expected URIs and `dataset_id`s and the authoritative-list instruction; missing plan hard-fails.
- **Unit:** `skill_paths_for_modes(search_tool_mode="preloaded", ...)` returns paths containing `plan-*` and `query-data` but never a `discover-data-*` entry.
- **Unit:** `TracePlugin` `submit_answer` branch writes a record with `tool="submit_answer"` and `answer_text` populated.
- **Unit:** `failure_attribution.classify_task` returns the correct label on fixture traces covering each of the four categories.
- **Integration:** 5-task Haiku smoke run with `--search_tool preloaded --agent_management naive` confirms the agent never invokes a search tool (none exist), opens the preloaded URIs via `peek_file`/`query_file`, and produces a `submit_answer` record in the trace.

## 8. Validation and execution

Post-landing:

1. 5-task smoke run (Haiku, `preloaded × naive`).
2. Full 135-task run per model × management-mode cell for the paper's main table:
   - Haiku × naive, Haiku × standard
   - Sonnet × naive, Sonnet × standard
   - (GPT-5-mini, Llama-3.3-70B follow if budget allows)
3. Run `failure_attribution.summarize_run` on each output directory to produce the stacked-bar input for paper §3.2.

## 9. Open risks

- **Saturation risk.** If preloaded URIs push EM to near-ceiling, the paper's finding degenerates to "retrieval was the only bottleneck." Mitigation: prior `search_ideal` results provide a signal on expected ceiling; if EM saturates, pivot narrative to "retrieval + reasoning jointly, and retrieval dominates."
- **Wrong-query classification heuristic.** Separating wrong-query from wrong-final-answer requires reasoning-chain matching that may be brittle. Mitigation: manual spot-check on a 20-task sample; paper reports inter-rater agreement if needed.
- **Distribution shift in prompt shape.** Agents trained with search-tool loops may behave oddly when no search tools exist. Mitigation: the authoritative-list instruction explicitly sets expectations; smoke run validates behavior before full runs.

## 10. Decisions locked in

- Mode name: `preloaded`
- Block content: `dataset_id` + URI only (no description, schema, or snippet)
- Agent is told the set is complete ("Do not search")
- `discover-data` skill is omitted under `preloaded`; `query-data` and `plan-*` remain
- `prompts/search_preloaded.txt` is added alongside the existing mode overlays
- Failure attribution uses four categories; per-call error-text capture is deferred
- Only instrumentation change in this workstream is `submit_answer` tracing
- Existing `search_ideal` stays (unused, not removed)

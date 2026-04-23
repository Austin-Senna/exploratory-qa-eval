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
- Extension of sidecar instrumentation to support failure attribution (tool input, success/error status, error text, `submit_answer` tracing).
- An analysis helper that classifies task failures into five categories from the enriched trace.

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

Under the preloaded mode, failure attribution collapses to five mutually exclusive, exhaustive categories:

| Category | Detection |
|---|---|
| didn't-open | Gold URI present in preloaded list but absent from union of `read_dataset_ids` across the task |
| wrong-format | A read tool returned a format-unsupported error for a gold URI (detected from tool `status` + `error_text`) |
| wrong-query | A read tool executed (status=success) but returned data inconsistent with the gold reasoning chain — detected by the absence of successful `query_file`/`grep_file` calls producing values the reasoning chain implies |
| execution-error | `execute_code` returned a non-zero status or exception |
| wrong-final-answer | All retrieval/execution succeeded but the `submit_answer` text does not match the gold answer |

The first two are derivable from trace metadata. The third is heuristic; the spec permits manual review of uncertain cases. The last two are deterministic once `submit_answer` is traced.

## 5. Architecture

### 5.1 Mode-system extension (`agent_with_mode.py`)

- Add `preloaded` to `_MODES` for the `search_tool` axis.
- In `_build_search_tools`, `search_mode == "preloaded"` returns `[]`.
- In `_build_management`, after composing the base prompt, if `search_tool_mode == "preloaded"`:
  - Load the task's plan via the existing `plan_store.load_plan_for_context` helper.
  - Hard-fail if the plan is missing or lacks a non-empty `source_sequence`.
  - Append the `## PRELOADED DATASETS` block to the prompt.
- `search_results` mode is ignored when `search_tool=preloaded` (the payload wrapper has no search tools to wrap).

### 5.2 Prompt composer

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

### 5.3 CLI surface (`run_mode_eval.py`)

- `--search_tool preloaded` becomes a valid value.
- Variant label format gains `p` as a `search_tool` slot character: `search_p_results_{n|i}_plan_{n|d|i}`.
- Because `search_results` is inert under `preloaded`, the label still reflects the configured value for traceability.

### 5.4 Instrumentation extension (`read_trace_plugin.py`, `trace_plugin.py`)

Extend the per-call record written by `ReadTracePlugin.on_after_tool` to include:

| Field | Source | Purpose |
|---|---|---|
| `tool_input` | `event.tool_use["input"]` (full, truncated to 4 KB) | Captures SQL for `query_file`, pattern for `grep_file`, code for any embedded snippet |
| `status` | `event.result.get("status")` (`"success"` or `"error"`) | Enables error-vs-success classification |
| `error_text` | first text block of `event.result["content"]` if `status=error`, truncated to 2 KB | Enables format-error vs execution-error classification |

Extend `TracePlugin` to handle `submit_answer`:

- On `submit_answer` calls, log `task_id`, `tool="submit_answer"`, `answer_text` (the input), `timestamp_ms`.
- Matches the existing search-tool record shape; consumers distinguish by `tool` field.

### 5.5 Analysis helper (`analysis/failure_attribution.py`)

A new module that takes a sidecar trace file + a gold task and returns a single category label per task. Implementation notes:

- Reads sidecar JSONL once; builds in-memory lists of read-tool calls, `submit_answer` call, and final-answer text.
- Applies the five rules in the order listed in §4 (first-matching-wins).
- Exposes a `classify_task(trace_path, gold_task) -> str` function and a `summarize_run(trace_dir, tasks) -> dict` helper returning category counts.

## 6. Data flow

```
plans_mini/k-*-d-*/task_*.json
        │
        ▼ load_plan_for_context
source_sequence, dataset_sequence
        │
        ▼ compose_preloaded_prompt
system prompt with ## PRELOADED DATASETS block
        │
        ▼ agent.run(prompt, tools=[data_tools + management_tools])
agent uses peek_file / query_file / execute_code / submit_answer
        │
        ▼ ReadTracePlugin + TracePlugin (extended)
sidecar JSONL with tool_input, status, error_text, submit_answer
        │
        ▼ analysis/failure_attribution.py
{didn't-open | wrong-format | wrong-query | execution-error | wrong-final-answer}
```

## 7. Testing

- **Unit:** `search_tool=preloaded` returns empty search-tool list; prompt contains expected URIs and `dataset_id`s and the authoritative-list instruction; missing plan hard-fails.
- **Unit:** extended `ReadTracePlugin` record includes `tool_input`, `status`, `error_text` on both success and error paths; `submit_answer` trace records appear in JSONL.
- **Unit:** `failure_attribution.classify_task` returns the correct label on fixture traces covering each of the five categories.
- **Integration:** 5-task Haiku smoke run with `--search_tool preloaded --agent_management naive` confirms the agent never invokes a search tool (none exist), opens the preloaded URIs via `peek_file`/`query_file`, and produces a `submit_answer` traced in the sidecar.

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
- Sidecar extension is part of this workstream, not a follow-up
- Existing `search_ideal` stays (unused, not removed)

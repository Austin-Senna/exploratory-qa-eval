# SANA Sprint Turn-Waste Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Tighten SANA sprint runtime control to reduce redundant verification, renewal churn, unnecessary source switches, and terminal lookup stalls.

**Architecture:** Extend the existing `sprint` schema and `SprintSteerHandler` rather than adding a new mode. Source packages remain represented by `SourceSessionState`, with related-source membership and a small final-budget state machine owned by the steering plugin.

**Tech Stack:** Python, Strands plugin hooks, `pytest`, existing `sana_evaluation` unit tests.

---

### Task 1: Cadence Settled Facts

**Files:**
- Modify: `sana_evaluation/tools/sprint_tool.py`
- Modify: `sana_evaluation/prompts/sprint.py`
- Test: `sana_evaluation/tests/test_sprint_tool.py`
- Test: `sana_evaluation/tests/test_plugins.py`
- Test: `sana_evaluation/tests/test_prompts.py`

- [x] **Step 1: Write failing tests**

Add assertions that cadence records reject missing `settled_facts`, accept `settled_facts=[]`, persist `settled_facts`, and prompt text mentions settled facts as non-recheck memory.

- [x] **Step 2: Verify red**

Run: `uv run python -m pytest sana_evaluation/tests/test_sprint_tool.py sana_evaluation/tests/test_plugins.py sana_evaluation/tests/test_prompts.py -q`

Expected: failures mention missing `settled_facts` support.

- [x] **Step 3: Implement schema and prompt**

Add optional parameter `settled_facts: Optional[List[str]] = None`, include it in the record, require it for cadence, validate it is a list, and render it in `## CURRENT SPRINT`. Update cadence prompt and guide reason to request it.

- [x] **Step 4: Verify green**

Run: `uv run python -m pytest sana_evaluation/tests/test_sprint_tool.py sana_evaluation/tests/test_plugins.py sana_evaluation/tests/test_prompts.py -q`

Expected: all selected tests pass.

### Task 2: Related Source Packages

**Files:**
- Modify: `sana_evaluation/plugins/source_session.py`
- Modify: `sana_evaluation/tools/sprint_tool.py`
- Modify: `sana_evaluation/plugins/sprint_plugin.py`
- Modify: `sana_evaluation/prompts/sprint.py`
- Test: `sana_evaluation/tests/test_source_session.py`
- Test: `sana_evaluation/tests/test_sprint_tool.py`
- Test: `sana_evaluation/tests/test_plugins.py`
- Test: `sana_evaluation/tests/test_prompts.py`

- [x] **Step 1: Write failing tests**

Add tests for storing `related_sources`, package membership, related-source calls sharing budget, related sources avoiding switch contracts, and outside-package sources still triggering switch contracts.

- [x] **Step 2: Verify red**

Run: `uv run python -m pytest sana_evaluation/tests/test_source_session.py sana_evaluation/tests/test_sprint_tool.py sana_evaluation/tests/test_plugins.py sana_evaluation/tests/test_prompts.py -q`

Expected: failures mention `related_sources` support or source-switch behavior.

- [x] **Step 3: Implement package behavior**

Store `related_sources` on `SourceSessionState`, add `contains_source(source)`, and update `SprintSteerHandler` to compare requested sources against package membership.

- [x] **Step 4: Verify green**

Run: `uv run python -m pytest sana_evaluation/tests/test_source_session.py sana_evaluation/tests/test_sprint_tool.py sana_evaluation/tests/test_plugins.py sana_evaluation/tests/test_prompts.py -q`

Expected: all selected tests pass.

### Task 3: Renewal Evidence

**Files:**
- Modify: `sana_evaluation/tools/sprint_tool.py`
- Modify: `sana_evaluation/plugins/sprint_plugin.py`
- Modify: `sana_evaluation/prompts/sprint.py`
- Test: `sana_evaluation/tests/test_sprint_tool.py`
- Test: `sana_evaluation/tests/test_plugins.py`
- Test: `sana_evaluation/tests/test_prompts.py`

- [x] **Step 1: Write failing tests**

Add tests that renewal contracts require `evidence_gained` and `remaining_gap`, while first contracts and source-switch contracts do not.

- [x] **Step 2: Verify red**

Run: `uv run python -m pytest sana_evaluation/tests/test_sprint_tool.py sana_evaluation/tests/test_plugins.py sana_evaluation/tests/test_prompts.py -q`

Expected: failures mention renewal evidence validation.

- [x] **Step 3: Implement renewal validation**

Track renewal pending state in `SprintState`, set it when budget exhaustion triggers a contract, require evidence/gap only for renewal contracts, and persist the fields when provided.

- [x] **Step 4: Verify green**

Run: `uv run python -m pytest sana_evaluation/tests/test_sprint_tool.py sana_evaluation/tests/test_plugins.py sana_evaluation/tests/test_prompts.py -q`

Expected: all selected tests pass.

### Task 4: Final-Budget Gate

**Files:**
- Modify: `sana_evaluation/plugins/sprint_plugin.py`
- Test: `sana_evaluation/tests/test_plugins.py`

- [x] **Step 1: Write failing tests**

Add tests that final-budget gating overrides cadence and commitment gates, allows one arbitrary data/source tool after the warning, then blocks data/source tools while allowing `submit_answer`.

- [x] **Step 2: Verify red**

Run: `uv run python -m pytest sana_evaluation/tests/test_plugins.py -q`

Expected: failures mention final-budget behavior.

- [x] **Step 3: Implement final-budget state machine**

Track counted tool calls, derive `tool_calls_left`, warn at `<= 2`, allow one final non-admin tool, lock further non-admin tools, and keep `submit_answer` plus admin tools allowed.

- [x] **Step 4: Verify green**

Run: `uv run python -m pytest sana_evaluation/tests/test_plugins.py -q`

Expected: plugin tests pass.

### Task 5: Full Verification

**Files:**
- Modify: no new files unless verification reveals a targeted fix.

- [x] **Step 1: Run focused SANA suite**

Run: `uv run python -m pytest sana_evaluation/tests/test_flags.py sana_evaluation/tests/test_prompts.py sana_evaluation/tests/test_sprint_tool.py sana_evaluation/tests/test_plugins.py sana_evaluation/tests/test_source_session.py -q`

Expected: all selected tests pass.

- [x] **Step 2: Inspect git diff**

Run: `git diff -- sana_evaluation docs/superpowers/plans/2026-05-08-sana-sprint-turn-waste-fixes.md`

Expected: only planned files changed.

- [x] **Step 3: Commit implementation**

Run:

```bash
git add docs/superpowers/plans/2026-05-08-sana-sprint-turn-waste-fixes.md sana_evaluation
git commit -m "Implement SANA sprint turn-waste controls"
```

Expected: one implementation commit on `codex/sana-sprint-turn-waste-fixes`.

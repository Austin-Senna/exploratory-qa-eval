# Short Plan Source Budget Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `short_plan` mode axis so SANA can compare fixed-cadence reflection against source-budget-contract reflection for multi-turn dataset commitments.

**Architecture:** Keep `short_plan` as one SANA primitive, controlled by `SanaFlags.short_plan`, and add `SanaFlags.short_plan_mode` with `cadence` and `source_budget`. The existing `ShortPlanSteerHandler` remains the runtime owner; it delegates source extraction/session bookkeeping to a new small helper module and branches internally between cadence and source-budget steering.

**Tech Stack:** Python dataclasses, Strands `SteeringHandler` / `Guide` / `Proceed`, pytest, existing `sana_evaluation` plugin and prompt modules.

---

## File Structure

- Modify `sana_evaluation/flags.py`
  - Add valid short-plan modes.
  - Add `short_plan_mode` and `source_budget_calls` fields.
  - Validate mode and source-budget call count.

- Modify `sana_evaluation/run_sana_eval.py`
  - Add `--short-plan-mode {cadence,source_budget}`.
  - Add `--source-budget-calls`.
  - Include short-plan mode in condition labels when `short_plan` is active.

- Modify `sana_evaluation/sana_config.py`
  - No new fields are required if all values live inside `SanaFlags`.

- Modify `sana_evaluation/sana_bundle.py`
  - Pass `short_plan_mode` and `source_budget_calls` into `short_plan_block()` and `ShortPlanSteerHandler`.

- Modify `sana_evaluation/prompts/short_plan.py`
  - Render different instructions for `cadence` and `source_budget`.
  - Keep the state-of-task readout bundled into reflection.

- Create `sana_evaluation/plugins/source_session.py`
  - Own source-id extraction from tool calls.
  - Own source-session dataclasses and budget state.
  - Keep this independent from Strands so it can be unit tested without async hooks.

- Modify `sana_evaluation/plugins/short_plan_plugin.py`
  - Preserve existing cadence behavior.
  - Add source-budget contract and source-session reflection flow.
  - Include source-session state in `describe_for_dashboard()`.

- Modify `sana_evaluation/tests/test_flags.py`
  - Cover mode validation and source-budget validation.

- Modify `sana_evaluation/tests/test_prompts.py`
  - Cover cadence prompt and source-budget prompt separately.

- Modify `sana_evaluation/tests/test_plugins.py`
  - Keep current cadence tests.
  - Add source-budget tests for contract, budget exhaustion, source switch, and dashboard text.

- Create `sana_evaluation/tests/test_source_session.py`
  - Test source extraction and session bookkeeping directly.

---

### Task 1: Add Short-Plan Mode Configuration

**Files:**
- Modify: `sana_evaluation/flags.py`
- Modify: `sana_evaluation/run_sana_eval.py`
- Test: `sana_evaluation/tests/test_flags.py`

- [ ] **Step 1: Write failing tests for mode defaults and validation**

Add these tests to `sana_evaluation/tests/test_flags.py`:

```python
def test_short_plan_mode_defaults_to_cadence() -> None:
    flags = SanaFlags(short_plan=True)
    assert flags.short_plan_mode == "cadence"
    assert flags.source_budget_calls == 3


def test_short_plan_accepts_source_budget_mode() -> None:
    flags = SanaFlags.from_feature_names(
        ["short_plan"],
        short_plan_mode="source_budget",
        source_budget_calls=4,
    )
    assert flags.short_plan is True
    assert flags.short_plan_mode == "source_budget"
    assert flags.source_budget_calls == 4
    flags.validate(agent_management="standard")


def test_short_plan_rejects_unknown_mode() -> None:
    flags = SanaFlags(short_plan=True, short_plan_mode="bogus")
    with pytest.raises(ValueError, match="short_plan_mode"):
        flags.validate(agent_management="standard")


def test_source_budget_calls_must_be_positive() -> None:
    flags = SanaFlags(short_plan=True, short_plan_mode="source_budget", source_budget_calls=0)
    with pytest.raises(ValueError, match="source_budget_calls"):
        flags.validate(agent_management="standard")
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
.venv/bin/python -m pytest sana_evaluation/tests/test_flags.py -q
```

Expected: tests fail because `SanaFlags` does not yet accept `short_plan_mode`, `source_budget_calls`, or the new `from_feature_names()` keyword arguments.

- [ ] **Step 3: Implement `SanaFlags` fields and validation**

In `sana_evaluation/flags.py`, add:

```python
_VALID_SHORT_PLAN_MODES = {"cadence", "source_budget"}
```

Update the dataclass fields:

```python
short_plan: bool = False
CoT: bool = False
results_apis: bool = False

macro_reflection_k: int = 5
short_plan_mode: str = "cadence"
source_budget_calls: int = 3
```

Update `validate()`:

```python
if self.short_plan_mode not in _VALID_SHORT_PLAN_MODES:
    raise ValueError(
        f"short_plan_mode must be one of {sorted(_VALID_SHORT_PLAN_MODES)}; "
        f"got {self.short_plan_mode!r}."
    )
if self.source_budget_calls <= 0:
    raise ValueError(
        f"source_budget_calls must be > 0; got {self.source_budget_calls}."
    )
```

Update `from_feature_names()` signature:

```python
def from_feature_names(
    cls,
    feature_names: Iterable[str],
    *,
    macro_reflection_k: int = 5,
    short_plan_mode: str = "cadence",
    source_budget_calls: int = 3,
) -> "SanaFlags":
```

Update its constructor call:

```python
return cls(
    macro_reflection_k=macro_reflection_k,
    short_plan_mode=short_plan_mode,
    source_budget_calls=source_budget_calls,
    **kwargs,
)
```

- [ ] **Step 4: Run flag tests**

Run:

```bash
.venv/bin/python -m pytest sana_evaluation/tests/test_flags.py -q
```

Expected: all `test_flags.py` tests pass.

- [ ] **Step 5: Add CLI arguments and condition labels**

In `sana_evaluation/run_sana_eval.py`, add mode labels near `_SANA_FEATURE_LETTERS`:

```python
_SHORT_PLAN_MODE_LETTERS = {
    "cadence": "spc",
    "source_budget": "spsb",
}
```

In `_variant_condition_label()`, replace the `short_plan` feature letter handling with explicit mode handling:

```python
sana_letters = []
if sana_flags.short_plan:
    sana_letters.append(_SHORT_PLAN_MODE_LETTERS[sana_flags.short_plan_mode])
for name in ("CoT", "results_apis"):
    if getattr(sana_flags, name):
        sana_letters.append(_SANA_FEATURE_LETTERS[name])
```

Keep the cadence `mrk` label and add the source-budget budget label:

```python
if sana_flags.short_plan:
    if sana_flags.short_plan_mode == "cadence":
        parts.append(f"mrk{sana_flags.macro_reflection_k}")
    elif sana_flags.short_plan_mode == "source_budget":
        parts.append(f"sbc{sana_flags.source_budget_calls}")
```

Add parser arguments after `--macro-reflection-k`:

```python
parser.add_argument(
    "--short-plan-mode",
    choices=["cadence", "source_budget"],
    default="cadence",
    help=(
        "Short-plan control mode when --sana-feature short_plan is enabled. "
        "cadence reflects every --macro-reflection-k tool calls; source_budget "
        "uses per-source budget contracts."
    ),
)
parser.add_argument(
    "--source-budget-calls",
    type=int,
    default=3,
    help="Default per-source call budget for --short-plan-mode source_budget.",
)
```

Add validation:

```python
if args.source_budget_calls <= 0:
    parser.error("--source-budget-calls must be > 0")
```

Pass values into `SanaFlags.from_feature_names()`:

```python
sana_flags = SanaFlags.from_feature_names(
    args.sana_feature,
    macro_reflection_k=args.macro_reflection_k,
    short_plan_mode=args.short_plan_mode,
    source_budget_calls=args.source_budget_calls,
)
```

- [ ] **Step 6: Run a CLI help smoke check**

Run:

```bash
.venv/bin/python -m sana_evaluation.run_sana_eval --help | rg "short-plan-mode|source-budget-calls"
```

Expected: both new arguments appear in help output.

- [ ] **Step 7: Commit configuration changes**

Run:

```bash
git add sana_evaluation/flags.py sana_evaluation/run_sana_eval.py sana_evaluation/tests/test_flags.py
git commit -m "Add short plan mode configuration"
```

---

### Task 2: Add Source Session Helper Module

**Files:**
- Create: `sana_evaluation/plugins/source_session.py`
- Create: `sana_evaluation/tests/test_source_session.py`

- [ ] **Step 1: Write source extraction tests**

Create `sana_evaluation/tests/test_source_session.py`:

```python
from sana_evaluation.plugins.source_session import SourceSessionState, source_from_tool_use


def test_source_from_dataset_id_input() -> None:
    source = source_from_tool_use(
        {"name": "peek_file", "input": {"dataset_id": "county-population"}}
    )
    assert source == "county-population"


def test_source_from_single_dataset_ids_input() -> None:
    source = source_from_tool_use(
        {"name": "list_files", "input": {"dataset_ids": ["libraries-2021"]}}
    )
    assert source == "libraries-2021"


def test_source_from_s3_uri_input() -> None:
    source = source_from_tool_use(
        {
            "name": "read_file",
            "input": {
                "s3_uri": (
                    "s3://lakeqa-yc4103-datalake/datagov/"
                    "iowa-local-area-unemployment-statistics/files/rows.csv"
                )
            },
        }
    )
    assert source == "iowa-local-area-unemployment-statistics"


def test_source_from_batch_files_same_dataset() -> None:
    source = source_from_tool_use(
        {
            "name": "peek_multiple",
            "input": {
                "files": [
                    {"dataset_id": "schools", "file_path": "a.csv"},
                    {"dataset_id": "schools", "file_path": "b.csv"},
                ]
            },
        }
    )
    assert source == "schools"


def test_source_from_batch_files_multiple_datasets() -> None:
    source = source_from_tool_use(
        {
            "name": "peek_multiple",
            "input": {
                "files": [
                    {"dataset_id": "schools", "file_path": "a.csv"},
                    {"dataset_id": "libraries", "file_path": "b.csv"},
                ]
            },
        }
    )
    assert source == "multi:libraries,schools"


def test_execute_code_falls_back_to_active_source() -> None:
    source = source_from_tool_use(
        {"name": "execute_code", "input": {"code": "print('x')"}},
        fallback_source="schools",
    )
    assert source == "schools"


def test_session_counts_and_budget_exhaustion() -> None:
    state = SourceSessionState(
        current_source="schools",
        commitment_goal="count schools",
        max_source_calls=2,
        success_condition="answer has count",
    )
    assert state.calls_used == 0
    assert state.is_budget_exhausted() is False
    state.record_call("peek_file")
    assert state.calls_used == 1
    assert state.is_budget_exhausted() is False
    state.record_call("query_file")
    assert state.calls_used == 2
    assert state.is_budget_exhausted() is True
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
.venv/bin/python -m pytest sana_evaluation/tests/test_source_session.py -q
```

Expected: import fails because `source_session.py` does not exist.

- [ ] **Step 3: Implement source extraction and state**

Create `sana_evaluation/plugins/source_session.py`:

```python
"""Source-session helpers for short_plan source-budget mode."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


SOURCE_SESSION_TOOLS = {
    "list_files",
    "peek_file",
    "peek_multiple",
    "read_file",
    "grep_file",
    "query_file",
    "download",
    "execute_code",
}

_S3_DATASET_RE = re.compile(
    r"^s3://[^/]+/(?:datagov|wikipedia)/(?P<dataset_id>[^/]+)/"
)


def _clean_source(value: Any) -> Optional[str]:
    if not isinstance(value, str):
        return None
    value = value.strip()
    return value or None


def _source_from_s3_uri(uri: Any) -> Optional[str]:
    uri = _clean_source(uri)
    if uri is None:
        return None
    match = _S3_DATASET_RE.match(uri)
    if not match:
        return None
    return match.group("dataset_id")


def _source_from_files(files: Any) -> Optional[str]:
    if isinstance(files, dict):
        files = [files]
    if not isinstance(files, list) or not files:
        return None
    sources: List[str] = []
    for item in files:
        if isinstance(item, str):
            source = _source_from_s3_uri(item)
        elif isinstance(item, dict):
            source = _clean_source(item.get("dataset_id")) or _source_from_s3_uri(
                item.get("s3_uri") or item.get("uri")
            )
        else:
            source = None
        if source:
            sources.append(source)
    unique = sorted(set(sources))
    if not unique:
        return None
    if len(unique) == 1:
        return unique[0]
    return "multi:" + ",".join(unique)


def source_from_tool_use(
    tool_use: Dict[str, Any],
    *,
    fallback_source: Optional[str] = None,
) -> Optional[str]:
    """Return canonical source id for a tool call, if source-bearing."""

    tool_name = (tool_use or {}).get("name", "")
    if tool_name not in SOURCE_SESSION_TOOLS:
        return None
    tool_input = (tool_use or {}).get("input", {}) or {}

    if tool_name == "execute_code":
        return fallback_source

    source = _clean_source(tool_input.get("dataset_id"))
    if source:
        return source

    dataset_ids = tool_input.get("dataset_ids")
    if isinstance(dataset_ids, list) and dataset_ids:
        cleaned = sorted(set(filter(None, (_clean_source(v) for v in dataset_ids))))
        if len(cleaned) == 1:
            return cleaned[0]
        if len(cleaned) > 1:
            return "multi:" + ",".join(cleaned)

    source = _source_from_s3_uri(tool_input.get("s3_uri") or tool_input.get("uri"))
    if source:
        return source

    return _source_from_files(tool_input.get("files") or tool_input.get("entries"))


@dataclass
class SourceSessionState:
    current_source: str
    commitment_goal: str
    max_source_calls: int
    success_condition: str
    calls_used: int = 0
    tools_used: List[str] = field(default_factory=list)

    def record_call(self, tool_name: str) -> None:
        self.calls_used += 1
        if tool_name:
            self.tools_used.append(tool_name)

    def is_budget_exhausted(self) -> bool:
        return self.calls_used >= self.max_source_calls

    def describe(self) -> str:
        tools = ", ".join(self.tools_used[-5:]) if self.tools_used else "-"
        return (
            f"source_session: {self.current_source} | "
            f"calls: {self.calls_used}/{self.max_source_calls} | "
            f"goal: {self.commitment_goal} | "
            f"success: {self.success_condition} | "
            f"recent_tools: {tools}"
        )
```

- [ ] **Step 4: Run source-session tests**

Run:

```bash
.venv/bin/python -m pytest sana_evaluation/tests/test_source_session.py -q
```

Expected: all `test_source_session.py` tests pass.

- [ ] **Step 5: Commit helper module**

Run:

```bash
git add sana_evaluation/plugins/source_session.py sana_evaluation/tests/test_source_session.py
git commit -m "Add source session helper for short plan"
```

---

### Task 3: Add Source-Budget Runtime Steering

**Files:**
- Modify: `sana_evaluation/plugins/short_plan_plugin.py`
- Test: `sana_evaluation/tests/test_plugins.py`

- [ ] **Step 1: Write failing plugin tests for source-budget mode**

Add these tests to `sana_evaluation/tests/test_plugins.py` under the `ShortPlanSteerHandler` section:

```python
def test_source_budget_requests_contract_on_first_source_tool() -> None:
    h = ShortPlanSteerHandler(
        macro_reflection_k=5,
        short_plan_mode="source_budget",
        source_budget_calls=3,
    )
    action = _run_steer(
        h,
        {"name": "peek_file", "input": {"dataset_id": "schools"}},
    )
    assert isinstance(action, Guide)
    assert "source budget contract" in action.reason.lower()
    assert "schools" in action.reason


def test_source_budget_parses_contract_and_allows_retry() -> None:
    h = ShortPlanSteerHandler(
        macro_reflection_k=5,
        short_plan_mode="source_budget",
        source_budget_calls=3,
    )
    _run_steer(h, {"name": "peek_file", "input": {"dataset_id": "schools"}})
    h.on_after_model(
        _StubAfterModelEvent(
            stop_response=_StubStopResponse(
                _assistant_message(
                    '{"current_source": "schools", '
                    '"commitment_goal": "find enrollment count", '
                    '"max_source_calls": 2, '
                    '"success_condition": "query returns count"}'
                )
            )
        )
    )
    action = _run_steer(
        h,
        {"name": "peek_file", "input": {"dataset_id": "schools"}},
    )
    assert isinstance(action, Proceed)
    assert h.source_session is not None
    assert h.source_session.current_source == "schools"
    assert h.source_session.max_source_calls == 2


def test_source_budget_guides_when_session_budget_exhausted() -> None:
    h = ShortPlanSteerHandler(
        macro_reflection_k=5,
        short_plan_mode="source_budget",
        source_budget_calls=2,
    )
    _run_steer(h, {"name": "peek_file", "input": {"dataset_id": "schools"}})
    h.on_after_model(
        _StubAfterModelEvent(
            stop_response=_StubStopResponse(
                _assistant_message(
                    '{"current_source": "schools", '
                    '"commitment_goal": "find enrollment count", '
                    '"max_source_calls": 2, '
                    '"success_condition": "query returns count"}'
                )
            )
        )
    )
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file", "input": {"dataset_id": "schools"}}))
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "query_file", "input": {"dataset_id": "schools"}}))

    action = _run_steer(
        h,
        {"name": "query_file", "input": {"dataset_id": "schools"}},
    )
    assert isinstance(action, Guide)
    assert "source-session budget" in action.reason.lower()
    assert "next_action" in action.reason


def test_source_budget_guides_before_source_switch() -> None:
    h = ShortPlanSteerHandler(
        macro_reflection_k=5,
        short_plan_mode="source_budget",
        source_budget_calls=3,
    )
    _run_steer(h, {"name": "peek_file", "input": {"dataset_id": "schools"}})
    h.on_after_model(
        _StubAfterModelEvent(
            stop_response=_StubStopResponse(
                _assistant_message(
                    '{"current_source": "schools", '
                    '"commitment_goal": "find enrollment count", '
                    '"max_source_calls": 3, '
                    '"success_condition": "query returns count"}'
                )
            )
        )
    )
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file", "input": {"dataset_id": "schools"}}))

    action = _run_steer(
        h,
        {"name": "list_files", "input": {"dataset_ids": ["libraries"]}},
    )
    assert isinstance(action, Guide)
    assert "before switching sources" in action.reason.lower()
    assert "schools" in action.reason
    assert "libraries" in action.reason


def test_source_budget_reflection_can_extend_current_source() -> None:
    h = ShortPlanSteerHandler(
        macro_reflection_k=5,
        short_plan_mode="source_budget",
        source_budget_calls=1,
    )
    _run_steer(h, {"name": "peek_file", "input": {"dataset_id": "schools"}})
    h.on_after_model(
        _StubAfterModelEvent(
            stop_response=_StubStopResponse(
                _assistant_message(
                    '{"current_source": "schools", '
                    '"commitment_goal": "find enrollment count", '
                    '"max_source_calls": 1, '
                    '"success_condition": "query returns count"}'
                )
            )
        )
    )
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file", "input": {"dataset_id": "schools"}}))
    _run_steer(h, {"name": "query_file", "input": {"dataset_id": "schools"}})
    h.on_after_model(
        _StubAfterModelEvent(
            stop_response=_StubStopResponse(
                _assistant_message(
                    '{"current_source": "schools", '
                    '"calls_used": 1, '
                    '"commitment_goal": "find enrollment count", '
                    '"evidence_gained": "found schema", '
                    '"remaining_gap": "need count", '
                    '"next_action": "continue_source", '
                    '"revised_budget": 2}'
                )
            )
        )
    )
    assert h.source_session is not None
    assert h.source_session.max_source_calls == 3
    assert h.source_session.calls_used == 1
```

- [ ] **Step 2: Run plugin tests to verify they fail**

Run:

```bash
.venv/bin/python -m pytest sana_evaluation/tests/test_plugins.py -q
```

Expected: new source-budget tests fail because `ShortPlanSteerHandler` does not accept the new constructor arguments or source-session behavior.

- [ ] **Step 3: Add constructor fields and source-session state**

In `sana_evaluation/plugins/short_plan_plugin.py`, import:

```python
from sana_evaluation.plugins.source_session import SourceSessionState, source_from_tool_use
```

Update the constructor:

```python
def __init__(
    self,
    *,
    macro_reflection_k: int,
    short_plan_mode: str = "cadence",
    source_budget_calls: int = 3,
) -> None:
    super().__init__()
    self._k = max(int(macro_reflection_k), 1)
    self._mode = short_plan_mode
    self._source_budget_calls = max(int(source_budget_calls), 1)
    self._reset()
    self.dashboard_plugin: Optional[Any] = None
```

Update `_reset()`:

```python
self._tool_calls_since_reflection = 0
self._awaiting_reflection_response = False
self._awaiting_contract_response = False
self._pending_contract_source: Optional[str] = None
self._pending_switch_source: Optional[str] = None
self._reflections_done = 0
self.last_reflection: Optional[Dict[str, Any]] = None
self.source_session: Optional[SourceSessionState] = None
```

- [ ] **Step 4: Split cadence and source-budget steering paths**

Replace `steer_before_tool()` body with:

```python
async def steer_before_tool(self, *, agent, tool_use, **kwargs) -> ToolSteeringAction:
    tool_name = (tool_use or {}).get("name", "")
    if tool_name in _EXCLUDED_TOOLS:
        return Proceed(reason="administrative tool - never gated by reflection")
    if self._mode == "source_budget":
        return self._steer_source_budget(tool_use or {})
    return self._steer_cadence(tool_name)
```

Add `_steer_cadence()` using the existing k-boundary logic:

```python
def _steer_cadence(self, tool_name: str) -> ToolSteeringAction:
    if (
        self._tool_calls_since_reflection >= self._k
        and not self._awaiting_reflection_response
    ):
        self._awaiting_reflection_response = True
        self._tool_calls_since_reflection = 0
        return Guide(reason=self._compose_reason(_REFLECTION_GUIDE_REASON))
    return Proceed(reason="within sprint window")
```

Add `_compose_reason()`:

```python
def _compose_reason(self, instruction: str) -> str:
    if self.dashboard_plugin is None:
        return instruction
    try:
        return self.dashboard_plugin.render_block() + "\n\n" + instruction
    except Exception as exc:  # pragma: no cover - defensive
        logger.warning("Dashboard render_block failed: %s", exc)
        return instruction
```

- [ ] **Step 5: Add source-budget Guide instructions**

Add constants near `_REFLECTION_GUIDE_REASON`:

```python
_SOURCE_CONTRACT_GUIDE_REASON = (
    "Pause tool calls. You are starting work on source `{source}`. "
    "Respond with ONE JSON object only - no tool calls on this response. "
    "This is a source budget contract. Schema: "
    '{"current_source": "{source}", '
    '"commitment_goal": "<what you will learn from this source>", '
    '"max_source_calls": <positive integer, default {default_budget}>, '
    '"success_condition": "<what evidence means this source commitment is complete>"}. '
    "After the JSON is parsed, retry the source tool call you were about to make."
)

_SOURCE_REFLECTION_GUIDE_REASON = (
    "Pause tool calls. The source-session budget is exhausted or a source switch "
    "is about to happen. Current source: `{current_source}`. Requested next source: `{next_source}`. "
    "Respond with ONE JSON object only - no tool calls on this response. "
    "Schema: "
    '{"current_source": "{current_source}", '
    '"calls_used": <integer>, '
    '"commitment_goal": "<current source goal>", '
    '"evidence_gained": "<what this source yielded>", '
    '"remaining_gap": "<what is still missing>", '
    '"next_action": "continue_source" | "switch_source" | "submit", '
    '"revised_budget": <integer additional calls if continuing, else 0>}. '
    "After the JSON is parsed, continue according to next_action."
)
```

- [ ] **Step 6: Implement source-budget steering**

Add:

```python
def _steer_source_budget(self, tool_use: Dict[str, Any]) -> ToolSteeringAction:
    if self._awaiting_contract_response or self._awaiting_reflection_response:
        return Proceed(reason="awaiting model response to pending source-budget instruction")

    active_source = self.source_session.current_source if self.source_session else None
    requested_source = source_from_tool_use(tool_use, fallback_source=active_source)
    tool_name = (tool_use or {}).get("name", "")

    if requested_source is None:
        return Proceed(reason="tool has no source-session identity")

    if self.source_session is None:
        self._awaiting_contract_response = True
        self._pending_contract_source = requested_source
        return Guide(
            reason=self._compose_reason(
                _SOURCE_CONTRACT_GUIDE_REASON.format(
                    source=requested_source,
                    default_budget=self._source_budget_calls,
                )
            )
        )

    if requested_source != self.source_session.current_source:
        self._awaiting_reflection_response = True
        self._pending_switch_source = requested_source
        return Guide(
            reason=self._compose_reason(
                _SOURCE_REFLECTION_GUIDE_REASON.format(
                    current_source=self.source_session.current_source,
                    next_source=requested_source,
                )
                + " Reflect before switching sources."
            )
        )

    if self.source_session.is_budget_exhausted():
        self._awaiting_reflection_response = True
        return Guide(
            reason=self._compose_reason(
                _SOURCE_REFLECTION_GUIDE_REASON.format(
                    current_source=self.source_session.current_source,
                    next_source=self.source_session.current_source,
                )
            )
        )

    return Proceed(reason="within source-session budget")
```

- [ ] **Step 7: Update tool counting for source-budget mode**

Update `on_after_tool()`:

```python
@hook
def on_after_tool(self, event: AfterToolCallEvent) -> None:
    tool_use = getattr(event, "tool_use", {}) or {}
    tool_name = tool_use.get("name", "")
    if tool_name in _EXCLUDED_TOOLS:
        return
    if self._mode == "source_budget":
        active_source = self.source_session.current_source if self.source_session else None
        requested_source = source_from_tool_use(tool_use, fallback_source=active_source)
        if self.source_session is not None and requested_source == self.source_session.current_source:
            self.source_session.record_call(tool_name)
        return
    self._tool_calls_since_reflection += 1
```

- [ ] **Step 8: Parse contract JSON and reflection JSON**

Update `on_after_model()` so it branches:

```python
if self._awaiting_contract_response:
    self._handle_contract_response(text)
    return
if self._awaiting_reflection_response:
    self._handle_reflection_response(text)
    return
```

Add:

```python
def _handle_contract_response(self, text: str) -> None:
    parsed = self._parse_reflection_json(text)
    self._awaiting_contract_response = False
    if parsed is None:
        logger.warning("Source budget contract did not contain parseable JSON.")
        return
    source = str(parsed.get("current_source") or self._pending_contract_source or "").strip()
    if not source:
        logger.warning("Source budget contract missing current_source.")
        return
    budget = parsed.get("max_source_calls", self._source_budget_calls)
    try:
        budget_int = max(int(budget), 1)
    except (TypeError, ValueError):
        budget_int = self._source_budget_calls
    self.source_session = SourceSessionState(
        current_source=source,
        commitment_goal=str(parsed.get("commitment_goal") or "unspecified"),
        max_source_calls=budget_int,
        success_condition=str(parsed.get("success_condition") or "unspecified"),
    )
    self._pending_contract_source = None
```

Add:

```python
def _handle_reflection_response(self, text: str) -> None:
    parsed = self._parse_reflection_json(text)
    self._awaiting_reflection_response = False
    if parsed is None:
        logger.warning("Macro-reflection response did not contain parseable JSON.")
        return
    self.last_reflection = parsed
    self._reflections_done += 1
    if self._mode != "source_budget" or self.source_session is None:
        return
    next_action = str(parsed.get("next_action") or "").strip()
    if next_action == "continue_source":
        revised_budget = parsed.get("revised_budget", 0)
        try:
            additional = max(int(revised_budget), 0)
        except (TypeError, ValueError):
            additional = 0
        if additional > 0:
            self.source_session.max_source_calls = self.source_session.calls_used + additional
    elif next_action in {"switch_source", "submit"}:
        self.source_session = None
    self._pending_switch_source = None
```

Keep `_parse_reflection_json()` unchanged.

- [ ] **Step 9: Include source session in dashboard description**

Update `describe_for_dashboard()` to append source-session state:

```python
if self.source_session is not None:
    lines.append(self.source_session.describe())
```

- [ ] **Step 10: Run plugin tests**

Run:

```bash
.venv/bin/python -m pytest sana_evaluation/tests/test_plugins.py -q
```

Expected: all plugin tests pass.

- [ ] **Step 11: Commit runtime changes**

Run:

```bash
git add sana_evaluation/plugins/short_plan_plugin.py sana_evaluation/tests/test_plugins.py
git commit -m "Add source budget short plan steering"
```

---

### Task 4: Add Source-Budget Prompt Text

**Files:**
- Modify: `sana_evaluation/prompts/short_plan.py`
- Modify: `sana_evaluation/sana_bundle.py`
- Test: `sana_evaluation/tests/test_prompts.py`

- [ ] **Step 1: Write prompt tests for both modes**

Replace the existing short-plan prompt test in `sana_evaluation/tests/test_prompts.py` with:

```python
@pytest.mark.parametrize("search_tool", _SEARCH_MODES)
def test_short_plan_block_describes_cadence_reflection(search_tool: str) -> None:
    text = short_plan_block(search_tool, short_plan_mode="cadence")
    assert "K-TURN SPRINT REFLECTION" in text
    assert "short_forward_plan" in text
    assert "global_status" in text
    assert "potential_answer" in text
    assert "answer_confidence" in text
    assert "turns 1-2" in text
    assert "State of Task" in text
    assert "long_plan" in text
    assert "confidence" in text
    assert "evidence" in text
    assert "source budget contract" not in text.lower()
    assert "SANA" not in text


@pytest.mark.parametrize("search_tool", _SEARCH_MODES)
def test_short_plan_block_describes_source_budget_contract(search_tool: str) -> None:
    text = short_plan_block(search_tool, short_plan_mode="source_budget")
    assert "SOURCE BUDGET CONTRACT" in text
    assert "current_source" in text
    assert "commitment_goal" in text
    assert "max_source_calls" in text
    assert "success_condition" in text
    assert "next_action" in text
    assert "continue_source" in text
    assert "switch_source" in text
    assert "State of Task" in text
    assert "SANA" not in text
```

- [ ] **Step 2: Run prompt tests to verify they fail**

Run:

```bash
.venv/bin/python -m pytest sana_evaluation/tests/test_prompts.py -q
```

Expected: tests fail because `short_plan_block()` does not accept `short_plan_mode`.

- [ ] **Step 3: Update `short_plan_block()` signature**

Change the function signature:

```python
def short_plan_block(search_tool: str, short_plan_mode: str = "cadence") -> str:
```

Keep the existing cadence text as a helper:

```python
def _cadence_block() -> str:
    return "..."
```

Add a source-budget helper:

```python
def _source_budget_block() -> str:
    return (
        "\n\n## SOURCE BUDGET CONTRACT REFLECTION\n"
        "- Dataset access is a multi-turn commitment. When you begin using a source, "
        "the runtime may pause the attempted tool call and ask for a source budget contract.\n"
        "- The contract declares what you are trying to learn from that source, how many "
        "source calls you intend to spend, and what evidence closes the commitment.\n"
        "\n"
        "Source budget contract JSON shape:\n"
        "{\n"
        '  "current_source": "<dataset_id or source id>",\n'
        '  "commitment_goal": "<what this source should answer>",\n'
        '  "max_source_calls": 3,\n'
        '  "success_condition": "<evidence that means this source is complete>"\n'
        "}\n"
        "\n"
        "When the source budget is exhausted, or before switching sources, the runtime "
        "will ask for a source-session reflection.\n"
        "\n"
        "Source-session reflection JSON shape:\n"
        "{\n"
        '  "current_source": "<dataset_id or source id>",\n'
        '  "calls_used": 3,\n'
        '  "commitment_goal": "<current source goal>",\n'
        '  "evidence_gained": "<what this source yielded>",\n'
        '  "remaining_gap": "<what is still missing>",\n'
        '  "next_action": "continue_source" | "switch_source" | "submit",\n'
        '  "revised_budget": 0\n'
        "}\n"
        "\n"
        "If `next_action` is `continue_source`, use `revised_budget` for the additional "
        "source calls you need. If it is `switch_source`, move on. If it is `submit`, "
        "submit the answer on the next turn.\n"
        "\n"
        "Each reflection includes a state-of-task readout before the JSON instruction. "
        "Use that readout as the runtime view of plan progress, confidence trend, and evidence count.\n"
        "When the runtime asks for a contract or reflection, respond with ONE JSON object only - "
        "do not call any tool on that response.\n"
    )
```

Return by mode:

```python
if short_plan_mode == "source_budget":
    return _source_budget_block()
return _cadence_block()
```

- [ ] **Step 4: Pass mode from bundle**

In `sana_evaluation/sana_bundle.py`, update:

```python
parts.append(short_plan_block(st, short_plan_mode=flags.short_plan_mode))
```

Update `ShortPlanSteerHandler` construction:

```python
short_plan_plugin = ShortPlanSteerHandler(
    macro_reflection_k=flags.macro_reflection_k,
    short_plan_mode=flags.short_plan_mode,
    source_budget_calls=flags.source_budget_calls,
)
```

- [ ] **Step 5: Run prompt tests**

Run:

```bash
.venv/bin/python -m pytest sana_evaluation/tests/test_prompts.py -q
```

Expected: all prompt tests pass.

- [ ] **Step 6: Run bundle import smoke test**

Run:

```bash
.venv/bin/python - <<'PY'
from sana_evaluation.flags import SanaFlags
from sana_evaluation.prompts.short_plan import short_plan_block
flags = SanaFlags(short_plan=True, short_plan_mode="source_budget")
flags.validate(agent_management="standard")
print(short_plan_block("preloaded", short_plan_mode=flags.short_plan_mode).splitlines()[2])
PY
```

Expected: output contains `SOURCE BUDGET CONTRACT REFLECTION`.

- [ ] **Step 7: Commit prompt and bundle changes**

Run:

```bash
git add sana_evaluation/prompts/short_plan.py sana_evaluation/sana_bundle.py sana_evaluation/tests/test_prompts.py
git commit -m "Document source budget short plan mode"
```

---

### Task 5: Wire Source-Budget Mode Into Labels And End-to-End Tests

**Files:**
- Modify: `sana_evaluation/tests/test_flags.py`
- Modify: `sana_evaluation/tests/test_plugins.py`
- Create: `sana_evaluation/tests/test_run_sana_eval_config.py`

- [ ] **Step 1: Add condition-label tests**

Create `sana_evaluation/tests/test_run_sana_eval_config.py`:

```python
from sana_evaluation.flags import SanaFlags
from sana_evaluation.run_sana_eval import _variant_condition_label


def test_variant_label_includes_cadence_short_plan_mode() -> None:
    label = _variant_condition_label(
        search_tool="preloaded",
        search_results="ideal",
        agent_management="standard",
        k=None,
        search_calls=None,
        sana_flags=SanaFlags(short_plan=True, short_plan_mode="cadence", macro_reflection_k=5),
    )
    assert "sana_spc" in label
    assert "mrk5" in label


def test_variant_label_includes_source_budget_short_plan_mode() -> None:
    label = _variant_condition_label(
        search_tool="preloaded",
        search_results="ideal",
        agent_management="standard",
        k=None,
        search_calls=None,
        sana_flags=SanaFlags(
            short_plan=True,
            short_plan_mode="source_budget",
            source_budget_calls=4,
        ),
    )
    assert "sana_spsb" in label
    assert "sbc4" in label
    assert "mrk" not in label
```

- [ ] **Step 2: Run the new label tests**

Run:

```bash
.venv/bin/python -m pytest sana_evaluation/tests/test_run_sana_eval_config.py -q
```

Expected: tests pass after Task 1. If they fail because importing `run_sana_eval` mutates shared runner state, move these tests into `test_flags.py` and import only `_variant_condition_label`.

- [ ] **Step 3: Run the full SANA unit suite**

Run:

```bash
.venv/bin/python -m pytest sana_evaluation/tests/ -x -q
```

Expected: all SANA tests pass.

- [ ] **Step 4: Run source-budget CLI smoke with no execution**

Use `--help` and parser validation first:

```bash
.venv/bin/python -m sana_evaluation.run_sana_eval \
  --sana-feature short_plan \
  --short-plan-mode source_budget \
  --source-budget-calls 0 \
  --help >/tmp/sana_help.txt
```

Expected: command exits 0 because `--help` short-circuits validation and `/tmp/sana_help.txt` contains parser help.

Then validate parser error by omitting `--help` and using a harmless non-existing task-dir. This should fail during argument validation before task loading:

```bash
.venv/bin/python -m sana_evaluation.run_sana_eval \
  --sana-feature short_plan \
  --short-plan-mode source_budget \
  --source-budget-calls 0 \
  --task-dir /tmp/does-not-exist
```

Expected: exits non-zero with `--source-budget-calls must be > 0`.

- [ ] **Step 5: Commit label and test coverage**

Run:

```bash
git add sana_evaluation/tests/test_run_sana_eval_config.py sana_evaluation/tests/test_flags.py sana_evaluation/tests/test_plugins.py
git commit -m "Test short plan source budget wiring"
```

---

### Task 6: Verification Smoke Run

**Files:**
- No code changes expected.

- [ ] **Step 1: Run full SANA unit suite**

Run:

```bash
.venv/bin/python -m pytest sana_evaluation/tests/ -x -q
```

Expected: all tests pass.

- [ ] **Step 2: Verify no dashboard flag regression**

Run:

```bash
rg -n '"dashboard"|dashboard_active|confidence_advisory' sana_evaluation/flags.py sana_evaluation/run_sana_eval.py sana_evaluation/sana_bundle.py sana_evaluation/prompts
```

Expected: no matches, except matches in comments only if those comments describe removed legacy behavior. Prefer zero matches in active code.

- [ ] **Step 3: Smoke cadence mode on one small task**

Run:

```bash
.venv/bin/python -m sana_evaluation.run_sana_eval \
  --search_tool preloaded \
  --search_results ideal \
  --agent_management standard \
  --sana-feature short_plan \
  --short-plan-mode cadence \
  --macro-reflection-k 3 \
  --task-set tasks_mini \
  --tasks-per-dir 1 \
  --parallel 1 \
  --model-name gpt-5.4-nano \
  --results-output-dir /tmp/sana_short_plan_cadence_results \
  --logs-output-dir /tmp/sana_short_plan_cadence_logs
```

Expected: run completes or fails only for external model/API reasons. If it runs, condition label contains `sana_spc` and `mrk3`.

- [ ] **Step 4: Smoke source-budget mode on one small task**

Run:

```bash
.venv/bin/python -m sana_evaluation.run_sana_eval \
  --search_tool preloaded \
  --search_results ideal \
  --agent_management standard \
  --sana-feature short_plan \
  --short-plan-mode source_budget \
  --source-budget-calls 3 \
  --task-set tasks_mini \
  --tasks-per-dir 1 \
  --parallel 1 \
  --model-name gpt-5.4-nano \
  --results-output-dir /tmp/sana_short_plan_source_budget_results \
  --logs-output-dir /tmp/sana_short_plan_source_budget_logs
```

Expected: run completes or fails only for external model/API reasons. If it runs, condition label contains `sana_spsb` and `sbc3`.

- [ ] **Step 5: Inspect logs for source-budget contract**

Run:

```bash
rg -n "source budget contract|source-session budget|next_action|current_source" /tmp/sana_short_plan_source_budget_logs /tmp/sana_short_plan_source_budget_results
```

Expected: source-budget mode logs contain contract or source-session reflection text at source-session boundaries.

- [ ] **Step 6: Commit final verification notes when docs changed**

If implementation added or changed docs, run:

```bash
git add docs sana_evaluation
git commit -m "Verify short plan source budget mode"
```

If no docs changed during verification, do not create an empty commit.

---

## Self-Review

- Spec coverage: The plan covers the requested axis, `short_plan = off | cadence | source_budget`, using the existing `short_plan` flag for off/on and a new `short_plan_mode` field for the active strategy. It also covers source-session reflection, dataset budget contracts, CLI labels, prompt text, runtime steering, and tests.
- Placeholder scan: No task contains placeholder markers or an unspecified "add tests" instruction. Every task names exact files, concrete code snippets, commands, and expected outcomes.
- Type consistency: The same names are used throughout: `short_plan_mode`, `source_budget_calls`, `source_budget`, `SourceSessionState`, `source_from_tool_use`, `source_session`, `continue_source`, `switch_source`, and `submit`.
- Scope check: This plan does not implement confidence advisory, new analysis figures, or paper text. It only adds the source-budget mode under the existing dashboard-folded `short_plan` primitive.

"""Shared loader/state for ideal-mode task plans.

Default mappings:
- tasks_mini/... -> plans_mini/...
- tasks_core/... -> plans_mini/tasks_core/...
- tasks_core_quality/... -> plans_core_quality/...
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

_PLANS_ROOT = Path("plans_mini")
_QUALITY_PLANS_ROOT = Path("plans_core_quality")
_TASK_CONTEXT: Dict[str, Any] = {}


@dataclass(frozen=True)
class IdealTaskPlan:
    task_id: str
    plan_path: Path
    dataset_sequence: List[str]
    source_sequence: List[str]
    reasoning_chain_text: str


def set_plans_root(path: str | Path) -> None:
    global _PLANS_ROOT
    _PLANS_ROOT = Path(path)


def plans_root() -> Path:
    return _PLANS_ROOT


def set_task_context(task_context: Optional[Dict[str, Any]]) -> None:
    global _TASK_CONTEXT
    _TASK_CONTEXT = dict(task_context or {})


def get_task_context() -> Dict[str, Any]:
    return dict(_TASK_CONTEXT)


def task_id_from_context(task_context: Optional[Dict[str, Any]]) -> str:
    return str((task_context or {}).get("task_id") or "").strip()


def _plan_location_from_task(task_id: str) -> tuple[Path, Path]:
    raw = str(task_id or "").strip()
    if not raw:
        raise ValueError("Missing task_id for ideal plan lookup.")

    p = Path(raw)
    parts = p.parts
    for task_root in ("tasks_core_quality", "tasks_core", "tasks_mini"):
        if task_root not in parts:
            continue
        idx = parts.index(task_root)
        suffix = parts[idx + 1 :]
        if not suffix:
            raise ValueError(f"Could not derive relative plan path from task_id '{task_id}'.")
        if task_root == "tasks_core_quality":
            return (_QUALITY_PLANS_ROOT, Path(*suffix))
        if task_root == "tasks_core":
            return (plans_root(), Path(task_root) / Path(*suffix))
        return (plans_root(), Path(*suffix))

    if p.is_absolute():
        return (plans_root(), Path(p.name))
    return (plans_root(), p)


def plan_path_for_task(task_id: str) -> Path:
    root, relpath = _plan_location_from_task(task_id)
    return root / relpath


def _validate_dataset_sequence(raw: Any, *, plan_path: Path) -> List[str]:
    if not isinstance(raw, list):
        raise ValueError(f"Invalid plan at '{plan_path}': dataset_sequence must be a list.")

    out: List[str] = []
    for i, item in enumerate(raw):
        if not isinstance(item, str):
            raise ValueError(
                f"Invalid plan at '{plan_path}': dataset_sequence[{i}] must be a string."
            )
        dataset_id = item.strip()
        if not dataset_id:
            raise ValueError(
                f"Invalid plan at '{plan_path}': dataset_sequence[{i}] cannot be empty."
            )
        if "/" in dataset_id or "://" in dataset_id:
            raise ValueError(
                f"Invalid plan at '{plan_path}': dataset_sequence[{i}] must be a bare dataset ID, got '{dataset_id}'."
            )
        out.append(dataset_id)
    return out


def _validate_source_sequence(raw: Any, *, plan_path: Path) -> List[str]:
    if not isinstance(raw, list):
        raise ValueError(f"Invalid plan at '{plan_path}': source_sequence must be a list.")

    out: List[str] = []
    for i, item in enumerate(raw):
        if not isinstance(item, str):
            raise ValueError(
                f"Invalid plan at '{plan_path}': source_sequence[{i}] must be a string."
            )
        source = item.strip()
        if not source:
            raise ValueError(
                f"Invalid plan at '{plan_path}': source_sequence[{i}] cannot be empty."
            )
        if "/" not in source:
            raise ValueError(
                f"Invalid plan at '{plan_path}': source_sequence[{i}] must be a dataset-relative file path, got '{source}'."
            )
        if "://" in source:
            raise ValueError(
                f"Invalid plan at '{plan_path}': source_sequence[{i}] must be a dataset-relative file path, got '{source}'."
            )
        out.append(source)
    if not out:
        raise ValueError(f"Invalid plan at '{plan_path}': source_sequence cannot be empty.")
    return out


def _validate_reasoning_text(raw: Any, *, plan_path: Path) -> str:
    if isinstance(raw, str):
        text = raw.strip()
        if "\\n" in text and "\n" not in text:
            text = text.replace("\\n", "\n")
        if not text:
            raise ValueError(f"Invalid plan at '{plan_path}': reasoning_chain_text cannot be empty.")
        return text

    if isinstance(raw, list):
        if not raw:
            raise ValueError(f"Invalid plan at '{plan_path}': reasoning_chain_text cannot be an empty list.")

        lines: List[str] = []
        for i, item in enumerate(raw):
            if not isinstance(item, str):
                raise ValueError(
                    f"Invalid plan at '{plan_path}': reasoning_chain_text[{i}] must be a string."
                )
            text = item.strip()
            if not text:
                raise ValueError(
                    f"Invalid plan at '{plan_path}': reasoning_chain_text[{i}] cannot be empty."
                )
            lines.append(text)
        return "\n".join(lines)

    raise ValueError(
        f"Invalid plan at '{plan_path}': reasoning_chain_text must be a string or a list of strings."
    )


def load_plan_for_task(task_id: str) -> IdealTaskPlan:
    plan_path = plan_path_for_task(task_id)
    if not plan_path.exists():
        raise FileNotFoundError(
            f"Missing ideal plan file for task '{task_id}': expected '{plan_path}'."
        )

    try:
        payload = json.loads(plan_path.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in ideal plan file '{plan_path}': {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError(f"Invalid plan at '{plan_path}': root JSON value must be an object.")

    dataset_sequence = _validate_dataset_sequence(
        payload.get("dataset_sequence"),
        plan_path=plan_path,
    )
    source_sequence = _validate_source_sequence(
        payload.get("source_sequence"),
        plan_path=plan_path,
    )
    reasoning_chain_text = _validate_reasoning_text(
        payload.get("reasoning_chain_text"),
        plan_path=plan_path,
    )

    return IdealTaskPlan(
        task_id=str(task_id),
        plan_path=plan_path,
        dataset_sequence=dataset_sequence,
        source_sequence=source_sequence,
        reasoning_chain_text=reasoning_chain_text,
    )


def load_plan_for_context(task_context: Optional[Dict[str, Any]] = None) -> IdealTaskPlan:
    ctx = task_context if task_context is not None else get_task_context()
    task_id = task_id_from_context(ctx)
    return load_plan_for_task(task_id)


__all__ = [
    "IdealTaskPlan",
    "set_plans_root",
    "plans_root",
    "set_task_context",
    "get_task_context",
    "task_id_from_context",
    "plan_path_for_task",
    "load_plan_for_task",
    "load_plan_for_context",
]

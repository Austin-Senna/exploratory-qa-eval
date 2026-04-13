#!/usr/bin/env python3
"""Verify plan fidelity against the mirrored task and cleanliness rubric."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


_OPERATION_PATTERNS = {
    "aggregation": re.compile(r"(?i)\b(sum|average|avg|count|aggregate|compute)\b"),
    "comparison_or_ranking": re.compile(
        r"(?i)\b(compare|comparison|rank|ranked|top\b|highest|lowest|maximum|minimum|higher|lower|more|fewer)\b"
    ),
    "intersection_or_narrowing": re.compile(
        r"(?i)(?:\bintersect(?:ion|ing)?\b|\bremain(?:ing)?\b|common to|appear in all|from those|from that subset|from the subset|\bkeep\b|\bnarrow\b)"
    ),
    "filter_or_lookup": re.compile(
        r"(?i)\b(filter|identify|determine|find|retrieve|return|lookup|capital|county seat|headquarters|operates|founded|chartered|incorporated)\b"
    ),
}


def _repo_root(start: Path) -> Path:
    anchor = start if start.is_dir() else start.parent
    for candidate in [anchor, *anchor.parents]:
        if (candidate / "tasks_mini").exists() and (candidate / "plans_mini").exists():
            return candidate
    raise RuntimeError(f"Could not locate repo root from '{start}'.")


def _load_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON at '{path}': {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at '{path}'.")
    return payload


def _plan_relpath(plan_path: Path, repo_root: Path) -> Path:
    plans_root = (repo_root / "plans_mini").resolve()
    resolved = plan_path.resolve()
    try:
        return resolved.relative_to(plans_root)
    except ValueError as exc:
        raise ValueError(
            f"Plan path '{plan_path}' must be inside '{plans_root}'."
        ) from exc


def _task_path_for_plan(plan_path: Path, repo_root: Path) -> Path:
    relpath = _plan_relpath(plan_path, repo_root)
    return repo_root / "tasks_mini" / relpath


def _load_author_checker(repo_root: Path):
    checker_path = repo_root / ".agents" / "skills" / "author-ideal-plans" / "scripts" / "check_plan_cleanliness.py"
    if not checker_path.exists():
        raise FileNotFoundError(
            f"Missing author-ideal-plans checker at '{checker_path}'."
        )
    spec = importlib.util.spec_from_file_location("author_ideal_plans_check", checker_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load checker module from '{checker_path}'.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _add_issue(issues: List[Dict[str, Any]], code: str, message: str, **extra: Any) -> None:
    item: Dict[str, Any] = {"code": code, "message": message}
    item.update(extra)
    issues.append(item)


def _normalized_reasoning_text(raw: Any) -> str:
    if raw is None:
        return ""
    if isinstance(raw, str):
        text = raw.strip()
        if "\\n" in text and "\n" not in text:
            text = text.replace("\\n", "\n")
        return text
    if isinstance(raw, list):
        lines = []
        for item in raw:
            if isinstance(item, str):
                text = item.strip()
                if text:
                    lines.append(text)
        return "\n".join(lines)
    return str(raw).strip()


def _normalized_list(raw: Any) -> List[str]:
    if not isinstance(raw, list):
        return []
    out: List[str] = []
    for item in raw:
        if isinstance(item, str):
            value = item.strip()
            if value:
                out.append(value)
    return out


def _dataset_id_from_source(source: Any) -> Optional[str]:
    if not isinstance(source, str):
        return None
    value = source.strip()
    if not value:
        return None
    parts = value.split("/")
    if len(parts) >= 2:
        dataset_id = parts[1].strip()
        return dataset_id or None
    return value


def _node_dataset_sequence(task_payload: Dict[str, Any]) -> List[str]:
    raw_nodes = task_payload.get("nodes")
    if not isinstance(raw_nodes, dict):
        return []

    def _node_sort_key(item: tuple[str, Any]) -> tuple[int, Any]:
        key = item[0]
        try:
            return (0, int(key))
        except (TypeError, ValueError):
            return (1, str(key))

    out: List[str] = []
    seen: set[str] = set()
    for _node_id, node_payload in sorted(raw_nodes.items(), key=_node_sort_key):
        if not isinstance(node_payload, dict):
            continue
        dataset_id = _dataset_id_from_source(node_payload.get("source"))
        if not dataset_id or dataset_id in seen:
            continue
        seen.add(dataset_id)
        out.append(dataset_id)
    return out


def _source_reasoning_text(plan_payload: Dict[str, Any], task_payload: Dict[str, Any]) -> str:
    source = plan_payload.get("original_reasoning_chain")
    if source is None:
        source = task_payload.get("reasoning_chain")

    if isinstance(source, str):
        return source.strip()
    if isinstance(source, list):
        return "\n".join(str(item).strip() for item in source if str(item).strip())
    return ""


def _present_operation_families(text: str) -> List[str]:
    present: List[str] = []
    for name, pattern in _OPERATION_PATTERNS.items():
        if pattern.search(text):
            present.append(name)
    return present


def _issue_codes(items: Iterable[Dict[str, Any]]) -> set[str]:
    codes = set()
    for item in items:
        code = item.get("code")
        if isinstance(code, str):
            codes.add(code)
    return codes


def evaluate_verification(plan_path: str | Path) -> Dict[str, Any]:
    resolved_plan_path = Path(plan_path).resolve()
    repo_root = _repo_root(resolved_plan_path)
    task_path = _task_path_for_plan(resolved_plan_path, repo_root)
    if not task_path.exists():
        raise FileNotFoundError(
            f"Missing mirrored task file for '{resolved_plan_path}': expected '{task_path}'."
        )

    author_checker = _load_author_checker(repo_root)
    base_result = author_checker.evaluate_plan(resolved_plan_path)

    plan_payload = _load_json(resolved_plan_path)
    task_payload = _load_json(task_path)

    issues: List[Dict[str, Any]] = list(base_result.get("issues", []))
    notes: List[str] = []
    existing_codes = _issue_codes(issues)

    plan_sequence = _normalized_list(plan_payload.get("dataset_sequence"))
    task_datasets = _normalized_list(task_payload.get("datasets_used"))
    node_datasets = _node_dataset_sequence(task_payload)
    expected_sequence = node_datasets or task_datasets

    if (
        node_datasets
        and task_datasets
        and set(node_datasets) != set(task_datasets)
        and "task_source_dataset_mismatch" not in existing_codes
    ):
        _add_issue(
            issues,
            "task_source_dataset_mismatch",
            "The mirrored task's datasets_used list does not match the unique dataset IDs referenced by nodes.",
            task_datasets=task_datasets,
            node_datasets=node_datasets,
        )

    if set(plan_sequence) != set(expected_sequence):
        if "dataset_coverage_mismatch" in existing_codes:
            pass
        else:
            _add_issue(
                issues,
                "dataset_coverage_mismatch",
                "dataset_sequence does not cover the same dataset IDs as the mirrored task's node sequence.",
                missing_from_plan=sorted(set(expected_sequence) - set(plan_sequence)),
                extra_in_plan=sorted(set(plan_sequence) - set(expected_sequence)),
            )
    elif plan_sequence != expected_sequence:
        if "dataset_order_mismatch" not in existing_codes:
            _add_issue(
                issues,
                "dataset_order_mismatch",
                "dataset_sequence order does not match the mirrored task's first-appearance node order.",
                expected_sequence=expected_sequence,
                actual_sequence=plan_sequence,
            )

    source_reasoning = _source_reasoning_text(plan_payload, task_payload)
    if not source_reasoning:
        _add_issue(
            issues,
            "missing_source_reasoning_chain",
            "Could not find an original reasoning chain on the plan or mirrored task.",
        )
    else:
        source_ops = _present_operation_families(source_reasoning)
        plan_ops = _present_operation_families(_normalized_reasoning_text(plan_payload.get("reasoning_chain_text")))
        missing_ops = [name for name in source_ops if name not in plan_ops]
        if missing_ops:
            _add_issue(
                issues,
                "reasoning_chain_mismatch",
                "The cleaned plan appears to drop operation families required by the original reasoning chain.",
                missing_operation_families=missing_ops,
                source_operation_families=source_ops,
                plan_operation_families=plan_ops,
            )

    cleanliness_codes = _issue_codes(issues)
    if "answer_leak" in cleanliness_codes:
        notes.append("Plan leaks discovered task results and may allow step-skipping.")
    if "step_count_mismatch" in cleanliness_codes:
        notes.append("Plan step count mismatch usually indicates collapsed or skipped reasoning.")

    return {
        "status": "clean" if not issues else "needs_revision",
        "plan_path": str(resolved_plan_path),
        "task_path": str(task_path),
        "issues": issues,
        "notes": notes,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify a plans_mini file against its mirrored task and leak-prevention rubric."
    )
    parser.add_argument("plan_json_path", help="Path to plans_mini/.../task_*.json")
    args = parser.parse_args(argv)

    try:
        result = evaluate_verification(args.plan_json_path)
    except Exception as exc:
        print(json.dumps({
            "status": "needs_revision",
            "issues": [{"code": "runtime_error", "message": str(exc)}],
            "notes": [],
        }, indent=2))
        return 1

    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "clean" else 1


if __name__ == "__main__":
    raise SystemExit(main())

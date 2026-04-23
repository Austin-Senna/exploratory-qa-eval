"""Preflight checks for mode-based eval runs.

Exercises every loader required by the selected mode combination before any
model/API call, so missing or corrupt dependencies fail loudly and cheaply.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence

from strands_evaluation.config import RunConfig

_PROMPTS_DIR = Path("prompts")
_PROFILES_PATH = Path("datagov_tables_profiles.jsonl")


@dataclass
class PreflightCheck:
    name: str
    ok: bool
    detail: str = ""


class PreflightError(RuntimeError):
    """Raised when one or more preflight checks fail."""


def _prompt_files_for_modes(search_tool_mode: str, agent_management_mode: str) -> List[Path]:
    base_name = "baseline.txt" if agent_management_mode == "naive" else "managed.txt"
    overlay_name = f"search_{search_tool_mode}.txt"
    return [_PROMPTS_DIR / base_name, _PROMPTS_DIR / overlay_name]


def _check_file_exists(path: Path, label: str) -> PreflightCheck:
    if path.is_file():
        return PreflightCheck(label, True, f"found: {path}")
    return PreflightCheck(label, False, f"missing: {path}")


def _check_lance_db(path: Path) -> PreflightCheck:
    label = f"lance_db:{path}"
    if not path.exists():
        return PreflightCheck(label, False, f"missing dir: {path}")
    lakeqa = path / "lakeqa.lance"
    if not lakeqa.exists():
        return PreflightCheck(label, False, f"missing table: {lakeqa}")
    return PreflightCheck(label, True, f"found: {lakeqa}")


def _check_desc_cache_for_enrichment() -> PreflightCheck:
    from strands_evaluation.tools.external.ideal import search_wrapper as _sw

    _sw._DESC_CACHE_LOADED = False
    _sw._DESC_BY_URI = {}
    label = "table_descriptions.jsonl (ideal enrichment load)"
    try:
        _sw._load_desc_cache()
    except Exception as exc:
        return PreflightCheck(label, False, str(exc))
    return PreflightCheck(label, True, f"loaded {len(_sw._DESC_BY_URI)} URI entries")


def _check_snippet_cache() -> PreflightCheck:
    from strands_evaluation.tools.external.ideal import search_wrapper as _sw

    _sw._SNIPPET_CACHE_LOADED = False
    _sw._SNIPPET_BY_URI = {}
    label = "snippet.jsonl"
    try:
        _sw._load_snippet_cache()
    except Exception as exc:
        return PreflightCheck(label, False, str(exc))
    return PreflightCheck(label, True, f"loaded {len(_sw._SNIPPET_BY_URI)} URI entries")


def _check_schemas_jsonl_load() -> PreflightCheck:
    from strands_evaluation.tools.external.ideal import search_wrapper as _sw

    _sw._SCHEMAS_CACHE_LOADED = False
    _sw._SCHEMA_BY_SLUG_FILENAME = {}
    label = "datagov_tables_schemas_full.jsonl"
    try:
        _sw._load_schemas_cache()
    except Exception as exc:
        return PreflightCheck(label, False, str(exc))
    return PreflightCheck(
        label,
        True,
        f"loaded {len(_sw._SCHEMA_BY_SLUG_FILENAME)} (slug, file) entries",
    )


def _check_profiles_jsonl() -> PreflightCheck:
    label = "datagov_tables_profiles.jsonl"
    if not _PROFILES_PATH.exists():
        return PreflightCheck(
            label,
            True,
            f"missing: {_PROFILES_PATH} (Agent 1 falls back to legacy schema+snippet+description)",
        )

    count = 0
    try:
        with _PROFILES_PATH.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                count += 1
    except Exception as exc:
        return PreflightCheck(label, False, str(exc))
    return PreflightCheck(label, True, f"found: {count} entries")


def _check_plan_files(task_files: Sequence[str]) -> List[PreflightCheck]:
    from strands_evaluation.tools.external.ideal import plan_store

    checks: List[PreflightCheck] = []
    for task_path in task_files:
        label = f"plan:{task_path}"
        try:
            plan_store.load_plan_for_task(task_path)
        except Exception as exc:
            checks.append(PreflightCheck(label, False, str(exc)))
            continue
        checks.append(PreflightCheck(label, True, "plan loads and validates"))
    return checks


def run_preflight(
    run_config: RunConfig,
    task_files: Sequence[str],
    *,
    stream=None,
) -> List[PreflightCheck]:
    """Execute every dep-loader required by the mode combo.

    Prints a report; raises PreflightError on any failure.
    """
    stream = stream or sys.stdout

    st = (run_config.search_tool_mode or "standard").strip().lower()
    sr = (run_config.search_results_mode or "naive").strip().lower()
    am = (run_config.agent_management_mode or "standard").strip().lower()
    sana = run_config.sana_level

    checks: List[PreflightCheck] = []

    for prompt_path in _prompt_files_for_modes(st, am):
        checks.append(_check_file_exists(prompt_path, f"prompt:{prompt_path.name}"))

    if st in {"standard", "naive"}:
        db_path = Path(run_config.search_db_path or "./lance_data")
        checks.append(_check_lance_db(db_path))

    if st in {"ideal", "preloaded"} or am == "ideal":
        if not task_files:
            checks.append(
                PreflightCheck(
                    "plan_files",
                    False,
                    "ideal mode requires resolvable task files at preflight time.",
                )
            )
        else:
            checks.extend(_check_plan_files(task_files))

    # SANA Agent 1 requires the three profile jsonl files; also loaded by search_results=ideal.
    if (sr == "ideal" and st != "preloaded") or (sana is not None and sana >= 1):
        checks.append(_check_desc_cache_for_enrichment())
        checks.append(_check_snippet_cache())
        checks.append(_check_schemas_jsonl_load())
    if sana is not None and sana >= 1:
        checks.append(_check_profiles_jsonl())

    ok_count = sum(1 for c in checks if c.ok)
    fail_count = len(checks) - ok_count

    print(f"\n=== Preflight ({ok_count}/{len(checks)} passed) ===", file=stream)
    for c in checks:
        mark = "OK  " if c.ok else "FAIL"
        print(f"  [{mark}] {c.name} — {c.detail}", file=stream)

    if fail_count:
        msg = f"Preflight FAILED: {fail_count} check(s) failed. Aborting before any model call."
        print(f"\n{msg}\n", file=stream)
        raise PreflightError(msg)

    print("Preflight OK\n", file=stream)
    return checks


__all__ = ["PreflightCheck", "PreflightError", "run_preflight"]

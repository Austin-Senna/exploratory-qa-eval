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
from strands_evaluation.tools.agent_tools import configure_benchmark
from strands_evaluation.tools.external.ideal.benchmark_paths import (
    artifact_paths,
    canonical_source_uri,
    normalize_benchmark,
)

_PROMPTS_DIR = Path("prompts")
_PROFILES_PATH = Path("datagov_tables_profiles.jsonl")


@dataclass
class PreflightCheck:
    name: str
    ok: bool
    detail: str = ""


class PreflightError(RuntimeError):
    """Raised when one or more preflight checks fail."""


def _prompt_files_for_modes(search_tool_mode: str, plan_mode: str) -> List[Path]:
    base_name = "baseline.txt" if plan_mode == "naive" else "managed.txt"
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
    label = f"{_sw._TABLE_DESCRIPTIONS_PATH.name} (ideal enrichment load)"
    try:
        _sw._load_desc_cache()
    except Exception as exc:
        return PreflightCheck(label, False, str(exc))
    return PreflightCheck(label, True, f"loaded {len(_sw._DESC_BY_URI)} URI entries")


def _check_snippet_cache() -> PreflightCheck:
    from strands_evaluation.tools.external.ideal import search_wrapper as _sw

    _sw._SNIPPET_CACHE_LOADED = False
    _sw._SNIPPET_BY_URI = {}
    label = _sw._SNIPPETS_PATH.name
    try:
        _sw._load_snippet_cache()
    except Exception as exc:
        return PreflightCheck(label, False, str(exc))
    return PreflightCheck(label, True, f"loaded {len(_sw._SNIPPET_BY_URI)} URI entries")


def _check_schemas_jsonl_load() -> PreflightCheck:
    from strands_evaluation.tools.external.ideal import search_wrapper as _sw

    _sw._SCHEMAS_CACHE_LOADED = False
    _sw._SCHEMA_BY_SLUG_FILENAME = {}
    label = _sw._SCHEMAS_PATH.name
    try:
        _sw._load_schemas_cache()
    except Exception as exc:
        return PreflightCheck(label, False, str(exc))
    return PreflightCheck(
        label,
        True,
        f"loaded {len(_sw._SCHEMA_BY_SLUG_FILENAME)} (slug, file) entries",
    )


def _check_tasks_mini_source_description_coverage(
    task_files: Sequence[str],
    *,
    benchmark: str,
) -> PreflightCheck:
    from strands_evaluation.tools.external.ideal import plan_store
    from strands_evaluation.tools.external.ideal import search_wrapper as _sw

    label = "tasks_mini plan source description coverage"
    missing: List[str] = []
    checked = 0
    try:
        _sw._load_desc_cache()
    except Exception as exc:
        return PreflightCheck(label, False, str(exc))

    for task_path in task_files:
        task_str = str(task_path)
        if "tasks_mini/" not in task_str and "tasks-mini-kramabench/" not in task_str:
            continue
        try:
            plan = plan_store.load_plan_for_task(task_str)
        except Exception as exc:
            return PreflightCheck(label, False, f"{task_str}: {exc}")
        for source in plan.source_sequence:
            checked += 1
            uri = canonical_source_uri(source, benchmark)
            if uri not in _sw._DESC_BY_URI:
                missing.append(f"{task_str} -> {uri}")

    if missing:
        if benchmark == "kramabench" and not _sw._DESC_BY_URI:
            return PreflightCheck(
                label,
                True,
                f"kramabench description artifact is a stub; skipped coverage for {checked} planned source(s)",
            )
        preview = "; ".join(missing[:5])
        suffix = f"; +{len(missing) - 5} more" if len(missing) > 5 else ""
        return PreflightCheck(
            label,
            False,
            f"missing descriptions for {len(missing)}/{checked} planned source(s): {preview}{suffix}",
        )

    return PreflightCheck(label, True, f"covered {checked} planned source(s)")


def _check_profiles_jsonl(*, required: bool = False) -> PreflightCheck:
    label = _PROFILES_PATH.name
    if not _PROFILES_PATH.exists():
        if required:
            return PreflightCheck(
                label,
                False,
                f"missing: {_PROFILES_PATH} (required as the primary search_results=ideal profile source)",
            )
        return PreflightCheck(
            label,
            True,
            f"missing: {_PROFILES_PATH} (profile enrichment unavailable; peek_file omits profile)",
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
    suffix = " (primary search_results=ideal profile source)" if required else ""
    return PreflightCheck(label, True, f"found: {count} entries{suffix}")


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


def _check_ideal_computation_records(
    task_files: Sequence[str],
    *,
    benchmark: str = "lakeqa",
) -> List[PreflightCheck]:
    from strands_evaluation.tools.external.ideal import plan_store

    checks: List[PreflightCheck] = []
    for task_path in task_files:
        try:
            plan = plan_store.load_plan_for_task(task_path)
        except Exception as exc:
            if benchmark != "kramabench":
                checks.append(PreflightCheck(f"ideal_query:{task_path}", False, str(exc)))
            checks.append(PreflightCheck(f"ideal_code:{task_path}", False, str(exc)))
            continue

        if benchmark == "kramabench":
            checks.append(
                PreflightCheck(
                    f"ideal_query:{task_path}",
                    True,
                    "skipped: query_file/query_ideal disabled for kramabench; use execute_ideal",
                )
            )
        else:
            runnable_query_records = [
                record for record in plan.ideal_query if not getattr(record, "blocked", False)
            ]
            blocked_query_records = [
                record for record in plan.ideal_query if getattr(record, "blocked", False)
            ]
            if runnable_query_records or blocked_query_records:
                detail = f"loaded {len(runnable_query_records)} runnable query record(s)"
                if blocked_query_records:
                    detail += (
                        f"; {len(blocked_query_records)} blocked by query_file limits "
                        "(use execute_ideal/download-style code)"
                    )
                checks.append(
                    PreflightCheck(f"ideal_query:{task_path}", True, detail)
                )
            else:
                checks.append(
                    PreflightCheck(
                        f"ideal_query:{task_path}",
                        True,
                        "no authored ideal_query records; use read/grep/parse tools or execute_ideal as appropriate",
                    )
                )

        if plan.ideal_code:
            checks.append(
                PreflightCheck(
                    f"ideal_code:{task_path}",
                    True,
                    f"loaded {len(plan.ideal_code)} code record(s)",
                )
            )
        else:
            checks.append(
                PreflightCheck(
                    f"ideal_code:{task_path}",
                    True,
                    "no authored ideal_code records; task may be text/prose-only",
                )
            )
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
    pm = (run_config.plan_mode or "standard").strip().lower()
    ct = (getattr(run_config, "computation_tool_mode", None) or "standard").strip().lower()
    benchmark = normalize_benchmark(getattr(run_config, "benchmark", None) or "lakeqa")
    configure_benchmark(benchmark)

    from strands_evaluation.tools.external.ideal import search_wrapper as _sw
    from strands_evaluation.helper import peek_profile as _pp

    paths = artifact_paths(benchmark)
    if benchmark != "lakeqa" or _sw._TABLE_DESCRIPTIONS_PATH.name.startswith("kramabench_"):
        _sw.configure_dependency_paths(
            descriptions=paths.descriptions,
            snippets=paths.snippets,
            schemas=paths.schemas,
        )
    global _PROFILES_PATH
    if benchmark != "lakeqa" or _PROFILES_PATH.name.startswith("kramabench_"):
        _PROFILES_PATH = paths.profiles
        _pp._PROFILES_PATH = Path(__file__).resolve().parents[1] / paths.profiles
        _pp._PROFILES_LOADED = False

    checks: List[PreflightCheck] = []

    for prompt_path in _prompt_files_for_modes(st, pm):
        checks.append(_check_file_exists(prompt_path, f"prompt:{prompt_path.name}"))

    if st in {"standard", "naive"}:
        db_path = Path(run_config.search_db_path or "./lance_data")
        checks.append(_check_lance_db(db_path))

    if st in {"ideal", "preloaded"} or pm == "ideal" or ct == "ideal":
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

    if ct == "ideal":
        if not task_files:
            checks.append(
                PreflightCheck(
                    "ideal_computation_records",
                    False,
                    "ideal computation mode requires resolvable task files at preflight time.",
                )
            )
        else:
            checks.extend(_check_ideal_computation_records(task_files, benchmark=benchmark))

    # search_tool=ideal needs descriptions for the internal selector context.
    if st == "ideal":
        checks.append(_check_desc_cache_for_enrichment())

    # search_results=ideal needs the legacy description/snippet/schema caches.
    if sr == "ideal" and st != "preloaded":
        if st != "ideal":
            checks.append(_check_desc_cache_for_enrichment())
        checks.append(_check_snippet_cache())
        checks.append(_check_schemas_jsonl_load())

    if (st == "ideal" or sr == "ideal") and task_files:
        checks.append(_check_tasks_mini_source_description_coverage(task_files, benchmark=benchmark))

    sana_flags = getattr(run_config, "sana_flags", None)
    if getattr(sana_flags, "results", False):
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

"""
Sidecar instrumentation decorator for per-call trace logging.

Wraps @tool functions and logs JSONL traces to {output_dir}/{task_id}.jsonl
without modifying Strands internals.

Usage:
    from strands_evaluation.instrumentation.sidecar import instrument, set_sidecar_context

    # In the task loop (before agent.run()):
    set_sidecar_context(task_id, task["datasets_used"], sidecar_dir)

    # At agent build time:
    wrapped_tool = instrument("search_sparse", sidecar_dir)(search_sparse)
"""
import functools
import json
import os
import time
from pathlib import Path
from typing import Any, Callable, List

# ---------------------------------------------------------------------------
# Module-level context (mirrors set_sandbox_dir pattern)
# ---------------------------------------------------------------------------

_current_task_id: str = ""
_current_gold_ids: List[str] = []
_current_output_dir: str = ""
_turn_counters: dict = {}  # task_id -> turn count

_S3_PREFIX = "s3://lakeqa-yc4103-datalake/"


def set_sidecar_context(task_id: str, gold_dataset_ids: List[str], output_dir: str) -> None:
    """Set context for the current task. Call once per task before agent.run()."""
    global _current_task_id, _current_gold_ids, _current_output_dir
    _current_task_id = task_id
    _current_gold_ids = list(gold_dataset_ids or [])
    _current_output_dir = output_dir
    _turn_counters[task_id] = 0


def _uri_to_dataset_id(uri: str) -> str:
    """Strip S3 prefix, return first path component."""
    if uri.startswith(_S3_PREFIX):
        remainder = uri[len(_S3_PREFIX):]
    else:
        remainder = uri
    return remainder.split("/")[0] if remainder else uri


def _extract_dataset_ids(result: Any) -> List[str]:
    """Parse dataset IDs from a tool result dict."""
    if not isinstance(result, dict):
        return []
    items = result.get("results", [])
    if not isinstance(items, list):
        return []
    ids = []
    for item in items:
        if not isinstance(item, dict):
            continue
        uri = item.get("dataset_uri") or item.get("uri", "")
        if uri:
            ids.append(_uri_to_dataset_id(uri))
    return ids


def _compute_gold_rank(result_ids: List[str], gold_ids: List[str]) -> int:
    """Return 1-based rank of first gold hit, or -1 if none found."""
    gold_set = set(gold_ids)
    for rank, rid in enumerate(result_ids, start=1):
        if rid in gold_set:
            return rank
    return -1


# ---------------------------------------------------------------------------
# Decorator
# ---------------------------------------------------------------------------

def instrument(tool_name: str, output_dir: str = "") -> Callable:
    """Return a decorator that wraps a @tool function with sidecar logging.

    Args:
        tool_name:  Name used in trace records (e.g. "search_sparse").
        output_dir: Base output directory. Falls back to _current_output_dir
                    if empty, which is set by set_sidecar_context().
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            task_id = _current_task_id
            effective_dir = output_dir or _current_output_dir
            # Increment turn counter
            turn = _turn_counters.get(task_id, 0) + 1
            _turn_counters[task_id] = turn

            # Extract query from args/kwargs
            query = kwargs.get("query", "") or (args[0] if args else "")

            # Approximate token length (chars / 4)
            query_length_tokens = len(str(query)) // 4

            t0 = time.time()
            result = func(*args, **kwargs)
            latency_ms = int((time.time() - t0) * 1000)

            result_ids = _extract_dataset_ids(result)
            gold_ids = _current_gold_ids

            gold_in_results = [gid for gid in gold_ids if gid in result_ids]
            gold_rank = _compute_gold_rank(result_ids, gold_ids)

            record: dict = {
                "task_id": task_id,
                "turn": turn,
                "tool": tool_name,
                "query": str(query),
                "query_length_tokens": query_length_tokens,
                "latency_ms": latency_ms,
                "num_results": len(result_ids),
                "result_dataset_ids": result_ids,
                "gold_dataset_ids_in_results": gold_in_results,
                "gold_rank": gold_rank,
                "timestamp_ms": int(time.time() * 1000),
            }

            # Extra fields for planning tools
            if isinstance(result, dict):
                if "plan" in result:
                    record["plan_text"] = result.get("plan", "")
                    record["is_replan"] = bool(result.get("revised", False))

            if effective_dir and task_id:
                out_path = Path(effective_dir) / f"{task_id}.jsonl"
                out_path.parent.mkdir(parents=True, exist_ok=True)
                with open(out_path, "a") as f:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")

            return result

        # Propagate Strands @tool metadata so the framework recognises the wrapper
        for attr in ("TOOL_SPEC", "tool_spec", "__strands_tool__", "__tool_spec__"):
            if hasattr(func, attr):
                setattr(wrapper, attr, getattr(func, attr))

        return wrapper
    return decorator

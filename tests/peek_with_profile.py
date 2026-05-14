#!/usr/bin/env python3
"""Run peek_file on random profile-backed dataset URIs and log calls/results.

This is a diagnostics utility, not a pytest test. It samples dataset URIs from
the repo-root datagov_tables_profiles.jsonl, calls the actual peek_file tool
implementation for each URI, and writes every tool call plus the full result to
a JSONL log.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

DEFAULT_PROFILE_PATH = REPO_ROOT / "datagov_tables_profiles.jsonl"
DEFAULT_LOG_PATH = REPO_ROOT / "tests" / "peek_with_profile_log.jsonl"


def _load_s3_uris(profile_path: Path) -> List[str]:
    uris: List[str] = []
    with profile_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(row, dict):
                continue
            uri = str(row.get("s3_uri") or "").strip()
            if uri:
                uris.append(uri)
    return uris


def _json_safe(value: Any) -> Any:
    try:
        json.dumps(value)
        return value
    except TypeError:
        return str(value)


def run_peek_with_profile_sample(
    *,
    sample_size: int = 10,
    profile_path: Path = DEFAULT_PROFILE_PATH,
    log_path: Path = DEFAULT_LOG_PATH,
    max_rows: int = 20,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """Sample URIs, call peek_file, and write full tool calls/results to JSONL."""
    os.environ.setdefault("S3_ACCESS_MODE", "unsigned")

    # Import after setting S3_ACCESS_MODE so the tool uses anonymous public S3.
    from strands_evaluation.tools.agent_tools_v2 import peek_file

    uris = _load_s3_uris(profile_path)
    if not uris:
        raise RuntimeError(f"No s3_uri rows found in {profile_path}")
    if sample_size > len(uris):
        raise ValueError(f"sample_size={sample_size} exceeds {len(uris)} available URI rows")

    rng = random.Random(seed) if seed is not None else random.SystemRandom()
    sampled_uris = rng.sample(uris, sample_size)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    written = 0
    with log_path.open("w") as out:
        for index, uri in enumerate(sampled_uris, start=1):
            call = {
                "tool": "peek_file",
                "arguments": {
                    "s3_uri": uri,
                    "max_rows": max_rows,
                },
            }
            started = time.perf_counter()
            started_at = datetime.now(timezone.utc).isoformat()
            try:
                result = peek_file._tool_func(s3_uri=uri, max_rows=max_rows)
                ok = isinstance(result, dict) and "error" not in result
                error = None
            except Exception as exc:  # pragma: no cover - diagnostic script
                result = {"exception": f"{type(exc).__name__}: {exc}"}
                ok = False
                error = result["exception"]

            record = {
                "index": index,
                "started_at": started_at,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
                "ok": ok,
                "error": error,
                "tool_call": call,
                "result": _json_safe(result),
            }
            out.write(json.dumps(record, ensure_ascii=False))
            out.write("\n")
            written += 1

    return {
        "profile_path": str(profile_path),
        "profile_uri_count": len(uris),
        "log_path": str(log_path),
        "sample_size": sample_size,
        "max_rows": max_rows,
        "seed": seed,
        "written": written,
        "sampled_uris": sampled_uris,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample-size", type=int, default=10)
    parser.add_argument("--profile-path", type=Path, default=DEFAULT_PROFILE_PATH)
    parser.add_argument("--log-path", type=Path, default=DEFAULT_LOG_PATH)
    parser.add_argument("--max-rows", type=int, default=20)
    parser.add_argument("--seed", type=int, default=None)
    return parser.parse_args()


def main() -> int:
    summary = run_peek_with_profile_sample(**vars(_parse_args()))
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

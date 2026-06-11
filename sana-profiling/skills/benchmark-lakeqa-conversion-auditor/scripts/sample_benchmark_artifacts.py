#!/usr/bin/env python3
"""Sample benchmark artifacts with simple structural diversity."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _positive_int(raw: str) -> int:
    value = int(raw)
    if value <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return value


def _load_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _signature(value: Any) -> str:
    if isinstance(value, dict):
        parts: list[str] = []
        for key in sorted(value):
            item = value[key]
            if isinstance(item, list):
                parts.append(f"{key}:list:{len(item)}")
            elif isinstance(item, dict):
                parts.append(f"{key}:dict:{len(item)}")
            else:
                parts.append(f"{key}:{type(item).__name__}")
        return "|".join(parts)
    if isinstance(value, list):
        return f"root:list:{len(value)}"
    return f"root:{type(value).__name__}"


def sample(root: Path, limit: int) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*.json")):
        payload = _load_json(path)
        if payload is None:
            continue
        candidates.append(
            {
                "path": str(path),
                "relative_path": str(path.relative_to(root)),
                "signature": _signature(payload),
            }
        )

    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for candidate in candidates:
        if candidate["signature"] in seen:
            continue
        selected.append(candidate)
        seen.add(candidate["signature"])
        if len(selected) >= limit:
            break

    if len(selected) < limit:
        for candidate in candidates:
            if candidate in selected:
                continue
            selected.append(candidate)
            if len(selected) >= limit:
                break

    return {
        "benchmark_root": str(root),
        "candidate_count": len(candidates),
        "sampling_rule": "structural diversity first, deterministic path order fallback",
        "samples": selected,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("benchmark_root")
    parser.add_argument("--limit", type=_positive_int, default=8)
    args = parser.parse_args()

    root = Path(args.benchmark_root).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Benchmark root not found: {root}")
    print(json.dumps(sample(root, args.limit), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

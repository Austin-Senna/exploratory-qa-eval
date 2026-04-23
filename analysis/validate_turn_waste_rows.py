#!/usr/bin/env python3
"""
Validate row-level turn-waste audits against raw logs and optionally rewrite the
mirrored CSVs with validation columns.

Example:
    python analysis/validate_turn_waste_rows.py --source-root results-ec2_semantic_turn_waste --logs-dir logs-ec2/modes --rewrite
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis.turn_waste_validation import validate_turn_waste_root


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", default="results-ec2_semantic_turn_waste")
    parser.add_argument("--logs-dir", default="logs-ec2/modes")
    parser.add_argument("--rewrite", action="store_true")
    args = parser.parse_args()

    outputs = validate_turn_waste_root(
        source_root=args.source_root,
        logs_dir=args.logs_dir,
        rewrite=args.rewrite,
    )
    print(f"Wrote {outputs['failures_path']}")
    print(f"Wrote {outputs['report_path']}")
    print(f"Invalid rows: {len(outputs['invalid_rows'])}")


if __name__ == "__main__":
    main()

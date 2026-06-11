"""Canonical package name for SANA analysis modules.

The implementation still lives in ``analysis/`` during the incremental
migration. Exposing that path here lets new code import ``sana_analysis`` while
older scripts continue to import ``analysis``.
"""

from __future__ import annotations

from pathlib import Path

__path__ = [str(Path(__file__).resolve().parents[1] / "analysis")]

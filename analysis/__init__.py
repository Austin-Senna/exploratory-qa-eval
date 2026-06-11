"""Compatibility namespace for older ``analysis.*`` imports.

New code should import modules from ``sana_analysis``. This package only points
legacy imports at the canonical package while generated analysis outputs finish
migrating away from the old directory name.
"""

from __future__ import annotations

from pathlib import Path

__path__ = [str(Path(__file__).resolve().parents[1] / "sana_analysis")]

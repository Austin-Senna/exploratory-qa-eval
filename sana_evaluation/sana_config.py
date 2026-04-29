"""SanaRunConfig — RunConfig extension carrying SANA feature flags.

Keeps `sana_flags` out of the baseline RunConfig so strands_evaluation/ stays
SANA-clean. SanaDataLakeAgent reads `run_config.sana_flags`; default is an
all-off SanaFlags() if a plain RunConfig is passed in.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from strands_evaluation.config import RunConfig

from sana_evaluation.flags import SanaFlags


@dataclass
class SanaRunConfig(RunConfig):
    sana_flags: SanaFlags = field(default_factory=SanaFlags)


__all__ = ["SanaRunConfig"]

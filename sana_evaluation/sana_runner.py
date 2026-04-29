"""SanaBatchRunner — BatchRunner subclass that uses SanaDataLakeAgent."""

from __future__ import annotations

from strands_evaluation.agent_with_mode import BatchRunner

from sana_evaluation.sana_bundle import SanaDataLakeAgent


class SanaBatchRunner(BatchRunner):
    """Runs tasks through SanaDataLakeAgent instead of the default DataLakeAgent."""

    _AGENT_CLASS = SanaDataLakeAgent


__all__ = ["SanaBatchRunner"]

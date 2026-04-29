"""SANA evaluation harness — runtime-control primitives layered on the strands_evaluation baseline.

This module imports baseline building blocks from `strands_evaluation` and composes
its own agent with SANA-specific prompt blocks and plugins. It does not modify
`strands_evaluation` itself.

See docs/superpowers/specs/2026-04-28-sana-rework-design.md for the design rationale.
"""

from sana_evaluation.flags import SanaFlags

__all__ = ["SanaFlags"]

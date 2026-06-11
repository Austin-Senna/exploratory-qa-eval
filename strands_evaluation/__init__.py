"""Compatibility package for the renamed :mod:`sana_evaluation` runtime."""

from __future__ import annotations

import sana_evaluation as _sana_evaluation

__path__ = _sana_evaluation.__path__

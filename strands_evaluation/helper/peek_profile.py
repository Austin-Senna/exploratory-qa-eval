"""Shared dataset-profile lookup used by optional enhanced tool contexts.

The baseline peek_file behavior intentionally does not import or attach profile
data. Callers that need richer internal context can use this helper, which
reuses SANA's profile loader when that package is available.
"""

from __future__ import annotations

from typing import Any, Dict, Optional


def load_dataset_profile(s3_uri: str) -> Optional[Dict[str, Any]]:
    """Return a cached profile for an S3 file URI, or None if unavailable."""
    try:
        from sana_evaluation.helper.peek_profile import load_dataset_profile as _load
    except Exception:
        return None
    try:
        return _load(s3_uri)
    except Exception:
        return None


__all__ = ["load_dataset_profile"]

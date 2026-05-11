"""Dataset-profile enrichment loader for peek_file (SANA results flag).

When the SANA `results` flag is on, `sana_bundle._decorate_tools` installs a
profile-aware peek_file wrapper. peek_file then attaches a `profile` field to
its return value when a profile is available for the URI.

Profile data sources (in priority order):
1. Precomputed profile rows from `sana_evaluation/data/datagov_tables_profiles.jsonl`
   — keyed by either S3 URI or (slug, filename-stem). Includes column stats,
   top_2_rows, llm_description, schema_columns, etc.
2. Legacy fallback via the ideal-search wrapper's caches (schema, description,
   snippet) when no precomputed row is available. Soft-fails to None if those
   caches aren't loadable in the current environment.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


_PROFILES_PATH = Path(__file__).parents[1] / "data" / "datagov_tables_profiles.jsonl"

_PROFILE_BY_URI: Dict[str, Dict[str, Any]] = {}
_PROFILE_BY_SLUG_FILENAME: Dict[Tuple[str, str], Dict[str, Any]] = {}
_PROFILES_LOADED: bool = False


def _load_profiles_cache() -> None:
    """Load precomputed dataset profiles into in-process caches."""
    global _PROFILES_LOADED, _PROFILE_BY_URI, _PROFILE_BY_SLUG_FILENAME
    if _PROFILES_LOADED:
        return

    profiles_by_uri: Dict[str, Dict[str, Any]] = {}
    profiles: Dict[Tuple[str, str], Dict[str, Any]] = {}
    if _PROFILES_PATH.exists():
        with _PROFILES_PATH.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                s3_uri = str(obj.get("s3_uri") or "").strip()
                if s3_uri and s3_uri not in profiles_by_uri:
                    profiles_by_uri[s3_uri] = obj
                slug = str(obj.get("slug") or "").strip()
                filename = str(obj.get("filename") or "").strip()
                if slug and filename and (slug, filename) not in profiles:
                    profiles[(slug, filename)] = obj

    _PROFILE_BY_URI = profiles_by_uri
    _PROFILE_BY_SLUG_FILENAME = profiles
    _PROFILES_LOADED = True


def _apply_description_row(profile: Dict[str, Any], description_row: Optional[Dict[str, Any]]) -> None:
    if not description_row:
        return
    if description_row.get("description") and not profile.get("llm_description"):
        profile["llm_description"] = str(description_row["description"])


def _load_legacy_dataset_profile(s3_uri: str, search_wrapper_module) -> Optional[Dict[str, Any]]:
    """Fall back to the ideal-search wrapper's schema/description/snippet caches."""
    try:
        search_wrapper_module._load_schemas_cache()
        search_wrapper_module._load_desc_cache()
        search_wrapper_module._load_snippet_cache()
    except FileNotFoundError:
        return None
    except Exception:
        return None

    schema = search_wrapper_module._lookup_schema(s3_uri)
    description = search_wrapper_module._DESC_BY_URI.get(s3_uri)
    description_row = getattr(search_wrapper_module, "_DESC_ROW_BY_URI", {}).get(s3_uri)
    snippet = search_wrapper_module._SNIPPET_BY_URI.get(s3_uri)

    if schema is None and description is None and description_row is None and snippet is None:
        return None

    profile: Dict[str, Any] = {}
    if schema is not None:
        profile["schema_columns"] = schema.get("columns")
        profile["table_kind"] = schema.get("kind")
    if description is not None:
        profile["llm_description"] = description
    _apply_description_row(profile, description_row)
    if snippet is not None:
        profile["snippet"] = snippet
    return profile


def load_dataset_profile(s3_uri: str) -> Optional[Dict[str, Any]]:
    """Look up cached profile for a dataset file URI. Returns None if no cache hit.

    Tries precomputed profile rows first, then falls back to the legacy
    schema/description/snippet bundle from the ideal-search wrapper.
    """
    try:
        from strands_evaluation.tools.external.ideal import search_wrapper as _sw
    except Exception:
        _sw = None

    try:
        _load_profiles_cache()
    except Exception:
        pass
    else:
        profile = _PROFILE_BY_URI.get(s3_uri)
        if profile is not None:
            merged = dict(profile)
            if _sw is not None:
                _apply_description_row(
                    merged, getattr(_sw, "_DESC_ROW_BY_URI", {}).get(s3_uri)
                )
            return merged
        if _sw is not None:
            try:
                key = _sw._slug_stem_from_uri(s3_uri)
            except Exception:
                key = None
            if key is not None:
                profile = _PROFILE_BY_SLUG_FILENAME.get(key)
                if profile is not None:
                    merged = dict(profile)
                    _apply_description_row(
                        merged, getattr(_sw, "_DESC_ROW_BY_URI", {}).get(s3_uri)
                    )
                    return merged

    if _sw is None:
        return None
    return _load_legacy_dataset_profile(s3_uri, _sw)


__all__ = ["load_dataset_profile"]

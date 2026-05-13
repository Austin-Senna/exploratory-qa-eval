"""Shared raw dataset-profile lookup for profile-aware tools.

The canonical profile artifact is repo-root ``datagov_tables_profiles.jsonl``.
Rows are returned as stored; callers that need schema/snippet fallbacks should
layer those fallbacks outside this loader.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


_PROFILES_PATH = Path(__file__).resolve().parents[2] / "datagov_tables_profiles.jsonl"

_PROFILE_BY_URI: Dict[str, Dict[str, Any]] = {}
_PROFILE_BY_SLUG_FILENAME: Dict[Tuple[str, str], Dict[str, Any]] = {}
_PROFILES_LOADED: bool = False


def _stem(name: str) -> str:
    value = str(name or "").strip().rsplit("/", 1)[-1]
    return value.rsplit(".", 1)[0] if "." in value else value


def _slug_stem_from_uri(uri: str) -> Optional[Tuple[str, str]]:
    raw = str(uri or "").strip()
    if not raw:
        return None
    if "://" in raw:
        raw = raw.split("://", 1)[1]
        if "/" not in raw:
            return None
        raw = raw.split("/", 1)[1]
    parts = raw.split("/")
    if len(parts) < 4 or parts[0] != "datagov":
        return None
    slug = parts[1]
    if "files" not in parts:
        return None
    idx = parts.index("files")
    if idx + 1 >= len(parts):
        return None
    filename = parts[idx + 1]
    return (slug, _stem(filename))


def _profile_key_from_row(obj: Dict[str, Any]) -> Optional[Tuple[str, str]]:
    slug = str(obj.get("slug") or obj.get("dataset_slug") or obj.get("dataset_id") or "").strip()
    filename = str(obj.get("filename") or obj.get("file_path") or obj.get("relative_path") or "").strip()
    if not slug or not filename:
        return None
    return (slug, _stem(filename))


def _load_profiles_cache() -> None:
    """Load raw precomputed dataset profiles into in-process caches."""
    global _PROFILES_LOADED, _PROFILE_BY_URI, _PROFILE_BY_SLUG_FILENAME
    if _PROFILES_LOADED:
        return

    profiles_by_uri: Dict[str, Dict[str, Any]] = {}
    profiles_by_slug_filename: Dict[Tuple[str, str], Dict[str, Any]] = {}
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
                if not isinstance(obj, dict):
                    continue
                s3_uri = str(obj.get("s3_uri") or "").strip()
                if s3_uri and s3_uri not in profiles_by_uri:
                    profiles_by_uri[s3_uri] = obj
                key = _profile_key_from_row(obj)
                if key is not None and key not in profiles_by_slug_filename:
                    profiles_by_slug_filename[key] = obj

    _PROFILE_BY_URI = profiles_by_uri
    _PROFILE_BY_SLUG_FILENAME = profiles_by_slug_filename
    _PROFILES_LOADED = True


def load_dataset_profile(s3_uri: str) -> Optional[Dict[str, Any]]:
    """Return a raw cached profile for a dataset file URI, or None."""
    if not s3_uri:
        return None
    _load_profiles_cache()
    profile = _PROFILE_BY_URI.get(str(s3_uri))
    if profile is not None:
        return dict(profile)
    key = _slug_stem_from_uri(str(s3_uri))
    if key is None:
        return None
    profile = _PROFILE_BY_SLUG_FILENAME.get(key)
    if profile is None:
        return None
    return dict(profile)


__all__ = ["load_dataset_profile"]

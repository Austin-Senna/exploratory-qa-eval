"""Search tool wrappers for multi-axis ablation experiments.

This module wraps search tools to control:
1) Fixed result limits (k)
2) Search result payload richness (naive | standard | ideal)
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from strands import tool
from strands.tools.decorator import DecoratedFunctionTool

logger = logging.getLogger(__name__)

_QUERY_TOOLS = {"search_value", "search_schema", "search_reranked", "search_ideal"}
_PREFIX_TOOLS = {"search_prefix"}
_SEARCH_TOOL_NAMES = _QUERY_TOOLS | _PREFIX_TOOLS

_IDEAL_SNIPPET_WORDS = 100

_TABLE_DESCRIPTIONS_PATH = Path("table_descriptions.jsonl")
_SCHEMAS_PATH = Path("datagov_tables_schemas_full.jsonl")

_DESC_CACHE_LOADED = False
_DESC_BY_URI: Dict[str, str] = {}

_SCHEMAS_CACHE_LOADED = False
_SCHEMA_BY_SLUG_FILENAME: Dict[Tuple[str, str], str] = {}


def _dataset_id_from_uri(uri: str) -> Optional[str]:
    raw = str(uri or "")
    if "://" not in raw:
        return None
    try:
        # s3://bucket/<folder>/<dataset_id>/...
        tail = raw.split("://", 1)[1]
        parts = tail.split("/")
        if len(parts) >= 3:
            return parts[2]
    except Exception:
        return None
    return None


def _first_non_empty(values: Iterable[Optional[str]]) -> Optional[str]:
    for value in values:
        if value:
            return str(value)
    return None


def _extract_uri(item: Dict[str, Any]) -> Optional[str]:
    return _first_non_empty([item.get("dataset_uri"), item.get("uri")])


def _extract_dataset_id(item: Dict[str, Any]) -> Optional[str]:
    dsid = _first_non_empty([item.get("dataset_id")])
    if dsid:
        return dsid
    uri = _extract_uri(item)
    if uri:
        return _dataset_id_from_uri(uri)
    return None


def _extract_search_text(item: Dict[str, Any]) -> str:
    text = _first_non_empty([item.get("document"), item.get("text"), item.get("content")])
    return text or ""


def _truncate_words(text: str, max_words: int) -> str:
    words = (text or "").split()
    if len(words) <= max_words:
        return " ".join(words)
    return " ".join(words[:max_words])


def _reshape_source_driven_row(row: Dict[str, Any], mode: str) -> Dict[str, Any]:
    dataset_id = _extract_dataset_id(row)
    if mode == "naive":
        out: Dict[str, Any] = {}
        if dataset_id:
            out["dataset_id"] = dataset_id
        return out

    out = {}
    if dataset_id:
        out["dataset_id"] = dataset_id

    uri = _extract_uri(row)
    if uri:
        out["uri"] = uri

    description = _first_non_empty([row.get("description")])
    if description:
        out["description"] = description

    content = _first_non_empty([row.get("content"), row.get("snippet"), row.get("document")])
    if content:
        if mode == "ideal":
            out["dataset_snippet"] = _truncate_words(content, max_words=_IDEAL_SNIPPET_WORDS)
        else:
            out["content"] = _truncate_words(content, max_words=200)

    return out


def _load_desc_cache() -> None:
    global _DESC_CACHE_LOADED, _DESC_BY_URI
    if _DESC_CACHE_LOADED:
        return

    if not _TABLE_DESCRIPTIONS_PATH.exists():
        raise FileNotFoundError(
            f"Required dependency '{_TABLE_DESCRIPTIONS_PATH}' not found. "
            "search_results=ideal enrichment requires table_descriptions.jsonl at the repo root."
        )

    _DESC_CACHE_LOADED = True
    uri_map: Dict[str, str] = {}
    with _TABLE_DESCRIPTIONS_PATH.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            uri = str(obj.get("dataset_uri") or obj.get("uri") or "").strip()
            desc = str(obj.get("description") or "").strip()
            if uri and desc and uri not in uri_map:
                uri_map[uri] = desc

    _DESC_BY_URI = uri_map


def _slug_filename_from_uri(uri: str) -> Optional[Tuple[str, str]]:
    """Derive (dataset_slug, filename) from either a full s3:// URI or a versioned s3_key."""
    raw = (uri or "").strip()
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
    return (slug, parts[idx + 1])


def _format_schema_text(table: Dict[str, Any]) -> str:
    rel = str(table.get("relative_path") or "").strip() or "?"
    kind = str(table.get("table_kind") or "").strip() or "unknown"
    columns = table.get("columns") or []
    column_list = ", ".join(str(c) for c in columns) if isinstance(columns, list) else ""
    delimiter = table.get("delimiter")

    header = f"table: {rel} ({kind}"
    if isinstance(delimiter, str) and delimiter:
        header += f', delimiter="{delimiter}"'
    header += ")"
    if column_list:
        return f"{header}\ncolumns: {column_list}"
    return header


def _load_schemas_cache() -> None:
    global _SCHEMAS_CACHE_LOADED, _SCHEMA_BY_SLUG_FILENAME
    if _SCHEMAS_CACHE_LOADED:
        return

    if not _SCHEMAS_PATH.exists():
        raise FileNotFoundError(
            f"Required dependency '{_SCHEMAS_PATH}' not found. "
            "search_results=ideal with a non-ideal search_tool requires "
            "datagov_tables_schemas_full.jsonl at the repo root."
        )

    cache: Dict[Tuple[str, str], str] = {}
    with _SCHEMAS_PATH.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            slug = str(obj.get("dataset_slug") or "").strip()
            if not slug:
                continue
            tables = obj.get("tables") or []
            if not isinstance(tables, list):
                continue
            for table in tables:
                if not isinstance(table, dict):
                    continue
                rel = str(table.get("relative_path") or "").strip()
                if not rel:
                    continue
                filename = rel.rsplit("/", 1)[-1]
                key = (slug, filename)
                if key in cache:
                    continue
                cache[key] = _format_schema_text(table)

    _SCHEMA_BY_SLUG_FILENAME = cache
    _SCHEMAS_CACHE_LOADED = True


def _lookup_schema_text(uri: str) -> Optional[str]:
    key = _slug_filename_from_uri(uri)
    if key is None:
        return None
    _load_schemas_cache()
    return _SCHEMA_BY_SLUG_FILENAME.get(key)


def reshape_search_payload(payload: Any, mode: str) -> Any:
    """Transform a search payload into naive/standard/ideal result richness."""
    normalized = str(mode or "standard").strip().lower()
    if normalized not in {"naive", "standard", "ideal"}:
        raise ValueError(f"Unsupported search_results mode '{mode}'. Expected: naive|standard|ideal")

    if not isinstance(payload, dict):
        return payload
    if "results" not in payload or not isinstance(payload["results"], list):
        return payload

    source_driven = bool(payload.get("ideal_source_driven"))

    if normalized == "ideal" and not source_driven:
        _load_desc_cache()

    shaped: List[Any] = []
    for row in payload["results"]:
        if not isinstance(row, dict):
            shaped.append(row)
            continue

        if source_driven:
            shaped.append(_reshape_source_driven_row(row, normalized))
            continue

        uri = _extract_uri(row)
        dataset_id = _extract_dataset_id(row)

        if normalized == "naive":
            out: Dict[str, Any] = {}
            if uri:
                out["uri"] = uri
            shaped.append(out)
            continue

        if normalized == "standard":
            snippet = _truncate_words(_extract_search_text(row), max_words=200)
            score = row.get("score")
            out = {}
            if uri:
                out["uri"] = uri
            if dataset_id:
                out["dataset_id"] = dataset_id
            if score is not None:
                out["score"] = score
            if snippet:
                out["snippet"] = snippet
            shaped.append(out)
            continue

        # ideal
        desc = _DESC_BY_URI.get(uri or "", "")
        schema = _lookup_schema_text(uri) if uri else None
        snippet = _truncate_words(_extract_search_text(row), max_words=_IDEAL_SNIPPET_WORDS)

        out = {}
        if uri:
            out["uri"] = uri
        if dataset_id:
            out["dataset_id"] = dataset_id
        if desc:
            out["description"] = desc
        if schema:
            out["schema"] = schema
        if snippet:
            out["dataset_snippet"] = snippet
        shaped.append(out)

    transformed = dict(payload)
    transformed["results"] = shaped
    transformed["count"] = len(shaped)
    return transformed


def _query_default(spec: Dict[str, Any], field_name: str, fallback: int) -> int:
    try:
        props = spec.get("inputSchema", {}).get("json", {}).get("properties", {})
        if field_name in props and "default" in props[field_name]:
            return int(props[field_name]["default"])
    except Exception:
        pass
    return fallback


def _compose_description(
    base_description: str,
    *,
    tool_name: str,
    fixed_k: Optional[int],
    mode: str,
) -> str:
    desc = base_description.strip()
    notes: List[str] = []
    if fixed_k is not None:
        if tool_name == "search_ideal":
            notes.append(f"Each call returns up to {fixed_k} planned sources from source_sequence; callers cannot change the call signature.")
        else:
            notes.append(f"Result limit is fixed at {fixed_k}; callers cannot change it.")
    notes.append(f"Result payload mode: {mode}.")
    return f"{desc} {' '.join(notes)}".strip()


def _wrap_query_tool(
    base_tool: DecoratedFunctionTool,
    *,
    fixed_k: Optional[int],
    mode: str,
) -> DecoratedFunctionTool:
    spec = base_tool.tool_spec
    tool_name = spec["name"]
    wrapped_description = _compose_description(
        spec.get("description", ""),
        tool_name=tool_name,
        fixed_k=fixed_k,
        mode=mode,
    )
    top_k_default = _query_default(spec, "top_k", 10)

    if fixed_k is not None:
        def _wrapped(query: str) -> dict:
            return reshape_search_payload(base_tool(query=query, top_k=fixed_k), mode)

        return tool(_wrapped, name=tool_name, description=wrapped_description)

    def _wrapped(query: str, top_k: int = top_k_default) -> dict:
        return reshape_search_payload(base_tool(query=query, top_k=top_k), mode)

    return tool(_wrapped, name=tool_name, description=wrapped_description)


def _wrap_prefix_tool(
    base_tool: DecoratedFunctionTool,
    *,
    fixed_k: Optional[int],
    mode: str,
) -> DecoratedFunctionTool:
    spec = base_tool.tool_spec
    tool_name = spec["name"]
    wrapped_description = _compose_description(
        spec.get("description", ""),
        tool_name=tool_name,
        fixed_k=fixed_k,
        mode=mode,
    )
    limit_default = _query_default(spec, "limit", 50)

    if fixed_k is not None:
        def _wrapped(prefixes: List[str]) -> dict:
            return reshape_search_payload(base_tool(prefixes=prefixes, limit=fixed_k), mode)

        return tool(_wrapped, name=tool_name, description=wrapped_description)

    def _wrapped(prefixes: List[str], limit: int = limit_default) -> dict:
        return reshape_search_payload(base_tool(prefixes=prefixes, limit=limit), mode)

    return tool(_wrapped, name=tool_name, description=wrapped_description)


def build_search_tools(
    base_tools: Sequence[DecoratedFunctionTool],
    *,
    fixed_k: Optional[int],
    results_mode: str,
) -> List[DecoratedFunctionTool]:
    """Return search tools wrapped with k-control and payload shaping."""
    mode = str(results_mode or "standard").strip().lower()
    if mode not in {"naive", "standard", "ideal"}:
        raise ValueError(
            f"Unsupported results_mode '{results_mode}'. Expected: naive|standard|ideal"
        )

    wrapped: List[DecoratedFunctionTool] = []
    for tool_obj in base_tools:
        tool_name = tool_obj.tool_spec.get("name", "")
        if tool_name in _QUERY_TOOLS:
            wrapped.append(_wrap_query_tool(tool_obj, fixed_k=fixed_k, mode=mode))
        elif tool_name in _PREFIX_TOOLS:
            wrapped.append(_wrap_prefix_tool(tool_obj, fixed_k=fixed_k, mode=mode))
        else:
            wrapped.append(tool_obj)
    return wrapped


def search_tool_names_in(tools: Sequence[DecoratedFunctionTool]) -> Tuple[str, ...]:
    names = [
        t.tool_spec["name"]
        for t in tools
        if t.tool_spec.get("name") in _SEARCH_TOOL_NAMES
    ]
    return tuple(dict.fromkeys(names))

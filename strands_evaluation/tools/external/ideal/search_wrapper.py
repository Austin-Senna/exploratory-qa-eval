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

_TABLE_DESCRIPTIONS_PATH = Path("table_descriptions.jsonl")
_SCHEMA_DB_PATH = Path("lance_table_descriptions")

_DESC_CACHE_LOADED = False
_DESC_BY_URI: Dict[str, str] = {}

_SCHEMA_TABLE_INIT = False
_SCHEMA_TABLE = None
_SCHEMA_BY_URI: Dict[str, Optional[str]] = {}


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
        out["content"] = _truncate_words(content, max_words=200)

    return out


def _load_desc_cache() -> None:
    global _DESC_CACHE_LOADED, _DESC_BY_URI
    if _DESC_CACHE_LOADED:
        return
    _DESC_CACHE_LOADED = True

    if not _TABLE_DESCRIPTIONS_PATH.exists():
        logger.warning(
            "table_descriptions.jsonl not found at '%s'; ideal payload description will be empty.",
            _TABLE_DESCRIPTIONS_PATH,
        )
        return

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


def _init_schema_table() -> None:
    global _SCHEMA_TABLE_INIT, _SCHEMA_TABLE
    if _SCHEMA_TABLE_INIT:
        return
    _SCHEMA_TABLE_INIT = True

    if not _SCHEMA_DB_PATH.exists():
        logger.warning(
            "Schema index path '%s' not found; ideal payload schema will be empty.",
            _SCHEMA_DB_PATH,
        )
        return

    try:
        import lancedb

        db = lancedb.connect(str(_SCHEMA_DB_PATH))
        _SCHEMA_TABLE = db.open_table("lakeqa_schema")
    except Exception as exc:
        logger.warning("Could not initialize schema index: %s", exc)
        _SCHEMA_TABLE = None


def _lookup_schema_text(uri: str) -> Optional[str]:
    if uri in _SCHEMA_BY_URI:
        return _SCHEMA_BY_URI[uri]

    _init_schema_table()
    if _SCHEMA_TABLE is None:
        _SCHEMA_BY_URI[uri] = None
        return None

    try:
        escaped = uri.replace("'", "''")
        rows = _SCHEMA_TABLE.search().where(f"uri = '{escaped}'").limit(1).select(["text"]).to_list()
        schema_text = str(rows[0].get("text", "")).strip() if rows else ""
    except Exception:
        schema_text = ""

    _SCHEMA_BY_URI[uri] = schema_text or None
    return _SCHEMA_BY_URI[uri]


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

        out = {}
        if uri:
            out["uri"] = uri
        if dataset_id:
            out["dataset_id"] = dataset_id
        if desc:
            out["description"] = desc
        if schema:
            out["schema"] = schema
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

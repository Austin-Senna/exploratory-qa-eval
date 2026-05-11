"""Source-session helpers for sprint commitment mode."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


SOURCE_SESSION_TOOLS = {
    "list_files",
    "peek_file",
    "peek_multiple",
    "read_file",
    "grep_file",
    "parse_xml_records",
    "query_file",
    "query_ideal",
    "download",
    "execute_code",
    "execute_ideal",
}

_S3_DATASET_RE = re.compile(
    r"^s3://[^/]+/(?:datagov|wikipedia)/(?P<dataset_id>[^/]+)/"
)
_RELATIVE_DATASET_RE = re.compile(
    r"^(?:datagov|wikipedia)/(?P<dataset_id>[^/]+)/"
)


def _clean_source(value: Any) -> Optional[str]:
    if not isinstance(value, str):
        return None
    value = value.strip().strip("/")
    for prefix in ("datagov/", "wikipedia/"):
        if value.startswith(prefix):
            value = value[len(prefix):]
    return value or None


def _source_from_s3_uri(uri: Any) -> Optional[str]:
    if not isinstance(uri, str):
        return None
    value = uri.strip().strip("/")
    if not value:
        return None
    for pattern in (_S3_DATASET_RE, _RELATIVE_DATASET_RE):
        match = pattern.match(value)
        if match:
            return match.group("dataset_id")
    return None


def _source_from_files(files: Any) -> Optional[str]:
    if isinstance(files, dict):
        files = [files]
    if not isinstance(files, list) or not files:
        return None

    sources: List[str] = []
    for item in files:
        if isinstance(item, str):
            source = _source_from_s3_uri(item)
        elif isinstance(item, dict):
            source = _clean_source(item.get("dataset_id")) or _source_from_s3_uri(
                item.get("s3_uri") or item.get("uri")
            )
        else:
            source = None
        if source:
            sources.append(source)

    unique = sorted(set(sources))
    if not unique:
        return None
    if len(unique) == 1:
        return unique[0]
    return "multi:" + ",".join(unique)


def source_from_tool_use(
    tool_use: Dict[str, Any],
    *,
    fallback_source: Optional[str] = None,
) -> Optional[str]:
    """Return canonical source id for a tool call, if source-bearing."""

    tool_name = (tool_use or {}).get("name", "")
    if tool_name not in SOURCE_SESSION_TOOLS:
        return None

    tool_input = (tool_use or {}).get("input", {}) or {}

    if tool_name == "execute_code":
        return fallback_source

    source = _clean_source(tool_input.get("dataset_id"))
    if source:
        return source

    dataset_ids = tool_input.get("dataset_ids")
    if isinstance(dataset_ids, list) and dataset_ids:
        cleaned = sorted(set(filter(None, (_clean_source(v) for v in dataset_ids))))
        if len(cleaned) == 1:
            return cleaned[0]
        if len(cleaned) > 1:
            return "multi:" + ",".join(cleaned)

    source = _source_from_s3_uri(tool_input.get("s3_uri") or tool_input.get("uri"))
    if source:
        return source

    source = _source_from_files(tool_input.get("files") or tool_input.get("entries"))
    if source:
        return source

    if tool_name == "execute_ideal":
        return fallback_source
    return None


@dataclass
class SourceSessionState:
    current_source: str
    commitment_goal: str
    max_source_calls: int
    plan_step: str = ""
    success_condition: str = ""
    related_sources: List[str] = field(default_factory=list)
    calls_used: int = 0
    tools_used: List[str] = field(default_factory=list)

    def _source_package(self) -> set[str]:
        return {self.current_source, *self.related_sources}

    def contains_source(self, source: Optional[str]) -> bool:
        if source is None:
            return False
        if source.startswith("multi:"):
            parts = [part for part in source[len("multi:") :].split(",") if part]
            return bool(parts) and all(part in self._source_package() for part in parts)
        return source in self._source_package()

    def record_call(self, tool_name: str) -> None:
        self.calls_used += 1
        if tool_name:
            self.tools_used.append(tool_name)

    def is_budget_exhausted(self) -> bool:
        return self.calls_used >= self.max_source_calls

    def describe(self) -> str:
        source_line = (
            f"source_session: {self.current_source} | "
            f"source_calls: {self.calls_used}/{self.max_source_calls}"
        )
        if not self.commitment_goal:
            return source_line
        return source_line + f"\nsource_goal: {self.commitment_goal}"


__all__ = ["SOURCE_SESSION_TOOLS", "SourceSessionState", "source_from_tool_use"]

"""
Aurum v2 Tools for LLM Agent

Provides schema/value/join search tools backed by the Aurum v2 index:
  - search_value  — find columns whose data values match a query
  - search_field  — find columns/tables whose names match a query
  - neighbor      — find cross-table pk/fk, content, or schema relationships
"""
from strands import tool
from pathlib import Path
from typing import Any, Dict, Optional

# ---------------------------------------------------------------------------
# Lazy singleton for the Aurum AgentAPI
# ---------------------------------------------------------------------------

_aurum_agent: Any = None


def _get_aurum_agent():
    """Lazily initialise the Aurum AgentAPI singleton."""
    global _aurum_agent
    if _aurum_agent is None:
        import sys as _sys
        _repo_root = str(Path(__file__).resolve().parent.parent.parent)
        if _repo_root not in _sys.path:
            _sys.path.insert(0, _repo_root)
        from aurum_v2 import init_agent
        from strands_evaluation.config import AurumConfig
        _aurum_config = AurumConfig()
        _aurum_agent = init_agent(_aurum_config.graph_path, _aurum_config.db_path)
    return _aurum_agent


# ---------------------------------------------------------------------------
# Tool functions
# ---------------------------------------------------------------------------
@tool
def search_value(
    query: str,
    top_k: int = 10,
    dedup_tables: bool = False,
) -> Dict[str, Any]:
    """Find columns whose actual data *values* match the query.

    Use this to locate which datasets contain a specific data point,
    e.g. the city "Los Angeles" appearing in rows.

    Args:
        query: The specific data value to search for.
        top_k: Maximum number of results to return (default is 10).
        dedup_tables: If True, returns only one result per table.
    """
    try:
        results = _get_aurum_agent().search_value(query, top_k=top_k, dedup_tables=dedup_tables)
        return {"results": results, "count": len(results), "query": query}
    except Exception as e:
        return {"error": str(e), "query": query}

@tool
def search_field(
    query: str,
    top_k: int = 10,
    dedup_tables: bool = True,
) -> Dict[str, Any]:
    """Find columns or tables whose *names* (schema) match the query.

    Use this when looking for tables that have a specific column name,
    e.g. "population" or "federalShareObligated".

    Returns a list of ``{table, column, score}`` dicts sorted by relevance.
    """
    try:
        results = _get_aurum_agent().search_field(query, top_k=top_k, dedup_tables=dedup_tables)
        return {"results": results, "count": len(results), "query": query}
    except Exception as e:
        return {"error": str(e), "query": query}

@tool
def search_field_and_value(
    field_query: str,
    value_query: str,
    top_k: int = 10,
) -> Dict[str, Any]:
    """Find columns matching the field_query that ALSO contain the value_query."""
    try:
        agent = _get_aurum_agent()
        field_results = agent.search_field(field_query, top_k=top_k * 2, dedup_tables=False)
        field_nids = {r["nid"] for r in field_results}
        value_results = agent.search_value(value_query, top_k=top_k * 2, dedup_tables=False)
        combined = [r for r in value_results if r["nid"] in field_nids][:top_k]
        return {"results": combined, "count": len(combined), "field_query": field_query, "value_query": value_query}
    except Exception as e:
        return {"error": str(e), "field_query": field_query, "value_query": value_query}

@tool
def neighbor(
    target_id: str,
    relation: str = "pkfk",
    top_k: Optional[int] = None,
) -> Dict[str, Any]:
    """Find cross-table relationships for a given table or column.

    Use this to discover joinable or related datasets.
    ``relation`` must be one of:
    - ``"pkfk"``    — strict primary/foreign-key links (best for joins)
    - ``"content"`` — columns with overlapping data values
    - ``"schema"``  — columns with similar names

    ``target_id`` is either a table name (``"dataset/file.csv"``) or a column
    network ID (``"dataset/file.csv.col_name"``).

    Returns a list of ``{table, column, score}`` dicts, same-table results excluded.
    """
    try:
        results = _get_aurum_agent().neighbor(target_id, relation=relation, top_k=top_k)
        return {"results": results, "count": len(results), "input": target_id, "relation": relation}
    except Exception as e:
        return {"error": str(e), "input": target_id, "relation": relation}


__all__ = ["search_value", "search_field", "search_field_and_value", "neighbor"]

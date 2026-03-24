"""Search tools for Condition A (tools-rich): hybrid RRF, schema, and reranked."""
import sys
from pathlib import Path

from strands import tool

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "external-tools" / "hybrid_search"))

from api import setup, hybrid_search, hybrid_search_schema, hybrid_search_with_reranker  # noqa: E402




@tool
def search_value(query: str, top_k: int = 10) -> dict:
    """Hybrid semantic + keyword search over dataset content (RRF reranking).

    Args:
        query: Natural-language query or topic.
        top_k: Maximum number of results to return (default 10).
    """
    try:
        results = hybrid_search(query, k=top_k)
        return {"results": results, "count": len(results), "query": query}
    except Exception as e:
        return {"error": str(e), "query": query, "results": [], "count": 0}


@tool
def search_schema(query: str, top_k: int = 10) -> dict:
    """Hybrid semantic + keyword search over dataset schemas (column names, types).

    Args:
        query: Natural-language query about schema structure.
        top_k: Maximum number of results to return (default 10).
    """
    try:
        results = hybrid_search_schema(query, k=top_k)
        return {"results": results, "count": len(results), "query": query}
    except Exception as e:
        return {"error": str(e), "query": query, "results": [], "count": 0}


@tool
def search_reranked(query: str, top_k: int = 10) -> dict:
    """Hybrid semantic + keyword search with cross-encoder reranking. Slower but more accurate.

    Args:
        query: Natural-language query or topic.
        top_k: Maximum number of results to return (default 10).
    """
    try:
        results = hybrid_search_with_reranker(query, k=top_k)
        return {"results": results, "count": len(results), "query": query}
    except Exception as e:
        return {"error": str(e), "query": query, "results": [], "count": 0}

"""Search tools for Condition B (planning-rich): sparse FTS only."""
import sys
from pathlib import Path

from strands import tool

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "external-tools" / "hybrid_search"))

from api import setup, sparse_search  # noqa: E402

setup()


@tool
def search_value(query: str, top_k: int = 10) -> dict:
    """Sparse keyword search over dataset content (FTS).

    Args:
        query: Keywords or short phrase to search for.
        top_k: Maximum number of results to return (default 10).
    """
    try:
        results = sparse_search(query, k=top_k)
        return {"results": results, "count": len(results), "query": query}
    except Exception as e:
        return {"error": str(e), "query": query, "results": [], "count": 0}

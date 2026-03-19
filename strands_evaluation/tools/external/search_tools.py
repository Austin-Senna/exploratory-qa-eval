"""
Search backend wrappers for Condition A (tools-rich) and Condition B (planning-rich).

Three @tool-decorated functions wrapping external-tools/ APIs:
  - search_sparse   — BM25 (default) or SPLADE sparse search
  - search_hybrid   — hybrid dense+sparse with reranker
  - search_graph    — RAG-Anything knowledge graph search
"""
import asyncio
import importlib.util
import os
import sys
from pathlib import Path
from typing import Any, Dict

from strands import tool

# Path to external-tools directory (mirrors aurum_tools.py pattern)
_EXTERNAL_TOOLS_DIR = str(Path(__file__).resolve().parent.parent.parent.parent / "external-tools")

_BM25_DIR = os.path.join(_EXTERNAL_TOOLS_DIR, "simple_bm25")
_HYBRID_DIR = os.path.join(_EXTERNAL_TOOLS_DIR, "simple_hybrid_search")
_RAG_DIR = os.path.join(_EXTERNAL_TOOLS_DIR, "rag-anything")


def _load_api(module_dir: str, cache_name: str):
    """Load api.py from a specific directory by absolute path, bypassing module cache."""
    cached = sys.modules.get(cache_name)
    if cached:
        return cached
    spec = importlib.util.spec_from_file_location(
        cache_name, os.path.join(module_dir, "api.py")
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules[cache_name] = mod
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Lazy singletons — one per backend
# ---------------------------------------------------------------------------

_rag_initialized = False


def _ensure_rag():
    global _rag_initialized
    if not _rag_initialized:
        if _RAG_DIR not in sys.path:
            sys.path.insert(0, _RAG_DIR)
        _rag_initialized = True


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@tool
def search_sparse(query: str, top_k: int = 10) -> Dict[str, Any]:
    """Keyword/sparse search over the data catalog.

    Finds datasets whose metadata text matches the query keywords.
    Use for precise keyword lookups, dataset names, or known field names.

    Controlled by SEARCH_SPARSE_BACKEND env var:
      - "bm25"   (default) — DuckDB FTS / BM25
      - "splade" — SPLADE sparse neural search via ChromaDB

    Args:
        query: Keywords or short phrase to search for.
        top_k: Maximum number of results to return (default 10).
    """
    backend = os.environ.get("SEARCH_SPARSE_BACKEND", "bm25").lower()
    try:
        if backend == "splade":
            hybrid_api = _load_api(_HYBRID_DIR, "hybrid_api")
            raw = hybrid_api.sparse_search(query, k=top_k)
            results = [
                {"dataset_uri": r.get("uri", ""), "score": float(r.get("score", 0))}
                for r in raw
            ]
        else:
            bm25_api = _load_api(_BM25_DIR, "bm25_api")
            raw = bm25_api.search_keyword(query, top_k=top_k)
            results = [
                {"dataset_uri": r.get("dataset_uri", ""), "score": float(r.get("relevance_score", 0))}
                for r in raw
            ]
        return {"results": results, "count": len(results), "query": query, "backend": backend}
    except Exception as e:
        return {"error": str(e), "query": query, "backend": backend, "results": [], "count": 0}


@tool
def search_hybrid(query: str, top_k: int = 10) -> Dict[str, Any]:
    """Hybrid semantic + keyword search with reranking over the data catalog.

    Combines dense vector search and sparse keyword search, then reranks
    results. Best for natural-language queries when keyword search misses.

    Args:
        query: Natural-language query or topic.
        top_k: Maximum number of results to return (default 10).
    """
    try:
        hybrid_api = _load_api(_HYBRID_DIR, "hybrid_api")
        raw = hybrid_api.hybrid_search_with_reranker(query, k=top_k)
        results = [
            {"dataset_uri": r.get("uri", ""), "score": float(r.get("score", 0))}
            for r in raw
        ]
        return {"results": results, "count": len(results), "query": query}
    except Exception as e:
        return {"error": str(e), "query": query, "results": [], "count": 0}


@tool
def search_graph(query: str) -> Dict[str, Any]:
    """Knowledge-graph semantic search over the data catalog (RAG-Anything).

    Traverses the indexed knowledge graph built from dataset metadata.
    Best for relational or exploratory queries: 'datasets about X related to Y'.
    Returns a synthesised natural-language answer, not a ranked list.

    Args:
        query: Natural-language question or topic.
    """
    try:
        _ensure_rag()
        from agentapi import search_data_catalog  # rag-anything/agentapi.py
        answer = asyncio.run(search_data_catalog(query_text=query, search_depth="mix"))
        return {"results": str(answer), "query": query}
    except Exception as e:
        return {"error": str(e), "query": query, "results": ""}


__all__ = ["search_sparse", "search_hybrid", "search_graph"]

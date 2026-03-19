#!/usr/bin/env python3
"""
Behavioral analysis:
  - Condition A: tool switching patterns (which backends used per task, in what order)
  - Condition B: query drift via Jaccard/cosine similarity between consecutive queries

Usage:
    python analysis/behavioral.py [--sidecar-dir results/sidecar] [--condition a|b]
"""
import argparse
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path


def tokenize(text: str) -> set:
    return set(re.findall(r"\w+", text.lower()))


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def cosine_tf(a: list, b: list) -> float:
    """Cosine similarity using TF vectors from token lists."""
    def tf(tokens):
        c: Counter = Counter(tokens)
        return c

    ca = tf(a)
    cb = tf(b)
    vocab = set(ca) | set(cb)
    dot = sum(ca[w] * cb[w] for w in vocab)
    mag_a = math.sqrt(sum(v**2 for v in ca.values()))
    mag_b = math.sqrt(sum(v**2 for v in cb.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def load_sidecar_traces(sidecar_dir: str) -> dict[str, list]:
    traces: dict = defaultdict(list)
    for jsonl_path in Path(sidecar_dir).rglob("*.jsonl"):
        task_id = jsonl_path.stem
        with open(jsonl_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    traces[task_id].append(json.loads(line))
    return dict(traces)


def analyze_tool_switching(traces: dict[str, list]) -> dict:
    """Condition A: tool switching patterns per task."""
    switch_counts: list = []
    backend_sequences: list = []

    for task_id, task_traces in traces.items():
        sorted_traces = sorted(task_traces, key=lambda t: t.get("turn", 0))
        backends = [t.get("tool", "?") for t in sorted_traces]
        backend_sequences.append(backends)

        # Count switches (consecutive different backends)
        switches = sum(1 for i in range(1, len(backends)) if backends[i] != backends[i-1])
        switch_counts.append(switches)

    n = len(switch_counts)
    backend_usage: Counter = Counter()
    for seq in backend_sequences:
        backend_usage.update(set(seq))  # unique per task

    return {
        "n_tasks": n,
        "avg_switches": sum(switch_counts) / n if n else 0.0,
        "max_switches": max(switch_counts) if switch_counts else 0,
        "backend_task_coverage": dict(backend_usage),
    }


def analyze_query_drift(traces: dict[str, list]) -> dict:
    """Condition B: query reformulation drift via Jaccard and cosine."""
    jaccard_scores: list = []
    cosine_scores: list = []
    drift_per_task: list = []

    for task_id, task_traces in traces.items():
        sorted_traces = sorted(task_traces, key=lambda t: t.get("turn", 0))
        queries = [t.get("query", "") for t in sorted_traces if t.get("query")]
        if len(queries) < 2:
            continue

        task_jaccards = []
        task_cosines = []
        for i in range(1, len(queries)):
            tok_a = list(tokenize(queries[i-1]))
            tok_b = list(tokenize(queries[i]))
            j = jaccard(set(tok_a), set(tok_b))
            c = cosine_tf(tok_a, tok_b)
            task_jaccards.append(j)
            task_cosines.append(c)

        avg_j = sum(task_jaccards) / len(task_jaccards)
        avg_c = sum(task_cosines) / len(task_cosines)
        jaccard_scores.append(avg_j)
        cosine_scores.append(avg_c)
        drift_per_task.append({
            "task_id": task_id,
            "num_queries": len(queries),
            "avg_jaccard": avg_j,
            "avg_cosine": avg_c,
        })

    n = len(jaccard_scores)
    return {
        "n_tasks": n,
        "avg_jaccard_similarity": sum(jaccard_scores) / n if n else None,
        "avg_cosine_similarity": sum(cosine_scores) / n if n else None,
        "drift_per_task": drift_per_task,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sidecar-dir", default="results/sidecar")
    parser.add_argument("--condition", choices=["a", "b", "both"], default="both")
    args = parser.parse_args()

    traces = load_sidecar_traces(args.sidecar_dir)
    print(f"Loaded traces for {len(traces)} tasks from {args.sidecar_dir}")

    if args.condition in ("a", "both"):
        print("\n=== Condition A: Tool Switching ===")
        sw = analyze_tool_switching(traces)
        print(f"  Tasks analyzed:        {sw['n_tasks']}")
        print(f"  Avg tool switches/task: {sw['avg_switches']:.2f}")
        print(f"  Max switches in a task: {sw['max_switches']}")
        print(f"  Backend coverage (tasks using each):")
        for b, n in sorted(sw["backend_task_coverage"].items()):
            print(f"    {b:<22}: {n}")

    if args.condition in ("b", "both"):
        print("\n=== Condition B: Query Drift ===")
        drift = analyze_query_drift(traces)
        n = drift["n_tasks"]
        avg_j = drift["avg_jaccard_similarity"]
        avg_c = drift["avg_cosine_similarity"]
        print(f"  Tasks with 2+ queries:  {n}")
        print(f"  Avg Jaccard similarity: {avg_j:.3f}" if avg_j is not None else "  Avg Jaccard similarity: N/A")
        print(f"  Avg Cosine similarity:  {avg_c:.3f}" if avg_c is not None else "  Avg Cosine similarity:  N/A")
        print("  (Lower = more query drift/reformulation)")


if __name__ == "__main__":
    main()

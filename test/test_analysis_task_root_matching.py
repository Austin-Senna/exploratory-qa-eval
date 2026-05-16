import json
import tempfile
from pathlib import Path

from analysis.discovery_metrics import compute_discovery_metrics, load_task_gold_ids
from analysis.provenance import compute_provenance
from analysis.reasoning_density import compute_reasoning_density_curve
from analysis.search_bottleneck import compute_search_bottleneck


def test_discovery_does_not_match_explicit_trace_to_wrong_task_root() -> None:
    traces = {
        "k-1-d-1/task_1": [
            {
                "task_id": "tasks_mini/k-1-d-1/task_1.json",
                "tool": "search_ideal",
                "result_dataset_ids": ["right-dataset"],
            },
            {
                "task_id": "tasks_mini/k-1-d-1/task_1.json",
                "tool": "query_file",
                "read_dataset_ids": ["right-dataset"],
            },
        ]
    }
    wrong_root_gold = {
        "tasks_core_quality/k-1-d-1/task_1.json": ["wrong-dataset"],
    }

    metrics = compute_discovery_metrics(traces, wrong_root_gold)

    assert metrics == {"task_metrics": [], "aggregate": {}}


def test_discovery_matches_explicit_trace_to_same_task_root() -> None:
    traces = {
        "k-1-d-1/task_1": [
            {
                "task_id": "tasks_mini/k-1-d-1/task_1.json",
                "tool": "search_ideal",
                "result_dataset_ids": ["right-dataset"],
            },
            {
                "task_id": "tasks_mini/k-1-d-1/task_1.json",
                "tool": "query_file",
                "read_dataset_ids": ["right-dataset"],
            },
        ]
    }
    right_root_gold = {
        "tasks_mini/k-1-d-1/task_1.json": ["right-dataset"],
    }

    metrics = compute_discovery_metrics(traces, right_root_gold)

    assert metrics["aggregate"]["n"] == 1
    assert metrics["aggregate"]["D_ret"] == 1.0
    assert metrics["aggregate"]["D_acc"] == 1.0


def test_task_gold_ids_normalize_sources_instead_of_dirty_datasets_used() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        task_path = Path(tmpdir) / "tasks-mini-kramabench" / "k-2-d-1-s-1" / "task_1.json"
        task_path.parent.mkdir(parents=True)
        task_path.write_text(
            json.dumps({
                "datasets_used": ["worldcities.csv"],
                "sources_used": [
                    "datagov/kramabench-archeology-easy-10/files/worldcities.csv",
                    "s3://sana-kramabench/datagov/kramabench-archeology-easy-10/files/cities.csv",
                ],
                "nodes": {
                    "1": {
                        "source": "datagov/kramabench-archeology-easy-10/files/worldcities.csv"
                    }
                },
            }),
            encoding="utf-8",
        )

        gold = load_task_gold_ids(str(task_path.parents[1]))

    assert gold[str(task_path)] == ["kramabench-archeology-easy-10"]


def test_task_gold_ids_fall_back_to_node_sources_before_datasets_used() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        task_path = Path(tmpdir) / "tasks-mini-kramabench" / "k-2-d-1-s-1" / "task_1.json"
        task_path.parent.mkdir(parents=True)
        task_path.write_text(
            json.dumps({
                "datasets_used": ["worldcities.csv"],
                "nodes": {
                    "1": {
                        "source": "datagov/kramabench-archeology-easy-10/files/worldcities.csv"
                    },
                    "2": {
                        "source": "datagov/kramabench-archeology-easy-10/files/worldcities.csv"
                    },
                },
            }),
            encoding="utf-8",
        )

        gold = load_task_gold_ids(str(task_path.parents[1]))

    assert gold[str(task_path)] == ["kramabench-archeology-easy-10"]


def test_provenance_does_not_match_explicit_trace_to_wrong_task_root() -> None:
    traces = {
        "k-1-d-1/task_1": [
            {
                "task_id": "tasks_mini/k-1-d-1/task_1.json",
                "tool": "search_ideal",
                "result_dataset_ids": ["right-dataset"],
                "gold_dataset_ids_in_results": ["right-dataset"],
            }
        ]
    }
    wrong_root_gold = {
        "tasks_core_quality/k-1-d-1/task_1.json": ["wrong-dataset"],
    }

    provenance = compute_provenance(traces, wrong_root_gold)

    assert provenance["total_gold"] == 0
    assert provenance["task_provenance"] == []


def test_search_bottleneck_does_not_match_explicit_trace_to_wrong_task_root() -> None:
    grouped_traces = {
        "model/variant": {
            "k-1-d-1/task_1": [
                {
                    "task_id": "tasks_mini/k-1-d-1/task_1.json",
                    "tool": "search_ideal",
                    "turn": 1,
                    "result_dataset_ids": ["right-dataset"],
                }
            ]
        }
    }
    wrong_root_gold = {
        "tasks_core_quality/k-1-d-1/task_1.json": ["wrong-dataset"],
    }

    bottleneck = compute_search_bottleneck(grouped_traces, {}, wrong_root_gold)

    assert bottleneck["per_task_rows"] == []
    assert bottleneck["condition_model_summary"] == {}


def test_reasoning_density_does_not_match_explicit_record_to_wrong_task_root() -> None:
    records = [
        {
            "task_id": "tasks_mini/k-1-d-1/task_1.json",
            "condition": "condition-a",
            "exact_match": 1,
        }
    ]
    wrong_root_counts = {
        "tasks_core_quality/k-1-d-1/task_1.json": 8,
        "k-1-d-1/task_1": 8,
    }

    curve = compute_reasoning_density_curve(records, wrong_root_counts)

    assert curve == {}

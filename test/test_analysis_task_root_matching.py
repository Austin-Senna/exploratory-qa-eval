import json
import tempfile
from pathlib import Path

from analysis.discovery_metrics import (
    compute_discovery_metrics,
    load_task_gold_ids,
    load_task_gold_ids_for_traces,
    load_task_gold_source_ids,
    load_task_gold_unit_ids,
)
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


def test_kramabench_gold_unit_ids_preserve_source_file_units() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        task_path = Path(tmpdir) / "tasks-mini-kramabench" / "k-2-d-1-s-1" / "task_1.json"
        task_path.parent.mkdir(parents=True)
        task_path.write_text(
            json.dumps({
                "nodes": {
                    "1": {
                        "source": "datagov/kramabench-archeology-easy-10/files/worldcities.csv"
                    },
                    "2": {
                        "source": "datagov/kramabench-archeology-easy-10/files/cities.csv"
                    },
                },
            }),
            encoding="utf-8",
        )

        unique_gold = load_task_gold_ids(str(task_path.parents[1]))
        unit_gold = load_task_gold_unit_ids(str(task_path.parents[1]))

    assert unique_gold[str(task_path)] == ["kramabench-archeology-easy-10"]
    assert unit_gold[str(task_path)] == [
        "kramabench-archeology-easy-10",
        "kramabench-archeology-easy-10",
    ]


def test_kramabench_source_gold_uses_unique_ideal_plan_source_sequence() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        task_path = root / "tasks-mini-kramabench" / "k-2-d-1-s-1" / "task_1.json"
        plan_path = root / "plans-mini-kramabench" / "k-2-d-1-s-1" / "task_1.json"
        task_path.parent.mkdir(parents=True)
        plan_path.parent.mkdir(parents=True)
        task_path.write_text(json.dumps({"datasets_used": ["worldcities.csv"]}), encoding="utf-8")
        plan_path.write_text(
            json.dumps({
                "source_sequence": [
                    "datagov/kramabench-archeology-easy-10/files/worldcities.csv",
                    "s3://sana-kramabench/datagov/kramabench-archeology-easy-10/files/worldcities.csv",
                ]
            }),
            encoding="utf-8",
        )

        gold = load_task_gold_source_ids(str(task_path.parents[1]))

    assert gold[str(task_path)] == ["kramabench-archeology-easy-10/files/worldcities.csv"]


def test_discovery_kramabench_source_metric_counts_exact_source_uri_once() -> None:
    traces = {
        "k-2-d-1-s-1/task_1": [
            {
                "task_id": "tasks-mini-kramabench/k-2-d-1-s-1/task_1.json",
                "tool": "search_ideal",
                "result_dataset_ids": ["kramabench-archeology-easy-10"],
                "result_source_ids": ["kramabench-archeology-easy-10/files/worldcities.csv"],
            },
            {
                "task_id": "tasks-mini-kramabench/k-2-d-1-s-1/task_1.json",
                "tool": "peek_file",
                "read_dataset_ids": ["kramabench-archeology-easy-10"],
                "read_source_ids": ["kramabench-archeology-easy-10/files/worldcities.csv"],
            },
        ]
    }
    gold = {
        "tasks-mini-kramabench/k-2-d-1-s-1/task_1.json": [
            "kramabench-archeology-easy-10/files/worldcities.csv",
        ],
    }

    metrics = compute_discovery_metrics(traces, gold)

    task_metric = metrics["task_metrics"][0]
    assert task_metric["d_ret"] == 1.0
    assert task_metric["d_acc"] == 1.0
    assert task_metric["gold_ids"] == ["kramabench-archeology-easy-10/files/worldcities.csv"]


def test_discovery_kramabench_source_metric_counts_download_as_access() -> None:
    traces = {
        "k-2-d-1-s-1/task_1": [
            {
                "task_id": "tasks-mini-kramabench/k-2-d-1-s-1/task_1.json",
                "tool": "download",
                "read_dataset_ids": [],
                "read_source_ids": ["kramabench-archeology-easy-10/files/worldcities.csv"],
            },
        ]
    }
    gold = {
        "tasks-mini-kramabench/k-2-d-1-s-1/task_1.json": [
            "kramabench-archeology-easy-10/files/worldcities.csv",
        ],
    }

    metrics = compute_discovery_metrics(traces, gold)

    task_metric = metrics["task_metrics"][0]
    assert task_metric["d_ret"] == 0.0
    assert task_metric["d_acc"] == 1.0
    assert task_metric["num_read_calls"] == 1


def test_discovery_kramabench_source_metric_does_not_expand_bundle_to_multiple_files() -> None:
    traces = {
        "k-4-d-1-s-2/task_1": [
            {
                "task_id": "tasks-mini-kramabench/k-4-d-1-s-2/task_1.json",
                "tool": "search_ideal",
                "result_dataset_ids": ["kramabench-archeology-hard-5"],
            }
        ]
    }
    gold = {
        "tasks-mini-kramabench/k-4-d-1-s-2/task_1.json": [
            "kramabench-archeology-hard-5/files/radiocarbon_database_regional.xlsx",
            "kramabench-archeology-hard-5/files/climateMeasurements.xlsx",
        ],
    }

    metrics = compute_discovery_metrics(traces, gold)

    assert metrics["task_metrics"][0]["d_ret"] == 0.0


def test_task_gold_ids_for_traces_uses_explicit_trace_task_paths_when_configured_root_is_stale() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        task_path = root / "tasks-mini-kramabench" / "k-2-d-1-s-1" / "task_1.json"
        stale_root = root / "tasks_mini"
        task_path.parent.mkdir(parents=True)
        stale_root.mkdir()
        task_path.write_text(
            json.dumps({
                "datasets_used": ["dirty-fallback"],
                "nodes": {
                    "1": {
                        "source": "datagov/kramabench-archeology-easy-10/files/worldcities.csv"
                    }
                },
            }),
            encoding="utf-8",
        )
        traces = {
            "k-2-d-1-s-1/task_1": [
                {
                    "task_id": str(task_path),
                    "tool": "search_value",
                    "result_dataset_ids": ["kramabench-archeology-easy-10"],
                },
                {
                    "task_id": str(task_path),
                    "tool": "peek_file",
                    "read_dataset_ids": ["kramabench-archeology-easy-10"],
                },
            ]
        }

        gold = load_task_gold_ids_for_traces(str(stale_root), traces)
        metrics = compute_discovery_metrics(traces, gold)

    assert gold[str(task_path)] == ["kramabench-archeology-easy-10"]
    assert metrics["aggregate"]["D_ret"] == 1.0
    assert metrics["aggregate"]["D_acc"] == 1.0


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


def test_search_bottleneck_does_not_count_repeated_kramabench_bundle_as_multiple_source_units() -> None:
    grouped_traces = {
        "model/variant": {
            "k-2-d-1-s-1/task_1": [
                {
                    "task_id": "tasks-mini-kramabench/k-2-d-1-s-1/task_1.json",
                    "tool": "search_ideal",
                    "turn": 1,
                    "result_dataset_ids": ["kramabench-archeology-easy-10"],
                    "gold_dataset_ids_in_results": ["kramabench-archeology-easy-10"],
                },
                {
                    "task_id": "tasks-mini-kramabench/k-2-d-1-s-1/task_1.json",
                    "tool": "peek_multiple",
                    "read_dataset_ids": [
                        "kramabench-archeology-easy-10",
                        "kramabench-archeology-easy-10",
                    ],
                    "gold_dataset_ids_read": [
                        "kramabench-archeology-easy-10",
                        "kramabench-archeology-easy-10",
                    ],
                },
            ]
        }
    }
    unit_gold = {
        "tasks-mini-kramabench/k-2-d-1-s-1/task_1.json": [
            "kramabench-archeology-easy-10",
            "kramabench-archeology-easy-10",
        ],
    }

    bottleneck = compute_search_bottleneck(grouped_traces, {}, unit_gold)

    per_call = bottleneck["per_call_rows"][0]
    assert per_call["n_gold_datasets"] == 2
    assert per_call["cumulative_search_gold_count"] == 1
    assert per_call["cumulative_search_gold_recall"] == 0.5
    assert per_call["cumulative_read_gold_count"] == 1
    assert per_call["cumulative_read_gold_recall"] == 0.5


def test_search_bottleneck_falls_back_when_kramabench_gold_hit_side_channel_is_empty() -> None:
    grouped_traces = {
        "model/variant": {
            "k-2-d-1-s-1/task_1": [
                {
                    "task_id": "tasks-mini-kramabench/k-2-d-1-s-1/task_1.json",
                    "tool": "search_ideal",
                    "turn": 1,
                    "result_dataset_ids": ["kramabench-archeology-easy-10"],
                    "gold_dataset_ids_in_results": [],
                },
            ]
        }
    }
    unit_gold = {
        "tasks-mini-kramabench/k-2-d-1-s-1/task_1.json": [
            "kramabench-archeology-easy-10",
            "kramabench-archeology-easy-10",
        ],
    }

    bottleneck = compute_search_bottleneck(grouped_traces, {}, unit_gold)

    per_call = bottleneck["per_call_rows"][0]
    assert per_call["cumulative_search_gold_count"] == 1
    assert per_call["cumulative_search_gold_recall"] == 0.5


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

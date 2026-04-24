import json
import os
import sys
import unittest
from contextlib import ExitStack
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import strands_evaluation.tools.external.ideal.search_ideal as search_ideal
import strands_evaluation.tools.external.ideal.search_wrapper as search_wrapper

_TASK_ROOT = "k-1-d-1"
_TASK_ID_TEMPLATE = f"tasks_mini/{_TASK_ROOT}/{{task_name}}"
_LIVE_LOG_PATH = Path("test_logs/search_ideal_judge_samples.jsonl")
_LIVE_SOURCE_SEQUENCE = [
    "datagov/chicago-crime-2015/files/rows.txt",
    "datagov/chicago-crime-2016/files/rows.txt",
    "datagov/chicago-crime-2017/files/rows.txt",
    "datagov/chicago-parks/files/rows.txt",
    "datagov/chicago-building-permits/files/rows.txt",
    "datagov/chicago-school-enrollment/files/rows.txt",
    "datagov/chicago-bike-trips/files/rows.txt",
    "datagov/chicago-fire-stations/files/rows.txt",
    "datagov/chicago-library-locations/files/rows.txt",
    "datagov/chicago-311-service-requests/files/rows.txt",
    "datagov/chicago-public-health-indicators/files/rows.txt",
]
_CRIME_DATASET_IDS = {
    "chicago-crime-2015",
    "chicago-crime-2016",
    "chicago-crime-2017",
}


def _reset_wrapper_caches() -> None:
    search_wrapper._DESC_CACHE_LOADED = False
    search_wrapper._DESC_BY_URI = {}
    search_wrapper._DESC_ROW_BY_URI = {}
    search_wrapper._SNIPPET_CACHE_LOADED = False
    search_wrapper._SNIPPET_BY_URI = {}
    search_wrapper._SCHEMAS_CACHE_LOADED = False
    search_wrapper._SCHEMA_BY_SLUG_FILENAME = {}


def _dataset_id(source_path: str) -> str:
    return search_ideal._dataset_id_from_source(source_path)


def _task_id(task_name: str) -> str:
    return _TASK_ID_TEMPLATE.format(task_name=task_name)


def _write_plan(plans_root: Path, *, task_name: str, source_sequence: list[str]) -> str:
    target = plans_root / _TASK_ROOT
    target.mkdir(parents=True, exist_ok=True)
    (target / task_name).write_text(
        json.dumps(
            {
                "dataset_sequence": [_dataset_id(source) for source in source_sequence],
                "source_sequence": list(source_sequence),
                "reasoning_chain_text": "1. Find the right dataset.\n2. Query it.",
            }
        )
    )
    return _task_id(task_name)


def _set_task_context(plans_root: Path, *, task_name: str, source_sequence: list[str]) -> tuple[str, list[str]]:
    task_id = _write_plan(plans_root, task_name=task_name, source_sequence=source_sequence)
    search_ideal.set_plans_root(plans_root)
    search_ideal.reset_state()
    search_ideal.set_task_context({"task_id": task_id})
    return task_id, [search_ideal._canonical_uri(source) for source in source_sequence]


def _log_judge_call(
    *,
    test_name: str,
    query: str,
    candidates: list[tuple[str, str]],
    picked: list[str] | None,
    reason: str | None,
    count: int,
) -> None:
    _LIVE_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _LIVE_LOG_PATH.open("a") as handle:
        handle.write(
            json.dumps(
                {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "test": test_name,
                    "query": query,
                    "candidates": [
                        {"s3_uri": s3_uri, "dataset_id": dataset_id}
                        for s3_uri, dataset_id in candidates
                    ],
                    "picked": list(picked or []),
                    "reason": reason,
                    "count": count,
                }
            )
            + "\n"
        )


class _FakeJudge:
    def __init__(self, *, tools, action, kwargs):
        self.tools = list(tools)
        self._action = action
        self.kwargs = dict(kwargs)

    def __call__(self, prompt: str) -> None:
        if self._action is not None:
            self._action(prompt, self.tools)


class _FakeAgentFactory:
    def __init__(self, action=None):
        self._action = action
        self.calls: list[_FakeJudge] = []

    def __call__(self, *args, **kwargs):
        _ = args
        judge = _FakeJudge(
            tools=kwargs.get("tools", []),
            action=self._action,
            kwargs=kwargs,
        )
        self.calls.append(judge)
        return judge


class TestSearchIdealJudge(unittest.TestCase):
    def tearDown(self) -> None:
        search_ideal.set_plans_root("plans_mini")
        search_ideal.reset_state()
        _reset_wrapper_caches()

    def _patch_support_files(
        self,
        root: Path,
        *,
        uri: str,
        dataset_slug: str,
        desc: str = "LLM description",
        snippet: str = "dataset snippet words",
        schema_kind: str = "csv",
        columns: list[str] | None = None,
    ) -> ExitStack:
        desc_path = root / "table_descriptions.jsonl"
        desc_path.write_text(json.dumps({"dataset_uri": uri, "description": desc}) + "\n")

        snippet_path = root / "snippet.jsonl"
        snippet_path.write_text(json.dumps({"dataset_uri": uri, "dataset_snippet": snippet}) + "\n")

        schema_path = root / "datagov_tables_schemas_full.jsonl"
        schema_path.write_text(
            json.dumps(
                {
                    "dataset_slug": dataset_slug,
                    "tables": [
                        {
                            "relative_path": "files/rows.txt",
                            "table_kind": schema_kind,
                            "columns": columns if columns is not None else ["col_a", "col_b"],
                        }
                    ],
                }
            )
            + "\n"
        )

        stack = ExitStack()
        stack.enter_context(patch.object(search_wrapper, "_TABLE_DESCRIPTIONS_PATH", desc_path))
        stack.enter_context(patch.object(search_wrapper, "_SNIPPETS_PATH", snippet_path))
        stack.enter_context(patch.object(search_wrapper, "_SCHEMAS_PATH", schema_path))
        return stack

    def test_set_task_context_hard_fails_when_source_sequence_missing(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            target = plans_root / _TASK_ROOT
            target.mkdir(parents=True, exist_ok=True)
            (target / "task_1.json").write_text(
                json.dumps(
                    {
                        "dataset_sequence": ["ds_one"],
                        "reasoning_chain_text": "Step 1",
                    }
                )
            )

            search_ideal.set_plans_root(plans_root)
            with self.assertRaisesRegex(ValueError, "source_sequence"):
                search_ideal.set_task_context({"task_id": _task_id("task_1.json")})

    def test_invalid_pick_raises_in_pick_tool(self):
        factory = _FakeAgentFactory()
        remaining = [
            ("s3://lakeqa-yc4103-datalake/datagov/ds_one/files/rows.txt", "ds_one"),
        ]

        with patch.object(search_ideal, "Agent", factory), patch.object(
            search_ideal,
            "_judge_model",
            return_value="fake-model",
        ):
            judge, state = search_ideal._build_judge(remaining)

        self.assertIs(judge, factory.calls[0])
        pick = judge.tools[0]
        with self.assertRaisesRegex(ValueError, "not in candidate list"):
            pick(
                s3_uris=["s3://lakeqa-yc4103-datalake/datagov/not-a-match/files/rows.txt"],
                reason="bad pick",
            )
        self.assertIsNone(state["picked"])

    def test_fallback_pick_on_judge_no_pick(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            _, uris = _set_task_context(
                plans_root,
                task_name="task_1.json",
                source_sequence=[
                    "datagov/chicago-crime-2017/files/rows.txt",
                    "datagov/chicago-parks/files/rows.txt",
                ],
            )
            factory = _FakeAgentFactory(action=lambda prompt, tools: None)

            with patch.object(search_ideal, "Agent", factory), patch.object(
                search_ideal,
                "_judge_model",
                return_value="fake-model",
            ):
                with self.assertLogs(search_ideal.logger, level="WARNING") as logs:
                    result = search_ideal.search_ideal("crime data in Chicago 2017")

        self.assertEqual(result["count"], 1)
        self.assertEqual(result["results"][0]["s3_uri"], uris[0])
        self.assertEqual(result["results"][0]["dataset_id"], "chicago-crime-2017")
        self.assertFalse(result["plan_exhausted"])
        self.assertEqual(search_ideal._USED_S3_URIS, {uris[0]})
        self.assertEqual(len(factory.calls), 1)
        self.assertTrue(any("falling back" in message for message in logs.output))

    def test_set_task_context_resets_used(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            _, uris = _set_task_context(
                plans_root,
                task_name="task_1.json",
                source_sequence=[
                    "datagov/chicago-crime-2017/files/rows.txt",
                    "datagov/chicago-parks/files/rows.txt",
                ],
            )
            search_ideal._USED_S3_URIS.update(uris)

            search_ideal.set_task_context({"task_id": _task_id("task_1.json")})

        self.assertEqual(search_ideal._USED_S3_URIS, set())
        self.assertEqual(len(search_ideal._CANDIDATES), 2)

    def test_plan_exhausted_returns_empty(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            _, uris = _set_task_context(
                plans_root,
                task_name="task_1.json",
                source_sequence=[
                    "datagov/chicago-crime-2017/files/rows.txt",
                    "datagov/chicago-parks/files/rows.txt",
                ],
            )
            search_ideal._USED_S3_URIS.update(uris)
            factory = _FakeAgentFactory(action=lambda prompt, tools: None)

            with patch.object(search_ideal, "Agent", factory), patch.object(
                search_ideal,
                "_judge_model",
                return_value="fake-model",
            ):
                result = search_ideal.search_ideal("anything")

        self.assertEqual(result, {"results": [], "count": 0, "query": "anything", "plan_exhausted": True})
        self.assertEqual(len(factory.calls), 0)

    def test_wrapper_hides_top_k_from_agent(self):
        wrapped = search_wrapper.build_search_tools(
            [search_ideal.search_ideal],
            fixed_k=None,
            results_mode="naive",
        )[0]
        properties = wrapped.tool_spec["inputSchema"]["json"]["properties"]
        self.assertEqual(set(properties), {"query"})
        self.assertNotIn("top_k", properties)

    def test_wrapper_applies_naive_vs_ideal_shaping(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            _, uris = _set_task_context(
                plans_root,
                task_name="task_1.json",
                source_sequence=["datagov/chicago-crime-2017/files/rows.txt"],
            )
            uri = uris[0]
            factory = _FakeAgentFactory(
                action=lambda prompt, tools: tools[0](s3_uris=[uri], reason="exact match")
            )

            with self._patch_support_files(
                Path(tmpdir),
                uri=uri,
                dataset_slug="chicago-crime-2017",
            ):
                with patch.object(search_ideal, "Agent", factory), patch.object(
                    search_ideal,
                    "_judge_model",
                    return_value="fake-model",
                ):
                    naive_tool = search_wrapper.build_search_tools(
                        [search_ideal.search_ideal],
                        fixed_k=None,
                        results_mode="naive",
                    )[0]
                    naive = naive_tool(query="crime 2017")

                    search_ideal.reset_state()
                    search_ideal.set_plans_root(plans_root)
                    search_ideal.set_task_context({"task_id": _task_id("task_1.json")})

                    ideal_tool = search_wrapper.build_search_tools(
                        [search_ideal.search_ideal],
                        fixed_k=None,
                        results_mode="ideal",
                    )[0]
                    ideal = ideal_tool(query="crime 2017")

        self.assertEqual(
            naive["results"][0],
            {
                "dataset_id": "chicago-crime-2017",
                "s3_uri": uri,
            },
        )
        self.assertNotIn("llm_desc", naive["results"][0])

        self.assertEqual(
            ideal["results"][0],
            {
                "dataset_id": "chicago-crime-2017",
                "s3_uri": uri,
                "llm_desc": "LLM description",
                "columns": ["col_a", "col_b"],
                "dataset_snippet": "dataset snippet words",
            },
        )


def _capture_builder_calls(captured_calls: list[dict]):
    original = search_ideal._build_judge

    def _wrapped(remaining: list[tuple[str, str]]):
        judge, state = original(remaining)
        captured_calls.append({"remaining": list(remaining), "state": state})
        return judge, state

    return _wrapped

@unittest.skipUnless(os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY not set")
class TestSearchIdealJudgeLive(unittest.TestCase):
    def tearDown(self) -> None:
        search_ideal.set_plans_root("plans_mini")
        search_ideal.reset_state()

    def test_live_single_match(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            _set_task_context(
                plans_root,
                task_name="task_live_single.json",
                source_sequence=_LIVE_SOURCE_SEQUENCE,
            )
            captured_calls: list[dict] = []
            query = "crime data in Chicago 2017"
            with patch.object(search_ideal, "_build_judge", side_effect=_capture_builder_calls(captured_calls)):
                result = search_ideal.search_ideal(query)

        self.assertEqual(result["count"], 1)
        self.assertEqual(result["results"][0]["dataset_id"], "chicago-crime-2017")
        self.assertTrue(captured_calls)
        _log_judge_call(
            test_name="test_live_single_match",
            query=query,
            candidates=captured_calls[0]["remaining"],
            picked=captured_calls[0]["state"]["picked"],
            reason=captured_calls[0]["state"]["reason"],
            count=result["count"],
        )

    def test_live_aggregation_multi_pick(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            _set_task_context(
                plans_root,
                task_name="task_live_aggregate.json",
                source_sequence=_LIVE_SOURCE_SEQUENCE,
            )
            captured_calls: list[dict] = []
            query = "all years of Chicago crime data"
            with patch.object(search_ideal, "_build_judge", side_effect=_capture_builder_calls(captured_calls)):
                result = search_ideal.search_ideal(query)

        picked_ids = {row["dataset_id"] for row in result["results"]}
        self.assertGreaterEqual(len(picked_ids & _CRIME_DATASET_IDS), 2)
        self.assertTrue(captured_calls)
        _log_judge_call(
            test_name="test_live_aggregation_multi_pick",
            query=query,
            candidates=captured_calls[0]["remaining"],
            picked=captured_calls[0]["state"]["picked"],
            reason=captured_calls[0]["state"]["reason"],
            count=result["count"],
        )

    def test_live_dedup_across_calls(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            _set_task_context(
                plans_root,
                task_name="task_live_dedup.json",
                source_sequence=_LIVE_SOURCE_SEQUENCE,
            )
            captured_calls: list[dict] = []
            query = "all years of Chicago crime data"
            with patch.object(search_ideal, "_build_judge", side_effect=_capture_builder_calls(captured_calls)):
                first = search_ideal.search_ideal(query)
                first_used = set(search_ideal._USED_S3_URIS)
                second = search_ideal.search_ideal(query)
                second_used = set(search_ideal._USED_S3_URIS)

        first_uris = {row["s3_uri"] for row in first["results"]}
        second_uris = {row["s3_uri"] for row in second["results"]}
        self.assertTrue(first_uris)
        self.assertTrue(second_uris)
        self.assertTrue(first_uris.isdisjoint(second_uris))
        self.assertGreater(len(second_used), len(first_used))
        self.assertEqual(len(captured_calls), 2)
        _log_judge_call(
            test_name="test_live_dedup_across_calls:first",
            query=query,
            candidates=captured_calls[0]["remaining"],
            picked=captured_calls[0]["state"]["picked"],
            reason=captured_calls[0]["state"]["reason"],
            count=first["count"],
        )
        _log_judge_call(
            test_name="test_live_dedup_across_calls:second",
            query=query,
            candidates=captured_calls[1]["remaining"],
            picked=captured_calls[1]["state"]["picked"],
            reason=captured_calls[1]["state"]["reason"],
            count=second["count"],
        )

    def test_live_specific_query_ignores_aggregate(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            _set_task_context(
                plans_root,
                task_name="task_live_specific.json",
                source_sequence=_LIVE_SOURCE_SEQUENCE,
            )
            captured_calls: list[dict] = []
            query = "Chicago crime 2017 specifically"
            with patch.object(search_ideal, "_build_judge", side_effect=_capture_builder_calls(captured_calls)):
                result = search_ideal.search_ideal(query)

        self.assertEqual(result["count"], 1)
        self.assertEqual(result["results"][0]["dataset_id"], "chicago-crime-2017")
        self.assertTrue(captured_calls)
        _log_judge_call(
            test_name="test_live_specific_query_ignores_aggregate",
            query=query,
            candidates=captured_calls[0]["remaining"],
            picked=captured_calls[0]["state"]["picked"],
            reason=captured_calls[0]["state"]["reason"],
            count=result["count"],
        )

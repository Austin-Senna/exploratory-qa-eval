from sana_evaluation.plugins.source_session import (
    SOURCE_SESSION_TOOLS,
    SourceSessionState,
    source_from_tool_use,
)


def test_source_from_dataset_id_input() -> None:
    source = source_from_tool_use(
        {"name": "peek_file", "input": {"dataset_id": "county-population"}}
    )
    assert source == "county-population"


def test_source_from_single_dataset_ids_input() -> None:
    source = source_from_tool_use(
        {"name": "list_files", "input": {"dataset_ids": ["libraries-2021"]}}
    )
    assert source == "libraries-2021"


def test_source_from_s3_uri_input() -> None:
    source = source_from_tool_use(
        {
            "name": "read_file",
            "input": {
                "s3_uri": (
                    "s3://lakeqa-yc4103-datalake/datagov/"
                    "iowa-local-area-unemployment-statistics/files/rows.csv"
                )
            },
        }
    )
    assert source == "iowa-local-area-unemployment-statistics"


def test_source_from_relative_datagov_uri_input() -> None:
    source = source_from_tool_use(
        {
            "name": "peek_file",
            "input": {
                "s3_uri": (
                    "datagov/bridge-conditions-nys-department-of-transportation/"
                    "files/rows.txt"
                )
            },
        }
    )
    assert source == "bridge-conditions-nys-department-of-transportation"


def test_source_from_relative_wikipedia_uri_input() -> None:
    source = source_from_tool_use(
        {
            "name": "grep_file",
            "input": {"s3_uri": "wikipedia/Khan_Lab_School/content.txt"},
        }
    )
    assert source == "Khan_Lab_School"


def test_source_from_batch_files_same_dataset() -> None:
    source = source_from_tool_use(
        {
            "name": "peek_multiple",
            "input": {
                "files": [
                    {"dataset_id": "schools", "file_path": "a.csv"},
                    {"dataset_id": "schools", "file_path": "b.csv"},
                ]
            },
        }
    )
    assert source == "schools"


def test_source_from_batch_files_multiple_datasets() -> None:
    source = source_from_tool_use(
        {
            "name": "peek_multiple",
            "input": {
                "files": [
                    {"dataset_id": "schools", "file_path": "a.csv"},
                    {"dataset_id": "libraries", "file_path": "b.csv"},
                ]
            },
        }
    )
    assert source == "multi:libraries,schools"


def test_execute_code_falls_back_to_active_source() -> None:
    source = source_from_tool_use(
        {"name": "execute_code", "input": {"code": "print('x')"}},
        fallback_source="schools",
    )
    assert source == "schools"


def test_ideal_computation_tools_participate_in_source_sessions() -> None:
    assert "query_ideal" in SOURCE_SESSION_TOOLS
    assert "execute_ideal" in SOURCE_SESSION_TOOLS
    query_source = source_from_tool_use(
        {"name": "query_ideal", "input": {"dataset_id": "schools"}}
    )
    execute_source = source_from_tool_use(
        {"name": "execute_ideal", "input": {"code": "print('x')"}},
        fallback_source="schools",
    )
    assert query_source == "schools"
    assert execute_source == "schools"


def test_session_counts_and_budget_exhaustion() -> None:
    state = SourceSessionState(
        current_source="schools",
        commitment_goal="count schools",
        max_source_calls=2,
        success_condition="answer has count",
    )
    assert state.calls_used == 0
    assert state.is_budget_exhausted() is False
    state.record_call("peek_file")
    assert state.calls_used == 1
    assert state.is_budget_exhausted() is False
    state.record_call("query_file")
    assert state.calls_used == 2
    assert state.is_budget_exhausted() is True


def test_session_contains_current_and_related_sources() -> None:
    state = SourceSessionState(
        current_source="schools",
        commitment_goal="compare enrollment sources",
        max_source_calls=3,
        related_sources=["school-sites", "school-results"],
    )

    assert state.contains_source("schools") is True
    assert state.contains_source("school-sites") is True
    assert state.contains_source("school-results") is True
    assert state.contains_source("libraries") is False

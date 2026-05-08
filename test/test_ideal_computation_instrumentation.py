from strands_evaluation.helper import result as result_module
from strands_evaluation.instrumentation import read_trace_plugin


def test_read_trace_treats_query_ideal_as_dataset_read() -> None:
    assert "query_ideal" in read_trace_plugin._READ_TOOLS
    read_ids = read_trace_plugin._extract_read_dataset_ids(
        "query_ideal",
        {
            "s3_uri": (
                "s3://lakeqa-yc4103-datalake/datagov/"
                "school-directory/files/rows.txt"
            )
        },
    )
    assert read_ids == ["school-directory"]


def test_tool_metrics_classify_query_ideal_as_api_read_tool() -> None:
    assert "query_ideal" in result_module._API_TOOL_NAMES

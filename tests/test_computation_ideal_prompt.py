from pathlib import Path
from types import SimpleNamespace

from strands_evaluation.tools.external.ideal import computation_ideal


def test_plan_records_prompt_includes_selection_index_and_expected_output():
    plan = SimpleNamespace(task_id="task", plan_path=Path("plans/task.json"))
    records = [
        SimpleNamespace(
            node_id="2",
            dataset_id="kramabench-wildfire-easy-1",
            source="datagov/kramabench-wildfire-easy-1/files/noaa_wildfires_monthly_stats.csv",
            intent="Which consecutive 3-month period has the highest total acres burned?",
            payload="print(start, end)",
            answer="201506|201508",
            blocked=False,
        ),
        SimpleNamespace(
            node_id="3",
            dataset_id="kramabench-wildfire-easy-1",
            source="datagov/kramabench-wildfire-easy-1/files/noaa_wildfires_monthly_stats.csv",
            intent="What is the total acres burned in that period?",
            payload="print(best_total)",
            answer="7805421",
            blocked=False,
        ),
    ]

    prompt_json = computation_ideal._plan_records_for_prompt(plan, records)

    assert '"selection_index": 1' in prompt_json
    assert '"selection_index": 2' in prompt_json
    assert '"expected_output": "201506|201508"' in prompt_json
    assert '"expected_output": "7805421"' in prompt_json

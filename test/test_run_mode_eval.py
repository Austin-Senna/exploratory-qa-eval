import importlib.util
import sys
import types
import unittest
from pathlib import Path

def _load_run_eval_module():
    repo_root = Path(__file__).resolve().parents[1]
    module_path = repo_root / "strands_evaluation" / "run_eval.py"

    fake_pkg = types.ModuleType("strands_evaluation")
    fake_pkg.__path__ = [str(module_path.parent)]

    fake_agent = types.ModuleType("strands_evaluation.agent")
    fake_agent.BatchRunner = object

    fake_config = types.ModuleType("strands_evaluation.config")
    fake_config.AgentConfig = object
    fake_config.ConditionConfig = object
    fake_config.RunConfig = object

    saved = {
        "strands_evaluation": sys.modules.get("strands_evaluation"),
        "strands_evaluation.agent": sys.modules.get("strands_evaluation.agent"),
        "strands_evaluation.config": sys.modules.get("strands_evaluation.config"),
    }
    sys.modules["strands_evaluation"] = fake_pkg
    sys.modules["strands_evaluation.agent"] = fake_agent
    sys.modules["strands_evaluation.config"] = fake_config
    try:
        spec = importlib.util.spec_from_file_location("_test_run_eval_module", module_path)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        return module
    finally:
        for name, original in saved.items():
            if original is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original


def _load_run_mode_eval_module():
    repo_root = Path(__file__).resolve().parents[1]
    module_path = repo_root / "strands_evaluation" / "run_mode_eval.py"

    fake_pkg = types.ModuleType("strands_evaluation")
    fake_pkg.__path__ = [str(module_path.parent)]

    fake_base_eval = types.ModuleType("strands_evaluation.run_eval")
    fake_base_eval.BatchRunner = object
    fake_base_eval._display_name = lambda agent_config: "openai_gpt-5.2-xhigh"
    fake_base_eval._results_dir = lambda run_config, agent_config: "unused"
    fake_base_eval.find_all_task_dirs = lambda *_args, **_kwargs: []

    fake_agent_with_mode = types.ModuleType("strands_evaluation.agent_with_mode")
    fake_agent_with_mode.BatchRunner = object

    fake_config = types.ModuleType("strands_evaluation.config")
    fake_config.AgentConfig = object
    fake_config.ConditionConfig = object
    fake_config.RunConfig = object

    saved = {
        "strands_evaluation": sys.modules.get("strands_evaluation"),
        "strands_evaluation.run_eval": sys.modules.get("strands_evaluation.run_eval"),
        "strands_evaluation.agent_with_mode": sys.modules.get("strands_evaluation.agent_with_mode"),
        "strands_evaluation.config": sys.modules.get("strands_evaluation.config"),
    }
    sys.modules["strands_evaluation"] = fake_pkg
    sys.modules["strands_evaluation.run_eval"] = fake_base_eval
    sys.modules["strands_evaluation.agent_with_mode"] = fake_agent_with_mode
    sys.modules["strands_evaluation.config"] = fake_config
    try:
        spec = importlib.util.spec_from_file_location("_test_run_mode_eval_module", module_path)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        return module
    finally:
        for name, original in saved.items():
            if original is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original


run_eval = _load_run_eval_module()
run_mode_eval = _load_run_mode_eval_module()


class RunModeEvalTests(unittest.TestCase):
    def test_variant_condition_label_uses_compact_mode_letters(self):
        label = run_mode_eval._variant_condition_label(
            search_tool="ideal",
            search_results="naive",
            agent_management="naive",
            k=5,
            search_calls=2,
        )

        self.assertEqual(label, "search_i_results_n_plann_k5_sc2")

    def test_mode_results_dir_does_not_append_model_twice(self):
        agent_config = types.SimpleNamespace(
            model_name="openai/gpt-5.2",
            model_id="unused",
            extra_model_kwargs={"reasoning_effort": "xhigh"},
        )
        run_config = types.SimpleNamespace(
            results_output_dir="results",
            condition_config=types.SimpleNamespace(
                condition="modes/openai_gpt-5.2-xhigh/search_i_results_i_plani_k5",
            ),
        )

        self.assertEqual(
            run_eval._results_dir(run_config, agent_config).replace("\\", "/"),
            "results/modes/openai_gpt-5.2-xhigh/search_i_results_i_plani_k5",
        )

    def test_standard_results_dir_layout_is_unchanged(self):
        agent_config = types.SimpleNamespace(
            model_name="openai/gpt-5.2",
            model_id="unused",
            extra_model_kwargs={},
        )
        run_config = types.SimpleNamespace(
            results_output_dir="results",
            condition_config=types.SimpleNamespace(condition="baseline"),
        )

        self.assertEqual(
            run_eval._results_dir(run_config, agent_config).replace("\\", "/"),
            "results/baseline/openai_gpt-5.2",
        )


if __name__ == "__main__":
    unittest.main()

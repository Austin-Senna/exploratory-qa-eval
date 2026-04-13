import importlib.util
import types
import unittest
from pathlib import Path
from unittest.mock import patch


def _load_logger_module():
    repo_root = Path(__file__).resolve().parents[1]
    module_path = repo_root / "strands_evaluation" / "helper" / "logger.py"
    spec = importlib.util.spec_from_file_location("_test_logger_module", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


logger_module = _load_logger_module()


class LoggerOutputDirTests(unittest.TestCase):
    def test_configure_worker_logging_uses_run_config_log_root(self):
        run_config = types.SimpleNamespace(logs_output_dir="custom_logs")

        with patch.object(logger_module, "configure_logging") as mock_configure:
            logger_module.configure_worker_logging(
                run_config,
                model="openai/gpt-5.2-xhigh",
                condition="st-ideal_sr-ideal_am-ideal_k5/baseline",
                task_id="tasks_mini/k-1-d-1/task_1.json",
            )

        mock_configure.assert_called_once_with(
            log_dir="custom_logs",
            model="openai/gpt-5.2-xhigh",
            condition="st-ideal_sr-ideal_am-ideal_k5/baseline",
            task_id="tasks_mini/k-1-d-1/task_1.json",
            level=logger_module.logging.DEBUG,
        )


if __name__ == "__main__":
    unittest.main()

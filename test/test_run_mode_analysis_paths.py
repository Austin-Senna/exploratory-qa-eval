import tempfile
import unittest
from pathlib import Path

from analysis.run_mode_analysis import _resolve_input_roots


class RunModeAnalysisPathTests(unittest.TestCase):
    def test_resolve_input_roots_infers_ec2_traces_and_logs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "results-ec2" / "traces" / "modes").mkdir(parents=True)
            (root / "logs-ec2").mkdir(parents=True)

            results_dir, traces_dir, logs_dir = _resolve_input_roots(
                results_dir=str(root / "results-ec2"),
                traces_dir="results/traces/modes",
                logs_dir="logs",
            )

            self.assertEqual(results_dir, str(root / "results-ec2"))
            self.assertEqual(traces_dir, str(root / "results-ec2" / "traces" / "modes"))
            self.assertEqual(logs_dir, str(root / "logs-ec2"))

    def test_resolve_input_roots_preserves_explicit_overrides(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            explicit_traces = root / "custom-traces"
            explicit_logs = root / "custom-logs"
            explicit_traces.mkdir()
            explicit_logs.mkdir()

            results_dir, traces_dir, logs_dir = _resolve_input_roots(
                results_dir=str(root / "results-ec2"),
                traces_dir=str(explicit_traces),
                logs_dir=str(explicit_logs),
            )

            self.assertEqual(results_dir, str(root / "results-ec2"))
            self.assertEqual(traces_dir, str(explicit_traces))
            self.assertEqual(logs_dir, str(explicit_logs))


if __name__ == "__main__":
    unittest.main()

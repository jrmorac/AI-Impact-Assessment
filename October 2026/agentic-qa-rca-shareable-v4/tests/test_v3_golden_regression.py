import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import main


ROOT = Path(__file__).resolve().parents[1]
GOLDEN_ROOT = Path(__file__).resolve().parent / "golden"
CONTEXT = ROOT / "project-context" / "baseline-project.yaml"
INPUT = ROOT / "data" / "input" / "demo_cases.json"
VOLATILE_KEYS = {
    "created_at_utc",
    "generated_at_utc",
    "recorded_at_utc",
    "timestamp_utc",
    "updated_at_utc",
}


def canonicalize(value):
    if isinstance(value, dict):
        return {
            key: canonicalize(item)
            for key, item in value.items()
            if key not in VOLATILE_KEYS and key not in {"input_file"}
        }
    if isinstance(value, list):
        return [canonicalize(item) for item in value]
    if isinstance(value, str) and Path(value).is_absolute():
        return "<ABSOLUTE_PATH>"
    return value


class V3GoldenRegressionTests(unittest.TestCase):
    def run_case(self, case_name):
        expected = json.loads((GOLDEN_ROOT / f"{case_name}.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temporary:
            output_root = Path(temporary)
            session_path = output_root / f"{case_name}-session.json"
            report_path = output_root / f"{case_name}-report.md"
            batch_path = output_root / f"{case_name}-batch.json"
            evidence_path = output_root / "evidence.csv"
            capa_path = output_root / "capa.csv"
            ado_path = output_root / "ado.csv"

            result = main.run_guided_rca(
                context_path=CONTEXT,
                input_path=INPUT,
                defect_id=expected["defect_id"],
                session_path=session_path,
                role="qa",
                output_report_path=report_path,
                quick_plan=main._load_quick_plan(ROOT / "data" / "input" / f"demo_quick_plan_{case_name}.json"),
            )
            main.run(CONTEXT, INPUT, batch_path, evidence_path)
            main.export_capa_csv(session_path=session_path, output_path=capa_path, provider="ado", assignee="", due_date="")
            main.export_ado_testcases_csv(
                session_path=session_path,
                output_path=ado_path,
                assigned_to="",
                area_path="",
                iteration_path="",
                state="Design",
                variant_set="standard",
            )

            session = json.loads(session_path.read_text(encoding="utf-8"))
            report = json.loads(batch_path.read_text(encoding="utf-8"))
            canonical_session = canonicalize(session)
            canonical_report = canonicalize(report)
            analysis = next(
                item for item in canonical_report["analysis"] if item["defect_id"] == expected["defect_id"]
            )
            raw_analysis = next(
                item for item in report["analysis"] if item["defect_id"] == expected["defect_id"]
            )

            self.assertEqual(result["status"], expected["session_status"])
            self.assertEqual(canonical_session["status"], expected["session_status"])
            self.assertEqual(canonical_session["category"], expected["category"])
            self.assertEqual(len(canonical_session["why_chain"]), expected["why_depth"])
            self.assertNotIn("input_file", canonical_report)
            self.assertEqual(analysis["category"], expected["category"])
            self.assertEqual(analysis["action_mode"], expected["batch_action_mode"])
            self.assertEqual(
                [trace["agent"] for trace in analysis["agent_trace"]],
                expected["batch_trace_agents"],
            )
            self.assertEqual(len(capa_path.read_text(encoding="utf-8").splitlines()), expected["capa_task_count"] + 1)
            self.assertEqual(len(ado_path.read_text(encoding="utf-8").splitlines()), expected["ado_test_case_count"] + 1)

            for key in expected["required_session_keys"]:
                self.assertIn(key, canonical_session)
            for key in expected["required_analysis_keys"]:
                self.assertIn(key, analysis)
            for trace in raw_analysis["agent_trace"]:
                self.assertEqual(set(trace), {"timestamp_utc", "agent", "input", "output"})

    def test_why1_golden(self):
        self.run_case("why1")

    def test_why3_golden(self):
        self.run_case("why3")

    def test_why5_golden(self):
        self.run_case("why5")


if __name__ == "__main__":
    unittest.main()
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import main


ROOT = Path(__file__).resolve().parents[1]
CONTEXT = ROOT / "project-context" / "baseline-project.yaml"
INPUT = ROOT / "data" / "input" / "demo_cases.json"


class QuickPlanTargetDepthTests(unittest.TestCase):
    def test_finite_non_closing_plan_stops_at_target_depth(self):
        answers = [
            {
                "answer": f"Because synthetic control condition {index} was not enforced by the workflow.",
                "evidence_refs": [f"synthetic-step-{index}.log"],
                "controllable": True,
                "resolved": False,
                "prevents_recurrence": False,
            }
            for index in range(1, 6)
        ]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plan_path = root / "quick-plan.json"
            session_path = root / "session.json"
            report_path = root / "report.md"
            plan_path.write_text(json.dumps({"answers": answers}), encoding="utf-8")
            result = main.run_guided_rca(
                context_path=CONTEXT,
                input_path=INPUT,
                defect_id="DEMO-WHY5",
                session_path=session_path,
                role="qa",
                output_report_path=report_path,
                quick_plan=main._load_quick_plan(plan_path),
            )
            self.assertEqual(result["status"], "target_depth_reached")
            self.assertTrue(report_path.exists())


if __name__ == "__main__":
    unittest.main()

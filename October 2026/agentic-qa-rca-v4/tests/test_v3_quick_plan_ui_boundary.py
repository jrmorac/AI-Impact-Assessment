import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHAREABLE_ROOT = ROOT.parent / "agentic-qa-rca-shareable-v3"


class QuickPlanUiBoundaryTests(unittest.TestCase):
    def assert_ui_hides_quick_plans(self, html_path):
        source = html_path.read_text(encoding="utf-8")
        self.assertNotIn('id="quickPlan"', source)
        self.assertNotIn('id="runQuickPlanBtn"', source)
        self.assertNotIn("function runQuickPlan", source)
        self.assertNotIn('"/api/run-quick-plan"', source)

    def test_working_ui_hides_quick_plans(self):
        self.assert_ui_hides_quick_plans(ROOT / "web" / "index.html")

    def test_shareable_ui_hides_quick_plans(self):
        self.assert_ui_hides_quick_plans(SHAREABLE_ROOT / "web" / "index.html")

    def test_automation_entrypoint_remains_available(self):
        source = (ROOT / "src" / "main.py").read_text(encoding="utf-8")
        self.assertIn("quick_plan", source)
        self.assertIn("run_guided_rca", source)


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHAREABLE_ROOT = ROOT.parent / "agentic-qa-rca-shareable-v3"


class TerminalCarouselContractTests(unittest.TestCase):
    def assert_terminal_carousel_contract(self, html_path):
        source = html_path.read_text(encoding="utf-8")
        self.assertIn('"root_cause_confirmed"', source)
        self.assertIn('"target_depth_reached"', source)
        self.assertIn('"max_depth_reached"', source)
        self.assertIn("terminalWithHistory", source)
        self.assertIn("? history.length - 1", source)
        self.assertIn("(terminalWithHistory && historyIndex >= history.length - 1)", source)
        self.assertIn("if (terminal ||", source)

    def test_working_v3_terminal_demo_contract(self):
        self.assert_terminal_carousel_contract(ROOT / "web" / "index.html")

    def test_shareable_v3_terminal_demo_contract(self):
        self.assert_terminal_carousel_contract(SHAREABLE_ROOT / "web" / "index.html")


if __name__ == "__main__":
    unittest.main()

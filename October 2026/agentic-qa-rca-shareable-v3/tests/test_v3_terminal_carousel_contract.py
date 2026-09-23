import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TerminalCarouselContractTests(unittest.TestCase):
    def test_shareable_v3_terminal_demo_contract(self):
        source = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        self.assertIn('"root_cause_confirmed"', source)
        self.assertIn('"target_depth_reached"', source)
        self.assertIn('"max_depth_reached"', source)
        self.assertIn("terminalWithHistory", source)
        self.assertIn("? history.length - 1", source)
        self.assertIn("(terminalWithHistory && historyIndex >= history.length - 1)", source)
        self.assertIn("if (terminal ||", source)


if __name__ == "__main__":
    unittest.main()

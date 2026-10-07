import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import agents
import interactive_rca
from io_utils import load_yaml

PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"


class F008PromptTemplateExtractionTests(unittest.TestCase):
    """Covers F-008: Five Whys question templates and answer guidance are loaded
    from versioned files under prompts/ instead of being hardcoded in function
    bodies. Behavior must stay byte-identical to the pre-extraction hardcoded text."""

    def test_prompt_files_exist_with_version_field(self):
        for filename in (
            "five_whys_question_templates.yaml",
            "guided_rca_question_templates.yaml",
            "answer_guidance_templates.yaml",
        ):
            path = PROMPTS_DIR / filename
            self.assertTrue(path.is_file(), f"Missing prompt template file: {path}")
            config = load_yaml(path)
            self.assertEqual(config.get("version"), 1)

    def test_five_why_templates_match_expected_text_per_category(self):
        expected_first_by_category = {
            "performance": "Why did the system exceed the expected response-time threshold?",
            "data-quality": "Why did data integrity break (null/duplicate/inconsistent values)?",
            "business-rule": "Why did rule evaluation produce an incorrect decision?",
            "integration": "Why did the interface or contract fail between systems?",
            "security": "Why did the control fail to prevent unauthorized behavior?",
            "test-automation": "Why did the test process produce unstable or inconsistent results?",
        }
        expected_remaining = [
            "Why was the immediate technical condition possible?",
            "Why did prevention controls not stop this earlier?",
            "Why did detection controls not catch this before impact?",
            "Why does the process allow this pattern to recur?",
        ]
        for category, expected_first in expected_first_by_category.items():
            templates = agents._five_why_templates(category)
            self.assertEqual(templates[0], expected_first)
            self.assertEqual(templates[1:], expected_remaining)

    def test_five_why_templates_default_for_unknown_category(self):
        templates = agents._five_why_templates("unknown-category")
        self.assertEqual(templates[0], "Why did the observed defect happen in the current process?")

    def test_guided_first_question_matches_expected_text(self):
        defect = {"component": "TargetComponent", "summary": "Synthetic summary", "observed_behavior": "Synthetic observed"}
        question = interactive_rca._build_first_question(defect, "data-quality")
        self.assertEqual(
            question,
            "Why did Synthetic summary (Synthetic observed) occur in TargetComponent, and what evidence "
            "supports that first causal explanation? Start with the most direct data-quality cause you can defend.",
        )

    def test_guided_next_question_matches_expected_text(self):
        question = interactive_rca._build_next_question("Because the validation step was skipped under load.")
        self.assertEqual(
            question,
            "What deeper cause made this possible: the validation step was skipped under load? "
            "What evidence shows that this deeper cause is real rather than assumed?",
        )

    def test_answer_guidance_matches_expected_text_for_all_checks(self):
        checks = {
            "answer_specific_enough": False,
            "evidence_items_sufficient": False,
            "causal_link_stated": False,
            "controllable_cause": False,
            "prevents_recurrence": False,
        }
        requests = interactive_rca._build_data_requests(checks)
        self.assertEqual(
            requests,
            [
                "Refine the answer so it names a specific mechanism or control failure, not a broad symptom.",
                "Attach at least one evidence item that supports this answer before moving to the next Why.",
                "Rewrite the answer so it clearly explains why this cause led to the previous problem statement.",
                "Clarify whether this cause is within the team's ability to change or control.",
                "Explain whether removing this cause would actually stop recurrence, and why.",
            ],
        )

    def test_answer_guidance_omits_passing_checks(self):
        checks = {
            "answer_specific_enough": True,
            "evidence_items_sufficient": True,
            "causal_link_stated": True,
            "controllable_cause": True,
            "prevents_recurrence": True,
        }
        self.assertEqual(interactive_rca._build_data_requests(checks), [])


if __name__ == "__main__":
    unittest.main()

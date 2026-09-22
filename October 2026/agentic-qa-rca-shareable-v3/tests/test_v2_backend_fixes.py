import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import web_app
from interactive_rca import answer_session, revise_current_answer


def _session(status="awaiting_answer", current_why_index=1, why_chain=None):
    return {
        "session_id": "synthetic-session",
        "status": status,
        "current_why_index": current_why_index,
        "current_question": f"Why {current_why_index}?",
        "session_config": {
            "min_depth": 1,
            "target_depth": 5,
            "max_depth": 8,
            "min_answer_length": 10,
            "min_evidence_items": 1,
        },
        "why_chain": why_chain or [],
    }


class WebBackendFixTests(unittest.TestCase):
    def test_run_demo_dispatches_at_route_level(self):
        handler = object.__new__(web_app.RcaWebHandler)
        handler.path = "/api/run-demo"
        with patch.object(web_app, "_read_json_body", return_value={}), patch.object(
            handler, "_handle_run_demo"
        ) as run_demo:
            handler._dispatch_post()
        run_demo.assert_called_once_with({})

    def test_export_defaults_and_choice_validation(self):
        session_path = web_app.PROJECT_ROOT / "evidence" / "rca_sessions" / "synthetic.json"
        self.assertEqual(
            web_app._export_output_path({}, session_path, "capa"),
            web_app.PROJECT_ROOT / "evidence" / "capa_exports" / "synthetic-capa.csv",
        )
        self.assertEqual(
            web_app._export_output_path({}, session_path, "testcases"),
            web_app.PROJECT_ROOT / "evidence" / "capa_exports" / "synthetic-testcases.csv",
        )
        self.assertEqual(web_app._validated_choice({}, "provider", "ado", web_app.CAPA_PROVIDERS), "ado")
        with self.assertRaises(web_app.RequestValidationError):
            web_app._validated_choice({"provider": "other"}, "provider", "ado", web_app.CAPA_PROVIDERS)
        with self.assertRaises(web_app.RequestValidationError):
            web_app._validated_choice({"variant_set": "other"}, "variant_set", "standard", web_app.ADO_VARIANT_SETS)


class InteractiveRcaFixTests(unittest.TestCase):
    def _write_session(self, session, folder):
        path = Path(folder) / "session.json"
        path.write_text(json.dumps(session), encoding="utf-8")
        return path

    def test_answer_requires_awaiting_answer_and_revision_requires_gated_state(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self._write_session(_session(status="needs_more_evidence"), folder)
            with self.assertRaises(ValueError):
                answer_session(
                    session_path=path,
                    answer="A sufficiently specific causal answer because the control failed.",
                    evidence_refs=["synthetic.log"],
                    resolved=False,
                    controllable=True,
                    prevents_recurrence=False,
                )

            closed = self._write_session(_session(status="closed"), folder)
            with self.assertRaises(ValueError):
                revise_current_answer(
                    session_path=closed,
                    answer="A revised synthetic answer because evidence confirms it.",
                    evidence_refs=["synthetic.log"],
                    resolved=False,
                    controllable=True,
                    prevents_recurrence=False,
                )

    def test_revision_replaces_explicit_node_and_preserves_question(self):
        chain = [
            {"why_index": 1, "question": "Original Why 1?", "answer": "Original answer", "evidence_refs": ["old.log"]},
            {"why_index": 2, "question": "Original Why 2?", "answer": "Needs revision", "evidence_refs": ["weak.log"]},
        ]
        with tempfile.TemporaryDirectory() as folder:
            path = self._write_session(_session("needs_more_evidence", 2, chain), folder)
            result = revise_current_answer(
                session_path=path,
                answer="A stronger synthetic cause because the control boundary failed.",
                evidence_refs=["synthetic.log"],
                resolved=False,
                controllable=True,
                prevents_recurrence=False,
                target_why_index=1,
            )
        self.assertEqual(len(result["why_chain"]), 2)
        self.assertEqual(result["why_chain"][0]["why_index"], 1)
        self.assertEqual(result["why_chain"][0]["question"], "Original Why 1?")
        self.assertEqual(result["why_chain"][0]["answer"], "A stronger synthetic cause because the control boundary failed.")

    def test_target_depth_stops_without_creating_why_six(self):
        chain = [
            {"why_index": index, "question": f"Why {index}?", "answer": f"Answer {index}"}
            for index in range(1, 5)
        ]
        with tempfile.TemporaryDirectory() as folder:
            path = self._write_session(_session("awaiting_answer", 5, chain), folder)
            result = answer_session(
                session_path=path,
                answer="A valid non-stopping cause because the control was missing.",
                evidence_refs=["synthetic.log"],
                resolved=False,
                controllable=True,
                prevents_recurrence=False,
            )
        self.assertEqual(result["status"], "target_depth_reached")
        self.assertEqual(result["current_why_index"], 5)
        self.assertEqual(len(result["why_chain"]), 5)

    def test_advanced_continuation_allows_target_depth_to_continue(self):
        session = _session("awaiting_answer", 5, [])
        session["session_config"]["advanced_continuation"] = True
        with tempfile.TemporaryDirectory() as folder:
            path = self._write_session(session, folder)
            result = answer_session(
                session_path=path,
                answer="A valid deeper cause because the control was missing.",
                evidence_refs=["synthetic.log"],
                resolved=False,
                controllable=True,
                prevents_recurrence=False,
            )
        self.assertEqual(result["status"], "awaiting_answer")
        self.assertEqual(result["current_why_index"], 6)


if __name__ == "__main__":
    unittest.main()

import io
import json
import logging
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import orchestrator
import web_app


class FakeHandler:
    def __init__(self):
        self.request_id = "synthetic-request"
        self.response_status = 200
        self.wfile = io.BytesIO()
        self.sent_headers = {}

    def send_response(self, status):
        self.response_status = status

    def send_header(self, name, value):
        self.sent_headers[name] = value

    def end_headers(self):
        pass


def _triage_kwargs():
    return {
        "defect": {
            "defect_id": "synthetic-defect-001",
            "summary": "Synthetic API timeout under a deterministic test load",
            "observed_behavior": "The synthetic request exceeds the timeout threshold.",
            "expected_behavior": "The synthetic request completes within the agreed threshold.",
            "component": "synthetic-api",
            "severity": "high",
            "evidence": [{"type": "log", "ref": "synthetic-log.txt"}],
        },
        "required_fields": ["summary", "observed_behavior", "expected_behavior", "component", "severity"],
        "severity_model": {"high": 4},
        "known_categories": ["performance", "data-quality"],
        "confidence_calibration": {},
        "prioritization_weights": {},
        "priority_tiers": {},
        "min_hypothesis_support": 0.65,
        "require_evidence_artifact_for_capa": True,
        "min_artifact_quality_score": 0.60,
        "require_artifact_traceability": True,
        "require_capa_validation_experiment": True,
        "outcome_evaluation_policy": {},
        "min_confidence": 0.70,
        "request_id": "synthetic-request",
        "session_id": "synthetic-session",
    }


class V3ObservabilityTests(unittest.TestCase):
    def test_agent_step_schema_duration_correlation_and_legacy_trace_shape(self):
        with self.assertLogs(orchestrator.LOGGER, level=logging.INFO) as captured:
            _, _, _, traces = orchestrator.run_triage_agents(**_triage_kwargs())

        events = [json.loads(record.getMessage()) for record in captured.records]
        self.assertEqual(len(events), orchestrator.MAX_TRIAGE_STEPS)
        self.assertEqual([event["step_index"] for event in events], [1, 2, 3])
        self.assertEqual(
            [event["step_name"] for event in events],
            list(orchestrator.TRIAGE_STEP_NAMES),
        )
        for event in events:
            self.assertEqual(
                set(event),
                {"event", "step_name", "step_index", "duration_ms", "outcome", "defect_id", "request_id", "session_id"},
            )
            self.assertEqual(event["event"], "agent_step")
            self.assertGreaterEqual(event["duration_ms"], 0)
            self.assertEqual(event["outcome"], "success")
            self.assertEqual(event["defect_id"], "synthetic-defect-001")
            self.assertEqual(event["request_id"], "synthetic-request")
            self.assertEqual(event["session_id"], "synthetic-session")

        self.assertEqual(len(traces), orchestrator.MAX_TRIAGE_STEPS)
        for trace in traces:
            self.assertEqual(set(trace), {"timestamp_utc", "agent", "input", "output"})

    def test_fixed_step_configuration_is_three(self):
        self.assertEqual(orchestrator.MAX_TRIAGE_STEPS, 3)
        orchestrator._validate_fixed_step_sequence()

    def test_server_error_logs_traceback_but_response_is_sanitized(self):
        handler = FakeHandler()
        try:
            raise RuntimeError("synthetic internal detail")
        except RuntimeError as exc:
            with self.assertLogs(web_app.LOGGER, level=logging.INFO) as captured:
                handler._handle_exception = web_app.RcaWebHandler._handle_exception.__get__(handler)
                handler._handle_exception(exc)

        response = json.loads(handler.wfile.getvalue())
        self.assertEqual(response["error_code"], "INTERNAL_ERROR")
        self.assertNotIn("synthetic internal detail", json.dumps(response))
        error_events = [json.loads(record.getMessage()) for record in captured.records]
        self.assertEqual(len(error_events), 1)
        self.assertIn("RuntimeError", error_events[0]["traceback"])
        self.assertNotIn("synthetic internal detail", json.dumps(response))
        self.assertEqual(error_events[0]["request_id"], "synthetic-request")

    def test_client_error_does_not_log_traceback(self):
        handler = FakeHandler()
        error = web_app.RequestValidationError("synthetic invalid request")
        with self.assertLogs(web_app.LOGGER, level=logging.INFO) as captured:
            handler._handle_exception = web_app.RcaWebHandler._handle_exception.__get__(handler)
            handler._handle_exception(error)

        event = json.loads(captured.records[0].getMessage())
        response = json.loads(handler.wfile.getvalue())
        self.assertEqual(response["error_code"], "INVALID_REQUEST")
        self.assertNotIn("traceback", event)


if __name__ == "__main__":
    unittest.main()
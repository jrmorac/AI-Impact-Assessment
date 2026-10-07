import json
import logging
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import orchestrator


def _triage_kwargs(**overrides):
    base = {
        "defect": {
            "defect_id": "synthetic-defect-100",
            "summary": "Synthetic error-path defect under a deterministic test load",
            "observed_behavior": "The synthetic request fails before completing triage.",
            "expected_behavior": "The synthetic request completes triage successfully.",
            "component": "synthetic-component",
            "severity": "medium",
            "evidence": [{"type": "log", "ref": "synthetic-log.txt"}],
        },
        "required_fields": ["summary", "observed_behavior", "expected_behavior", "component", "severity"],
        "severity_model": {"medium": 2},
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
        "request_id": "synthetic-request-100",
        "session_id": "synthetic-session-100",
    }
    base.update(overrides)
    return base


class F007ErrorLifecycleEventTests(unittest.TestCase):
    """Covers F-007: a dedicated `error` lifecycle event emitted alongside the
    existing agent_step outcome='error' behavior, with no raw traceback leaked."""

    def _events(self, captured):
        return [json.loads(record.getMessage()) for record in captured.records]

    def test_planner_exception_emits_error_event_alongside_agent_step(self):
        with mock.patch.object(orchestrator, "planner_agent", side_effect=ValueError("synthetic planner failure")):
            with self.assertLogs(orchestrator.LOGGER, level=logging.INFO) as captured:
                with self.assertRaises(ValueError):
                    orchestrator.run_triage_agents(**_triage_kwargs())

        events = self._events(captured)
        error_events = [event for event in events if event["event"] == "error"]
        agent_step_events = [event for event in events if event["event"] == "agent_step"]

        self.assertEqual(len(error_events), 1)
        error_event = error_events[0]
        self.assertEqual(error_event["error_type"], "ValueError")
        self.assertEqual(error_event["error_category"], "permanent")
        self.assertEqual(error_event["step_name"], "planner_agent")
        self.assertEqual(error_event["defect_id"], "synthetic-defect-100")
        self.assertEqual(error_event["request_id"], "synthetic-request-100")
        self.assertEqual(error_event["session_id"], "synthetic-session-100")
        self.assertNotIn("traceback", error_event)
        self.assertNotIn("synthetic planner failure", json.dumps(error_event))

        self.assertEqual(len(agent_step_events), 1)
        self.assertEqual(agent_step_events[0]["outcome"], "error")

    def test_analyzer_exception_emits_error_event_with_permanent_category(self):
        with mock.patch.object(orchestrator, "analyzer_agent", side_effect=KeyError("synthetic-config-key")):
            with self.assertLogs(orchestrator.LOGGER, level=logging.INFO) as captured:
                with self.assertRaises(KeyError):
                    orchestrator.run_triage_agents(**_triage_kwargs())

        error_events = [event for event in self._events(captured) if event["event"] == "error"]
        self.assertEqual(len(error_events), 1)
        self.assertEqual(error_events[0]["step_name"], "analyzer_agent")
        self.assertEqual(error_events[0]["error_type"], "KeyError")
        self.assertEqual(error_events[0]["error_category"], "permanent")
        self.assertNotIn("traceback", error_events[0])

    def test_validator_exception_emits_error_event_with_guardrail_category(self):
        with mock.patch.object(orchestrator, "validator_agent", side_effect=RuntimeError("synthetic validator failure")):
            with self.assertLogs(orchestrator.LOGGER, level=logging.INFO) as captured:
                with self.assertRaises(RuntimeError):
                    orchestrator.run_triage_agents(**_triage_kwargs())

        error_events = [event for event in self._events(captured) if event["event"] == "error"]
        self.assertEqual(len(error_events), 1)
        self.assertEqual(error_events[0]["step_name"], "validator_agent")
        self.assertEqual(error_events[0]["error_category"], "guardrail")
        self.assertNotIn("traceback", error_events[0])

    def test_capa_agent_exception_emits_error_event(self):
        session = {"session_id": "synthetic-session-capa", "defect": {"defect_id": "synthetic-defect-100"}}
        with mock.patch.object(orchestrator, "generate_capa_tasks", side_effect=ValueError("synthetic capa failure")):
            with self.assertLogs(orchestrator.LOGGER, level=logging.INFO) as captured:
                with self.assertRaises(ValueError):
                    orchestrator.run_capa_agent(session, request_id="synthetic-request-200")

        events = self._events(captured)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event"], "error")
        self.assertEqual(events[0]["step_name"], "capa_agent")
        self.assertEqual(events[0]["error_category"], "permanent")
        self.assertEqual(events[0]["session_id"], "synthetic-session-capa")
        self.assertEqual(events[0]["request_id"], "synthetic-request-200")
        self.assertNotIn("traceback", events[0])

    def test_testcase_agent_exception_emits_error_event(self):
        session = {"session_id": "synthetic-session-tc", "defect": {"defect_id": "synthetic-defect-100"}}
        with mock.patch.object(orchestrator, "generate_ado_test_cases", side_effect=ValueError("synthetic testcase failure")):
            with self.assertLogs(orchestrator.LOGGER, level=logging.INFO) as captured:
                with self.assertRaises(ValueError):
                    orchestrator.run_testcase_agent(session, "standard")

        events = self._events(captured)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event"], "error")
        self.assertEqual(events[0]["step_name"], "testcase_agent")
        self.assertEqual(events[0]["session_id"], "synthetic-session-tc")
        self.assertNotIn("traceback", events[0])

    def test_successful_triage_run_does_not_emit_spurious_error_event(self):
        with self.assertLogs(orchestrator.LOGGER, level=logging.INFO) as captured:
            orchestrator.run_triage_agents(**_triage_kwargs())

        events = self._events(captured)
        self.assertTrue(events)
        self.assertFalse(any(event["event"] == "error" for event in events))
        self.assertTrue(all(event["outcome"] == "success" for event in events if event["event"] == "agent_step"))

    def test_successful_capa_and_testcase_flows_do_not_emit_spurious_error_event(self):
        session = {
            "session_id": "synthetic-session-ok",
            "defect": {
                "defect_id": "synthetic-defect-100",
                "component": "synthetic-component",
                "summary": "Synthetic defect",
            },
            "root_cause_summary": "Synthetic confirmed root cause",
            "why_chain": [],
        }
        with mock.patch.object(orchestrator.LOGGER, "info") as mock_info:
            tasks, _ = orchestrator.run_capa_agent(session)
            test_cases, _ = orchestrator.run_testcase_agent(session, "standard")

        self.assertTrue(tasks)
        self.assertTrue(test_cases)
        mock_info.assert_not_called()


if __name__ == "__main__":
    unittest.main()

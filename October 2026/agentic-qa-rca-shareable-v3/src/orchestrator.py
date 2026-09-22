from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

from agents import AgentResult, analyzer_agent, planner_agent, validator_agent
from workflow_agents import generate_ado_test_cases, generate_capa_tasks

LOGGER = logging.getLogger("agentic_qa.orchestrator")
LOGGER.setLevel(logging.INFO)
LOGGER.propagate = False
if not LOGGER.handlers:
    _log_handler = logging.StreamHandler()
    _log_handler.setFormatter(logging.Formatter("%(message)s"))
    LOGGER.addHandler(_log_handler)
TRIAGE_STEP_NAMES = ("planner_agent", "analyzer_agent", "validator_agent")
MAX_TRIAGE_STEPS = 3
LOCAL_LOG_RETENTION_DAYS = 360


def _validate_fixed_step_sequence() -> None:
    if len(TRIAGE_STEP_NAMES) != MAX_TRIAGE_STEPS:
        raise AssertionError("Triage must remain a fixed three-step sequence")


def _emit_agent_step(
    *,
    step_name: str,
    step_index: int,
    started_at: float,
    outcome: str,
    defect_id: str,
    request_id: str | None,
    session_id: str | None,
) -> None:
    event: Dict[str, Any] = {
        "event": "agent_step",
        "step_name": step_name,
        "step_index": step_index,
        "duration_ms": max(0, int(round((time.monotonic() - started_at) * 1000))),
        "outcome": outcome,
        "defect_id": defect_id,
    }
    if request_id:
        event["request_id"] = request_id
    if session_id:
        event["session_id"] = session_id
    LOGGER.info(json.dumps(event, separators=(",", ":"), sort_keys=True))


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_capa_agent(session: Dict[str, object]) -> Tuple[List[Dict[str, str]], List[Dict[str, object]]]:
    tasks = generate_capa_tasks(session)
    trace = [
        {
            "timestamp_utc": _now_utc(),
            "agent": "capa_agent",
            "input": {"session_id": str(session.get("session_id", "")), "type": "rca_session"},
            "output": {"tasks_generated": len(tasks)},
        }
    ]
    return tasks, trace


def run_testcase_agent(
    session: Dict[str, object],
    variant_set: str,
) -> Tuple[List[Dict[str, str]], List[Dict[str, object]]]:
    test_cases = generate_ado_test_cases(session, variant_set=variant_set)
    trace = [
        {
            "timestamp_utc": _now_utc(),
            "agent": "testcase_agent",
            "input": {
                "session_id": str(session.get("session_id", "")),
                "variant_set": variant_set,
                "type": "rca_session",
            },
            "output": {"test_cases_generated": len(test_cases)},
        }
    ]
    return test_cases, trace


def run_triage_agents(
    *,
    defect: Dict[str, Any],
    required_fields: List[str],
    severity_model: Dict[str, int],
    known_categories: List[str],
    confidence_calibration: Dict[str, float],
    prioritization_weights: Dict[str, float],
    priority_tiers: Dict[str, int],
    min_hypothesis_support: float,
    require_evidence_artifact_for_capa: bool,
    min_artifact_quality_score: float,
    require_artifact_traceability: bool,
    require_capa_validation_experiment: bool,
    outcome_evaluation_policy: Dict[str, float],
    min_confidence: float,
    request_id: str | None = None,
    session_id: str | None = None,
) -> Tuple[List[str], AgentResult, Dict[str, object], List[Dict[str, object]]]:
    _validate_fixed_step_sequence()
    defect_id = str(defect.get("defect_id", ""))
    planner_started_at = time.monotonic()
    try:
        missing_fields = planner_agent(defect, required_fields)
    except Exception:
        _emit_agent_step(
            step_name=TRIAGE_STEP_NAMES[0], step_index=1, started_at=planner_started_at,
            outcome="error", defect_id=defect_id, request_id=request_id, session_id=session_id,
        )
        raise
    _emit_agent_step(
        step_name=TRIAGE_STEP_NAMES[0], step_index=1, started_at=planner_started_at,
        outcome="success", defect_id=defect_id, request_id=request_id, session_id=session_id,
    )
    planner_trace = {
        "timestamp_utc": _now_utc(),
        "agent": "planner_agent",
        "input": {
            "defect_id": str(defect.get("defect_id", "")),
            "required_fields_count": len(required_fields),
        },
        "output": {
            "missing_fields_count": len(missing_fields),
            "missing_fields": missing_fields,
        },
    }

    analyzer_started_at = time.monotonic()
    try:
        agent_result = analyzer_agent(
            defect,
            severity_model,
            known_categories,
            missing_fields,
            confidence_calibration,
            prioritization_weights,
            priority_tiers,
            min_hypothesis_support,
            require_evidence_artifact_for_capa,
            min_artifact_quality_score,
            require_artifact_traceability,
            require_capa_validation_experiment,
            outcome_evaluation_policy,
        )
    except Exception:
        _emit_agent_step(
            step_name=TRIAGE_STEP_NAMES[1], step_index=2, started_at=analyzer_started_at,
            outcome="error", defect_id=defect_id, request_id=request_id, session_id=session_id,
        )
        raise
    _emit_agent_step(
        step_name=TRIAGE_STEP_NAMES[1], step_index=2, started_at=analyzer_started_at,
        outcome="success", defect_id=defect_id, request_id=request_id, session_id=session_id,
    )
    analyzer_trace = {
        "timestamp_utc": _now_utc(),
        "agent": "analyzer_agent",
        "input": {
            "defect_id": str(defect.get("defect_id", "")),
            "missing_fields_count": len(missing_fields),
        },
        "output": {
            "category": agent_result.category,
            "confidence": agent_result.confidence,
            "action_mode": agent_result.action_mode,
            "priority_tier": agent_result.priority_tier,
        },
    }

    validator_started_at = time.monotonic()
    try:
        validation = validator_agent(
            agent_result,
            missing_fields,
            min_confidence,
            min_hypothesis_support,
            min_artifact_quality_score,
            require_artifact_traceability,
            require_capa_validation_experiment,
        )
    except Exception:
        _emit_agent_step(
            step_name=TRIAGE_STEP_NAMES[2], step_index=3, started_at=validator_started_at,
            outcome="error", defect_id=defect_id, request_id=request_id, session_id=session_id,
        )
        raise
    _emit_agent_step(
        step_name=TRIAGE_STEP_NAMES[2], step_index=3, started_at=validator_started_at,
        outcome="success", defect_id=defect_id, request_id=request_id, session_id=session_id,
    )
    validator_trace = {
        "timestamp_utc": _now_utc(),
        "agent": "validator_agent",
        "input": {
            "defect_id": str(defect.get("defect_id", "")),
            "confidence": agent_result.confidence,
            "action_mode": agent_result.action_mode,
        },
        "output": {
            "accepted": bool(validation.get("accepted", False)),
            "checks_passed": sum(
                1 for passed in (validation.get("checks", {}) or {}).values() if bool(passed)
            ),
            "checks_total": len(validation.get("checks", {}) or {}),
        },
    }

    return missing_fields, agent_result, validation, [planner_trace, analyzer_trace, validator_trace]

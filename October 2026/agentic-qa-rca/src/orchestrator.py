from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

from agents import AgentResult, analyzer_agent, planner_agent, validator_agent
from workflow_agents import generate_ado_test_cases, generate_capa_tasks


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
) -> Tuple[List[str], AgentResult, Dict[str, object], List[Dict[str, object]]]:
    missing_fields = planner_agent(defect, required_fields)
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

    validation = validator_agent(
        agent_result,
        missing_fields,
        min_confidence,
        min_hypothesis_support,
        min_artifact_quality_score,
        require_artifact_traceability,
        require_capa_validation_experiment,
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

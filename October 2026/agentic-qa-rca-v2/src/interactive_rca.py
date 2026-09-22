from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from agents import analyzer_agent, planner_agent
from io_utils import load_json, write_json


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _strip_causal_prefix(answer: str) -> str:
    normalized = answer.strip().rstrip(".")
    prefixes = [
        "because ",
        "due to ",
        "it happened because ",
        "the problem happened because ",
        "the issue happened because ",
        "this happened because ",
    ]
    lowered = normalized.lower()
    for prefix in prefixes:
        if lowered.startswith(prefix):
            return normalized[len(prefix):].strip()
    return normalized


def _first_sentence(text: str) -> str:
    stripped = text.strip()
    if not stripped:
        return "the prior answer"
    sentence = stripped.split(".")[0].strip()
    return sentence or stripped


def _normalize_focus_clause(answer: str) -> str:
    stripped = _strip_causal_prefix(answer)
    primary = stripped.split(",")[0].strip()
    primary = primary.split(";", 1)[0].strip()
    return primary.rstrip(".") or stripped


def _problem_statement(defect: Dict[str, Any]) -> str:
    summary = str(defect.get("summary", "")).strip()
    observed = str(defect.get("observed_behavior", "")).strip()
    if summary and observed:
        return f"{summary} ({observed})"
    if summary:
        return summary
    if observed:
        return observed
    return "the reported problem"


def _build_first_question(defect: Dict[str, Any], category: str) -> str:
    component = str(defect.get("component", "the target component")).strip()
    problem = _problem_statement(defect)
    return (
        f"Why did {problem} occur in {component}, and what evidence supports that first causal explanation? "
        f"Start with the most direct {category} cause you can defend."
    )


def _build_next_question(previous_answer: str) -> str:
    cause_clause = _first_sentence(_normalize_focus_clause(previous_answer))
    return (
        f"What deeper cause made this possible: {cause_clause}? What evidence shows that this deeper cause is real rather than assumed?"
    )


def _build_data_requests(checks: Dict[str, bool]) -> List[str]:
    requests: List[str] = []
    if not checks["answer_specific_enough"]:
        requests.append("Refine the answer so it names a specific mechanism or control failure, not a broad symptom.")
    if not checks["evidence_items_sufficient"]:
        requests.append("Attach at least one evidence item that supports this answer before moving to the next Why.")
    if not checks["causal_link_stated"]:
        requests.append("Rewrite the answer so it clearly explains why this cause led to the previous problem statement.")
    if not checks["controllable_cause"]:
        requests.append("Clarify whether this cause is within the team's ability to change or control.")
    if not checks["prevents_recurrence"]:
        requests.append("Explain whether removing this cause would actually stop recurrence, and why.")
    return requests


def _evaluate_checkpoint(
    *,
    answer: str,
    evidence_refs: List[str],
    resolved: bool,
    controllable: bool,
    prevents_recurrence: bool,
    why_index: int,
    session_cfg: Dict[str, Any],
    advanced_continuation: bool = False,
) -> Dict[str, Any]:
    min_depth = int(session_cfg.get("min_depth", 1))
    max_depth = int(session_cfg.get("max_depth", 8))
    target_depth = int(session_cfg.get("target_depth", 5))
    min_answer_length = int(session_cfg.get("min_answer_length", 25))
    min_evidence_items = int(session_cfg.get("min_evidence_items", 1))

    checks = {
        "answer_specific_enough": len(answer.strip()) >= min_answer_length,
        "evidence_items_sufficient": len([item for item in evidence_refs if item.strip()]) >= min_evidence_items,
        "causal_link_stated": any(token in answer.lower() for token in ["because", "due to", "caused by", "led to"]),
        "controllable_cause": controllable,
        "prevents_recurrence": prevents_recurrence,
        "resolved_by_this_cause": resolved,
        "minimum_depth_met": why_index >= min_depth,
        "max_depth_reached": why_index >= max_depth,
        "target_depth_reached": why_index >= target_depth,
    }

    if not checks["answer_specific_enough"] or not checks["evidence_items_sufficient"] or not checks["causal_link_stated"]:
        decision = "needs_more_evidence"
    elif checks["resolved_by_this_cause"] and checks["controllable_cause"] and checks["prevents_recurrence"] and checks["minimum_depth_met"]:
        decision = "stop_root_cause_confirmed"
    elif checks["max_depth_reached"]:
        decision = "stop_max_depth_reached"
    elif checks["target_depth_reached"] and not advanced_continuation:
        decision = "stop_target_depth_reached"
    else:
        decision = "continue"

    return {
        "decision": decision,
        "checks": checks,
        "recommended_data_requests": _build_data_requests(checks),
    }


def _session_defaults(rca_cfg: Dict[str, Any]) -> Dict[str, Any]:
    interactive_cfg = rca_cfg.get("interactive", {})
    return {
        "min_depth": int(interactive_cfg.get("min_depth", 1)),
        "target_depth": int(interactive_cfg.get("target_depth", 5)),
        "max_depth": int(interactive_cfg.get("max_depth", 8)),
        "advanced_continuation": bool(interactive_cfg.get("advanced_continuation", False)),
        "min_answer_length": int(interactive_cfg.get("min_answer_length", 25)),
        "min_evidence_items": int(interactive_cfg.get("min_evidence_items", 1)),
    }


def _build_session_node(
    *,
    why_index: int,
    question: str,
    answer: str,
    evidence_refs: List[str],
    resolved: bool,
    controllable: bool,
    prevents_recurrence: bool,
    checkpoint: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "why_index": why_index,
        "question": question,
        "answer": answer,
        "evidence_refs": evidence_refs,
        "resolved_by_this_cause": resolved,
        "controllable_cause": controllable,
        "prevents_recurrence": prevents_recurrence,
        "checkpoint": checkpoint,
        "recorded_at_utc": _utc_now(),
    }


def _apply_decision_to_session(session: Dict[str, Any], *, why_index: int, answer: str, checkpoint: Dict[str, Any]) -> None:
    decision = checkpoint["decision"]
    if decision == "needs_more_evidence":
        session["status"] = "needs_more_evidence"
        session["current_why_index"] = why_index
        session["next_action"] = "Provide a revised answer or stronger evidence for the current Why."
    elif decision == "stop_root_cause_confirmed":
        session["status"] = "root_cause_confirmed"
        session["current_why_index"] = why_index
        session["root_cause_summary"] = answer
        session["stop_reason"] = "Checkpoint confirmed a controllable cause that should prevent recurrence."
        session["next_action"] = "Document CAPA and validation plan against this confirmed root cause."
    elif decision == "stop_max_depth_reached":
        session["status"] = "max_depth_reached"
        session["current_why_index"] = why_index
        session["root_cause_summary"] = answer
        session["stop_reason"] = "Maximum Why depth reached without confirmed stop condition. Escalate to facilitated review."
        session["next_action"] = "Escalate the case for facilitated RCA review and challenge remaining assumptions."
    elif decision == "stop_target_depth_reached":
        session["status"] = "target_depth_reached"
        session["current_why_index"] = why_index
        session["root_cause_summary"] = answer
        session["stop_reason"] = "Normal target Why depth reached without a confirmed stop condition. Enable advanced continuation for deeper analysis."
        session["next_action"] = "Review the RCA outcome or explicitly enable advanced continuation."
    else:
        session["status"] = "awaiting_answer"
        session["current_why_index"] = why_index + 1
        session["current_question"] = _build_next_question(answer)
        session["next_action"] = "Answer the next Why and attach evidence references."


def _build_report_markdown(session: Dict[str, Any]) -> str:
    defect = session.get("defect", {})
    why_chain = session.get("why_chain", [])
    evidence_refs: List[str] = []
    for node in why_chain:
        for item in node.get("evidence_refs", []):
            if item not in evidence_refs:
                evidence_refs.append(item)

    lines = [
        "# RCA Case Report",
        "",
        f"- Session ID: {session.get('session_id', '')}",
        f"- Generated UTC: {_utc_now()}",
        f"- Status: {session.get('status', '')}",
        f"- Defect ID: {defect.get('defect_id', '')}",
        f"- Category: {session.get('category', '')}",
        f"- Problem Summary: {_problem_statement(defect)}",
        f"- Root Cause Summary: {session.get('root_cause_summary', 'Not yet confirmed')}",
        f"- Stop Reason: {session.get('stop_reason', 'Not yet stopped')}",
        "",
        "## Why Chain",
        "",
    ]

    for node in why_chain:
        checkpoint = node.get("checkpoint", {})
        lines.extend(
            [
                f"### Why {node.get('why_index', '')}",
                f"- Question: {node.get('question', '')}",
                f"- Answer: {node.get('answer', '')}",
                f"- Evidence: {', '.join(node.get('evidence_refs', [])) or 'None'}",
                f"- Decision: {checkpoint.get('decision', '')}",
                f"- Controllable: {node.get('controllable_cause', False)}",
                f"- Prevents Recurrence: {node.get('prevents_recurrence', False)}",
                "",
            ]
        )

    lines.extend(["## Evidence Register", ""])
    if evidence_refs:
        lines.extend([f"- {item}" for item in evidence_refs])
    else:
        lines.append("- No evidence references recorded")

    lines.extend([
        "",
        "## Next Action",
        "",
        f"- {session.get('next_action', '')}",
        "",
    ])
    return "\n".join(lines)


def _load_defect(input_path: Path, defect_id: str) -> Dict[str, Any]:
    payload = load_json(input_path)
    if not isinstance(payload, list):
        raise ValueError("Interactive RCA requires an input JSON list of defect objects.")
    for defect in payload:
        if isinstance(defect, dict) and str(defect.get("defect_id")) == defect_id:
            return defect
    raise ValueError(f"Defect ID not found in input: {defect_id}")


def start_session(
    *,
    context: Dict[str, Any],
    quality_gates: Dict[str, Any],
    input_path: Path,
    defect_id: str,
    session_path: Path,
) -> Dict[str, Any]:
    defect = _load_defect(input_path, defect_id)

    agentic_cfg = context.get("agentic", {})
    rca_cfg = agentic_cfg.get("rca", {})
    severity_model = context.get("severity_model", {})
    known_categories = context.get("defect_taxonomy", [])
    required_fields = quality_gates.get("required_fields", [])

    agent_result = analyzer_agent(
        defect,
        severity_model,
        known_categories,
        planner_agent(defect, required_fields),
        agentic_cfg.get("confidence_calibration", {}),
        agentic_cfg.get("prioritization_weights", {}),
        agentic_cfg.get("priority_tiers", {}),
        float(rca_cfg.get("min_hypothesis_support", 0.65)),
        bool(rca_cfg.get("require_evidence_artifact_for_capa", True)),
        float(rca_cfg.get("min_artifact_quality_score", 0.60)),
        bool(rca_cfg.get("require_artifact_traceability", True)),
        bool(rca_cfg.get("require_capa_validation_experiment", True)),
        rca_cfg.get("outcome_evaluation", {}),
    )

    session_cfg = _session_defaults(rca_cfg)
    session = {
        "session_id": session_path.stem,
        "created_at_utc": _utc_now(),
        "updated_at_utc": _utc_now(),
        "status": "awaiting_answer",
        "project": context.get("project", {}),
        "input_file": str(input_path),
        "defect": defect,
        "category": agent_result.category,
        "current_why_index": 1,
        "current_question": _build_first_question(defect, agent_result.category),
        "session_config": session_cfg,
        "why_chain": [],
        "root_cause_summary": "",
        "stop_reason": "",
        "next_action": "Answer the current Why and attach evidence references.",
    }
    write_json(session_path, session)
    return session


def answer_session(
    *,
    session_path: Path,
    answer: str,
    evidence_refs: List[str],
    resolved: bool,
    controllable: bool,
    prevents_recurrence: bool,
    advanced_continuation: bool = False,
) -> Dict[str, Any]:
    session = load_json(session_path)
    if not isinstance(session, dict):
        raise ValueError("Session file is invalid.")

    status = str(session.get("status", ""))
    if status in {"root_cause_confirmed", "max_depth_reached", "target_depth_reached", "closed"}:
        raise ValueError(f"Session is already closed with status: {session.get('status')}")
    if status != "awaiting_answer":
        raise ValueError(f"Session does not accept an ordinary answer with status: {status}")

    why_index = int(session.get("current_why_index", 1))
    current_question = str(session.get("current_question", "")).strip()
    session_cfg = session.get("session_config", {})
    checkpoint = _evaluate_checkpoint(
        answer=answer,
        evidence_refs=evidence_refs,
        resolved=resolved,
        controllable=controllable,
        prevents_recurrence=prevents_recurrence,
        why_index=why_index,
        session_cfg=session_cfg,
        advanced_continuation=advanced_continuation or bool(session_cfg.get("advanced_continuation", False)),
    )

    node = _build_session_node(
        why_index=why_index,
        question=current_question,
        answer=answer,
        evidence_refs=evidence_refs,
        resolved=resolved,
        controllable=controllable,
        prevents_recurrence=prevents_recurrence,
        checkpoint=checkpoint,
    )

    why_chain = session.get("why_chain", [])
    if not isinstance(why_chain, list):
        why_chain = []
    why_chain.append(node)
    session["why_chain"] = why_chain

    _apply_decision_to_session(session, why_index=why_index, answer=answer, checkpoint=checkpoint)

    session["updated_at_utc"] = _utc_now()
    write_json(session_path, session)
    return session


def revise_current_answer(
    *,
    session_path: Path,
    answer: str,
    evidence_refs: List[str],
    resolved: bool,
    controllable: bool,
    prevents_recurrence: bool,
    target_why_index: int | None = None,
) -> Dict[str, Any]:
    session = load_json(session_path)
    if not isinstance(session, dict):
        raise ValueError("Session file is invalid.")

    status = str(session.get("status", ""))
    if status in {"root_cause_confirmed", "max_depth_reached", "target_depth_reached", "closed"}:
        raise ValueError(f"Session is already closed with status: {status}")
    why_chain = session.get("why_chain", [])
    if not isinstance(why_chain, list):
        raise ValueError("Session why_chain is invalid.")

    why_index = int(session.get("current_why_index", 1)) if target_why_index is None else int(target_why_index)
    replace_index = -1
    for idx, node in enumerate(why_chain):
        node = why_chain[idx]
        if int(node.get("why_index", -1)) == why_index:
            replace_index = idx
            break

    if replace_index == -1:
        raise ValueError("No current Why answer exists to revise. Use answer-rca first.")

    current_question = str(why_chain[replace_index].get("question", "")).strip()

    session_cfg = session.get("session_config", {})
    checkpoint = _evaluate_checkpoint(
        answer=answer,
        evidence_refs=evidence_refs,
        resolved=resolved,
        controllable=controllable,
        prevents_recurrence=prevents_recurrence,
        why_index=why_index,
        session_cfg=session_cfg,
        advanced_continuation=bool(session_cfg.get("advanced_continuation", False)),
    )

    why_chain[replace_index] = _build_session_node(
        why_index=why_index,
        question=current_question,
        answer=answer,
        evidence_refs=evidence_refs,
        resolved=resolved,
        controllable=controllable,
        prevents_recurrence=prevents_recurrence,
        checkpoint=checkpoint,
    )
    session["why_chain"] = why_chain
    _apply_decision_to_session(session, why_index=why_index, answer=answer, checkpoint=checkpoint)
    session["updated_at_utc"] = _utc_now()
    write_json(session_path, session)
    return session


def load_session_status(session_path: Path) -> Dict[str, Any]:
    session = load_json(session_path)
    if not isinstance(session, dict):
        raise ValueError("Session file is invalid.")
    return session


def export_session_report(*, session_path: Path, output_path: Path) -> Path:
    session = load_session_status(session_path)
    markdown = _build_report_markdown(session)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    return output_path
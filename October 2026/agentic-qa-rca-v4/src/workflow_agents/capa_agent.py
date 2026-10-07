from __future__ import annotations

from typing import Dict, List


def generate_capa_tasks(session: Dict[str, object]) -> List[Dict[str, str]]:
    defect = session.get("defect", {}) if isinstance(session, dict) else {}
    if not isinstance(defect, dict):
        defect = {}

    defect_id = str(defect.get("defect_id", "UNKNOWN-DEFECT")).strip() or "UNKNOWN-DEFECT"
    component = str(defect.get("component", "TargetComponent")).strip() or "TargetComponent"
    summary = str(defect.get("summary", "Recurring defect")).strip() or "Recurring defect"
    root_cause = str(session.get("root_cause_summary", "")).strip().rstrip(". ")

    evidence_refs: List[str] = []
    why_chain = session.get("why_chain", [])
    if isinstance(why_chain, list):
        for node in why_chain:
            if not isinstance(node, dict):
                continue
            refs = node.get("evidence_refs", [])
            if not isinstance(refs, list):
                continue
            for item in refs:
                ref = str(item).strip()
                if ref and ref not in evidence_refs:
                    evidence_refs.append(ref)

    evidence_line = ", ".join(evidence_refs) if evidence_refs else "No explicit evidence refs in session"

    traceability = (
        f"Corrective action for {summary} in {component}. Root cause: "
        f"{root_cause or 'RCA root cause pending confirmation'}. Evidence refs: {evidence_line}."
    )
    return [
        {
            "title": f"{defect_id}: Implement corrective control in {component}",
            "description": traceability,
            "owner_role": "Engineering",
            "priority": "High",
            "labels": f"capa,{defect_id.lower()},corrective-control",
        },
        {
            "title": f"{defect_id}: Add regression coverage for {summary}",
            "description": (
                f"Create a repeatable QA check that reproduces the observed behavior and verifies the expected behavior. {traceability}"
            ),
            "owner_role": "QA",
            "priority": "High",
            "labels": f"capa,{defect_id.lower()},regression-test",
        },
        {
            "title": f"{defect_id}: Add monitoring or workflow gate for recurrence",
            "description": (
                f"Add a measurable control that detects or blocks recurrence of {summary}, with an actionable failure signal. {traceability}"
            ),
            "owner_role": "QA",
            "priority": "Medium",
            "labels": f"capa,{defect_id.lower()},quality-gate",
        },
        {
            "title": f"{defect_id}: Validate corrective action effectiveness",
            "description": (
                f"Run a defined before/after validation sample, compare the observed and expected behavior, and record regression results. {traceability}"
            ),
            "owner_role": "QA",
            "priority": "Medium",
            "labels": f"capa,{defect_id.lower()},validation-experiment,metrics",
        },
    ]

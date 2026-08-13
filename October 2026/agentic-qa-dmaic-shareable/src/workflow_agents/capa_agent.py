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

    return [
        {
            "title": f"{defect_id}: Implement idempotency replay guard in {component}",
            "description": (
                f"Add merge-write replay/idempotency guard to prevent duplicate insertions for {summary}. "
                f"Root cause anchor: {root_cause or 'RCA confirmed recurring replay risk controls were missing'}. "
                f"Evidence refs: {evidence_line}."
            ),
            "owner_role": "Engineering",
            "priority": "High",
            "labels": f"capa,{defect_id.lower()},idempotency,replay-guard",
        },
        {
            "title": f"{defect_id}: Persist deterministic deduplication state",
            "description": (
                "Implement persisted dedup/replay-key state across nightly runs and enforce deterministic duplicate rejection. "
                f"Traceability: linked to RCA Why chain for {defect_id}."
            ),
            "owner_role": "Engineering",
            "priority": "High",
            "labels": f"capa,{defect_id.lower()},deduplication,data-quality",
        },
        {
            "title": f"{defect_id}: Add CI deterministic rerun gate test",
            "description": (
                "Create mandatory CI gate that runs same dataset twice under identical merge keys and fails when duplicate count > 0. "
                "Capture gate logs as release evidence."
            ),
            "owner_role": "QA",
            "priority": "High",
            "labels": f"capa,{defect_id.lower()},qa-gate,ci",
        },
        {
            "title": f"{defect_id}: Update release checklist with idempotency sign-off",
            "description": (
                "Add release criterion requiring explicit idempotency verification, evidence attachment, and accountable owner approval "
                "before promotion."
            ),
            "owner_role": "Release Management",
            "priority": "Medium",
            "labels": f"capa,{defect_id.lower()},release-governance",
        },
        {
            "title": f"{defect_id}: Run CAPA validation experiment and publish outcomes",
            "description": (
                "Execute at least five repeated-run pairs using deterministic input. Acceptance criteria: duplicate_key_count_after_rerun = 0 "
                "for all runs; publish baseline vs post metrics and any regression signals."
            ),
            "owner_role": "QA",
            "priority": "Medium",
            "labels": f"capa,{defect_id.lower()},validation-experiment,metrics",
        },
    ]

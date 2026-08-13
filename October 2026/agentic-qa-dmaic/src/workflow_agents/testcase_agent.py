from __future__ import annotations

from typing import Dict, List


def generate_ado_test_cases(session: Dict[str, object], variant_set: str = "standard") -> List[Dict[str, str]]:
    defect = session.get("defect", {}) if isinstance(session, dict) else {}
    if not isinstance(defect, dict):
        defect = {}

    defect_id = str(defect.get("defect_id", "UNKNOWN-DEFECT")).strip() or "UNKNOWN-DEFECT"
    component = str(defect.get("component", "TargetComponent")).strip() or "TargetComponent"
    summary = str(defect.get("summary", "Recurring defect")).strip() or "Recurring defect"
    expected_behavior = str(defect.get("expected_behavior", "Expected behavior not provided")).strip()
    observed_behavior = str(defect.get("observed_behavior", "Observed behavior not provided")).strip()
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

    evidence_line = ", ".join(evidence_refs) if evidence_refs else "No evidence refs recorded"
    system_info = (
        f"Defect ID: {defect_id}. Component: {component}. "
        f"Observed: {observed_behavior}. Expected: {expected_behavior}."
    )
    base_description = (
        f"Generated from RCA session {session.get('session_id', '')}. "
        f"Summary: {summary}. Root cause: {root_cause or 'RCA root cause pending confirmation'}. "
        f"Evidence: {evidence_line}."
    )

    base_cases = [
        {
            "title": f"{defect_id} - Idempotency replay guard blocks duplicates",
            "description": base_description,
            "repro_steps": (
                "1. Configure merge pipeline with replay/idempotency guard enabled.\\n"
                "2. Execute deterministic batch input under merge key set A.\\n"
                "3. Re-execute the same batch input in the same merge window.\\n"
                "4. Query duplicate key count in target table."
            ),
            "acceptance_criteria": "Duplicate key count after rerun is 0 and pipeline run is marked successful.",
            "system_info": system_info,
        },
        {
            "title": f"{defect_id} - Persisted dedup state survives reruns",
            "description": base_description,
            "repro_steps": (
                "1. Execute first merge run and persist dedup/replay state.\\n"
                "2. Restart pipeline process/service.\\n"
                "3. Re-run the same deterministic dataset and keys.\\n"
                "4. Validate dedup state is reused and duplicate inserts are rejected."
            ),
            "acceptance_criteria": "Persisted dedup state is read on rerun and prevents duplicate inserts across process restarts.",
            "system_info": system_info,
        },
        {
            "title": f"{defect_id} - CI rerun gate fails on duplicate count greater than zero",
            "description": base_description,
            "repro_steps": (
                "1. Trigger CI job that runs deterministic dataset twice under same merge keys.\\n"
                "2. Capture duplicate count SQL output artifact from gate.\\n"
                "3. Simulate a failing condition with duplicates greater than zero.\\n"
                "4. Verify gate marks build as failed and blocks release."
            ),
            "acceptance_criteria": "Build is blocked when duplicate count is greater than 0; passes only when duplicate count equals 0.",
            "system_info": system_info,
        },
        {
            "title": f"{defect_id} - Release checklist enforces idempotency sign-off",
            "description": base_description,
            "repro_steps": (
                "1. Open release checklist for target deployment candidate.\\n"
                "2. Locate idempotency verification and evidence attachment fields.\\n"
                "3. Attempt release without completing idempotency sign-off.\\n"
                "4. Complete sign-off and reattempt release approval."
            ),
            "acceptance_criteria": "Release cannot be approved without idempotency sign-off and linked evidence artifacts.",
            "system_info": system_info,
        },
        {
            "title": f"{defect_id} - CAPA validation experiment confirms recurrence prevention",
            "description": base_description,
            "repro_steps": (
                "1. Execute at least five repeated-run pairs using deterministic input.\\n"
                "2. Record duplicate_key_count_after_rerun for each pair.\\n"
                "3. Compare baseline and post-control metrics.\\n"
                "4. Confirm no adjacent regression signals in related pipeline checks."
            ),
            "acceptance_criteria": (
                "All validation runs show duplicate_key_count_after_rerun = 0 and no Sev1/Sev2 regressions are introduced."
            ),
            "system_info": system_info,
        },
    ]

    if variant_set != "expanded":
        return base_cases

    expanded_cases: List[Dict[str, str]] = []
    for base in base_cases:
        expanded_cases.append(base)

        expanded_cases.append(
            {
                "title": f"{base['title']} - Negative",
                "description": (
                    f"Negative variant. {base['description']} Validate that missing/invalid control inputs or failed preconditions "
                    "are rejected safely and surfaced with actionable diagnostics."
                ),
                "repro_steps": (
                    f"{base['repro_steps']}\\n"
                    "5. Intentionally disable or misconfigure the target control for this scenario.\\n"
                    "6. Re-run validation and capture failure handling behavior."
                ),
                "acceptance_criteria": (
                    "System blocks unsafe progression, emits clear diagnostics, and does not allow silent pass on invalid conditions."
                ),
                "system_info": f"{base['system_info']} Negative variant coverage.",
            }
        )

        expanded_cases.append(
            {
                "title": f"{base['title']} - Boundary",
                "description": (
                    f"Boundary variant. {base['description']} Validate behavior at threshold conditions for run volume, "
                    "timing window, and duplicate count limits."
                ),
                "repro_steps": (
                    f"{base['repro_steps']}\\n"
                    "5. Execute at lower boundary (minimum valid records / single replay cycle).\\n"
                    "6. Execute at upper boundary (maximum planned batch volume / edge replay window)."
                ),
                "acceptance_criteria": (
                    "Control behavior remains deterministic and policy-compliant at both lower and upper boundary conditions."
                ),
                "system_info": f"{base['system_info']} Boundary variant coverage.",
            }
        )

    return expanded_cases

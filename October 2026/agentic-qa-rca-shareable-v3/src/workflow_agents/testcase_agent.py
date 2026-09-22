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
        {"title": f"{defect_id} - Corrective control resolves the observed defect", "description": base_description, "repro_steps": f"1. Prepare the synthetic conditions for: {summary}.\\n2. Execute the workflow before applying the corrective control.\\n3. Apply the corrective control linked to the confirmed root cause.\\n4. Execute the same deterministic scenario again.", "acceptance_criteria": f"The observed behavior is no longer present and the expected behavior is met: {expected_behavior}.", "system_info": system_info},
        {"title": f"{defect_id} - Regression gate detects recurrence", "description": base_description, "repro_steps": "1. Run the deterministic regression scenario with the corrective control enabled.\\n2. Capture the result and supporting evidence artifact.\\n3. Repeat the scenario under the relevant boundary or recurrence condition.\\n4. Verify the gate reports a clear pass or failure.", "acceptance_criteria": "The regression gate passes only when the expected behavior is observed and emits actionable diagnostics otherwise.", "system_info": system_info},
        {"title": f"{defect_id} - Corrective action validation shows no regression", "description": base_description, "repro_steps": "1. Execute the agreed before/after validation sample.\\n2. Compare defect recurrence and adjacent quality metrics.\\n3. Record the sample size, results, and evidence references.\\n4. Confirm the validation outcome and any follow-up action.", "acceptance_criteria": "The defect does not recur in the validation sample and no related regression is introduced.", "system_info": system_info},
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

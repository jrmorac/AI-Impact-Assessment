from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from interactive_rca import answer_session, export_session_report, load_session_status, revise_current_answer, start_session
from io_utils import load_json, load_yaml, write_json
from orchestrator import run_capa_agent, run_testcase_agent, run_triage_agents


ROLE_RESPONSE_TEMPLATES: Dict[str, str] = {
    "dev": (
        "Focus on implementation mechanics. Use: Because <specific control/code path> failed or was missing, "
        "<observable effect> occurred under <trigger condition>."
    ),
    "qa": (
        "Focus on test and gate coverage. Use: Because <specific validation/gate> was absent or weak, "
        "<defect behavior> escaped to <stage>."
    ),
    "sre": (
        "Focus on operability and safeguards. Use: Because <monitoring/alert/runbook control> did not detect or block "
        "<failure pattern>, recurrence continued under <operational condition>."
    ),
    "release-manager": (
        "Focus on governance and release criteria. Use: Because <ownership/approval criterion> did not require "
        "<preventive control>, risk was accepted implicitly and propagated to release."
    ),
}


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    argv = list(sys.argv[1:] if argv is None else argv)

    if argv and argv[0] in {
        "start-rca",
        "answer-rca",
        "revise-rca",
        "status-rca",
        "export-rca-report",
        "guided-rca",
        "export-capa-csv",
        "export-ado-testcases-csv",
    }:
        parser = argparse.ArgumentParser(description="Agentic QA DMAIC Assistant")
        subparsers = parser.add_subparsers(dest="command", required=True)

        start_parser = subparsers.add_parser("start-rca", help="Start an interactive RCA session")
        start_parser.add_argument("--context", required=True, help="Path to project context YAML")
        start_parser.add_argument("--input", required=True, help="Path to defect input JSON")
        start_parser.add_argument("--defect-id", required=True, help="Defect ID to investigate")
        start_parser.add_argument("--session", required=True, help="Path to RCA session JSON file")

        answer_parser = subparsers.add_parser("answer-rca", help="Answer the current Why in an RCA session")
        answer_parser.add_argument("--session", required=True, help="Path to RCA session JSON file")
        answer_parser.add_argument("--answer", required=True, help="Answer to the current Why question")
        answer_parser.add_argument(
            "--evidence-ref",
            action="append",
            default=[],
            help="Evidence reference for this answer. Repeat this flag for multiple items.",
        )
        answer_parser.add_argument("--resolved", action="store_true", help="Mark this cause as resolving the problem")
        answer_parser.add_argument("--controllable", action="store_true", help="Mark this cause as controllable by the team")
        answer_parser.add_argument(
            "--prevents-recurrence",
            action="store_true",
            help="Mark this cause as preventing recurrence if fixed",
        )

        revise_parser = subparsers.add_parser("revise-rca", help="Revise the current Why answer in an RCA session")
        revise_parser.add_argument("--session", required=True, help="Path to RCA session JSON file")
        revise_parser.add_argument("--answer", required=True, help="Revised answer to the current Why question")
        revise_parser.add_argument(
            "--evidence-ref",
            action="append",
            default=[],
            help="Evidence reference for this revised answer. Repeat this flag for multiple items.",
        )
        revise_parser.add_argument("--resolved", action="store_true", help="Mark this cause as resolving the problem")
        revise_parser.add_argument("--controllable", action="store_true", help="Mark this cause as controllable by the team")
        revise_parser.add_argument(
            "--prevents-recurrence",
            action="store_true",
            help="Mark this cause as preventing recurrence if fixed",
        )

        status_parser = subparsers.add_parser("status-rca", help="Show current RCA session status")
        status_parser.add_argument("--session", required=True, help="Path to RCA session JSON file")

        export_parser = subparsers.add_parser("export-rca-report", help="Export a formal RCA case report")
        export_parser.add_argument("--session", required=True, help="Path to RCA session JSON file")
        export_parser.add_argument("--output", required=True, help="Path to markdown RCA report")

        guided_parser = subparsers.add_parser(
            "guided-rca",
            help="Run an interactive guided RCA workflow with evidence suggestions and automatic report export",
        )
        guided_parser.add_argument("--context", required=True, help="Path to project context YAML")
        guided_parser.add_argument("--input", required=True, help="Path to defect input JSON")
        guided_parser.add_argument("--defect-id", required=True, help="Defect ID to investigate")
        guided_parser.add_argument(
            "--session",
            help="Optional path to RCA session JSON file. If omitted, a timestamped path is generated.",
        )
        guided_parser.add_argument(
            "--role",
            choices=["dev", "qa", "sre", "release-manager"],
            default="qa",
            help="Role-based answer guidance template shown at each Why step.",
        )
        guided_parser.add_argument(
            "--output-report",
            help="Optional path to markdown RCA report. If omitted, a default evidence/rca_reports/<session>.md path is used.",
        )
        guided_parser.add_argument(
            "--quick-plan",
            help=(
                "Optional JSON file for non-interactive execution. "
                "Plan format: {\"answers\": [{\"answer\": str, \"evidence_refs\": [str], "
                "\"controllable\": bool, \"resolved\": bool, \"prevents_recurrence\": bool}], "
                "\"default_evidence_refs\": [str], \"default_flags\": {...}}"
            ),
        )

        capa_parser = subparsers.add_parser(
            "export-capa-csv",
            help="Export CAPA tasks from an RCA session to CSV for ADO, Jira, or generic import",
        )
        capa_parser.add_argument("--session", required=True, help="Path to RCA session JSON file")
        capa_parser.add_argument("--output", required=True, help="Path to output CSV file")
        capa_parser.add_argument(
            "--provider",
            choices=["ado", "jira", "generic"],
            default="ado",
            help="Target CSV schema provider. Default is ado.",
        )
        capa_parser.add_argument(
            "--assignee",
            default="",
            help="Optional default assignee value applied to exported tasks.",
        )
        capa_parser.add_argument(
            "--due-date",
            default="",
            help="Optional due date applied to exported tasks (YYYY-MM-DD).",
        )

        ado_tc_parser = subparsers.add_parser(
            "export-ado-testcases-csv",
            help="Export ADO-compatible Test Case CSV from RCA session CAPA and root-cause findings",
        )
        ado_tc_parser.add_argument("--session", required=True, help="Path to RCA session JSON file")
        ado_tc_parser.add_argument("--output", required=True, help="Path to output CSV file")
        ado_tc_parser.add_argument("--assigned-to", default="", help="Optional default Assigned To value")
        ado_tc_parser.add_argument("--area-path", default="", help="Optional ADO Area Path value")
        ado_tc_parser.add_argument("--iteration-path", default="", help="Optional ADO Iteration Path value")
        ado_tc_parser.add_argument("--state", default="Design", help="ADO State value. Default is Design")
        ado_tc_parser.add_argument(
            "--variant-set",
            choices=["standard", "expanded"],
            default="standard",
            help="Use expanded to include negative and boundary variants for each CAPA test case.",
        )

        return parser.parse_args(argv)

    parser = argparse.ArgumentParser(description="Agentic QA DMAIC Assistant")
    parser.add_argument("--context", required=True, help="Path to project context YAML")
    parser.add_argument("--input", required=True, help="Path to synthetic defects JSON")
    parser.add_argument("--output", required=True, help="Path to output report JSON")
    parser.add_argument(
        "--evidence-log",
        default="evidence/evidence_log.csv",
        help="Path to evidence CSV log",
    )
    args = parser.parse_args(argv)
    args.command = "batch"
    return args


def _resolve_quality_gate_path(context_path: Path, context: Dict[str, Any]) -> Path:
    gate_file = context.get("quality_gates_file", "quality-gates.template.yaml")
    return context_path.parent / gate_file


def _load_context_bundle(context_path: Path) -> tuple[Dict[str, Any], Dict[str, Any]]:
    context = load_yaml(context_path)
    quality_gates = load_yaml(_resolve_quality_gate_path(context_path, context)).get("quality_gates", {})
    return context, quality_gates


def _append_evidence_row(
    evidence_log_path: Path,
    project_name: str,
    input_file: str,
    output_file: str,
    total: int,
    accepted: int,
    flagged: int,
) -> None:
    evidence_log_path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not evidence_log_path.exists()

    with evidence_log_path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(
                [
                    "timestamp_utc",
                    "project_name",
                    "input_file",
                    "output_file",
                    "defects_total",
                    "accepted_count",
                    "flagged_count",
                ]
            )
        writer.writerow(
            [
                datetime.now(timezone.utc).isoformat(),
                project_name,
                input_file,
                output_file,
                total,
                accepted,
                flagged,
            ]
        )


def _slugify(value: str) -> str:
    lowered = value.strip().lower().replace(" ", "-")
    allowed = [ch for ch in lowered if ch.isalnum() or ch in {"-", "_"}]
    slug = "".join(allowed).strip("-")
    return slug or "rca-session"


def _default_session_path(defect_id: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return Path("evidence/rca_sessions") / f"{_slugify(defect_id)}-{stamp}.json"


def _default_report_path(session_path: Path) -> Path:
    return Path("evidence/rca_reports") / f"{session_path.stem}.md"


def _prompt_yes_no(prompt: str, default: bool = False) -> bool:
    default_hint = "Y/n" if default else "y/N"
    while True:
        raw = input(f"{prompt} [{default_hint}]: ").strip().lower()
        if not raw:
            return default
        if raw in {"y", "yes"}:
            return True
        if raw in {"n", "no"}:
            return False
        print("Please answer with y or n.")


def _discover_evidence_refs(project_root: Path, session: Dict[str, Any], limit: int = 12) -> List[str]:
    defect = session.get("defect", {}) if isinstance(session, dict) else {}
    defect_id = str(defect.get("defect_id", "")).strip().lower()
    seeded: List[str] = []
    for artifact in defect.get("evidence_artifacts", []) if isinstance(defect, dict) else []:
        item = str(artifact).strip()
        if item and item not in seeded:
            seeded.append(item)

    discovered: List[str] = []
    for folder in [project_root / "evidence", project_root / "data"]:
        if not folder.exists():
            continue
        for path in folder.rglob("*"):
            if not path.is_file():
                continue
            if defect_id and defect_id not in path.name.lower():
                continue
            rel = path.relative_to(project_root).as_posix()
            if rel not in discovered:
                discovered.append(rel)

    ordered: List[str] = []
    for item in seeded + sorted(discovered):
        if item not in ordered:
            ordered.append(item)
    return ordered[:limit]


def _collect_evidence_refs(suggestions: List[str]) -> List[str]:
    if suggestions:
        print("Suggested evidence references:")
        for idx, item in enumerate(suggestions, start=1):
            print(f"  {idx}. {item}")
    else:
        print("No evidence suggestions found. Enter custom references.")

    raw = input("Evidence refs (comma-separated numbers and/or custom values, Enter for defaults): ").strip()
    if not raw:
        return suggestions[:2]

    selected: List[str] = []
    for token in [part.strip() for part in raw.split(",") if part.strip()]:
        if token.isdigit():
            position = int(token)
            if 1 <= position <= len(suggestions):
                item = suggestions[position - 1]
                if item not in selected:
                    selected.append(item)
            continue
        if token not in selected:
            selected.append(token)
    return selected


def _load_quick_plan(plan_path: Path) -> Dict[str, Any]:
    payload = load_json(plan_path)
    if not isinstance(payload, dict):
        raise ValueError("Quick plan must be a JSON object.")
    answers = payload.get("answers", [])
    if not isinstance(answers, list) or not answers:
        raise ValueError("Quick plan must include a non-empty 'answers' list.")
    for idx, item in enumerate(answers, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Quick plan answer at index {idx} must be an object.")
        answer_text = str(item.get("answer", "")).strip()
        if not answer_text:
            raise ValueError(f"Quick plan answer at index {idx} is missing 'answer' text.")
        refs = item.get("evidence_refs", [])
        if refs is not None and not isinstance(refs, list):
            raise ValueError(f"Quick plan answer at index {idx} has invalid 'evidence_refs' (must be list).")
    return payload


def _next_quick_step(
    plan: Dict[str, Any],
    step_index: int,
    suggested_refs: List[str],
) -> Dict[str, Any]:
    answers = plan.get("answers", [])
    if step_index >= len(answers):
        raise ValueError(
            "Quick plan ran out of answers before RCA session closed. "
            "Add more 'answers' entries or mark closure flags on the final entry."
        )

    step = answers[step_index]
    default_flags = plan.get("default_flags", {})
    if not isinstance(default_flags, dict):
        default_flags = {}

    answer_text = str(step.get("answer", "")).strip()
    evidence_refs = step.get("evidence_refs", [])
    if not evidence_refs:
        plan_default_refs = plan.get("default_evidence_refs", [])
        if isinstance(plan_default_refs, list) and plan_default_refs:
            evidence_refs = [str(item).strip() for item in plan_default_refs if str(item).strip()]
        else:
            evidence_refs = suggested_refs[:2]

    resolved = bool(step.get("resolved", default_flags.get("resolved", False)))
    controllable = bool(step.get("controllable", default_flags.get("controllable", True)))
    prevents_recurrence = bool(step.get("prevents_recurrence", default_flags.get("prevents_recurrence", False)))

    return {
        "answer": answer_text,
        "evidence_refs": [str(item).strip() for item in evidence_refs if str(item).strip()],
        "resolved": resolved,
        "controllable": controllable,
        "prevents_recurrence": prevents_recurrence,
    }


def _derive_capa_tasks(session: Dict[str, Any]) -> List[Dict[str, str]]:
    defect = session.get("defect", {}) if isinstance(session, dict) else {}
    defect_id = str(defect.get("defect_id", "UNKNOWN-DEFECT")).strip() or "UNKNOWN-DEFECT"
    component = str(defect.get("component", "TargetComponent")).strip() or "TargetComponent"
    summary = str(defect.get("summary", "Recurring defect")).strip() or "Recurring defect"
    root_cause = str(session.get("root_cause_summary", "")).strip().rstrip(". ")
    root_cause = root_cause.rstrip(". ")

    evidence_refs: List[str] = []
    why_chain = session.get("why_chain", [])
    if isinstance(why_chain, list):
        for node in why_chain:
            for item in node.get("evidence_refs", []) if isinstance(node, dict) else []:
                ref = str(item).strip()
                if ref and ref not in evidence_refs:
                    evidence_refs.append(ref)
    evidence_line = ", ".join(evidence_refs) if evidence_refs else "No explicit evidence refs in session"

    tasks: List[Dict[str, str]] = [
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
    return tasks


def export_capa_csv(
    *,
    session_path: Path,
    output_path: Path,
    provider: str,
    assignee: str,
    due_date: str,
) -> Path:
    session = load_json(session_path)
    if not isinstance(session, dict):
        raise ValueError("Session file is invalid.")

    tasks, _trace = run_capa_agent(session)
    defect_id = str(session.get("defect", {}).get("defect_id", "UNKNOWN-DEFECT"))
    session_id = str(session.get("session_id", session_path.stem))

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if provider == "ado":
        headers = ["Work Item Type", "Title", "State", "Assigned To", "Description", "Tags", "Due Date"]
        rows = [
            {
                "Work Item Type": "Task",
                "Title": task["title"],
                "State": "New",
                "Assigned To": assignee,
                "Description": f"{task['description']} Session: {session_id}. Defect: {defect_id}.",
                "Tags": task["labels"],
                "Due Date": due_date,
            }
            for task in tasks
        ]
    elif provider == "jira":
        headers = ["Summary", "Issue Type", "Priority", "Assignee", "Description", "Labels", "Due Date"]
        rows = [
            {
                "Summary": task["title"],
                "Issue Type": "Task",
                "Priority": task["priority"],
                "Assignee": assignee,
                "Description": f"{task['description']} Session: {session_id}. Defect: {defect_id}.",
                "Labels": task["labels"],
                "Due Date": due_date,
            }
            for task in tasks
        ]
    else:
        headers = [
            "task_title",
            "task_description",
            "owner_role",
            "priority",
            "assignee",
            "due_date",
            "status",
            "labels",
            "source_session",
            "source_defect_id",
        ]
        rows = [
            {
                "task_title": task["title"],
                "task_description": task["description"],
                "owner_role": task["owner_role"],
                "priority": task["priority"],
                "assignee": assignee,
                "due_date": due_date,
                "status": "planned",
                "labels": task["labels"],
                "source_session": session_id,
                "source_defect_id": defect_id,
            }
            for task in tasks
        ]

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    return output_path


def _derive_ado_test_cases(session: Dict[str, Any], variant_set: str = "standard") -> List[Dict[str, str]]:
    defect = session.get("defect", {}) if isinstance(session, dict) else {}
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
            for item in node.get("evidence_refs", []) if isinstance(node, dict) else []:
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


def export_ado_testcases_csv(
    *,
    session_path: Path,
    output_path: Path,
    assigned_to: str,
    area_path: str,
    iteration_path: str,
    state: str,
    variant_set: str,
) -> Path:
    session = load_json(session_path)
    if not isinstance(session, dict):
        raise ValueError("Session file is invalid.")

    test_cases, _trace = run_testcase_agent(session, variant_set=variant_set)
    headers = [
        "ID",
        "Work Item Type",
        "Title",
        "Assigned To",
        "State",
        "Area Path",
        "Iteration Path",
        "Description",
        "Repro Steps",
        "System Info",
        "Acceptance Criteria",
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for case in test_cases:
            writer.writerow(
                {
                    "ID": "",
                    "Work Item Type": "Test Case",
                    "Title": case["title"],
                    "Assigned To": assigned_to,
                    "State": state,
                    "Area Path": area_path,
                    "Iteration Path": iteration_path,
                    "Description": case["description"],
                    "Repro Steps": case["repro_steps"],
                    "System Info": case["system_info"],
                    "Acceptance Criteria": case["acceptance_criteria"],
                }
            )

    return output_path


def run_guided_rca(
    *,
    context_path: Path,
    input_path: Path,
    defect_id: str,
    session_path: Path,
    role: str,
    output_report_path: Path,
    quick_plan: Dict[str, Any] | None = None,
) -> Dict[str, str]:
    context, quality_gates = _load_context_bundle(context_path)
    project_root = context_path.parent.parent

    session = start_session(
        context=context,
        quality_gates=quality_gates,
        input_path=input_path,
        defect_id=defect_id,
        session_path=session_path,
    )

    print("\nGuided RCA session started.")
    print(f"Session file: {session_path.as_posix()}")
    print(f"Role template ({role}): {ROLE_RESPONSE_TEMPLATES[role]}")
    if quick_plan is not None:
        print("Execution mode: quick-plan (non-interactive)")
    else:
        print("Execution mode: interactive")

    quick_step_index = 0
    while str(session.get("status", "")) not in {"root_cause_confirmed", "max_depth_reached"}:
        why_index = session.get("current_why_index", "?")
        print("\n" + "=" * 80)
        print(f"Why {why_index}")
        print(str(session.get("current_question", "")).strip())
        print(f"Template hint: {ROLE_RESPONSE_TEMPLATES[role]}")

        suggestions = _discover_evidence_refs(project_root=project_root, session=session)
        if quick_plan is None:
            evidence_refs = _collect_evidence_refs(suggestions)

            answer = ""
            while not answer.strip():
                answer = input("Answer: ").strip()
                if not answer:
                    print("Answer cannot be empty.")

            controllable = _prompt_yes_no("Is this cause controllable by the team", default=True)
            resolved = _prompt_yes_no("Would resolving this cause fix the current problem", default=False)
            prevents_recurrence = _prompt_yes_no("Would this fix prevent recurrence of this defect class", default=False)
        else:
            quick_step = _next_quick_step(quick_plan, quick_step_index, suggestions)
            quick_step_index += 1
            answer = quick_step["answer"]
            evidence_refs = quick_step["evidence_refs"]
            controllable = bool(quick_step["controllable"])
            resolved = bool(quick_step["resolved"])
            prevents_recurrence = bool(quick_step["prevents_recurrence"])
            print("Quick answer loaded from plan.")
            print(f"Evidence refs used: {', '.join(evidence_refs) if evidence_refs else 'None'}")
            print(
                "Flags: "
                f"controllable={controllable}, "
                f"resolved={resolved}, "
                f"prevents_recurrence={prevents_recurrence}"
            )

        current_status = str(session.get("status", ""))
        if current_status == "needs_more_evidence":
            session = revise_current_answer(
                session_path=session_path,
                answer=answer,
                evidence_refs=evidence_refs,
                resolved=resolved,
                controllable=controllable,
                prevents_recurrence=prevents_recurrence,
            )
        else:
            session = answer_session(
                session_path=session_path,
                answer=answer,
                evidence_refs=evidence_refs,
                resolved=resolved,
                controllable=controllable,
                prevents_recurrence=prevents_recurrence,
            )

        status = str(session.get("status", ""))
        why_chain = session.get("why_chain", [])
        decision = ""
        requests: List[str] = []
        if isinstance(why_chain, list) and why_chain:
            checkpoint = why_chain[-1].get("checkpoint", {})
            if isinstance(checkpoint, dict):
                decision = str(checkpoint.get("decision", ""))
                requests = checkpoint.get("recommended_data_requests", []) or []

        print(f"Decision: {decision or 'n/a'}")
        print(f"Session status: {status}")
        if requests:
            print("Recommended follow-up data:")
            for item in requests:
                print(f"- {item}")

    report_path = export_session_report(session_path=session_path, output_path=output_report_path)
    print("\nGuided RCA completed.")
    print(f"Final status: {session.get('status', '')}")
    print(f"Report path: {report_path.as_posix()}")

    return {
        "session_path": session_path.as_posix(),
        "report_path": report_path.as_posix(),
        "status": str(session.get("status", "")),
    }


def run(context_path: Path, input_path: Path, output_path: Path, evidence_log_path: Path) -> None:
    context, quality_gates = _load_context_bundle(context_path)

    agentic_cfg = context.get("agentic", {})
    min_confidence = float(agentic_cfg.get("min_confidence_to_autosuggest", 0.70))
    confidence_calibration = agentic_cfg.get("confidence_calibration", {})
    prioritization_weights = agentic_cfg.get("prioritization_weights", {})
    priority_tiers = agentic_cfg.get("priority_tiers", {})
    rca_cfg = agentic_cfg.get("rca", {})
    min_hypothesis_support = float(rca_cfg.get("min_hypothesis_support", 0.65))
    require_evidence_artifact_for_capa = bool(rca_cfg.get("require_evidence_artifact_for_capa", True))
    min_artifact_quality_score = float(rca_cfg.get("min_artifact_quality_score", 0.60))
    require_artifact_traceability = bool(rca_cfg.get("require_artifact_traceability", True))
    require_capa_validation_experiment = bool(rca_cfg.get("require_capa_validation_experiment", True))
    outcome_evaluation_policy = rca_cfg.get("outcome_evaluation", {})

    severity_model = context.get("severity_model", {})
    known_categories = context.get("defect_taxonomy", [])
    required_fields: List[str] = quality_gates.get("required_fields", [])

    defects = load_json(input_path)
    if not isinstance(defects, list):
        raise ValueError("Input JSON must be a list of defect objects")

    analyzed = []
    accepted_count = 0

    for defect in defects:
        if not isinstance(defect, dict):
            continue
        missing_fields, agent_result, validation, agent_trace = run_triage_agents(
            defect=defect,
            required_fields=required_fields,
            severity_model=severity_model,
            known_categories=known_categories,
            confidence_calibration=confidence_calibration,
            prioritization_weights=prioritization_weights,
            priority_tiers=priority_tiers,
            min_hypothesis_support=min_hypothesis_support,
            require_evidence_artifact_for_capa=require_evidence_artifact_for_capa,
            min_artifact_quality_score=min_artifact_quality_score,
            require_artifact_traceability=require_artifact_traceability,
            require_capa_validation_experiment=require_capa_validation_experiment,
            outcome_evaluation_policy=outcome_evaluation_policy,
            min_confidence=min_confidence,
        )
        if validation["accepted"]:
            accepted_count += 1

        analyzed.append(
            {
                "defect_id": agent_result.defect_id,
                "category": agent_result.category,
                "root_cause_hypothesis": agent_result.root_cause_hypothesis,
                "hypothesis_support_score": agent_result.hypothesis_support_score,
                "assumptions": agent_result.assumptions,
                "rca_5whys": agent_result.rca_5whys,
                "action_mode": agent_result.action_mode,
                "capa_actions": agent_result.capa_actions,
                "investigation_actions": agent_result.investigation_actions,
                "artifact_quality_score": agent_result.artifact_quality_score,
                "artifact_quality_breakdown": agent_result.artifact_quality_breakdown,
                "artifact_traceability_pass": agent_result.artifact_traceability_pass,
                "capa_validation_experiment": agent_result.capa_validation_experiment,
                "capa_effectiveness": agent_result.capa_effectiveness,
                "confidence": agent_result.confidence,
                "confidence_breakdown": agent_result.confidence_breakdown,
                "risk_score": agent_result.risk_score,
                "priority_score": agent_result.priority_score,
                "priority_tier": agent_result.priority_tier,
                "repeat_signal": agent_result.repeat_signal,
                "validation": validation,
                "agent_trace": agent_trace,
            }
        )

    analyzed.sort(key=lambda item: item.get("priority_score", 0), reverse=True)

    total = len(analyzed)
    flagged_count = total - accepted_count
    high_priority_count = sum(1 for item in analyzed if item.get("priority_tier") == "high")
    medium_priority_count = sum(1 for item in analyzed if item.get("priority_tier") == "medium")
    low_priority_count = sum(1 for item in analyzed if item.get("priority_tier") == "low")
    confirmed_capa_count = sum(1 for item in analyzed if item.get("action_mode") == "confirmed_capa")
    investigate_first_count = sum(1 for item in analyzed if item.get("action_mode") == "investigate_first")
    traceability_pass_count = sum(1 for item in analyzed if item.get("artifact_traceability_pass"))
    capa_experiment_count = sum(1 for item in analyzed if item.get("capa_validation_experiment"))
    effective_count = sum(1 for item in analyzed if item.get("capa_effectiveness", {}).get("status") == "effective")
    partial_count = sum(1 for item in analyzed if item.get("capa_effectiveness", {}).get("status") == "partial")
    ineffective_count = sum(1 for item in analyzed if item.get("capa_effectiveness", {}).get("status") == "ineffective")
    not_available_count = sum(1 for item in analyzed if item.get("capa_effectiveness", {}).get("status") == "not_available")
    invalid_data_count = sum(1 for item in analyzed if item.get("capa_effectiveness", {}).get("status") == "invalid_data")

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": context.get("project", {}),
        "input_file": str(input_path),
        "summary": {
            "defects_total": total,
            "accepted_count": accepted_count,
            "flagged_count": flagged_count,
            "acceptance_rate": round((accepted_count / total), 3) if total else 0.0,
            "priority_breakdown": {
                "high": high_priority_count,
                "medium": medium_priority_count,
                "low": low_priority_count,
            },
            "action_mode_breakdown": {
                "confirmed_capa": confirmed_capa_count,
                "investigate_first": investigate_first_count,
            },
            "artifact_traceability_pass_count": traceability_pass_count,
            "capa_validation_experiment_count": capa_experiment_count,
            "capa_effectiveness_breakdown": {
                "effective": effective_count,
                "partial": partial_count,
                "ineffective": ineffective_count,
                "not_available": not_available_count,
                "invalid_data": invalid_data_count,
            },
        },
        "analysis": analyzed,
    }

    write_json(output_path, report)

    project_name = context.get("project", {}).get("project_name", "UnknownProject")
    _append_evidence_row(
        evidence_log_path=evidence_log_path,
        project_name=project_name,
        input_file=str(input_path),
        output_file=str(output_path),
        total=total,
        accepted=accepted_count,
        flagged=flagged_count,
    )


def main() -> None:
    args = parse_args()
    if args.command == "batch":
        run(
            context_path=Path(args.context),
            input_path=Path(args.input),
            output_path=Path(args.output),
            evidence_log_path=Path(args.evidence_log),
        )
        return

    if args.command == "start-rca":
        context, quality_gates = _load_context_bundle(Path(args.context))
        session = start_session(
            context=context,
            quality_gates=quality_gates,
            input_path=Path(args.input),
            defect_id=args.defect_id,
            session_path=Path(args.session),
        )
        print(json.dumps(session, indent=2))
        return

    if args.command == "answer-rca":
        session = answer_session(
            session_path=Path(args.session),
            answer=args.answer,
            evidence_refs=args.evidence_ref,
            resolved=bool(args.resolved),
            controllable=bool(args.controllable),
            prevents_recurrence=bool(args.prevents_recurrence),
        )
        print(json.dumps(session, indent=2))
        return

    if args.command == "revise-rca":
        session = revise_current_answer(
            session_path=Path(args.session),
            answer=args.answer,
            evidence_refs=args.evidence_ref,
            resolved=bool(args.resolved),
            controllable=bool(args.controllable),
            prevents_recurrence=bool(args.prevents_recurrence),
        )
        print(json.dumps(session, indent=2))
        return

    if args.command == "status-rca":
        session = load_session_status(Path(args.session))
        print(json.dumps(session, indent=2))
        return

    if args.command == "export-rca-report":
        output_path = export_session_report(session_path=Path(args.session), output_path=Path(args.output))
        print(json.dumps({"report_path": str(output_path)}, indent=2))
        return

    if args.command == "guided-rca":
        session_path = Path(args.session) if args.session else _default_session_path(args.defect_id)
        output_report_path = Path(args.output_report) if args.output_report else _default_report_path(session_path)
        quick_plan = _load_quick_plan(Path(args.quick_plan)) if args.quick_plan else None
        result = run_guided_rca(
            context_path=Path(args.context),
            input_path=Path(args.input),
            defect_id=args.defect_id,
            session_path=session_path,
            role=args.role,
            output_report_path=output_report_path,
            quick_plan=quick_plan,
        )
        print(json.dumps(result, indent=2))
        return

    if args.command == "export-capa-csv":
        csv_path = export_capa_csv(
            session_path=Path(args.session),
            output_path=Path(args.output),
            provider=str(args.provider),
            assignee=str(args.assignee),
            due_date=str(args.due_date),
        )
        print(json.dumps({"csv_path": str(csv_path), "provider": str(args.provider)}, indent=2))
        return

    if args.command == "export-ado-testcases-csv":
        csv_path = export_ado_testcases_csv(
            session_path=Path(args.session),
            output_path=Path(args.output),
            assigned_to=str(args.assigned_to),
            area_path=str(args.area_path),
            iteration_path=str(args.iteration_path),
            state=str(args.state),
            variant_set=str(args.variant_set),
        )
        print(json.dumps({"csv_path": str(csv_path), "schema": "ado-testcase", "variant_set": str(args.variant_set)}, indent=2))
        return


if __name__ == "__main__":
    main()

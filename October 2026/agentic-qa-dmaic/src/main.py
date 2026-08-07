from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from agents import analyzer_agent, planner_agent, validator_agent
from interactive_rca import answer_session, export_session_report, load_session_status, revise_current_answer, start_session
from io_utils import load_json, load_yaml, write_json


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    argv = list(sys.argv[1:] if argv is None else argv)

    if argv and argv[0] in {"start-rca", "answer-rca", "revise-rca", "status-rca", "export-rca-report"}:
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
        missing_fields = planner_agent(defect, required_fields)
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
        validation = validator_agent(
            agent_result,
            missing_fields,
            min_confidence,
            min_hypothesis_support,
            min_artifact_quality_score,
            require_artifact_traceability,
            require_capa_validation_experiment,
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


if __name__ == "__main__":
    main()

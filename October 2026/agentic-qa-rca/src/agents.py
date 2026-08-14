from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class AgentResult:
    defect_id: str
    root_cause_hypothesis: str
    hypothesis_support_score: float
    assumptions: List[str]
    category: str
    rca_5whys: List[Dict[str, object]]
    action_mode: str
    capa_actions: List[str]
    investigation_actions: List[str]
    artifact_quality_score: float
    artifact_quality_breakdown: Dict[str, float]
    artifact_traceability_pass: bool
    capa_validation_experiment: Dict[str, object]
    capa_effectiveness: Dict[str, object]
    confidence: float
    confidence_breakdown: Dict[str, float]
    risk_score: int
    priority_score: int
    priority_tier: str
    repeat_signal: bool
    missing_fields: List[str]


def planner_agent(defect: Dict[str, str], required_fields: List[str]) -> List[str]:
    missing = [field for field in required_fields if not defect.get(field)]
    return missing


def _severity_to_risk(severity: str, severity_model: Dict[str, int]) -> int:
    weight = severity_model.get(severity.lower(), 1)
    return min(100, max(10, weight * 20))


def _infer_category(text: str, known_categories: List[str]) -> Tuple[str, float]:
    lowered = text.lower()

    rules = [
        ("timeout", "performance"),
        ("latency", "performance"),
        ("slow", "performance"),
        ("null", "data-quality"),
        ("mismatch", "business-rule"),
        ("duplicate", "data-quality"),
        ("unauthorized", "security"),
        ("token", "security"),
        ("schema", "integration"),
        ("api", "integration"),
        ("flaky", "test-automation"),
        ("assertion", "test-automation"),
    ]

    for keyword, category in rules:
        if keyword in lowered and category in known_categories:
            return category, 0.85

    default_category = known_categories[0] if known_categories else "data-quality"
    return default_category, 0.60


def _capa_by_category(category: str) -> List[str]:
    mapping = {
        "performance": [
            "Add focused performance regression test for affected component.",
            "Review query/index or service call path tied to symptom.",
            "Set alert threshold for repeated latency condition.",
        ],
        "data-quality": [
            "Add data validation test for null/duplicate edge cases.",
            "Add deterministic synthetic dataset for reproduction.",
            "Add control check in pipeline to block malformed records.",
        ],
        "business-rule": [
            "Document expected decision rule with product owner.",
            "Add boundary and negative test cases for the rule.",
            "Add assertion coverage for known exception path.",
        ],
        "integration": [
            "Add contract test for schema and field-level compatibility.",
            "Add retry/fallback behavior test for dependent API failure.",
            "Version and pin integration contract assumptions.",
        ],
        "security": [
            "Add security-focused negative test for auth and access control.",
            "Validate secret and token handling path in test environment.",
            "Add CI check for insecure patterns in changed files.",
        ],
        "test-automation": [
            "Stabilize flaky test with deterministic setup and teardown.",
            "Introduce failure triage tags for rerun analysis.",
            "Add isolated fixture to remove cross-test interference.",
        ],
    }
    return mapping.get(category, ["Add targeted regression test and monitoring control."])


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _calibrate_confidence(
    base_confidence: float,
    missing_fields: List[str],
    defect: Dict[str, str],
    calibration: Dict[str, float],
) -> Tuple[float, Dict[str, float]]:
    missing_field_penalty = float(calibration.get("missing_field_penalty", 0.08))
    short_text_penalty = float(calibration.get("short_text_penalty", 0.07))
    strong_repro_bonus = float(calibration.get("strong_repro_bonus", 0.04))

    summary = defect.get("summary", "")
    observed = defect.get("observed_behavior", "")
    text = f"{summary} {observed}".strip()
    text_len = len(text)

    penalty_missing = min(0.40, len(missing_fields) * missing_field_penalty)
    penalty_short_text = short_text_penalty if text_len < 60 else 0.0
    bonus_repro = strong_repro_bonus if defect.get("reproduction_steps") else 0.0
    bonus_expected = strong_repro_bonus if defect.get("expected_behavior") else 0.0

    calibrated = base_confidence - penalty_missing - penalty_short_text + bonus_repro + bonus_expected
    calibrated = round(_clamp(calibrated, 0.05, 0.98), 3)

    breakdown = {
        "base": round(base_confidence, 3),
        "penalty_missing_fields": round(penalty_missing, 3),
        "penalty_short_text": round(penalty_short_text, 3),
        "bonus_reproduction_steps": round(bonus_repro, 3),
        "bonus_expected_behavior": round(bonus_expected, 3),
        "final": calibrated,
    }
    return calibrated, breakdown


def _has_repeat_signal(defect: Dict[str, str]) -> bool:
    text = f"{defect.get('summary', '')} {defect.get('observed_behavior', '')}".lower()
    repeat_tokens = ["again", "recurr", "repeat", "reopen", "flaky"]
    return any(token in text for token in repeat_tokens)


def _compute_priority_score(
    risk_score: int,
    confidence: float,
    repeat_signal: bool,
    weights: Dict[str, float],
) -> int:
    risk_weight = float(weights.get("risk", 0.65))
    uncertainty_weight = float(weights.get("uncertainty", 0.25))
    repeat_weight = float(weights.get("repeat_signal", 0.10))

    # Normalize if custom weights do not sum to 1.0.
    total = risk_weight + uncertainty_weight + repeat_weight
    if total <= 0:
        risk_weight, uncertainty_weight, repeat_weight = 0.65, 0.25, 0.10
    else:
        risk_weight /= total
        uncertainty_weight /= total
        repeat_weight /= total

    uncertainty_score = 100 - int(confidence * 100)
    repeat_score = 100 if repeat_signal else 0

    score = (
        risk_weight * risk_score
        + uncertainty_weight * uncertainty_score
        + repeat_weight * repeat_score
    )
    return int(round(_clamp(score, 0, 100), 0))


def _priority_tier(score: int, tiers: Dict[str, int]) -> str:
    high_min = int(tiers.get("high_min", 75))
    medium_min = int(tiers.get("medium_min", 50))
    if score >= high_min:
        return "high"
    if score >= medium_min:
        return "medium"
    return "low"


def _five_why_templates(category: str) -> List[str]:
    category_first_why = {
        "performance": "Why did the system exceed the expected response-time threshold?",
        "data-quality": "Why did data integrity break (null/duplicate/inconsistent values)?",
        "business-rule": "Why did rule evaluation produce an incorrect decision?",
        "integration": "Why did the interface or contract fail between systems?",
        "security": "Why did the control fail to prevent unauthorized behavior?",
        "test-automation": "Why did the test process produce unstable or inconsistent results?",
    }
    first = category_first_why.get(
        category,
        "Why did the observed defect happen in the current process?",
    )
    return [
        first,
        "Why was the immediate technical condition possible?",
        "Why did prevention controls not stop this earlier?",
        "Why did detection controls not catch this before impact?",
        "Why does the process allow this pattern to recur?",
    ]


def _build_evidence_support(
    defect: Dict[str, str],
    repeat_signal: bool,
) -> Tuple[float, List[str], Dict[str, float]]:
    summary = defect.get("summary", "")
    observed = defect.get("observed_behavior", "")
    reproduction = defect.get("reproduction_steps", "")
    expected = defect.get("expected_behavior", "")

    artifacts = defect.get("evidence_artifacts", [])
    has_artifacts = isinstance(artifacts, list) and len(artifacts) > 0

    contributions = {
        "reproduction_steps": 0.20 if reproduction else 0.0,
        "observed_behavior": 0.20 if observed else 0.0,
        "expected_behavior": 0.10 if expected else 0.0,
        "component_context": 0.10 if defect.get("component") else 0.0,
        "summary_quality": 0.10 if len(summary.strip()) >= 40 else 0.0,
        "created_date": 0.05 if defect.get("created_date") else 0.0,
        "evidence_artifacts": 0.20 if has_artifacts else 0.0,
        "repeat_signal": 0.05 if repeat_signal else 0.0,
    }

    score = round(_clamp(sum(contributions.values()), 0.0, 1.0), 3)

    assumptions: List[str] = []
    if not reproduction:
        assumptions.append("Reproduction path is incomplete; root-cause chain may be unstable.")
    if not observed:
        assumptions.append("Observed behavior detail is missing; symptom signal is weak.")
    if not expected:
        assumptions.append("Expected behavior baseline is missing; gap cannot be quantified well.")
    if not has_artifacts:
        assumptions.append("No evidence artifacts linked (logs, SQL output, traces, screenshots).")

    return score, assumptions, contributions


def _build_five_whys(
    category: str,
    defect: Dict[str, str],
    assumptions: List[str],
) -> List[Dict[str, object]]:
    templates = _five_why_templates(category)
    summary = defect.get("summary", "")
    observed = defect.get("observed_behavior", "")
    component = defect.get("component", "unknown component")

    # Deterministic answers with explicit assumption markers to avoid over-claiming.
    answers = [
        f"Because the symptom in {component} matches a {category} failure pattern from the defect narrative.",
        "Because one or more technical controls (data checks, timeouts, contracts, or test fixtures) likely did not enforce constraints at execution time.",
        "Because prevention controls were either absent, weakly configured, or not applied consistently for this path.",
        "Because detection controls prioritized generic pass/fail output instead of early risk indicators for this defect type.",
        "Because the process lacks a closed-loop control that converts this failure into a mandatory regression prevention check.",
    ]

    evidence_refs = [
        "summary" if summary else "",
        "observed_behavior" if observed else "",
        "reproduction_steps" if defect.get("reproduction_steps") else "",
        "expected_behavior" if defect.get("expected_behavior") else "",
        "evidence_artifacts" if defect.get("evidence_artifacts") else "",
    ]
    evidence_refs = [ref for ref in evidence_refs if ref]

    chain: List[Dict[str, object]] = []
    for idx, (question, answer) in enumerate(zip(templates, answers), start=1):
        chain.append(
            {
                "why_index": idx,
                "question": question,
                "answer": answer,
                "evidence_refs": evidence_refs,
                "assumption_count": len(assumptions),
            }
        )
    return chain


def _investigation_actions(assumptions: List[str], category: str) -> List[str]:
    actions = [
        "Collect missing factual evidence before implementing CAPA (logs, traces, deterministic repro output).",
        "Run focused 5 Whys review with QA + Engineering and confirm each why with evidence references.",
    ]

    for item in assumptions:
        if "Reproduction" in item:
            actions.append("Define deterministic reproduction steps and capture exact run parameters.")
        if "Observed behavior" in item:
            actions.append("Capture observed behavior with measurable symptom details (counts, thresholds, timestamps).")
        if "Expected behavior" in item:
            actions.append("Document expected behavior and acceptance criteria from approved specification.")
        if "evidence artifacts" in item:
            actions.append("Attach at least one concrete evidence artifact (query output, logs, API trace, or screenshot).")

    actions.append(f"After evidence closure, regenerate CAPA recommendations for category {category}.")
    return actions


def _safe_token(text: str) -> str:
    return text.lower().replace("-", "").replace("_", "")


def _analyze_artifact_quality(defect: Dict[str, str]) -> Tuple[float, Dict[str, float], bool]:
    defect_id = str(defect.get("defect_id", "")).lower()
    created_date = str(defect.get("created_date", ""))
    date_token = created_date.replace("-", "")

    artifacts = defect.get("evidence_artifacts", [])
    if not isinstance(artifacts, list):
        artifacts = []
    cleaned_artifacts = [str(item).strip() for item in artifacts if str(item).strip()]

    if not cleaned_artifacts:
        return 0.0, {
            "artifact_presence": 0.0,
            "artifact_count": 0.0,
            "artifact_signal_diversity": 0.0,
            "artifact_traceability": 0.0,
            "artifact_date_context": 0.0,
            "final": 0.0,
        }, False

    signal_groups = {
        "log": ["log", "trace", "event"],
        "metric": ["metric", "latency", "chart", "count", "kpi"],
        "data": ["sql", "query", "csv", "dataset", "table"],
        "capture": ["screenshot", "png", "jpg", "pdf"],
    }

    matched_groups = set()
    has_traceability = False
    has_date_context = False
    normalized_defect_id = _safe_token(defect_id)

    for artifact in cleaned_artifacts:
        artifact_lower = artifact.lower()
        normalized_artifact = _safe_token(artifact_lower)

        if normalized_defect_id and normalized_defect_id in normalized_artifact:
            has_traceability = True
        if date_token and date_token in normalized_artifact:
            has_date_context = True

        for group_name, tokens in signal_groups.items():
            if any(token in artifact_lower for token in tokens):
                matched_groups.add(group_name)

    presence_score = 0.35
    count_score = min(0.15, (len(cleaned_artifacts) / 3.0) * 0.15)
    diversity_score = (len(matched_groups) / 4.0) * 0.20
    traceability_score = 0.20 if has_traceability else 0.0
    date_context_score = 0.10 if has_date_context else 0.0

    final_score = round(
        _clamp(
            presence_score + count_score + diversity_score + traceability_score + date_context_score,
            0.0,
            1.0,
        ),
        3,
    )

    breakdown = {
        "artifact_presence": round(presence_score, 3),
        "artifact_count": round(count_score, 3),
        "artifact_signal_diversity": round(diversity_score, 3),
        "artifact_traceability": round(traceability_score, 3),
        "artifact_date_context": round(date_context_score, 3),
        "final": final_score,
    }
    return final_score, breakdown, has_traceability


def _build_capa_validation_experiment(
    defect: Dict[str, str],
    category: str,
    risk_score: int,
    capa_actions: List[str],
) -> Dict[str, object]:
    defect_id = defect.get("defect_id", "UNKNOWN")
    component = defect.get("component", "unknown component")
    severity = defect.get("severity", "low")
    selected_capa = capa_actions[0] if capa_actions else "Implement targeted preventive control"

    return {
        "experiment_id": f"EXP-{defect_id}",
        "hypothesis_to_test": f"Applying selected CAPA reduces recurrence for {category} issues in {component}.",
        "baseline_metric": f"Current defect recurrence rate for {component} / {category}",
        "intervention": selected_capa,
        "measurement_window": "next_2_sprints",
        "sample_size_or_runs": "minimum_5_relevant_runs_or_all_occurrences",
        "acceptance_criteria": {
            "target_reduction_percent": 20 if risk_score >= 80 else 15,
            "no_regression_in_adjacent_quality_metrics": True,
        },
        "rollback_condition": "If recurrence worsens or critical risk increases after intervention, rollback and re-open RCA.",
        "owner_role": "QA_Lead",
        "priority": "high" if risk_score >= 80 else "medium",
        "severity_context": severity,
    }


def _to_float(value: object) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _evaluate_capa_effectiveness(
    defect: Dict[str, str],
    experiment_plan: Dict[str, object],
    policy: Dict[str, float],
) -> Dict[str, object]:
    outcome = defect.get("experiment_outcome", {})
    if not isinstance(outcome, dict) or not outcome:
        return {
            "status": "not_available",
            "score": 0.0,
            "reason": "No experiment outcome provided yet.",
        }

    executed = bool(outcome.get("executed", False))
    if not executed:
        return {
            "status": "not_available",
            "score": 0.0,
            "reason": "Experiment outcome exists but is marked as not executed.",
        }

    baseline = _to_float(outcome.get("baseline_value"))
    post = _to_float(outcome.get("post_value"))
    if baseline is None or post is None or baseline == 0:
        return {
            "status": "invalid_data",
            "score": 0.0,
            "reason": "Outcome is missing valid numeric baseline_value or post_value.",
        }

    higher_is_better = bool(outcome.get("higher_is_better", False))
    if higher_is_better:
        actual_change_percent = ((post - baseline) / abs(baseline)) * 100.0
    else:
        actual_change_percent = ((baseline - post) / abs(baseline)) * 100.0

    target_reduction_percent = _to_float(outcome.get("target_reduction_percent"))
    if target_reduction_percent is None:
        target_reduction_percent = _to_float(
            experiment_plan.get("acceptance_criteria", {}).get("target_reduction_percent")
            if isinstance(experiment_plan.get("acceptance_criteria"), dict)
            else None
        )
    if target_reduction_percent is None or target_reduction_percent <= 0:
        target_reduction_percent = float(policy.get("default_target_reduction_percent", 15.0))

    adjacent_regression_detected = bool(outcome.get("adjacent_regression_detected", False))
    sample_size = int(_to_float(outcome.get("sample_size")) or 0)
    min_sample_size = int(policy.get("min_sample_size", 5))

    target_achievement_ratio = max(0.0, actual_change_percent / target_reduction_percent)
    target_component = min(1.0, target_achievement_ratio)
    regression_component = 0.0 if adjacent_regression_detected else 1.0
    sample_component = 1.0 if sample_size >= min_sample_size else (sample_size / max(1, min_sample_size))

    weight_target = float(policy.get("weight_target", 0.70))
    weight_regression = float(policy.get("weight_regression", 0.20))
    weight_sample = float(policy.get("weight_sample", 0.10))
    weight_total = weight_target + weight_regression + weight_sample
    if weight_total <= 0:
        weight_target, weight_regression, weight_sample = 0.70, 0.20, 0.10
    else:
        weight_target /= weight_total
        weight_regression /= weight_total
        weight_sample /= weight_total

    score = 100.0 * (
        weight_target * target_component
        + weight_regression * regression_component
        + weight_sample * sample_component
    )
    score = round(_clamp(score, 0.0, 100.0), 2)

    effective_threshold = float(policy.get("effective_threshold", 80.0))
    partial_threshold = float(policy.get("partial_threshold", 60.0))
    if score >= effective_threshold:
        status = "effective"
    elif score >= partial_threshold:
        status = "partial"
    else:
        status = "ineffective"

    return {
        "status": status,
        "score": score,
        "actual_change_percent": round(actual_change_percent, 2),
        "target_reduction_percent": round(target_reduction_percent, 2),
        "target_achievement_ratio": round(target_achievement_ratio, 3),
        "adjacent_regression_detected": adjacent_regression_detected,
        "sample_size": sample_size,
        "sample_size_min_required": min_sample_size,
    }


def analyzer_agent(
    defect: Dict[str, str],
    severity_model: Dict[str, int],
    known_categories: List[str],
    missing_fields: List[str],
    confidence_calibration: Dict[str, float],
    prioritization_weights: Dict[str, float],
    priority_tiers: Dict[str, int],
    min_hypothesis_support: float,
    require_evidence_artifact_for_capa: bool,
    min_artifact_quality_score: float,
    require_artifact_traceability: bool,
    require_capa_validation_experiment: bool,
    outcome_evaluation_policy: Dict[str, float],
) -> AgentResult:
    defect_id = defect.get("defect_id", "UNKNOWN")
    summary = defect.get("summary", "")
    observed = defect.get("observed_behavior", "")
    text = f"{summary} {observed}"

    category, base_confidence = _infer_category(text, known_categories)
    severity = defect.get("severity", "low")
    risk_score = _severity_to_risk(severity, severity_model)
    confidence, confidence_breakdown = _calibrate_confidence(
        base_confidence,
        missing_fields,
        defect,
        confidence_calibration,
    )
    repeat_signal = _has_repeat_signal(defect)
    hypothesis_support_score, assumptions, support_breakdown = _build_evidence_support(defect, repeat_signal)
    artifacts = defect.get("evidence_artifacts", [])
    has_evidence_artifacts = isinstance(artifacts, list) and len(artifacts) > 0
    artifact_quality_score, artifact_quality_breakdown, artifact_traceability_pass = _analyze_artifact_quality(defect)
    priority_score = _compute_priority_score(
        risk_score=risk_score,
        confidence=confidence,
        repeat_signal=repeat_signal,
        weights=prioritization_weights,
    )
    priority_tier = _priority_tier(priority_score, priority_tiers)

    root_cause_hypothesis = (
        f"Provisional {category} hypothesis inferred from defect narrative and symptom keywords."
    )

    supports_capa = hypothesis_support_score >= min_hypothesis_support and not missing_fields
    if require_evidence_artifact_for_capa:
        supports_capa = supports_capa and has_evidence_artifacts
    supports_capa = supports_capa and artifact_quality_score >= min_artifact_quality_score
    if require_artifact_traceability:
        supports_capa = supports_capa and artifact_traceability_pass

    if artifact_quality_score < min_artifact_quality_score:
        assumptions.append(
            f"Artifact quality score {artifact_quality_score:.2f} is below threshold {min_artifact_quality_score:.2f}."
        )
    if require_artifact_traceability and not artifact_traceability_pass:
        assumptions.append("Evidence artifacts are not traceable to the defect ID.")

    rca_5whys = _build_five_whys(category, defect, assumptions)

    if supports_capa:
        action_mode = "confirmed_capa"
        capa_actions = _capa_by_category(category)
        investigation_actions: List[str] = []
        capa_validation_experiment = _build_capa_validation_experiment(defect, category, risk_score, capa_actions)
    else:
        action_mode = "investigate_first"
        capa_actions = []
        investigation_actions = _investigation_actions(assumptions, category)
        capa_validation_experiment = {}

    if action_mode == "confirmed_capa" and require_capa_validation_experiment and not capa_validation_experiment:
        action_mode = "investigate_first"
        capa_actions = []
        investigation_actions = _investigation_actions(
            assumptions + ["Mandatory CAPA validation experiment is missing."],
            category,
        )

    capa_effectiveness = _evaluate_capa_effectiveness(
        defect=defect,
        experiment_plan=capa_validation_experiment,
        policy=outcome_evaluation_policy,
    )

    confidence_breakdown = {
        **confidence_breakdown,
        "hypothesis_support_score": hypothesis_support_score,
        "support_reproduction_steps": round(support_breakdown.get("reproduction_steps", 0.0), 3),
        "support_observed_behavior": round(support_breakdown.get("observed_behavior", 0.0), 3),
        "support_expected_behavior": round(support_breakdown.get("expected_behavior", 0.0), 3),
        "support_component_context": round(support_breakdown.get("component_context", 0.0), 3),
        "support_summary_quality": round(support_breakdown.get("summary_quality", 0.0), 3),
        "support_created_date": round(support_breakdown.get("created_date", 0.0), 3),
        "support_evidence_artifacts": round(support_breakdown.get("evidence_artifacts", 0.0), 3),
        "support_repeat_signal": round(support_breakdown.get("repeat_signal", 0.0), 3),
        "artifact_quality_score": artifact_quality_score,
        "artifact_traceability_pass": 1.0 if artifact_traceability_pass else 0.0,
    }

    return AgentResult(
        defect_id=defect_id,
        root_cause_hypothesis=root_cause_hypothesis,
        hypothesis_support_score=hypothesis_support_score,
        assumptions=assumptions,
        category=category,
        rca_5whys=rca_5whys,
        action_mode=action_mode,
        capa_actions=capa_actions,
        investigation_actions=investigation_actions,
        artifact_quality_score=artifact_quality_score,
        artifact_quality_breakdown=artifact_quality_breakdown,
        artifact_traceability_pass=artifact_traceability_pass,
        capa_validation_experiment=capa_validation_experiment,
        capa_effectiveness=capa_effectiveness,
        confidence=confidence,
        confidence_breakdown=confidence_breakdown,
        risk_score=risk_score,
        priority_score=priority_score,
        priority_tier=priority_tier,
        repeat_signal=repeat_signal,
        missing_fields=missing_fields,
    )


def validator_agent(
    result: AgentResult,
    missing_fields: List[str],
    min_confidence: float,
    min_hypothesis_support: float,
    min_artifact_quality_score: float,
    require_artifact_traceability: bool,
    require_capa_validation_experiment: bool,
) -> Dict[str, object]:
    if result.action_mode == "confirmed_capa":
        action_policy_ok = (
            len(result.capa_actions) > 0
            and result.hypothesis_support_score >= min_hypothesis_support
            and result.artifact_quality_score >= min_artifact_quality_score
        )
        if require_artifact_traceability:
            action_policy_ok = action_policy_ok and result.artifact_traceability_pass
        if require_capa_validation_experiment:
            action_policy_ok = action_policy_ok and bool(result.capa_validation_experiment)
    else:
        action_policy_ok = len(result.investigation_actions) > 0

    checks = {
        "missing_required_fields": len(missing_fields) == 0,
        "confidence_above_threshold": result.confidence >= min_confidence,
        "has_complete_5whys": len(result.rca_5whys) == 5,
        "hypothesis_support_above_threshold": result.hypothesis_support_score >= min_hypothesis_support,
        "artifact_quality_above_threshold": result.artifact_quality_score >= min_artifact_quality_score,
        "artifact_traceability_ok": (result.artifact_traceability_pass if require_artifact_traceability else True),
        "has_capa_validation_experiment": (
            bool(result.capa_validation_experiment)
            if (require_capa_validation_experiment and result.action_mode == "confirmed_capa")
            else True
        ),
        "action_policy_compliant": action_policy_ok,
    }
    accepted = all(checks.values())

    return {
        "accepted": accepted,
        "checks": checks,
        "missing_fields": missing_fields,
    }

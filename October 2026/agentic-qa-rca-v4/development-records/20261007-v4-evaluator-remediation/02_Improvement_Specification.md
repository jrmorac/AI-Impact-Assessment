# Improvement Specification — v4 Evaluator Remediation

Owner: QA Engineering Team / Senior Agentic Engineer
Scope: F-001 through F-009 (Tier 1 + Tier 2). F-010 (Tier 3) is explicitly out of scope for this cycle.

## Acceptance criteria per finding

### F-001 — Maintainer placeholder
- `README_OPS.md`, `ARCHITECTURE_AND_EVALUATOR_APPLICABILITY.md`, `docs/review/RELEASE_SIGNOFF_TEMPLATE.md` no longer contain "Jose Mora"; all read "QA Engineering Team".
- Applies identically to both `agentic-qa-rca-v4/` and `agentic-qa-rca-shareable-v4/`.
- Out of scope: historical `development-records/` from prior cycles (internal implementation evidence, excluded from the shareable package; rewriting history is not appropriate).

### F-002 — Release tagging
- `VERSION` = `4.0.0` and `CHANGELOG.md` has a `4.0.0` entry in both packages (done).
- Git tag `v4.0.0` created in the repository (**pending human action** — no terminal/git access available in this session).

### F-003 / F-004 / F-006 — README consolidation
- `README.md` has dedicated, discoverable sections: "Intended Audience", "Production Deployment / Local-Only Scope", "Out-of-Scope and Prohibited Uses", "Limitations and Failure Modes".
- Content must not contradict existing statements in `ARCHITECTURE_AND_EVALUATOR_APPLICABILITY.md` or `README_OPS.md`.

### F-005 — CSP documentation
- `README_OPS.md` documents the exact CSP directive string, explains what it permits/restricts, and states how to modify it.

### F-007 — Dedicated error lifecycle event
- A new `error` event type is emitted (not replacing) alongside the existing `agent_step` outcome='error' whenever an exception is caught in `run_triage_agents`, `run_capa_agent`, or `run_testcase_agent`.
- Required fields: `event`, `error_type`, `error_category` (`transient`|`permanent`|`guardrail`), `step_name`; optional `defect_id`, `request_id`, `session_id`.
- No raw traceback or original exception message text in the event payload (tracebacks remain in controlled logs only, consistent with `web_app.py`'s existing pattern).
- Positive: forced exception on each of the 5 call sites (planner/analyzer/validator/capa/testcase) emits exactly one `error` event with correct `error_category`.
- Negative: a successful run emits zero `error` events.
- Boundary: golden regression suite (why1/why3/why5) behavior is unchanged.

### F-008 — Prompt template extraction + versioning
- Five Whys and guided-RCA question/answer-guidance text moved from hardcoded Python into `prompts/*.yaml`, each with a `version: 1` field.
- Behavior is byte-identical to the pre-extraction hardcoded strings for all categories and both guided-flow question builders.
- Positive: golden regression and new unit tests confirm identical output text.

### F-009 — Frontend accessibility
- Escape key closes any open overlay (export modal, term tooltip, open `<details class="advanced-panel">`), not only the export modal.
- Field-level errors (`PATH_NOT_ALLOWED`, `EXPORT_APPROVAL_REQUIRED`, `EXPORT_CONFLICT`, `INVALID_REQUEST`, etc.) include an actionable remediation hint appended to the existing message, without changing the API contract.
- `aria-describedby` links inputs to their hint text; `aria-invalid` is set/cleared based on validation state; existing `aria-live="assertive"` region is reused (no new live region).
- No change to CSP, API request/response shapes, or existing positive-path functionality.

## Out of scope for this cycle
F-010 (Tier 3): Docker/containerization, cloud INFRASTRUCTURE.md, WORM-backed audit storage, KMS-encrypted persistent logging, data-residency policy/model cards, per-session intent capsules, real-time monitoring/alerting platform, `tool_call` lifecycle events, cross-session knowledge extraction. Rationale: disproportionate to a declared local, single-user, deterministic tool; see `10_Risk_and_Rollback_Register.md`.

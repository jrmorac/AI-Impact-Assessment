# Phase 2 AI Enhancements for the Agentic QA RCA App

## Objective

Add an optional AI-assisted recommendation layer to the existing deterministic RCA workflow without replacing the validated, human-controlled process. The core app will remain the system of record for root cause analysis, while AI supports drafting, prioritization, and quality review.

## Design Principle

The app must remain deterministic and auditable. AI should be advisory only. Any generated recommendation must be clearly labeled as a draft, require human review, and never be auto-submitted or auto-exported without explicit user action.

## Scope of Phase 2

The Phase 2 version should support the following recommended features:

1. AI-generated answer suggestions for the current Why question
2. AI-generated CAPA recommendations based on root cause and evidence
3. AI-generated regression test case suggestions
4. Confidence and evidence-gap scoring
5. Human approval workflow before accepting AI suggestions

## Core Constraints

### 1. Compliance and Data Handling
- No production patient data, client identifiers, or sensitive operational data may be used.
- Use only synthetic / approved test data.
- No AI interaction may send protected or regulated information to external tools without formal approval.
- All AI output must be reviewed by a human before actions are finalized.

### 2. Deterministic Core Must Stay Intact
- The deterministic RCA workflow remains the primary execution path.
- The AI layer is supplemental, not authoritative.
- No automatic acceptance of AI-generated answers or corrective actions.
- Users must explicitly approve or edit any AI output before submission.

### 3. Auditability
- Record the model version, prompt version, and input context used for each AI recommendation.
- Log the user decision: accepted, edited, or rejected.
- Maintain traceability for each final answer and final CAPA action.

### 4. Model Reliability
- AI output should be treated as suggestion quality, not fact.
- Low-confidence or weak-evidence suggestions should be flagged for review.
- The app should not hide uncertainty; it should surface evidence gaps and confidence ratings.

### 5. Data and Deployment Constraints
- AI functionality should be optional and configurable.
- If the app is used in a restricted environment, support offline or approved internal-model deployment.
- The app should support model provider configuration without hardcoding a single service.

## Proposed AI Features

### A. Suggested Answer Drafts

When the user is preparing an answer for the current Why node, the app may generate 2–3 candidate answer drafts based on:
- current defect data
- evidence references
- prior Why chain entries
- known patterns from similar RCA cases

Recommended UX:
- button: “Suggest answer”
- display a short list of possible drafts
- show confidence score and reasons for the recommendation
- allow user to insert one draft into the answer field or edit manually

Example output:
- Suggested answer: “The release pipeline skipped validation for the new configuration because the pre-deploy check was not gated by feature flag state.”
- Confidence: 0.74
- Evidence gap: missing release log reference

### B. CAPA Recommendation Engine

After root cause selection or completion of the Why flow, the AI assistant can suggest potential corrective and preventive actions based on:
- root cause category
- process gap
- affected system area
- historical RCA patterns

Suggested CAPA categories:
- engineering fix
- configuration control
- release gating
- monitoring / alerting
- regression test coverage
- SOP or process training

Recommended UX:
- button: “Suggest CAPA actions”
- show a checklist of draft actions
- allow selection or editing before export
- require final user approval before export to CSV

### C. Test Case Recommendation Generator

When root cause analysis is close to completion, the AI layer can propose test cases that validate the corrective action and reduce regression risk.

Suggested fields:
- test case title
- scenario description
- expected result
- affected module or workflow
- priority

Recommended UX:
- generate test case draft list after root cause is confirmed
- allow one-click insertion into the ADO export flow
- keep the final CSV export under human control

### D. Evidence Quality Feedback

AI can help assess whether the current answer is adequately supported by evidence.

Suggested assessment categories:
- strong evidence
- moderate evidence
- weak evidence
- missing evidence

The AI should highlight:
- what evidence is missing
- which facts are implied rather than documented
- whether the answer is logically connected to the root cause

### E. Confidence and Risk Signals

The app should expose confidence scores and risk labels instead of silent recommendations.

Example:
- confidence: 0.81
- risk: medium
- rationale: “The answer is consistent with release logs but lacks a direct validation artifact.”

## Ethical and Operational Guardrails

- Do not generate actions that are legally or operationally binding without human approval.
- Do not assume root cause without evidence.
- Do not replace evidence-based QA decisions with model prediction.
- Keep all AI-assisted suggestions visible and editable.
- Record user decisions for review and traceability.

## Proposed Phase 2 UI Pattern

Add a new optional panel or drawer titled:
- AI Assistant
- Suggest Recommendations
- Draft Review

This panel should include:
- Suggest answer
- Suggest CAPA actions
- Suggest regression tests
- View evidence quality
- Accept / Edit / Reject controls

Important: the panel must not overwrite the user’s working answer without explicit action.

## Example Workflow

1. User completes the current Why step and provides evidence.
2. User clicks “Suggest answer.”
3. AI returns 2–3 draft answers with confidence and rationale.
4. User selects the best option or edits it manually.
5. User reviews the answer and submits it to the deterministic workflow.
6. If root cause is confirmed, user clicks “Suggest CAPA actions.”
7. User reviews, edits, and approves the final CAPA items.
8. User exports the approved report and CSV artifacts.

## Minimum Viable Phase 2 Scope

If scope must stay lean, the minimum viable Phase 2 should include only:

1. AI answer suggestions for the current Why
2. AI CAPA suggestion list
3. Human approval gate before acceptance
4. Confidence and evidence-gap summary

This keeps the scope practical while adding measurable value.

## Expected Value

The Phase 2 AI layer should improve:
- analyst productivity
- consistency of answer formulation
- speed of CAPA drafting
- coverage of regression test suggestions

The overall value comes from making the deterministic workflow faster and more consistent, not from replacing it.

## Recommended Decision

Proceed with Phase 2 only if the tool remains:
- human-led
- evidence-based
- auditable
- safe for healthcare QA use

If those conditions hold, AI can become a valuable advisory assistant for RCA and corrective-action development without compromising trust or compliance.

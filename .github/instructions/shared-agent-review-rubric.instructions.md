---
description: "Use when triaging QA findings, writing specs, planning fixes, reviewing code, or making integration decisions across Senior Backend Engineer, Senior Frontend Engineer, Senior QA Agent, and Senior Agentic Engineer. Defines shared severity, traceability, and done criteria."
name: "Shared Agent Review Rubric"
---
# Shared Agent Review Rubric

## Purpose
Use this rubric as the single quality baseline for all specialized agents.

## Severity Model
- Critical: data integrity, security boundary, or core workflow break.
- High: major functional risk, repeated incorrect behavior, or release blocker.
- Medium: meaningful quality or reliability issue with workaround.
- Low: minor issue with limited operational impact.

## Required Output Order
1. Findings ordered by severity.
2. Spec or requirement delta.
3. Plan or implementation summary.
4. Validation and test evidence.
5. Risks and rollback notes.
6. Final recommendation: Approve, Conditionally Approve, or Block.

## Acceptance Criteria Rules
- Each requirement must be specific and verifiable.
- Expected outcomes must be observable and testable.
- Include positive, negative, and boundary scenarios.
- Do not close any item with vague language.

## Traceability Requirements
Each work item must map through:
- Finding ID -> Requirement ID -> Task ID -> Code or config change -> Test evidence -> Decision record

If any link is missing, the item remains open.

## Evidence Quality Rules
- Prefer deterministic and repeatable checks.
- Flag assumptions explicitly.
- Require human review before final approval decisions.
- Use synthetic and non-sensitive artifacts only.

## Governance Gates
- Pre-implementation: triage complete, spec approved, risks recorded.
- Pre-merge: tests pass, no open Critical or High findings, traceability updated.
- Pre-release: metrics captured, integration decision recorded, residual risk accepted.

## Block Conditions
- Missing acceptance criteria for High or Critical findings.
- Missing regression evidence for behavior changes.
- Conflicting agent recommendations without documented resolution.
- Incomplete traceability matrix.

## Done Criteria
Work is done only when:
- All required gates pass.
- Required evidence is attached.
- Final decision record is signed off.

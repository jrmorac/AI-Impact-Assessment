---
description: "Use when preparing merge or release decisions for app enhancements and defect fixes. Enforces release-gate checks, residual risk handling, and rollback readiness for multi-agent workflows."
name: "Release Gate Checklist"
---
# Release Gate Checklist

## Scope
Apply to any change set produced from QA findings and multi-agent implementation work.

## Gate 1: Pre-Implementation
- Findings are triaged with severity and reproducibility.
- Spec includes acceptance criteria and out-of-scope boundaries.
- Risks and rollback triggers are defined for High and Critical items.
- Owners and target dates are assigned.

## Gate 2: Pre-Merge
- Code changes map to approved requirements.
- Positive, negative, and boundary tests are executed or evidenced.
- No open Critical findings.
- No open High findings without explicit owner-approved waiver.
- Traceability matrix is current.

## Gate 3: Pre-Release
- Integration review completed.
- Conflicting recommendations are resolved and documented.
- Residual risks are listed with acceptance owner.
- Rollback actions are explicit and testable.
- Final decision recorded: Approve, Conditionally Approve, or Block.

## Required Artifacts
- Findings triage record
- Improvement specification
- Implementation plan
- Code review findings
- Traceability matrix
- Metrics baseline versus after snapshot
- Risk and rollback register
- Integration decision record

## Non-Negotiable Rules
- No production secrets, PII, or sensitive client data in evidence.
- No silent closure of unresolved High or Critical items.
- No release decision without explicit owner sign-off.

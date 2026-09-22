# Enhancement Implementation Plan

Plan ID: PLAN-V2-20260922-01  
Status: Ready for implementation  
Release posture: Blocked

## Sequence

1. **Backend route and export contract — Senior Backend Engineer**
   - Move `/api/run-demo` outside the quick-plan branch.
   - Add `evidence/capa_exports` to the write allowlist while retaining root/symlink checks.
   - Provide deterministic defaults for CAPA and ADO output when blank, matching the UI.
   - Validate provider and variant values.
   - Normalize state and validation errors to safe 400/409 responses.

2. **Session state and Why depth — Senior Backend Engineer**
   - Decide and document normal target-depth behavior: stop at Why 5, or expose a clearly labeled advanced continuation mode.
   - Prevent answer append when status is `needs_more_evidence`; require revision.
   - Add closed-session guard to revision.
   - Change revision API to accept an explicit Why index or selected node identity, then recalculate checkpoint/status without duplicate nodes.

3. **Frontend carousel and submit state — Senior Frontend Engineer**
   - Keep a distinct live-answer index from historical navigation index.
   - Disable Next at the normal target-depth boundary and prevent silent reset to a sixth item.
   - Enable Submit for `awaiting_answer` and valid `needs_more_evidence` revision states.
   - Preserve entered fields on failure, keep the revise checkbox stable, and label the action as revise when a historical/current node is selected.

4. **Trace viewer refresh — Senior Frontend Engineer**
   - Refresh report options after demo/export and preserve a valid selection.
   - Auto-select the newest valid batch JSON report when no selection exists.
   - Populate defect IDs on report selection and load the selected trace, clearing stale trace data on failure or empty results.

5. **Regression and browser evidence — Senior QA Agent**
   - Add API/unit tests for route dispatch, output allowlists/defaults, export validation, Why state transitions, target depth, and revision replacement.
   - Add browser smoke checks for both v2 packages: export previews, Why 5 boundary, trace dropdowns, and revise submit.
   - Re-run existing security tests and retain synthetic fixtures only.

6. **Mirrored package and release gate — Senior Agentic Engineer**
   - Apply equivalent changes to `agentic-qa-rca-shareable-v2`.
   - Update traceability, risk/rollback, and integration decision records.
   - Rebuild the v2 ZIP only after both packages pass.

## Task mapping

| Task | Requirement | Owner | Evidence |
|---|---|---|---|
| V2-T-001 | V2-ROUTE-01/V2-EXP-01 | Backend | API route/export tests and generated synthetic files |
| V2-T-002 | V2-EXP-02 | Backend + QA | Negative path/provider/variant tests |
| V2-T-003 | V2-WHY-01/V2-STATE-01 | Backend | Target-depth and carousel boundary tests |
| V2-T-004 | V2-SUBMIT-01..03 | Backend + Frontend | Session transition and revision replacement tests |
| V2-T-005 | V2-TRACE-01 | Frontend | Trace selector/trace rendering browser evidence |
| V2-T-006 | All | QA | Regression matrix and browser smoke results |
| V2-T-007 | All | Agentic lead | Mirrored package, traceability, release decision, ZIP hash |

## Release gates

- Pre-implementation: this spec approved and target-depth policy decided.
- Pre-merge: all API/unit tests pass; no High finding remains without evidence.
- Pre-release: browser evidence attached, both v2 packages match behavior, ZIP rebuilt, risks accepted, and owner sign-off recorded.

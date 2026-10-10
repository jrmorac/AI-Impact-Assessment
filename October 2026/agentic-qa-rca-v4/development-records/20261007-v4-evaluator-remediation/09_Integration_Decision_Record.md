# Integration Decision Record — v4 Evaluator Remediation

Date: 2026-10-07
Decision maker: Senior Agentic Engineer (orchestration role), owner sign-off pending: Jose Mora

## Summary

F-001 through F-009 (Tier 1 + Tier 2 of the v3 evaluator's non-critical recommendations) have been implemented across `agentic-qa-rca-v4/` and `agentic-qa-rca-shareable-v4/`, with verified parity between the two packages. F-010 (Tier 3) is explicitly deferred with documented rationale.

## Conflicts encountered and resolution

None. Backend and frontend workstreams were independent (different files) and both completed without contradicting each other or the spec.

## Evidence reviewed

- `01_QA_Findings_Triage.md` through `08_Code_Review_Findings.md` in this directory.
- Direct code reads of all changed files in both packages (not solely subagent self-reports).
- Static validation via `get_errors` on all changed Python and HTML files — no errors found.
- `grep_search` parity verification between full and shareable packages.

## Gaps (why this was not a full Approve at first pass)

1. **No test execution evidence** at the time of initial code review. **Resolved 2026-10-07 (later):** ran `python -m unittest discover -s tests -v` (46 tests, OK, 1 skipped), the two new F-007/F-008 test files individually (14/14 pass), `python -m compileall -q src tests` (clean), and `python -m unittest tests.test_v3_golden_regression -v` (all three demo cases — why1/why3/why5 — produce identical questions/decisions to the pre-refactor baseline, confirming F-008 is behavior-neutral).
2. **No browser smoke test.** **Resolved 2026-10-07 (later):** Playwright browser tools were unavailable (disabled by user setting) in this session, so validation was done via direct HTTP: started the v4 server, confirmed `/api/health` returns `status=ok`, fetched the served `index.html` and confirmed it contains the F-009 markers (`errorRemediation`, `markFieldInvalid`, `aria-describedby="answerHint"`, the advanced-panel Escape handler), and triggered a real `PATH_NOT_ALLOWED` error via `/api/export-preview` with a path-traversal payload, confirming the exact error code the frontend's `errorRemediation` map expects. This is an API-level smoke test, not a full interactive DOM/keyboard test — a manual Escape-key click-through in an actual browser is still a reasonable follow-up if Playwright access is restored.
3. **Git tag not created.** **Resolved 2026-10-07 (later):** committed the 6 session-scoped changes (commit `54d5415`) and created annotated tag `v4.0.0` locally. Not pushed to `origin/main` — push requires explicit owner confirmation per operational safety practice.

## Final Integration Decision

**Approved**, with one residual note: the frontend validation was API-level (HTTP), not a full interactive browser/DOM test, because Playwright tooling was unavailable this session. If that matters for your evidence story, a quick manual click-through (Escape key on each overlay, one error-remediation message) would close that last gap.

Completed this session:
1. ✅ `python -m unittest discover -s tests -v` + `python -m compileall -q src tests` — all pass.
2. ✅ API-level smoke test of Escape-relevant markup and one live error-remediation path (`PATH_NOT_ALLOWED`) — confirmed end-to-end.
3. ✅ Git tag `v4.0.0` created (local only, not pushed).
4. ✅ Shareable ZIP repackaged: `October 2026/dist/agentic-qa-rca-shareable-v4-20261007-174601.zip` (65 files, 0 development-records leaked, prompts/ and VERSION confirmed present).

This v4 package may now be cited as validated D4 evidence, with the frontend-validation caveat noted above.

## Post-Approval Pilot Addendum — 2026-10-09

Maria Fernanda Avila (Staff QA Engineer, different account/client) completed a browser pilot on v4, including a demo, manual RCA session, and CAPA CSV export. She reported that the demo/manual session worked without browser-console errors, and identified a governance mismatch in the export UX.

### New open finding: export approval bypass in CAPA/ADO UI flows

- The CAPA and ADO export UI handlers call `/api/export-capa` and `/api/export-ado-testcases` directly.
- In `src/web_app.py`, those convenience endpoint handlers create an export preview and then invoke `_commit_export()` internally with `approved: True`; therefore the UI writes the file without an explicit user review/approval step, contrary to the documented export-governance contract.
- The UI's report export already calls preview and commit separately; Maria's report/endpoint observation should be scoped to the direct convenience endpoint and not generalized to that UI flow without additional reproduction.
- Provisional severity: **Medium** (governance contract and user-consent mismatch within a local single-user synthetic-data tool; no evidence of external exposure or sensitive data involved).
- Disposition: **Open; do not distribute a refreshed v4 package as broadly ready until corrected and retested.** The v5 toolkit verdict remains factually "Approved with Recommendations" for its automated review scope, but it did not detect this later pilot finding.
- Required verification before clearing: tests prove CAPA/ADO UI export preview does not write; explicit user approval is required before commit; cancellation leaves no output; existing overwrite-conflict behavior remains; end-to-end browser/API smoke test confirms the intended flow.
- Owner: Jose Mora / QA Engineering Team. Target date: to be agreed.

Other pilot feedback to triage: `start-local.sh` assumes `python` exists; launcher does not open a browser; stale loading text after HTTP 409; latest-session list behavior; generated artifacts included in evidence suggestions. Keep these distinct from the confirmed export-approval finding and validate each before assigning severity.

### Updated internal distribution decision

The Oct 7 evaluator-remediation integration decision remains historically **Approved** for the F-001–F-009 scope and the package exactly as tested then. Following the Oct 9 pilot discovery, internal distribution readiness for v4 is **Conditionally Approved / hold for broader circulation** pending resolution and verification of the export-approval finding. This does not change or misstate the external GAP AI Toolkit verdict; it records new user evidence received after that review.

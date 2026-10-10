# Risk and Rollback Register — v4 Evaluator Remediation

## Residual risks

| Risk | Likelihood | Impact | Mitigation | Acceptance owner |
|---|---|---|---|---|
| CAPA/ADO export UI paths commit exports without an explicit user approval step (Maria v4 pilot, 2026-10-09; confirmed by source review of `/api/export-capa` and `/api/export-ado-testcases`) | Medium (provisional) | High for the documented governance contract; export can write when user expected a review/approval gate | Hold broader v4 distribution. Route these UI actions through preview → explicit user approval → commit; test no-write-before-approval, cancel/no-write, and overwrite conflict; re-run suite and pilot. | Jose Mora / QA Engineering Team |
| Other Maria pilot observations not yet triaged: launcher assumes `python`; browser is not auto-opened; stale loading message after 409; latest-session list issue; generated files included in evidence suggestions | Low-Medium (untriaged) | Usability/reliability impact not yet established | Reproduce individually, assign severities, and add to a follow-up spec only after confirmation. | Jose Mora |
| Frontend Escape/ARIA changes had API/static validation only before pilot | Low | Remaining accessibility behavior is not fully verified by screen-reader testing; pilot reported no browser console errors but did not verify WCAG conformance | Perform keyboard and screen-reader checks after export-flow correction; don't claim full WCAG 2.1 AA certification from source inspection alone. | Jose Mora |
| Git tag `v4.0.0` and test execution | Resolved | No remaining risk from missing tag/test evidence | Local tag exists; 46 tests passed (1 skipped), 14 targeted tests passed, compileall clean, golden regression passed on 2026-10-07. | Jose Mora |
| Tier 3 items (F-010) remain unaddressed | Low | Low — these were already non-critical in the v3 evaluator review and are explicitly out of scope for a local single-user tool | Documented decision to defer; revisit only if deployment scope changes (shared/cloud/multi-user) | Jose Mora |
| Shareable package sync was done via manual targeted diffs rather than a verified automated copy | Low | Medium — a missed diff could cause the shareable package to silently diverge from the full project | Mitigated by `grep_search` parity verification (46/46 matching markers); recommend a follow-up full-file diff tool (e.g. `git diff --no-index`) if available in a future session | Jose Mora |

## Rollback plan

If post-distribution testing finds a regression:
1. Stop distributing `agentic-qa-rca-shareable-v4`.
2. Revert to the last known-good v3 package: `October 2026/dist/agentic-qa-rca-shareable-v3-20260922-184218.zip`.
3. Do not delete `agentic-qa-rca-v4/` or `agentic-qa-rca-shareable-v4/` — preserve for investigation.
4. Record the failing test name, affected finding ID, and owner decision in this file before re-attempting the fix.

## Deferred scope (F-010) rationale

Docker/containerization, cloud INFRASTRUCTURE.md, WORM-backed audit storage, KMS-encrypted persistent logging, formal data-residency policy/model cards, per-session intent capsules, real-time monitoring/alerting platform integration, `tool_call` lifecycle events, and cross-session knowledge extraction all assume a cloud, multi-tenant, or LLM-backed deployment that this tool explicitly does not have (confirmed in `ARCHITECTURE_AND_EVALUATOR_APPLICABILITY.md`'s "Deployment decision" section). Building them now would be disproportionate engineering effort for a declared local, single-user, deterministic tool and was explicitly declined by the owner on 2026-10-07. Revisit if and when deployment scope changes.

## Distribution status after Oct 9 pilot

The GAP AI Toolkit's v5 evaluator verdict remains **Approved with Recommendations** for its audit scope. Internal distribution of the current v4 ZIP is on **hold for broader circulation** until the CAPA/ADO export approval mismatch is fixed and retested. Preserve the package and pilot feedback for investigation; do not silently overwrite the v4 artifact.

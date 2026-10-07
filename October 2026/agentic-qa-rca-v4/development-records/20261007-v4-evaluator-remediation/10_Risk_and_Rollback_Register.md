# Risk and Rollback Register — v4 Evaluator Remediation

## Residual risks

| Risk | Likelihood | Impact | Mitigation | Acceptance owner |
|---|---|---|---|---|
| New unit tests (`test_v4_error_lifecycle_event.py`, `test_v4_prompt_template_extraction.py`) have not been executed in this session | Medium | Medium — a latent bug could ship undetected | Human must run `python -m unittest discover -s tests -v` and `python -m compileall -q src tests` before distribution | Jose Mora |
| Frontend changes (`web/index.html`) were only statically reviewed, not browser-tested | Low-Medium | Medium — a UI regression in Escape handling or ARIA attributes could ship undetected | Human smoke test: open the Web UI, trigger each overlay, confirm Escape closes it; trigger each error code and confirm remediation text appears | Jose Mora |
| Git tag `v4.0.0` not yet created | Low | Low — version drift between `VERSION`/`CHANGELOG.md` and git history | Human runs `git tag v4.0.0` (or equivalent) after test validation passes | Jose Mora |
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

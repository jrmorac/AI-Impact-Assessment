# Risk and Rollback Register

| Risk ID | Risk / trigger | Severity | Preventive control | Rollback or containment | Owner |
|---|---|---|---|---|---|
| RR-001 | Any request reads/writes outside approved directories or bypasses validation through symlink. | Critical | Central validator, allowlist, negative tests, fail-closed behavior. | Disable affected file endpoints and keep server local-only; revert only behind a bounded development flag while fix is prepared. | Senior Backend Engineer |
| RR-002 | Regression suite or CI does not run the security and workflow tests. | Critical | Clean-checkout CI gate and required test IDs. | Block merge/release; retain failing test and revert behavior change if existing workflows break. | Senior QA Agent |
| RR-003 | Logs omit correlation fields or include evidence/PII. | Critical | Field allowlist, sanitized fixtures, schema tests. | Disable production exposure/log sink, preserve local diagnostics without payload logging, correct schema. | Senior Backend Engineer |
| RR-004 | Additive response changes break UI parsing or leave controls disabled after failure. | High | Single API helper, compatibility fields, `finally` cleanup, browser failure tests. | Revert UI/API contract change while retaining tests and documented contract. | Senior Frontend Engineer |
| RR-005 | CSP blocks core UI workflows or preview rendering. | High | Browser console/network checks and explicit asset policy. | Revert to controlled local version, keep shared exposure blocked, correct CSP before retry. | Senior Frontend Engineer |
| RR-006 | Session schema or atomic-write change corrupts legacy synthetic sessions. | High | Versioned reader/migration, backup/temporary file tests. | Disable new write path, restore last known-good synthetic artifacts, migrate explicitly. | Senior Backend Engineer |
| RR-007 | Deployment target expands to cloud/shared/regulatory use without required controls. | Critical | Deployment decision gate and applicability review. | Do not deploy; require architecture/security review for auth, retention, monitoring, WORM, and tenant controls. | Senior Agentic Engineer |

## Residual-risk rule

No Critical or High item may be silently deferred. A waiver requires a named owner, expiration date, compensating control, and release-owner approval.

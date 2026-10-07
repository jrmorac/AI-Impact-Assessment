# Governance Gate Checklist

Record: AER-20260921-01

## Gate 1: Pre-implementation

- [x] Evaluator findings reviewed and normalized.
- [x] Applicable versus N/A criteria documented.
- [x] Requirements have verifiable acceptance criteria.
- [x] Workstream owners and dependencies identified.
- [x] High/Critical risks and rollback triggers recorded.
- [ ] Specification approved by named owner.
- [ ] Deployment target confirmed.

## Gate 2: Pre-merge

- [ ] PR-SEC-01 path tests pass, including traversal and symlink negative cases.
- [ ] PR-QA-01 deterministic regression suite passes.
- [ ] PR-QA-02 CI blocks failures from a clean checkout.
- [ ] PR-OBS-01/02 event and error contract tests pass.
- [ ] PR-SEC-02 CSP browser checks pass.
- [ ] PR-UI-01 and PR-A11Y-01 browser checks pass.
- [ ] No open Critical findings.
- [ ] No open High findings without named, time-bound waiver.
- [ ] Traceability matrix updated with code and test evidence.

## Gate 3: Pre-release

- [ ] Operations and architecture documentation reviewed.
- [ ] Retention, integrity, owner, and rollback decisions recorded.
- [ ] CR-003 and CR-005 browser evidence attached.
- [ ] Synthetic-data compliance confirmed.
- [ ] Metrics/evidence snapshot captured.
- [ ] Residual risks accepted by named owner.
- [ ] Final integration decision signed.

## Current gate result

**BLOCKED at pre-implementation approval / not releasable.** The artifacts are ready for implementation planning, but no code remediation or acceptance evidence has been completed in this record.

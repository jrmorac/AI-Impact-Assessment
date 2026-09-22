# Integration Decision Record

Record ID: IDR-E2-20260922-01  
Date: 2026-09-22  
Decision: **Block shared/production/distributable release; conditionally approve controlled local synthetic validation**

## Owner decisions recorded

- Target: local, single-user, deterministic, synthetic-data-only.
- LLM phase: deferred; no LLM provider will be added now.
- Export approval: separate preview and commit endpoints.
- CI: GitHub Actions.
- Docker: not required for this release.
- Maintainer/release owner: Jose Mora.
- Retention: 360 days by default for synthetic sessions, reports, exports, and logs.

## Reconciled findings

The v2 evaluator rejection contains valid current blockers: no CI/golden regression gate, no human approval/overwrite protection, incomplete local observability, incomplete architecture/operations documentation, and incomplete release evidence.

It also includes LLM and shared-deployment criteria that do not apply to the current implementation: token consumption, model inference guardrails, LLM mocking, LLM exfiltration probes, model cards, GenAI OpenTelemetry, tenant billing, and WORM storage. These are recorded as conditional future requirements and must not be claimed as current capabilities.

## Required unblock conditions

- E2-REQ-01 through E2-REQ-10 implemented and evidenced.
- Separate preview/commit approval and overwrite behavior tested through API and browser.
- Golden deterministic dataset runs in CI from a clean checkout.
- Agent-step logs, tracebacks, retention, and safe correlation fields are validated.
- Architecture diagram, operations runbook, owner, cadence, version, rollback, and classification are documented.
- Working/shareable v2 parity and ZIP evidence are recorded.
- Traceability and residual-risk acceptance are complete.

## Owner decisions complete

All scope decisions are confirmed: local single-user deterministic release, no LLM phase, separate preview/commit endpoints, GitHub Actions, no Docker requirement, Jose Mora as maintainer/release owner, and 360-day default retention.

## Current residual risk

The app remains appropriate for controlled local synthetic testing. It is not approved for shared, production, regulated, or distributable use until applicable requirements and evidence gates close.

# Evaluator Findings Triage

Date: 2026-09-21  
Source: `AI Agent Evaluator feedback report.md`  
Severity model: Critical = security boundary, data integrity, or release blocker; High = major reliability or production risk; Medium = meaningful quality gap with workaround.

## Critical findings

| ID | Finding | Evaluator criteria | Applicability | Required direction |
|---|---|---|---|---|
| F-PR-001 | User-controlled paths can resolve outside the project root and allow unintended reads/writes. | 10.4, 10.8, 10.9 | Confirmed | Enforce read/write directory allowlists, root containment, and symlink-aware validation on every file endpoint. |
| F-PR-002 | No automated regression suite or merge quality gate exists. | 5.1, 5.3, 5.4, 5.5, 5.11; related 2.4 | Confirmed | Add deterministic unit/API/security tests and CI gates using synthetic fixtures only. |
| F-PR-003 | No structured request lifecycle/error observability or request correlation exists. | 3.1, 6.1, 6.2, 6.3, 6.4, 6.7, 6.8 | Confirmed | Add newline-delimited JSON events with request/session correlation and safe error envelopes. |

## High findings

| ID | Finding | Evaluator criteria | Applicability | Required direction |
|---|---|---|---|---|
| F-PR-004 | The production operating contract is incomplete. | 2.4, 2.6, 2.7, 2.10, 7.1, 7.2, 7.3, 7.4, 7.6, 7.7, 7.9, 7.10 | Confirmed for supported-operation documentation; deployment extras conditional | Document runtime, topology, configuration, health, ownership, review cadence, API contract, architecture, retention, and rollback. Add CI and reproducible dependency definition. |
| F-PR-005 | API errors are not semantically differentiated and lack request IDs; UI does not expose actionable traceability. | 4.5, 6.7, 8.6 | Confirmed | Define 4xx/5xx mapping and `{error_code,message,request_id}` response contract; display safe guidance in UI. |
| F-PR-006 | CSP and browser security baseline are incomplete. | 8.1 | Confirmed for any shared/production browser exposure; local pilot risk to document | Add a restrictive CSP compatible with the UI and test normal workflows without unsafe fallback. |

## Medium findings

| ID | Finding | Evaluator criteria | Applicability | Required direction |
|---|---|---|---|---|
| F-PR-007 | Loading state, focus visibility, skip link, and live-region coverage are incomplete. | 8.2, 8.4, 8.5 | Confirmed | Add visible async state, keyboard focus/skip link, and appropriate live announcements. |
| F-PR-008 | Session artifacts lack documented retention and integrity behavior. | 3.7, 11.8 | Confirmed as local evidence governance gap; WORM conditional | Add retention/deletion/recovery policy and atomic writes or integrity hashes. Mark WORM export conditional on compliance decision. |
| F-PR-009 | Existing browser evidence for session and trace refresh remains incomplete. | Prior cycle CR-003, CR-005 | Confirmed | Execute browser-level validation and attach reproducible logs/screenshots before release decision. |

## Not applicable or conditional under current architecture

- LLM routing, model IDs, token budgets, provider abstraction, LLM-as-judge, live model-call mocking, malformed LLM output parsing, jailbreak tests, and GenAI OpenTelemetry attributes: **N/A while the implementation remains rules-based with no LLM provider**.
- Cloud billing tags, cloud monitoring provider, tenant cost anomaly monitoring, and WORM-backed storage: **conditional on an approved shared/cloud/regulatory deployment target**.
- Database migrations, vector indexes, batch inference, external API retry policy, and durable workflow engines: **N/A for the current file-backed local service**.
- Cross-session learning, prompt registries, agent personas, and prompt self-correction: **deferred maintainability enhancements**, not release blockers for the current deterministic engine.

## Triage conclusion

The report's headline count is internally inconsistent with its area table and overlapping criteria. This record consolidates the applicable work into nine findings and six unified requirements. Production approval remains blocked until the critical requirements are implemented and evidenced.

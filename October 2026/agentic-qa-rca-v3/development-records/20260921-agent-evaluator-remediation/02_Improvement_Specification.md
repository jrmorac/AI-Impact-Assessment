# Improvement Specification

Spec ID: SPEC-20260921-01  
Status: Draft for approval  
Owner: Senior Agentic Engineer

## Scope

Remediate applicable evaluator findings for the current deterministic local RCA application. Preserve existing RCA, CAPA, ADO export, and session workflows unless a requirement below explicitly changes the HTTP or file-safety contract.

## Requirements

| Requirement | Source findings | Priority | Acceptance criteria |
|---|---|---|---|
| PR-SEC-01 Confined file access | F-PR-001 | Critical | Every user-controlled path resolves under an explicit allowlist for `project-context/`, `data/input/`, `evidence/rca_sessions/`, and `data/output/`. Reject traversal, outside absolute paths, symlink escapes, missing paths, and disallowed writes before file I/O. |
| PR-QA-01 Deterministic regression suite | F-PR-002 | Critical | Tests cover path handling, session lifecycle, RCA checkpoints, exports, trace extraction, malformed input, invalid IDs, and boundary depth/answer/evidence cases. Tests use no external services or live models. |
| PR-QA-02 CI merge gate | F-PR-002/F-PR-004 | Critical | A clean checkout can install the declared dependencies and run the full test suite; CI fails on test, import, syntax, or security-regression failure. |
| PR-OBS-01 Structured lifecycle telemetry | F-PR-003 | Critical | JSON events are emitted for `request_start`, `agent_step`, `error`, and `request_end`, with timestamp, request ID, operation, outcome, duration, and session ID when available. Evidence content and PII are excluded. |
| PR-OBS-02 Correlated error contract | F-PR-003/F-PR-005 | High | Every JSON response includes a request ID. Errors use stable codes and safe messages; malformed input is 400, missing resource 404, conflict 409, oversized body 413, and unexpected failure 500. |
| PR-SEC-02 Browser security baseline | F-PR-006 | High | HTML responses send a restrictive CSP compatible with the UI. Tests verify no normal workflow produces CSP violations and no unsafe fallback is introduced without documented approval. |
| PR-UI-01 Actionable async UX | F-PR-005/F-PR-007 | High | Start, answer, demo, status, and export actions show a visible loading state within 100ms, prevent duplicate submission, restore controls in success/failure paths, and expose operation-specific guidance plus request ID on failure. |
| PR-A11Y-01 Keyboard and status accessibility | F-PR-007 | Medium | A skip link targets main content; interactive elements have visible `:focus-visible` styling; session/status/error regions use appropriate live announcements; modal focus is restored after close. |
| PR-OPS-01 Supported operating baseline | F-PR-004/F-PR-008 | High | Documentation defines supported runtime, configuration, topology, health checks, API contract, data classification, retention, prohibited uses, limitations, owner, review cadence, and rollback. Architecture diagram and reproducible dependency artifact are included. |
| PR-GOV-01 Traceability and release evidence | F-PR-001..009 | Critical | Each finding maps to a requirement, task, code/config change, test evidence, and decision record. No Critical or High item closes without deterministic evidence and named approval. |

## Out of scope

- Adding an LLM provider or changing the deterministic engine into an LLM workflow.
- Cloud deployment, cloud monitoring, tenant billing, WORM storage, authentication, or multi-user authorization without an approved target architecture.
- Cross-session learning and prompt-version rollback registry as part of this remediation release.

## Required test classes

- Positive: approved project-relative paths, valid API requests, valid session transitions, successful exports, correlated success events.
- Negative: traversal, absolute outside paths, symlink escape, malformed JSON, invalid content type, unknown resource, closed session, unsafe output path, unexpected exception.
- Boundary: project root versus parent, mixed separators, empty and maximum fields, maximum Why depth, duplicate request IDs, missing content length, concurrent session update, slow response, narrow viewport.

## Definition of done

All Critical requirements pass automated validation; High requirements have automated or reproducible browser evidence; traceability is complete; residual risks have owners and rollback triggers; and the release owner signs the integration decision.

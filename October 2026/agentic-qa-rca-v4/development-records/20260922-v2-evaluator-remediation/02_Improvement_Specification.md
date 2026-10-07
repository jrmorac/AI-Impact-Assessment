# v2 Evaluator Improvement Specification

Spec ID: SPEC-E2-20260922-01  
Status: Ready for approval  
Owner: Jose Mora / Senior Agentic Engineer

## Confirmed architecture decisions

- The release remains local, single-user, deterministic, and synthetic-data-only.
- No LLM-backed recommendation phase will be added for this release.
- Export governance will use separate preview and commit endpoints.
- GitHub Actions is the CI platform.
- Docker is not required for this release.
- Jose Mora is the named maintainer and release owner.
- Default retention is 360 days for synthetic sessions, reports, exports, and application logs.

## Current-release requirements

| Requirement | Source | Acceptance criteria |
|---|---|---|
| E2-REQ-01 CI regression gate | E2-F-001 | A clean checkout installs the declared environment, runs all unit/API/security tests, runs golden demo comparisons, and fails the build on any regression. No live network or client data is allowed. |
| E2-REQ-02 Reproducible environment | E2-F-001 | Dependency versions are reproducible from a committed lock or fully hashed requirements artifact; supported Python version and test command are documented. |
| E2-REQ-03 Export preview and approval | E2-F-002 | Separate preview and commit endpoints are implemented. Preview generates report/CSV content without filesystem mutation. Commit requires explicit approval bound to the exact session, options, target path, and content hash. |
| E2-REQ-04 Overwrite protection | E2-F-002 | Existing targets return a conflict unless explicit overwrite confirmation is supplied. Rejected writes do not truncate or replace the target. |
| E2-REQ-05 Atomic export | E2-F-002/E2-F-007 | Approved exports write atomically; interrupted or invalid writes cannot leave partial artifacts. Web and CLI paths use the same policy. |
| E2-REQ-06 Golden regression set | E2-F-003 | Why 1/3/5 demos and representative negative cases have versioned semantic expectations for status, stop depth, CAPA gating, CSV schema, and trace shape. Timestamps and paths are normalized. |
| E2-REQ-07 Local observability | E2-F-004 | Request start/end/error and planner/analyzer/validator/interactive-step events contain event name, request ID, session ID when available, step/index, outcome, duration, and safe error metadata. Tracebacks remain controlled-log-only. |
| E2-REQ-08 Architecture and operations documentation | E2-F-005 | README includes the local-only production boundary and data classification; Mermaid architecture diagram, README_OPS, version/changelog, Jose Mora as owner, review cadence, health checks, 360-day retention, and rollback are present. |
| E2-REQ-09 Evidence governance | E2-F-006 | Every applicable finding maps to requirement, task, code/config, test result, decision, owner, and residual-risk disposition. Browser evidence covers exports, Why 5, trace viewer, and revision. |
| E2-REQ-10 Package parity | E2-F-006 | Working and shareable v2 trees pass the same test IDs; package manifest and ZIP hash are recorded before distribution. |

## Future architecture requirements

| Requirement | Activation trigger | Acceptance criteria |
|---|---|---|
| E2-FUT-01 Token budget | LLM/provider introduced | Provider exposes usage; per-session and per-feature hard ceilings stop calls before budget breach; usage is logged without sensitive content; budget exhaustion is tested. |
| E2-FUT-02 Inference guardrails | Content sent to external model | Input/output filtering, PII policy, prompt-injection probes, refusal handling, and human review are enforced before model output can influence writes. |
| E2-FUT-03 LLM CI isolation | LLM phase approved | Injectable provider, deterministic mocks, network-denied CI, malformed/truncated output tests, adversarial/exfiltration suite, and no live calls. |
| E2-FUT-04 Shared deployment controls | Multi-user/cloud/regulated deployment | Authentication, authorization, intent capsule, tenant isolation, retention, monitoring, immutable audit storage, residency review, and rollback evidence pass. |

## Out of scope for this release

- Adding an LLM solely to satisfy evaluator criteria.
- Claiming token consumption or inference guardrails for a rules-only engine.
- Cloud monitoring, WORM storage, authentication, or container deployment without an approved target architecture.
- Delete-operation approval where no delete operation exists.

## Definition of done

All current-release requirements pass deterministic tests and documentation review, browser evidence is attached, both v2 packages are behaviorally equivalent, all applicable Critical/High findings are closed, future controls are recorded as conditional, and a named owner signs the release decision.

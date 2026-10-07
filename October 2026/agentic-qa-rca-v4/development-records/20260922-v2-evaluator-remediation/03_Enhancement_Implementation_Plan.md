# v2 Evaluator Enhancement Implementation Plan

Plan ID: PLAN-E2-20260922-01  
Status: Ready for implementation  
Release posture: Blocked for shared/distributable release

## Confirmed scope decisions

- Local, single-user, deterministic, synthetic-data-only release.
- No LLM-backed recommendation phase in this release.
- Separate export preview and commit endpoints.
- GitHub Actions for CI.
- Docker deferred and not required.
- Jose Mora is maintainer and release owner.
- 360-day default retention for synthetic artifacts and logs.

## Phase 0: Architecture and scope lock

Owner: Senior Agentic Engineer  
Output: applicability decision, deployment boundary, named owner, approved spec.

- Confirm the current release remains deterministic, local, file-backed, and synthetic-data-only.
- Record token/LLM controls as future gates, not current implementation tasks.
- Record the deployment boundary and owner decision in the evaluator-facing applicability document.

## Phase 1: CI, reproducibility, and golden regression

Owners: Senior Backend Engineer + Senior QA Agent

- Add a GitHub Actions workflow for syntax/import checks, unittest suite, security tests, and golden demos.
- Add a reproducible dependency artifact; keep PyYAML pinned and document the selected lock strategy. Docker is explicitly out of scope.
- Create normalized expected outputs for Why 1/3/5, negative evidence-gated cases, CAPA/ADO schemas, and agent traces.
- Add package parity and clean-checkout checks.

Exit gate: CI passes from a clean checkout with network disabled for application tests.

## Phase 2: Human-gated export integrity

Owners: Senior Backend Engineer + Senior Frontend Engineer

- Add separate preview-only and commit endpoints.
- Generate exports in memory; return content hash, target, existence, and approval token.
- Commit only after explicit approval; reject stale token, changed content, missing approval, and overwrite without confirmation.
- Use atomic writes and record export audit metadata.
- Mirror policy in CLI/export helpers.

Exit gate: positive preview/commit, cancel, stale approval, overwrite conflict, traversal, and interrupted-write tests pass.

## Phase 3: Local observability and operational controls

Owner: Senior Backend Engineer

- Emit planner/analyzer/validator and interactive Why step events with duration and session correlation.
- Add controlled traceback logging for unexpected errors and document redaction/retention.
- Add defensive fixed-step ceiling to the orchestrator and assert no unexpected extra step.
- Document synchronous request behavior and local status semantics.

Exit gate: event-schema tests and sanitized log samples pass.

## Phase 4: Documentation and governance

Owner: Senior Agentic Engineer

- Add Mermaid architecture diagram, README_OPS, and the evaluator-facing applicability document.
- Document data classification, synthetic-data restriction, retention, failure modes, rollback, owner, review cadence, version, and changelog.
- Create `docs/review/` sign-off records and complete traceability.

Exit gate: documentation review and named owner acceptance.

## Phase 5: Browser and package validation

Owners: Senior Frontend Engineer + Senior QA Agent

- Run browser checks for preview/approval/overwrite, Why 5 boundary, trace viewer population, revision, CSP, keyboard, and errors.
- Run identical tests against working and shareable v2.
- Rebuild ZIP and record manifest/hash.

Exit gate: no applicable Critical/High findings remain; release decision signed.

## CI gate design

1. Static: syntax/import, dependency integrity, secret scan, forbidden dynamic execution, required docs.
2. Rules-only: full unit/API/security suite with synthetic fixtures.
3. Golden: canonicalized demo outputs and schemas.
4. Browser: export approval, Why boundary, trace viewer, revision, CSP/accessibility.
5. Package: parity manifest, clean packaging, ZIP contents/hash.
6. Future LLM gate: only when enabled; mocked provider, network denied, token/iteration ceilings, malformed output and adversarial probes.

## Block conditions

- No CI run from a clean checkout.
- Export can overwrite without approval.
- Golden output or browser evidence is absent.
- Working/shareable v2 behavior diverges.
- Traceability or owner sign-off is incomplete.
- An LLM/shared deployment is enabled without the future controls in the specification.

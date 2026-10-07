# Enhancement Implementation Plan — v4 Evaluator Remediation

Owner: QA Engineering Team / Senior Agentic Engineer

## Sequence

1. Create `agentic-qa-rca-v4/` and `agentic-qa-rca-shareable-v4/` as full copies of the v3 packages (owner action via `robocopy`, completed 2026-10-07).
2. Apply F-001, F-003, F-004, F-005, F-006 as direct documentation edits in `agentic-qa-rca-v4/` (orchestrator role), then mirror identically into `agentic-qa-rca-shareable-v4/`.
3. Bump `VERSION` to `4.0.0` and add a `4.0.0` `CHANGELOG.md` entry in both packages (F-002, partial — git tag remains a pending human action).
4. Delegate F-007 and F-008 to Senior Backend Engineer, scoped to `agentic-qa-rca-v4/` only.
5. Delegate F-009 to Senior Frontend Engineer, scoped to `agentic-qa-rca-v4/web/index.html` only.
6. Orchestrator verifies backend/frontend deliverables (file-existence checks, `get_errors` static validation, code reading) and syncs the exact same changes into `agentic-qa-rca-shareable-v4/` via matched before/after text diffs against the shareable copy's pre-fix baseline.
7. Produce governance artifacts (this directory) and the integration decision record.

## Backend delegation (F-007, F-008)

- Scope: `src/orchestrator.py`, `src/agents.py`, `src/interactive_rca.py`, new `prompts/*.yaml`, new tests.
- Constraints given to the agent: deterministic-only (no LLM calls), synthetic data only, do not touch Tier 3 items, add/update unit tests for positive/negative/boundary coverage, run `python -m compileall` and `unittest discover` if terminal access is available.
- Result: implemented correctly (verified by direct code read and `get_errors`); the agent's own terminal/test-execution access was not confirmed in its final report, so test execution evidence is treated as **unverified** pending a human test run (see `08_Code_Review_Findings.md`).

## Frontend delegation (F-009)

- Scope: `web/index.html` only, additive accessibility/UX polish, no CSP or API contract changes.
- Result: implemented correctly per the agent's final report and confirmed by direct code read (`errorRemediation` map, `markFieldInvalid`, `aria-describedby` additions, expanded Escape handling).

## Shareable package sync

- Backend: 3 targeted diff sets applied to `agentic-qa-rca-shareable-v4/src/{orchestrator,agents,interactive_rca}.py`, matched against the verified pre-fix baseline (confirmed identical to v3 before editing). 2 new YAML prompt files and 1 pre-existing YAML file created. 2 new test files copied verbatim.
- Frontend: 13 targeted diffs applied to `agentic-qa-rca-shareable-v4/web/index.html`, matched against the verified pre-fix baseline.
- Verification: `grep_search` for `aria-describedby`, `errorRemediation`, `markFieldInvalid`, `applyCheckpointFeedback` confirms parity between the two packages (46 matches each, same line-for-line structure).

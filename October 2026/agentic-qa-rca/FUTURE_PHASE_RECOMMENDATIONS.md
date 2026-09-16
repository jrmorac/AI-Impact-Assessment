# Future Phase Recommendations (Prototype)

## Purpose

This document captures improvement recommendations identified during the August 2026 code review.
The current solution is still a prototype, so these actions are intentionally planned for a later phase instead of immediate implementation.

## Context Reference

Source context and continuity notes:
- October 2026/context/SESSION_HANDOFF_CONTEXT.md

This recommendation set aligns with the current decision to prioritize pilot validation and adoption evidence before additional feature or hardening work.

## Recommended Future Improvements

### 1) API Path Safety Hardening (High Priority)

Problem:
- The local web API resolves caller-provided paths and currently allows absolute or external paths.
- In a future multi-user or broader network scenario, this could enable unintended file access outside the project boundary.

Future-phase action:
- Restrict all API-resolved paths to the project root or explicit allowlisted subfolders.
- Reject path traversal and absolute paths outside allowed scope.
- Split validation into read-path and write-path policies.

Expected benefit:
- Improves baseline security posture and prevents accidental or malicious file access outside the prototype scope.

### 2) Remove Duplicate Legacy Logic in Main Module (Medium Priority)

Problem:
- Legacy helper generators in src/main.py overlap with current workflow-agent implementations.
- This creates maintainability risk if one path is updated and the other is forgotten.

Future-phase action:
- Keep a single source of truth in workflow agents and orchestrator modules.
- Remove or archive duplicate legacy generator functions from src/main.py.
- Add a brief architecture note explaining canonical code paths.

Expected benefit:
- Reduces drift risk, simplifies maintenance, and improves long-term code clarity.

### 3) Add Automated Test Coverage for Decision Gates and API Flow (Medium Priority)

Problem:
- Core RCA gate decisions and session transitions are critical behavior, but there is no formal automated test suite.
- Prototype changes can unintentionally alter stop/continue logic.

Future-phase action:
- Add unit tests for RCA checkpoint decisions:
  - needs_more_evidence
  - stop_root_cause_confirmed
  - stop_max_depth_reached
- Add API tests for start/answer/status/export happy paths and invalid input handling.
- Add one deterministic end-to-end test using synthetic inputs.

Expected benefit:
- Protects core workflow behavior and increases confidence for team adoption and future refactoring.

### 4) Add Checkpoint Preview Assist Mode (High Priority)

Problem:
- The RCA flow currently requires manual trial-and-error to discover whether an answer is likely to continue, stop, or be rejected for weak evidence.
- Users submit answers without seeing which checkpoint conditions are currently failing.

Future-phase action:
- Add a non-mutating checkpoint preview capability for both Web UI and CLI.
- Return predicted decision, pass/fail status per checkpoint condition, and targeted remediation guidance before answer submission.
- Surface this in the UI as a live panel that updates when answer text, evidence references, or flags change.
- Keep final checkpoint decision unchanged and deterministic at submit time.

Expected benefit:
- Reduces unnecessary iteration in the Why loop.
- Improves answer quality and evidence completeness earlier in the flow.
- Lowers dependency on manual interpretation of gate rules.

### 5) Add Suggest Answer Assist Mode (High Priority)

Problem:
- The current workflow depends heavily on users to draft each Why answer from scratch.
- Existing templates and role hints are static and do not adapt to prior case patterns.

Future-phase action:
- Add suggestion generation for both Web UI and CLI with 2 to 3 ranked draft answers per Why step.
- Use retrieval-grounded suggestions first, based on similar prior RCA sessions and evidence patterns.
- Allow optional model-based suggestions behind feature flags only, with strict fallback to retrieval or template suggestions when unavailable.
- Return confidence, rationale, evidence references, and provenance for each suggestion source.
- Require explicit human accept, edit, or reject action before any suggestion is used.

Expected benefit:
- Reduces analyst drafting effort and session completion time.
- Improves consistency of answer structure and causal quality.
- Increases practical autonomy while preserving governance and auditability.

### 6) Add Assist Telemetry and Learning Signals (Medium Priority)

Problem:
- Suggestion quality cannot be improved reliably without structured feedback on what users accept, edit, or reject.
- Current logs are not yet sufficient for closed-loop tuning of assist behavior.

Future-phase action:
- Log assist events with source, confidence, selected option, and user decision outcome.
- Track checkpoint preview prediction versus final submitted decision.
- Record assist metrics in sprint tracking for accepted suggestions, flagged suggestions, and time-to-closure impact.
- Keep telemetry lightweight, append-only, and compatible with current evidence workflows.

Expected benefit:
- Enables measurable improvement of assist quality over time.
- Supports defensible D3 and D4 evidence with operational metrics.
- Creates a reliable foundation for future adaptive tuning.

## Suggested Implementation Sequence (Future Phase)

1. Implement API path-safety constraints.
2. Add checkpoint preview assist mode in Web UI and CLI.
3. Add suggest-answer assist mode with retrieval-first behavior.
4. Enable optional model-based suggestion path behind feature flags with mandatory fallback.
5. Consolidate and remove duplicated generation logic.
6. Add automated unit/API/end-to-end test baseline, including assist-enabled paths.

## Notes

- No production data assumptions are required for these improvements.
- All validation should continue using synthetic/demo inputs unless scope changes are explicitly approved.

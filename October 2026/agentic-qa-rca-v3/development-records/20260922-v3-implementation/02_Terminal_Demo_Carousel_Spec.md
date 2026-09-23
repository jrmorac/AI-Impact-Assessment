# Terminal Demo Carousel Specification

Date: 2026-09-22  
Finding: Completed demos initially show a misleading live `Current Why` instead of the final recorded Why node.

## Root cause

The UI resets `whyHistoryIndex` to `-1` after demo loading. Terminal RCA statuses were not included in `isClosedSession()`, so `renderSnapshot()` displayed `session.current_question` and default checkbox state instead of selecting the final `why_chain` item.

## Requirements

- Completed statuses include `root_cause_confirmed`, `target_depth_reached`, `max_depth_reached`, `closed`, and `completed`.
- When a terminal session has a non-empty Why chain and no selected history item, the UI selects the final recorded node.
- Why 1, Why 3, and Why 5 demos display `Why N of N (final)` on initial load.
- The final node restores its answer, evidence, controllable, resolved, and prevents-recurrence values.
- The Next arrow is enabled while a later recorded Why exists, including terminal Why 1 and Why 3 demos.
- The Next arrow is disabled only at the final recorded Why for terminal sessions.
- Active `awaiting_answer` and `needs_more_evidence` sessions retain the live/current behavior.
- Explicit advanced continuation remains available only when the session declares it.

## Out of scope

- Changes to RCA checkpoint decisions or session persistence.
- Changes to advanced continuation policy.
- Changes to original v1/v2 folders.

## Acceptance tests

- Why 1 demo opens on its only recorded Why.
- Why 3 demo opens on Why 3 and cannot navigate to a live fourth item.
- Why 5 demo opens on Why 5 and Next is disabled.
- From Why 1 or Why 2 in a completed Why 3 demo, Next advances to the next recorded Why.
- Final node checkbox values match the stored node.
- Active manual session still displays the live current question.
- Both working and shareable v3 UIs contain equivalent logic.

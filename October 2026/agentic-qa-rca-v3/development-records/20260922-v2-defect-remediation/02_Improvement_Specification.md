# Improvement Specification

Spec ID: SPEC-V2-20260922-01  
Status: Ready for implementation  
Owner: Senior Agentic Engineer

## Requirements

| Requirement | Finding | Acceptance criteria |
|---|---|---|
| V2-EXP-01 | V2-F-001 | CAPA and ADO exports succeed with the displayed default paths, return HTTP 200, create valid CSV files under `evidence/capa_exports`, and open their previews. |
| V2-EXP-02 | V2-F-001/V2-F-006 | Traversal, outside-root, empty, invalid provider, and invalid variant inputs fail with stable actionable errors and create no unauthorized file. |
| V2-ROUTE-01 | V2-F-002 | `/api/run-demo` dispatches at the same level as other POST routes and returns session, RCA, CAPA, ADO, and batch-report paths. |
| V2-TRACE-01 | V2-F-002/V2-F-005 | After bootstrap, demo, or refresh, the newest valid JSON batch report appears in the selector; selecting it populates defect IDs and loading a defect renders its trace. Invalid or Markdown reports show a deterministic empty/error state without stale trace data. |
| V2-WHY-01 | V2-F-004 | Why 4 may advance to Why 5. In normal mode, a completed Why 5 cannot create or navigate to Why 6. If advanced depth is retained, it requires explicit configuration or control and is bounded by max depth. |
| V2-SUBMIT-01 | V2-F-003 | A valid answer in `awaiting_answer` appends exactly one node and advances. Empty, short, causally vague, or evidence-free answers preserve the current form and expose validation feedback. |
| V2-SUBMIT-02 | V2-F-003 | A `needs_more_evidence` session enables revision of the current node, replaces that node without changing chain length, and recalculates status/checkpoint. |
| V2-SUBMIT-03 | V2-F-003 | Revising a selected historical node uses its explicit Why index, preserves the question/index, and never appends a duplicate. Closed sessions reject answer and revise operations. |
| V2-STATE-01 | V2-F-003/V2-F-004 | Carousel navigation distinguishes historical review from the live answer state; Next is disabled at the final allowed Why and does not silently reset to a new answer. |

## Out of scope

- Changes to the RCA analysis heuristics beyond target-depth/state handling.
- New LLM, cloud, database, authentication, OTel, or WORM capabilities.
- Changes to original v1 folders.

## Required test classes

- Positive: demo route, CAPA export, ADO standard/expanded export, trace selection/loading, valid answer, valid revision.
- Negative: unauthorized export path, invalid provider/variant, malformed report, unknown defect, closed-session answer/revise, duplicate submit.
- Boundary: Why 4 to Why 5, Why 5 stop/continue behavior, max depth, empty output fields, long evidence lists, report refresh preserving valid selection.

## Definition of done

All High findings have passing API/UI tests; the working and shareable v2 packages contain equivalent fixes; traceability maps finding to code and evidence; and a browser smoke run confirms the four reported workflows.

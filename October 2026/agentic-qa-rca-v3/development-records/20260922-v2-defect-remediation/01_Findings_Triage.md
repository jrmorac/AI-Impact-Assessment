# Findings Triage

Date: 2026-09-22  
Source: v2 user testing, source inspection, Senior Backend Engineer, Senior Frontend Engineer, and Senior QA Agent reviews.

## High findings

| ID | Finding | Root cause | Scope |
|---|---|---|---|
| V2-F-001 | CAPA and ADO Test Case export buttons fail with the displayed defaults. | UI writes to `evidence/capa_exports`, but the backend write allowlist excludes that directory. | Both v2 packages |
| V2-F-002 | Demo-driven Agent Trace Viewer population is unavailable. | `/api/run-demo` is nested after the quick-plan return in `src/web_app.py`, so the route is unreachable and no batch report is returned. | Both v2 packages |
| V2-F-003 | Submit Answer cannot reliably revise gated or previously answered Why nodes. | UI disables submit outside exact `awaiting_answer`, clears revise state during render, and backend revision searches the post-answer `current_why_index` rather than an explicitly selected node. | Both v2 packages |

## Medium findings

| ID | Finding | Root cause | Scope |
|---|---|---|---|
| V2-F-004 | The carousel can expose Why 6 after a Why 5 continuation. | `target_depth: 5` is configured but checkpoint logic only enforces `max_depth: 8`; navigation also resets from the last item to the live state. | Both v2 packages |
| V2-F-005 | Trace selectors and trace content have incomplete refresh semantics. | Report refresh depends on reachable batch output; refresh-only trace loading populates defect options but intentionally leaves the trace panel unchanged. | Both v2 packages |
| V2-F-006 | Export option validation is inconsistent. | CAPA/ADO outputs are required by the backend despite UI defaults, and provider/variant values are not explicitly validated. | Both v2 packages |

## Applicability and assumptions

- The default normal workflow targets five Whys. Deeper analysis may remain available only through an explicit advanced-mode decision; it must not appear accidentally through the carousel.
- Batch reports are JSON files under `data/output` containing `analysis[].agent_trace`; Markdown RCA reports are not trace-compatible and should not populate the batch report selector.
- Existing v2 security tests do not cover exports, demo dispatch, trace refresh, Why depth, or revision transitions.

## Severity conclusion

Release is blocked by V2-F-001, V2-F-002, and V2-F-003 because they break core deliverables or correction workflows. V2-F-004 through V2-F-006 require regression coverage and should close in the same change set.

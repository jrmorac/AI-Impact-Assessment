# Agent Trace Viewer All-Workflows Specification

Date: 2026-09-22  
Decision: Extend trace visibility beyond demos.

## Problem

The Agent Trace Viewer currently populates reliably after demo runs because `run_demo()` creates a batch JSON report with `analysis[].agent_trace`. Manual Start RCA and Quick Plan workflows create sessions and Markdown reports but do not create a trace-compatible batch report, leaving the report and defect selectors empty in a clean/shareable package.

## Requirements

- Start RCA creates a trace-compatible batch JSON report and returns `batch_report_path`.
- Quick Plan creates a trace-compatible batch JSON report and returns `batch_report_path`.
- The Web UI refreshes the report selector, selects the returned report, populates defect IDs, and loads the trace automatically after Start or Quick Plan.
- Demo behavior remains unchanged.
- Batch reports remain synthetic, local, and deterministic except for documented timestamps and paths.
- Invalid or empty trace reports continue to show a safe empty state.

## Acceptance criteria

- Start Session with a synthetic input produces a non-empty batch report selector entry.
- Quick Plan produces a non-empty batch report selector entry.
- Selecting each report populates its defect IDs and planner/analyzer/validator trace.
- Demo trace behavior remains passing.
- Working and shareable v3 packages contain equivalent behavior.

## Out of scope

- LLM tracing, cloud telemetry, or external monitoring.
- Changing RCA/session decisions.
- Adding trace data to Markdown reports.

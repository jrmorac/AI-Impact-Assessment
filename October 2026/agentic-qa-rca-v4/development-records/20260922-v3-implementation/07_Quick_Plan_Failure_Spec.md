# Quick Plan Failure Specification

Date: 2026-09-22  
Finding: Web UI Quick Plan requests failed with `Failed to fetch`.

## Root cause

`run_guided_rca()` stopped only for `root_cause_confirmed` and `max_depth_reached`. When a valid Quick Plan reached the configured normal target depth with no confirmed stop flags, the session entered `target_depth_reached`, but the loop continued and `_next_quick_step()` attempted to read a sixth answer. The resulting exception terminated the request before the UI received a response.

## Requirements

- Quick Plan execution must stop when status is `target_depth_reached`.
- Quick Plan execution must continue to support `root_cause_confirmed` and `max_depth_reached` termination.
- A finite plan must never require an extra answer after a terminal status.
- The HTTP endpoint must return a structured response for a successful target-depth completion.
- The fix must be mirrored in working and shareable v3 packages.

## Acceptance tests

- A five-answer non-closing Quick Plan returns successfully with `target_depth_reached`.
- A plan that confirms root cause still returns `root_cause_confirmed`.
- Existing demo and Quick Plan regression suites pass.
- The UI receives `session`, `report_path`, and `batch_report_path` after completion.

# Integration Decision Record

Record ID: IDR-V2-20260922-01  
Date: 2026-09-22  
Decision: **Conditionally Approve for continued validation; production release remains blocked**

## Changes implemented

- `/api/run-demo` is reachable.
- CAPA and ADO exports support the documented synthetic output directory and validate options.
- Normal Why flow stops at configured target depth 5 unless explicit advanced continuation is requested.
- Revision uses an explicit Why index, requires the correct session state, and replaces the selected node without duplication.
- Trace report and defect selectors refresh and auto-load from valid batch JSON reports.

## Validation evidence

- Working v2: 10 tests, 9 passed, 1 skipped because Windows symlink creation privilege was unavailable.
- Shareable v2: 13 tests, 12 passed, 1 skipped for the same environment limitation.
- No test failures or errors.
- Static diagnostics are clean in changed Python, JavaScript/HTML, and test files.

## Open evidence

- Browser smoke evidence is still required for exports, Why 5 navigation, trace viewer population, and revise submission.
- The shareable ZIP must be rebuilt from the corrected package and verified.
- Final release-owner sign-off remains pending.

## Decision rationale

The reported runtime defects are addressed and covered by focused synthetic tests. Production approval remains blocked until browser evidence, package verification, and release governance gates are complete.
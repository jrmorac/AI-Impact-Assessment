# Report Export Preview Fix

Date: 2026-09-22  
Finding: Report export did not open the preview modal on the first click in the v3 Web UI. CAPA and ADO Test Case previews were working.

## Root cause

The Report button used the legacy `/api/export-report` wrapper and waited for a session/report-list refresh before opening the modal. CAPA and ADO flows were already aligned with the explicit v3 preview/commit contract.

## Fix

Updated both v3 Web UIs so Report export:

1. Calls `POST /api/export-preview` with `kind: report`.
2. Commits the exact preview through `POST /api/export-commit` using the returned content hash.
3. Opens the preview modal from the committed report path immediately.
4. Refreshes report/session lists after the modal is opened.

The working and shareable v3 packages were updated identically.

## Validation

- Working v3: 23 tests discovered; 22 passed, 1 symlink test skipped because Windows symlink creation privilege was unavailable.
- Shareable v3: 26 tests discovered; 25 passed, 1 symlink test skipped for the same environment limitation.
- No test failures or errors.
- Browser confirmation of the first-click modal behavior remains a manual UI evidence item.

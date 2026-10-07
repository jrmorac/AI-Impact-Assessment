# Manual Trace PATH_NOT_ALLOWED Fix

Date: 2026-09-22  
Finding: Start Session and Quick Plan returned `PATH_NOT_ALLOWED` after manual trace-report generation was added.

## Root cause

The shared manual trace helper writes `evidence/evidence_log.csv` through `_resolve_path(..., access="write")`. The v3 write allowlist permitted output reports, sessions, RCA reports, and CAPA exports, but not the exact evidence log file.

## Fix

Both v3 web servers now allow the exact file `evidence/evidence_log.csv` for the batch runner while keeping the evidence directory itself out of the write allowlist. The selected input file was not the source of the error.

## Validation

- Added a regression test for the default evidence-log write path in both packages.
- Working web security suite: 6 passed, 1 Windows symlink skip.
- Shareable web security suite: 8 passed, 1 Windows symlink skip.
- Full-suite validation follows after this record update.

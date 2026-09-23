# Operations Runbook

Version: 3.0.0  
Maintainer and release owner: Jose Mora  
Data classification: Internal synthetic/non-sensitive QA artifacts  
Default retention: 360 days

## Supported boundary

This application is a local, single-user, deterministic QA workflow. Do not expose it to production, customer data, shared multi-user traffic, or external networks. Do not add an LLM provider without a new architecture and security review.

## Start and stop

```text
python src/web_app.py --host 127.0.0.1 --port 8787
```

Stop with `Ctrl+C`. The application uses synchronous HTTP requests and file-backed JSON sessions.

## Health checks

- `GET /api/health` returns `status=ok`.
- `GET /api/bootstrap` returns available synthetic contexts, inputs, sessions, and batch reports.
- Request and response logs are newline-delimited JSON on stdout.

## Validation commands

```text
python -m unittest discover -s tests -v
```

GitHub Actions runs the same suite on Python 3.10 and 3.11, plus golden regression checks and import/compile validation.

Quick Plans are retained for CLI, GitHub Actions, golden regression, and QA automation. They are not exposed in the Web UI; use `Run Demo Case` for bundled repeatable examples.

## Export governance

Exports use separate preview and commit operations. Preview must not mutate files. Commit requires explicit approval bound to the generated content hash, session/options, and target path. Existing files require explicit overwrite confirmation. Writes are atomic.

## Failure modes

- `PATH_NOT_ALLOWED`: requested path is outside the configured allowlist.
- `EXPORT_APPROVAL_REQUIRED`: commit lacks explicit approval or a valid preview.
- `EXPORT_CONFLICT`: target exists and overwrite was not confirmed.
- `INVALID_REQUEST`: malformed request or invalid export option.
- Unexpected errors return a safe request ID; traceback details remain in controlled logs only.

## Retention and recovery

Synthetic sessions, reports, exports, and application logs have a default 360-day retention period. Retention is local and must be reviewed before any deployment outside the controlled workspace. Preserve synthetic evidence and the release manifest for rollback investigations.

## Rollback

If export governance, session transitions, or trace loading regress, stop distribution and use the last approved v2 package. Do not delete or overwrite evidence during rollback. Record the failing test, package hash, and owner decision.

## Review cadence

Jose Mora reviews the local operating boundary and retention policy at least every six months and before any shared, cloud, regulated, or LLM-backed deployment.

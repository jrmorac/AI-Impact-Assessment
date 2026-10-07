# Trace Viewer All-Workflows Implementation

Date: 2026-09-22  
Status: Implemented  
Owner: Jose Mora

## Change

The Agent Trace Viewer previously populated automatically only after demos because demos generated a batch JSON report containing `analysis[].agent_trace`. Manual Start RCA and Quick Plan now generate the same batch-compatible report and return `batch_report_path`.

## Backend

Both v3 `src/web_app.py` files now:

- Generate `data/output/report_<session>.json` through the existing deterministic batch runner.
- Return `batch_report_path` from Start RCA and Quick Plan responses.
- Preserve the existing session Markdown report and interactive workflow.

## Frontend

Both v3 Web UIs now:

- Refresh report options after Start RCA and Quick Plan.
- Select the returned batch report.
- Populate defect IDs and load the planner/analyzer/validator trace automatically.
- Preserve existing demo trace behavior.

## Validation

- Working v3: 27 tests, 26 passed, 1 Windows symlink skip.
- Shareable v3: 29 tests, 28 passed, 1 Windows symlink skip.
- No failures or errors.
- Browser validation remains recommended for manual Start RCA and Quick Plan trace population.

# Quick Plan Web UI Boundary

Date: 2026-09-22  
Decision: Quick Plans are automation/QA infrastructure, not a primary Web UI workflow.

## Change

Removed from both v3 Web UIs:

- Quick Plan selector
- Run Quick Plan button
- Quick Plan browser handler
- Quick Plan bootstrap population
- Demo-only Quick Plan selector assignment

## Preserved

Quick Plans remain available through:

- CLI execution via `src/main.py`
- Demo execution, which uses bundled Quick Plans internally
- GitHub Actions and unittest golden regression
- Automation and QA workflows

## Validation

- Working v3 UI boundary tests: 3 passed.
- Shareable v3 UI boundary tests: 2 passed.
- Working v3 full suite: 32 tests, 31 passed, 1 Windows symlink skip.
- Shareable v3 full suite: 33 tests, 32 passed, 1 Windows symlink skip.
- No failures or errors.

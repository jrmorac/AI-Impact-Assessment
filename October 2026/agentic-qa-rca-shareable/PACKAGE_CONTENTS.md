# Package Contents

This package was prepared for QA team sharing and local validation.

## Folder Map

- `src/`: Python implementation (CLI, RCA, agents, orchestrator)
- `web/`: Local web UI
- `project-context/`: Reusable project/context templates
- `data/input/`: Synthetic sample inputs plus three demo cases (`Why 1`, `Why 3`, and `Why 5`) and their quick plans
- `data/output/`: Output target folder (initially empty)
- `evidence/`: Runtime evidence/export target folders (initially empty)
- `metrics/`: Placeholder for local metric tracking

## Utility Scripts Included

- `check_env.py`: Cross-platform first-run environment validation (Python/version/dependency/files/port)
- `start_local.py`: Cross-platform local startup with automatic port fallback
- `package_shareable.py`: Cross-platform clean timestamped zip package in sibling `dist/`
- `check-env.sh`: macOS/Linux wrapper for `check_env.py`
- `start-local.sh`: macOS/Linux wrapper for `start_local.py`
- `package-shareable.sh`: macOS/Linux wrapper for `package_shareable.py`
- `check-env.ps1`, `start-local.ps1`, `package-shareable.ps1`: Optional Windows PowerShell scripts

## Demo Contents

- `demo_cases.json`: Three synthetic RCA cases with variable 5-Whys depth.
- `demo_quick_plan_why1.json`: Stops at Why 1.
- `demo_quick_plan_why3.json`: Stops at Why 3.
- `demo_quick_plan_why5.json`: Stops at Why 5.
- `demo-run`: Generates an RCA report, CAPA CSV, and ADO Test Case CSV automatically.

The web UI refreshes defect IDs when the input file changes, provides Why history navigation with restored answers and decision flags, and previews generated export content before dismissal.

## Why this package is clean

- Historical outputs and development traces are excluded.
- Only runtime code, templates, demo inputs, and clean synthetic samples are included.
- Output/evidence folders exist but start empty for each team.

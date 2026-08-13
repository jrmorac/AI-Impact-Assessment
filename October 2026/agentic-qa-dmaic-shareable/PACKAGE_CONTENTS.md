# Package Contents

This package was prepared for QA team sharing and local validation.

## Folder Map

- `src/`: Python implementation (CLI, RCA, agents, orchestrator)
- `web/`: Local web UI
- `project-context/`: Reusable project/context templates
- `data/input/`: Minimal synthetic sample inputs
- `data/output/`: Output target folder (initially empty)
- `evidence/`: Runtime evidence/export target folders (initially empty)
- `metrics/`: Placeholder for local metric tracking

## Utility Scripts Included

- `check-env.ps1`: First-run environment validation (Python/version/dependency/files/port)
- `start-local.ps1`: One-command local startup with automatic port fallback
- `package-shareable.ps1`: Generates clean timestamped zip package in sibling `dist/`

## Why this package is clean

- Historical outputs and development traces are excluded.
- Only runtime code + templates + minimal synthetic samples are included.
- Output/evidence folders exist but start empty for each team.

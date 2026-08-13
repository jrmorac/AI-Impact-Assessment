# Agentic QA DMAIC Assistant (Shareable Package)

This is a clean, shareable build of the RCA tool for QA teams.

## Included

- Core CLI + RCA engine
- Local web UI (`src/web_app.py`, `web/index.html`)
- Agent orchestration (`src/orchestrator.py` + `src/workflow_agents/`)
- Context templates (`project-context/`)
- Minimal synthetic input samples (`data/input/`)

## Not Included (intentionally cleaned)

- Historical session files
- Generated reports/exports
- Working evidence logs from development
- Temporary or local runtime artifacts

## Quick Start

1. One-command local startup (recommended):

```text
powershell -ExecutionPolicy Bypass -File .\start-local.ps1
```

This runs environment checks and starts the web app on the first available port from `8787`.

Optional flags:

```text
powershell -ExecutionPolicy Bypass -File .\start-local.ps1 -DryRun
powershell -ExecutionPolicy Bypass -File .\start-local.ps1 -SkipCheck
```

2. Run first-time environment check only:

```text
powershell -ExecutionPolicy Bypass -File .\check-env.ps1
```

3. Install dependencies:

```text
pip install -r requirements.txt
```

4. Run batch analysis:

```text
python src/main.py --context project-context/baseline-project.yaml --input data/input/synthetic_defects_sprint1.json --output data/output/report_sprint1.json
```

5. Run local UI manually:

```text
python src/web_app.py --host 127.0.0.1 --port 8787
```

Open:

```text
http://127.0.0.1:8787
```

## Create Shareable Zip (One Command)

From this folder, run:

```text
powershell -ExecutionPolicy Bypass -File .\package-shareable.ps1
```

The script creates a timestamped zip in the sibling `dist/` folder and excludes local runtime outputs.

## Included Utility Scripts

- `check-env.ps1`: Validates Python, required files, PyYAML import, and local port readiness.
- `start-local.ps1`: Runs checks and launches the web app on the first available port.
- `package-shareable.ps1`: Builds a clean timestamped zip for teammate distribution.

## Key CLI Commands

Start RCA:

```text
python src/main.py start-rca --context project-context/baseline-project.yaml --input data/input/synthetic_defects_with_evidence.json --defect-id PRJ-DEF-201 --session evidence/rca_sessions/prj-def-201.json
```

Answer current Why:

```text
python src/main.py answer-rca --session evidence/rca_sessions/prj-def-201.json --answer "Because ..." --evidence-ref "artifact-1" --controllable
```

Check status:

```text
python src/main.py status-rca --session evidence/rca_sessions/prj-def-201.json
```

Export RCA report:

```text
python src/main.py export-rca-report --session evidence/rca_sessions/prj-def-201.json --output evidence/rca_reports/prj-def-201.md
```

Export CAPA CSV:

```text
python src/main.py export-capa-csv --session evidence/rca_sessions/prj-def-201.json --output evidence/capa_exports/prj-def-201-ado.csv --provider ado
```

Export ADO Test Cases CSV:

```text
python src/main.py export-ado-testcases-csv --session evidence/rca_sessions/prj-def-201.json --output evidence/capa_exports/prj-def-201-ado-testcases.csv
```

## Team Handoff Notes

- Use only synthetic/non-sensitive data.
- Keep context files project-specific in `project-context/`.
- Share resulting CSV/report artifacts through your normal QA workflow (ADO/Jira/Confluence).

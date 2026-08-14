# Agentic QA RCA Assistant (Shareable Package)

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

## Preferred workflow: Web UI

Start the local web UI from this folder:

```text
powershell -ExecutionPolicy Bypass -File .\start-local.ps1
```

The script runs environment checks and starts the web app on the first available port from `8787`. Open the URL shown in the terminal, normally `http://127.0.0.1:8787`.

Use the UI for the complete workflow:

1. Select a context, input file, and defect ID.
2. Select `Run Demo Case` for the bundled `Why 1`, `Why 3`, or `Why 5` examples, or select `Start RCA Session` for a manual case.
3. Answer each Why and attach evidence references.
4. Review the session status and root-cause report.
5. Use `Export Report`, `Export CAPA CSV`, and `Export ADO TestCase CSV` to generate the deliverables.
6. Use `New Session` before starting another analysis.

The demo action generates the RCA report, CAPA tasks, and ADO test cases automatically. Manual sessions can export the same artifacts from the export panel.

### Which UI action should I use?

- `Run Demo Case`: recommended for demonstrations; loads a bundled case and completes the flow automatically, including RCA, CAPA, and Test Case outputs.
- `Start RCA Session`: recommended for a real or custom case; answer each Why manually and export the artifacts from the UI when finished.
- `Run Quick Plan`: optional; runs a selected predefined answer plan against the current input. It is useful for repeatable tests, not required for normal use.

Optional flags:

```text
powershell -ExecutionPolicy Bypass -File .\start-local.ps1 -DryRun
powershell -ExecutionPolicy Bypass -File .\start-local.ps1 -SkipCheck
```

## CLI fallback and automation

The terminal commands below are secondary options for automation, CI, or advanced users. They are not required for normal use.

Run the first-time environment check only:

```text
powershell -ExecutionPolicy Bypass -File .\check-env.ps1
```

Install dependencies:

```text
pip install -r requirements.txt
```

Run batch analysis:

```text
python src/main.py --context project-context/baseline-project.yaml --input data/input/synthetic_defects_sprint1.json --output data/output/report_sprint1.json
```

Run the UI manually, if needed:

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

## Demo Run

The package includes three synthetic demo cases that show variable 5-Whys depth:

- `why1`: simple case that confirms at Why 1
- `why3`: moderate case that confirms at Why 3
- `why5`: complex case that confirms at Why 5

Run a demo directly from this folder:

```text
python src/main.py demo-run --case why3
```

The command loads the matching demo input and quick plan, creates a new timestamped session when `--session` is omitted, and exports three artifacts: the RCA report, an ADO-compatible CAPA CSV, and an ADO-compatible Test Case CSV. The web UI exposes the same flow through `Run Demo Case`.

Use `New Session` in the web UI before starting another manual analysis. It clears the active session path so the next start creates a fresh session. Existing session files remain available in the session list for review.

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

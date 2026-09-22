# Agentic QA RCA Assistant (Shareable Package)

This is a clean, shareable build of the RCA tool for QA teams.

**Architecture and evaluator applicability:** See [ARCHITECTURE_AND_EVALUATOR_APPLICABILITY.md](ARCHITECTURE_AND_EVALUATOR_APPLICABILITY.md) for the deterministic, LLM-free release boundary, applicable controls, deferred LLM requirements, data handling, retention, and release governance.

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
- Development records under `October 2026/agentic-qa-rca/development-records/`
- Temporary or local runtime artifacts

Development records are internal engineering artifacts and are intentionally excluded from this shareable package.

## Preferred workflow: Web UI

Start the local web UI from this folder:

```text
python start_local.py
```

macOS/Linux alternative:

```text
bash ./start-local.sh
```

The script runs environment checks and starts the web app on the first available port from `8787`. Open the URL shown in the terminal, normally `http://127.0.0.1:8787`.

Security note: no `ExecutionPolicy Bypass` command is required.

Use the UI for the complete workflow:

1. Select a context, input file, and defect ID. Changing the input file refreshes the available defect IDs automatically.
2. Select `Run Demo Case` for the bundled `Why 1`, `Why 3`, or `Why 5` examples, or select `Start RCA Session` for a manual case.
3. Answer each Why and attach evidence references. Use the back/next controls to review the recorded question-and-answer history; the selected answer, evidence, and decision flags are restored in the form.
4. Review the session status and root-cause report.
5. Use `Export Report`, `Export CAPA CSV`, and `Export ADO TestCase CSV` to generate the deliverables. Each export opens a confirmation preview with the generated file content and an `OK` button.
6. Use `New Session` before starting another analysis.

The demo action generates the RCA report, CAPA tasks, and ADO test cases automatically. Manual sessions can export the same artifacts from the export panel.

## Web UI User Manual

### Start the application

1. Open a terminal in the shareable package folder.
2. Run `python start_local.py`.
3. Open the localhost URL printed in the terminal. The launcher normally uses `http://127.0.0.1:8787`, but it selects another available port when necessary.
4. Keep the terminal running while using the app. Stop the server with `Ctrl+C` when finished.

The application runs locally. Use synthetic or non-sensitive QA data only.

### Start a manual RCA session

1. In **Context file**, choose the project profile for the run.
2. In **Input file**, choose a JSON file containing a list of defect objects.
3. Choose a **Defect ID**. The dropdown is populated from the selected input file's `defect_id` fields. If the ID is not listed, enter it in **Manual Defect ID**.
4. Choose a role: `qa`, `dev`, `sre`, or `release-manager`. The role changes the answer guidance shown during the RCA.
5. Optionally enter a session path. Leave it blank to create a timestamped session under `evidence/rca_sessions/`.
6. Select **Start RCA Session**.

The first question uses the selected defect's summary, observed behavior, component, and inferred category. The session is saved as JSON for review or continuation.

### Answer each Why

1. Read the **Current question** and write a specific causal answer in the **Answer** box. Start with `Because ...` and name the mechanism, control, or process failure.
2. Add filenames or other traceable references in **Evidence refs**, separated by commas.
3. Set the flags accurately:
	- **controllable**: the team can change or control this cause.
	- **resolved**: fixing this cause solves the current defect.
	- **prevents recurrence**: the fix adds a durable preventive control.
	- **revise current node**: replace the current answer instead of adding another Why.
4. Select **Submit Answer**.

If the answer or evidence is weak, the workflow stays on the same Why and explains what must be strengthened. The normal target is five Whys, but the workflow may stop earlier when the evidence supports a controllable cause that resolves the defect and prevents recurrence.

### Navigate and revise the Why history

- Use the left and right arrow buttons beside **Current Why** to review recorded questions and answers.
- Selecting a previous Why restores its answer, evidence, and decision flags.
- Use **revise current node** to correct an answer without creating a duplicate Why.

### Use demo cases

Choose a demo case and select **Run Demo Case**:

- **Why 1**: simple issue that stops at the first Why.
- **Why 3**: moderate issue that stops at the third Why.
- **Why 5**: complex issue that continues to the fifth Why.

Each demo uses synthetic data, creates a fresh session, and generates the RCA report, CAPA CSV, and ADO Test Case CSV automatically.

### Export the results

- **Export Report** creates the Markdown RCA report.
- **Export CAPA CSV** creates CAPA tasks. Choose `ado`, `jira`, or `generic`, then optionally enter an assignee and due date.
- **Export ADO TestCase CSV** creates ADO-compatible test cases. Use `standard` for core cases or `expanded` to add negative and boundary variants.

Set the output path before exporting. Each export opens a preview of the generated file; review it and select **OK** to close the preview. Start or load a session before exporting.

### Load or reset sessions

- Use **Latest session** and **Load Selected Session** to reopen a saved session.
- Use **Refresh Session and Report Lists** after creating files outside the current page.
- Use **Refresh Status** to reload the current session state.
- Select **New Session** before starting another manual analysis. Existing session files are preserved.

### Agent Trace Viewer

Select a batch report and defect ID in **Agent Trace Viewer**, then choose **Load Agent Trace** to inspect the planner, analyzer, and validator steps for that defect. Select **Refresh Trace Inputs** after generating a new report.

### Common issues

- **No defect IDs appear:** confirm the input is a JSON list and each object has a non-empty `defect_id`; then refresh the page or change the input file.
- **The session will not advance:** provide a specific answer, at least one evidence reference, and a clear causal link.
- **Exports are disabled:** start or load a session first.
- **The browser cannot connect:** confirm the launcher is still running and use the exact URL printed in the terminal.
- **Old data remains in the form:** select **New Session**, then choose the new context, input, and defect.

### How CAPA and Test Cases are generated

After the 5-Whys session, the tool uses the complete RCA record to generate the deliverables. It uses the defect summary, component, observed and expected behavior, confirmed root cause, and evidence references collected across the Why chain.

CAPA output contains four task types:

- implement the corrective control
- add regression coverage
- add a monitoring or workflow gate
- validate corrective-action effectiveness

ADO Test Case output contains three base cases:

- corrective control resolves the defect
- regression gate detects recurrence
- corrective-action validation shows no regression

The output is based on the consolidated root-cause decision; the tool does not create one CAPA task for every individual Why. Expanded Test Case export can additionally create negative and boundary variants.

### Which UI action should I use?

- `Run Demo Case`: recommended for demonstrations; loads a bundled case and completes the flow automatically, including RCA, CAPA, and Test Case outputs.
- `Start RCA Session`: recommended for a real or custom case; answer each Why manually and export the artifacts from the UI when finished.
- Quick plans are retained for CLI and automation workflows, but are not exposed as a separate UI action. Use `Run Demo Case` for the bundled repeatable examples.

Optional flags:

```text
python start_local.py --dry-run
python start_local.py --skip-check
python start_local.py --host 127.0.0.1 --port 8787
```

## CLI fallback and automation

The terminal commands below are secondary options for automation, CI, or advanced users. They are not required for normal use.

Run the first-time environment check only:

```text
python check_env.py
```

macOS/Linux alternative:

```text
bash ./check-env.sh
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
python package_shareable.py
```

macOS/Linux alternative:

```text
bash ./package-shareable.sh
```

The script creates a timestamped zip in the sibling `dist/` folder and excludes local runtime outputs.

## Included Utility Scripts

- `check_env.py`: Cross-platform environment validation (Python/version/dependency/files/port).
- `start_local.py`: Cross-platform startup with automatic port fallback.
- `package_shareable.py`: Cross-platform clean packaging to sibling `dist/`.
- `check-env.sh`: Shell wrapper for `check_env.py` (macOS/Linux).
- `start-local.sh`: Shell wrapper for `start_local.py` (macOS/Linux).
- `package-shareable.sh`: Shell wrapper for `package_shareable.py` (macOS/Linux).
- `check-env.ps1`, `start-local.ps1`, `package-shareable.ps1`: Optional Windows PowerShell scripts when policy allows trusted local script execution.

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

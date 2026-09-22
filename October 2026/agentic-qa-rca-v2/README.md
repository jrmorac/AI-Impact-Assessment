# Agentic QA RCA Assistant

Purpose: project-agnostic defect triage and root-cause support workflow that combines Six Sigma and Software QA.

**Architecture and evaluator applicability:** See [ARCHITECTURE_AND_EVALUATOR_APPLICABILITY.md](ARCHITECTURE_AND_EVALUATOR_APPLICABILITY.md) for the deterministic, LLM-free release boundary, applicable controls, deferred LLM requirements, data handling, retention, and release governance.

## What this starter does

1. Reads project context from YAML files.
2. Reads synthetic defect events from a JSON file.
3. Runs a 3-step agentic flow:
   - Planner: selects analysis path and checks required fields.
   - Analyzer: proposes root-cause hypothesis and CAPA actions.
   - Validator: checks confidence and quality-gate compliance.
4. Calibrates confidence using data completeness and narrative quality signals.
5. Computes prioritization score and tier to rank triage actions.
6. Applies Five Whys RCA before CAPA release.
7. Enforces evidence-gated CAPA: if hypothesis support is weak or evidence artifacts are missing, output switches to investigate-first actions.
8. Scores evidence artifact quality and validates artifact traceability to defect IDs.
9. Requires a CAPA validation experiment plan for every confirmed CAPA recommendation.
10. Ingests experiment outcomes and computes CAPA effectiveness scores (effective/partial/ineffective/not_available).
11. Supports interactive RCA sessions with checkpoint gating and adaptive stop/continue logic.
12. Produces a structured output report in data/output, including per-defect `agent_trace` for planner/analyzer/validator execution visibility.
13. Appends an evidence row for assessment tracking.

## Project structure

- src: implementation
- project-context: reusable client/project/standards configuration
- data/input: synthetic defect input samples
- data/output: generated analysis reports
- evidence: logs for evaluation evidence
- metrics: baseline and sprint KPIs

## Preferred workflow: Web UI

Run the local web UI from this folder:

```text
python src/web_app.py --host 127.0.0.1 --port 8787
```

Open `http://127.0.0.1:8787` in your browser. The complete workflow is available from the UI:

1. Select a context, input file, and defect ID. Changing the input file refreshes the available defect IDs automatically.
2. Select `Run Demo Case` for the bundled `Why 1`, `Why 3`, or `Why 5` examples, or select `Start RCA Session` for a manual case.
3. Answer each Why and attach evidence references. Use the back/next controls to review the recorded question-and-answer history; selected answers, evidence, and decision flags are restored in the form.
4. Review the session status and root-cause report.
5. Use `Export Report`, `Export CAPA CSV`, and `Export ADO TestCase CSV` to generate the deliverables. Each export opens a confirmation preview with the generated file content.
6. Use `New Session` before starting another analysis.

The demo action generates the RCA report, CAPA tasks, and ADO test cases automatically. Manual sessions can export the same artifacts from the export panel.

## Web UI User Manual

### Start the application

1. Open a terminal in the `agentic-qa-rca` folder.
2. Start the server with the command shown above.
3. Open the displayed local URL in a browser.
4. Keep the terminal running while using the Web UI. Stop the server with `Ctrl+C` when finished.

The application runs locally. Use synthetic or non-sensitive QA data only.

### Start a manual RCA session

1. In **Context file**, choose the project profile that defines the severity model, taxonomy, quality gates, and RCA settings.
2. In **Input file**, choose a JSON file containing a list of defect objects.
3. Choose a **Defect ID**. The dropdown is populated from the selected input file's `defect_id` fields. If the ID is not listed, enter it in **Manual Defect ID**.
4. Choose a role: `qa`, `dev`, `sre`, or `release-manager`. The role changes the guidance shown for writing answers.
5. Optionally enter a session path. Leave it blank to create a timestamped session under `evidence/rca_sessions/`.
6. Select **Start RCA Session**.

The first question is created from the selected defect's summary, observed behavior, component, and inferred defect category. The session is saved as JSON so it can be reviewed or resumed.

### Answer each Why

1. Read the **Current question** and write a specific causal answer in the **Answer** box. Start with `Because ...` and name the mechanism, control, or process failure.
2. Add evidence references in the comma-separated **Evidence refs** field. Use filenames or other traceable references, for example `run-log.txt, duplicate-count.csv`.
3. Set the decision flags carefully:
   - **controllable**: the team can change or control this cause.
   - **resolved**: fixing this cause would solve the current defect, not only a contributing symptom.
   - **prevents recurrence**: the fix adds a durable control that prevents the defect from returning.
   - **revise current node**: replace the current answer instead of adding another Why step.
4. Select **Submit Answer**.

The checkpoint rules validate answer length, causal wording, evidence, controllability, resolution, and recurrence prevention. If the answer or evidence is weak, the session stays on the same Why and tells you what to strengthen.

### Navigate and revise the Why history

- Use the left and right arrow buttons beside **Current Why** to review recorded questions and answers.
- Selecting a previous Why restores its answer, evidence references, and decision flags in the form.
- Use **revise current node** when correcting an answer. This updates the existing Why instead of creating a duplicate entry.
- The workflow normally targets five Whys, but it can stop earlier when the checkpoint confirms a controllable root cause that resolves the defect and prevents recurrence.

### Use demo cases

Select a demo case and choose **Run Demo Case** to run a complete synthetic example:

- **Why 1**: simple issue that stops at the first Why.
- **Why 3**: moderate issue that stops at the third Why.
- **Why 5**: complex issue that continues to the fifth Why.

The demo creates a fresh session and generates the RCA report, CAPA CSV, and ADO Test Case CSV. Use demos to understand the workflow before running a custom case.

### Export the results

Use the export panel after a session has been started:

- **Export Report** creates the Markdown RCA case report.
- **Export CAPA CSV** creates corrective and preventive action tasks. Choose `ado`, `jira`, or `generic` as the provider and optionally set an assignee and due date.
- **Export ADO TestCase CSV** creates ADO-compatible test cases. The standard variant exports the core cases; the expanded variant also adds negative and boundary cases.

Set output paths before exporting. The UI opens a preview of each generated file; review it and select **OK** to close the preview. The export buttons remain unavailable until a session is loaded.

### Load an existing session

Use **Latest session** and **Load Selected Session** to reopen a saved session. Use **Refresh Session and Report Lists** after creating files outside the current page. **Refresh Status** reloads the current session state without starting a new one.

Select **New Session** before beginning another manual analysis. This clears the active session from the form while preserving existing session files.

### Agent Trace Viewer

The **Agent Trace Viewer** is for batch reports. Select a report file and defect ID, then choose **Load Agent Trace** to inspect the planner, analyzer, and validator steps recorded for that defect. Use **Refresh Trace Inputs** after generating a new batch report.

### Common issues

- **No defect IDs appear:** confirm that the selected input is a JSON list and each defect has a non-empty `defect_id` field, then refresh the page or change the input file.
- **The session will not advance:** add a concrete answer, at least one evidence reference, and a clear causal link. Review the recommended data requests shown by the workflow.
- **Exports are disabled:** start or load a session first.
- **The browser cannot connect:** confirm the Python server is still running and use the exact localhost URL printed in the terminal.
- **Starting another case shows old data:** select **New Session**, then select the new context, input, and defect.

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
- Quick plans remain available for CLI and automation workflows, but are not exposed as a separate UI action. Use `Run Demo Case` for the bundled repeatable examples.

## Demo Run

The project includes three synthetic demo cases that show variable 5-Whys depth:

- `why1`: simple case that confirms at Why 1
- `why3`: moderate case that confirms at Why 3
- `why5`: complex case that confirms at Why 5

Run a demo directly from this folder:

```text
python src/main.py demo-run --case why3
```

The command loads the matching demo input and quick plan, creates a new timestamped session when `--session` is omitted, and exports three artifacts: the RCA report, an ADO-compatible CAPA CSV, and an ADO-compatible Test Case CSV. The web UI exposes the same flow through `Run Demo Case`.

Use `New Session` in the web UI before starting another manual analysis. It clears the active session path so the next start creates a fresh session. Existing session files remain available in the session list for review.

## CLI fallback and automation

The terminal commands below expose the same workflow for automation, CI, or advanced users. They are not required for normal use.

### Interactive RCA Session Mode

Start a session for one defect:

```text
python src/main.py start-rca --context project-context/baseline-project.yaml --input data/input/synthetic_defects_with_evidence.json --defect-id PRJ-DEF-201 --session evidence/rca_sessions/prj-def-201.json
```

Answer the current Why with evidence and checkpoint flags:

```text
python src/main.py answer-rca --session evidence/rca_sessions/prj-def-201.json --answer "Because the merge process allowed duplicate keys after replay due to a missing idempotency guard." --evidence-ref "PRJ-DEF-201_sql-output-dup-count-2026-08-07.csv" --evidence-ref "PRJ-DEF-201_pipeline-run-log-merge-window-2026-08-07.txt" --controllable
```

Revise the current Why instead of appending a second attempt:

```text
python src/main.py revise-rca --session evidence/rca_sessions/prj-def-201.json --answer "Because the merge process replayed records without an idempotency guard, duplicate keys were inserted into the target table." --evidence-ref "PRJ-DEF-201_sql-output-dup-count-2026-08-07.csv" --evidence-ref "PRJ-DEF-201_pipeline-run-log-merge-window-2026-08-07.txt" --controllable
```

Check session status:

```text
python src/main.py status-rca --session evidence/rca_sessions/prj-def-201.json
```

Export a formal RCA case report:

```text
python src/main.py export-rca-report --session evidence/rca_sessions/prj-def-201.json --output evidence/rca_reports/prj-def-201.md
```

Run a guided one-command RCA workflow (interactive terminal wizard):

```text
python src/main.py guided-rca --context project-context/baseline-project.yaml --input data/input/synthetic_defects_with_evidence.json --defect-id PRJ-DEF-201 --role qa
```

Optional guided flags:
- `--session` to reuse or pin a session path
- `--output-report` to customize the exported markdown report path
- `--role` values: `dev`, `qa`, `sre`, `release-manager`
- `--quick-plan` to run non-interactively from a predefined JSON answer plan

Run guided mode non-interactively (quick mode):

```text
python src/main.py guided-rca --context project-context/baseline-project.yaml --input data/input/synthetic_defects_with_evidence.json --defect-id PRJ-DEF-201 --role qa --quick-plan data/input/quick_plan_prj-def-201.json --session evidence/rca_sessions/prj-def-201-quick.json --output-report evidence/rca_reports/prj-def-201-quick.md
```

Quick plan schema:

```json
{
   "default_evidence_refs": ["artifact-a", "artifact-b"],
   "default_flags": {
      "controllable": true,
      "resolved": false,
      "prevents_recurrence": false
   },
   "answers": [
      {
         "answer": "Because ..."
      },
      {
         "answer": "Because ...",
         "evidence_refs": ["artifact-c"],
         "resolved": true,
         "prevents_recurrence": true
      }
   ]
}
```

Sample quick plan included:
- `data/input/quick_plan_prj-def-201.json`

Guided mode improvements for real team adoption:
- one-command session flow from start to report export
- role-based answer templates shown at each Why step
- automatic evidence suggestion by defect ID from `evidence/` and `data/`
- automatic report export when the stop condition is reached
- optional non-interactive quick mode for demos and CI-assisted execution

## CAPA CSV Export (ADO/Jira/Generic)

Export CAPA tasks from a confirmed RCA session as import-ready CSV:

```text
python src/main.py export-capa-csv --session evidence/rca_sessions/prj-def-201-quick.json --output evidence/capa_exports/prj-def-201-ado.csv --provider ado --assignee qa.lead@sampleclient.com --due-date 2026-08-28
```

Jira format example:

```text
python src/main.py export-capa-csv --session evidence/rca_sessions/prj-def-201-quick.json --output evidence/capa_exports/prj-def-201-jira.csv --provider jira --assignee qa.lead --due-date 2026-08-28
```

Provider options:
- `ado`: columns for Azure DevOps import
- `jira`: columns for Jira CSV import
- `generic`: neutral schema for custom tooling

## ADO Test Case CSV Export

Export ADO-compatible Test Case work items from an RCA session using the required field order:

```text
python src/main.py export-ado-testcases-csv --session evidence/rca_sessions/prj-def-201-quick.json --output evidence/capa_exports/prj-def-201-ado-testcases.csv --assigned-to qa.lead@sampleclient.com --area-path SampleProject\\QA --iteration-path SampleProject\\Sprint-2 --state Design
```

Expanded mode example (adds negative and boundary variants per base test case):

```text
python src/main.py export-ado-testcases-csv --session evidence/rca_sessions/prj-def-201-quick.json --output evidence/capa_exports/prj-def-201-ado-testcases-expanded.csv --assigned-to qa.lead@sampleclient.com --area-path SampleProject\\QA --iteration-path SampleProject\\Sprint-2 --state Design --variant-set expanded
```

Exported columns (exact order):
- `ID`
- `Work Item Type`
- `Title`
- `Assigned To`
- `State`
- `Area Path`
- `Iteration Path`
- `Description`
- `Repro Steps`
- `System Info`
- `Acceptance Criteria`

Notes:
- Output is comma-delimited CSV.
- `Work Item Type` is set to `Test Case` for all rows.
- `ID` is left empty so ADO assigns it on import.
- Multi-step content is represented with `\\n` inside quoted fields for safe row integrity.
- `--variant-set standard` exports core CAPA-aligned cases only (default).
- `--variant-set expanded` exports standard + negative + boundary variants.

The interactive RCA session will:
- continue if another Why is needed
- stop when the checkpoint confirms a controllable cause that should prevent recurrence
- pause for more evidence when the answer is too weak to progress

## How to adapt to another project

1. Copy project-context/project-profile.template.yaml into a new profile file.
2. Fill standards, workflow, severity mappings, and acceptance criteria.
3. Use synthetic or non-sensitive defect inputs only.
4. Run the same command with the new context file.

## Evidence checklist per run

After each run, capture:
- input file name and timestamp
- number of analyzed defects
- accepted vs flagged suggestions
- manual corrections performed
- estimated triage-time delta
- evidence artifacts linked for each defect when CAPA confirmation is expected
- experiment outcome metrics (baseline vs post, target achievement, sample size, regression signal)

Use evidence/evidence_log.csv and evidence/validation_corrections_log.md.

## Web UI capabilities

Run the local UI server:

```text
python src/web_app.py --host 127.0.0.1 --port 8787
```

Open in browser:

```text
http://127.0.0.1:8787
```

What the UI supports:
- Start RCA session from context/input/defect selection
- Defect ID dropdown is auto-loaded from the selected input JSON list (field `defect_id`)
- Manual Defect ID override when you need to type an ID not present in dropdown
- Load latest saved session from a selector
- One-click quick plan execution (non-interactive)
- Answer or revise Why nodes with evidence refs and checkpoint flags
- Vertical option cards for `controllable`, `resolved`, `prevents recurrence`, and `revise current node` with inline explanations
- Built-in stop-logic hint explaining early closure before Why 5 when checkpoint criteria are satisfied
- Refresh and inspect live session state
- Export RCA report, CAPA CSV, and ADO Test Case CSV
- Agent Trace Viewer for batch reports: pick report + defect ID and inspect `agent_trace` directly in UI

API health endpoint:

```text
http://127.0.0.1:8787/api/health
```

Agent trace endpoint:

```text
http://127.0.0.1:8787/api/report-agent-trace?report=data/output/report_sprint1_orchestrated.json
```


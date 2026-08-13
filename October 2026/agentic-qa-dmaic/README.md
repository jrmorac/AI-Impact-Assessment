# Agentic QA DMAIC Assistant

Purpose: project-agnostic defect triage and root-cause support workflow that combines Six Sigma and Software QA.

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

## Quick start

1. Open a terminal in this folder.
2. Run:

   python src/main.py --context project-context/baseline-project.yaml --input data/input/synthetic_defects_sprint1.json --output data/output/report_sprint1.json

3. Review:
- data/output/report_sprint1.json
- evidence/evidence_log.csv

## Interactive RCA Session Mode

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

## Guided execution

Use DAY_BY_DAY_SPRINT1_GUIDE.md for a 10-day implementation cadence with evidence checkpoints.

## Local Web UI (localhost)

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


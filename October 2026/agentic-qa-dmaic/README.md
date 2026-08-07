# Agentic QA DMAIC Assistant

Purpose: project-agnostic defect triage and root-cause support workflow that combines Six Sigma and Software QA.

This starter is designed to help build Level 3 evidence for the Engineering track:
- D1: Daily AI-first workflow using structured context files.
- D2: Formal validation via quality gates and correction logging.
- D3: Measurable impact with baseline and sprint metrics templates.
- D4: Agentic pipeline (planner, analyzer, validator) that runs repeatedly.
- D5: Reusable, shareable framework across projects and clients.

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
4. Produces a structured output report in data/output.
5. Appends an evidence row for assessment tracking.

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


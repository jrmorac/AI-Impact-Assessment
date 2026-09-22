# RCA Case Report

- Session ID: prj-def-201-wording2
- Generated UTC: 2026-08-11T17:04:21.167562+00:00
- Status: root_cause_confirmed
- Defect ID: PRJ-DEF-201
- Category: data-quality
- Problem Summary: Recurring duplicate records after nightly merge window (Duplicate keys increased from 0 to 37 in repeated run)
- Root Cause Summary: Because ownership and governance for idempotency-by-design were not explicitly assigned in the delivery process, replay-risk controls were not consistently translated into mandatory engineering and QA gate criteria. Establishing explicit ownership plus a required replay/idempotency control checklist and CI rerun test gate would directly remove this failure mode and prevent recurrence for this defect class.
- Stop Reason: Checkpoint confirmed a controllable cause that should prevent recurrence.

## Why Chain

### Why 1
- Question: Why did Recurring duplicate records after nightly merge window (Duplicate keys increased from 0 to 37 in repeated run) occur in CustomerActivityIngestion, and what evidence supports that first causal explanation? Start with the most direct data-quality cause you can defend.
- Answer: Because the merge process replayed records without an idempotency guard, duplicate keys were inserted into the target table.
- Evidence: PRJ-DEF-201_sql-output-dup-count-2026-08-07.csv, PRJ-DEF-201_pipeline-run-log-merge-window-2026-08-07.txt
- Decision: continue
- Controllable: True
- Prevents Recurrence: False

### Why 2
- Question: What deeper cause made this possible: the merge process replayed records without an idempotency guard? What evidence shows that this deeper cause is real rather than assumed?
- Answer: Because the ingestion pipeline lacks a persisted deduplication state and deterministic replay key check between nightly runs, previously merged records are re-accepted on rerun. The merge logic validates incoming schema but does not enforce idempotent replay controls at the write boundary, so identical business keys can pass again during the same merge window.
- Evidence: PRJ-DEF-201_pipeline-run-log-merge-window-2026-08-07.txt, PRJ-DEF-201_sql-output-dup-count-2026-08-07.csv
- Decision: continue
- Controllable: True
- Prevents Recurrence: False

### Why 3
- Question: What deeper cause made this possible: the ingestion pipeline lacks a persisted deduplication state and deterministic replay key check between nightly runs? What evidence shows that this deeper cause is real rather than assumed?
- Answer: Because the pipeline design and release criteria did not require idempotency controls as a hard acceptance condition, the implementation shipped without replay-state safeguards. The defect escaped because duplicate-prevention was treated as an implicit expectation rather than an explicit, testable requirement tied to merge-window reruns.
- Evidence: PRJ-DEF-201_pipeline-run-log-merge-window-2026-08-07.txt, PRJ-DEF-201_sql-output-dup-count-2026-08-07.csv
- Decision: continue
- Controllable: True
- Prevents Recurrence: False

### Why 4
- Question: What deeper cause made this possible: the pipeline design and release criteria did not require idempotency controls as a hard acceptance condition? What evidence shows that this deeper cause is real rather than assumed?
- Answer: Because the QA and release workflow did not include a mandatory deterministic rerun/idempotency test scenario in the pre-release gate, missing replay safeguards were not detected before deployment. The quality gate checked functional merge success but not repeat-run behavior against duplicate-key integrity constraints.
- Evidence: PRJ-DEF-201_pipeline-run-log-merge-window-2026-08-07.txt, PRJ-DEF-201_sql-output-dup-count-2026-08-07.csv
- Decision: continue
- Controllable: True
- Prevents Recurrence: False

### Why 5
- Question: What deeper cause made this possible: the QA and release workflow did not include a mandatory deterministic rerun/idempotency test scenario in the pre-release gate? What evidence shows that this deeper cause is real rather than assumed?
- Answer: Because ownership and governance for idempotency-by-design were not explicitly assigned in the delivery process, replay-risk controls were not consistently translated into mandatory engineering and QA gate criteria. Establishing explicit ownership plus a required replay/idempotency control checklist and CI rerun test gate would directly remove this failure mode and prevent recurrence for this defect class.
- Evidence: PRJ-DEF-201_pipeline-run-log-merge-window-2026-08-07.txt, PRJ-DEF-201_sql-output-dup-count-2026-08-07.csv
- Decision: stop_root_cause_confirmed
- Controllable: True
- Prevents Recurrence: True

## Evidence Register

- PRJ-DEF-201_sql-output-dup-count-2026-08-07.csv
- PRJ-DEF-201_pipeline-run-log-merge-window-2026-08-07.txt

## Next Action

- Document CAPA and validation plan against this confirmed root cause.

## CAPA Plan

### Corrective Actions (Immediate)

1. Add an idempotency replay guard at merge-write boundary.
2. Introduce a persisted deduplication state keyed by deterministic business keys plus run-window metadata.
3. Enforce duplicate-key rejection behavior with explicit logging when replay is detected.

### Preventive Actions (Systemic)

1. Assign explicit ownership for idempotency-by-design in engineering and QA workflows.
2. Add an idempotency checklist to definition-of-done and release sign-off criteria.
3. Add a mandatory deterministic rerun test gate in CI for merge pipelines.

### Owners and Due Dates

1. Engineering owner: Implement replay guard and persisted dedup state.
2. QA owner: Add deterministic rerun tests and release-gate checks.
3. Delivery owner: Update governance checklist and approval workflow.
4. Target completion window: next sprint (10 working days).

## CAPA Validation Experiment

### Hypothesis

If replay/idempotency controls plus mandatory rerun gate checks are implemented, duplicate-key recurrence for this defect class will be reduced to zero under repeated-run conditions.

### Baseline

- Baseline metric: Duplicate keys introduced on repeated run.
- Baseline value: 37 duplicate keys after rerun.
- Baseline evidence: PRJ-DEF-201_sql-output-dup-count-2026-08-07.csv.

### Intervention

1. Deploy replay guard and dedup state persistence.
2. Execute deterministic rerun gate in CI before release.
3. Block release if rerun duplicate count is greater than 0.

### Measurement Design

1. Dataset: synthetic batch B (same deterministic input and merge key).
2. Test method: run batch twice in same merge window and compare uniqueness counts.
3. Sample size: minimum 5 repeated-run pairs across two consecutive release cycles.
4. Primary metric: duplicate_key_count_after_rerun.
5. Secondary metrics: rerun pass rate, false-positive replay rejects, pipeline runtime delta.

### Acceptance Criteria

1. Primary: duplicate_key_count_after_rerun = 0 for all validation runs.
2. Secondary: rerun pass rate >= 95% with no Sev1/Sev2 regression introduced.
3. Stability: runtime increase from controls <= 10% compared to baseline median.

### Rollback and Escalation

1. Roll back release if duplicate_key_count_after_rerun > 0 in gate run.
2. Open high-priority defect and perform targeted root-cause branch analysis on replay-state logic.
3. Require engineering + QA sign-off before re-promoting build.

### Evidence to Capture

1. CI rerun gate logs with pass/fail outcome.
2. Duplicate count SQL output artifact per validation run.
3. Release checklist artifact showing idempotency sign-off.

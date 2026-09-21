# RCA Case Report

- Session ID: prj-def-201-quick
- Generated UTC: 2026-09-16T18:28:48.146523+00:00
- Status: root_cause_confirmed
- Defect ID: PRJ-DEF-201
- Category: data-quality
- Problem Summary: Recurring duplicate records after nightly merge window (Duplicate keys increased from 0 to 37 in repeated run)
- Root Cause Summary: Because ownership and governance for idempotency-by-design were not explicitly assigned, replay-risk controls were not translated into mandatory engineering and QA gates. Establishing explicit ownership plus required replay control checklists and CI rerun gate will prevent recurrence.
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
- Answer: Because the ingestion pipeline lacks a persisted deduplication state and deterministic replay key check between nightly runs, previously merged records are re-accepted on rerun.
- Evidence: PRJ-DEF-201_sql-output-dup-count-2026-08-07.csv, PRJ-DEF-201_pipeline-run-log-merge-window-2026-08-07.txt
- Decision: continue
- Controllable: True
- Prevents Recurrence: False

### Why 3
- Question: What deeper cause made this possible: the ingestion pipeline lacks a persisted deduplication state and deterministic replay key check between nightly runs? What evidence shows that this deeper cause is real rather than assumed?
- Answer: Because the pipeline design and release criteria did not require idempotency controls as a hard acceptance condition, replay-state safeguards were omitted.
- Evidence: PRJ-DEF-201_sql-output-dup-count-2026-08-07.csv, PRJ-DEF-201_pipeline-run-log-merge-window-2026-08-07.txt
- Decision: continue
- Controllable: True
- Prevents Recurrence: False

### Why 4
- Question: What deeper cause made this possible: the pipeline design and release criteria did not require idempotency controls as a hard acceptance condition? What evidence shows that this deeper cause is real rather than assumed?
- Answer: Because QA and release workflow did not include a mandatory deterministic rerun/idempotency test gate, this defect was not detected before deployment.
- Evidence: PRJ-DEF-201_sql-output-dup-count-2026-08-07.csv, PRJ-DEF-201_pipeline-run-log-merge-window-2026-08-07.txt
- Decision: continue
- Controllable: True
- Prevents Recurrence: False

### Why 5
- Question: What deeper cause made this possible: QA and release workflow did not include a mandatory deterministic rerun/idempotency test gate? What evidence shows that this deeper cause is real rather than assumed?
- Answer: Because ownership and governance for idempotency-by-design were not explicitly assigned, replay-risk controls were not translated into mandatory engineering and QA gates. Establishing explicit ownership plus required replay control checklists and CI rerun gate will prevent recurrence.
- Evidence: PRJ-DEF-201_sql-output-dup-count-2026-08-07.csv, PRJ-DEF-201_pipeline-run-log-merge-window-2026-08-07.txt
- Decision: stop_root_cause_confirmed
- Controllable: True
- Prevents Recurrence: True

## Evidence Register

- PRJ-DEF-201_sql-output-dup-count-2026-08-07.csv
- PRJ-DEF-201_pipeline-run-log-merge-window-2026-08-07.txt

## Next Action

- Document CAPA and validation plan against this confirmed root cause.

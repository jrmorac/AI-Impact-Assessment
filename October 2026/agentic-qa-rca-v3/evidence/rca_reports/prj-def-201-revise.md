# RCA Case Report

- Session ID: prj-def-201-revise
- Generated UTC: 2026-08-07T19:19:00.696776+00:00
- Status: awaiting_answer
- Defect ID: PRJ-DEF-201
- Category: data-quality
- Problem Summary: Recurring duplicate records after nightly merge window (Duplicate keys increased from 0 to 37 in repeated run)
- Root Cause Summary: 
- Stop Reason: 

## Why Chain

### Why 1
- Question: Why did Recurring duplicate records after nightly merge window (Duplicate keys increased from 0 to 37 in repeated run) occur in CustomerActivityIngestion, and what evidence supports that first causal explanation? Start with the most direct data-quality cause you can defend.
- Answer: Because the merge process replayed records without an idempotency guard, duplicate keys were inserted into the target table.
- Evidence: PRJ-DEF-201_sql-output-dup-count-2026-08-07.csv, PRJ-DEF-201_pipeline-run-log-merge-window-2026-08-07.txt
- Decision: continue
- Controllable: True
- Prevents Recurrence: False

## Evidence Register

- PRJ-DEF-201_sql-output-dup-count-2026-08-07.csv
- PRJ-DEF-201_pipeline-run-log-merge-window-2026-08-07.txt

## Next Action

- Answer the next Why and attach evidence references.

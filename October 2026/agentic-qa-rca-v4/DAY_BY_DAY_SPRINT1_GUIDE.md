# Day-by-Day Sprint 1 Guide (10 Working Days)

Use this guide to execute the project with evidence discipline from the first week.

## Day 1 - Baseline and setup lock

Actions:
- Confirm dependency install from requirements.txt.
- Run baseline command with the generic project profile.
- Save run output and verify evidence log row.

Evidence:
- data/output/report_sprint1.json
- evidence/evidence_log.csv (new timestamp row)

## Day 2 - Context hardening

Actions:
- Review project-context/baseline-project.yaml.
- Tune min_confidence_to_autosuggest and priority tiers if needed.
- Document why thresholds were chosen.

Evidence:
- YAML changes in version control
- One short threshold rationale note in your sprint notes

## Day 3 - Validator stress test

Actions:
- Run mixed defects input with incomplete fields and recurring language.
- Confirm flagged entries appear when confidence is low or fields are missing.
- Confirm CAPA is deferred when evidence_artifacts are not linked.

Suggested command:
python src/main.py --context project-context/baseline-project.yaml --input data/input/synthetic_defects_sprint1_mixed.json --output data/output/report_sprint1_mixed.json

Evidence:
- report showing accepted and flagged outputs
- correction entries in evidence/validation_corrections_log.md

## Day 4 - Correction loop quality

Actions:
- Review flagged items manually.
- Apply correction logging discipline:
  - what the agent suggested,
  - what you changed,
  - why.
- Add or reference evidence artifacts (logs, traces, SQL outputs) so deferred items can progress to confirmed CAPA.

Evidence:
- at least 3 new correction rows

## Day 5 - Prioritization tuning

Actions:
- Compare top-priority list against your QA expert judgment.
- If priority ordering is off, tune prioritization weights in context.

Evidence:
- before/after output comparison
- documented weight update and rationale

## Day 6 - Reuse test (project-agnostic proof)

Actions:
- Copy project-context/project-profile.template.yaml to a second profile.
- Define taxonomy, standards, and thresholds for another project context.
- Run same input with new context.

Evidence:
- new context profile file
- output report generated with same pipeline

## Day 7 - KPI capture start

Actions:
- Fill first current-sprint row in metrics/sprint_metrics.csv.
- Keep methodology consistent with baseline window in metrics/baseline_metrics.csv.

Evidence:
- updated sprint_metrics.csv row
- one methodology note attached to sprint data

## Day 8 - Team walkthrough prep

Actions:
- Prepare a 10-15 minute walkthrough:
  - problem,
  - workflow,
  - output fields,
  - correction process.
- Invite at least 2 colleagues to test one run each.

Evidence:
- session invite or attendance note
- names and outcomes for each participant

## Day 9 - Adoption capture

Actions:
- Record teammate runs and outcomes.
- Add adoption results to sharing tracker in July folder.

Evidence:
- July 2026/prompt-library/Prompt_Library_Sharing_Record.md updates
- optional supporting chat/email confirmations

## Day 10 - Sprint checkpoint package

Actions:
- Create a mini evidence bundle for this sprint:
  - one baseline run,
  - one mixed run,
  - correction log excerpt,
  - KPI row,
  - adoption notes.

Evidence:
- sprint package folder or indexed list of files

## End-of-sprint pass criteria

- At least 4 total runs logged
- At least 1 mixed-input run with flagged outputs
- At least 3 correction entries
- At least 1 KPI row completed
- At least 1 teammate trial completed

## Notes for Level 3 alignment

- D2 improves through correction rigor and gate enforcement.
- D3 improves through consistent KPI methodology.
- D4 improves through repeatable, configurable orchestration.
- D5 improves through teammate adoption evidence.


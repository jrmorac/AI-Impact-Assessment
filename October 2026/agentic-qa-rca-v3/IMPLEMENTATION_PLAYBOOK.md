# Implementation Playbook (August to October 2026)

This playbook is your step-by-step path to implement the project and produce verifiable Level 3 evidence.

## Goal

Build a reusable, project-agnostic QA RCA agent workflow that:
- reduces defect triage effort,
- improves root-cause consistency,
- produces reusable team assets.

## Sprint 1 (Week 1-2): Stabilize the foundation

### Step 1: Run baseline workflow
Command:

python src/main.py --context project-context/baseline-project.yaml --input data/input/synthetic_defects_sprint1.json --output data/output/report_sprint1.json

Success criteria:
- output report generated
- one row appended to evidence/evidence_log.csv

Evidence to keep:
- report file
- log row timestamp

### Step 2: Configure a new client/project profile
Actions:
- copy project-context/project-profile.template.yaml
- create project-context/<new-project>.yaml
- map standards, defect taxonomy, and quality gates for that project

Success criteria:
- same script runs with the new context file

Evidence to keep:
- new context file commit
- output report generated using the new context

### Step 3: Add real non-sensitive defect samples
Actions:
- replace or add synthetic datasets in data/input
- keep only non-sensitive data

Success criteria:
- at least 15 defects processed across 2 runs

Evidence to keep:
- input dataset versions
- output reports

## Sprint 2 (Week 3-4): Improve analysis quality

### Step 4: Improve analyzer heuristics
Actions:
- extend keyword and category mapping in src/agents.py
- add project-specific CAPA actions by category

Success criteria:
- fewer manual category corrections in validation log

Evidence to keep:
- before/after comparison in evidence/validation_corrections_log.md
- PR or commit references

### Step 5: Tighten validator gates
Actions:
- increase minimum confidence threshold in context
- add stronger rejection rules in quality-gates.template.yaml

Success criteria:
- flagged outputs are reviewed before use
- no low-confidence autosuggestions accepted without human review

Evidence to keep:
- rejected case examples
- correction log entries with rationale

## Sprint 3 (Week 5-6): Integrate into team workflow

### Step 6: Add a repeatable operating cadence
Actions:
- run the assistant on each triage batch or sprint review
- nominate reviewer role for correction logging

Success criteria:
- at least 4 recurring runs in evidence log

Evidence to keep:
- evidence log growth over time
- run frequency trend

### Step 7: Track measurable outcomes
Actions:
- populate metrics/sprint_metrics.csv at each sprint end
- compare against metrics/baseline_metrics.csv

Success criteria:
- measurable trend in at least 2 KPIs:
  - avg triage minutes per defect
  - defect reopen rate
  - repeat defect rate

Evidence to keep:
- completed sprint metrics table
- short methodology note on how numbers were measured

## Sprint 4 (Week 7-8): Multiplier and Level 3 packaging

### Step 8: Team adoption and transfer
Actions:
- onboard at least 2 colleagues
- ask each to run one analysis using a project profile

Success criteria:
- adoption entries with user, date, and output produced

Evidence to keep:
- adoption proof in existing sharing record:
  - July 2026/prompt-library/Prompt_Library_Sharing_Record.md
- optional screenshots or chat confirmations with outcome context

### Step 9: Prepare evaluation-ready evidence bundle
Actions:
- prepare one folder with selected artifacts:
  - architecture and workflow explanation
  - representative output reports
  - evidence log and correction log
  - KPI baseline vs sprint trend
  - teammate adoption proof

Success criteria:
- every engineering question (D1-D5) has at least one direct artifact attachment

Evidence to keep:
- final curated attachment list by question

## Weekly ritual (15-20 min)

1. Run at least one batch through the agent.
2. Update evidence/evidence_log.csv.
3. Log corrections in evidence/validation_corrections_log.md.
4. Update one KPI row in metrics/sprint_metrics.csv.
5. Capture one short note: what improved, what failed, what changed.

## Mapping to Engineering Dimensions

- D1: regular usage cadence and context-profile maintenance
- D2: correction log + validation gates
- D3: baseline and sprint KPI trend
- D4: planner-analyzer-validator automation runs over time
- D5: teammate onboarding and reusable context model across projects


---
description: "Run a full multi-agent improvement cycle and write outputs aligned to development-records artifacts 01-10. Use when converting QA findings into spec, plan, review evidence, and final integration decision."
name: "Development Records Cycle"
argument-hint: "Provide findings input and target cycle folder"
agent: "Senior Agentic Engineer"
---
Orchestrate a complete improvement cycle using specialized agents and map deliverables to the development-records structure.

Inputs:
- Findings input: ${input:QA findings source or summary}
- Target cycle folder: ${input:Path like October 2026/agentic-qa-rca/development-records/YYYYMMDD-agent-review-cycle-XX}
- Scope: ${input:Backend, Frontend, or Both}

Execution requirements:
1. Use Senior QA Agent to triage findings and populate severity/reproducibility details.
2. Use Senior Backend Engineer for backend requirements and fix plan when backend scope exists.
3. Use Senior Frontend Engineer for frontend requirements and fix plan when frontend scope exists.
4. Use Senior QA Agent to validate acceptance criteria, test strategy, and evidence gaps.
5. Use Senior Agentic Engineer to reconcile conflicts and issue integration decision.

Artifact mapping requirements:
- 01_QA_Findings_Triage.md: triage table and severity summary.
- 02_Improvement_Specification.md: requirements, scope boundaries, acceptance criteria.
- 03_Enhancement_Implementation_Plan.md: workstreams, dependencies, tasks, done criteria.
- 04_Agent_Activity_Log.md: timestamped actions by each agent.
- 05_Traceability_Matrix.csv: Finding ID -> Requirement ID -> Task ID -> Change -> Test -> Review.
- 06_Metrics_Baseline_vs_After.csv: baseline and post-change metrics.
- 07_Governance_Gate_Checklist.md: pre-implementation, pre-merge, pre-release status.
- 08_Code_Review_Findings.md: severity-first findings and resolutions.
- 09_Integration_Decision_Record.md: conflict resolutions and final decision.
- 10_Risk_and_Rollback_Register.md: risk entries with rollback triggers/actions.

Output requirements:
- Report missing inputs before proceeding.
- Keep findings ordered by severity.
- Do not mark completed when traceability links are missing.
- Return final recommendation: Approve, Conditionally Approve, or Block.

Guardrails:
- Use synthetic and non-sensitive data only.
- Keep development-record artifacts out of shareable package outputs.

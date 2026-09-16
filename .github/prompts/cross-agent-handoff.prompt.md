---
description: "Run structured handoffs across Senior QA Agent, Senior Backend Engineer, Senior Frontend Engineer, and Senior Agentic Engineer from findings to final integration decision."
name: "Cross-Agent Handoff"
argument-hint: "Provide findings source, scope, and target record folder"
agent: "Senior Agentic Engineer"
---
Orchestrate a complete improvement cycle using specialized agents and map deliverables to the development-records structure.

Inputs:
- Findings source: ${input:Findings source path or summary}
- Scope: ${input:Backend, Frontend, or Both}
- Target records folder: ${input:Path to development-records cycle folder}

Current defaults for quick reuse:
- Findings source default: C:\Users\JoseRafaelMoraCasal\AI Impact Assessment\October 2026\agentic-qa-rca\development-records\20260913-agent-review-cycle-01\Quality report 2026-09-13.txt
- Scope default: Both
- Target records folder default: C:\Users\JoseRafaelMoraCasal\AI Impact Assessment\October 2026\agentic-qa-rca\development-records\20260913-agent-review-cycle-01

Preflight:
1. Confirm findings input is synthetic and non-sensitive before processing.
2. Normalize scope values to Backend, Frontend, or Both.

Execution requirements:
1. Use Senior QA Agent to triage findings and populate severity and reproducibility details.
2. Use Senior Backend Engineer for backend requirements and fix plan when backend scope exists.
3. Use Senior Frontend Engineer for frontend requirements and fix plan when frontend scope exists.
4. Re-run Senior QA Agent to validate acceptance criteria, test strategy, and evidence gaps.
5. Use Senior Agentic Engineer to reconcile conflicts, enforce traceability, and issue integration decision.

Output requirements:
- Report missing inputs before proceeding.
- Findings by severity.
- Consolidated requirement IDs.
- Plan by workstream and dependencies.
- Traceability and evidence gap report.
- Release gate recommendation: Approve, Conditionally Approve, or Block.

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
- 10_Risk_and_Rollback_Register.md: risk entries with rollback triggers and actions.

Mandatory file updates in Target records folder:
- Write or update all artifacts 01 through 10.
- If metric data is not yet available for 06_Metrics_Baseline_vs_After.csv, add an evidence-gap note in 09_Integration_Decision_Record.md.

Completion rule:
- Do not mark completed unless required file updates and traceability links are present.

Guardrails:
- Use synthetic and non-sensitive data only.
- Do not mark complete if traceability links are missing.
- Explicitly document unresolved risks and rollback conditions.
- Keep development-record artifacts out of shareable package outputs.

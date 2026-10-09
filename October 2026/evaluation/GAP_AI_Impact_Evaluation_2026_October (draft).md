# GAP AI Impact Evaluation

**Employee:** Jose Rafael Mora Casal
**Cycle:** October 2026

> Draft prepared for copy/paste into the evaluation portal. Review every bracketed note, confirm dates/names, and attach artifacts independently to each question before submitting.

---

# Project Constraints

- [x] Client limitations on AI usage
- [x] Security or compliance restrictions
- [x] Highly regulated environment

**Constraints Note:** The client operates under healthcare data regulations (HIPAA context). Direct AI use on client data or production systems is restricted to prevent PII exposure. All AI work in this cycle — including the multi-agent engineering process described below — was applied exclusively to non-sensitive project artifacts: documentation, synthetic/demo data, QA tooling source code, and internal governance records.

---

# Daily AI-First Workflow

## Question

Describe your daily AI-first workflow: How specifically do you integrate AI into your task planning, code generation, testing, use of shared organizational assets, among others, where applicable? Explain in detail how you applied AI within the last 6 months.

### Response

My daily AI-first workflow on the DOM project runs on a deliberate, repeatable pattern: ground the task in source requirements or prior artifacts, draft and refine through isolated, single-session AI prompts, and apply human review before anything is committed or shared. I keep this single-prompt pattern intentionally — not as a capability limit, but because the DOM project is a highly regulated, client-restricted environment (healthcare data, HIPAA context) where autonomous or multi-step agentic execution against client systems is out of scope without a new architecture and security review. This produced six officially adopted deliverables between April and July: a requirements-vs-proposal comparison used in client-facing discussion, deterministic SQL synthetic test-data scripts used in actual project testing, a performance testing strategy adopted as the project's QA baseline, 27 test cases imported and actively executed in Azure DevOps, a performance testing annex presented at a client-attended review, and AI-transcribed meeting minutes distributed as the official record.

Because the regulated project constrains agentic execution, I built and exercised that capability where policy allows: a separate, project-agnostic QA tool using a governed multi-agent engineering process (detailed fully in Question 4). This is not a workaround — it's how I apply AI-first thinking even where direct agentic use on client data isn't permitted: build and validate the agentic capability in a safe, synthetic-data environment, govern it with the same rigor (shared review rubric, release-gate checklist, traceability), and keep it ready to redeploy the moment project constraints allow it.

### Supporting Artifacts

- `.github/copilot-instructions.md`
- `prompts/README.md` and `prompts/TEAM-GUIDE.md`
- `October 2026/agentic-qa-rca-v3/development-records/20260913-agent-review-cycle-01/04_Agent_Activity_Log.md`
- `October 2026/agentic-qa-rca-v4/README.md` (Production Deployment / Local-Only Scope section)
- Artifact A: `Client requirements vs proposal comparizon.md`
- Artifact B: `CustomerActivityAndExceptionLogs sql scripts creation.md`
- Artifact D: `DOM_QA_Strategy_New_Requested_TestCases creation and json for ADO.md`
- Artifact F: `Performance_Testing_Meeting_Minutes.md`

### Artifact Description

The project-level config and prompt library show AI integrated as the default starting point for recurring QA tasks, and `copilot-instructions.md` documents the regulated-environment constraint that keeps daily use at single-prompt scope. The Agent Activity Log and v4 README show the agentic capability built and governed separately where policy allows. Artifacts A, B, D, and F are deliverables officially adopted by the team or client between April and July 2026.

---

# AI Output Validation & Governance

## Question

Describe how you audit AI outputs before committing them. How do you stress-test AI-generated solutions? Describe your process for edge case testing, security review, identifying architectural compliance issues, or hallucination in AI-authored code.

### Response

In my DOM project work, I don't produce or maintain code — there's no QA automation codebase to audit for "AI-authored code hallucination" in the traditional sense. My validation applies to documentation, SQL test-data scripts, test cases, and analysis artifacts. I maintain a structured validation log covering every AI-generated artifact delivered this review period: 8 outputs reviewed, with specific issues identified and resolved in each case where one existed, including a SQL logic error (`DATEADD()` rejecting a minutes parameter, corrected by converting to an hours-based calculation), two hallucinations caught and removed (an unsupported inferred requirements finding, and a reference to a security control — Azure Defender — not actually deployed in the project), a CSV/ADO import format fix, a meeting-minutes attribution correction, and full edge-case/boundary coverage confirmed for the 27-case test suite.

Where I do produce and validate AI-authored code is the separate QA RCA tool I designed, built, and maintain. There, I run a spec-driven, multi-agent development process with four specialized roles — Senior Backend Engineer, Senior Frontend Engineer, Senior Agentic Engineer (orchestration), and Senior QA Agent — that work from a written specification and a shared review rubric, not ad hoc prompting. Every change is gated behind explicit human-in-the-loop approval: nothing merges without a documented traceability link (finding → requirement → task → code → test → decision record) and a signed-off integration decision. This is not theoretical — in the most recent cycle (Oct 7–8) I personally executed the validation gate myself: ran the full unit test suite (46 tests, 1 skipped, all passing) plus 14 new tests targeting the specific changes, confirmed the golden-regression suite showed zero behavior drift after a refactor, and ran a live API-level security/error-handling check before approving the release. Security review is also structured, not ad hoc: the tool's architecture document defines explicit controls (CSP, path allowlists, output escaping) that were independently confirmed by a third-party automated production-readiness review with zero critical findings across 13 audited dimensions.

### Supporting Artifacts

- `July 2026/metrics-and-logs/AI_Output_Validation_Log.md`
- `.github/instructions/shared-agent-review-rubric.instructions.md`
- `.github/instructions/release-gate-checklist.instructions.md`
- `October 2026/agentic-qa-rca-v3/development-records/20260913-agent-review-cycle-01/09_Integration_Decision_Record.md`
- `October 2026/agentic-qa-rca-v3/development-records/20260913-agent-review-cycle-01/05_Traceability_Matrix.csv`
- `October 2026/agentic-qa-rca-v4/development-records/20261007-v4-evaluator-remediation/05_Traceability_Matrix.csv`
- `October 2026/agentic-qa-rca-v4/development-records/20261007-v4-evaluator-remediation/07_Governance_Gate_Checklist.md`
- `October 2026/agentic-qa-rca-v4/development-records/20261007-v4-evaluator-remediation/09_Integration_Decision_Record.md`
- `October 2026/agentic-qa-rca-v3/tests/test_v3_golden_regression.py`
- `October 2026/AI Agent Evaluator feedback report v3.md`

### Artifact Description

The validation log documents 8 reviewed documentation/data outputs with specific issues and corrections. The shared instructions files are the written spec/rubric the 4-agent process operates under. The traceability matrices and integration decision records show the finding→requirement→test→decision chain and the explicit human sign-off for both the September and the October (v4) engineering cycles. The v4 governance gate checklist records the actual test execution evidence (46+14 tests, golden regression) I ran before approving that release. The evaluator feedback report is third-party confirmation of the tool's security/architecture controls.

---

# Productivity & Measurable Impact

## Question

What data illustrates your AI usage is driving value? Cite specific metrics, not estimates, such as velocity gains or reduced cycle times, and identify an opportunity or manual bottleneck you've flagged for optimization.

### Response

The clearest productivity signal remains delivery outcome, not a time estimate: every AI-assisted deliverable produced between April and July was officially adopted — the QA strategy became the project's working testing baseline, the performance testing plan was adopted by client-side stakeholders, 27 test cases were imported into Azure DevOps and are in active execution, and the requirements comparison was delivered as a formal management report. A documented task-decomposition methodology estimates approximately 63.5 hours of effort redirected to higher-value work across those six deliverables; I'm presenting this as an estimate, not a measured metric, because the prospective tracking framework built to replace it has not yet produced its first dataset.

One new, dated, fully measured data point from this cycle: on October 7–8, I ran a complete remediation cycle against 9 named findings (F-001 through F-009) from a third-party production-readiness review, spanning backend, frontend, and documentation workstreams across two specialist engineering roles, validated end-to-end with 60 automated tests (46 existing + 14 new) — all passing, zero regressions confirmed against the golden-case baseline — completed within a single working session. This is a real cycle-time/throughput fact (9 findings, 60 tests, 1 session), not an estimate, though it measures remediation throughput rather than a velocity comparison against a pre-AI baseline.

The identified manual bottleneck is workload characterization and synthetic dataset creation for performance testing. I've built the instrumentation to close it (triage time, reopen rate, repeat-defect rate fields in a sprint-metrics framework) and have started a direct prospective time-tracking log this cycle to capture real before/after numbers on recurring tasks going forward, since the framework alone had produced zero collected data points to date.

### Supporting Artifacts

- `October 2026/metrics-and-logs/AI_Productivity_Metrics.md`
- `October 2026/metrics-and-logs/AI_Time_Tracking_Log.md`
- `July 2026/deliverables/[F] Performance_Testing_Meeting_Minutes.md`
- `October 2026/agentic-qa-rca-v4/development-records/20261007-v4-evaluator-remediation/04_Agent_Activity_Log.md`
- `October 2026/agentic-qa-rca-v4/development-records/20261007-v4-evaluator-remediation/07_Governance_Gate_Checklist.md`
- `October 2026/agentic-qa-rca-v3/metrics/sprint_metrics.csv`

### Artifact Description

The productivity metrics document provides the task-decomposition methodology for the 63.5-hour estimate (labeled as an estimate, not measured data). The v4 development records provide the new, dated, countable Oct 7–8 data (9 findings, 60 tests, 1 session). The time tracking log is the newly started prospective-measurement instrument, shown honestly alongside the still-empty sprint metrics framework.

---

# AI Agents, Automation & Advanced Workflows

## Question

How do you use AI agents, automated pipelines, workflows, or customized tools to solve complex project-specific challenges? If you maintain existing AI resources: how do you monitor them for reliability or degradation over time? Have you performed any prompt tuning, implemented fallback mechanisms, or customized tools with RAG or fine-tuned models?

### Response

In September, I designed and ran a scoped multi-agent engineering workflow — four specialized roles operating under a shared review rubric and release-gate checklist — to carry a defined set of QA-tool improvements from findings triage through specification, implementation, traceability mapping, and a formal integration decision, with every action logged and cross-referenced to requirement and finding IDs. This is the orchestration layer I designed and maintain: it is reusable for any future improvement cycle, not a one-time exercise.

I also built and maintain a project-specific tool — a root-cause-analysis and CAPA generation application — around a bounded, orchestrated three-step pipeline (planner → analyzer → validator) with hard iteration ceilings, structured per-step execution traces for transparency, and a versioned golden-case regression suite that runs automatically in CI on every change to guard against regression. This tool was independently reviewed twice by the GAP AI Toolkit's automated production-readiness evaluator: an initial review returned "Approved with Recommendations" with zero critical failures, and after I personally triaged and fixed 9 of its non-critical findings (dedicated error-lifecycle events, versioned/externalized prompt templates, documentation completeness, maintainer governance) across a one-session multi-role engineering cycle, a second independent re-review on October 8 confirmed every one of those 9 fixes landed — again "Approved with Recommendations," zero critical failures across all 13 audited dimensions. To be precise about scope: the application's runtime is deterministic and does not call an LLM, so prompt tuning, RAG, and fine-tuned models apply to the engineering process that designed and validated it, not to the application's own execution logic.

This agent-building pattern is not new to September: earlier this cycle, during GAP's Autonomous Engineer Intensive Training, I independently authored 3 custom Copilot agents and 2 custom skills on top of the standard Playwright MCP server, generating API test suites and defect-analysis reports against a public training target. I'm including it here as secondary evidence that agentic development is a sustained capability, not a one-time exercise.

### Supporting Artifacts

- `October 2026/agentic-qa-rca-v4/development-records/20261007-v4-evaluator-remediation/04_Agent_Activity_Log.md`
- `October 2026/agentic-qa-rca-v4/development-records/20261007-v4-evaluator-remediation/09_Integration_Decision_Record.md`
- `October 2026/agentic-qa-rca-v4/development-records/20261007-v4-evaluator-remediation/06_Metrics_Baseline_vs_After.csv`
- `October 2026/agentic-qa-rca-v4/src/orchestrator.py`
- `October 2026/agentic-qa-rca-v4/tests/test_v3_golden_regression.py`
- `October 2026/AI Agent Evaluator feedback report v3.md` (initial review)
- `October 2026/AI Agent Evaluator feedback report v5.md` (independent re-review confirming all 9 fixes)
- GitHub (secondary/training evidence): `https://github.com/jrmorac/AI-Training-Hackaton-project`

### Artifact Description

The activity log and integration decision record show the designed, reusable multi-agent engineering workflow applied twice: the September improvement cycle and the October 7 evaluator-remediation cycle. The metrics baseline-vs-after file maps each of the 9 fixed findings to its before/after evaluator status. The orchestrator and golden-regression tests show the deployed, monitored pipeline. The two evaluator feedback reports are independent, third-party, before/after confirmation of the application's production-readiness quality and of the specific fixes landing correctly. The GitHub repository is secondary evidence showing agent-authoring capability predates this cycle's in-project work — a public, single-author repository with custom Copilot agents and skills (built on top of the standard Playwright MCP server) driving API test-generation and defect-analysis reports during the Autonomous Engineer Intensive Training.

**Note: if the submission portal limits this question to 5 attachments, prioritize in this order:** v5 report → v3 report → Integration Decision Record → Metrics Baseline vs. After (Confirmed) → Architecture document. **Note: the portal does not accept `.csv` or `.py` files** — use `06_Metrics_Baseline_vs_After_Confirmed.md` (markdown version with real v5-confirmed results, replaces the `.csv`) and `ARCHITECTURE_AND_EVALUATOR_APPLICABILITY.md` (replaces `orchestrator.py` — already `.md`, contains the Mermaid diagram of the same planner→analyzer→validator pipeline). Drop the Agent Activity Log, golden-regression test file, and GitHub repo last (their value is substantially covered by the five above, or by Q1/Q5 where the GitHub repo is already attached).

---

# Scaling AI Impact

## Question

Describe any actions you've taken to extend AI value beyond your own work. This could include: contributing reusable assets, leading or participating in internal AI initiatives, mentoring peers, or demonstrating tangible AI Return On Investment.

### Response

I built and published two reusable assets this cycle: a six-template QA prompt library for recurring documentation, SQL test-data, and test-case tasks, and a fully packaged, team-shareable version of the RCA/CAPA application — including a quick-start README, one-command environment check and launch scripts, and compliance-safe onboarding guidance — so any teammate can run it locally without CLI experience. I also authored a leadership-facing presentation script framing the tool as a reusable pattern for regulated-environment QA work, ready for delivery to engineering and delivery leadership.

Beyond this project, my July deliverables already demonstrate AI value extending past my own task list: the QA strategy I produced is the team's standing testing baseline, the performance testing plan was adopted by client-side stakeholders as the official testing approach, and the 27 test cases I generated are in active use by the broader test execution effort. I completed GAP's Autonomous Engineer Intensive Training (now "Intro to Agentic Development") and Anthropic's Claude 101 course this cycle, building the orchestration and prompt-design foundation behind the September multi-agent workflow. That training translated into a tangible build, not just course completion: I authored custom Copilot agents and skills on top of a standard MCP server during the training, retained publicly as secondary evidence of applied capability. My near-term next step is delivering the prepared leadership presentation and collecting direct teammate usage of the shareable package.

### Supporting Artifacts

- `prompts/README.md` and `prompts/TEAM-GUIDE.md`
- `October 2026/agentic-qa-rca-shareable-v3/README.md`
- `October 2026/deliverables/GAP_Leadership_Presentation_Script_Agentic_QA_RCA.md`
- `July 2026/certificates/Autonomous_Engineer_Intensive_Training_-_Certificate.pdf`
- `July 2026/certificates/certificate-u6d3dqgyn2hx-1778113791-claude-101.pdf`
- Artifact C: `dom_performance_testing_strategy.html`
- Artifact D: `DOM_QA_Strategy_New_Requested_TestCases creation and json for ADO.md`
- GitHub (secondary/training evidence): `https://github.com/jrmorac/AI-Training-Hackaton-project`

### Artifact Description

The prompt library and shareable package are the reusable assets created for team use. The presentation script shows leadership-level initiative in progress. The training certificates document the capability-building behind this cycle's agentic work. Artifacts C and D show prior deliverables already adopted by the team and client. The GitHub repository is secondary evidence that the training certificate corresponds to real applied building (custom agents and skills authored on top of the standard Playwright MCP server), not just attendance.

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

Where I do produce and validate AI-authored code is the separate QA RCA tool I designed, built, and maintain. There, I run a spec-driven, multi-agent development process with four specialized roles — Senior Backend Engineer, Senior Frontend Engineer, Senior Agentic Engineer (orchestration), and Senior QA Agent — that work from a written specification and a shared review rubric, not ad hoc prompting. Code changes go through human review, test evidence, traceability (finding → requirement → task → code → test → decision record), and an integration decision. In the most recent cycle (Oct 7–8), the full discovered unit suite ran 46 tests (1 skipped), including 14 new targeted cases; those 14 were also run separately (14/14 passed). The golden-regression suite and a live API-level security/error-handling check also passed. A subsequent v4 pilot by Maria, a QA colleague from another account, demonstrated why human validation must continue after automated tests and evaluator review: she found that CAPA/ADO export UI actions bypass the documented explicit approval interaction. I verified and logged this as an open corrective issue rather than claiming the export paths are safe; broader distribution is on hold pending a fix and regression tests. The v5 Toolkit review found zero critical failures in its audit scope, but it did not detect this pilot finding.

### Supporting Artifacts

- `July 2026/metrics-and-logs/AI_Output_Validation_Log.md`
- `.github/instructions/shared-agent-review-rubric.instructions.md`
- `.github/instructions/release-gate-checklist.instructions.md`
- `October 2026/agentic-qa-rca-v3/development-records/20260913-agent-review-cycle-01/09_Integration_Decision_Record.md`
- `October 2026/agentic-qa-rca-v4/development-records/20261007-v4-evaluator-remediation/08_Code_Review_Findings.md`
- `October 2026/agentic-qa-rca-v4/development-records/20261007-v4-evaluator-remediation/07_Governance_Gate_Checklist.md`
- `October 2026/agentic-qa-rca-v4/development-records/20261007-v4-evaluator-remediation/09_Integration_Decision_Record.md`
- `October 2026/agentic-qa-rca-v4/development-records/20261007-v4-evaluator-remediation/10_Risk_and_Rollback_Register.md`
- `July 2026/prompt-library/Prompt_Library_Sharing_Record.md` (Maria's pilot feedback)
- `October 2026/AI Agent Evaluator feedback report v3.md`
- `October 2026/AI Agent Evaluator feedback report v5.md`

### Artifact Description

The validation log documents 8 reviewed documentation/data outputs with specific issues and corrections. The shared instructions files are the written spec/rubric the 4-agent process operates under. The code-review findings, governance gate checklist, and integration decision record document the traceability chain, the 46-test full-suite run (including 14 new targeted cases), golden regression, and human decision. The two evaluator reports provide third-party before/after confirmation. Maria's pilot feedback and the risk register show a gap the automated review missed and the corrective action still open. The raw traceability matrices (`.csv`) and golden-regression test file (`.py`) remain in the repository for audit traceability but are not attached because the portal rejects those file types.

**If limited to 5 attachments for this question, prioritize:** AI Output Validation Log → v4 Governance Gate Checklist → v4 Integration Decision Record → v5 Evaluator Report → Prompt Library Sharing Record (Maria's pilot finding). The shared rubric/release-gate instructions, code-review report, and raw CSV/Python test sources remain in the repository for reference.

---

# Productivity & Measurable Impact

## Question

What data illustrates your AI usage is driving value? Cite specific metrics, not estimates, such as velocity gains or reduced cycle times, and identify an opportunity or manual bottleneck you've flagged for optimization.

### Response

The clearest productivity signal remains delivery outcome, not a time estimate: every AI-assisted deliverable produced between April and July was officially adopted — the QA strategy became the project's working testing baseline, the performance testing plan was adopted by client-side stakeholders, 27 test cases were imported into Azure DevOps and are in active execution, and the requirements comparison was delivered as a formal management report. A documented task-decomposition methodology estimates approximately 63.5 hours of effort redirected to higher-value work across those six deliverables; I'm presenting this as an estimate, not a measured metric, because the prospective tracking framework built to replace it has not yet produced its first dataset.

One new, dated, countable data point from this cycle: on October 7–8, I ran a remediation cycle against 9 named findings (F-001 through F-009) from a third-party production-readiness review, spanning backend, frontend, and documentation workstreams across two specialist engineering roles. The full discovered suite ran 46 tests (1 skipped), including 14 new targeted cases; all executed tests passed, and the golden-case regression remained unchanged. The 14 targeted tests were also rerun separately, not added to the full-suite count. The cycle took one working session. This documents remediation throughput (9 findings, 46 full-suite tests, 1 session), not a velocity comparison against a pre-AI baseline.

The identified manual bottleneck is workload characterization and synthetic dataset creation for performance testing. I've built the instrumentation to close it (triage time, reopen rate, repeat-defect rate fields in a sprint-metrics framework) and have started a direct prospective time-tracking log this cycle to capture real before/after numbers on recurring tasks going forward, since the framework alone had produced zero collected data points to date.

### Supporting Artifacts

- `October 2026/metrics-and-logs/AI_Productivity_Metrics.md`
- `October 2026/metrics-and-logs/AI_Time_Tracking_Log.md`
- `July 2026/deliverables/[F] Performance_Testing_Meeting_Minutes.md`
- `October 2026/agentic-qa-rca-v4/development-records/20261007-v4-evaluator-remediation/04_Agent_Activity_Log.md`
- `October 2026/agentic-qa-rca-v4/development-records/20261007-v4-evaluator-remediation/07_Governance_Gate_Checklist.md`
- `October 2026/agentic-qa-rca-v4/development-records/20261007-v4-evaluator-remediation/06_Metrics_Baseline_vs_After_Confirmed.md`

### Artifact Description

The productivity metrics document provides the task-decomposition methodology for the 63.5-hour estimate (labeled as an estimate, not measured data). The v4 development records provide the new, dated, countable Oct 7–8 data (9 findings, 46 full-suite tests, 1 session; the 14 targeted tests are included in the 46 and were rerun separately). The time tracking log is the newly started prospective-measurement instrument, shown honestly alongside the still-empty sprint metrics framework. The raw `sprint_metrics.csv` is retained in the repository but not attached because the portal rejects CSV files.

---

# AI Agents, Automation & Advanced Workflows

## Question

How do you use AI agents, automated pipelines, workflows, or customized tools to solve complex project-specific challenges? If you maintain existing AI resources: how do you monitor them for reliability or degradation over time? Have you performed any prompt tuning, implemented fallback mechanisms, or customized tools with RAG or fine-tuned models?

### Response

In September, I designed and ran a scoped multi-agent engineering workflow — four specialized roles operating under a shared review rubric and release-gate checklist — to carry a defined set of QA-tool improvements from findings triage through specification, implementation, traceability mapping, and a formal integration decision, with every action logged and cross-referenced to requirement and finding IDs. This is the orchestration layer I designed and maintain: it is reusable for any future improvement cycle, not a one-time exercise.

I also built and maintain a project-specific tool — a root-cause-analysis and CAPA generation application — around a bounded, orchestrated three-step pipeline (planner → analyzer → validator) with hard iteration ceilings, structured per-step execution traces for transparency, and a versioned golden-case regression suite that runs automatically in CI on every change to guard against regression. The GAP AI Toolkit reviewed it twice: the initial review returned "Approved with Recommendations," and an independent v5 re-review on October 8 confirmed all 9 targeted non-critical fixes landed, again with zero critical findings across 13 audited dimensions. A subsequent v4 pilot by a Staff QA Engineer from another account exposed an export-governance gap the automated reviews did not catch: the CAPA and ADO export UI actions use convenience endpoints that internally approve and write exports, bypassing the documented explicit preview/approval interaction. I recorded this as an open corrective item; I will not claim those UI paths enforce user approval until the behavior is corrected and regression-tested. The runtime is deterministic and does not call an LLM, so prompt tuning, RAG, and fine-tuned models apply to the engineering process, not runtime inference.

This agent-building pattern is not new to September: earlier this cycle, during GAP's Autonomous Engineer Intensive Training, I independently authored 3 custom Copilot agents and 2 custom skills on top of the standard Playwright MCP server, generating API test suites and defect-analysis reports against a public training target. I'm including it here as secondary evidence that agentic development is a sustained capability, not a one-time exercise.

### Supporting Artifacts

- `October 2026/agentic-qa-rca-v4/development-records/20261007-v4-evaluator-remediation/04_Agent_Activity_Log.md`
- `October 2026/agentic-qa-rca-v4/development-records/20261007-v4-evaluator-remediation/09_Integration_Decision_Record.md`
- `October 2026/agentic-qa-rca-v4/development-records/20261007-v4-evaluator-remediation/06_Metrics_Baseline_vs_After_Confirmed.md`
- `October 2026/agentic-qa-rca-v4/ARCHITECTURE_AND_EVALUATOR_APPLICABILITY.md`
- `October 2026/AI Agent Evaluator feedback report v3.md` (initial review)
- `October 2026/AI Agent Evaluator feedback report v5.md` (independent re-review confirming all 9 fixes)
- `July 2026/prompt-library/Prompt_Library_Sharing_Record.md` (Maria's v4 pilot use and feedback)
- GitHub (secondary/training evidence): `https://github.com/jrmorac/AI-Training-Hackaton-project`

### Artifact Description

The activity log and integration decision record show the reusable multi-agent engineering workflow applied in September and October. The before/after evaluator reports confirm the 9 targeted fixes, while Maria's cross-account v4 pilot adds real user testing and surfaced an export-approval gap that remains open for correction. The architecture document provides an upload-safe representation of the pipeline and its declared boundaries. The source `.py` implementation and `.csv` baseline, plus the golden-regression test file, remain in the repository for traceability but are not listed as portal attachments because the portal rejects those file types. The GitHub repository is secondary evidence of earlier agent-authoring capability.

**Note: if the submission portal limits this question to 5 attachments, prioritize in this order:** v5 report → v3 report → Integration Decision Record → Metrics Baseline vs. After (Confirmed) → Architecture document. The portal rejects `.csv` and `.py` files; the upload-safe markdown equivalents are listed above. The original source CSV, Python implementation, and golden-regression test remain in the repository for traceability but are not portal attachments. The activity log, sharing record, and GitHub repo are secondary options if the portal permits more than five.

---

# Scaling AI Impact

## Question

Describe any actions you've taken to extend AI value beyond your own work. This could include: contributing reusable assets, leading or participating in internal AI initiatives, mentoring peers, or demonstrating tangible AI Return On Investment.

### Response

I built and published two reusable assets this cycle: a six-template QA prompt library for recurring documentation, SQL test-data, and test-case tasks, and a packaged, team-shareable version of the RCA/CAPA application with a quick-start README, environment-check and launch scripts, and synthetic-data onboarding guidance. A Staff QA Engineer from another account tested v4 in the browser, ran a demo and manual RCA session, and exercised CAPA export. She reported that the demo and manual session worked without console errors, and provided actionable feedback on startup behavior, session/evidence suggestions, and an export-approval mismatch. This is concrete cross-account pilot use and feedback, but not evidence of broad or sustained adoption or measured ROI; the export-governance issue is recorded for correction before wider distribution. I also authored a leadership-facing presentation script, ready for delivery to engineering and delivery leadership.

On October 7, a colleague asked for advice on creating agents to test and improve API endpoints with Postman. I shared my public Autonomous Engineer hackathon repository and pointed her to the custom agent definitions in `.github/agents/` and skills in `.vscode/skills/`. She replied that she would explore it. This documents knowledge-sharing and colleague interest; I do not yet claim she used or adopted the agents or that this interaction produced measurable impact.

Beyond this project, my July deliverables already demonstrate AI value extending past my own task list: the QA strategy I produced is the team's standing testing baseline, the performance testing plan was adopted by client-side stakeholders as the official testing approach, and the 27 test cases I generated are in active use by the broader test execution effort. I completed GAP's Autonomous Engineer Intensive Training and Anthropic's Claude 101 course this cycle, building the orchestration and prompt-design foundation behind the September multi-agent workflow. That training translated into a tangible build, not just course completion: I authored custom Copilot agents and skills on top of a standard MCP server during the training, retained publicly as secondary evidence of applied capability. My next step is to correct the export-approval issue and continue the pilot; I am not claiming sustained adoption from one test.

### Supporting Artifacts

- `prompts/README.md` and `prompts/TEAM-GUIDE.md`
- `October 2026/agentic-qa-rca-shareable-v4/README.md`
- `July 2026/prompt-library/Prompt_Library_Sharing_Record.md` (RCA Adoption Entry 001: v4 pilot)
- `October 2026/deliverables/GAP_Leadership_Presentation_Script_Agentic_QA_RCA.md`
- Teams screenshot of the Oct 7 hackathon-agent/skills knowledge-share with Sonia Sijia (colleague reply: "voy a explorar")
- `July 2026/certificates/Autonomous_Engineer_Intensive_Training_-_Certificate.pdf`
- `July 2026/certificates/certificate-u6d3dqgyn2hx-1778113791-claude-101.pdf`
- Artifact C: `dom_performance_testing_strategy.html`
- Artifact D: `DOM_QA_Strategy_New_Requested_TestCases creation and json for ADO.md`
- GitHub (secondary/training evidence): `https://github.com/jrmorac/AI-Training-Hackaton-project`

### Artifact Description

The prompt library and shareable package are reusable assets. Maria's v4 pilot documents actual cross-account use and actionable feedback, including an issue now tracked for correction. The Oct 7 Teams screenshot documents a separate knowledge-sharing interaction: I shared the hackathon repository and Sonia said she would explore it; this is interest, not confirmed adoption. The presentation script shows leadership-level initiative in progress. Training certificates and the public repository connect capability-building to the custom agents and skills I authored on top of the standard Playwright MCP server. Artifacts C and D show prior deliverables already adopted by the team and client.

**If the portal limits this question to 5 attachments, prioritize:** (1) `Prompt_Library_Sharing_Record.md` (both the v4 pilot and hackathon share are logged), (2) Maria's written pilot feedback email, (3) the Oct 7 Teams screenshot with Sonia, (4) `prompts/TEAM-GUIDE.md` (reusable asset), and (5) Artifact D (27 test cases in active execution). Keep the full list above for the record; do not describe Sonia's interest as adoption or Maria's single pilot as sustained use.

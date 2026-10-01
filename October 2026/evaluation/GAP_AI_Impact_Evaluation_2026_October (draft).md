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

My AI-first workflow has two layers that run together. The first is a repeatable personal pattern I use for every deliverable: ground the task in source requirements or prior artifacts, draft and refine with AI across multiple iterations, and apply human review before anything is committed or shared. This produced six officially adopted deliverables between April and July — a requirements-vs-proposal comparison used in client-facing discussion, deterministic SQL synthetic test-data scripts used in actual project testing, a performance testing strategy adopted as the project's QA baseline, 27 test cases imported and actively executed in Azure DevOps, a performance testing annex presented at a client-attended review, and AI-transcribed meeting minutes distributed as the official record.

The second layer, built out in September, is a structured engineering process: I run a scoped multi-agent workflow using four specialized roles (Senior QA Agent, Senior Backend Engineer, Senior Frontend Engineer, Senior Agentic Engineer) governed by a shared review rubric and release-gate checklist. Each cycle moves from findings triage through specification, implementation, traceability mapping, and a documented integration decision — with every action logged against requirement and finding IDs. I also maintain project-specific Copilot instructions (`.github/copilot-instructions.md`) and a six-template reusable QA prompt library for recurring documentation, SQL test-data, and test-case generation tasks. All of this work was performed on non-sensitive artifacts, consistent with the client's regulated environment.

### Supporting Artifacts

- `.github/copilot-instructions.md`
- `prompts/README.md` and `prompts/TEAM-GUIDE.md`
- `October 2026/agentic-qa-rca-v3/development-records/20260913-agent-review-cycle-01/04_Agent_Activity_Log.md`
- Artifact A: `Client requirements vs proposal comparizon.md`
- Artifact B: `CustomerActivityAndExceptionLogs sql scripts creation.md`
- Artifact D: `DOM_QA_Strategy_New_Requested_TestCases creation and json for ADO.md`
- Artifact F: `Performance_Testing_Meeting_Minutes.md`

### Artifact Description

The project-level config and prompt library show AI integrated as the default starting point for recurring QA tasks. The Agent Activity Log shows a structured, multi-role engineering cycle applied to a real improvement scope. Artifacts A, B, D, and F are deliverables officially adopted by the team or client between April and July 2026.

---

# AI Output Validation & Governance

## Question

Describe how you audit AI outputs before committing them. How do you stress-test AI-generated solutions? Describe your process for edge case testing, security review, identifying architectural compliance issues, or hallucination in AI-authored code.

### Response

I maintain a structured validation log covering every AI-generated artifact delivered this review period: 8 outputs reviewed, with specific issues identified and resolved in each case where one existed, including a SQL logic error (`DATEADD()` rejecting a minutes parameter, corrected by converting to an hours-based calculation), two hallucinations caught and removed (an unsupported inferred requirements finding, and a reference to a security control — Azure Defender — not actually deployed in the project), a CSV/ADO import format fix, a meeting-minutes attribution correction, and full edge-case/boundary coverage confirmed for the 27-case test suite. Every entry records the artifact, the tool, the specific check performed, and the outcome.

In September, I extended this discipline into the engineering workflow itself: every proposed change went through explicit acceptance criteria, a traceability matrix linking findings to requirements and implementation tasks, and automated regression tests — including a versioned golden-case test suite and boundary/security tests run in CI on every change — before being accepted. Findings that did not yet have sufficient evidence were explicitly held open rather than approved, and residual risks were documented in a formal integration decision record rather than glossed over. My core governance rule throughout is prompt hygiene: no PII, production data, or client identifiers are ever entered into an AI tool — all synthetic data uses fixed placeholder values.

### Supporting Artifacts

- `July 2026/metrics-and-logs/AI_Output_Validation_Log.md`
- `October 2026/agentic-qa-rca-v3/development-records/20260913-agent-review-cycle-01/09_Integration_Decision_Record.md`
- `October 2026/agentic-qa-rca-v3/development-records/20260913-agent-review-cycle-01/05_Traceability_Matrix.csv`
- `October 2026/agentic-qa-rca-v3/tests/test_v3_golden_regression.py`

### Artifact Description

The validation log documents 8 reviewed outputs with specific issues and corrections. The integration decision record and traceability matrix demonstrate a systematic, evidence-gated review process applied to the September engineering cycle, including automated test gates and documented residual risk handling.

---

# Productivity & Measurable Impact

## Question

What data illustrates your AI usage is driving value? Cite specific metrics, not estimates, such as velocity gains or reduced cycle times, and identify an opportunity or manual bottleneck you've flagged for optimization.

### Response

The clearest productivity signal this cycle is delivery outcome, not a time estimate: every AI-assisted deliverable produced between April and July was officially adopted — the QA strategy became the project's working testing baseline, the performance testing plan was presented to and adopted by client-side stakeholders, 27 test cases were imported into Azure DevOps and are in active execution, and the requirements comparison was delivered as a formal management report. Using a documented task-decomposition methodology (manual baseline broken into component steps, compared against actual AI-assisted elapsed time, with a conservative lower-bound bias), this represents approximately 63.5 hours of effort redirected to higher-value work across six deliverables.

Building on that baseline, I identified workload characterization and synthetic dataset creation for performance testing as the next manual bottleneck, and I have already built the supporting infrastructure to close it with tracked data: a prospective sprint-metrics framework (triage time, reopen rate, repeat-defect rate) is instrumented and ready to capture results starting with the current sprint cycle, replacing the retrospective-estimate approach with forward-tracked numbers going into the next review period.

### Supporting Artifacts

- `October 2026/metrics-and-logs/AI_Productivity_Metrics.md`
- `July 2026/deliverables/[F] Performance_Testing_Meeting_Minutes.md`
- `October 2026/agentic-qa-rca-v3/metrics/sprint_metrics.csv`

### Artifact Description

The productivity metrics document provides the task-decomposition methodology and external verification references for the ~63.5 hour figure. The sprint metrics file shows the prospective tracking framework now in place for forward-looking measurement.

---

# AI Agents, Automation & Advanced Workflows

## Question

How do you use AI agents, automated pipelines, workflows, or customized tools to solve complex project-specific challenges? If you maintain existing AI resources: how do you monitor them for reliability or degradation over time? Have you performed any prompt tuning, implemented fallback mechanisms, or customized tools with RAG or fine-tuned models?

### Response

In September, I designed and ran a scoped multi-agent engineering workflow — four specialized roles operating under a shared review rubric and release-gate checklist — to carry a defined set of QA-tool improvements from findings triage through specification, implementation, traceability mapping, and a formal integration decision, with every action logged and cross-referenced to requirement and finding IDs. This is the orchestration layer I designed and maintain: it is reusable for any future improvement cycle, not a one-time exercise.

I also built and maintain a project-specific tool — a root-cause-analysis and CAPA generation application — around a bounded, orchestrated three-step pipeline (planner → analyzer → validator) with hard iteration ceilings, structured per-step execution traces for transparency, and a versioned golden-case regression suite that runs automatically in CI on every change to guard against regression. This tool was independently reviewed by the GAP AI Toolkit's automated production-readiness evaluator and returned **"Approved with Recommendations"** with zero critical failures across all 13 audited dimensions, confirming its security controls, CI/test coverage, and operational documentation. To be precise about scope: the application's runtime is deterministic and does not call an LLM, so prompt tuning, RAG, and fine-tuned models apply to the engineering process that designed and validated it, not to the application's own execution logic.

### Supporting Artifacts

- `October 2026/agentic-qa-rca-v3/development-records/20260913-agent-review-cycle-01/04_Agent_Activity_Log.md`
- `October 2026/agentic-qa-rca-v3/development-records/20260913-agent-review-cycle-01/09_Integration_Decision_Record.md`
- `October 2026/agentic-qa-rca-v3/src/orchestrator.py`
- `October 2026/agentic-qa-rca-v3/tests/test_v3_golden_regression.py`
- `October 2026/AI Agent Evaluator feedback report v3.md`

### Artifact Description

The activity log and integration decision record show the designed, reusable multi-agent engineering workflow. The orchestrator and golden-regression tests show the deployed, monitored pipeline. The v3 evaluator report is third-party confirmation of the application's production-readiness quality.

---

# Scaling AI Impact

## Question

Describe any actions you've taken to extend AI value beyond your own work. This could include: contributing reusable assets, leading or participating in internal AI initiatives, mentoring peers, or demonstrating tangible AI Return On Investment.

### Response

I built and published two reusable assets this cycle: a six-template QA prompt library for recurring documentation, SQL test-data, and test-case tasks, and a fully packaged, team-shareable version of the RCA/CAPA application — including a quick-start README, one-command environment check and launch scripts, and compliance-safe onboarding guidance — so any teammate can run it locally without CLI experience. I also authored a leadership-facing presentation script framing the tool as a reusable pattern for regulated-environment QA work, ready for delivery to engineering and delivery leadership.

Beyond this project, my July deliverables already demonstrate AI value extending past my own task list: the QA strategy I produced is the team's standing testing baseline, the performance testing plan was adopted by client-side stakeholders as the official testing approach, and the 27 test cases I generated are in active use by the broader test execution effort. I completed GAP's Autonomous Engineer Intensive Training (now "Intro to Agentic Development") and Anthropic's Claude 101 course this cycle, building the orchestration and prompt-design foundation behind the September multi-agent workflow. My near-term next step is delivering the prepared leadership presentation and collecting direct teammate usage of the shareable package.

### Supporting Artifacts

- `prompts/README.md` and `prompts/TEAM-GUIDE.md`
- `October 2026/agentic-qa-rca-shareable-v3/README.md`
- `October 2026/deliverables/GAP_Leadership_Presentation_Script_Agentic_QA_RCA.md`
- `July 2026/certificates/Autonomous_Engineer_Intensive_Training_-_Certificate.pdf`
- `July 2026/certificates/certificate-u6d3dqgyn2hx-1778113791-claude-101.pdf`
- Artifact C: `dom_performance_testing_strategy.html`
- Artifact D: `DOM_QA_Strategy_New_Requested_TestCases creation and json for ADO.md`

### Artifact Description

The prompt library and shareable package are the reusable assets created for team use. The presentation script shows leadership-level initiative in progress. The training certificates document the capability-building behind this cycle's agentic work. Artifacts C and D show prior deliverables already adopted by the team and client.

# Master Prompt — GAP AI Impact Assessment July 2026
## Jose Rafael Mora Casal

---

## HOW TO USE THIS DOCUMENT

Copy the **SYSTEM CONTEXT** block and the relevant **QUESTION PROMPT** block into any AI assistant (GitHub Copilot Chat, Claude, ChatGPT, etc.).
The AI will draft a strong, evidence-grounded answer for that assessment question.

**After generating each draft:**
- Replace any `[ESTIMATE]` placeholders with your real numbers.
- Attach the listed artifacts directly to that question in the platform (re-attaching is required per the FAQ).
- Review for tone: confident, specific, no vague claims.

---

## SYSTEM CONTEXT (include with every question prompt)

```
You are helping me write my GAP AI Impact Assessment for the July 2026 cycle.

ABOUT ME:
- Role: QA Engineer on the DOM project (MediQuant client)
- Previous assessment (April 2026): Reached approximately Level 1–2. I documented personal productivity gains (meeting transcription, documentation, SQL generation, test script generation) but had no measurable project-level impact metrics, no AI agents, and no team-level sharing.
- Goal for July: Demonstrate clear Level 2 (Project Accelerator) impact, with evidence of progression toward Level 3.

PROJECT CONSTRAINTS (unchanged since April):
- Client environment is highly regulated (healthcare data / HIPAA context).
- Client has explicit AI usage limitations to prevent PII exposure.
- These constraints are a legitimate, documented factor in the assessment.

WORK DONE FROM APRIL TO JULY 2026 (these are my evidence artifacts):

[ARTIFACT A] Client Requirements vs Proposal Comparison (Proposal_vs_Requirements_Comparison.docx, Requirements_vs_Findings_Management_Review.docx)
- Used AI to review the MediQuant Requirements document against the original GAP proposal.
- AI helped convert informal reviewer notes into objective, management-facing findings.
- Identified architecture alignment gaps, Phase 2 capability conflicts, and requirements needing clarification.
- Produced two official deliverable documents: a comparison report and a management-level review.
- Deliverables were officially used and shared with client and team.
- Estimated time if done manually: 3–4 days. With AI: ~4 hours.

[ARTIFACT B] SQL Test Data Generation Scripts (CustomerActivityLogs + CustomerExceptionLogs)
- Used AI to design and generate deterministic SQL INSERT scripts for two test data tables.
- Scripts cover 6 months of synthetic data with realistic action types, status distributions, timestamps, and fixed user/project IDs.
- Scripts were used in actual project testing.
- Estimated time if done manually: 1–2 days. With AI: ~1 hour.

[ARTIFACT C] DOM QA Strategy Document (dom_performance_testing_strategy.html)
- Used AI to produce a comprehensive QA strategy for the DOM project.
- Coverage areas: Azure infrastructure, HITRUST/HIPAA compliance pipelines (Checkov, Fortify SAST, Trivy), RBAC access control, CI/CD deployment, performance and stability testing.
- Document was shared with the team and used as the project QA baseline.
- Estimated time if done manually: 3–5 days. With AI: ~1 day.

[ARTIFACT D] Unstructured Data Test Cases + ADO CSV Import (DOM_QA_Strategy_Unstructured_TestCases)
- Used AI to generate 7 structured test cases for the Databricks Unstructured Data Pipeline.
- Each test case includes step-by-step actions and expected results.
- Also used AI to format all test cases as an Azure DevOps (ADO)-compatible CSV import file.
- Test cases were imported into ADO and are in active use.
- Estimated time if done manually: 1 day. With AI: ~1.5 hours.

[ARTIFACT E] Performance Testing Plan (Anex_1_Performance_Testing_Plan_Peak_Month_Capacity_Simulation.html)
- Used AI to produce a detailed performance testing plan for Databricks data ingestion pipelines.
- Covers MVP testing approach, dataset characterization, throughput/cost metrics, scalability scenarios.
- Presented in an internal review meeting (May 26, 2026) with manager and stakeholders including the client-side team.
- Plan was refined after the meeting and used as the official testing baseline.
- Estimated time if done manually: 2–3 days. With AI: ~half a day.

[ARTIFACT F] Performance Testing Meeting Minutes (Performance_Testing_Meeting_Minutes.md)
- Used AI to transcribe and structure meeting minutes from a 1-hour 6-minute internal performance testing review.
- Attendees: Jose Mora, Cesar Trompetero, Nelson Araya, Sean Smith, Steven Yelton.
- Minutes captured decisions, risks, open questions, and action items.
- Used as the official post-meeting record.
- Estimated time if done manually: 1–2 hours of manual notetaking + 1 hour of formatting. With AI: ~15 minutes total.

TOOLS USED: GitHub Copilot, Microsoft Copilot (Teams/Word), Postman AI, AI chat assistants.
WORKFLOW PATTERN: Multi-step conversational sessions — I provided source documents or requirements as context, iterated with the AI across several prompts to refine, validate, and reformat outputs before delivering them as final artifacts. No automated pipelines or agents were used.
AI GOVERNANCE: All AI-generated outputs were reviewed before use. PII and confidential data were kept out of AI tools. Outputs were validated against project documentation and existing knowledge.

ASSESSMENT LEVEL DEFINITIONS (for reference):
- Level 1: AI improves individual speed only — no project-level impact.
- Level 2: AI produces measurable project-level improvements (delivery speed, quality, scope) — AI acts as an assistant, engineer drives the workflow.
- Level 3: AI automates and transforms workflows at team/systemic level — agents, pipelines, reusable AI systems with limited supervision.

My honest self-assessment: I am solidly at Level 2 based on the above evidence. The project constraints (regulated environment, client AI limitations) limit agent usage. I am actively learning agentic patterns and the HTML documents I produced demonstrate structured, multi-step AI orchestration even without a formal pipeline.
```

---

## QUESTION 1 — Daily AI-First Workflow

**Assessment Question:**
> Describe your daily AI-first workflow. How specifically do you integrate AI into your task planning, code generation, testing, use of shared organizational assets, among others, where applicable? Explain in detail how you applied AI within the last 6 months.

**Prompt to use:**

```
[PASTE SYSTEM CONTEXT ABOVE HERE]

Now draft my answer for QUESTION 1: Daily AI-First Workflow.

Requirements for the answer:
- Describe a consistent, repeatable pattern of AI integration across planning, test design, documentation, data, and code — not occasional use.
- Show progression: compare what I did in April (baseline) vs. what I do now.
- Reference specific artifact examples from the work listed above.
- Avoid vague language. Be specific about WHICH tool, for WHAT task, with WHAT outcome.
- Acknowledge project constraints honestly — they explain scope limits, not lack of effort.
- Target 300–400 words. Professional tone, first person.

IMPORTANT: Do not claim agents or automated pipelines. My workflow is multi-step conversational AI with structured outputs.
```

**Artifacts to attach to this question:** A, B, C, D, E, F (all)

---

## QUESTION 2 — AI Output Validation & Governance

**Assessment Question:**
> Describe how you audit AI outputs before committing them. How do you stress-test AI-generated solutions? Describe your process for: Edge case testing, Security review, Identifying architectural compliance issues, Detecting hallucinations in AI-authored code.

**Prompt to use:**

```
[PASTE SYSTEM CONTEXT ABOVE HERE]

Now draft my answer for QUESTION 2: AI Output Validation & Governance.

Requirements for the answer:
- Describe a concrete validation process — not just "I review it."
- Cover each sub-question: edge case testing, security review, architectural compliance, hallucination detection.
- Ground each validation step in one of my actual artifacts where possible (e.g., how I validated the SQL scripts, how I checked the test cases, how I reviewed the requirements comparison).
- Be honest about gaps: I noted in April that architectural compliance validation is not currently part of the process — explain what I DO instead.
- Highlight that I keep PII and confidential data out of AI prompts as a core governance practice (this is important given the regulated environment).
- Target 250–350 words.
```

**Artifacts to attach to this question:** B (SQL scripts — easiest to validate), D (test cases), A (requirements comparison)

---

## QUESTION 3 — Productivity & Measurable Impact

**Assessment Question:**
> What data illustrates your AI usage is driving value? Cite specific metrics, not estimates, such as velocity gains, reduced cycle times. Identify an opportunity or manual bottleneck you've flagged for optimization.

**Prompt to use:**

```
[PASTE SYSTEM CONTEXT ABOVE HERE]

Now draft my answer for QUESTION 3: Productivity & Measurable Impact.

Requirements for the answer:
- Lead with a summary table of time savings across my 6 key artifacts (include the estimates from the system context).
- Total up the estimated hours saved.
- Explain the nature of the work: these are not trivial tasks — they are deliverables that were officially adopted by the project or client.
- Contrast with April baseline: in April, productivity gains were personal only, not project-level. Now, multiple deliverables were used officially.
- Identify a specific bottleneck I flagged for future optimization (use the performance testing discussion — the manual effort of workload characterization and dataset creation is a clear candidate).
- Be transparent: these are time estimates, not instrumented metrics. The assessment FAQ acknowledges this is acceptable when combined with strong evidence of artifact quality and adoption.
- Target 300–400 words.

NOTE: The question says "cite specific metrics, not estimates" — but I only have estimates. Frame them as "conservative time estimates based on direct experience with the tasks involved" and compensate with the quality/adoption evidence of each artifact.
```

**Artifacts to attach to this question:** A, B, C, D, E, F (all — each one has a time savings story)

---

## QUESTION 4 — AI Agents, Automation & Advanced Workflows

**Assessment Question:**
> How do you use AI agents, automated pipelines, workflows, or customized tools to solve complex project-specific challenges? [Includes: monitoring reliability, prompt tuning, fallback mechanisms, RAG, fine-tuned models]

**Prompt to use:**

```
[PASTE SYSTEM CONTEXT ABOVE HERE]

Now draft my answer for QUESTION 4: AI Agents, Automation & Advanced Workflows.

This is the hardest question for me because I do not use formal agents, automated pipelines, RAG, or fine-tuned models. I need to answer honestly without overstating.

Requirements for the answer:
- Be transparent: I do not operate formal AI agents or automated pipelines.
- However, describe my structured multi-step conversational workflow as an emerging form of orchestration: I provide source documents as context, chain prompts to refine output, iterate across steps (research → draft → validate → format → deliver), and treat each session as a purposeful workflow rather than isolated queries.
- Describe the prompt discipline I apply: structured context-setting, constraint specification, output format direction, iterative refinement.
- Acknowledge project constraints (regulated environment) as the key reason agents have not been feasible.
- State concrete next steps: I am actively learning agentic patterns (GitHub Copilot agent mode, VS Code agent workflows) and plan to introduce structured prompt libraries and reusable templates as a first step toward Level 3.
- Avoid: claiming things I haven't done. The Adversarial Agent will catch overstatements.
- Target 200–300 words. Honest, forward-looking, constraint-aware.
```

**Artifacts to attach to this question:** E (Performance Testing Plan — best example of structured multi-step AI orchestration producing a complex professional deliverable), C (QA Strategy)

---

## QUESTION 5 — Scaling AI Impact

**Assessment Question:**
> Describe any actions you've taken to extend AI value beyond your own work. Examples: contributing reusable assets, leading/participating in internal AI initiatives, mentoring peers, demonstrating measurable AI ROI.

**Prompt to use:**

```
[PASTE SYSTEM CONTEXT ABOVE HERE]

Now draft my answer for QUESTION 5: Scaling AI Impact.

Context: I have not formally mentored peers or led AI initiatives. My AI use has been individual. However, the deliverables I produced have had team and client-level impact.

Requirements for the answer:
- Acknowledge honestly that formal AI mentoring or initiative leadership has not occurred yet.
- Reframe what HAS happened: by producing AI-generated deliverables that were adopted by the team and presented to the client, I have demonstrated AI ROI at the project level — the artifacts themselves carry the proof.
- Highlight the performance testing plan and QA strategy as examples of artifacts that changed how the project approaches those areas — they are now the working baseline documents.
- Mention availability and willingness to contribute to internal AI initiatives and knowledge sharing.
- If applicable, mention that the structured prompt approach and multi-step workflow I use could be templated and shared (position this as a near-term action).
- Be concrete about future intent: participating in AI squad activities, sharing prompt templates, contributing to internal knowledge bases.
- Target 200–250 words. Honest, grounded, forward-looking.
```

**Artifacts to attach to this question:** A (management report — demonstrates AI ROI communicated to stakeholders), E (performance testing plan — team-adopted artifact)

---

## EVIDENCE SUMMARY TABLE

Use this to quickly match artifacts to questions when attaching files in the platform:

| Artifact | File(s) | Q1 | Q2 | Q3 | Q4 | Q5 |
|---|---|:---:|:---:|:---:|:---:|:---:|
| A — Requirements vs Proposal | Proposal_vs_Requirements_Comparison.docx, Requirements_vs_Findings_Management_Review.docx | ✅ | ✅ | ✅ | | ✅ |
| B — SQL Test Data Scripts | CustomerActivityAndExceptionLogs sql scripts creation.md | ✅ | ✅ | ✅ | | |
| C — DOM QA Strategy | dom_performance_testing_strategy.html | ✅ | | ✅ | ✅ | |
| D — Unstructured Test Cases + ADO CSV | DOM_QA_Strategy_Unstructured_TestCases creation and json for ADO.md | ✅ | ✅ | ✅ | | |
| E — Performance Testing Plan | Anex_1_Performance_Testing_Plan_Peak_Month_Capacity_Simulation.html | ✅ | | ✅ | ✅ | ✅ |
| F — Meeting Minutes | Performance_Testing_Meeting_Minutes.md | ✅ | | ✅ | | |

---

## SELF-ASSESSMENT GUIDANCE

Based on the evidence, your realistic target level is:

| Dimension | April Baseline | July Target | Notes |
|---|---|---|---|
| Daily AI Workflow | Level 1–2 | **Level 2** | Consistent, structured, multi-artifact |
| Output Validation | Level 1 | **Level 2** | Review process documented |
| Productivity Impact | Level 1 (personal only) | **Level 2** | Project-level adoption confirmed |
| Agents / Automation | Level 0 | **Level 1–2** | Honest gap; structured workflow is the argument |
| Scaling AI Impact | Level 0 | **Level 1** | Deliverable adoption = indirect scaling |

**Overall honest range: Level 2 (strong case), with constraints noted.**

> The regulated environment and client AI restrictions are legitimate mitigating factors the rubric accounts for. Do not let these gaps pull your score down unfairly — document them clearly in the **Project Constraints** section of the form.

---

## PROJECT CONSTRAINTS CHECKLIST (fill in the form)

Check both of these in the assessment form:
- [x] **Client limitations on AI usage**
- [x] **Highly regulated environment**

Add a brief note (the form may allow a text field): *"Client operates under healthcare data regulations (HIPAA context). Direct AI use on client data or production systems is restricted to prevent PII exposure. AI tools are used exclusively on non-sensitive project artifacts: documentation, test strategies, synthetic data, and analysis documents."*

---

*Document created: 2026-07-06 | For use in GAP AI Impact Assessment July 2026 submission*

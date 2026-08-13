# GAP Leadership Presentation Script
## Agentic QA DMAIC Assistant: From QA Analysis to Team-Ready Automation

**Presenter:** Jose Rafael Mora Casal  
**Role:** QA Engineer, DOM Project (MediQuant)  
**Audience:** GAP Leadership (Engineering, Delivery, AI Enablement)  
**Estimated duration:** 18-22 minutes  
**Format:** Slide deck + optional narrated video

---

## 0) Presenter Setup Notes (Not for slides)

- Use only synthetic/non-sensitive examples.
- Do not include real client data, PHI, PII, production IDs, or credentials.
- Keep language outcome-focused: reliability, governance, adoption, measurable operational value.
- Position the tool as a reusable pattern for regulated environments, not only one project utility.

---

## 1) Slide: Title

### Slide content
**Agentic QA DMAIC Assistant**  
A reusable, compliance-safe workflow for root cause analysis, CAPA planning, and QA artifact generation

**Presenter:** Jose Rafael Mora Casal  
**Date:** August 2026

### Speaker notes
Today I will show how we transformed a manual QA root cause workflow into an agentic, traceable, and shareable system. The focus is practical leadership value: faster decision support, better governance, and easier team adoption in a regulated context.

---

## 2) Slide: Why This Matters to GAP

### Slide content
- QA and incident analysis are still often manual and inconsistent.
- Regulated clients require stronger auditability and evidence discipline.
- Teams need repeatable workflows, not isolated prompt sessions.

**Leadership opportunity:** convert individual AI usage into reusable delivery capability.

### Speaker notes
This initiative closes the gap between personal AI productivity and organizational AI capability. We are creating a workflow that can be reused, audited, and operationalized by multiple team members.

---

## 3) Slide: Problem Statement (Before)

### Slide content
**Before this tool:**
- RCA depth and quality varied by person.
- Stop criteria were subjective.
- CAPA and test artifacts required repetitive manual formatting.
- Execution transparency was limited.
- Onboarding non-CLI users was slower than needed.

### Speaker notes
The issue was not whether people could use AI. The issue was consistency, validation, and adoption at team scale. That is where leadership-level value appears.

---

## 4) Slide: Solution Overview (What We Built)

### Slide content
**Agentic QA DMAIC Assistant** includes:
- Guided Five Whys RCA workflow (CLI + local web UI)
- Evidence-gated decision checkpoints
- Automated exports:
  - RCA report (Markdown)
  - CAPA CSV
  - ADO test case CSV
- Orchestrated agent pipeline with trace visibility
- Shareable package with startup and validation scripts

### Speaker notes
The design goal was to preserve engineering rigor while reducing operational friction. This is not a chat transcript tool; it is a structured execution workflow.

---

## 5) Slide: Architecture at a Glance

### Slide content
**Workflow:** planner -> analyzer -> validator  
**Orchestration:** centralized in `src/orchestrator.py`  
**Specialized agents:** CAPA and Test Case modules  
**Traceability:** per-defect `agent_trace` in output and UI viewer

### Speaker notes
Leadership should note the modularity. This supports maintainability, targeted upgrades, and easier quality controls compared to a monolithic script.

---

## 6) Slide: Governance and Compliance by Design

### Slide content
- Synthetic/non-sensitive input model
- Evidence requirements before confirming root cause actions
- Explicit stop logic for early closure only when criteria are met
- Environment validation before launch (`check-env.ps1`)
- Reproducible packaging for controlled team distribution

### Speaker notes
The strongest point in regulated environments is intentional constraints. We do not try to automate sensitive data pathways. We automate non-sensitive QA workflows with governance built in.

---

## 7) Slide: User Experience and Adoption Improvements

### Slide content
- Local web UI for non-CLI users
- Option explanations for RCA flags
- Early-stop guidance visible in workflow
- Agent Trace Viewer for transparency
- One-command startup (`start-local.ps1`)

### Speaker notes
Adoption depends on usability. We reduced friction by exposing decision logic and making startup deterministic for teammates with different technical depth.

---

## 8) Slide: Packaging for Team Scale

### Slide content
**Shareable package includes:**
- Runtime code + templates
- Environment checker (`check-env.ps1`)
- One-command launch (`start-local.ps1`)
- One-command packaging (`package-shareable.ps1`)

**Current distribution artifact:**
- `October 2026/dist/agentic-qa-dmaic-shareable-20260811-170319.zip`

### Speaker notes
This is the bridge from prototype to operational asset. A clean package and deterministic setup are key enablers for multiplier impact.

---

## 9) Slide: Demonstration Flow (Live or Recorded)

### Slide content
1. Run environment check or one-command startup  
2. Start RCA session from synthetic defect input  
3. Submit Why answers with evidence references  
4. Show checkpoint behavior and stop logic  
5. Export RCA/CAPA/TestCase artifacts  
6. Open Agent Trace Viewer and inspect trace

### Speaker notes
Keep the demo short and controlled. Use one representative synthetic defect and emphasize process reliability over feature count.

---

## 10) Slide: Business Value for Leadership

### Slide content
**Delivery value**
- More consistent RCA quality
- Faster artifact generation for execution teams
- Reduced setup and onboarding friction

**Risk/Governance value**
- Better evidence discipline
- Explicit decision checkpoints
- Improved auditability and trace visibility

### Speaker notes
This aligns with leadership goals: better quality signals, stronger governance posture, and scalable team enablement.

---

## 11) Slide: AI Impact Mapping (D1-D5)

### Slide content
- **D1:** AI-first daily workflow operationalized in CLI and UI
- **D2:** Validation checkpoints and evidence gating embedded
- **D3:** Productivity improved through repeatable startup/export flows
- **D4:** Agentic orchestration and modular workflow implementation
- **D5:** Shareable package and onboarding path for wider adoption

### Speaker notes
This is the evidence-backed narrative for AI maturity progression: from individual usage to reusable, governed, team-ready workflow.

---

## 12) Slide: Current Status and Next Steps

### Slide content
**Current status**
- Productized workflow complete
- Shareable distribution package ready
- Leadership demo-ready

**Next 30-60 days**
- Run adoption pilots with 2+ teammates
- Capture prospective operational metrics
- Collect manager/lead verification of delivery impact
- Package feedback into next revision

### Speaker notes
The immediate objective is not adding complexity. It is proving repeatable adoption and measurable impact at team level.

---

## 13) Slide: Leadership Ask

### Slide content
Request support for:
- Pilot adoption with selected QA/engineering users
- Lightweight metric instrumentation for adoption and cycle-time tracking
- A short internal showcase slot for cross-team visibility

### Speaker notes
With leadership sponsorship, this can move from one-team asset to a reusable GAP pattern for regulated QA contexts.

---

## 14) Slide: Closing

### Slide content
**Key message:** We converted AI usage from ad-hoc assistance into a structured, governed, and shareable QA capability.

Questions and feedback

### Speaker notes
Close with openness to feedback on rollout strategy, not only technical details.

---

# Appendix A: 90-Second Executive Version (Optional)

Use this script when you only have 1-2 minutes:

We built an Agentic QA DMAIC Assistant to standardize root cause analysis and accelerate QA action planning in a regulated environment. It combines guided Five Whys, evidence-gated decisions, and automated outputs for RCA reports, CAPA CSVs, and ADO test cases. We moved from manual, person-dependent execution to an orchestrated workflow with trace visibility and a shareable package for team onboarding. The result is stronger governance, faster repeatable execution, and a practical path from individual AI productivity to scalable team impact.

---

# Appendix B: Video Narration Script (5-7 minutes)

## Scene 1 - Context
In regulated QA delivery, consistency and auditability are as important as speed. Manual root cause workflows often produce variable quality and weak traceability.

## Scene 2 - The Tool
The Agentic QA DMAIC Assistant provides a structured Five Whys workflow with evidence checkpoints, automated exports, and transparent execution traces.

## Scene 3 - How It Works
Users can run it through CLI or local web UI. The workflow guides RCA responses, validates stop conditions, and generates execution artifacts. Behind the scenes, orchestrated agents manage planning, analysis, and validation.

## Scene 4 - Governance
The tool is designed for compliance-safe usage. It operates on synthetic and non-sensitive artifacts, requires evidence discipline, and supports reproducible setup through environment checks.

## Scene 5 - Team Adoption
A clean shareable package, one-command startup, and clear usage guidance reduce onboarding friction and make adoption easier for non-CLI users.

## Scene 6 - Leadership Value
This shifts AI usage from personal assistance to a reusable operational capability: better quality signals, stronger governance, and scalable team impact.

## Scene 7 - Next Step
The next phase is pilot adoption, prospective metric capture, and broader rollout as a reusable GAP pattern.

---

# Appendix C: Prompts for Slide/Video AI Tools

Use these prompt seeds in external slide/video generators. Keep synthetic data only.

## Slide Generator Prompt
Create a professional leadership presentation titled "Agentic QA DMAIC Assistant" for a regulated healthcare-adjacent QA context. Emphasize business impact, governance, traceability, and team adoption. Include sections: problem, solution, architecture, compliance-by-design, demo flow, D1-D5 AI impact mapping, next steps, leadership ask. Style should be clean, executive, and data-driven. No real client or patient data.

## Video Generator Prompt
Create a 6-minute business-technical explainer video for leadership about a QA automation workflow called "Agentic QA DMAIC Assistant." Tone: confident, practical, governance-focused. Visuals: workflow diagrams, UI snapshots placeholders, artifact examples, adoption roadmap. Include voiceover sections for context, solution, governance, adoption, and next steps. Do not include any real client data or identifiable information.

---

# Appendix D: Suggested Supporting Artifacts to Attach

- `October 2026/agentic-qa-dmaic/src/orchestrator.py`
- `October 2026/agentic-qa-dmaic/src/web_app.py`
- `October 2026/agentic-qa-dmaic/web/index.html`
- `October 2026/agentic-qa-dmaic-shareable/README.md`
- `October 2026/agentic-qa-dmaic-shareable/PACKAGE_CONTENTS.md`
- `October 2026/dist/agentic-qa-dmaic-shareable-20260811-170319.zip`

# Engineering Track — AI Impact Evaluation Reference

## The 4-Level Scale

| Level | Label | Tag | What it means |
|-------|-------|-----|---------------|
| **0** | Non-Integrator | "Doesn't meaningfully use AI" | Rare or basic AI use. Mainly uses AI as a Google search substitute. Copy-pastes outputs without judgment. Work style unchanged from pre-AI era. |
| **1** | Operative User | "Uses AI for personal speed" | Regular use for explanations, snippets, research, documentation. AI improves personal task speed but impact stays individual — not visible at project level. |
| **2** | Project Accelerator | "AI delivers project-level impact" | Structured, consistent AI use that improves project outcomes. AI-first mindset for engineering tasks. Engineer still drives step-by-step, with AI as active assistant. Measurable improvements in delivery speed, quality, or scope. |
| **3** | Autonomous Engineer (The Transformer) | "AI-driven systems transform delivery" | Designs and builds AI agents or automated workflows. Uses agentic AI daily. Automates meaningful portions of the delivery process. Introduces reusable AI systems adopted by teams. Systemic impact across team or organization. |

**The key Level 2 → Level 3 distinction:** At Level 2, AI *assists* tasks you still drive manually. At Level 3, AI *executes* parts of the workflow with limited supervision while you design and orchestrate the systems.

---

## The 5 Evaluation Dimensions

### Dimension 1 — AI Integration in Daily Workflow
**Objective:** Transition from "Manual-First" to "AI-First."

| Level | What It Looks Like |
|-------|--------------------|
| 0 | AI absent or used so rarely it has no impact. Work style unchanged. |
| 1 | AI used occasionally for ad hoc tasks. Reactive, not habitual. |
| 2 | AI is part of the daily routine — task planning, code scaffolding, documentation, code review prep. AI-first mindset when approaching engineering tasks. |
| 3 | AI is the default starting point for all engineering work. Has standing agents or automations integrated into personal workflow. Uses AI to handle boilerplate so focus goes to high-level architecture and team innovation. |

**Level 3 Examples:**
- Uses GitHub Copilot, Claude Code, or Cursor with custom system prompts tuned to the project
- Maintains a personal prompt library for recurring engineering patterns
- Has automated repetitive daily tasks (standup prep, PR descriptions, ticket creation)

---

### Dimension 2 — Appropriate Use and Validation of AI Outputs
**Objective:** Maintain "Human-in-the-Loop" architecture for safety and standards.

| Level | What It Looks Like |
|-------|--------------------|
| 0 | Accepts AI output as-is or doesn't use AI. No awareness of hallucination risk. |
| 1 | Reviews AI output informally (reads before committing). Knows AI can be wrong but no structured process. |
| 2 | Active verification: checks AI code against architecture patterns, runs edge case tests, reviews for security issues and tech debt. Can explain specific errors caught. |
| 3 | Systematic validation process. Has established team-level guidelines for AI output review. Audits for hallucinations, architectural compliance, security vulnerabilities. Documents and shares validation workflows. May have built automated testing or linting for AI-generated code. |

**Level 3 Examples:**
- Built a pre-commit hook or CI check that scans AI-generated code for security anti-patterns
- Created a team checklist or runbook for validating AI-authored code
- Can cite specific hallucinations caught and how they were resolved

---

### Dimension 3 — Productivity and Measurable Impact
**Objective:** Translate AI usage into tangible economic value (ROI).

| Level | What It Looks Like |
|-------|--------------------|
| 0 | No data. Cannot show AI changed any outcome. |
| 1 | Feels faster but can't prove it. No metrics. Personal anecdotes only. |
| 2 | Has concrete metrics: story points per sprint increased, PR cycle time reduced, bug rate down. Can show before/after comparison for at least one dimension. Has flagged at least one manual bottleneck for optimization. |
| 3 | Multiple metrics across time periods showing compounding improvement. AI has demonstrably freed up engineering capacity for higher-leverage work. Impact visible to the client or delivery manager. Has quantified ROI in hours saved or value delivered. |

**Strong Evidence Examples:**
- Jira velocity chart showing story point increase after adopting AI workflows
- PR cycle time reduction (e.g., "average PR review time dropped from 3 days to 1.5 days")
- Bug rate reduction ("hotfixes in production dropped 40% after adding AI-assisted code review")
- Time savings with methodology: "Tracked for 4 weeks; saved ~6 hours/week on boilerplate writing"

**Weak Evidence (avoid):**
- "I feel faster" — no data
- Generic AI conversation screenshots without outcomes
- Estimates made after the fact without tracking methodology

---

### Dimension 4 — Capacity to Operate at Agentic Level
**Objective:** Evolve from "Tool User" to "System Orchestrator."

| Level | What It Looks Like |
|-------|--------------------|
| 0 | Uses no AI tools or only for basic lookup. No agent or automation work. |
| 1 | Uses AI tools (Copilot, ChatGPT, Claude) for code generation and Q&A. No custom configurations or agents. |
| 2 | Uses more advanced features: custom system prompts, RAG-style context injection, multi-step prompting, API integrations. May have built simple automations or scripts using AI APIs. |
| 3 | Designs and deploys multi-step AI agents. Builds automated CI/CD integrations with AI. Creates custom tools with RAG or fine-tuned models. Maintains agents and monitors for drift/degradation. Has implemented fallback mechanisms. Uses AI frameworks (LangChain, AutoGen, CrewAI, Claude Code SDK, etc.). |

**Level 3 Examples:**
- Built a code review agent that automatically flags security issues in PRs
- Created an AI-powered test generation pipeline integrated into CI/CD
- Developed a RAG system over internal codebase documentation for the team
- Built a multi-agent orchestration pipeline for a client deliverable
- Created and maintains custom Claude/GPT prompts with project-specific context

**Evidence That Scores Well:**
- Agent architecture diagrams
- GitHub PRs showing the agent or automation code
- Production usage metrics (e.g., "the test agent runs on 100% of PRs, catching X issues/month")
- Technical design documents describing the system

---

### Dimension 5 — Use of AI as a Multiplier
**Objective:** Act as a "Multiplier" for the organization and clients.

| Level | What It Looks Like |
|-------|--------------------|
| 0 | AI work stays within personal tasks. Nothing shared. |
| 1 | Shares occasional tips or prompts informally with teammates. No structured contribution. |
| 2 | Has contributed reusable assets: prompt libraries, scripts, or workflow guides that teammates actually use. Participates in at least one internal AI initiative. |
| 3 | Leads or co-leads AI initiatives with demonstrable team or client impact. Mentors teammates who are struggling with AI adoption. Has built internal tools or frameworks adopted by multiple projects. Contributes reusable assets to organizational shared libraries. Delivers AI-driven capabilities that create new value for clients. |

**Level 3 Examples:**
- Built and maintains a shared prompt library used by 5+ engineers on the project
- Led an AI onboarding session that helped 3+ colleagues reach Level 2
- Delivered an AI-native feature or product capability the client now sells or promotes
- Created an internal tool (e.g., AI code review bot, documentation generator) used across multiple GAP projects

---

## What Constitutes Level 3 (Summary Checklist)

To reach Level 3, an engineer typically needs **all** of the following:
- [ ] AI is the default starting point for daily tasks (not optional/reactive)
- [ ] Has built at least one AI agent, automated pipeline, or custom AI tool
- [ ] Can cite specific metrics (not estimates) showing project-level impact
- [ ] Has validation process beyond "reading before committing"
- [ ] Has contributed something reusable that others use (prompts, tools, frameworks)
- [ ] Has some cross-team or client-facing impact from AI work

---

## Level 2 → Level 3 Engineering Playbook

If you're already at Level 2, you likely have the workflows and tools — the gap is almost always **documentation, measurement, and socialization**, not starting from scratch. Work through these:

### Step 1: Productionize an Existing Workflow (Dimension 4)
Move one personal or external agentic workflow into your actual project repository. Commit it, wire it into the project's tooling, and demonstrate it running reliably over at least 2 sprints. *External tools in isolation* don't count; what matters is systemic, in-project reliability.

### Step 2: Build a Formal Validation Log (Dimension 2)
Start (or backfill) a structured log of AI-generated outputs you reviewed, corrections made, and hallucinations caught. Format it as a markdown or spreadsheet file with date, tool, issue type, and correction. Even 10 retrospective entries with git commit cross-references proves a systematic practice.

### Step 3: Track Productivity with a Methodology (Dimension 3)
Don't just claim you're faster — measure it. Use Jira velocity (story points per sprint), PR cycle time, or time-on-task before/after AI adoption. Track for 2–4 sprints minimum. The methodology matters as much as the numbers (the adversarial agent will ask: "How did you control for other variables?").

### Step 4: Publish a Team-Adopted Asset (Dimension 5)
Create one reusable artifact — a prompt library, a how-to guide, an agent template, or an automation script — and publish it to a team-accessible repository (internal wiki, shared GitHub repo, Confluence). Then *actively* get at least 2 colleagues to use it and document their adoption. "I shared it" is not enough; you need adoption proof.

### Step 5: Articulate Organizational Impact
Write one clear story connecting your AI work to a client outcome or a delivery improvement visible to stakeholders beyond your immediate team. It doesn't need to be huge — a 15% reduction in bug escape rate on a specific feature is compelling if it's verifiable.

---

## Frequently Missed Level 3 Requirements

1. **Building vs. Using**: Most people stop at using AI tools. Level 3 requires *building* AI-powered systems.
2. **Personal vs. Systemic**: Level 2 improves your own output. Level 3 improves how the *team* or *project* delivers.
3. **Anecdotes vs. Metrics**: "I'm faster" is Level 1. "Sprint velocity increased 35% and I have the data" is Level 2+.
4. **One-time vs. Ongoing**: A demo or experiment doesn't qualify. Level 3 requires sustained, daily use in production workflows.
5. **Solo vs. Shared**: Work that only you benefit from cannot reach Level 3 Multiplier.

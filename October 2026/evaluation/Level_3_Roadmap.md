# Level 3 Roadmap — Autonomous QA Engineer
**Engineer:** Jose Rafael Mora Casal  
**Role:** QA Engineer — DOM project (MediQuant client)  
**Track:** Engineering  
**Current Level:** 2 (targeted July 2026) → **Target: Level 3 (October 2026 window)**  
**Created:** July 20, 2026

---

> **⚠️ Disclaimer:** This roadmap is based on the official GAP AI Impact Framework documentation. It does not represent the official evaluation system or guarantee any outcome. The evaluation involves 20+ internal scoring dimensions not publicly documented. Final classifications are determined by the official review process, including manager calibration. Use this to strengthen your submission — the official rubric and your manager are the final authorities.

---

## The Level 2 → Level 3 Shift

| Dimension | Level 2 (current) | Level 3 (target) |
|-----------|-------------------|------------------|
| D1 — Daily Workflow | AI part of daily routine for major tasks | AI is the default starting point for ALL tasks; standing automations integrated |
| D2 — Validation | Active verification, documented log | Systematic process + team-level guidelines/automated checks |
| D3 — Productivity | Concrete metrics for at least one dimension | Multiple metrics over time showing compounding impact; visible to client/DM |
| D4 — Agentic | Advanced prompting, multi-step chaining | **Built and maintains an agent/pipeline/custom tool** |
| D5 — Multiplier | Reusable asset created + shared | Asset ADOPTED by others; leads/co-leads initiative; mentors peers |

**The two decisive gaps for you:** D4 (build something that runs) and D5 (prove adoption). Everything else is largely in place.

---

## Constraint Frame — "Agentic QA under HIPAA"

The client's HIPAA restrictions prevent AI agents from touching **client data or production systems**. They do **not** prevent automation around **non-sensitive QA artifacts**:
- Requirements documents (text)
- Synthetic test data
- Test case definitions
- QA strategy docs
- Meeting transcripts

**Level 3 strategy:** Build automation that operates exclusively on these non-sensitive artifacts. This is fully compliant AND fully qualifies as agentic work.

---

## Milestone 1 — Build the Agentic Artifact (Dimension 4) 🎯 CRITICAL

**This is the single most important milestone. Level 3 is nearly impossible without it.**

### Primary Project: Test Case Generation Agent
Convert `prompts/test-case-generation.md` from a fill-in template into a runnable script.

| Attribute | Detail |
|-----------|--------|
| **Input** | A requirements doc / user story (text file) |
| **Process** | Script calls AI API → generates structured test cases → self-validates coverage → formats as ADO CSV |
| **Output** | Ready-to-import ADO CSV |
| **Why Level 3** | Multi-step pipeline that executes with orchestration, not per-prompt hand-holding |
| **HIPAA-safe** | Operates on requirements text + synthetic data only |
| **Evidence produced** | Committed script + README + run logs across multiple sprints |

**Level 3 criteria this satisfies:**
- [ ] "Designs and deploys multi-step AI workflow"
- [ ] "Automates a meaningful portion of the delivery process"
- [ ] "Monitors reliability over time" (via run logs)

### Acceptance Criteria for Milestone 1
- [ ] Script committed to a repository
- [ ] Runs on **at least 3 real feature specs** across **2+ sprints**
- [ ] README documents usage + example run
- [ ] Run log shows reliable repeated execution (the "reliability over time" signal)
- [ ] At least one prompt-tuning iteration documented (satisfies "have you performed prompt tuning?")

### Fallback / Alternative Projects (pick one if Test Case Agent doesn't fit)
- **B — AI Test Data Generator:** schema in → deterministic SQL + self-check report out
- **C — CI/CD Quality Gate:** pipeline step that auto-generates PR descriptions or coverage summaries (highest signal, highest effort)

---

## Milestone 2 — Prove Team Adoption (Dimension 5)

Creating the prompt library was Level 1–2. **Adoption by others is Level 3.**

### Actions
- [ ] Share prompt library + test case agent with the DOM team (use `Prompt_Library_Outreach_Drafts.md`)
- [ ] Get **at least 2 colleagues** to use a template or the agent on real work
- [ ] Log each adoption in `Prompt_Library_Sharing_Record.md` with evidence (their artifact / Teams reply)
- [ ] Run **one AI squad or knowledge-share session** demoing the test case agent
- [ ] Capture attendance (meeting invite + attendee list screenshot)

### Acceptance Criteria for Milestone 2
- [ ] 2+ documented adoption entries with verifiable evidence
- [ ] 1 knowledge-share session delivered with recorded audience
- [ ] Adoption produces at least one artifact made by a *colleague* using your tool

---

## Milestone 3 — Prospective Metrics (Dimension 3)

Your current metrics are retrospective estimates. Level 3 wants **tracked, compounding, verifiable** data.

### Actions
- [ ] Track test-case-creation cycle time: manual baseline vs. agent-generated, over 2–4 sprints
- [ ] Track a second metric (e.g., test coverage added per sprint, or defects caught earlier)
- [ ] Get a written confirmation from Cesar Trompetero on delivery impact (Teams message is enough)
- [ ] Present the metric trend to the delivery manager (makes impact "visible to client/DM")

### Acceptance Criteria for Milestone 3
- [ ] 2+ sprints of prospective before/after data (not estimated after the fact)
- [ ] At least one metric shows a trend over time, not a single snapshot
- [ ] Third-party (manager/lead) confirmation on record

---

## Milestone 4 — Daily Workflow & Validation Polish (D1 + D2)

Low-effort reinforcement of dimensions already near Level 3.

### Actions
- [ ] Add `.github/copilot-instructions.md` to the DOM repo with QA/project-specific context
- [ ] Keep `AI_Output_Validation_Log.md` current — add any issues the agent catches
- [ ] Draft a short team-level "AI output validation checklist" (turns personal practice into team guideline → D2 Level 3 signal)

### Acceptance Criteria for Milestone 4
- [ ] Project-level AI config committed (`copilot-instructions.md`)
- [ ] Validation log has entries dated within the current cycle
- [ ] A shareable validation checklist exists and is shared with the team

---

## Timeline (July 20 → October 2026)

| Weeks | Focus | Milestone |
|-------|-------|-----------|
| Jul 20 – Aug 3 | Build test case agent (v1), commit, first run | M1 core |
| Aug 4 – Aug 17 | Add `copilot-instructions.md`; share library + agent with team; start metric tracking | M2 start, M3 start, M4 |
| Aug 18 – Sep 7 | Run agent on real specs across 2 sprints; log adoptions; prompt-tune | M1 completion, M2 |
| Sep 8 – Sep 28 | Knowledge-share session; collect metrics trend; manager confirmation | M2, M3 |
| Sep 29 – Oct | Assemble evidence; write assessment responses; attach artifacts to each question | Submission |

---

## Evidence Map — What to Attach per Question (October Submission)

Each question is scored independently. Attach evidence to EVERY relevant question.

| Question (Dimension) | Primary Evidence | Supporting |
|----------------------|------------------|------------|
| Q1 — Daily Workflow | `copilot-instructions.md`, prompt library | Agent script |
| Q2 — Validation | `AI_Output_Validation_Log.md`, team validation checklist | Agent self-check logic |
| Q3 — Productivity | Prospective metric trend, manager confirmation | `AI_Productivity_Metrics.md` |
| Q4 — Agentic | **Test case agent (code + run logs + README)** | Prompt-tuning notes |
| Q5 — Multiplier | `Prompt_Library_Sharing_Record.md` (2+ adoptions), squad session evidence | Colleague-produced artifacts |

---

## Level 3 Readiness Checklist (self-audit before submitting)

- [ ] Built and committed at least one AI agent/automation that runs with limited supervision
- [ ] It ran reliably across 2+ sprints with a run log
- [ ] Performed and documented at least one prompt-tuning iteration
- [ ] At least 2 colleagues adopted a reusable asset I created (with evidence)
- [ ] Delivered at least one knowledge-share/mentoring session
- [ ] Have prospective (not retrospective) metrics showing a trend
- [ ] Have third-party confirmation of impact from a lead or manager
- [ ] AI is my default starting point, backed by project-level config
- [ ] Validation practice is documented AND shared as a team guideline

**If all boxes are checked, you have a defensible Level 3 submission.**

---

## Common Level 3 Traps (from the framework)

1. **Building vs. Using** — Using AI tools is Level 2. You must *build* something. → Milestone 1 is non-negotiable.
2. **Personal vs. Systemic** — Improving your own output isn't enough; the team must benefit. → Milestone 2.
3. **Anecdotes vs. Metrics** — "I'm faster" fails; "cycle time dropped X% with tracked data" passes. → Milestone 3.
4. **One-time vs. Ongoing** — A demo doesn't count; sustained daily/sprint use does. → run logs across sprints.
5. **Solo vs. Shared** — Work only you benefit from can't reach Level 3. → adoption proof.

---

## Next Action

**Recommended:** Build the Test Case Generation Agent (Milestone 1) — it's the highest-leverage artifact and the hardest gap to close. Ask the coach to scaffold it in this workspace.

Secondary quick win: add `.github/copilot-instructions.md` to the DOM repo.

# Evidence Guide — AI Impact Assessment

## How the Evaluation System Works

The assessment is evaluated by a **Multi-Agent AI System** composed of:

1. **Evaluator Agent** — Scores your response against the rubric for each dimension
2. **Adversarial Agent** — Challenges unsupported claims and looks for weaknesses in the evidence
3. **Referee Agent** — Resolves disagreements and determines the final score for that dimension
4. **Final Level Agent** — Assigns a Level based on the outputs of the previous agents

**Critical implication:** The evaluation system does not assume context between questions. For every question, you must:
- Answer the question directly
- Attach evidence supporting that specific answer
- Ensure the evidence clearly demonstrates the capability being evaluated

**If evidence is not attached to a question, it will be treated as missing** — even if the same artifact appears elsewhere in your assessment.

---

## What Makes Strong Evidence

Strong evidence is:
- **Verifiable** — Can be independently confirmed, not just claimed
- **Directly related to the question** — Addresses what was specifically asked
- **Demonstrates measurable impact** — Has numbers, comparisons, or concrete outcomes
- **Clearly attributable to your work** — Not a team effort described in a way that obscures your individual contribution
- **Recent and representative** — From the past 6 months; reflects your current capabilities

**Strong evidence examples:**
- Pull Requests (with description of AI contribution and impact)
- Technical design documents describing AI systems you built
- Workflow automations with documented run counts or time saved
- Agent architectures (diagrams, code, documentation)
- Before-and-after productivity metrics with tracking methodology
- Analysis reports or dashboards built with AI assistance
- Internal tools with usage statistics
- Process improvements with measurable outcomes (cite the numbers)

---

## What Makes Weak Evidence

Weak evidence:
- Relies on self-reporting without proof
- Lacks measurable outcomes
- Cannot be independently verified
- Provides activity without impact

**Weak evidence examples (avoid these):**
- Slack messages or chat screenshots without context showing outcome
- Generic AI prompts without showing what they produced or the impact
- Meeting attendance without demonstrating what changed
- Statements like "I use AI every day" without showing what you built or improved
- Screenshots of AI conversations without evidence of what happened next
- Descriptions of work without supporting artifacts

---

## Reusing Evidence Across Questions

The same artifact may support multiple assessment dimensions. However, because questions are evaluated independently:

✅ **Attach the artifact to every question where it is relevant**

❌ **Do not reference another answer and assume the evaluator will retrieve it**

*Example: If a GitHub PR shows both your agentic workflow (Dimension 4) and its productivity impact (Dimension 3), attach that PR to both Question 3 and Question 4 separately.*

---

## Track-Specific Evidence Guidance

### Engineering Track — What Scores Well

Strongest evidence:
- Multi-step AI agent implementations in production
- Agent orchestration pipelines
- PRs demonstrating measurable improvements (with metrics)
- Internal AI tooling used by multiple engineers or projects
- Technical design documents for AI systems
- Cost, quality, productivity, or delivery improvements supported by data

Evidence with limited value:
- AI conversations without outcomes
- Experimental work that never reached practical application
- Descriptions of work without supporting artifacts
- General statements about AI usage ("I use Copilot every day")

---

### Shared Services Track — What Scores Well

**Individual Contributors — Strong evidence:**
- AI-assisted analysis with before/after comparisons
- Workflow automations with time-savings data
- Process improvements with measurable outcomes
- Time savings supported by tracking data (not estimates)
- Improved quality, throughput, or operational efficiency (with numbers)

**Managers — Strong evidence:**
- Team adoption initiatives with data showing team maturity progression
- AI enablement programs you created or led
- Coaching outcomes: "Moved 3 direct reports from Level 1 to Level 2"
- Team-level productivity improvements with metrics
- Evidence of sustained AI adoption across the organization

Managers are evaluated not only on personal AI usage but on their ability to increase AI capability within their teams.

---

## Feedback-to-Dimension Mapping

When evaluator feedback uses vague language, use these mappings to identify which dimension needs improvement:

| Evaluator Says... | Most Likely Dimension Gap | What It Actually Means |
|---|---|---|
| "needs rigorous tracking", "no measurement", "unsubstantiated productivity claim" | **Dimension 3 – Productivity** | You described activity without showing before/after metrics or a tracking methodology |
| "integrate into shared ecosystem", "collective assets", "personal tools vs. team assets" | **Dimension 5 – Multiplier / Organizational Impact** | Your impact stayed at personal scope; needs to reach the team or organization |
| "formal log", "validation process", "documentation of corrections", "LLM-as-a-judge", "hallucination handling" | **Dimension 2 – Validation & Quality** | Your review process isn't documented or systematic; evaluator can't verify your quality gates |
| "internalize workflows", "in-project use", "systemic adoption", "consistent integration" | **Dimension 4 – Agentic Capacity** | Work may exist externally or experimentally; needs to be shown as reliable and embedded in actual project work |
| "prompt library contribution", "reusable asset", "knowledge transfer" | **Dimension 5 – Multiplier** | Work is self-contained; needs to be packaged and adopted by others |
| "unsupported claims", "self-reported only", "cannot verify" | **Any dimension** | Evidence is missing or not attached; adversarial agent could not confirm the claim |
| "velocity tracking", "Jira metrics", "sprint data" | **Dimension 3 – Productivity** | Need sprint-level tracking data comparing AI-assisted vs. baseline performance |
| "Copilot only", "surface-level usage", "beyond chat/completion" | **Dimension 4 – Agentic Capacity** | Tool usage is at Level 1–2; needs structured agents or multi-step automations |
| "not demonstrated at scale", "one-time example" | **Dimension 3 or 4** | Evidence is singular; Level 3 requires sustained, recurring pattern |

---

## Re-evaluation Submission Rules

**Critical: Re-evaluations are not incremental.** The multi-agent system scores each question independently as if it were the first time. This means:

1. **All artifacts must be re-attached** — The system does not carry over prior submissions. If a PR or document supported your prior answer, attach it again to every applicable question.
2. **Every question needs a complete, standalone answer** — Do not reference other answers with phrases like "as mentioned above" or "see Question 2." Each question must stand alone.
3. **New evidence must clearly be dated within the evaluation period** — If you add new work, make sure timestamps are visible and the work happened after the prior evaluation.
4. **The adversarial agent will still challenge you** — Even if a prior evaluation gave partial credit, the next evaluation will re-scrutinize every claim. Strengthen all weak areas, not just the ones called out explicitly.

---



When preparing your responses, adopt the mindset of the Adversarial Agent — it will ask:

- **"Can you prove that?"** → If you can't point to an artifact, metric, or third-party confirmation, the claim is weak
- **"Could this result have happened without AI?"** → You need to demonstrate causal connection, not correlation
- **"Is this systemic or a one-time thing?"** → Level 3 requires sustained, recurring impact
- **"Who else benefited from this?"** → Individual impact alone cannot reach Level 3 Multiplier
- **"How do you know it was you and not the team?"** → Be specific about your contribution vs. the team's

---

## Measuring and Documenting Impact

Before your next evaluation cycle, start tracking:

| What to Track | How to Track It | Why It Matters |
|---------------|-----------------|----------------|
| Time on specific recurring tasks | Weekly time log (even a simple spreadsheet) | Before/after comparison for Productivity dimension |
| Story points or tickets completed per sprint | Jira/project tool history | Velocity evidence for Engineering |
| Number of times a tool/prompt you created was used | Usage logs, team feedback | Multiplier dimension evidence |
| Error or bug rates | QA metrics, post-deploy incident counts | Quality improvement evidence |
| Number of team members you coached | 1:1 notes, their Level progression | Multiplier dimension for Managers |
| AI-generated deliverables in production | Git commits, deployment logs | Agentic capacity evidence |

**Pro tip:** Start a "brag doc" today. Each week, write 2-3 bullet points about what AI helped you accomplish and what the outcome was. This makes evidence collection easy at evaluation time.

---

## Evaluation Timeline and Re-Evaluation Windows

- **Monthly Progress Updates:** June–September 2026
- **Re-evaluation cycles:** July and October 2026
- **Merit increases:** Retroactive to April 1st for those who qualify in May; applied at July or October for those who qualify later

If you didn't reach Level 3 in the initial evaluation, you have multiple opportunities to level up with new evidence from the re-evaluation windows.

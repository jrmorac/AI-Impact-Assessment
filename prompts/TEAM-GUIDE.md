# DOM Project — AI Prompt Library: Team Quick Start Guide
**Shared by:** Jose Rafael Mora Casal  
**Project:** DOM (MediQuant client)  
**Last Updated:** July 2026

---

## What Is This?

This is a library of reusable AI prompt templates for the most common QA tasks on the DOM project.

Instead of starting from scratch every time you use GitHub Copilot, Claude, or ChatGPT for a project task, these templates give you a pre-built starting point with:
- The right project constraints already embedded (no PII, HIPAA context, correct output format)
- Parameterized placeholders you fill in per task
- Follow-up prompts for the most common issues
- A validation checklist before you commit or share the output

**Time saved on first use:** Most engineers report these templates cut the "setup and iteration" phase of an AI task in half — you skip the 3–5 prompt cycles needed to get the AI to understand the project context.

---

## What's In the Library

| Template | What It Does | Typical Time Saved |
|----------|--------------|-------------------|
| [SQL Test Data Generation](sql-test-data-generation.md) | Generates deterministic INSERT scripts for synthetic test tables | 1–2 days → ~1 hour |
| [Test Case Generation](test-case-generation.md) | Structured test cases for data pipelines, ADO-ready | 1 day → ~1.5 hours |
| [ADO CSV Import](ado-csv-import.md) | Reformats test cases as ADO-compatible CSV for bulk import | 30 min → ~10 min |
| [Requirements Comparison](requirements-comparison.md) | Gap analysis: requirements doc vs. proposal/contract | 3–4 days → ~4 hours |
| [Meeting Minutes](meeting-minutes.md) | Formal minutes from transcript or notes, with attribution | 2–3 hours → ~15 min |
| [Performance Testing Plan](performance-testing-plan.md) | Full performance testing plan for data pipelines | 3–5 days → ~1 day |

---

## How to Use a Template (3 steps)

1. **Open the template** for your task (links above)
2. **Copy the SYSTEM CONTEXT block** and paste it into your AI chat first
3. **Fill in the `[PLACEHOLDERS]`** in the PROMPT TEMPLATE block, then paste it into the chat

Each template also includes:
- **Follow-up prompts** — for the most common issues (wrong format, missing coverage, etc.)
- **Validation checklist** — what to verify before accepting the AI output
- **Example usage note** — what happened when this was used on a real DOM task

---

## Project Constraints (already embedded in every template)

All templates include these guardrails so you don't have to remember them:
- **No PII or client production data** — all placeholders use synthetic values
- **HIPAA context** — outputs flag compliance-sensitive areas automatically
- **Human-in-the-loop required** — every template includes a validation checklist
- **Source traceability** — analysis prompts require findings to be traced to source documents

---

## Adding Your Own Templates

If you develop a prompt for a task not covered here, add it to the `prompts/` folder using the same structure:
1. System Context block
2. Prompt Template with [PLACEHOLDERS]
3. Follow-up prompts for common issues
4. Validation checklist
5. Example Usage Note

The goal is that anyone on the team can pick up a template cold and get a useful first draft within 10 minutes.

---

## Questions?

Contact Jose Rafael Mora Casal (Teams / Slack) — happy to walk through any template or help adapt one for a new task.

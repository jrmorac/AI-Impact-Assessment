# QA Prompt Library — DOM Project
**Maintainer:** Jose Rafael Mora Casal  
**Project:** DOM (MediQuant client)  
**Last Updated:** July 2026

---

## Purpose

This library contains reusable, parameterized prompt templates for recurring QA engineering tasks on the DOM project. Each template is designed for GitHub Copilot Chat, Claude, or similar AI assistants.

**Why a prompt library?**
- Eliminates re-writing the same context setup from scratch on every task
- Enforces consistent constraints (no PII, HIPAA context, output format)
- Makes the AI workflow repeatable and transferable to teammates
- Produces higher-quality first-draft outputs by embedding domain knowledge upfront

---

## How to Use a Template

1. Open the template for the task you need.
2. Copy the **SYSTEM CONTEXT** block and paste it into the AI chat first.
3. Fill in all `[PLACEHOLDER]` values with your specific task details.
4. Copy the **PROMPT** block and paste it after the system context.
5. Iterate with follow-up prompts as needed.
6. **Always validate the output** before committing or sharing — see the [AI Output Validation Log](../July%202026/AI_Output_Validation_Log.md) for the governance process.

---

## Templates

| # | File | Task | When to Use |
|---|------|------|-------------|
| 01 | [sql-test-data-generation.md](sql-test-data-generation.md) | SQL INSERT scripts for synthetic test data | Any new test table requiring deterministic seed data |
| 02 | [test-case-generation.md](test-case-generation.md) | Structured test cases for data pipelines | New pipeline feature, sprint test coverage, ADO import |
| 03 | [ado-csv-import.md](ado-csv-import.md) | Reformat test cases as ADO-compatible CSV | After test case generation, before ADO import |
| 04 | [requirements-comparison.md](requirements-comparison.md) | Requirements vs. proposal/contract gap analysis | New requirements document, scope review, client alignment |
| 05 | [meeting-minutes.md](meeting-minutes.md) | Structured meeting minutes from transcript or notes | Post any technical review or stakeholder meeting |
| 06 | [performance-testing-plan.md](performance-testing-plan.md) | Performance testing plan for data pipelines | New pipeline, capacity planning, load test design |

---

## Project Constraints (embedded in all templates)

All templates enforce the following DOM project constraints:
- **No PII or client data** in any prompt — synthetic/placeholder values only
- **HIPAA context** — outputs reference compliance requirements where applicable
- **Healthcare data regulations** — architectural claims are flagged for human verification
- **Human-in-the-loop** — every output requires review before delivery

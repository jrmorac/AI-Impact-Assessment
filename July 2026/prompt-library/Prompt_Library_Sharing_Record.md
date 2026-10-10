# Prompt Library — Sharing & Adoption Record
**Maintainer:** Jose Rafael Mora Casal  
**Asset Shared:** DOM QA Prompt Library (`prompts/` directory)  
**Purpose:** Track distribution and adoption of the prompt library as evidence of team-level AI impact

---

> **Why this record exists:**  
> The GAP AI Impact Framework (Dimension 5) evaluates whether AI work extends beyond individual contribution. This log records who the prompt library was shared with, what they used, and what outcome resulted. Update this record each time a colleague uses a template.

---

## Sharing Log

| # | Date | Shared With | Role | Channel | Templates Highlighted | Notes |
|---|------|-------------|------|---------|----------------------|-------|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |

*Fill in each row as you share. Channel = Teams / Email / Meeting / Confluence post / etc.*

---

## Adoption Log

Record each instance where a colleague used a template from the library (even informally).

### Adoption Entry Template

```
**Date:** 
**Colleague:** 
**Template Used:** [e.g., sql-test-data-generation.md]
**Task Applied To:** 
**Outcome / Time Saved:** 
**Evidence:** [e.g., Teams message, artifact delivered, ADO ticket]
```

---

### Adoption Entry 001
**Date:**  
**Colleague:**  
**Template Used:**  
**Task Applied To:**  
**Outcome / Time Saved:**  
**Evidence:**  

---

## RCA/CAPA Shareable Package — Sharing Log

**Asset Shared:** Agentic QA RCA/CAPA tool, shareable v3/v4 packages; Maria Fernanda Avila's documented pilot was on v4.

| # | Date | Shared With | Role | Channel | Notes |
|---|------|-------------|------|---------|-------|
| 1 | 2026-10-06 | Maria Fernanda Avila | Staff QA Engineer (different account/client) | Email (pilot invite sent) | Email couldn't carry the zip attachment (blocked by mail policy). |
| 2 | 2026-10-09 | Maria Fernanda Avila | Staff QA Engineer (different account/client) | v4 package hand-off channel unconfirmed; written feedback received by email | Completed browser demo, manual RCA session, and CAPA CSV export on v4. Reported both successful flows and actionable issues; see RCA Adoption Entry 001. |

### RCA Adoption Entry Template

```
**Date:** 
**Colleague:** 
**Package Version:** 
**Task Applied To:** 
**Outcome / Feedback:** 
**Evidence:** [e.g., Teams message, reply email, screenshot of run]
```

### RCA Adoption Entry 001
**Date:** 2026-10-09 (feedback received)
**Colleague:** Maria Fernanda Avila, Staff QA Engineer (different account/client)
**Package Version:** v4 (`agentic-qa-rca-shareable-v4`)
**Task Applied To:** Browser demo, manual RCA session, and CAPA CSV export using non-sensitive QA test inputs.
**Outcome / Feedback:** Maria reported the demo and manual session worked without browser console errors. She also identified actionable issues: `start-local.sh` assumes `python` exists on PATH; the launcher does not open the browser; CAPA and ADO export UI actions appear to write before explicit approval; an export conflict leaves stale loading text; the latest-session list does not show the latest session; and evidence suggestions include generated files. The export-approval mismatch is an open governance issue and must be fixed and regression-tested before broader distribution.
**Evidence:** Maria's email feedback, subject "Favor rápido — probar una herramienta de QA (10 minutos)" (received 2026-10-09); corresponding feedback copy in Jose's Downloads folder.

---

### Adoption Entry 002
**Date:**  
**Colleague:**  
**Template Used:**  
**Task Applied To:**  
**Outcome / Time Saved:**  
**Evidence:**  

---

### Adoption Entry 003
**Date:**  
**Colleague:**  
**Template Used:**  
**Task Applied To:**  
**Outcome / Time Saved:**  
**Evidence:**  

---

## AI Initiative Participation

Record any internal AI initiatives, squad sessions, or knowledge-sharing events participated in this cycle.

| Date | Event / Initiative | Role | What Was Contributed | Attendees / Audience |
|------|-------------------|------|----------------------|----------------------|
| 2026-10-07 | Hackathon agent/skills knowledge-share | Shared project example and guidance | Shared the public May hackathon repository and pointed a colleague to the custom `.github/agents/` and `.vscode/skills/` files for Postman API testing; colleague replied that she would explore it. No usage/adoption outcome confirmed yet. | Sonia Sijia |
| | | | | |

---

## Summary (for assessment use)

*Update this section when submitting or re-submitting the assessment.*

- **Asset created:** DOM QA Prompt Library — 6 reusable prompt templates for recurring QA tasks
- **Date created:** July 2026
- **Colleagues who received it:** *(fill in)*
- **Confirmed adopters:** *(fill in — minimum 1 for Level 2 evidence)*
- **AI initiatives participated in:** *(fill in)*
- **Evidence attachments:** This file + screenshots of sharing messages + any colleague-produced artifacts using the templates

# Copilot Instructions — DOM Project (QA Engineering)

## Project Context

- **Project:** DOM (Data Operations Management) platform
- **Client:** MediQuant (healthcare data management)
- **My role:** QA Engineer
- **Infrastructure:** Azure / Databricks
- **Work management:** Azure DevOps (ADO)

## Workspace Source of Truth

- For development changes, update and validate the main workspace at `C:\Users\JoseRafaelMoraCasal\AI Impact Assessment` unless the user explicitly requests worktree-only changes.
- If a session is running from an isolated worktree, transfer the implementation to the main workspace before testing, packaging, or reporting completion. Do not repeat full implementation and validation separately in both locations.

## Compliance Guardrails (NON-NEGOTIABLE)

This is a **HIPAA-regulated healthcare** environment. When generating any output:

- **Never** use real patient data, PII, or client production identifiers in examples, test data, or scripts.
- Use only **synthetic/placeholder values** (e.g., fixed emails like `jcasal@mediquant.com`, fixed IDs like `CustomerId: 647`).
- Do **not** propose workflows that send client data or production content to external AI tools.
- Automation and AI assistance apply only to **non-sensitive artifacts**: documentation, synthetic test data, test cases, QA strategies, requirements analysis, and meeting notes.
- Flag any output that touches compliance-sensitive areas for human review before use.

## QA Engineering Conventions

### Test Data (SQL)
- All test data scripts must be **deterministic** — running twice must produce identical records.
- Never use `GETDATE()`, `RAND()`, `NEWID()`, or other non-deterministic functions.
- Use a fixed anchor date; compute all timestamps as offsets from it.
- Target dialect: T-SQL (SQL Server / Azure SQL).
- Include realistic value distributions (status codes, severity levels, action types), not uniform fills.

### Test Cases
- Structure every test case as: **ID, Title, Type (Positive/Negative/Boundary), Preconditions, numbered Steps, Expected Result.**
- Always include negative and boundary scenarios: missing inputs, malformed inputs, empty inputs, known failure modes.
- Expected results must be **specific and verifiable** — never "should work correctly."

### ADO CSV Import
- Use **comma** delimiters (never semicolons — ADO import fails silently otherwise).
- Enclose all multi-line fields in double quotes; escape internal quotes as `""`.
- Work Item Type = `Test Case`; default State = `Design`.
- First row must be the exact ADO header schema.

### Documents (QA strategy, performance plans, requirements analysis)
- Verify architectural/tooling claims against actual DOM project setup before asserting them (e.g., container scanning uses **Trivy**, not Azure Defender).
- For requirements comparisons: every finding must trace to a specific source section — flag inferred items as "Requires Clarification," never as confirmed gaps.
- Use neutral, objective language; avoid implying contractual fault.

### Meeting Minutes
- Attribute every decision and action item to a **named** attendee; flag unclear attribution rather than guessing.
- Never invent action items not present in the source.

## AI Output Validation

Follow the human-in-the-loop process documented in [July 2026/metrics-and-logs/AI_Output_Validation_Log.md](../July%202026/metrics-and-logs/AI_Output_Validation_Log.md):
1. Trace AI claims to source material.
2. Test edge cases and determinism where applicable.
3. Confirm no PII / secrets / real data present.
4. Log corrections and caught hallucinations.

## Reusable Prompts

Prefer the parameterized templates in [prompts/](../prompts/README.md) for recurring tasks (SQL test data, test case generation, ADO CSV, requirements comparison, meeting minutes, performance testing plans) rather than starting from scratch.

# Prompt 01 — SQL Test Data Generation
**Task:** Generate deterministic SQL INSERT scripts for synthetic test data tables  
**Tools:** GitHub Copilot Chat, Claude, or ChatGPT  
**Validated:** ✅ Used for CustomerActivityLogs and CustomerExceptionLogs (June 2026)

---

## When to Use

- A new test table needs seed data for project testing
- Existing synthetic data needs to be regenerated with a different date range or volume
- You need realistic distribution across status codes, action types, or error categories

---

## SYSTEM CONTEXT
*(Paste this first into the AI chat)*

```
You are a SQL developer helping generate deterministic synthetic test data for a healthcare data management project.

CONSTRAINTS (non-negotiable):
- No real user data, PII, or production identifiers of any kind
- All user references must use fixed placeholder values (e.g., fixed email addresses, fixed numeric IDs)
- All scripts must be deterministic: running the script twice must produce identical records
- Do NOT use GETDATE(), RAND(), NEWID(), or any non-deterministic functions
- Use a fixed anchor date for all timestamp calculations; compute all dates as offsets from that anchor
- Output must be valid T-SQL compatible with SQL Server / Azure SQL

PROJECT CONTEXT:
- Project: DOM (Data Operations Management platform)
- Client environment: Highly regulated (healthcare data / HIPAA context)
- Test schema: [SCHEMA_NAME]
- Purpose: Synthetic test data for QA validation — no production data involved
```

---

## PROMPT TEMPLATE
*(Fill in all [PLACEHOLDERS], then paste after the system context)*

```
Generate a deterministic SQL INSERT script for the [TABLE_NAME] table with the following specifications:

TABLE STRUCTURE:
[Paste the CREATE TABLE statement or column definitions here]

REQUIREMENTS:
- Generate [NUMBER_OF_RECORDS] records
- Cover a date range from [START_DATE] to [END_DATE] (approximately [MONTHS] months)
- Distribute records realistically across the following values:
  - [COLUMN_1]: [VALUE_A] ([PERCENTAGE_A]%), [VALUE_B] ([PERCENTAGE_B]%), [VALUE_C] ([PERCENTAGE_C]%)
  - [COLUMN_2]: [DISTRIBUTION_DESCRIPTION]
- Use these fixed placeholder values for user/entity identifiers:
  - [IDENTIFIER_COLUMN]: [PLACEHOLDER_VALUE] (e.g., fixed UserId, fixed ProjectId)
- Anchor date for all timestamp calculations: [ANCHOR_DATE e.g., '2026-01-01']
- Group records [EVENLY / BY DISTRIBUTION] across the date range

EDGE CASES TO INCLUDE:
- [EDGE_CASE_1 e.g., records at month boundaries]
- [EDGE_CASE_2 e.g., records with NULL optional fields]
- [EDGE_CASE_3 e.g., minimum/maximum value boundaries]

OUTPUT FORMAT:
- A single INSERT INTO [TABLE_NAME] (...) VALUES (...) statement
- Include a comment block at the top explaining the seed logic and anchor date
- Add inline comments marking where edge case records appear
```

---

## Follow-Up Prompts

After reviewing the initial output, use these as needed:

**If distribution is off:**
```
The [COLUMN] distribution is not matching the required percentages. 
Recount the records per value and adjust — I need approximately [X] records 
with [VALUE_A] and [Y] records with [VALUE_B] out of [TOTAL] total records.
```

**If determinism check fails:**
```
Verify that your script contains no non-deterministic functions. 
List every function used in the script and confirm each one is deterministic.
```

**If edge cases are missing:**
```
Add [NUMBER] additional records specifically to cover [EDGE_CASE_DESCRIPTION]. 
Place them at the end of the INSERT block with a comment marking them as edge case records.
```

---

## Validation Checklist (before accepting)
- [ ] Ran the script twice — output is identical both times
- [ ] No `GETDATE()`, `RAND()`, `NEWID()`, or similar functions present
- [ ] Distribution percentages match requirements (count records per value)
- [ ] Date range boundaries are correct (first and last record dates)
- [ ] Month-boundary edge cases produce valid dates (no Feb 30 etc.)
- [ ] All placeholder values are synthetic — no real data present
- [ ] Script runs without errors on target schema

---

## Example Usage Note
*DOM project example (June 2026): Used for `CustomerActivityLogs` and `CustomerExceptionLogs`. Anchor date was `'2026-01-01'`. Issue caught: initial output used `DATEADD()` with minutes in a context expecting hours — corrected via reprompt.*

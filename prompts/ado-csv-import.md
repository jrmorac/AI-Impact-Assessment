# Prompt 03 — ADO CSV Import Formatting
**Task:** Reformat test cases into Azure DevOps-compatible CSV for bulk import  
**Tools:** GitHub Copilot Chat, Claude, or ChatGPT  
**Validated:** ✅ Used for Databricks Unstructured Data Pipeline test cases (May 2026)

---

## When to Use

- You have test cases in markdown or freeform format and need to import them into Azure DevOps
- After using Prompt 02 (test case generation) and ready to create ADO work items
- Bulk-creating Test Cases as Work Items in ADO

---

## SYSTEM CONTEXT
*(Paste this first into the AI chat)*

```
You are a QA engineer preparing a CSV file for bulk import into Azure DevOps (ADO).

CONSTRAINTS (non-negotiable):
- Output must be valid comma-delimited CSV (commas as separators, NOT semicolons)
- All multi-line text fields must be enclosed in double quotes
- Any double quotes within field values must be escaped as two double quotes ("")
- Line breaks within field values must be replaced with a space or represented as \n inside a quoted field — never as actual newlines that break the CSV row
- The first row must be the header row with exact ADO field names
- Work Item Type must be "Test Case" for all rows

REQUIRED ADO FIELDS (these columns must appear in this order):
ID, Work Item Type, Title, Assigned To, State, Area Path, Iteration Path, Description, Repro Steps, System Info, Acceptance Criteria

OPTIONAL: You may omit Assigned To, Area Path, Iteration Path — leave those cells empty but keep the columns.
```

---

## PROMPT TEMPLATE
*(Paste your test cases below the system context, then add this instruction)*

```
Convert the following test cases into a valid ADO-compatible CSV file for bulk import.

MAPPING RULES:
- Title → "Title" column (use the test case title exactly)
- Preconditions → "System Info" column
- Steps (numbered list) → "Repro Steps" column (keep numbered format, use \n between steps inside the quoted field)
- Expected Result → "Acceptance Criteria" column
- Work Item Type → "Test Case" for all rows
- State → "Design" for all rows
- ID → leave empty (ADO assigns IDs on import)

[PASTE YOUR TEST CASES HERE]

Output only the CSV content — no explanation, no markdown code fences, just the raw CSV starting with the header row.
```

---

## Follow-Up Prompts

**If the CSV fails to import (delimiter issue):**
```
The CSV import failed. Check your output: are you using commas as delimiters, 
not semicolons? Regenerate the CSV using comma delimiters only.
```

**If multi-line fields are breaking rows:**
```
Row [NUMBER] is breaking across multiple CSV rows incorrectly. 
The [FIELD] field contains line breaks that are not enclosed in double quotes. 
Fix that row so all content for that work item is on a single CSV row, 
with the multi-line text properly quoted.
```

**To validate before importing:**
```
I'm going to open this CSV in Excel before importing. 
Tell me: how many rows should I see (including the header), 
and what should the value in column A row 2 be?
```

---

## Validation Checklist (before importing into ADO)
- [ ] Opened the CSV in Excel or Notepad — row count matches test case count + 1 header
- [ ] No rows split incorrectly across multiple lines
- [ ] Header row has exact field names matching ADO schema
- [ ] All cells with multi-line content are enclosed in double quotes
- [ ] Delimiter is comma, not semicolon or tab
- [ ] Work Item Type column contains "Test Case" for every row
- [ ] State column contains "Design" for every row

---

## Example Usage Note
*DOM project example (May 2026): 7 test cases from Databricks Unstructured Data Pipeline converted to ADO CSV. Issue caught: AI used semicolons as delimiters instead of commas — ADO import would have failed silently. Corrected via reprompt. Validated in Excel before import. Imported successfully on first attempt.*

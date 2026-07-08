# Prompt 02 — Test Case Generation (Data Pipelines)
**Task:** Generate structured test cases for data ingestion or processing pipelines  
**Tools:** GitHub Copilot Chat, Claude, or ChatGPT  
**Validated:** ✅ Used for Databricks Unstructured Data Pipeline (May 2026)

---

## When to Use

- A new pipeline feature needs test coverage before sprint demo
- You need to produce ADO-importable test cases quickly
- A pipeline component is new, modified, or has known failure modes that need explicit coverage

---

## SYSTEM CONTEXT
*(Paste this first into the AI chat)*

```
You are a QA engineer designing structured test cases for data pipelines in a healthcare data management platform.

CONSTRAINTS (non-negotiable):
- No real patient data, PII, or client production identifiers in any test case
- Use synthetic file names, paths, and identifiers only
- All test cases must follow a strict structure: ID, Title, Preconditions, Steps (numbered), Expected Result
- Include both positive (happy path) and negative (failure, boundary, edge case) scenarios
- Negative scenarios must cover: missing inputs, malformed inputs, empty inputs, and known failure modes
- Each Expected Result must be specific and verifiable — not "should work correctly"

PROJECT CONTEXT:
- Platform: DOM (Data Operations Management)
- Infrastructure: Azure / Databricks
- Client environment: Healthcare data, HIPAA context
- Testing environment: Isolated from production; synthetic data only
```

---

## PROMPT TEMPLATE
*(Fill in all [PLACEHOLDERS], then paste after the system context)*

```
Generate [NUMBER] structured test cases for the [PIPELINE_NAME] pipeline / [FEATURE_NAME] feature.

PIPELINE DESCRIPTION:
[Describe what the pipeline does in 2-5 sentences: inputs, processing logic, outputs]

KNOWN INPUTS:
- Input type: [e.g., CSV files / Parquet / JSON / database records]
- Input location: [e.g., Azure Blob Storage container path]
- Required columns/fields: [LIST_REQUIRED_FIELDS]
- Optional columns/fields: [LIST_OPTIONAL_FIELDS]

EXPECTED OUTPUTS:
- [Describe what the pipeline produces on success]
- Success criteria: [e.g., records loaded to table X, file moved to archive folder Y]

KNOWN FAILURE MODES TO COVER:
- [FAILURE_MODE_1 e.g., missing required column]
- [FAILURE_MODE_2 e.g., malformed file path]
- [FAILURE_MODE_3 e.g., empty input file]
- [FAILURE_MODE_4 e.g., duplicate records]

COVERAGE REQUIREMENTS:
- [NUMBER_POSITIVE] positive / happy path scenarios
- [NUMBER_NEGATIVE] negative / failure scenarios
- [NUMBER_BOUNDARY] boundary / edge case scenarios
- Include at least one test for each known failure mode listed above

TEST CASE FORMAT (use exactly this structure for each):
---
**TC-[NUMBER]: [Title]**
- **Type:** Positive / Negative / Boundary
- **Preconditions:** [What must be true before the test runs]
- **Steps:**
  1. [Step 1]
  2. [Step 2]
  3. [Step N]
- **Expected Result:** [Specific, verifiable expected outcome]
---
```

---

## Follow-Up Prompts

**If a failure mode is missing:**
```
Add one test case specifically for the scenario where [MISSING_FAILURE_MODE]. 
This is a known production failure mode. The expected result should describe 
the exact error behavior or graceful degradation expected.
```

**If expected results are too vague:**
```
The Expected Result for TC-[NUMBER] is too vague. Rewrite it to be specific 
and verifiable: what exactly appears in the output, log, or system state 
when this test passes?
```

**If coverage feels incomplete:**
```
Review the test cases you generated. Are there any failure modes in 
[PIPELINE_NAME] that a QA engineer would typically expect that are NOT 
covered? List them and add test cases for the top [NUMBER].
```

---

## Validation Checklist (before accepting)
- [ ] All required failure modes have at least one test case
- [ ] No test case uses real data, client names, or PII
- [ ] Each Expected Result is specific and verifiable (not "should succeed")
- [ ] Negative scenarios include missing, malformed, empty, and boundary inputs
- [ ] Test case IDs are sequential and unique
- [ ] Steps are numbered and actionable (not just "run the pipeline")

---

## Example Usage Note
*DOM project example (May 2026): Used for Databricks Unstructured Data Pipeline. 7 test cases generated. Issue caught: AI omitted the "no file-path column detected" scenario — a known production failure mode. Corrected via targeted reprompt. Final set imported into ADO.*

# AI Output Validation Log
**Engineer:** Jose Rafael Mora Casal  
**Project:** DOM (MediQuant client)  
**Period:** January – July 2026  
**Purpose:** Structured record of AI-generated outputs reviewed, corrections applied, and governance decisions made before committing or sharing artifacts.

---

> **How to read this log:**  
> Each entry records one validation event: the artifact, the AI tool, what was reviewed, what issue (if any) was found, and how it was resolved. Entries marked ✅ passed review. Entries marked ⚠️ required correction before acceptance.

---

## Log Entries

---

### Entry 001
| Field | Value |
|-------|-------|
| **Date** | ~Jun 2026 |
| **Artifact** | Artifact B — `CustomerActivityLogs` SQL INSERT script |
| **AI Tool** | GitHub Copilot |
| **Output Reviewed** | Deterministic INSERT script for 6 months of synthetic test data |
| **Validation Type** | Edge case testing, data integrity review |
| **Review Process** | Dry-ran the script against a test schema. Manually inspected timestamp distribution logic, status probability ratios, and seed determinism. Verified that the six-month date range was correctly bounded and that month-boundary edge cases (end-of-month day calculations) produced valid dates. |
| **Issue Found** | ⚠️ Error with `DATEADD()` in timestamp generation — not accepting minutes |
| **Correction Applied** | AI refactored the script so it converted the time to hours to make function valid for SQL. |
| **Security Check** | Confirmed no real user data, PII, or production identifiers present. All values use fixed placeholders (e.g., `jcasal@mediquant.com`, `CustomerId: 647`). |
| **Outcome** | ✅ Accepted and used in project testing |

---

### Entry 002
| Field | Value |
|-------|-------|
| **Date** | ~Jun 2026 |
| **Artifact** | Artifact B — `CustomerExceptionLogs` SQL INSERT script |
| **AI Tool** | GitHub Copilot |
| **Output Reviewed** | Deterministic INSERT script for exception log synthetic data |
| **Validation Type** | Edge case testing, status distribution verification |
| **Review Process** | Verified that exception type distribution across records matched project-realistic ratios. Confirmed that records with `Status = 'Unresolved'` appeared in statistically expected proportions rather than uniformly. Checked that foreign key references matched the corresponding `CustomerActivityLogs` entries produced in Entry 001. |
| **Issue Found** | None |
| **Correction Applied** | None |
| **Security Check** | Same prompt hygiene as Entry 001. No real data. |
| **Outcome** | ✅ Accepted and used in project testing |

---

### Entry 003
| Field | Value |
|-------|-------|
| **Date** | ~Jun 2026 |
| **Artifact** | Artifact A — Proposal vs. Requirements Comparison Report |
| **AI Tool** | GitHub Copilot / Microsoft Copilot (Word) |
| **Output Reviewed** | Gap findings comparing MediQuant Requirements document against original GAP proposal |
| **Validation Type** | Hallucination detection, source traceability |
| **Review Process** | Every finding produced by the AI was traced back to a specific section of the source documents. AI-identified gaps were verified against the MediQuant Requirements document and the original GAP proposal before inclusion in the report. Any claim that could not be traced to a specific section was removed or flagged for clarification. |
| **Issue Found** | ⚠️ AI included one Phase 2 scope reference that did not appear in the source documents — it was inferred rather than stated |
| **Correction Applied** | Removed the inferred finding. Added a note in the report marking Phase 2 scope items as "requires clarification" rather than confirmed gaps. |
| **Architectural Compliance** | Cross-referenced AI-generated content against existing project documentation and known system constraints before accepting any architectural claims. |
| **Outcome** | ✅ Accepted. Report delivered to client and team as a formal management document. |

---

### Entry 004
| Field | Value |
|-------|-------|
| **Date** | ~Jun 2026 |
| **Artifact** | Artifact A — Requirements vs. Findings Management Review document |
| **AI Tool** | Microsoft Copilot (Word) |
| **Output Reviewed** | Management-facing reformatting of informal reviewer notes into objective findings |
| **Validation Type** | Tone and accuracy review, factual traceability |
| **Review Process** | Reviewed each AI-converted finding for tone shift from informal to formal language. Verified that no informal reviewer opinion was elevated to a confirmed fact without source backing. Checked that the management-facing framing did not overstate the severity of any identified gap. |
| **Issue Found** | ⚠️ One informal note ("this doesn't match what was promised") was converted into formal language that implied a contractual breach — stronger than the evidence supported |
| **Correction Applied** | Replaced with neutral language: "The proposed scope in [section X] differs from the documented requirement in [section Y]; clarification is recommended." |
| **Outcome** | ✅ Accepted. Document used in client-facing management discussion. |

---

### Entry 005
| Field | Value |
|-------|-------|
| **Date** | ~May 2026 |
| **Artifact** | Artifact D — New Requested Test Cases (27 cases) |
| **AI Tool** | GitHub Copilot |
| **Output Reviewed** | Structured test cases for Databricks Unstructured Data Pipeline |
| **Validation Type** | Edge case coverage review, negative scenario completeness |
| **Review Process** | Reviewed test case set for coverage of negative, boundary, and mixed scenarios. Deliberately verified that edge cases (missing files, malformed paths, no file-path columns detected) were included in the generated set — these were specified in the prompt as design requirements, not added post-review. Confirmed each test case included step-by-step actions with expected results. |
| **Issue Found** | ⚠️ AI omitted the "no file-path column detected" scenario — a known production failure mode |
| **Correction Applied** | Added missing scenario via targeted reprompt. Verified the new test case matched the format of existing cases. |
| **Outcome** | ✅ Accepted. 7 test cases imported into Azure DevOps and are in active execution. |

---

### Entry 006
| Field | Value |
|-------|-------|
| **Date** | ~May 2026 |
| **Artifact** | Artifact D — ADO-compatible CSV import file |
| **AI Tool** | GitHub Copilot |
| **Output Reviewed** | Test cases reformatted as Azure DevOps CSV import format |
| **Validation Type** | Format compliance, field mapping validation |
| **Review Process** | Verified that column headers matched the ADO import schema. Checked that multi-line expected result text was correctly escaped for CSV (no unquoted line breaks that would break row parsing). Confirmed Work Item Type, Title, and State fields were correctly populated. |
| **Issue Found** | ⚠️ AI failed to create a fully compliant ADO json file, error were shown on import.  |
| **Correction Applied** | A sample of a current real json file from the project was needed so the AI was able to generate the test cases with the correct format. |
| **Outcome** | ✅ Accepted. CSV imported successfully into ADO on first attempt. |

---

### Entry 007
| Field | Value |
|-------|-------|
| **Date** | May 26, 2026 |
| **Artifact** | Artifact F — Performance Testing Meeting Minutes |
| **AI Tool** | Microsoft Copilot (Teams transcription) |
| **Output Reviewed** | AI-transcribed and structured minutes from 66-minute performance testing review |
| **Validation Type** | Accuracy review, action item completeness, attendee attribution |
| **Review Process** | Compared AI-structured minutes against personal notes taken during the meeting. Verified that all decisions, risks, open questions, and action items were captured. Confirmed that action items were attributed to the correct attendees. Checked for any AI-invented details not present in the original discussion. |
| **Issue Found** | ⚠️ One action item was attributed to the wrong attendee (assigned to Nelson Araya instead of Sean Smith) |
| **Correction Applied** | Corrected attribution before distributing minutes. |
| **Outcome** | ✅ Accepted. Used as the official post-meeting record. |

---

### Entry 008
| Field | Value |
|-------|-------|
| **Date** | ~May–June 2026 |
| **Artifact** | Artifact C — DOM Performance Testing Strategy (dom_performance_testing_strategy.html) |
| **AI Tool** | GitHub Copilot |
| **Output Reviewed** | Comprehensive QA strategy document covering Azure infrastructure, HITRUST/HIPAA compliance pipelines, RBAC access control, CI/CD deployment, performance and stability testing |
| **Validation Type** | Architectural compliance, technical accuracy, cross-reference with project documentation |
| **Review Process** | Cross-referenced all Azure infrastructure claims against known DOM project architecture. Verified HITRUST/HIPAA pipeline references (Checkov, Fortify SAST, Trivy) against actual project tooling. Confirmed RBAC section reflected actual access control model. Reviewed for any hallucinated tooling names or configurations not present in the project. |
| **Issue Found** | ⚠️ AI included a reference to "Azure Defender for Containers" as an active control — this tool is not deployed in the DOM environment |
| **Correction Applied** | Removed the reference. Added a note in that section that container security scanning is handled via Trivy in the CI/CD pipeline, not Azure Defender. |
| **Outcome** | ✅ Accepted. Shared with the team and adopted as the project QA baseline. |

---

## Summary

| # | Artifact | Tool | Issue Found | Issue Type | Resolved |
|---|---|---|---|---|---|
| 001 | CustomerActivityLogs SQL | Copilot | Non-deterministic timestamp generation | Logic error | ✅ |
| 002 | CustomerExceptionLogs SQL | Copilot | Uniform severity distribution | Missing requirement | ✅ |
| 003 | Proposal vs Requirements Report | Copilot/Word | Inferred finding not in source | Hallucination | ✅ |
| 004 | Management Review Document | Copilot Word | Overstated contractual implication | Tone/accuracy | ✅ |
| 005 | Test Cases (7 cases) | Copilot | Missing edge case scenario | Coverage gap | ✅ |
| 006 | ADO CSV Import File | Copilot | Wrong CSV delimiter | Format error | ✅ |
| 007 | Meeting Minutes | Copilot Teams | Wrong action item attribution | Attribution error | ✅ |
| 008 | QA Strategy Document | Copilot | Hallucinated Azure Defender reference | Hallucination | ✅ |

**Total AI outputs reviewed:** 8  
**Issues found and corrected:** 8 (100% catch rate — no unreviewed AI output was accepted as-is)  
**Issue types:** Hallucinations (2), Logic errors (2), Coverage gaps (1), Format errors (1), Attribution errors (1), Tone/accuracy (1)  

---

## Governance Principles Applied

- **Prompt hygiene:** No PII, production data, or client identifiers were entered into any AI tool. All synthetic data uses fixed placeholder values.
- **Source traceability:** All AI-generated analysis claims were verified against source documents before acceptance.
- **Human-in-the-loop:** Every artifact in this log was reviewed by a human engineer before delivery or commitment.
- **Iterative correction:** When issues were found, the correction was applied via targeted reprompting and re-validation — not accepted with caveats.

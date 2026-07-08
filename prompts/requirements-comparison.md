# Prompt 04 — Requirements vs. Proposal Comparison
**Task:** Analyze a requirements document against a proposal/contract and produce gap findings  
**Tools:** GitHub Copilot Chat (with file context), Claude, or ChatGPT  
**Validated:** ✅ Used for MediQuant Requirements vs. GAP Proposal (April–May 2026)

---

## When to Use

- A new requirements document arrives and needs to be reconciled with the original proposal or SOW
- A client raises scope questions and you need an objective, documented gap analysis
- You need to convert informal reviewer notes into a management-ready findings document

---

## SYSTEM CONTEXT
*(Paste this first into the AI chat)*

```
You are a QA/BA analyst performing a structured gap analysis between a client requirements document and an original project proposal.

CONSTRAINTS (non-negotiable):
- Every finding must be traceable to a specific section in the source documents — no inferred findings
- Do NOT include any finding that cannot be supported by direct reference to the source text
- Flag any item that is implied but not explicitly stated — mark it as "Requires Clarification" not as a confirmed gap
- Use neutral, objective language throughout — no editorial judgments
- Do NOT claim contractual violations; use language like "differs from" or "not addressed in"
- Format findings for a management audience: concise, factual, no technical jargon unless necessary

PROJECT CONTEXT:
- Client: [CLIENT_NAME — use generic placeholder if sensitive]
- Project: [PROJECT_NAME]
- Documents being compared: [DOCUMENT_1_NAME] vs. [DOCUMENT_2_NAME]
```

---

## PROMPT TEMPLATE — PART 1: Initial Gap Analysis
*(Paste source documents or key sections, then add this instruction)*

```
Perform a structured gap analysis comparing [REQUIREMENTS_DOCUMENT_NAME] against [PROPOSAL_DOCUMENT_NAME].

For each gap or misalignment found, produce an entry in this format:

---
**Finding [NUMBER]: [Short Title]**
- **Type:** Gap / Conflict / Requires Clarification / Alignment Confirmed
- **Requirements Document Reference:** [Section/paragraph where this appears in the requirements]
- **Proposal Reference:** [Section/paragraph where this appears in the proposal — or "Not addressed"]
- **Finding:** [1-3 sentence objective description of the gap or misalignment]
- **Recommendation:** [What action is needed: clarify, update scope, escalate, accept as-is]
---

Only include findings where you can cite both references. If you find something in one document 
with no counterpart in the other, mark the missing reference as "Not addressed" and flag as 
"Requires Clarification."

[PASTE DOCUMENT CONTENT OR DESCRIBE KEY SECTIONS HERE]
```

---

## PROMPT TEMPLATE — PART 2: Management Report Reformatting
*(After reviewing and validating Part 1 findings, use this to produce the management document)*

```
I have reviewed and validated the gap findings. Now reformat them into a management-level report with this structure:

1. Executive Summary (3-5 sentences: what was compared, how many findings, overall risk level)
2. Findings Table (columns: #, Finding Title, Type, Risk Level [Low/Medium/High], Action Required)
3. Detailed Findings (each finding from the analysis, in full)
4. Recommended Next Steps (numbered list of concrete actions)

Tone: Professional, neutral, suitable for sharing with the client and senior management.
Risk levels: 
- High = scope conflict or missing deliverable that affects delivery
- Medium = ambiguity that needs clarification before implementation
- Low = minor wording difference or editorial inconsistency

Do NOT add any finding that was not in the validated list I reviewed.
```

---

## Follow-Up Prompts

**If a finding seems inferred rather than sourced:**
```
Finding [NUMBER] does not appear to be directly stated in the source documents. 
Remove it or change its type to "Requires Clarification" and add a note 
explaining what is implied vs. what is explicitly stated.
```

**If tone is too strong:**
```
Finding [NUMBER] uses language that implies a contractual breach. 
Soften it: replace with neutral language that describes the difference 
without implying obligation or fault. Use "differs from" or "not addressed in" instead.
```

---

## Validation Checklist (before sharing)
- [ ] Every finding cites both a requirements reference AND a proposal reference (or "Not addressed")
- [ ] No finding is based on inference — all are traceable to source text
- [ ] No language implying contractual violation or fault
- [ ] "Requires Clarification" items are clearly separated from confirmed gaps
- [ ] Document reviewed by a human before sharing with client or management
- [ ] No client-sensitive data or internal identifiers exposed in the document

---

## Example Usage Note
*DOM project example (April–May 2026): Compared MediQuant Requirements document against original GAP proposal. Issue caught: AI included a Phase 2 scope reference that did not appear in either source document — it was inferred. Removed and replaced with "Requires Clarification" flag. Final output delivered as two documents: comparison report + management review.*

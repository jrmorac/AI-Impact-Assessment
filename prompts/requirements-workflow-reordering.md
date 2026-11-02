# Prompt 07 - Requirements Analysis and Workflow Reordering
**Task:** Reorder an existing requirements checklist around the user journey while preserving traceability and recording evidence-based questions.
**Tool:** GitHub Copilot Chat with authorized, non-sensitive local files and spreadsheet tooling.
**Validation history:** Applied to the DOM checklist on 2026-10-19; 86 requirements and 111 original story references preserved. Automated integrity checks passed; PO approval and desktop Excel visual review remain unverified.

---

## When to Use

- A Product Owner wants requirements arranged in the sequence users experience the application.
- Technical prerequisites and background processing must be placed alongside the user actions they support.
- Existing requirement IDs, story links, phases and coverage statuses must survive the reordering.

This reorganizes an existing checklist. It does not reprioritize delivery, approve scope changes, or certify implementation or compliance.

## Inputs

Provide authorized, non-sensitive documents and fill in these parameters. Remove patient data, PII, secrets and production identifiers before supplying sources. Do not transmit sensitive client material to external AI services.

| Parameter | Value to Supply |
|-----------|-----------------|
| `[PROJECT]` | Project name or safe placeholder |
| `[PROPOSAL_PATH]` | Original proposal or approved scope reference |
| `[CHECKLIST_PATH]` | Existing requirements workbook and worksheet |
| `[BACKLOG_PATH]` | Exported stories, bugs and tasks; include acceptance criteria when authorized and available |
| `[USER_WORKFLOW]` | Ordered user journey, including correction/repeat loops |
| `[CONFIRMED_CHANGES]` | Approved architecture/terminology changes, with source and date |
| `[PROVISIONING_BOUNDARIES]` | Resources created per customer/project/execution, including dependencies |
| `[DEPLOYMENT_TRIGGER]` | Who deploys updated code and when; distinguish releases from routine use |
| `[BLANK_COVERAGE_LABEL]` | Approved label for blank Coverage; default: Need Review |
| `[OUTPUT_PATH]` | New Excel workbook; never overwrite the source |
| `[REVIEW_OWNER]` | Human role responsible for scope, mapping and acceptance decisions |

## Master Prompt

```text
Act as a senior business analyst for [PROJECT]. Analyze the supplied sources
and create a new Excel workbook at [OUTPUT_PATH], ordering the existing
requirements to follow the user workflow.

SOURCES
- Proposal / scope reference: [PROPOSAL_PATH]
- Existing requirements checklist: [CHECKLIST_PATH]
- Backlog export: [BACKLOG_PATH]
- User workflow: [USER_WORKFLOW]
- Confirmed changes, authority and date: [CONFIRMED_CHANGES]
- Provisioning boundaries: [PROVISIONING_BOUNDARIES]
- Code deployment trigger: [DEPLOYMENT_TRIGGER]
- Blank coverage label: [BLANK_COVERAGE_LABEL]
- Human review owner: [REVIEW_OWNER]

1. Establish the baseline before editing.
Read actual source contents, headers, worksheets and row counts. Do not infer
document contents from filenames or binary previews. If a source cannot be
read, state the limitation and ask for an accessible copy.
Use the proposal as the historical scope baseline, the checklist as the
artifact to reorder, and the backlog as supporting evidence. Attribute later
confirmed changes rather than silently rewriting the historical baseline.
Preserve original backlog titles, even if they mention a replaced technology.
Treat title-only mappings as provisional; titles and states cannot prove
acceptance criteria or tested coverage.

2. Resolve the controlling workflow boundaries.
Identify the actors, triggers, dependencies, user actions, automated steps,
outputs, exception paths and repeat loops. Ask only questions whose answers
materially change placement; do not ask again for facts already supplied.
Distinguish shared platform prerequisites, customer provisioning, project
provisioning, execution-time resources, reporting, ongoing lifecycle and
dev-team-triggered code releases. Do not assume deployment or provisioning
occurs on every execution. Record unresolved timing as Requires Clarification.

3. Preserve each original requirement as one whole row.
Keep original Requirement ID, Phase, Requirement and Story IDs exactly as
provided, including unresolved story placeholders. Do not renumber IDs,
rewrite wording, merge/split rows, duplicate requirements or delete rows.
Preserve Coverage exactly except blank cells become the approved blank label.
Distinguish blank cells from nonblank values such as Not Covered or Out of Scope.
If source IDs are missing or duplicated, flag them and retain source-row
identity; do not invent replacements or silently deduplicate the baseline.
Keep Phase independent of workflow order. Future requirements remain Future.
Covered does not mean implemented, tested, released or accepted.
Keep every original story link. Put possible replacements/additions in a
separate Suggested Story IDs (unapproved) field, never in the original field.
Do not create requirements for capabilities mentioned only in backlog titles.

4. Reorder by purpose and execution sequence, not by technology alone.
Give each requirement one primary stage and record secondary applicability
without duplicating the row. Within stages, order prerequisites, user actions,
processing, validation, outcomes and exception handling as supported by sources.
Place SQL queries, notebooks, infrastructure and SDK actions where they
actually run. Distinguish metadata capture during processing from later review.
Do not place post-load checks before their staged-data dependencies.
Show correction loops explicitly: new/corrected files return to acquisition;
existing stored files may return directly to execution. Do not equate manual
reruns with incremental loads, CDC, deletion or near-real-time capabilities.
Put confirmed current technology in added guidance. Preserve historical source
wording; propose any requirement wording changes separately for human approval.

5. Produce an auditable workbook.
Include:
- Workflow Requirements: original columns first, then Workflow Order, Workflow
  Stage, Workflow Substep, Activity Type, Also Applies To, Original Excel Row,
  Mapping Review, Review Notes, Source Reference and Suggested Story IDs (unapproved).
- Original Baseline: original row order and cell values, including blank coverage.
- Workflow Summary: stage sequence, technical boundaries and phase/count totals.
- Story References: original versus suggested links, exact exported title,
  work-item type, exported state and evidence limits; identify absent IDs.
- Review Register: review ID, severity, requirement/source reference, observation,
  evidence, decision needed and open status. Separate factual differences from
  inferred concerns; mark unsupported conclusions Requires Clarification.
- Read Me: source authority, confirmed changes, assumptions, scope limits,
  correction loop, review owner and rollback to the untouched source.
- Audit Evidence: executed checks, results, caught corrections and limitations.
Reference specific source sections, worksheet rows or story IDs for findings.
Suggested links are recommendations, not verified replacements or scope approval.
Use readable wrapping/row heights, filters, frozen headers and sensible widths.
Open the new workbook on the workflow view; avoid macros and external links.
Do not copy unnecessary production resource names, identities or sensitive data.

6. Audit adversarially and repair before claiming completion.
Derive expected counts from the actual input; do not hard-code this example's
counts into future runs. Independently reopen the output and verify:
- Every input requirement occurs exactly once using its original row identity.
- IDs, requirement wording, phase and original story links match the baseline.
- Only originally blank coverage cells changed, to the approved label.
- The embedded baseline exactly matches the source values and row order.
- Stage totals, phase totals and coverage totals reconcile with the source.
- Workflow keys sort correctly and source-row pointers resolve correctly.
- Every original numeric story reference is accounted for; missing IDs and
  unresolved placeholders are flagged rather than silently removed.
- Suggested IDs exist in the supplied export and remain explicitly unapproved.
- Technical steps respect confirmed provisioning, deployment and data dependencies.
- Notes do not describe uploads, reporting or costing as validation by accident.
- The workbook reopens cleanly; input files are unchanged; a rebuild produces
  the same worksheet cell values where generation is deterministic.
Inspect the output independently of the generation logic where practical.
Correct defects, rerun affected checks, and record what was caught and fixed.
If desktop Excel rendering is unavailable, disclose that visual layout remains
unverified. If any requirement cannot be met, identify the exact limitation.
Do not label a test PASS merely because a check was planned.

7. Deliver the new workbook and a concise evidence-based summary.
Report requirement/link counts, coverage changes, actual checks performed,
unresolved decisions and human-review needs. Distinguish artifact-integrity
success from semantic acceptance, product release readiness and compliance.
Do not invent time savings, ROI, adoption, team usage or approval.
Do not stop at a plan when the requested files and tooling are available.
```

## Validation and Follow-Up

- Have the review owner walk through initial ingestion and correction/reingestion scenarios.
- Confirm suggested mappings against story descriptions and acceptance criteria, not titles alone.
- Review security, access, retention and regulated-data implications with authorized owners.
- Record actual review outcome, corrections, elapsed effort and reuse only when observed.
- For assessment evidence, retain the before/after artifacts, generation method and audit results. A reusable prompt alone does not demonstrate colleague adoption or organizational impact.

## Validated Example

DOM application on 2026-10-19: customer creation > project creation > dataset import to storage > Databricks execution > reports/analysis > correction and repeat processing. The user confirmed customer resource provisioning, project-container-only setup, databases created as needed during execution, and functionality-triggered code releases.

The generated workbook retained 86 requirements, 57 Phase 1 rows, 29 Future rows and 111 original story references. Four blank Coverage cells became Need Review. Two generator/guidance defects were caught and corrected; rebuilding produced identical worksheet values. These are artifact-integrity results, not evidence of PO acceptance or measured productivity improvement.

Evidence: [workflow-ordered workbook](../October%202026/deliverables/DOM%20Product%20Acceptance%20Checklist%20-%20Workflow%20Ordered.xlsx) and [reproducible generator](../October%202026/deliverables/build_workflow_checklist.py).
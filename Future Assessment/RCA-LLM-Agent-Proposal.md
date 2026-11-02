# Proposal: LLM-Assisted Root Cause Analysis Agent

**Prepared:** October 29, 2026  
**Status:** Feasibility proposal for discussion; not an approved implementation plan  
**Track relevance:** Engineering

## Executive summary

Explore extending the existing deterministic, local, web-based RCA assistant with an optional LLM-powered agent that proposes candidate root causes and validation steps from user-provided facts and explicitly approved project context. Keep the existing 5-Why flow as the predictable baseline. The agent should assist analysis, not decide or publish the final root cause.

The concept is feasible in principle. A small, human-reviewed prototype using synthetic or otherwise explicitly approved, non-sensitive inputs is a reasonable first step. Feasibility for a real project depends on the selected Claude or GitHub Copilot environment, approved context sources, data-handling rules, and how the agent can access those sources. An agent or skill can guide the analysis, but does not by itself provide safe, complete project context.

This proposal is exploratory. It does not authorize changes to RCA v4, a production integration, or use of client data with an external AI service. The current Future Assessment context records an open v4 approval-flow finding and says v5 has not started; agree scope and address applicable release gates before implementation or broader distribution. See [Future Assessment context](./SESSION_CONTEXT.md).

## Problem and opportunity

The current RCA tool provides a deterministic 5-Why workflow and requires the user to enter the analysis. Feedback identified a limitation: it does not offer candidate answers or intelligent suggestions because LLMs are not integrated. Meanwhile, users may already have access to AI assistants such as Claude or GitHub Copilot.

An agent could make the workflow more helpful by proposing evidence-linked hypotheses, identifying missing information, and suggesting ways to test a hypothesis. The key question is whether it can do this safely and usefully with approved project context, while preserving user control and the reliability of the existing flow.

## Feasibility assessment

| Area | Initial assessment | Condition or unknown |
|---|---|---|
| User value | Promising: suggestions may help users move from symptoms to testable hypotheses. | Validate with representative synthetic cases and reviewers; do not assume faster or better outcomes. |
| Technical approach | Feasible as an agent/skill workflow or, later, as an application-level model integration. | Confirm which Claude/Copilot product and capabilities are approved and available. |
| Context grounding | Feasible if the agent receives a small, approved set of relevant project material. | Identify source documents, access method, freshness, permissions, and citation behavior. |
| Safety and quality | Feasible with constrained inputs, evidence-linked suggestions, uncertainty handling, and human approval. | Test unsupported claims, missing context, sensitive-input handling, and failure behavior. |
| Local web app integration | Possible, but materially expands scope beyond authoring an agent/skill. | Requires an approved model endpoint and design for authentication, data flow, logging, errors, support, and deployment. |
| Assessment evidence | Potentially relevant to agentic capability, validation, productivity measurement, and multiplier impact. | Evidence must show actual validation, measured results, and confirmed adoption; a prototype alone does not establish systemic impact or a level. |

## Proposed experience and boundaries

1. The user starts with the existing RCA flow and enters a concise problem statement and known facts.
2. The agent asks focused follow-up questions when important facts are missing.
3. When requested, the agent proposes a small set of **candidate** causes. Each proposal identifies:
   - which supplied facts or approved sources support it;
   - what remains unknown or is only an assumption; and
   - one or more practical checks that could support or refute it.
4. The user accepts, edits, or rejects each proposal. The existing deterministic flow remains usable if the agent is unavailable or not appropriate.
5. A human reviews and approves the final RCA. The agent does not autonomously close an RCA, update a system of record, create a CAPA/ADO item, or represent a hypothesis as a confirmed cause.

For the first prototype, keep the agent read-only and separate from any consequential workflow actions. Do not provide it with patient data, PII, production content, credentials, or sensitive client identifiers. Use synthetic cases unless an authorized review explicitly approves a sanitized dataset and the destination environment.

## Implementation options

### Option A — Platform-native agent or skill (recommended for initial feasibility)

Define the RCA analysis workflow in the approved Claude or GitHub Copilot environment. Supply only synthetic case material and approved, non-sensitive context. Keep the current web tool unchanged and compare the agent's suggestions with its deterministic 5-Why flow.

**Advantages:** Smaller initial change; tests the value of LLM-generated hypotheses before adding application integration.  
**Limitations:** Experience may be separate from the web app; context access and agent capabilities depend on the organization's configured platform.

### Option B — LLM integrated into the web application (consider only after the pilot)

Add a model-backed suggestion feature to the local web application, with explicit controls for data submitted, approved model/service, credentials, logging, failure handling, and user review.

**Advantages:** More integrated user experience and potential to preserve workflow context.  
**Limitations:** Larger engineering, security, compliance, and operational scope. Requires platform approval and a documented data-flow review before implementation.

Do not assume an agent/skill can automatically read the local application's files or project systems. Verify the selected platform's actual access and tool-integration capabilities before choosing an architecture.

## Proposed phases

### Phase 1 — Scope and approval

- Agree whether this is a separate prototype or proposed RCA v5 work; do not modify v4 as part of this exploration.
- Select the approved assistant environment and confirm its allowed data boundary.
- Choose synthetic case inputs and a small set of approved, non-sensitive context documents.
- Define human review responsibilities, prohibited actions, and a process for reporting a bad or unsafe suggestion.

### Phase 2 — Behavior specification

- Specify the agent's inputs, output structure, context sources, and when it must ask a question or abstain.
- Require clear separation of observed facts, hypotheses, assumptions, and proposed checks.
- Require a traceable source reference for every contextual claim; if no source supports a statement, label it as a hypothesis or omit it.
- Keep suggestions optional, read-only, and explicitly subject to human approval.

### Phase 3 — Synthetic prototype

- Create the platform-native agent/skill and a fixed synthetic evaluation set covering well-supported, ambiguous, incomplete, and contradictory cases.
- Run the existing deterministic workflow and the agent workflow on the same cases.
- Record outputs and reviewer judgments without including sensitive content.

### Phase 4 — QA evaluation and iteration

- Review factual support, usefulness, testability, missing-information behavior, and whether the agent correctly avoids overclaiming.
- Include cases with no plausible supported cause, conflicting evidence, malformed or empty inputs, and requests that would require prohibited data.
- Log errors and corrections; revise the instructions or context set, then rerun the same cases to check repeatability and regressions.

### Phase 5 — Controlled pilot decision

- If platform/data approvals and test results support continuing, request approval for a narrowly scoped pilot with consenting users and approved inputs.
- Measure outcomes against the deterministic baseline using a documented method.
- Decide whether to retain the separate agent, integrate it into the application, revise it, or stop. Do not expand use until applicable review and release gates are satisfied.

## Validation and initial acceptance criteria

The prototype is ready for a pilot decision only when all of the following are observable:

- The existing deterministic RCA flow remains available and does not depend on the LLM.
- Each agent suggestion is clearly labeled as a hypothesis, distinguishes facts from assumptions, and includes a proposed validation step.
- Context-dependent claims identify their approved source; unsupported claims are flagged or withheld.
- The agent requests missing information or abstains when the supplied evidence is inadequate, instead of asserting an unsupported root cause.
- Human approval is required before any proposed cause becomes a final RCA or any action is taken outside the analysis conversation.
- A fixed synthetic test set includes positive, negative, and boundary scenarios, and the evaluation records both successful behavior and failures/corrections.
- No patient data, PII, production content, credentials, or sensitive client identifiers are used in the prototype or its evidence.
- The pilot decision includes actual results, known limitations, and a named human owner for review; there is no success claim based solely on a demo.

## Measures to collect (baseline first)

Capture a baseline using the existing workflow before claiming improvement. Select a manageable set of measures, define their calculation, and compare the same or comparable synthetic cases:

- Time from case start to a human-reviewable candidate hypothesis.
- Reviewer rating of whether a suggestion is supported by evidence and useful to the investigation.
- Percentage of suggestions accepted, edited, or rejected, with reasons.
- Unsupported-claim rate and rate of appropriate abstention when information is insufficient.
- Number and type of missing facts identified that reviewers consider relevant.
- Whether a proposed validation step was actionable and actually used.

Do not equate suggestion count, prompt execution, or user interest with productivity, quality improvement, ROI, or team adoption. Report limitations and sample size alongside any results.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Fabricated or overconfident causes | Label outputs as hypotheses; require evidence references and test steps; support abstention; retain human approval. |
| Sensitive information sent to an unapproved service | Start with synthetic inputs; confirm platform approval and data boundaries before any real-world use; do not include sensitive data in prompts or evidence. |
| Irrelevant or stale project context | Allowlist sources, identify their version/date, minimize context, and have a human verify applicability. |
| Users treat suggestions as facts | Display uncertainty and supporting/missing evidence; preserve the distinction between candidate and confirmed cause. |
| Integration bypasses existing approval controls | Keep the prototype read-only; separately review any future write/export actions and regression-test approval requirements. |
| Unclear benefit or no adoption | Compare with a baseline, gather reviewer feedback, and distinguish confirmed use from interest. Stop or revise if value is not demonstrated. |
| Scope expands before governance is ready | Agree scope, ownership, acceptance criteria, risks, and rollback/stop conditions before implementation or pilot. |

This proposal does not resolve or supersede the existing v4 open finding; use the current [Future Assessment context](./SESSION_CONTEXT.md) and applicable development records when deciding project scope.

## Decisions to make during review

- Which environment is the target for the first prototype: Claude, GitHub Copilot, or another organization-approved option?
- Is the intended deliverable a standalone agent/skill, an application-integrated feature, or a staged path from one to the other?
- What project context is approved, who owns it, and how will the agent access it without exposing restricted information?
- Is RCA v5 the intended project scope, and what must be resolved before work can begin?
- Who will review the cases and suggestions, and what evidence is required before a pilot?
- What baseline and outcome measures are feasible, and over what period?

## Potential assessment evidence

If work proceeds, preserve non-sensitive, attributable artifacts such as the approved design, agent/skill definition, synthetic test cases, validation log, documented corrections, measured baseline-versus-pilot results, and evidence of colleague use. Attach relevant artifacts independently to each assessment question they support. Describe only work actually completed and results actually measured.

Potential dimension mapping (not a level prediction):

- **Agentic capability:** the designed workflow, tool/context boundaries, and evidence that it performs a useful multi-step analysis.
- **Validation and quality:** test results, unsupported-claim handling, abstentions, human review, and documented corrections.
- **Productivity and measurable impact:** reproducible comparison against the baseline, with methodology and observed results.
- **Multiplier impact:** reusable documentation or agent assets and confirmed use by others.
- **Daily workflow integration:** evidence only if the workflow is actually incorporated into recurring engineering work.

The assessment framework and this proposal do not guarantee an evaluation outcome. The official review process and manager calibration remain authoritative.

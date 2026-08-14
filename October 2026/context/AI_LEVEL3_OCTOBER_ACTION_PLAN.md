# AI Level 3 Action Plan — October 2026

## Goal
Reach Level 3 in the Engineering track by October 2026 by demonstrating:
- AI-first daily workflow
- disciplined validation
- measurable productivity impact
- agentic/systemic workflow execution
- adoption beyond personal use

## Core strategy
Use the Agentic QA project as the primary evidence asset, but do not rely on production client data or sensitive evidence. The project is positioned as a reusable, shareable QA workflow built around synthetic data and governance-safe practices. It should not be presented as a complete Six Sigma or RCA implementation unless that terminology is explicitly requested.

## Current implementation status — August 14, 2026

- The preferred entry point is the local Web UI, not the terminal.
- The shareable package is `October 2026/agentic-qa-rca-shareable/`.
- The package includes `Why 1`, `Why 3`, and `Why 5` demo cases.
- `Run Demo Case` generates the RCA report, CAPA CSV, and ADO Test Case CSV automatically.
- `Run Quick Plan` is optional and intended for repeatable predefined-plan execution.
- Current latest distribution: `October 2026/dist/agentic-qa-rca-shareable-20260814-160656.zip`.

## Sequence of actions

### 1) Stabilize the shareable project
- Ensure the project runs reliably in local setup.
- Create a clear quick-start README.
- Document what the workflow does and what it does not do.
- Make the project easy for a teammate to execute without help.

Deliverable:
- working local project with clear onboarding instructions

### 2) Pilot with 2–3 colleagues
- Share the project with 2–3 teammates.
- Ask each user to run one synthetic defect flow.
- Collect 3 types of feedback:
  - ease of use
  - clarity of output
  - suggestions for improvement
- Save comments in a short feedback file.

Deliverable:
- pilot feedback summary with 2–3 participant records

### 3) Build a validation log
- Record the outputs generated.
- Note what was reviewed.
- Note any corrections or issues identified.
- Capture examples where validation prevented weak or unsupported conclusions.

Deliverable:
- AI validation log with at least 5–10 entries

### 4) Capture simple metrics
- Measure before/after workflow effort for a few sample tasks.
- Track at least 3 metrics, such as:
  - time to produce a defect analysis
  - time to prepare RCA/CAPA artifacts
  - number of defects handled per session
- Use a simple table and keep the methodology explicit.

Deliverable:
- small metric sheet with methodology and trend data

### 5) Publish one reusable team asset
- Turn the project or supporting workflow into a reusable asset for others.
- Examples:
  - prompt library
  - workflow guide
  - usage template
  - execution checklist
- Make it accessible to teammates and document adoption.

Deliverable:
- one reusable team asset with evidence of usage

### 6) Create the Level 3 narrative
Prepare a concise story that links the work to the 5 evaluation dimensions:
- D1: AI-first workflow in daily tasks
- D2: validation and governance process
- D3: measurable impact
- D4: agentic/systemic workflow execution
- D5: adoption and multiplier effect

Deliverable:
- one-page narrative summary of the project and value created

### 7) Finalize evidence package for October
Assemble the final evidence set:
- README / setup instructions
- pilot feedback summary
- validation log
- metrics sheet
- reusable team asset
- example outputs from the workflow

Deliverable:
- compact evidence bundle ready for self-evaluation submission

## Success criteria for October
The project is Level 3-ready when it can be framed as:
- a reusable AI-enabled QA workflow
- built around governance-safe synthetic inputs
- validated by human review
- measured for impact
- shared and used by multiple teammates

## Key principle
The objective is not to pretend this is production data work. The objective is to demonstrate a credible, repeatable, documented, and shared AI engineering workflow that is relevant to regulated QA and is strong enough to show Level 3 impact.

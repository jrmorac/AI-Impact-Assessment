# Prompt: Reorganize AI Impact Assessment Workspace

## Goal
Reorganize loose files in the `AI Impact Assessment` workspace into a clear folder
structure. **Move files only — do not edit, rename, or alter file contents.**

## Rules
- Preserve exact file names (including spaces and `[A]`–`[G]` prefixes).
- Move files using OS-level moves; do not recreate or overwrite existing files.
- Do not delete anything. If a target file already exists, stop and report the conflict.
- Update any relative links inside `.md` files **only if** the move breaks them; report each change.
- Report a summary table of every move performed.

## Target Structure

### Workspace root (`/`)
Create `reference/` and move:
- `AI Evaluation - July Cycle - FAQ.md`
- `AI Impact Assessment   - Technical Guide.md`
- `AI IMPACT EVALUATION ENGINEERS FAQ.md`

### `July 2026/`
Create the following subfolders and move files into them:

**`deliverables/`**
- `[A] Client requirements vs proposal comparizon.md`
- `[B] CustomerActivityAndExceptionLogs sql scripts creation.md`
- `[C] dom_performance_testing_strategy.html`
- `[C] dom_performance_testing_strategy html.pdf`
- `[D] DOM_QA_Strategy_New_Requested_TestCases creation and json for ADO.md`
- `[E] Anex_1_Performance_Testing_Plan_Peak_Month_Capacity_Simulation.html`
- `[E] Anex_1_Performance_Testing_Plan_Peak_Month_Capacity_Simulation html.pdf`
- `[F] Performance_Testing_Meeting_Minutes.md`
- `[G] DOM Testing Strategy document.pdf`

**`evaluation/`**
- `GAP_AI_Impact_Evaluation_2026_July (done).md`
- `GAP_AI_Impact_Evaluation_2026_July (to be done).md`
- `MASTER_PROMPT_July_Assessment.md`

**`metrics-and-logs/`**
- `AI_Output_Validation_Log.md`

**`prompt-library/`**
- `Prompt_Library_Outreach_Drafts.md`
- `Prompt_Library_Sharing_Record.md`

**`context/`**
- `context.md`

**`certificates/`**
- `Autonomous_Engineer_Intensive_Training_-_Certificate.pdf`
- `AI Impact Assessment July 2026.pdf`

## Do Not Touch
- `.git/`, `.github/`, `April 2026/`, `October 2026/`, `gap-ai-coach-skill/`, `prompts/`
- Note: `Level_3_Roadmap.md`, `SESSION_HANDOFF_CONTEXT.md`, and `AI_Productivity_Metrics.md` have already been moved to `October 2026/` (Level 3 effort), organized into `October 2026/evaluation/`, `October 2026/context/`, and `October 2026/metrics-and-logs/` respectively — they are no longer in `July 2026/`.

## Validation After Move
1. Confirm no files remain loose at the workspace root except folders.
2. Confirm every file listed above exists at its new path.
3. List any `.md` internal links that were updated due to the move.

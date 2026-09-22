# QA Findings Triage

Date: 2026-09-13
QA Agent: Senior QA Agent
Input Sources: Quality report 2026-09-13.txt, web/index.html, src/web_app.py, src/main.py

## Severity Model
- Critical: breaks core flow, data integrity, or security boundary.
- High: major functionality risk or repeatable incorrect behavior.
- Medium: notable usability, resilience, or workflow issue.
- Low: cosmetic or low-impact improvement.

## Findings
| ID | Title | Severity | Area (Backend/Frontend/Workflow) | Repro Steps | Expected | Actual | Evidence | Proposed Direction |
|---|---|---|---|---|---|---|---|---|
| F-001 | Context file selector purpose is unclear | Medium | Frontend/Workflow | Open Start Session section and review context selector guidance | User can understand why different context files exist and when to pick each | Label exists, but selection intent and differences are not explained in UI | web/index.html Start Session block, project-context folder model in backend | Add concise inline help and selection guidance for context profiles |
| F-002 | Role selector purpose is unclear | Medium | Frontend/Workflow | Open Start Session and inspect role dropdown | User understands role changes answer guidance behavior | Role values are visible, but intent is not explicit in UI | web/index.html Role field, src/main.py ROLE_RESPONSE_TEMPLATES | Add role behavior hint near selector and show active role template summary |
| F-003 | Latest session list appears empty after running demo and clicking New Session | High | Frontend | Run demo case, click New Session, inspect Latest session dropdown | Recent sessions remain discoverable and can be reloaded from dropdown | Session state clears locally and dropdown may remain stale without refresh | web/index.html startNewSession function, bootstrap-only session list load | Refresh session list after demo/new session and add explicit reload action |
| F-004 | Advanced options purpose is unclear and may be perceived as mandatory | Medium | Frontend/Workflow | Expand Advanced options in Export ADO TestCase section | User can distinguish required vs optional fields and when to use them | Field purpose is not explicit; optionality is implied but not fully clear | web/index.html Advanced options panel labels | Add short per-field helper text and optional marker guidance |
| F-005 | Agent Trace Viewer not populated during demo workflow | High | Frontend/Workflow | Run demo and navigate to Agent Trace Viewer | Generated report and trace options are available without manual backend refresh | Report dropdown and trace view can remain stale because lists are loaded at bootstrap only | web/index.html loadBootstrap/loadAgentTrace usage, src/web_app.py /api/report-agent-trace | Refresh report list after demo/export and auto-load trace for newest report |
| F-006 | RCA tooltip displays incorrect definition due duplicate key collision | Medium | Frontend/Content | Hover RCA help icon | RCA tooltip defines root cause analysis | Duplicate RCA key overwrites definition with DMAIC text | web/index.html termDefinitions object | Split keys and correct tooltip mapping (RCA and DMAIC as separate terms) |

## Triage Decision Summary
- Total findings: 6
- Critical: 0
- High: 2
- Medium: 4
- Low: 0

## Approval
- QA Lead: Pending
- Engineering Owner: Pending

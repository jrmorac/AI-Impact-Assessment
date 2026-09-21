# Integration Decision Record

Record ID: IDR-20260913-01
Date: 2026-09-13
Decision: Conditionally Approve

## Inputs Considered
- Improvement specification
- Enhancement plan
- Code review findings
- Traceability matrix
- Metrics snapshot
- Risk and rollback register

## Conflicts Between Agents
| Conflict ID | Agents Involved | Topic | Resolution | Decision Owner |
|---|---|---|---|---|
| CF-001 | Senior QA Agent, Senior Frontend Engineer | F-003 interpretation (bug vs expected behavior) | Treated as defect because session list is not refreshed after new artifacts are created, causing recoverability failure from user perspective | Senior Agentic Engineer |
| CF-002 | Senior QA Agent, Senior Frontend Engineer | F-005 interpretation (feature unavailable vs stale data) | Resolved to conditionally approved: demo now returns batch JSON trace path and trace endpoint returns non-empty agent trace for DEMO-WHY3; remaining scope is browser-level UX confirmation | Senior Agentic Engineer |

## Final Decision
- Outcome: Conditionally Approve
- Conditions (if any):
	- Execute manual browser checks for CR-003 and CR-005 and attach screenshots or step logs.
	- Final release owner sign-off required after manual UI evidence review.
- Residual risks:
	- Browser-level selector/rendering behavior has a manual evidence gap.
	- Markdown report path is rejected by trace endpoint (HTTP 400), so report selection must stay constrained to JSON batch outputs.
- Required follow-up actions:
	- Run manual validation scripts defined in 08_Code_Review_Findings.md Manual Evidence Gaps section.
	- Record final owner sign-off decision after manual evidence is attached.
	- Re-run release gate check after manual evidence is attached.

## Validation Evidence Snapshot
- Automated pass: web API health/bootstrap/defects endpoints.
- Automated pass: /api/run-demo (why3) returns session/report/capa/testcases paths and batch_report_path.
- Automated pass: /api/bootstrap reflects newly created demo artifacts (sessions 15->16, output_reports 7->8, both new paths present in lists).
- Automated pass: /api/report-agent-trace using run-demo batch_report_path with defect_id DEMO-WHY3 returns HTTP 200, selected_defect_id DEMO-WHY3, and non-empty agent_trace length 3.
- Automated boundary pass: /api/report-agent-trace using run-demo markdown report_path returns HTTP 400 (non-JSON report rejected).

## Sign-off
- Final owner: Pending full release approval (conditionally approved for implementation validation stage)

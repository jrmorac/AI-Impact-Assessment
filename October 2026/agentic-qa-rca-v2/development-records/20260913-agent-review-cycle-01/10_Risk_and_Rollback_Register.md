# Risk and Rollback Register

Date: 2026-09-13

| Risk ID | Change/Task ID | Risk Description | Impact | Likelihood | Mitigation | Rollback Trigger | Rollback Action | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|
| RK-001 | T-003 | Session list refresh update introduces stale state or duplicate entries | High | Medium | Refresh from backend source of truth and de-duplicate by path | Latest session dropdown fails to load or shows duplicate corrupt values | Revert selector refresh logic and restore previous stable list behavior | Senior Frontend Engineer | Mitigation Implemented - Pending Validation |
| RK-002 | T-005 | Trace viewer refresh update breaks trace loading for existing reports | High | Medium | Keep existing /api/report-agent-trace contract and add fallback message handling | Load Agent Trace returns errors on known valid reports | Revert viewer refresh changes and keep manual trace load path | Senior Frontend Engineer | Mitigation Implemented - Pending Validation |
| RK-003 | T-006 | Tooltip dictionary fix unintentionally breaks help behavior for other terms | Medium | Low | Add regression check for all help buttons and term lookups | Help tooltip does not render for RCA/CAPA/D4/D5 | Revert tooltip map change and re-apply with unique keys | Senior Frontend Engineer | Mitigation Implemented - Pending Validation |
| RK-004 | T-001,T-002,T-004 | Added helper copy introduces visual clutter or misalignment in mobile layout | Medium | Medium | Keep copy concise and verify desktop/mobile rendering | Layout overflow or readability regression detected | Remove nonessential helper lines and keep section-help tooltip guidance only | Senior Frontend Engineer | Mitigation Implemented - Pending Validation |
| RK-005 | T-007 | Backend endpoint adjustments break existing UI bootstrap behavior | Medium | Low | Backward-compatible response shape and targeted endpoint changes only | /api/bootstrap or /api/report-agent-trace response schema mismatch | Revert backend endpoint edits and restore previous response contract | Senior Backend Engineer | Not Required |
| RK-006 | T-008 | Validation evidence is incomplete, blocking release despite code fixes | High | Medium | Use explicit pass/fail matrix and traceability updates before gate review | Missing regression evidence for High findings at gate check | Hold release decision and reopen QA validation tasks | Senior QA Agent | Open |

## Notes
- High/Critical items require explicit rollback trigger and action.
- Keep rollback actions deterministic and testable.

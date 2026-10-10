# QA Findings Triage — v4 Evaluator Remediation

Source: v3 GAP AI Toolkit evaluator review, "Recommended — Address in Upcoming Sprints" section (20 items, 0 Critical/High). Severity classification follows `shared-agent-review-rubric.instructions.md`.

| Finding ID | Evaluator Criterion | Severity | Description | Tier | Disposition |
|---|---|---|---|---|---|
| F-001 | 14.2 | Low | Personal maintainer name ("Jose Mora") embedded in distributed files | 1 | Fixed |
| F-002 | 7.5 | Low | No git tags for releases | 1 | Partially fixed (VERSION/CHANGELOG bumped; git tag creation requires a human action — no terminal/git access in this session) |
| F-003 | 7.8 | Low | No "Intended Audience" section in README | 1 | Fixed |
| F-004 | 7.1 | Low | Production deployment / local-only scope not explicit in README | 1 | Fixed |
| F-005 | 8.10 | Low | CSP set in `web/index.html` but not documented in `README_OPS.md` | 1 | Fixed |
| F-006 | 12.3, 12.4 | Low | Out-of-scope/prohibited-uses and limitations/failure-modes scattered across files, no consolidated README section | 1 | Fixed |
| F-007 | 6.7 | Medium (scout-flagged `critical: true`, evaluator verdict PARTIAL, no Critical/High FAILs overall) | No dedicated `error` lifecycle event in `orchestrator.py`; only `agent_step` outcome='error' | 2 | Fixed |
| F-008 | 1.12 (PARTIAL), 1.13 (FAIL) | Medium | Five Whys / guided-RCA question templates hardcoded in function bodies; no versioning scheme | 2 | Fixed |
| F-009 | 8.4, 8.6, 8.8 | Medium | Escape only closes export modal; generic error messages; incomplete ARIA/screen-reader support | 2 | Fixed |
| F-010 | 2.5, 2.10, 3.7, 3.1, 3.6, 3.12, 6.10, 6.5, 1.10 | Low | Cloud/multi-tenant infrastructure items (Docker, WORM audit storage, real-time monitoring, intent capsules, data residency/model cards, tool_call events, cross-session memory) | 3 | Deferred — out of scope, see risk register |
| F-011 | Pilot finding (not evaluator criterion) | Medium (provisional) | Maria's v4 pilot found CAPA/ADO export UI actions write through convenience endpoints that internally set `approved: true`, bypassing the documented explicit user approval interaction | Post-release pilot | Open — hold broader distribution pending fix and regression tests |

## Owner decision (2026-10-07)

Jose Mora confirmed: (a) defer and document rationale for Tier 3, (b) use "QA Engineering Team" as the maintainer placeholder, (c) scope is Tier 1 + Tier 2 only (F-001 through F-009).

## Post-release pilot finding

On 2026-10-09, Maria Fernanda Avila confirmed browser testing of shareable v4. Her feedback resulted in F-011; it is outside the original evaluator-remediation scope. See the post-approval addendum in `09_Integration_Decision_Record.md` and current risk in `10_Risk_and_Rollback_Register.md`.

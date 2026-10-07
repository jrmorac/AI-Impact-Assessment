# Changelog

## 4.0.0 - 2026-10-07

- Addressed non-critical recommendations from the v3 GAP AI Toolkit evaluator review (Tier 1 + Tier 2).
- Replaced the personal maintainer name with "QA Engineering Team" across distributed documentation.
- Documented the CSP policy in README_OPS.md.
- Added consolidated "Intended Audience", "Production Deployment / Local-Only Scope", "Out-of-Scope and Prohibited Uses", and "Limitations and Failure Modes" sections to README.md.
- Added a dedicated `error` lifecycle event (error_type, error_category, step_name) to the orchestrator for caught exceptions.
- Extracted Five Whys question templates into a versioned prompts directory.
- Added Escape-key handlers for all UI overlays and improved ARIA validation announcements.
- Deferred Tier 3 (cloud/multi-tenant infrastructure) recommendations; see v4 risk register in the full project's development-records.

## 3.0.0 - 2026-09-22

- Added export preview and explicit commit approval with overwrite protection.
- Added atomic export writes and content-hash validation.
- Added deterministic golden regression fixtures and GitHub Actions CI.
- Added agent-step telemetry, timing, correlation fields, and controlled traceback logging.
- Documented the local deterministic, synthetic-data-only operating boundary.

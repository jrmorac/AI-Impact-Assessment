# v2 Evaluator Findings Triage

Date: 2026-09-22  
Source: `October 2026/AI Agent Evaluator feedback report v2.md` and specialist review of the actual v2 source.

## Applicable current blockers

| ID | Finding | Severity | Applicability | Decision |
|---|---|---:|---|---|
| E2-F-001 | No CI/CD regression gate, reproducible dependency artifact, or clean-checkout evidence. | Critical | Applicable now | Implement CI and deterministic test gates; lock dependency installation. CD/containerization remain deployment-dependent. |
| E2-F-002 | Export and overwrite operations are not human-gated. The preview occurs after writing. | Critical | Applicable now | Add preview-only generation, explicit approval, overwrite confirmation, atomic commit, and audit metadata. |
| E2-F-003 | No formal golden regression dataset or canonical expected outputs. | High | Applicable now | Version semantic expectations for demo cases and compare normalized results in CI. |
| E2-F-004 | Local observability lacks agent-step events, duration/session correlation, traceback logging, and retention policy. | High | Applicable now | Extend structured local telemetry and document retention. |
| E2-F-005 | No unified architecture diagram or complete operations/release documentation. | Critical for release evidence | Applicable now | Add Mermaid architecture, README_OPS, ownership, review cadence, versioning, and rollback. |
| E2-F-006 | Evidence closure is incomplete: browser proof, package verification, traceability, and owner sign-off remain open. | Critical for release | Applicable now | Close evidence gates before any release decision. |
| E2-F-007 | CLI and any non-web file operations require the same safety and overwrite policy review. | High | Applicable now | Audit CLI paths, atomic writes, and overwrite behavior; do not assume web validation protects CLI. |

## Conditional future controls

| ID | Finding | Applicability condition | Required decision |
|---|---|---|---|
| E2-C-001 | Token-budget kill-switch and token consumption tracking. | An LLM/model provider or billable inference path is introduced. | Add provider abstraction, per-session/per-feature budget, hard stop, usage events, and budget tests before enabling inference. |
| E2-C-002 | Inference-path content/PII/prompt-injection guardrails. | User or evidence content is sent to an LLM or external model. | Add input/output guardrails, redaction, injection tests, policy decisions, and human review. |
| E2-C-003 | LLM mocking, malformed model-output tests, exfiltration probes, model cards, prompt registry, LLM-as-judge. | LLM-backed phase is approved. | Make provider injectable; deny network in CI; require adversarial and malformed-output suites. |
| E2-C-004 | OpenTelemetry GenAI conventions, cloud monitoring, tenant tags, WORM storage, authentication, intent capsules. | Shared, cloud, regulated, or multi-user deployment is approved. | Create target architecture and security/compliance review before deployment. |

## Not applicable to current implementation

- Per-call token limits, token spend, model IDs, provider routing, model cards, live LLM-call mocking, LLM-as-judge, GenAI spans, and prompt-injection resistance as an LLM control.
- Database migration rollback and vector-store indexing.
- Delete-operation approval: the current web app exposes no delete endpoint. Export overwrite approval remains applicable.

## Architecture conflicts in the evaluator report

- The orchestrator performs one fixed planner/analyzer/validator pass per defect; it has no unbounded loop. Add a defensive step-count assertion for evidence, but do not invent token accounting.
- Current v2 source already contains the export directory allowlist, reachable demo route, trace output, and target-depth fixes. These should be revalidated, not treated as absent without runtime evidence.
- The report's nine-critical tally combines current blockers with future LLM/shared-deployment controls. This plan uses applicability IDs instead of accepting that tally unchanged.

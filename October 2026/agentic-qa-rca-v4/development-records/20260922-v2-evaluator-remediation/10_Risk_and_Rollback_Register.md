# Risk and Rollback Register

| Risk | Trigger | Mitigation | Rollback/containment |
|---|---|---|---|
| Silent export overwrite | Existing report/CSV replaced without explicit approval. | Preview hash, approval token, conflict response, atomic commit. | Disable export commit routes; preserve existing artifacts and preview-only mode. |
| CI false confidence | Tests pass only in current workspace, not clean checkout. | Lock/hashed dependencies, clean runner, network-denied application tests. | Block merge/release until CI is reproducible. |
| Golden fixture drift | Expected outputs changed without reviewed behavior change. | Version fixtures, semantic canonicalization, owner review. | Revert fixture/code pair and reopen finding. |
| Sensitive telemetry | Evidence text or PII enters logs. | Field allowlist, redaction, synthetic fixtures, retention policy. | Disable log sink or revert event fields; retain safe error codes only. |
| Architecture mismatch | LLM/cloud controls are implemented without an approved target. | Applicability gate and future requirements. | Do not deploy; require architecture/security review. |
| Package divergence | Shareable v2 lacks a fix present in working v2. | Same test IDs, manifest comparison, ZIP verification. | Do not distribute ZIP; rebuild after parity. |
| Approval workflow regression | Users cannot export approved artifacts or cancel safely. | API/browser positive and negative tests, feature flag if needed. | Restore preview-only behavior while preserving no-overwrite protection. |

No current Critical or High finding may close without code/config evidence, deterministic tests, owner, and decision record.

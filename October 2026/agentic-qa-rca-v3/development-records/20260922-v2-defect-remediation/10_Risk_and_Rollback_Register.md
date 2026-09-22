# Risk and Rollback Register

| Risk | Trigger | Mitigation | Rollback |
|---|---|---|---|
| Export allowlist expansion | Files are written outside approved synthetic export directory. | Keep centralized root/symlink validation and test outside paths. | Disable CAPA/ADO exports and revert allowlist change; retain local session workflow. |
| Target-depth behavior change | Existing users depend on Why 6-8 continuation. | Decide advanced-mode policy before implementation and document it. | Restore prior max-depth behavior behind explicit advanced configuration; do not permit accidental UI continuation. |
| Revision data corruption | Chain length changes or wrong Why node is replaced. | Use explicit node index, atomic session write, and before/after chain assertions. | Disable revise action and preserve session files for review. |
| Trace stale state | Old trace remains visible after report/defect failure. | Clear trace before load and preserve only valid selections. | Revert auto-load behavior while retaining report selector refresh. |
| Mirrored package drift | Shareable v2 behaves differently from working v2. | Run the same test IDs against both packages before ZIP creation. | Do not distribute ZIP; rebuild after parity is restored. |

No High finding may be closed without code, test evidence, and a recorded integration decision.

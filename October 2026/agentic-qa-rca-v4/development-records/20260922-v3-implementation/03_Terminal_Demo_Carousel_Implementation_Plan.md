# Terminal Demo Carousel Implementation Plan

Plan ID: PLAN-V3-CAROUSEL-20260922-01  
Date: 2026-09-22  
Status: Implemented  
Owner: Jose Mora

## Work items

| Task | Description | Status |
|---|---|---|
| CAR-001 | Expand terminal session detection to include confirmed root cause and target/max-depth terminal states. | Complete |
| CAR-002 | When a terminal session has a Why chain and no selected index, select the final recorded node during render. | Complete |
| CAR-003 | Disable Next for all terminal sessions, including Why 1 and Why 3 demos. | Complete |
| CAR-004 | Preserve live Current Why behavior for active awaiting-answer and needs-more-evidence sessions. | Complete |
| CAR-005 | Mirror the UI fix and contract test in the shareable v3 package. | Complete |

## Validation

- Focused working v3 contract test: passed.
- Focused shareable v3 contract test: passed.
- Working v3 full suite: 25 tests, 24 passed, 1 Windows symlink skip.
- Shareable v3 full suite: 27 tests, 26 passed, 1 Windows symlink skip.
- No failures or errors.

## Browser acceptance

- Why 1 demo opens on Why 1 of 1 (final), with final-node checkbox values.
- Why 3 demo opens on Why 3 of 3 (final), with Next disabled.
- Why 5 demo opens on Why 5 of 5 (final), with Next disabled.
- Active manual sessions continue to show the live Current Why.

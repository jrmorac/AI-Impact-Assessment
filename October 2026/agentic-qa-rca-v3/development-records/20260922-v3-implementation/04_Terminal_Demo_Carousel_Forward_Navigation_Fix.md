# Terminal Demo Carousel Forward Navigation Fix

Date: 2026-09-22  
Finding: After the terminal-demo fix, the Next arrow was disabled for all terminal sessions, preventing forward navigation among already-recorded Why nodes.

## Root cause

The terminal-session flag was used as a blanket disable condition. That correctly prevented advancing beyond the final Why, but incorrectly blocked Why 1 -> Why 2 and Why 2 -> Why 3 navigation in completed demos.

## Fix

Updated both v3 Web UIs so:

- Terminal sessions can move forward while a later recorded Why exists.
- Next is disabled only when the selected node is the last recorded Why.
- Terminal sessions never transition from the final recorded Why to a new live question.
- Existing active-session and advanced-continuation behavior remains unchanged.

## Validation

- Working v3: 25 tests, 24 passed, 1 Windows symlink skip.
- Shareable v3: 27 tests, 26 passed, 1 Windows symlink skip.
- No failures or errors.
- Focused terminal-carousel contract tests passed in both packages.
- Browser confirmation remains recommended for Why 1 -> Why 2 -> Why 3 navigation.

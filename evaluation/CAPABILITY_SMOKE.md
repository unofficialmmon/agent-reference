# New capability evidence

## Automated direct-tool smoke

`capability-smoke.yml` installs selected exact test packages in a disposable GitHub runner, not on a user's machine. `tools/smoke_ast_grep.py` proves structural search, exclusion of string/comment lookalikes, one bounded rewrite and no remaining original match. `tools/smoke_playwright.cjs` connects directly through MCP, lists tools, navigates to a generated localhost fixture, checks an explicit snapshot and closes the browser. No account/profile, external website, model or provider token is involved. Package lock and sanitized summaries are retained as CI artifacts.

These are direct CLI/MCP checks, not OpenCode integration, OMO delegation, security sandboxing, browser E2E for a consumer application, or cross-platform certification. A setup on macOS/Windows still needs its own tests. Template unit tests validate the shipped examples and rejection paths, not arbitrary user configuration or upstream full schemas.

## Target-host acceptance

Record host/OpenCode/OMO versions, relevant tool versions or source pins, project revision, selected server IDs, effective configuration locations and current preset without secret values. Preserve existing user work and run:

| Surface | Required observation |
|---|---|
| Installation | Actual PATH/manager/version; missing prerequisites not hidden |
| OpenCode resolution | Fresh process starts, expected plugins/MCPs load, no duplicate Context7 |
| GitHub | Read one approved repository/PR; write tools absent in read-only mode; token scope not broadened |
| Context7 | Known library/version through the intended agent; source/version checked; failure handled honestly |
| ast-grep | Run the disposable fixture script with installed binary; no application changes |
| Serena pilot | Actual symbol/reference calls, fixed read-only exposure, rejected mutation, no duplicate memory; Java/JS-TS/multimodule results separately recorded |
| Playwright opt-in | Isolated localhost/test profile, expected UI observation, clean close, previous enablement restored |
| OMO | Intended specialist can perform an actual bounded call; other explicit denies remain; check after `/preset` when used |
| Existing stack | Relevant safety/RTK/memory/review/notification smoke from README remains healthy |
| NOOP/rollback | Second setup causes no unnecessary changes; restoring prior keys is tested when feasible |

Configuration presence is not PASS for a call. Transport initialization is not useful behavior. A direct MCP script is not a delegated OpenCode test. If credentials or the target host are unavailable, record the corresponding checks BLOCKED/NOT RUN; do not copy old evidence and change its date.

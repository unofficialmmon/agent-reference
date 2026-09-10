# OpenCode Tooling Setup Prompt

Set up or reconcile the approved OpenCode V1 development-tool stack on the target host. This is explicit environment/configuration work, not application implementation. The historical filename remains valid; it now covers approved MCPs and CLI capabilities as well as plugins.

Read [CONTRACT.md](../templates/setup/CONTRACT.md) and [INSTALLATION.md](../templates/setup/INSTALLATION.md). Resolve `catalog/tooling.json` and `catalog/agent-capabilities.json` from this prompt's source root. The runtime registry and capability registry are policy, not proof of installation or health. If either is missing, inventory read-only and report BLOCKED. Do not promote pilot tools or modify catalog policy during setup.

## Boundaries

Preserve user providers/models/variants, MCPs, agents, prompts, permissions, presets, companion settings, shell preferences and unrelated files. Do not modify application source/tests/schemas/migrations/deployment behavior, upgrade OpenCode to V2, commit or push. Inspect existing settings and review current upstream stable compatibility before installing missing approved tools. Missing tools are normal; missing authorization is not implicit permission.

The shared contract owns inventory, supported installation channels, mutation checkpoint, local recovery copy, surgical merge, status semantics and rollback. Do not duplicate it or silently replace a config file. Honor actual config directory and file overrides, JSON/JSONC precedence and managed settings. Never put credentials in committed config examples or reports.

## Preserve the existing runtime baseline

Reconcile only necessary changes to OMO Slim, cc-safety-net, RTK, Notifier, opencode-mem and Plannotator. Keep AgentsView an external companion, not a runtime hook. Hold/rejected tools remain excluded; opencode-pty remains explicit pilot. Preserve healthy supported versions and installation owners. Do not change unrelated host runtimes to force an optional tool to work.

- OMO Slim: preserve models, variants, MCP/Skill access, presets, prompts, companion and multiplexer choices; validate real delegation after change.
- cc-safety-net: preserve destructive-command protection; test one safe and one destructive command *analysis* without performing destructive actions. It is not a sandbox and may not cover PTY or other execution paths.
- RTK: verify both CLI and actual OpenCode rewrite/integration semantics, not just installation.
- Notifier: preserve deliberate disabled/noisy event choices; startup success is not proof a user observed a notification.
- Plannotator: local/manual plan or document review with feedback returned to the agent; code review when relevant. Do not force review for trivial edits or enable remote sharing/AI review without approval.
- AgentsView: verify session discovery and one usage/statistics read outside OpenCode; do not alter session source data. Stop a daemon started only for validation unless persistence was requested.

## Memory and retirement

opencode-mem owns routine persistent project memory. Preserve a working supported provider/model rather than installing a new one. Default scope is project; UI is loopback; auto-capture and bounded relevant injection are the normal path. Local storage does not imply local-only extraction: the provider may receive work context. Never store secrets.

Do not create `.opencode-mem-project` unless nested repositories intentionally share one memory domain. Do not recreate `.opencode/history/`, Simple Memory `.opencode/memory/`, `remember`/branch-handoff ceremony or synthetic NOOP tracking. Recalled memory never overrides current source/config/contracts/tests.

When retiring Simple Memory/TokenScope, remove only positively identified registrations and tool-specific wrappers/cache. Preserve legacy data until replacement persistence and injection are proven. Do not clear the entire OpenCode cache or delete unrelated plugins.

## Add approved capabilities

GitHub MCP: inventory an existing connection first. Prefer a reviewed remote read-only connection or official local binary/container, limited to needed toolsets. Keep minimum credential scope. A read-only connection cannot execute writes; writing requires separate explicit authority and a reviewed connection/credential change, never a permission bypass.

Context7: OMO may already provide it. Reuse one healthy instance. Only replace it after checking the installed OMO merge/disable contract; never register a second duplicate under another ID. Use for version-sensitive external documentation, not every local edit. Library version, source and returned documentation still need verification.

ast-grep: install only if missing and selected; distinguish `ast-grep` from unrelated `sg`. Use text search for literal text and AST patterns for structure. Preview matches and diffs before a bounded rewrite; tool availability is not permission for bulk mutation.

Serena: explicit pilot only. Pin the selected revision/release, inspect upstream security notes and target language prerequisites, and constrain to navigation. Do not create a second memory system or expose unreviewed shell/edit tools. Verify the actual exposed tools and call rejection, not only a `read_only` setting. It stays pilot until multi-project host evidence supports a separate promotion decision.

Playwright MCP: explicit browser task only. Keep disabled otherwise; when selected use an isolated test profile and target environment with no personal cookies/account bridge. Browser isolation and origin filters are not a security boundary. Close test contexts/processes afterward and restore temporary enablement. Do not permit concurrent agents to drive the same browser state.

## Configuration ownership

Use [the disabled MCP fragments and setup checks](../templates/opencode/README.md), [OMO access composition](../templates/omo/mcp/README.md) and [global reference merge](../templates/setup/GLOBAL_REFERENCE_MERGE.md) as scoped candidates. No example is a complete replacement configuration. Validate one actual direct operation and delegated call using [CAPABILITY_SMOKE.md](../evaluation/CAPABILITY_SMOKE.md).

External MCP server transport, command/URL, authentication reference and enabled state belong to OpenCode `mcp` configuration, not `plugin`. OMO defines which agents can access those MCPs; do not duplicate server endpoints there. CLI binaries need PATH visibility, not invented MCP entries. Models/providers remain unchanged.

Compose actual effective allowlists, preserving wildcards, explicit exclusions and unrelated MCPs/Skills. Do not blindly replace arrays with examples. Verify root vs active-preset behavior for the installed OMO version and test after `/preset` switching when used. Newly installed tools must not silently expand wildcard agents' operational access. Apply explicit permissions at the actual tool boundary; routing alone is not a sandbox.

## Required checks

After preserving active work, restart the affected OpenCode process. Use `evaluation/README.md` for existing runtime smoke requirements. At minimum check clean config/startup, real OMO delegation, retained safety/RTK/notification behavior, absence of retired plugins, Plannotator feedback and AgentsView discovery when those surfaces changed.

Memory PASS requires safe persistence from session A to fully restarted session B, automatic capture during a normal interactive idle lifecycle, relevant injection into a fresh session, and repository authority over stale context. One-shot CLI execution is insufficient proof of idle capture.

For new capabilities separately record: installed/resolved version, server initialize/tools-list, authentication, direct representative operation, delegated access and denied/unwanted operations. A config parse or server handshake alone is not useful-operation or host behavior PASS. Confirm unrelated settings/source are unchanged. Run a second reconciliation and record NOOP only when actually observed.

## Failure isolation and report

For startup failures isolate plain terminal vs background host, a clean project vs the affected project, plugins disabled vs active, and macOS TCC/filesystem access vs true descriptor exhaustion. Do not respond to a generic descriptor error with extreme system-wide `ulimit`/`launchctl` changes.

Restore only affected owned entries after failure; preserve data and stop test-only processes. Final report: Result / Changed / Validation / Needs attention, exact versions and sanitized paths. Distinguish PASS, FAIL, BLOCKED and NOT RUN for installation, routing, direct operations and full host behavior. No completion claim for required failed/unexecuted checks; no trailing optional-cleanup menu.

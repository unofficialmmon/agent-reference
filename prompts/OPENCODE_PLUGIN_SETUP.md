# OpenCode Tooling Setup Prompt

Set up or reconcile the recommended OpenCode development-tool stack for the current user environment. This is an environment/configuration task, not an application implementation task.

Do not modify application source, tests, schemas, migrations, deployment configuration, or project business logic. Preserve existing OpenCode, OMO Slim, provider, model, MCP, permission, agent, Skill, prompt, shell, and companion settings unless a change is strictly required for the tooling work below.

## Goal

Produce a small, role-separated, compatibility-aware stack that can be re-run after OpenCode, OMO Slim, the OS/runtime, or tool versions change.

Do not blindly install versions recorded in documentation or prior smoke evidence. Verify current stable upstream releases and the actual local install method before mutation.

## Current policy

### Active runtime / integrations

- OMO Slim — orchestration and delegated agents. Canonical repository: `alvinunreal/oh-my-opencode-slim`.
- cc-safety-net — destructive-command guard. Canonical repository: `kenryu42/cc-safety-net`.
- RTK — command-output/token optimization integration. Canonical repository: `rtk-ai/rtk`.
- OpenCode Notifier — user notifications. Canonical repository: `mohak34/opencode-notifier`.
- opencode-mem — automatic persistent project memory. Package/repository: `opencode-mem`, `tickernelz/opencode-mem`.
- Plannotator — human plan/document/code review and feedback. Canonical repository: `backnotprop/plannotator`.

### External companion

- AgentsView — standalone local session/history/token/cost analytics. Canonical repository: `kenn-io/agentsview`.

AgentsView is intentionally outside the OpenCode runtime hook stack.

### Retired from the active baseline

- Simple Memory (`@knikolov/opencode-plugin-simple-memory`) — replace with `opencode-mem`.
- TokenScope (`@ramtinj95/opencode-tokenscope`) — replace with AgentsView when standalone analytics is acceptable.

Do not delete legacy Simple Memory data during migration merely because the plugin registration was removed. Retain it until replacement persistence/injection has been proven, then treat cleanup as a separate explicit action.

### Pilot

- `opencode-pty` (`shekohex/opencode-pty`) — useful for interactive/multi-service processes, but install only after the current published release passes compatibility smoke with the active OpenCode/Bun/Node environment.

### Not baseline / hold

Do not install these by default:

- DCP — rejected for the baseline after background context-compression loops proved disruptive to the workflow;
- `opencode-snip` — hold while automatic shell rewriting can materially alter quoted/chained commands or permission semantics;
- `opencode-vibeguard` — hold while masking/secret-boundary concerns remain relevant;
- Morph Fast Apply — optional, not baseline while native editing is adequate;
- `opencode-ignore` — optional, not baseline while native permissions/safety rules cover the need.

A tool can be downgraded whenever current upstream evidence shows a regression. Popularity or a newer version alone is not enough to promote a held tool.

## Mutation boundary

Before changing anything:

1. locate the effective OpenCode config directory, honoring supported overrides such as `OPENCODE_CONFIG_DIR`;
2. inspect the actual OpenCode config file(s), plugin registry/cache state, OMO Slim configuration, RTK integration, installed binaries, commands, and external companions;
3. record current versions and installation channels when discoverable;
4. preserve unrelated user settings exactly;
5. identify retired Simple Memory/TokenScope entries by their actual paths/specs rather than guessing;
6. preserve a recoverable diff/copy before materially rewriting a user-managed config;
7. if an existing dirty/user-managed config requires a broad rewrite rather than a surgical merge, show one concise mutation checkpoint before replacing it.

Do not upgrade/downgrade OpenCode, providers, models, unrelated MCPs, or host runtimes merely to make one optional tool fit. Mark that tool `BLOCKED`/`HOLD` instead.

Do not commit or push any repository as part of this environment setup.

## 1. Inventory the environment

Determine at minimum:

- OS and architecture;
- shell/terminal host when relevant;
- OpenCode version and active plugin contract/runtime;
- Bun/Node versions when relevant;
- effective OpenCode config directory and config format;
- configured plugins and resolved package versions;
- OMO Slim version/configuration;
- cc-safety-net version/status;
- RTK version/integration status;
- Notifier version/configuration;
- opencode-mem version/configuration/state directory;
- Plannotator binary/plugin/commands;
- AgentsView binary/configuration/daemon status;
- relevant OpenCode permission policy.

Never expose credentials, provider keys, tokens, or private config values in the report.

## 2. Re-verify upstreams before install/update

For every tool that may change:

1. open its canonical repository and current official install/configuration documentation;
2. identify the latest stable release/package compatible with the active environment;
3. inspect material current compatibility issues for OpenCode, OMO/background agents, Bun/Node, OS, permissions, and native dependencies;
4. distinguish fixes on `main` from fixes shipped in the selected stable release;
5. preserve the current healthy version when a newer release has an unresolved regression;
6. use the upstream-supported installation/update channel rather than inventing one.

Recorded smoke versions are evidence snapshots, not permanent version locks.

## 3. Remove retired Simple Memory and TokenScope safely

If present, identify the exact installed entries first.

### Simple Memory

- remove only its OpenCode plugin registration and plugin-specific configuration/cache entries;
- do not delete unrelated `.opencode/` content;
- do not recreate `.opencode/history/`;
- retain existing legacy `.opencode/memory/` data during migration unless the user explicitly authorizes cleanup after `opencode-mem` persistence is proven.

### TokenScope

- remove only its plugin registration, command wrapper(s), and plugin-specific cache/state that can be identified safely;
- preserve unrelated commands and OpenCode cache packages.

After removal, restart/smoke later to prove neither retired plugin is loading.

## 4. Preserve/reconcile OMO Slim, cc-safety-net, RTK, and Notifier

Keep these working unless current upstream evidence requires a bounded update.

### OMO Slim

Preserve user-owned models, variants, MCPs, agents, companion settings, prompts, permissions, and project routing. After a version change, validate at least one real Orchestrator-to-specialist delegation rather than treating config parsing as proof.

### cc-safety-net

Use the upstream-supported OpenCode installation/configuration path. Do not weaken protection for convenience. Validate a safe/read-only command and a representative destructive command shape without damaging repository state. Do not describe it as a sandbox; native OpenCode permissions still apply.

### RTK

Preserve the existing OpenCode integration and update through the actual supported channel. Validate both the CLI version and one representative OpenCode command-rewrite/integration path.

### Notifier

Preserve deliberate event enable/disable choices. In OMO/background-agent workflows, avoid enabling noisy lifecycle or subagent-completion events merely because they exist. Validate startup and one safe notification path when practical; command success is not proof that a desktop notification was visually observed.

## 5. Install/reconcile opencode-mem

Use the official plugin entry and current upstream configuration schema.

Default policy:

- default memory scope: `project`;
- auto-capture: enabled;
- relevant-memory injection: enabled with a small bounded result count;
- web UI: loopback/localhost only unless the user intentionally configures authenticated remote access;
- storage: plugin-owned local state, not project-local `.opencode/memory/`;
- capture provider/model: preserve a healthy existing supported OpenCode/provider configuration rather than adding a new provider without need.

Do not hardcode a shared provider/model into every machine. If the current environment already has a validated capture provider (for example an OpenCode-connected Z.AI model), preserve it unless the user asks to change it.

Auto-capture/profile learning can send relevant conversation/work context to the configured AI provider. Local memory storage therefore does not automatically mean local-only extraction. Never put secrets in memory or print provider credentials.

Do not create `.opencode-mem-project` by default. Create/use that marker only when multiple nested repositories are intentionally meant to share one memory identity.

Do not restore the retired manual branch-handoff protocol. Normal use is:

```text
work normally -> session idle -> auto-capture -> later fresh session -> relevant memory injection
```

Use the manual `memory` tool only for immediate add/search/list/correction/migration needs.

### Required opencode-mem smoke

A final PASS requires runtime evidence, not config presence:

1. OpenCode starts and the plugin loads;
2. basic memory operation(s) work when exercised;
3. create/use safe project memory in session A;
4. fully end session A/OpenCode;
5. start a fresh session B for the same project and prove persistence/retrieval;
6. in a normal long-lived interactive session, allow idle auto-capture and prove that an automatic record is created;
7. start another fresh session and prove relevant memory can be injected automatically;
8. confirm current repository evidence still overrides stale memory.

One-shot CLI sessions are not sufficient evidence for auto-capture if the plugin's idle lifecycle never occurs.

## 6. Install/reconcile Plannotator

Use current upstream OpenCode installation guidance. The OpenCode integration currently uses the Plannotator binary plus OpenCode plugin/commands, but re-verify the exact package/config before mutation.

Baseline workflow is manual/local review:

```text
important plan or diff -> Plannotator review -> human feedback/approval -> implementation/continuation
```

Do not force Plannotator UI for every trivial task.

Validate:

- OpenCode integration/commands load;
- a local/manual plan or document review opens;
- approval/feedback returns to the OpenCode agent;
- a local code-review flow works when relevant;
- OMO Slim still delegates normally after integration.

Plans, diffs, annotations, and configuration are local by default according to upstream behavior, but network features can intentionally transmit content. Do not invoke share/workspace/AI-review network features unless the user wants them. If strict no-sharing behavior is desired and the current upstream still supports it, prefer its explicit share-disable setting rather than relying on convention.

## 7. Install/reconcile AgentsView as an external companion

Keep AgentsView outside the OpenCode plugin list.

Use it for:

- OpenCode session discovery/search;
- session/history browsing;
- token usage;
- cost estimates/analytics;
- broader cross-agent usage statistics.

Prefer local/loopback operation. A permanently running daemon is not a baseline requirement: read-only one-off commands may use the local archive directly, while freshness/write commands may start a daemon as required by current upstream behavior.

Smoke-test at least:

- `agentsview session list` or equivalent current session discovery;
- an OpenCode session is visible;
- one usage/statistics command returns data when available;
- any daemon started only for validation is stopped afterward unless the user explicitly wants it persistent.

Do not modify OpenCode session source data merely to make AgentsView discover it.

## 8. Evaluate opencode-pty only as a pilot

Do not promote/install it by default until the current published release loads cleanly in the active OpenCode/runtime/platform.

If explicitly piloted, use bounded local processes and validate spawn, read, input when safe, terminate/cleanup, interruption behavior, and permission handling. Do not assume cc-safety-net protects every command running inside a PTY.

## 9. Integrated restart and smoke

After changes, restart OpenCode and verify the whole stack together:

- OpenCode startup is clean;
- OMO Slim loads and one delegated task completes;
- cc-safety-net is active;
- RTK integration remains active;
- Notifier loads with intended event policy;
- Simple Memory no longer loads;
- TokenScope no longer loads;
- opencode-mem load/persistence/auto-capture/fresh-session injection meet the evidence above;
- Plannotator local/manual approval feedback works;
- AgentsView discovers OpenCode sessions outside the runtime plugin stack;
- no Hold/Rejected tool was installed silently;
- no unrelated global/project configuration changed.

### Startup-failure isolation

Do not respond to a generic low-file-descriptor message by immediately applying extreme system-wide `ulimit`/`launchctl` values.

First isolate the failure:

1. reproduce in a plain terminal outside terminal multiplexers/background-session hosts;
2. compare a clean temporary repository with the affected repository;
3. compare normal OpenCode with external plugins disabled when the host supports that escape hatch;
4. on macOS protected folders, distinguish filesystem/TCC `Operation not permitted` from real descriptor exhaustion;
5. inspect the terminal/background-server process context before changing OS-wide limits.

A terminal host or stale background server can be the fault boundary even when OpenCode surfaces the error.

## 10. Rollback discipline

Before declaring completion, know how to undo every changed component:

- restore the previous OpenCode config entry/options;
- remove only tool-specific cache/package state when necessary;
- preserve unrelated packages and settings;
- stop standalone daemons started for smoke tests;
- restart OpenCode and confirm rollback if a runtime plugin prevents startup.

Do not clear the entire OpenCode cache as a first-line fix.

## Final report

Report only:

### Versions
- OpenCode
- OMO Slim
- cc-safety-net
- RTK
- Notifier
- opencode-mem
- Plannotator
- AgentsView

### Validation
- OpenCode startup
- OMO Slim delegation
- cc-safety-net
- RTK
- Notifier
- Simple Memory removal
- TokenScope removal
- opencode-mem load
- opencode-mem fresh-session persistence
- opencode-mem automatic capture
- opencode-mem fresh-session injection
- Plannotator
- AgentsView OpenCode discovery

Use `PASS`, `PARTIAL`, `FAIL`, `BLOCKED`, or `NOT RUN` honestly.

### Changed
List only configuration/binary/state paths actually changed, without secrets.

### Retained
List intentionally retained migration/legacy data.

### Issues
List only material remaining issues. Do not claim the environment is healthy when a required smoke failed, was blocked, or was not run.

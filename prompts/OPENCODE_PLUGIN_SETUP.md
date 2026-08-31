# OpenCode Plugin Setup Prompt

Set up or reconcile the recommended OpenCode plugin stack for the current user environment. This is an environment/configuration task, not an application implementation task.

Do not modify application source, tests, schemas, migrations, deployment configuration, or project business logic. Preserve the user's existing OpenCode, OMO Slim, provider, model, MCP, permission, agent, Skill, prompt, and companion settings unless a change is strictly required for the plugin work below.

## Goal

Produce a reproducible, compatibility-aware OpenCode plugin setup that can be re-run after the OS, shell, OpenCode version, OMO Slim version, package versions, or plugin APIs change.

Do not blindly install versions recorded in this prompt. Treat the repository/package names below as starting points, then verify current upstream state before mutation.

## Candidate plugins

Current policy starts with these candidates:

### Baseline candidates

- Simple Memory — package `@knikolov/opencode-plugin-simple-memory`; canonical repository currently `ApplauseLab/opencode-plugin-simple-memory`.
- cc-safety-net — canonical repository currently `kenryu42/cc-safety-net`.
- TokenScope — package `@ramtinj95/opencode-tokenscope`; canonical repository currently `ramtinJ95/opencode-tokenscope`.
- OpenCode Notifier — canonical repository currently `mohak34/opencode-notifier`.

### Pilot candidate

- `opencode-pty` — canonical repository currently `shekohex/opencode-pty`. Install only when the current OpenCode plugin API/runtime and published package are compatible with the actual environment.

### Hold candidates

Do not install these by default. Re-evaluate only if the user explicitly asks or current upstream evidence shows that the blocking risks below have been resolved.

- `opencode-snip` — canonical repository currently `VincentHardouin/opencode-snip`; previously held because automatic shell rewriting could break quoted/chained commands and granular shell permissions.
- `opencode-vibeguard` — canonical repository currently `inkdust2021/opencode-vibeguard`; previously held because provider-bound masking did not cover every sharing/structured-output path and configuration could itself expose literal secrets if handled incorrectly.

A candidate's policy may be downgraded when a current regression is found. Do not promote a Hold candidate merely because a newer version exists; verify that the relevant compatibility/safety issue is actually resolved.

## Mutation boundary

Before changing configuration:

1. locate the effective OpenCode config directory, honoring `OPENCODE_CONFIG_DIR` when set;
2. inspect the actual OpenCode config file(s), package cache/install state, and OMO Slim configuration;
3. capture the current plugin list and relevant permission policy;
4. preserve a recoverable copy/diff of any file that will be changed;
5. if an existing dirty or user-managed configuration would be materially rewritten, show the proposed merge and ask one concise confirmation rather than replacing it silently.

Do not upgrade/downgrade OpenCode, OMO Slim, providers, models, or unrelated packages merely to make a candidate plugin fit. Mark incompatible candidates `BLOCKED` or `HOLD` instead.

If the effective configuration already matches a healthy supported setup, report `NOOP`; do not rewrite equivalent JSON/JSONC or clear caches without a reason.

## 1. Inventory the environment

Determine at minimum:

- OS and architecture;
- active shell/terminal environment when relevant;
- OpenCode version and whether the active host uses the V1 or V2 plugin contract;
- Bun/Node versions when relevant to a plugin;
- effective OpenCode config directory and config format;
- configured plugins and their package specs/versions when discoverable;
- OMO Slim package/version and current user/project configs;
- relevant OpenCode permissions, especially shell/external-directory rules;
- whether this is local TUI, server/container/remote, WSL, or another mode that changes plugin behavior.

Do not expose credentials or secret values in the report.

## 2. Re-verify every upstream before installing

For each candidate that may be installed:

1. open the canonical repository and current README/package metadata;
2. identify the latest stable published package/release that actually supports the current OpenCode generation;
3. inspect recent open issues/known limitations for compatibility with the current OpenCode version, OS/runtime, OMO/background agents, permissions, and the plugin's relevant hooks;
4. distinguish fixes present only on `main` from fixes actually shipped in the package being installed;
5. prefer stable releases over beta/prerelease builds unless the user explicitly wants a prerelease or the stable release is unusable and the trade-off is clearly approved;
6. do not assume OpenCode automatically updates an already cached plugin.

Record the verified repository, selected package spec/version, and any material caveat in the final report.

## 3. Install/reconcile cc-safety-net first

Install or preserve cc-safety-net before the other mutating plugins when current compatibility is healthy.

Use the upstream-supported OpenCode installation/configuration path. Start from the normal/recommended protection preset rather than weakening rules for convenience.

Validate with non-destructive diagnostics/explanations when available. Confirm that ordinary read-only Git commands remain usable and that representative destructive command shapes are recognized as blocked without actually destroying repository state.

Do not describe cc-safety-net as a sandbox. Native OpenCode permissions and normal repository safety rules still apply.

## 4. Install/reconcile Simple Memory

Use explicit/manual memory mode. Configure the plugin tuple so the effective behavior is:

```json
[
  [
    "@knikolov/opencode-plugin-simple-memory",
    {
      "autoLoad": false,
      "autoSave": false
    }
  ]
]
```

Merge this into the existing plugin array without deleting unrelated plugins or settings. Do not enable automatic memory injection/saving as part of this prompt.

Smoke-test the tools with non-sensitive temporary content:

1. `memory_remember`;
2. exact `memory_recall`;
3. `memory_update`;
4. recall the updated value;
5. clean up the temporary test memory when safe.

If the global `MEMORY.md` from agent-reference is installed, verify that its manual handoff assumptions match the available tool names/behavior. Never place credentials, tokens, cookies, private keys, authorization headers, or other sensitive values in memory.

Do not create or restore the deprecated `.opencode/history/` workflow.

## 5. Install/reconcile TokenScope

Install the current compatible stable TokenScope package using upstream guidance.

Run its normal diagnostics/report command once. Verify that it reads recorded OpenCode usage rather than rewriting conversation context and that any generated report/cache does not unexpectedly dirty the current project working tree.

Record a baseline result when practical, but do not treat local estimates as provider billing truth when the plugin labels them as estimates.

## 6. Install/reconcile Notifier

Install the current compatible stable Notifier release. Prefer a stable release over repository beta metadata unless explicitly approved.

For OMO Slim/background-agent environments, start conservatively:

- permission: enabled;
- error: enabled;
- question: enabled;
- subagent completion: disabled unless explicitly wanted;
- main completion: disable initially or verify that it does not fire prematurely while delegated/background work is still active;
- noisy/cancel events: keep disabled unless useful.

Run a small notification smoke test appropriate for the OS. Server/container/remote environments may not be able to notify the local desktop; report that limitation rather than claiming success.

## 7. Evaluate PTY as a pilot

Do not install `opencode-pty` until upstream verification confirms compatibility with the active OpenCode plugin generation/runtime and platform.

If installed, begin with exit wake-up behavior disabled/not relied upon when the selected published release still has known notification/model-delivery limitations.

Smoke-test only bounded local processes:

- spawn;
- read output;
- write/input when safe;
- terminate/kill;
- cleanup/no orphan process;
- behavior under interruption/session shutdown when practical;
- permission handling, including external-directory behavior.

Do not assume cc-safety-net protects every action inside a PTY. Keep OpenCode permission boundaries explicit.

If the current OpenCode generation is unsupported (for example a plugin API generation the selected release does not load), leave PTY uninstalled and report `BLOCKED`.

## 8. Hold Snip and VibeGuard unless re-approved

### Snip

Do not install the automatic OpenCode Snip plugin while current upstream still has unresolved command-tokenization/quote/permission regressions relevant to the environment.

A separately installed `snip` CLI may be evaluated independently if the user requests it; that does not authorize automatic rewriting of every OpenCode shell command.

### VibeGuard

Do not install by default while known masking gaps or unsafe literal-secret configuration patterns remain relevant.

If later approved, prefer regex/pattern configuration that does not require committing literal secrets, protect the config file itself from unnecessary agent reads, and never treat VibeGuard as protection for `/share`, all structured MCP output, Simple Memory storage, or local OpenCode database persistence unless current upstream explicitly proves those paths are covered.

## 9. Restart and integrated smoke test

After configuration changes, restart OpenCode before evaluating plugin behavior.

Verify:

- OpenCode starts without plugin-load errors;
- OMO Slim still loads with the same intended model/MCP/agent/Skill policy;
- normal safe shell/Git commands still work under existing permission policy;
- cc-safety-net hooks are active;
- Simple Memory tools work in manual mode;
- TokenScope runs;
- Notifier behaves without unacceptable background-agent noise;
- PTY works only if it was explicitly promoted from Pilot and installed;
- no Hold candidate was installed silently;
- no unrelated global/project configuration was changed.

## 10. Rollback discipline

For every installed/changed plugin, know how to undo the change before declaring completion:

- restore the previous OpenCode config entry/options;
- remove only the plugin-specific cache/package state when necessary;
- preserve unrelated cached packages and configuration;
- restart OpenCode and confirm the rollback when a plugin prevents startup.

Do not clear the entire OpenCode cache as a first-line fix.

## Final report

Report only:

1. environment discovered: OS/runtime/OpenCode/OMO versions and config location, excluding secrets;
2. each candidate as `INSTALLED`, `PRESERVED`, `NOOP`, `PILOT`, `HOLD`, `BLOCKED`, or `FAILED`;
3. canonical upstream and actual package/release selected for each installed plugin;
4. configuration files changed;
5. smoke tests actually run and their result;
6. known limitations that remain relevant;
7. rollback notes;
8. anything not run or not verifiable.

Do not claim the environment is fully healthy when a required smoke test failed, was blocked, or was not run.

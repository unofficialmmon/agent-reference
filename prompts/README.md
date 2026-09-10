# Convenience prompt index

Use the narrowest explicit entry point from a local, reviewed agent-reference source checkout or resolved APM package source. Catalog inclusion is not installation. Project technology Skills remain APM-owned; Spec Kit remains opt-in. These prompts coordinate native tools, not a new runtime or installer.

## First workstation setup, including missing tools

Read `TOOLING_SETUP.md` when workstation setup and its combined report are explicitly wanted:

```text
Read /path/to/agent-reference/prompts/TOOLING_SETUP.md and execute it for this machine.
Preserve my existing models, providers, MCP exclusions, shell configuration and project work.
Keep Serena pilot and Playwright/OpenRewrite disabled unless I explicitly select them.
```

Default scope is preferred agent capabilities plus rg/jq. Optional human UX tools require selection; project configuration requires a named/scoped repository. Actual credentials or administrator grants must be supplied through the supported host flow, never pasted into chat or committed. A GitHub-only execution cannot install the user's computer.

## Narrow setup entries

| Entry | Scope |
|---|---|
| `OPENCODE_PLUGIN_SETUP.md` | Existing compatible filename: OpenCode runtime/plugins, approved MCP capabilities, ast-grep, and minimal OpenCode/OMO configuration reconciliation |
| `DEVELOPER_CLI_SETUP.md` | Selected developer CLI installation and separately approved shell integrations |
| `PROJECT_TOOLING_SETUP.md` | Evidence-backed project CI/security/task/runtime/hook configuration; no application-source migration |

All setup entries use [the common contract](../templates/setup/CONTRACT.md) and [official installation channels](../templates/setup/INSTALLATION.md). Start with an inventory; preserve healthy installations; surgically merge approved keys; keep rollback; validate actual operations. No blind global upgrades, overwrite, automatic pilot promotion or optional-tool bulk installation.

## Project agent guidance and Skills

```text
Read /path/to/agent-reference/prompts/PROJECT_BOOTSTRAP.md and execute it for the current repository.
Do not modify application source or user-global configuration.
```

Bootstrap owns factual project AGENTS, relevant Skill selection and minimal routing. Tooling recommendations do not silently invoke a workstation installer or a security/Bot setup.

`PROJECT_REFRESH.md` reconciles stale guidance/Skill/routing facts; healthy state is NOOP. It does not restore removed Spec Kit or replace native build/runtime conventions.

`APM_SETUP.md` (`apm-setup`) performs first APM adoption and selected-content deployment. `AGENT_SYNC.md` (`agent-sync`) performs routine updates only after healthy adoption. Neither updates user-global tool installations. Canonical prompts and APM command mirrors retain their existing ownership.

`TEST_SETUP.md` (`test-setup`) establishes a real testing portfolio and may modify test infrastructure/tests/test CI, but not production behavior merely to pass checks. Do not substitute lint or security scanning for actual application tests.

## Read-only entries

- `PROJECT_AUDIT.md`: configuration health; do not install or repair during audit.
- `CODEBASE_ONBOARD.md`: current repository map; no files changed.
- `CHANGE_AUDIT.md`: acceptance review of the working-tree change; no files changed.

Use `/speckit.*` only for explicitly selected specification work. Do not chain all setup/audit prompts by default.

## Completion reports

Use the global completion contract: concrete Result, actual Changed paths, meaningful Behavior/Decision only when needed, actual Validation checks, material Needs attention, then stop. Separate installation, configuration, authentication, routing, direct operation and host behavior. Use PASS/FAIL/BLOCKED/NOT RUN honestly; configuration presence is not runtime success. Read-only prompts keep their purpose-built output. Do not end a finished setup with an optional-cleanup selector.

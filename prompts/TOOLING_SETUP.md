# Tooling setup entry point

Execute the approved OpenCode V1 tooling setup on the machine running this session. This is explicit environment/project-configuration work, not application implementation. Missing tools are a normal initial state. A GitHub-only session can update the reference repository but cannot certify or install the user's workstation.

Read [the shared setup contract](../templates/setup/CONTRACT.md) first. Resolve the agent-reference source root from this file, not from an assumed current directory. Read the four tool catalogs listed in [TOOLING.md](../catalog/TOOLING.md). Do not treat catalog membership as authorization to install every entry.

## Scope and sequence

Use the user's explicit selections. With no narrower selection, reconcile the preferred agent capabilities (GitHub read-only, one Context7 provider, ast-grep) and core developer CLI (rg, jq); preserve the existing healthy OpenCode runtime baseline. Optional human UX tools require selection. Serena stays pilot and Playwright/OpenRewrite remain operational opt-ins. Project-only tools require real project evidence and project setup authorization. No V2 or held/excluded tool is adopted.

1. Inventory the target host and report the concrete planned installation/configuration paths before mutation. Reuse the same inventory and checkpoint across the steps below.
2. Diff/merge the global router and conditional references using [GLOBAL_REFERENCE_MERGE.md](../templates/setup/GLOBAL_REFERENCE_MERGE.md); preserve personal rules and copy TOOLS only within this explicitly authorized environment scope.
3. Execute [OPENCODE_PLUGIN_SETUP.md](OPENCODE_PLUGIN_SETUP.md) for approved plugins, MCPs, ast-grep, and OpenCode/OMO configuration. Use [the MCP fragments and composition guide](../templates/opencode/README.md) as candidates, not full-file replacements. The existing filename remains supported.
4. Execute [DEVELOPER_CLI_SETUP.md](DEVELOPER_CLI_SETUP.md) for selected workstation utilities. Do not install a second copy under another manager.
5. Execute [PROJECT_TOOLING_SETUP.md](PROJECT_TOOLING_SETUP.md) only when a specific consumer repository is in scope. Repository bootstrap/refresh alone is not permission for global installs or security/Bot onboarding.
6. Restart the affected OpenCode process after preserving active work; run [direct and delegated capability checks](../evaluation/CAPABILITY_SMOKE.md) on the target host. Do not terminate unrelated sessions.
7. Re-inspect installation and effective configuration. Report NOOP on an equivalent second run; do not rewrite files merely to stamp dates.

Do not stage, commit, push, merge, change branch protection, install a GitHub App, migrate runtime managers, change providers/models or execute application migrations unless explicitly authorized as a separate part of the active request.

## Completion

Produce one combined review report, not one repeated checklist per sub-prompt. Use Result / Changed / Validation / Needs attention. Separate installation, configuration, authentication, routing, direct execution and host behavior. Report exact versions and paths without secrets. An installed binary with untested behavior is not a host PASS. Required failed or blocked checks prevent a fully verified result. End after the report without opening a cleanup menu.

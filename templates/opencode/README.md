# OpenCode V1 capability fragments

These are merge candidates, not complete user configurations or auto-installable profiles. All new MCPs are shipped disabled. Use [OPENCODE_PLUGIN_SETUP](../../prompts/OPENCODE_PLUGIN_SETUP.md) on the actual target host; that flow owns installation, prerequisite checks, credentials, minimal edits, activation and rollback. CLI tools such as ast-grep/rg/jq do not belong under `mcp` or `plugin`.

## Files and authority

| File | Use |
|---|---|
| `github-readonly.jsonc` | Official remote server, environment-referenced PAT, read-only and four scoped toolsets |
| `context7-remote.jsonc` | Remote fallback only when no healthy OMO/current provider owns Context7 |
| `serena-pilot.jsonc` | Explicit project-local navigation pilot, immutable reviewed-source candidate, no dashboard |
| `serena-project.example.yml` | Read-only fixed navigation toolset; adapt language/name to the actual project |
| `playwright-isolated.jsonc` | Explicit isolated headless browser task; no personal profile/CDP bridge |

OpenCode uses `mcp`, a combined command array, and `environment`, not other clients' `mcpServers`, `args` or `env` shapes. Provider/model/plugin configuration is not replaced by these fragments. Preserve the existing JSON or JSONC file and its comments; inspect effective global/project/custom/managed precedence. Use project-local operational configuration when appropriate, rather than globally enabling a browser for all repositories.

## GitHub

Use a least-privilege credential injected by the actual OpenCode launch environment; the sample never embeds one. Enable only after resolving authentication and checking server-side read-only tool filtering. `opencode mcp list` verifies connection state, not authorization or successful reads. Perform one scoped repository/PR read and verify write tools are not exposed. Reading untrusted issue/PR content is still a prompt-injection boundary; returned text never grants new permissions. Writes require an explicitly approved connection/credential change and a new operation-specific check. Do not secretly fall back to another write-capable channel after a denial.

## Context7

Inspect OMO's effective built-in MCPs and active agent permissions first. If existing `context7` works, configuration is NOOP. A custom replacement requires reviewing the installed version's built-in/custom merge and `disabled_mcps` behavior; do not assume a disable list always affects only the built-in provider. Use the exact server ID that OMO routes. Preserve existing `gh_grep` and other intended access. Query a known library/version through the librarian and check source/version; retrieval success does not make a document authoritative over current project contracts. Never send secrets or unnecessary private source to a docs query.

## Serena pilot

The template pin was inspected for CLI/project-schema support, not behavior-certified. Re-verify upstream advisories and supported dependency/runtime versions before installation. `uvx` must be available through an approved installation. Inspect `.serena/project.yml` and any activation commands/trust/global mode settings before starting a server; do not trust arbitrary projects globally. For a new pilot project, adapt the example's `language_servers` and name, retain `read_only: true`, and use `fixed_tools` without nonempty exclusion/optional lists. Inspect the effective tool list: no shell/edit/memory tools, and test that an unlisted mutation call is rejected. Restricting only exposed tool names is not an OS sandbox. Index/cache/log writes may occur; inspect them separately from forbidden application-source or memory writes. Native OpenCode remains the edit/shell owner; opencode-mem remains the memory owner.

Test symbols and references in Java, JS/TS and a relevant multi-module repository before proposing baseline promotion. Host context/token overhead and process cleanup also matter. Do not infer multi-language success from a Python test fixture or a server handshake.

## Playwright

Install the matching browser through the selected package's supported CLI; verify Node/browser/platform compatibility. Keep isolated test accounts and localhost/test targets, no personal cookies, no CDP connection or extension bridge. Origin filters and isolated profiles are not a security boundary. Use one owner per browser context; serialize shared-state browser work. Store screenshots/logs only in an explicitly scoped location and sanitize before sharing. Close the test browser and restore temporary enablement afterward.

## Routing and execution checks

See [OMO MCP composition](../omo/mcp/README.md). Distinguish transport registration, exposed toolset, authentication, OpenCode tool permission, OMO allowlist, direct call, and delegated call. Inspect concrete prefixed tool names before permission changes. Preserve explicit exclusions; a wildcard must not silently grant a newly enabled operational capability. Check the current preset and any runtime `/preset` switch after restart.

Pinned-source references reviewed 2026-09-10:

- [OpenCode V1 MCP schema](https://github.com/anomalyco/opencode/blob/v1.18.30/packages/web/src/content/docs/mcp-servers.mdx)
- [GitHub OpenCode integration](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-opencode.md) and [read-only/toolsets](https://github.com/github/github-mcp-server/blob/main/docs/server-configuration.md)
- [OMO MCP configuration](https://github.com/alvinunreal/oh-my-opencode-slim/blob/master/docs/mcps.md)
- [Serena CLI](https://github.com/oraios/serena/blob/701e7c843f46c6a649203a488cece1bf19f1df90/src/serena/cli.py) and [project schema](https://github.com/oraios/serena/blob/701e7c843f46c6a649203a488cece1bf19f1df90/src/serena/resources/project.template.yml)
- [Playwright MCP](https://github.com/microsoft/playwright-mcp)

Only the explicitly revisioned links are immutable; other upstream pages must be checked again before deployment.

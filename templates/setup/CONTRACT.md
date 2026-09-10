# Shared setup contract

This contract coordinates native installation/configuration tools; it is not an installer or a manifest execution engine. It applies only when an explicit setup task is being executed on the target machine.

## Inventory before installation

Record OS/architecture, actual shell/terminal host, current project/worktree and dirty state, OpenCode V1/OMO versions, PATH-visible binaries and package ownership, Node/Bun/Python/Java prerequisites, active global/project config paths and environment overrides. Inspect `OPENCODE_CONFIG`, `OPENCODE_CONFIG_DIR`, inline/managed configuration and `.json`/`.jsonc` precedence without printing values that contain secrets. Do not assume macOS just because an earlier host was macOS.

Use `command -v` (or the supported PowerShell equivalent), native package-manager inventory, and bounded `--version` checks. A binary missing from PATH does not prove it is uninstalled; inspect known manager/shim locations. Identify Mike Farah's yq, `ast-grep` rather than an unrelated `sg`, and distribution names such as `fdfind`/`batcat`. Check the PATH of the actual OpenCode process, not just an interactive shell.

Record per selected tool: policy, current installation/channel/version, prerequisites, config owner/path, authentication state (present/absent only), requested change, direct test and rollback. Do not export full config, environment, shell history, tokens or browser state into an inventory file.

## Install and reconcile

Consult the official documentation URL in the catalog. Check current stable release, security advisories, OS/runtime support and the actual supported install command. Preserve healthy supported versions rather than upgrading everything. Review pinned release notes/diffs before changing executable dependencies. Pin chosen local MCP packages and CI integrations; do not leave `@latest` or a floating image in a deployed configuration. Remote services cannot be revision-pinned; record that boundary separately.

Use the existing trusted manager where compatible. On macOS, use upstream-supported Homebrew formulae when Homebrew already exists. On Linux/Windows use the upstream-supported distro/package/binary route. Do not install Homebrew, Docker, Node, Python or a new runtime manager merely to satisfy one optional tool without explicit approval. Verify release checksums/signatures when provided. Do not pipe an unreviewed remote script into a shell.

The normal path installs missing selected tools, preserves healthy ones and repairs a narrow proven drift. Do not run blanket `brew upgrade`, global package updates, install-all commands or destructive cache cleanup. Remote MCPs do not need a local server binary. CodeQL/GitHub Apps are not workstation binaries. OpenRewrite belongs to its project's build integration, not a global MCP.

## Configuration transaction

Before the first write, show the selected tools, exact config paths, intended keys and package operations. Proceed for clean additive changes already authorized by setup. Ask one checkpoint only for dirty/unknown ownership, overwrite/deletion, new privilege, new external transmission boundary or expanded scope. Keep a recoverable local copy/diff with restrictive permissions (credentials may already exist in the source); never commit or upload that copy.

Merge only owned keys into the existing file. Preserve comments, order where practical, unrelated values, providers/models, custom agents, intentional deny rules and package ownership. Never parse JSONC through jq/yq and replace the entire file. Never append to an MCP/Skill allowlist as if it were necessarily an additive merge; preserve semantics of wildcards and exclusions. If a safe small edit cannot be proven, stop with BLOCKED instead of guessing.

Validate format/schema and the effective runtime configuration before claiming CONFIGURED. Missing authentication remains BLOCKED for authenticated calls; do not paste tokens into chat or source. Keep unsafe or unfinished MCP registrations disabled. A read-only token/server cannot become writable merely because the agent asks to write; use an explicitly approved connection/credential change. Do not silently broaden a credential or switch to another channel to evade a denial.

## Verification and rollback

Check installation/version, clean configuration resolution, explicit server connection, direct representative operation and (for OMO) a real delegated operation. Verify absence of unintended writes. Restart only affected processes with user work preserved. Test a second reconciliation for NOOP on the host; reading a template is not proof of idempotence.

On failure restore only the changed entries/files, restart affected services if appropriate, and preserve evidence of the failure. Remove a newly installed package only when its installation ownership and lack of other consumers are established and cleanup is authorized. Do not uninstall a shared runtime. Stop local processes started solely for tests.

Keep status dimensions separate:

- installation: MISSING / PRESENT / INSTALLED / RETAINED / BLOCKED;
- configuration: NOOP / CONFIGURED / BLOCKED;
- checks: PASS / FAIL / BLOCKED / NOT RUN / NOT APPLICABLE (with reason).

Overall completion may be COMPLETED, COMPLETED_WITH_ISSUES or BLOCKED, but never describe required unexecuted host checks as PASS. No synthetic memory, tracking files or version updates on a true NOOP.

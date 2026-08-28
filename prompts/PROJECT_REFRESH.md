# Project Refresh Prompt

Use this prompt when an established repository has changed enough that its agent-facing configuration may be stale.

Update configuration/reference files only. Do not modify application source, tests, schemas, migrations, generated output, build dependencies, or deployment configuration.

## Reference source

When this prompt is read from an `agent-reference/prompts/` directory, treat the parent `agent-reference/` directory as the reference source root. Resolve catalog and Skill paths from that root. If it cannot be located, do not guess or recreate Skill content; mark catalog reconciliation `NOT RUN`.

## Goal

Reconcile these areas with the repository as it exists now:

- project-root `AGENTS.md`;
- selected project-local Skills under `.opencode/skills/`;
- project-local OMO Slim Skill routing when present or intentionally managed;
- Spec Kit integration health and durable constitution guidance when Spec Kit is in use;
- ignore rules only where real credentials, caches, or machine-local artifacts require them.

Do not introduce a framework, workflow engine, agent-role system, or new project architecture.

If current guidance, Skill selection, OMO routing, and Spec Kit state already match the repository, report `NOOP`; do not rewrite files for stylistic equivalence.

## Safety

1. Start with `git status --short` and preserve existing user changes.
2. Treat sibling repositories as read-only unless explicitly authorized.
3. Treat CodeGraph/search indexes as navigation aids; verify important claims against current files.
4. Before deleting/replacing a user-modified Skill, materially rewriting an existing constitution, using `--force`, or overwriting an overlapping dirty file, show the proposed change and ask one concise confirmation.
5. Do not commit, push, reset, clean, deploy, or run destructive commands.

## Procedure

### 1. Recheck project facts

Read the current `AGENTS.md`, then inspect only enough maintained source, tests, build/package configuration, formatter/linter configuration, generated-source configuration, architecture/contracts, and current docs to verify its claims.

Correct only evidence-backed drift:

- stale paths or commands;
- removed/added technology actually used by the project;
- changed module/domain ownership;
- changed API/DB/auth/security/generated boundaries;
- obsolete project-specific rules;
- durable new project facts.

Do not copy generic engineering or framework guidance into the project file.

### 2. Reconcile selected Skills

When the agent-reference catalog is accessible:

- keep only Skills relevant to the current stack and boundaries;
- detect duplicate IDs across visible project/global discovery roots;
- never edit an upstream snapshot in place;
- when replacing a reviewed snapshot, replace the complete Skill directory and preserve all references, scripts, assets, and license files rather than copying only `SKILL.md`;
- do not install or retain an operational Skill without a current explicit need;
- do not remove or replace a user-modified Skill without confirmation.

If the catalog is inaccessible, mark Skill reconciliation `NOT RUN` instead of inventing IDs or content.

### 3. Reconcile project-local OMO Slim Skill routing

If OMO Slim is installed/configured or `.opencode/oh-my-opencode-slim.json[c]` exists:

- treat the project-local OMO config as auto-loaded trusted configuration that can alter agent behavior, tool access, and Skill access;
- inspect `templates/omo/README.md` and `ROUTING.md` when the reference source is available;
- treat stack templates as candidate examples, never as blind replacements;
- compare routed Skill IDs with current repository facts and actually discoverable Skills;
- preserve user-level/global OMO configuration and project-local model, variant, MCP, companion, multiplexer, permission, prompt, and custom-agent choices;
- treat each agent `skills` array as an effective allowlist: compare against the effective current policy and do not accidentally drop intentional non-operational entries while reconciling stack Skills;
- keep Orchestrator/Explorer/Librarian/Oracle unchanged unless a concrete project-specific need justifies a routing change;
- remove stale specialist Skill IDs only when the evidence is clear and no user modification conflict exists;
- never add or retain an operational Skill merely because it appears in a template or catalog;
- do not duplicate OMO Slim bundled Skills into the repository merely for routing;
- if both `.json` and `.jsonc` exist, account for JSONC precedence and do not create another competing file;
- prefer root `agents.<agent>.skills` for ordinary project stack routing during normal startup; preserve an existing intentional preset-specific design, and when runtime `/preset` switching is used verify effective routing after the switch rather than assuming startup precedence applies.

After a routing change, determine the OMO Slim package spec already configured by OpenCode and, when an existing supported runner can invoke that same package/version safely, run its `doctor --json` from the project root. Do not hard-code `@latest` for validation or upgrade the plugin as a side effect. Otherwise report diagnostics `NOT RUN`. Behavioral changes require an OpenCode restart before smoke testing.

### 4. Check Spec Kit with native commands

If `.specify/` exists, use Spec Kit's own manifest-aware diagnostics.

```bash
specify version
specify integration status --json
```

If `--json` is unsupported, use plain `specify integration status` and report the limitation. Do not silently upgrade the CLI.

- Do not rerun `specify init --here --force` as a normal refresh path.
- If OpenCode is missing, use `specify integration install opencode --script sh` on macOS/Linux or `--script ps` on Windows.
- If multi-install safety would require `--force`, ask before proceeding.
- If OpenCode is installed but not default, ask before `specify integration use opencode`.
- If managed files are missing or stale, use `specify integration upgrade opencode` with the platform-appropriate script type.
- If modified managed files are reported, do not force-overwrite them; preserve and report the conflict.
- Do not update the global CLI, extensions, or presets unless explicitly requested.

Inspect the constitution for conflict with durable project facts. Preserve a non-template constitution; show a proposed governance diff and ask before a material change.

### 5. Review repository hygiene

Inspect `.opencode/` before changing `.gitignore`. Never ignore the whole directory blindly. Keep non-secret commands and Skills trackable; ignore only concrete private or machine-local paths.

### 6. Validate the refresh

Review the final configuration diff. Run configuration-focused checks such as:

```bash
git diff --check
git status --short
```

Run `specify integration status --json` again after Spec Kit changes. Do not run the full application test suite solely for documentation/configuration refresh unless a project rule requires it.

## Final report

Report only:

1. stale configuration found;
2. files changed;
3. project facts added, removed, or corrected;
4. Skill selection changes and conflicts;
5. project-local OMO Slim routing changes and diagnostics;
6. Spec Kit status and native changes;
7. unresolved items or confirmations not granted;
8. checks actually performed, with `PASS`, `FAIL`, `NOT RUN`, or `BLOCKED` stated honestly.

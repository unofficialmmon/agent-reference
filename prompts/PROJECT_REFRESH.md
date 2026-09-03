# Project Refresh Prompt

Use this prompt when an established repository has changed enough that its agent-facing configuration may be stale.

Update configuration/reference files only. Do not modify application source, tests, schemas, migrations, generated output, build dependencies, or deployment configuration.

**Spec Kit is optional.** Its absence is healthy. Do not install, initialize, repair, upgrade, or restore Spec Kit unless the user explicitly asks for Spec Kit maintenance in this refresh.

## Reference source

When this prompt is read from an `agent-reference/prompts/` directory, treat the parent `agent-reference/` directory as the reference source root. Resolve catalog and Skill paths from that root. If it cannot be located, do not guess or recreate Skill content; mark catalog reconciliation `NOT RUN`.

## Goal

Reconcile only the agent-facing configuration the repository actually uses:

- project-root `AGENTS.md`;
- selected Skills and their current ownership/deployment model;
- project-local OMO Slim Skill routing when present or intentionally managed;
- optional Spec Kit state only when explicitly requested;
- ignore rules only where real credentials, caches, or machine-local artifacts require them.

Do not introduce a framework, workflow engine, agent-role system, new project architecture, or optional tool merely because agent-reference supports it.

If current guidance, Skill selection, and OMO routing already match the repository, report `NOOP`; do not rewrite files for stylistic equivalence.

## Safety

1. Start with `git status --short` and preserve existing user changes.
2. Treat sibling repositories as read-only unless explicitly authorized.
3. Treat CodeGraph/search indexes as navigation aids; verify important claims against current files.
4. Before deleting/replacing a user-modified Skill, materially changing an optional Spec Kit constitution, using `--force`, or overwriting an overlapping dirty file, show the proposed change and ask one concise confirmation.
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

### 2. Reconcile selected Skills and ownership

When the agent-reference catalog is accessible:

- keep only Skills relevant to the current stack and boundaries;
- detect same-ID content across visible discovery roots and distinguish identical shadowing from divergent ownership conflicts;
- never edit an upstream snapshot in place;
- do not install or retain an operational Skill without a current explicit need;
- do not remove or replace a user-modified Skill without confirmation.

Respect the existing deployment owner:

- For a coherent APM-managed project, do not hand-edit `.agents/skills/` or generated lock/output. Use `/agent-sync` for routine agent-reference updates and `/apm-setup` for first adoption or damaged/incomplete ownership.
- For manual project-local Skills, preserve complete directories and source provenance. Do not silently migrate them to APM merely because APM is available.
- If the catalog is inaccessible, mark Skill reconciliation `NOT RUN` instead of inventing IDs or content.

### 3. Reconcile project-local OMO Slim Skill routing

If OMO Slim is installed/configured or `.opencode/oh-my-opencode-slim.json[c]` exists:

- treat project-local OMO config as auto-loaded trusted configuration that can alter agent behavior, tool access, and Skill access;
- inspect `templates/omo/README.md` and `ROUTING.md` when the reference source is available;
- treat stack templates as candidate examples, never as blind replacements;
- compare routed Skill IDs with current repository facts and actually discoverable Skills;
- preserve user/global OMO configuration and project-local model, variant, MCP, companion, multiplexer, permission, prompt, and custom-agent choices;
- treat each agent `skills` array as an effective allowlist and preserve intentional non-operational entries;
- keep Orchestrator/Explorer/Librarian/Oracle unchanged unless a concrete project-specific need justifies a routing change;
- remove stale specialist Skill IDs only when evidence is clear and no ownership conflict exists;
- never add or retain an operational Skill merely because it appears in a template or catalog;
- account for JSONC precedence if both project config formats exist;
- prefer root `agents.<agent>.skills` for ordinary project routing unless the repository deliberately uses preset-specific routing.

After a routing change, determine the OMO Slim package spec already configured by OpenCode and, when an existing supported runner can invoke that same package/version safely, run its `doctor --json` from the project root. Do not hard-code `@latest` or upgrade the plugin as a side effect. Otherwise report diagnostics `NOT RUN`. Behavioral changes require an OpenCode restart before smoke testing.

### 4. Preserve or explicitly maintain optional Spec Kit

If Spec Kit maintenance was **not** explicitly requested:

- do not run `specify` commands;
- do not create, restore, repair, or delete `.specify/`;
- do not recreate `speckit.*` commands after a user has uninstalled the integration;
- do not modify a constitution;
- if `.specify/` or Spec Kit command remnants exist, report them as existing optional state, not as a refresh failure.

If the user explicitly requested Spec Kit maintenance, use Spec Kit's own manifest-aware commands as authority:

```bash
specify version
specify integration status --json
```

Use plain `specify integration status` if JSON output is unsupported. Do not silently upgrade the CLI. Use native install/upgrade/use operations only for the requested integration repair, never `init --here --force` as a routine refresh path, and never force-overwrite modified managed files.

Preserve an existing non-template constitution unless the user explicitly authorizes a material governance change.

### 5. Review repository hygiene

Inspect `.opencode/`, `.agents/`, and existing ignore rules before changing `.gitignore`. Never ignore whole agent configuration directories blindly. Keep non-secret commands, Skills, manifests, locks, and project configuration trackable when the repository intends to version them; ignore only concrete private or machine-local paths.

### 6. Validate the refresh

Review the final configuration diff. Run configuration-focused checks such as:

```bash
git diff --check
git status --short
```

Also verify that:

- APM-generated output was not hand-edited;
- every OMO-routed Skill is actually discoverable;
- no operational Skill was introduced without explicit authorization;
- Spec Kit files were untouched when Spec Kit maintenance was not requested;
- no application source or unrelated configuration changed.

Run Spec Kit status again only when Spec Kit maintenance was explicitly requested. Do not run the full application test suite solely for configuration refresh unless a project rule requires it.

## Final report

Report only:

1. stale configuration found;
2. files changed;
3. project facts added, removed, or corrected;
4. Skill selection/ownership changes and conflicts;
5. project-local OMO Slim routing changes and diagnostics;
6. Spec Kit as `NOT REQUESTED`, preserved-existing, or explicitly maintained state;
7. unresolved items or confirmations not granted;
8. checks actually performed, with `PASS`, `FAIL`, `NOT RUN`, or `BLOCKED` stated honestly.

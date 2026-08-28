# Project Bootstrap Prompt

Prepare the current repository's agent-facing configuration for OpenCode, selected agent-reference content, project-local OMO Slim Skill routing, and GitHub Spec Kit when it is available or requested.

This is a project-onboarding task, not a feature implementation task. Do not modify application source, business logic, tests, schemas, migrations, generated output, or deployment configuration except for tooling files explicitly covered below.

## Reference source

When this prompt is read from an `agent-reference/prompts/` directory, treat the parent `agent-reference/` directory as the reference source root. Resolve catalog and Skill paths from that root. If the source root cannot be located, do not guess paths or recreate Skill content; continue only with repository-local work and report Skill selection as `NOT RUN`.

## Intended result

Leave the repository with:

- a concise, factual project-root `AGENTS.md`;
- a healthy Spec Kit OpenCode integration when the CLI is available;
- a minimal constitution based on durable repository facts;
- only relevant project-local Skills selected;
- a minimal project-local OMO Slim Skill-routing override when OMO Slim is installed;
- no operational Skill enabled without explicit authorization;
- an honest report of changes, failures, blocked work, and unverified scope.

Do not create a new workflow engine, agent framework, installer, or project architecture. Do not modify OMO Slim global configuration, models, variants, MCPs, companion settings, prompt overrides, custom agents, or unrelated permissions during bootstrap. A project-local OMO Slim config may be created or updated only for minimal Skill routing covered by this prompt.

Treat project-local OMO Slim configuration as a trust boundary because OMO loads it automatically and it can alter agent behavior, tool access, and Skill access. Before creating or changing it, inspect the current file and repository trust context; never copy an unreviewed OMO config from another project.

If the repository is already correctly configured, finish with `NOOP` rather than rewriting equivalent content for style or wording alone. Bootstrap quality is measured by accurate minimal setup, not by the number of files changed.

## Safety and authority

Use this order:

1. explicit user instruction;
2. existing project `AGENTS.md` and authoritative contracts;
3. maintained source, tests, schemas, build/configuration, README, and architecture docs;
4. installed Spec Kit artifacts;
5. agent-reference templates and selected Skills;
6. global OpenCode references.

Preserve the current working tree.

- Start with `git status --short`.
- Do not run `git add`, `commit`, `stash`, `reset`, `clean`, `checkout --`, deploy, or destructive equivalents unless explicitly requested.
- Treat sibling repositories as read-only unless explicit authority grants writes.
- Do not ignore `.opencode/` wholesale. Inspect it first; committed commands and Skills may live there.
- Treat CodeGraph, search indexes, caches, and symbol databases as navigation aids. Confirm important claims against current files.

## Mutation checkpoint

Before the first write, prepare a concise change plan listing the files/directories to create or update.

Ask one concise confirmation before proceeding when any of these are true:

- the working tree is dirty and a planned target overlaps an existing change;
- `AGENTS.md`, `.specify/`, `.opencode/`, a project-local OMO Slim config, or relevant `.gitignore` entries already exist and may be materially rewritten;
- a command would require `--force` or overwrite a modified/unknown managed file;
- an existing Skill with the same ID would be replaced;
- an existing non-template constitution would be materially changed.

A request to run this bootstrap authorizes normal onboarding, but it does not authorize silent overwrite of overlapping user work. If targets are new and no conflict exists, proceed without an unnecessary question.

## 1. Inspect the repository

Inspect only enough current material to establish:

- repository purpose, stack, runtime, frameworks, and build/package manager;
- main modules, source roots, and ownership boundaries;
- maintained architecture/domain conventions;
- API/public contracts;
- DB/schema/migration authority;
- generated source and its contract/configuration/generator;
- auth/security boundaries;
- sibling/shared repository read/write scope;
- formatter/linter configuration;
- real build/test/validation commands;
- current `AGENTS.md`, `.opencode/`, `.specify/`, and installed Skill IDs.

Do not treat deleted, archived, generated, example, or stale-index-only material as current architecture authority.

## 2. Reconcile Spec Kit

First run:

```bash
specify version
```

If the CLI is unavailable, do not install a global tool silently. Mark this step `BLOCKED`, provide the official command below, and continue independent `AGENTS.md` and Skill work when safe.

```bash
uv tool install specify-cli
```

Do not upgrade the Specify CLI, extensions, or presets unless the user explicitly asks for a tool/version update.

### New Spec Kit project

When `.specify/` does not exist:

1. inspect for partial/conflicting remnants such as existing `speckit.*` commands, an integration manifest, or unowned files at expected managed paths;
2. satisfy the mutation checkpoint;
3. initialize with the platform-appropriate script type.

macOS/Linux:

```bash
specify init --here --force --integration opencode --script sh
```

Windows:

```powershell
specify init --here --force --integration opencode --script ps
```

`--force` only skips the non-empty-directory prompt after the user has approved the planned merge. It does not authorize unrelated overwrite. Inspect the resulting diff immediately.

### Existing Spec Kit project

Do not rerun `specify init --here --force` as the normal refresh path.

Prefer the machine-readable read-only status command:

```bash
specify integration status --json
```

If the installed CLI does not support `--json`, use:

```bash
specify integration status
```

and record the compatibility limitation. Do not silently upgrade the CLI.

Then:

- if the OpenCode integration is missing, use `specify integration install opencode --script sh` on macOS/Linux or `--script ps` on Windows;
- if another installed integration makes multi-install unsafe, do not add `--force` silently; ask for explicit approval or report the conflict;
- if OpenCode is installed but is not the default integration, ask before `specify integration use opencode`, because changing the default refreshes shared templates and active extension/preset artifacts;
- if OpenCode managed files are missing or stale, use `specify integration upgrade opencode` with the platform-appropriate `--script`;
- if status reports locally modified managed files, do not use `--force`; preserve them and report the conflict.

After any Spec Kit mutation, run status again and inspect:

```bash
git status --short
git diff --stat
```

Review changes under `.specify/`, `.opencode/`, `.gitignore`, and `AGENTS.md`. Do not accept an unexpected overwrite silently.

## 3. Create or refine project `AGENTS.md`

Use `agent-reference/project/AGENTS.template.md` as a structural reference when available. Follow the same quality bar as OpenCode's native `/init`: concise project-specific guidance, real commands and boundaries, and at most one targeted question when repository evidence cannot resolve a material fact. Do not copy placeholders or generic text blindly.

Keep only durable project-specific facts, normally:

- project purpose, stack, modules, and key docs;
- authority and ownership boundaries;
- architecture/dependency direction that current source actually demonstrates;
- API/DB/IPC/auth/security contracts;
- generated-source ownership and regeneration command;
- sibling/shared repository scope;
- actual formatter/linter/build/test commands;
- project-specific hazards and prohibitions;
- short Skill and Spec Kit routing notes when relevant.

Do not copy global `ENGINEERING.md`, whole Skill bodies, generic framework advice, OMO agent roles, speculative architecture, or mandatory Spec Kit usage for routine fixes.

Preserve valid existing project rules. When `AGENTS.md` conflicts with maintained contracts/source, treat it as possible drift and resolve the evidence rather than hiding the mismatch.

## 4. Select project Skills

When the agent-reference catalog is accessible, inspect `catalog/skills.lock.json` and the relevant Skill directories.

**Catalog inclusion is not activation.**

- Select only Skills directly relevant to the project's real stack or contract boundaries.
- Prefer project-local installation under `.opencode/skills/` during bootstrap.
- Check all visible project/global discovery roots for duplicate IDs before copying.
- Do not overwrite an existing Skill silently.
- Never edit an upstream snapshot in place.
- Copy a selected Skill as its complete directory, preserving `SKILL.md`, references, scripts, assets, and license files byte-for-byte. Do not reconstruct a Skill from excerpts or copy only its entrypoint.
- Use `api-contract` only when HTTP/API contract work exists.
- Use `generated-code` only when generated/tool-owned source exists.
- Use `java-style` only when its Java/Spring guidance does not conflict with repository formatters or conventions.
- Workflow Skills such as `bug-reproduction-brief`, `refactor-plan`, and `verification-before-completion` are explicit-use tools, not ambient defaults.
- Never install `skills/operational/*` without explicit authorization for the specific Skill.

If the catalog is inaccessible, do not invent Skill names or recreate content. Mark Skill reconciliation `NOT RUN` and report the useful technology categories only.

## 5. Configure project-local OMO Slim Skill routing

Do this only when OMO Slim is installed/configured or its project-local config already exists. Use the installed `oh-my-opencode-slim` Skill and current OMO Slim schema/documentation as configuration authority when available.

When `agent-reference/templates/omo/` is accessible, read `README.md` and `ROUTING.md`, then use the closest stack template as a **candidate example only**. Adapt it to repository evidence and the actually installed Skill IDs. Never copy a stack example blindly.

### Preserve the global setup

- Discover the effective user config directory, honoring `OPENCODE_CONFIG_DIR` when set; otherwise use the platform/default OpenCode config directory.
- Read the existing user OMO Slim config only as needed to understand existing agent policy. Never write it during project bootstrap.
- Project-local configuration belongs in `.opencode/oh-my-opencode-slim.json` or `.jsonc`. If one already exists, merge into that file. Do not create both formats merely because a template uses JSONC; JSONC takes precedence when both exist.
- Preserve existing model, variant, MCP, companion, multiplexer, permission, custom-agent, and prompt settings. Do not duplicate the entire user config into the repository.
- Treat each agent `skills` array as an effective allowlist rather than an additive list. Before writing an override, inspect the effective current agent policy and retain intentional non-operational entries that the user expects to keep.
- Prefer root `agents.<agent>.skills` for ordinary project stack routing when the project does not rely on runtime preset-specific Skill policies. Current OMO startup/config-file merging gives root agent entries precedence, but runtime `/preset` switching can apply a different merge order. If runtime switching is used, verify effective routing after a switch or deliberately maintain the relevant preset-local entries.

### Route Skills minimally

Default policy:

- Orchestrator: inherit the existing global policy; do not create a project override merely to repeat `skills: ["*"]`.
- Explorer and Librarian: no technology Skill routing by default.
- Oracle: preserve the existing policy (commonly `simplify`); add project-local workflow/review Skills only when deliberately selected.
- Fixer: route only implementation Skills proven relevant to the repository.
- Designer: route frontend/UI Skills only when that work is in scope.
- Observer: leave unchanged unless a concrete project need exists.
- Never auto-route `skills/operational/*`.
- OMO Skill routing does not replace OpenCode `permission.skill`; do not weaken existing `ask`/`deny` gates.
- Do not duplicate OMO Slim bundled Skills into `.opencode/skills/`; OMO owns their installation/update. Route them only when already discoverable and deliberately needed.

Every Skill ID written to OMO config must be discoverable after this bootstrap. Remove conditional example entries that the project does not use. A dependency appearing transitively is not enough evidence to select a Skill.

Write the smallest root `agents.<agent>.skills` override needed. If an existing project config intentionally uses preset-specific routing, preserve that design and update the active preset block instead of silently converting it. Record any non-obvious precedence decision.

Workflow Skills such as `bug-reproduction-brief`, `refactor-plan`, and `verification-before-completion` remain explicit-use tools by default. Do not add them to specialist routing merely because they are available.

After changing OMO Slim routing, plan for an OpenCode restart before behavioral smoke testing.

## 6. Establish or review the constitution

When Spec Kit is initialized, use the installed `/speckit.constitution` workflow as authority. If slash commands cannot be invoked from the current context, locate the installed OpenCode command and follow it rather than reconstructing the workflow from memory.

For a new/template constitution, derive only durable project-wide principles from repository evidence and the finalized `AGENTS.md`, such as:

- public contract preservation;
- module/domain ownership;
- generated-source ownership;
- DB/data-integrity constraints;
- auth/security boundaries;
- sibling repository write boundaries;
- truly mandatory validation gates.

Do not copy global engineering guidance, formatting preferences, temporary feature requirements, class/file-specific rules, speculative architecture, or generic framework advice.

Preserve an existing non-template constitution. For a material governance change, show the proposed diff and require confirmation before applying it; otherwise report the drift.

## 7. Repository hygiene

Inspect `.opencode/` before changing `.gitignore`.

- Keep commands, Skills, and non-secret project configuration trackable.
- Ignore only concrete credentials, tokens, caches, private profiles, or machine-local artifacts.
- Never print or copy secret contents into the report.

## 8. Validate onboarding

Run the checks that prove the onboarding work itself, without running unrelated expensive application tests.

At minimum when available:

```bash
specify version
specify integration status --json
git diff --check
git status --short
```

Use plain `specify integration status` if JSON output is unavailable. For OMO diagnostics, first determine the package spec already configured by OpenCode. When an existing supported runner can invoke that same OMO Slim package/version safely, run `doctor --json` from the project root. Do not hard-code `@latest` merely for validation, and do not change or upgrade the configured plugin as a side effect. If a matching diagnostic invocation cannot be established, mark OMO diagnostics `NOT RUN`.

Also verify:

- `.specify/` and OpenCode integration files exist when initialization succeeded;
- `AGENTS.md` has no unresolved placeholders;
- a newly created constitution has no unresolved template placeholders;
- selected Skill IDs are unique in the discovery roots inspected;
- every OMO-routed Skill ID is discoverable and no unrelated user-level OMO setting was copied into the project;
- project-local OMO config passes available doctor/schema diagnostics;
- no operational Skill was installed or routed without authorization;
- no application source, schema, migration, test, business logic, or upstream Skill snapshot was modified by onboarding.

## Final report

Report only:

1. project facts discovered;
2. Spec Kit state, version, default integration, and health;
3. `AGENTS.md` changes;
4. constitution state and any confirmed change;
5. selected Skills and duplicates/operational exclusions;
6. project-local OMO Slim routing and diagnostic status;
7. files changed;
8. actual validation results;
9. `NOT RUN`, `BLOCKED`, or unresolved conflicts.

Do not describe the repository as fully configured when a required step failed, was not run, or remains blocked.

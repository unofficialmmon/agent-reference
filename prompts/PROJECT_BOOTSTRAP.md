# Project Bootstrap Prompt

Prepare the current repository's agent-facing configuration for OpenCode, agent-reference guidance, selected Skills, and minimal project-local OMO Slim routing.

This is a project-onboarding task, not a feature implementation task. Do not modify application source, business logic, tests, schemas, migrations, generated output, or deployment configuration except for tooling/configuration files explicitly covered below.

**Spec Kit is optional.** Do not install, initialize, repair, upgrade, or make Spec Kit the default workflow unless the user explicitly asks for Spec Kit in this bootstrap. If an existing `.specify/` tree is present and Spec Kit was not requested, preserve it untouched and report its presence only.

## Reference source

When this prompt is read from an `agent-reference/prompts/` directory, treat the parent `agent-reference/` directory as the reference source root. Resolve catalog and Skill paths from that root. If the source root cannot be located, do not guess paths or recreate Skill content; continue only with repository-local work and report Skill selection as `NOT RUN`.

## Intended result

Leave the repository with:

- a concise, factual project-root `AGENTS.md`;
- only project-relevant Skill selection/deployment using the repository's existing ownership model;
- a minimal project-local OMO Slim Skill-routing override when OMO Slim is installed;
- no operational Skill enabled without explicit authorization;
- optional Spec Kit setup only when explicitly requested;
- an honest report of changes, failures, blocked work, and unverified scope.

Do not create a new workflow engine, agent framework, installer, or project architecture. Do not modify OMO Slim global configuration, models, variants, MCPs, companion settings, prompt overrides, custom agents, or unrelated permissions during bootstrap.

Treat project-local OMO Slim configuration as a trust boundary because OMO loads it automatically and it can alter agent behavior, tool access, and Skill access. Before creating or changing it, inspect the current file and repository trust context; never copy an unreviewed OMO config from another project.

If the repository is already correctly configured, finish with `NOOP` rather than rewriting equivalent content for style or wording alone. Bootstrap quality is measured by accurate minimal setup, not by the number of files changed.

## Safety and authority

Use this order:

1. explicit user instruction;
2. existing project `AGENTS.md` and authoritative contracts;
3. maintained source, tests, schemas, build/configuration, README, and architecture docs;
4. existing APM/OpenCode/OMO configuration and ownership;
5. explicitly requested Spec Kit artifacts;
6. agent-reference templates and selected Skills;
7. global OpenCode references.

Preserve the current working tree.

- Start with `git status --short`.
- Do not run `git add`, `commit`, `stash`, `reset`, `clean`, `checkout --`, deploy, or destructive equivalents unless explicitly requested.
- Treat sibling repositories as read-only unless explicit authority grants writes.
- Do not ignore `.opencode/` wholesale. Inspect it first; committed commands and configuration may live there.
- Treat CodeGraph, search indexes, caches, and symbol databases as navigation aids. Confirm important claims against current files.

## Mutation checkpoint

Before the first write, prepare a concise change plan listing the files/directories to create or update.

Ask one concise confirmation before proceeding when any of these are true:

- the working tree is dirty and a planned target overlaps an existing change;
- `AGENTS.md`, `.opencode/`, `.agents/skills/`, `.specify/`, a project-local OMO Slim config, `apm.yml`, or relevant `.gitignore` entries already exist and may be materially rewritten;
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
- current `AGENTS.md`, APM manifest/lock if present, `.opencode/`, `.agents/skills/`, and installed Skill IDs;
- `.specify/` only as an existing optional integration unless Spec Kit was explicitly requested.

Do not treat deleted, archived, generated, example, or stale-index-only material as current architecture authority.

## 2. Create or refine project `AGENTS.md`

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
- short Skill/APM/OMO routing notes when relevant.

Do not copy global `ENGINEERING.md`, whole Skill bodies, generic framework advice, OMO agent roles, speculative architecture, or mandatory methodology for routine fixes.

Preserve valid existing project rules. When `AGENTS.md` conflicts with maintained contracts/source, treat it as possible drift and resolve the evidence rather than hiding the mismatch.

## 3. Select project Skills without breaking ownership

When the agent-reference catalog is accessible, inspect `catalog/skills.lock.json` and relevant Skill directories.

**Catalog inclusion is not activation.**

- Select only Skills directly relevant to the project's real stack or contract boundaries.
- Check visible project/global discovery roots for duplicate IDs before deployment.
- Never edit an upstream snapshot in place.
- Never install `skills/operational/*` without explicit authorization for the specific Skill.
- Workflow Skills such as `bug-reproduction-brief`, `refactor-plan`, and `verification-before-completion` are explicit-use tools, not ambient defaults.

Respect the repository's existing Skill ownership model:

- If the project already has a coherent APM adoption, do not hand-copy or edit APM-generated `.agents/skills/` output. Preserve APM ownership and use the supported `/agent-sync` or `/apm-setup` path for dependency/selection changes.
- If APM is absent and the user did not explicitly request manual Skill deployment, report the recommended Skill IDs but do not create a competing manual installation. Recommend `/apm-setup` for first adoption.
- Manual project-local copying is a fallback only when APM is unavailable or the user explicitly chooses manual management. In that case, copy the complete Skill directory byte-for-byte and do not overwrite same-ID content silently.

If the catalog is inaccessible, do not invent Skill names or recreate content. Mark Skill reconciliation `NOT RUN` and report useful technology categories only.

## 4. Configure project-local OMO Slim Skill routing

Do this only when OMO Slim is installed/configured or its project-local config already exists. Use the installed `oh-my-opencode-slim` Skill and current OMO Slim schema/documentation as configuration authority when available.

When `agent-reference/templates/omo/` is accessible, read `README.md` and `ROUTING.md`, then use the closest stack template as a candidate example only. Adapt it to repository evidence and actually discoverable Skill IDs. Never copy a stack example blindly.

Preserve the global setup:

- Read the effective user config only as needed to understand current agent policy; never write it during project bootstrap.
- Project-local configuration belongs in `.opencode/oh-my-opencode-slim.json` or `.jsonc`. If one already exists, merge into that file. Do not create both formats merely because a template uses JSONC.
- Preserve existing model, variant, MCP, companion, multiplexer, permission, custom-agent, and prompt settings.
- Treat each agent `skills` array as an effective allowlist rather than an additive list.
- Prefer root `agents.<agent>.skills` for ordinary project stack routing when the project does not intentionally rely on preset-specific Skill policies.

Default routing policy:

- Orchestrator: inherit the existing global policy.
- Explorer and Librarian: no technology Skill routing by default.
- Oracle: preserve existing policy; add review/workflow Skills only when deliberately selected.
- Fixer: route only implementation Skills proven relevant and currently discoverable.
- Designer: route frontend/UI Skills only when that work is in scope.
- Observer: leave unchanged unless a concrete project need exists.
- Never auto-route operational Skills.
- Do not weaken existing OpenCode `permission.skill` gates.

Every Skill ID written to OMO config must be discoverable after bootstrap. After changing routing, restart OpenCode before behavioral smoke testing.

## 5. Optional Spec Kit handling

Run this section **only when the user explicitly requested Spec Kit as part of this bootstrap**.

If Spec Kit was not requested:

- do not run `specify` commands;
- do not create or repair `.specify/`;
- do not create or restore `speckit.*` commands;
- do not create or modify a constitution;
- preserve any existing Spec Kit files untouched and report `Spec Kit: NOT REQUESTED`.

When explicitly requested, use the installed Spec Kit CLI and its native integration workflow as authority. First run:

```bash
specify version
```

If the CLI is unavailable, do not install a global tool silently. Mark the step `BLOCKED` and provide the official installation command appropriate to the current documented Spec Kit release.

For a new integration, inspect for conflicting remnants and satisfy the mutation checkpoint before initialization. For an existing integration, prefer `specify integration status --json` (or plain `status` when unsupported), then use native install/upgrade/use operations only as required. Do not silently use `--force`, upgrade the CLI, change the default integration, or overwrite modified managed files.

A constitution is optional even when Spec Kit is installed. Create or materially change one only when explicitly requested and derive it from durable repository facts, not generic engineering philosophy.

## 6. Repository hygiene

Inspect `.opencode/`, `.agents/`, and existing ignore rules before changing `.gitignore`.

- Keep commands, Skills, manifests, locks, and non-secret project configuration trackable when the repository intends to version them.
- Ignore only concrete credentials, tokens, caches, private profiles, or machine-local artifacts.
- Never print or copy secret contents into the report.

## 7. Validate onboarding

Run checks that prove the onboarding work itself without running unrelated expensive application tests.

At minimum when available:

```bash
git diff --check
git status --short
```

Also verify:

- `AGENTS.md` has no unresolved placeholders;
- selected Skill IDs are unique across the discovery roots inspected;
- APM-managed outputs were not hand-edited;
- every OMO-routed Skill ID is discoverable and no unrelated user-level OMO setting was copied into the project;
- no operational Skill was installed or routed without explicit authorization;
- no application source, schema, migration, test, business logic, or upstream Skill snapshot was modified by onboarding;
- Spec Kit files were untouched when Spec Kit was not requested.

When Spec Kit was explicitly requested, additionally run its native status check after mutation and verify managed files/constitution as appropriate.

For OMO diagnostics, determine the package spec already configured by OpenCode. When an existing supported runner can invoke that same package/version safely, run `doctor --json` from the project root; otherwise report OMO diagnostics `NOT RUN`.

## Final report

Report only:

1. project facts discovered;
2. `AGENTS.md` changes;
3. selected Skills, ownership/deployment state, duplicates, and operational exclusions;
4. project-local OMO Slim routing and diagnostic status;
5. Spec Kit as `NOT REQUESTED`, preserved-existing, or explicitly configured state;
6. files changed;
7. actual validation results;
8. `NOT RUN`, `BLOCKED`, or unresolved conflicts.

Do not describe the repository as fully configured when a required requested step failed, was not run, or remains blocked.

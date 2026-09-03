# Project Audit Prompt

Perform a read-only audit of the repository's agent-facing development setup. Do not modify files.

## Goal

Determine whether the current configuration gives coding agents accurate, minimal, safe guidance without duplicating OpenCode, OMO Slim, APM, or optional Spec Kit behavior.

## Audit

1. Inspect `git status --short` and treat all existing changes as user-owned.
2. Compare project-root `AGENTS.md` with maintained source, tests, schemas, build/configuration, and authoritative docs.
3. Verify the claims that matter:
   - project purpose and active stack;
   - module/domain ownership and write boundaries;
   - API, DB, auth/security, IPC, and external contracts when present;
   - generated-source ownership and source of truth;
   - formatter/linter/build/test commands;
   - sibling/shared repository boundaries.
4. Treat CodeGraph/search indexes as navigation aids and verify important claims against current files.
5. Review Skill ownership and discovery:
   - identify the repository's actual Skill owner (APM-managed project deployment, intentional manual project Skill, or deliberate user-global utility/override);
   - for an APM-adopted repository, project technology Skills should resolve to the APM-managed project copy;
   - classify a higher-precedence user-global same-ID project technology Skill as `SHADOWED_IDENTICAL` when byte-identical and `SHADOWED_DIVERGENT` when different;
   - treat `SHADOWED_IDENTICAL` as cleanup debt toward a single APM owner, not as a runtime-content failure;
   - treat `SHADOWED_DIVERGENT` as a material ownership/version conflict because the effective runtime winner is not the intended APM content;
   - do not flag genuine cross-project utility/tooling Skills merely because they live under the user-global root;
   - flag irrelevant or obsolete project Skills;
   - flag important missing Skills only when the agent-reference catalog is accessible;
   - flag operational Skills active without an explicit current need.
6. Review project-local OMO Slim configuration when present or when OMO Slim is installed:
   - treat it as auto-loaded trusted configuration and flag unreviewed or unexpectedly introduced changes that can alter agent behavior, tools, or Skill access;
   - verify routed Skill IDs are actually discoverable and resolve to the intended/identical content;
   - flag stack Skills that no longer match repository evidence;
   - flag automatic routing of operational Skills;
   - flag unnecessary duplication of global model, variant, MCP, companion, multiplexer, prompt, or agent settings;
   - account for `.jsonc` precedence if both project config formats exist;
   - flag preset-specific stack routing that has no deliberate preset-specific reason when a smaller root `agents.<agent>.skills` override is sufficient for the project’s normal startup configuration; if runtime `/preset` switching is used, require evidence that effective routing remains correct after the switch;
   - flag project Skill allowlists that unintentionally drop deliberate user/global agent Skills;
   - when the OMO Slim package spec already configured by OpenCode can be invoked safely with an existing supported runner, run its read-only `doctor --json`; do not switch to `@latest` merely for the audit; otherwise record the diagnostic as `NOT RUN` (or `BLOCKED` when a required dependency prevents it);
   - do not modify global or project OMO Slim configuration.
7. Treat Spec Kit as optional:
   - absence of `.specify/` is healthy and is not an audit finding;
   - if `.specify/` exists, inspect the constitution for obvious conflict with durable project constraints;
   - when `specify` is available and existing Spec Kit state is in scope, run the read-only `specify integration status --json` command;
   - if `--json` is unsupported, use plain `specify integration status` and report that limitation;
   - report missing/modified/invalid managed state only for a repository that actually intends to keep Spec Kit;
   - flag stale `AGENTS.md` claims that Spec Kit is installed/required when current repository evidence and explicit user intent show it was retired;
   - do not run `init`, `install`, `upgrade`, `use`, extension/preset updates, or constitution changes.
8. Inspect `.opencode/`, `.agents/`, and ignore rules for actual credential/cache exposure or overly broad ignores.
9. Check for stale paths, nonexistent commands, removed technology, duplicated global guidance, speculative rules, and project instructions that conflict with maintained repository facts.

## Do not

- Do not edit source, docs, configuration, Skills, Spec Kit artifacts, or history.
- Do not delete global shadowing Skills during this audit; recommend user-scope cleanup separately when appropriate.
- Do not run destructive commands, deploy, commit, push, reset, or clean.
- Do not expand this into a whole-application code review or refactor proposal.
- If the agent-reference catalog or external tooling is unavailable, record the check as `NOT RUN` or `BLOCKED`; place any resulting audit conclusion under `UNVERIFIED` rather than guessing.

## Output

Use evidence labels consistently: `ACTUAL PASS`, `ACTUAL FAIL`, `STATIC`, `NOT RUN`, and `BLOCKED`. Audit conclusions may still be `PASS`, a concrete finding, or `UNVERIFIED` when the available evidence cannot decide the issue.

Use four sections only.

### PASS

Accurate configuration worth keeping.

### FINDINGS

Concrete stale, conflicting, unsafe, or unnecessary configuration with file/path evidence. Distinguish benign-but-unwanted `SHADOWED_IDENTICAL` cleanup debt from material `SHADOWED_DIVERGENT` runtime ownership conflicts.

### RECOMMENDED CHANGES

Small configuration-only corrections, ordered by importance. Do not implement them.

### UNVERIFIED

Anything that could not be proven from current repository evidence or available tools.

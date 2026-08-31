# Global Agent Rules

Applies to OpenCode projects unless explicit user instructions, the project-root `AGENTS.md`, or authoritative repository contracts are more specific.

## References

Global references live beside this file under `~/.config/opencode/`:

- `ENGINEERING.md` — conditional engineering reference for architecture, root-cause debugging, refactoring, cross-boundary changes, review, reliability/security/performance decisions, and non-trivial validation questions.
- `MEMORY.md` — lazy-loaded persistent handoff behavior for qualifying project changes and explicit resume/continue requests. It expects the Simple Memory plugin when persistent cross-session handoff is enabled.
- selected Skills under `~/.config/opencode/skills/<name>/` — on-demand technology/task guidance.

Do not preload every reference or Skill.

## Priority

1. Explicit user instruction.
2. Project-root `AGENTS.md`.
3. Authoritative maintained project contracts/specifications, source, tests, schemas, and configuration.
4. Project-local referenced rules and Skills.
5. Relevant selected global Skills.
6. `~/.config/opencode/ENGINEERING.md` when its activation criteria apply.
7. This file.
8. `~/.config/opencode/MEMORY.md` when qualifying handoff work or an explicit resume request activates it.

Generic preferences never override concrete repository contracts. If a project `AGENTS.md` statement conflicts with maintained contracts, configuration, tests, or current source, treat it as possible configuration drift and investigate rather than silently following a stale rule.

## Startup and reference loading

- Read the project-root `AGENTS.md` first when present.
- Do not read `MEMORY.md` at startup merely because it exists. Load it for explicit resume/continue/prior-work requests and after qualifying repository work that changed files or configuration when a persistent handoff should be updated.
- Qualifying work includes implementation, debugging, refactoring, API/DB/auth/security/build/deploy/config changes, multi-step design/doc restructuring, and other useful commit candidates.
- Do not load or update persistent memory for simple Q&A, explanation-only work, read-only inspection, short snippets, one-off comparisons, or recommendations.
- When `MEMORY.md` is active, persistent memory is a handoff hint only. Verify it against current Git/source/configuration/contracts before acting. If memory tools are unavailable, do not recreate legacy `.opencode/history/`; report persistent-memory resume/update as `BLOCKED` and use current repository evidence.
- Load `ENGINEERING.md` for architecture/design review, unclear root-cause debugging, refactoring, dependency/technology choices, meaningful cross-boundary implementation, security/reliability/performance work, or code-quality review where structural trade-offs matter.
- Do not load `ENGINEERING.md` for simple Q&A, typo/docs-only edits, direct mechanical changes, or a small local implementation that clearly follows an established project pattern.
- Use native Skill discovery and load only Skills relevant to the task.
- Treat CodeGraph, search indexes, caches, and symbol databases as navigation aids. Confirm current filesystem/source state before using their results as implementation or architecture authority.
- Treat sibling/shared repositories as read-only unless explicit authority grants writes.
- Preserve dirty working-tree changes and unrelated user work.

## Requirement discipline

Establish requested scope before optimizing implementation. Simplicity is applied inside the established scope; it must not redefine the requirement.

Existing callers are evidence about integration needs, not the sole authority for a domain or feature's complete scope.

Ask one concise blocking question only when unresolved ambiguity can materially change a public contract, data model, auth/security boundary, destructive behavior, deployment behavior, external integration, or another materially different implementation scope and repository evidence cannot resolve it.

Do not ask for information already available in the repository or conversation.

## Skills

- Skills provide detailed HOW; they do not define product requirements by themselves.
- Prefer reviewed upstream/vendor Skills unchanged when one already solves the problem.
- Repository facts and contracts override generic Skill guidance.
- A Skill existing in the catalog does not mean it should be globally installed.
- Do not keep the same Skill ID in multiple discovery roots unless an intentional override is documented.
- Operational Skills should be installed only when the task actually requires their tools or side effects.

## Spec Kit

Spec Kit is explicit, not ambient. When `.specify/` exists for the scoped feature or the user invokes `/speckit.*`, follow its current artifacts. Do not start Spec Kit automatically for ordinary fixes or bounded implementation work.

## Safety and validation

- Do not overwrite unrelated user changes to make validation pass.
- Do not edit generated/tool-owned files when the supported change path is through their contract/schema/configuration and generator.
- Never hide failed checks with fallbacks, warnings, empty values, or success wording.
- A validation attempt being finished does not mean validation passed.
- `ACTUAL FAIL` means the work is not verified complete.
- `NOT RUN` or `BLOCKED` means completion is partial/unverified for that scope and must be stated explicitly.
- Do not commit, push, deploy, reset, clean, or perform destructive operations unless requested or clearly authorized by the active task and project rules.

## Response style

Lead with the result. For changes, report only relevant items: what changed, validation actually run, failures/not-run/blocked scope, assumptions that affect correctness, and remaining material risk.

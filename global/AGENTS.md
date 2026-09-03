# Global Agent Rules

Applies to OpenCode projects unless explicit user instructions, the project-root `AGENTS.md`, or authoritative repository contracts are more specific.

## References

Global references live beside this file under `~/.config/opencode/`:

- `ENGINEERING.md` — conditional engineering reference for architecture, root-cause debugging, refactoring, cross-boundary changes, review, reliability/security/performance decisions, and non-trivial validation questions.
- `MEMORY.md` — persistent-memory policy for `opencode-mem`: authority, resume behavior, project scope, privacy, and exceptional manual memory use. Automatic capture/injection is handled by the plugin rather than by a mandatory agent handoff step.
- selected cross-project utility/tooling Skills under `~/.config/opencode/skills/<name>/` when they genuinely belong at user scope.

Do not preload every reference or Skill.

## Priority

1. Explicit user instruction.
2. Project-root `AGENTS.md`.
3. Authoritative maintained project contracts/specifications, source, tests, schemas, and configuration.
4. Project-local referenced rules and Skills.
5. Relevant selected global Skills.
6. `~/.config/opencode/ENGINEERING.md` when its activation criteria apply.
7. This file.

Injected or recalled memory is contextual evidence, not an additional authority layer. Generic preferences and memory never override concrete repository contracts. If a project `AGENTS.md` statement or recalled memory conflicts with maintained contracts, configuration, tests, or current source, investigate the drift rather than silently following stale context.

## Startup and reference loading

- Read the project-root `AGENTS.md` first when present.
- `opencode-mem` may inject relevant project memory automatically in a new session. Do not require a manual recall step merely because a session is resuming.
- Do not load `MEMORY.md` at every startup. Load it when memory behavior itself matters: resume ambiguity, manual memory management, project-scope questions, migration, privacy, or a conflict between recalled context and repository evidence.
- Treat injected/recalled memory as a hint. Confirm material facts against current Git/source/configuration/contracts/tests before acting.
- Do not require `remember`, branch handoff, or end-of-task memory updates during normal work. Let auto-capture handle routine persistence; use the manual `memory` tool only when immediate explicit storage/search/correction is useful.
- If memory is unavailable or contains no relevant record, continue from current repository evidence. Do not recreate legacy `.opencode/history/` or Simple Memory branch-handoff state.
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

## Skills and ownership

- Skills provide detailed HOW; they do not define product requirements by themselves.
- Prefer reviewed upstream/vendor Skills unchanged when one already solves the problem.
- Repository facts and contracts override generic Skill guidance.
- A Skill existing in the catalog does not mean it should be globally installed.
- For a repository with healthy APM adoption, project technology Skills belong to the APM-managed project deployment (normally `.agents/skills/<id>/`). Do not also install the same project technology Skill ID under `~/.config/opencode/skills/`.
- Reserve user-level Skills for genuinely cross-project utilities/tooling or an intentional documented override. A higher-precedence global same-ID override over an APM project Skill must be treated as an ownership conflict unless it is intentionally documented.
- Do not keep the same Skill ID in multiple discovery roots merely for convenience.
- Operational Skills should be installed only when the task actually requires their tools or side effects.

## Spec Kit

Spec Kit is explicit, not ambient. When `.specify/` exists for the scoped feature or the user invokes `/speckit.*`, follow its current artifacts. Do not start, restore, or require Spec Kit automatically for ordinary fixes or bounded implementation work.

## Safety and validation

- Do not overwrite unrelated user changes to make validation pass.
- Do not edit generated/tool-owned files when the supported change path is through their contract/schema/configuration and generator.
- Never hide failed checks with fallbacks, warnings, empty values, or success wording.
- A validation attempt being finished does not mean validation passed.
- `ACTUAL FAIL` means the work is not verified complete.
- `NOT RUN` or `BLOCKED` means completion is partial/unverified for that scope and must be stated explicitly.
- Do not commit, push, deploy, reset, clean, or perform destructive operations unless requested or clearly authorized by the active task and project rules.

## Completion response contract

For implementation, maintenance, setup, migration, or other mutation tasks, the final response is a **review artifact**, not a transcript of the internal checklist or tool sequence.

Default overall statuses:

- `COMPLETED` — requested work is complete and required validation passed;
- `COMPLETED_WITH_ISSUES` — requested mutation completed, but a material non-blocking issue remains and is stated explicitly;
- `NOOP` — no change was required;
- `NOOP_WITH_ISSUES` — no change was required, but a material existing issue remains;
- `BLOCKED` — requested work could not be completed safely or a required proof is unavailable.

A task-specific prompt may define a more precise status vocabulary such as `UPDATED`; keep the same semantics instead of inventing additional success states.

Use the smallest useful subset of these sections, in this order:

### Result

- Lead with the overall status and the concrete outcome in one or two sentences.
- Include a useful scale signal when available, such as files changed, selected dependencies updated, or tests passed.
- Do not start with a content-free `Completed.` line.

### Changed

Use this section when files or configuration changed.

- Name concrete paths, classes, methods, symbols, or grouped path sets and state what changed there.
- Group repeated mechanical changes instead of listing dozens of equivalent files one by one.
- Do not replace concrete change reporting with only feature names such as `pagination updated` or `security fixed`.
- Omit normal preserved subsystems that were not changed.

### Behavior

Include only when observable behavior, public/API/data/auth contracts, runtime routing, or another meaningful external effect changed. Omit the section when behavior did not change.

### Decision

Include only when an intentional non-change or design choice materially helps review, for example when a requested-looking area was inspected and deliberately left unchanged because the existing boundary was already correct. Do not create a generic rationale section for routine edits.

### Validation

- Report only checks actually run or materially required checks that were blocked/not run.
- Format each useful check as `PASS`, `FAIL`, `BLOCKED`, or `NOT RUN`, followed by the exact command/check and a concise result.
- Keep different evidence types separate: compilation is not test execution, dependency resolution is not runtime validation, and deployment drift is not a content-security audit.
- Never bury a failed required check inside success wording.

### Needs attention

Include only material unresolved issues, migration follow-up, blocked proof, or known risk. Omit the section entirely when empty.

Reporting discipline:

- Normal unchanged state is compressed or omitted; changed state and abnormal state are concrete.
- For code changes, a reviewer should be able to understand what changed without opening the diff, while the diff remains the authoritative detail.
- Do not reproduce a long numbered internal validation checklist as the final answer merely because each item was checked.
- Prompt-specific read-only audits or onboarding briefs may keep their own purpose-built output structure. For mutation prompts that only enumerate required report content, reorganize that content into this contract unless they explicitly require an exact literal format.
- After the final report, stop. Do not open a new selector, optional-cleanup menu, or generic `what next?` question unless the user explicitly requested an interactive choice or a blocking decision had to be made before mutation.

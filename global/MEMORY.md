# Persistent Memory Reference

Default persistent-handoff rules for qualifying OpenCode project work. Memory is lazy-loaded for resume/handoff work rather than preloaded at startup.

This reference assumes the Simple Memory plugin (`@knikolov/opencode-plugin-simple-memory`) is available. The recommended mode is explicit/manual memory use with `autoLoad: false` and `autoSave: false`.

Memory is a handoff aid, not a source of truth. Current Git state, maintained source, configuration, contracts, and fresh validation override stored memory.

## Activation

Load this reference when either condition applies:

- the user asks to resume, continue, pick up, summarize, or use prior project work;
- qualifying repository work changed files/configuration and a persistent handoff should be updated before the final response.

Qualifying work includes implementation, debugging, refactoring, API/DB/auth/security/build/deploy/config changes, multi-step design/doc restructuring, and other useful commit candidates.

Do not load or update persistent memory for simple Q&A, explanation-only work, read-only inspection, short snippets, one-off comparisons, or recommendations.

If the Simple Memory tools are unavailable, do not recreate the legacy `.opencode/history/` system or invent a handoff. Continue from current repository evidence when possible and report persistent-memory resume/update as `BLOCKED`.

## Handoff identity

Use one current handoff memory per active branch/worktree:

- type: `context`;
- scope: `handoff/<current-branch>`;
- scope matching: `exact`.

Resolve the current Git branch before recall/update. If HEAD is detached, use a stable scope such as `handoff/detached/<short-sha>` for that detached state.

Simple Memory stores data under the OpenCode project directory (`.opencode/memory/`). Separate worktree directories therefore have separate local memory stores; do not assume a handoff automatically crosses worktrees or machines.

## Resume procedure

For an explicit resume/continue request:

1. read the project-root `AGENTS.md` when present;
2. determine the current branch/worktree state;
3. call `memory_recall` with `type="context"`, exact scope `handoff/<current-branch>`, and a small limit sufficient to detect duplicates;
4. if no exact handoff exists, report that no persistent handoff exists for the current branch and continue only from current repository evidence;
5. if more than one exact handoff exists, resolve the duplicate state before trusting or updating it; do not append another duplicate;
6. verify the recalled goal/status against `git status`, current source/configuration/contracts, and any validation evidence that materially affects the next action;
7. recall additional `decision`, `blocker`, `pattern`, or `preference` memories only when they are relevant to the current task.

Do not use `memory_context` as the authoritative resume path because it intentionally builds a compact/truncated context pack. Use exact `memory_recall` for the current handoff.

## Handoff update

After qualifying work, keep exactly one current handoff for the active branch.

Use an upsert pattern because Simple Memory has separate remember/update tools:

1. exact-recall the current `context/handoff/<branch>` memory;
2. if none exists, create it with `memory_remember`;
3. if exactly one exists, replace its current contents with `memory_update`;
4. if duplicates exist, reconcile/remove stale duplicates before writing and never create another handoff entry for the same exact scope.

Keep the handoff compact, normally about 500-1500 characters. Record only facts useful to the next session:

- Goal;
- Status;
- Changed areas/files when useful;
- Validation actually run and its result;
- Remaining work;
- Unverified boundaries;
- Next action.

The current handoff is a resume pointer, not a journal. Overwrite/update it as work advances.

## Durable memory

Store durable memory sparsely and only when it is likely to remain useful across sessions:

- `decision/<topic>` — durable architectural/design decisions and their reason;
- `blocker/<topic>` — unresolved blockers that still constrain work;
- `pattern/<topic>` — recurring repository patterns that are not already better expressed by authoritative project rules;
- `preference/<topic>` — explicit user/project preferences that are appropriate to persist.

Prefer `AGENTS.md`, maintained contracts, configuration, and Skills for durable normative rules. Do not duplicate an authoritative rule into memory merely for convenience.

Do not automatically convert ordinary conversation, transient observations, or every completed task into durable memory.

## OMO Slim ownership

When OMO Slim delegates work, persistent-memory writes belong to the Orchestrator/coordinating agent.

- Subagents may read relevant memory when needed.
- Subagents should return discoveries to the Orchestrator rather than independently mutating persistent memory.
- The Orchestrator verifies material discoveries against the repository before persisting them.

This single-writer policy reduces races and contradictory handoffs during parallel delegation.

## Safety and privacy

Never store:

- secrets, credentials, API keys, tokens, cookies, private keys, or authorization headers;
- personal/sensitive data that is not explicitly appropriate for project-local persistence;
- private host details that should not be written to local project state;
- full conversations or private reasoning;
- full diffs, large terminal output, repeated failure logs, or generated diagnostics.

`memory_forget` and `memory_update` are not secure-erasure mechanisms; deletion/audit data may retain previous content. Therefore sensitive values must never enter memory in the first place.

Treat `.opencode/memory/` as machine-local runtime state by default. Do not commit it to Git unless a project has an explicit, reviewed reason to do so. Prefer a local exclusion such as `.git/info/exclude` when only one developer needs the setting; use a project `.gitignore` entry only when the repository intentionally standardizes the exclusion. Never ignore all of `.opencode/` because trackable commands, Skills, and project configuration may live there.

## Legacy History migration

Do not bulk-import the legacy `.opencode/history/` journal tree.

When migrating an existing project:

1. read only `current.md` and the currently active area/index material needed to understand unfinished work;
2. verify that state against current Git/source/configuration;
3. create one current branch handoff plus only genuinely durable decisions/blockers/patterns/preferences;
4. open a new OpenCode session and verify that a concise resume request can exact-recall the handoff and reconcile it with the repository;
5. only after that smoke test succeeds, remove the legacy History routing/files.

Past changelog entries that describe when the History system existed remain historical records and should not be rewritten merely because the active protocol changed.

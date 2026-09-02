# Persistent Memory Reference

Persistent-memory policy for OpenCode projects using `opencode-mem`.

Memory is contextual continuity, not a source of truth. Current Git state, maintained source, configuration, contracts, tests, and fresh validation override stored or injected memory.

## Normal behavior

`opencode-mem` is designed to work without a mandatory handoff ceremony.

Normal flow:

1. work normally in OpenCode;
2. after conversation turns, the plugin may auto-capture memorable technical context when the session becomes idle;
3. later sessions may receive relevant project memories automatically;
4. the agent reconciles that context with the current repository before relying on it.

A `Memory captured` notification is expected runtime feedback when auto-capture succeeds. It is not a request for the user or agent to save another handoff.

Do not require routine commands such as `remember`, `recall`, `update`, `handoff/main`, or `handoff/<branch>` before finishing work. Do not recreate the old branch-scoped Simple Memory workflow under new names.

## Authority and stale memory

Treat injected, searched, or manually added memory as a hint about prior work.

When memory and current repository evidence differ:

1. explicit user instruction and project authority remain primary;
2. maintained contracts/source/configuration/tests describe the current implementation;
3. memory may explain history or intent but must not override current evidence;
4. correct or forget stale memory when it is materially misleading and safe to do so.

Stable normative rules belong in `AGENTS.md`, maintained contracts, configuration, or another authoritative project document. Memory is better suited to project-specific decisions, prior failed approaches, temporary blockers, useful work context, and preferences discovered across sessions.

## Resume and continue requests

For an explicit resume/continue request:

1. read the project-root `AGENTS.md` when present and inspect the current repository state;
2. use already injected memory when relevant;
3. search memory only when the injected context is insufficient or a specific prior fact is needed;
4. reconcile material recalled facts with current Git/source/configuration/contracts/tests;
5. continue from repository evidence even when no useful memory exists.

Persistent memory is optional continuity. Missing or unavailable memory must not block ordinary repository work when current evidence is sufficient.

## Manual memory use

Use the `memory` tool on demand rather than as a required end-of-task step.

Reasonable manual uses include:

- immediately preserving a durable project decision before auto-capture runs;
- searching for prior work or a known decision that was not injected;
- listing or inspecting memories during troubleshooting;
- correcting or forgetting stale/incorrect memory;
- exporting/importing or migrating memory when the user explicitly wants that operation.

Do not manually store every completed task, transient observation, terminal log, diff, or conversation summary. Automatic capture should handle normal continuity.

## Scope and project identity

Use project scope by default unless there is a deliberate reason to query across projects.

`opencode-mem` normally derives project identity from the current project/Git context. Do not create `.opencode-mem-project` automatically.

Use a `.opencode-mem-project` marker only when multiple nested repositories are intentionally one memory domain, for example:

```text
workspace/
├── .opencode-mem-project
├── gateway/.git
├── core/.git
└── cargo/.git
```

The marker changes project identity semantics; treat it as an intentional project decision rather than generic setup boilerplate.

## Storage, provider, and privacy boundaries

`opencode-mem` stores memory in its own local data directory by default (commonly under `~/.opencode-mem/data`), not in the retired project-local Simple Memory `.opencode/memory/` store.

Local storage does not imply that every memory operation is local. Auto-capture and profile learning may use a configured AI provider. When that provider is remote, relevant conversation/work context can leave the machine for extraction even though the resulting memory database is local.

Therefore:

- never intentionally store secrets, credentials, API keys, tokens, cookies, private keys, authorization headers, or other sensitive authentication material;
- do not treat memory as a credential store;
- do not print provider secrets while troubleshooting;
- keep the web UI on loopback/localhost by default;
- if the UI is intentionally exposed beyond loopback, follow the current upstream authentication guidance;
- understand the configured capture provider and its data boundary before enabling auto-capture for sensitive repositories.

The shared policy does not mandate one provider or model. Preserve a healthy existing provider configuration unless the user explicitly asks to change it. A validated environment may use a remote provider such as Z.AI, while another environment may use a different supported provider.

## OMO Slim and delegated work

Do not impose the retired Simple Memory single-writer protocol on OMO Slim.

Subagents should still return important discoveries to the coordinating agent as part of normal orchestration. The coordinating agent verifies material findings against repository evidence. Routine persistent-memory capture remains the memory plugin's responsibility unless an immediate manual memory operation is actually useful.

## Migration and failure behavior

The retired systems are:

- file-based `.opencode/history/` work journals;
- Simple Memory branch/worktree handoffs;
- project-local `.opencode/memory/` as the active memory store.

Do not recreate them when `opencode-mem` is unavailable.

Existing legacy Simple Memory data may be retained temporarily during migration or audit. Do not delete legacy data automatically merely because the new plugin is installed. First prove fresh-session persistence and relevant-memory injection in the replacement system; cleanup is a separate explicit action.

A meaningful `opencode-mem` validation should distinguish:

- plugin load;
- basic memory search/list/add behavior when exercised;
- persistence across a closed and fresh OpenCode session;
- automatic capture in a normal long-lived interactive session;
- relevant memory injection in a fresh session.

Configuration presence alone is not runtime proof.

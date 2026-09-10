# MCP access composition for OMO Slim

MCP server definitions live in OpenCode configuration. OMO's `mcps` fields select per-agent access; they do not install a binary or define an endpoint. This directory is separate from the existing Skill-only stack templates, so their validator/ownership is unchanged.

The `readonly-research.jsonc` fragment is only a candidate for a librarian that should research external docs and GitHub. Do not copy its array over a user's current array. Inspect user + project + active preset configuration, then make the smallest authorized change. Preserve intended `gh_grep` and custom MCP entries and all `!name` exclusions. A contradictory `name`/`!name` pair does not grant access; exclusion wins. An existing `[]` or `!*` is deliberate denial until the user approves a change. Do not normalize every agent to `*`.

Suggested roles, only after scope and availability are proven:

| Agent | Candidate access |
|---|---|
| Librarian | Existing Context7/docs, existing code search, optional GitHub read-only |
| Explorer | Serena navigation only after explicit pilot opt-in; no memory/shell/edit tools |
| Fixer | Native edits/CLI by default; Serena navigation only for a demonstrated need |
| Designer | Playwright only for an explicitly selected browser task and isolated test target |
| Orchestrator/Oracle/others | Preserve existing policy; do not broaden access merely because a server was installed |

Root `agents` vs preset behavior and `/preset` switching must be verified against the installed OMO version. Examples are not a custom merge algorithm. Re-run a delegated read after restart and after a preset switch when used. Check effective OpenCode permissions as well as OMO allowlists; either layer may prevent access. Routing is not an OS security boundary.

Baseline installation must not silently make Serena/Playwright available to wildcard agents. Keep those servers disabled until selected, review explicit exclusions for agents that must not use them, and apply tool-level ask/deny rules based on the actual exposed prefixed tool names. CLI utilities need no `mcps` entries. Keep model/variant/prompt/multiplexer/companion settings unchanged.

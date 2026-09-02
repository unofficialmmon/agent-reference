# AGENTS.md

Keep this file factual and project-specific. Global personal defaults may live in `~/.config/opencode/AGENTS.md`, `~/.config/opencode/ENGINEERING.md`, and `~/.config/opencode/MEMORY.md`; do not duplicate them here.

## Project summary

- Purpose: `<what this repository/application does>`
- Stack: `<languages/frameworks/build tools>`
- Main modules: `<important modules/packages>`
- Architecture: `<short boundary/flow description>`
- Key docs: `<authoritative architecture/product/API docs>`

## Authority

Use this order when sources conflict:

1. explicit user instruction;
2. this project `AGENTS.md`;
3. authoritative project contracts/specifications;
4. maintained source, tests, schemas, build/configuration;
5. project-local Skills/conventions;
6. global engineering defaults and global Skills.

Injected or recalled memory is contextual evidence only. It may explain prior work, but it never outranks the authorities above and must be reconciled with the current repository before it drives a material change.

List any project document that must be read before substantive changes:

- `<path>` — `<why/when>`

Do not treat deleted, generated, archived, or example source as current architecture authority unless this file explicitly says otherwise. Treat code indexes/search databases as navigation aids and confirm important claims against current files. If this document conflicts with maintained contracts or source, investigate and update the stale authority rather than hiding the mismatch.

## Repository and ownership boundaries

- Writable repository/worktree: `<scope>`
- Read-only sibling/shared repositories: `<paths and purpose>`
- Generated/tool-owned paths: `<paths and owner/generator>`
- Human-owned implementation paths: `<paths if useful>`
- Files/directories that must not be changed: `<paths>`

## Architecture and project conventions

Document only rules that are genuinely specific to this project, for example:

- package/module ownership;
- allowed dependency direction;
- controller/service/persistence boundary;
- IPC/process boundaries;
- shared/common ownership;
- naming that differs from common ecosystem defaults.

Do not copy generic language/framework documentation here; use the relevant Skill instead.

## Contracts

Record concrete contracts that changes must preserve or intentionally update:

- HTTP/API/OpenAPI: `<authoritative path or none>`
- DB/schema/migrations: `<authority>`
- IPC/events/messages: `<authority>`
- auth/security boundary: `<authority>`
- generated code: `<contract/config -> generator command>`

For HTTP/OpenAPI changes, use the `api-contract` Skill when it is installed/selected and relevant.
For generator-owned source, use the `generated-code` Skill when it is installed/selected and relevant.

## Skills

List only project-specific routing or overrides. Prefer selecting maintained Skills from the shared `agent-reference` catalog instead of rewriting generic technology guidance in this file. Install them globally or project-locally according to the actual project need.

Examples:

- `<skill-name>` — use for `<project-specific trigger>`.

Do not load every Skill at startup.

## Spec Kit

If this repository uses Spec Kit:

- `.specify/` is owned by Spec Kit;
- use `/speckit.*` for features intentionally following the Spec Kit workflow;
- current project contracts/source and explicit user requirements still remain authoritative;
- do not start Spec Kit automatically for unrelated routine fixes.

## Testing

Record only the testing topology, executable evidence, commands, and prerequisites that actually exist in this project.

- Static evidence: `<command/scope>`
- Unit evidence: `<command/scope>`
- Integration evidence: `<real boundaries and command/evidence>`
- Contract evidence: `<authority/command/evidence or N/A reason>`
- Component evidence: `<deployables and command/evidence>`
- System evidence: `<multi-service topology and command/evidence>`
- E2E Critical Journeys: `<small representative list and command/evidence>`
- Endpoint completeness: `<API authority/scope/command or not required>`
- Schema/test-data authority: `<migrations/DDL/seed paths>`
- System/E2E prerequisites: `<images, local-only seeds, runtime requirements>`

If the same executable test provides evidence for more than one responsibility, record the factual overlap rather than creating an artificial duplicate suite.

## Validation

Use the repository's real commands. Replace this table with the project commands that actually exist.

| Change | Validation |
|---|---|
| format/lint | `<command>` |
| compile/typecheck | `<command>` |
| focused tests | `<command>` |
| full tests | `<command>` |
| build/package | `<command>` |
| API/contract | `<command>` |

Never claim a check passed unless it was actually run successfully.

## Project-specific prohibitions

List only concrete hazards, for example:

- `<do not edit generated files directly>`
- `<do not cross a process/security boundary>`
- `<do not change public contract X without explicit intent>`

Do not turn this section into a generic engineering checklist.

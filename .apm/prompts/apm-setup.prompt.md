# `apm-setup`

**Description:** Set up Microsoft APM and migrate this project to agent-reference APM management

Adopt the current Microsoft APM package-management workflow for this existing
repository, using `unofficialmmon/agent-reference` as the reviewed source for
selected Skills. This is one bounded configuration/deployment-only task. Do not modify application source, business logic, tests, schemas, migrations,
generated application output, or unrelated deployment configuration. Do not
build an installer, custom manifest engine, runtime, orchestration layer, or
parallel workflow engine.

## Non-negotiable first steps and authority

1. Your first action must be:

   ```bash
   git status --short
   ```

2. Read the current project-root `AGENTS.md` before inspecting or changing
   anything else. If it is absent, record that fact; do not create or alter it
   as part of this command.
3. Apply this authority order:

   1. explicit user request and this prompt;
   2. project-root `AGENTS.md` and authoritative repository contracts;
   3. maintained source, build/package configuration, modules, ownership,
      schemas, tests, and project documentation;
   4. the installed APM version's supported schema, commands, and docs;
   5. installed OpenCode, OMO Slim, and Spec Kit configuration and native
      diagnostics;
   6. the resolved, pinned `unofficialmmon/agent-reference` revision,
      catalog, and relevant definitions;
   7. generic or global guidance.

Preserve all dirty work. Never overwrite an overlapping user change. Do not
run `git add`, `git commit`, `git push`, `git stash`, `git reset`, `git clean`,
`checkout --`, or application deployment commands. Treat sibling repositories
as read-only. Never use a force or destructive operation to make adoption pass.

## Existing APM adoption and safe stop conditions

This command is for initial adoption of an existing project, not for cosmetic
rewriting. Detect whether APM is already correctly managing this repository by
checking its supported manifest/lock/metadata, ownership, selected content,
and current diagnostics. If it is already correct, make no cosmetic rewrite;
validate what is safely available and report the adoption result as exactly `NOOP`
(uppercase, with no punctuation). Include the future `/agent-sync`
update path in that report.

If the APM CLI, its supported schema, the reference source, or a safe
non-overwriting operation is unavailable, continue only with safe read-only
inspection. Mark the affected work `BLOCKED` or `NOT RUN` honestly, preserve
manual Skills and existing configuration, and do not approximate APM behavior
with hand-written tooling.

## Inspect before selecting or writing

Inspect only enough to establish, from current files and commands:

- stack, runtime, build/package manager, build and validation commands;
- modules, source roots, generated-content boundaries, and ownership;
- current APM files and whether each is managed, dirty, unowned, or unknown;
- both applicable OpenCode Skill roots (`.opencode/skills/` and
  `$OPENCODE_CONFIG_DIR/skills/`, or the platform default such as
  `~/.config/opencode/skills/`) and the active discovery root, honoring
  `OPENCODE_CONFIG_DIR` and platform defaults;
- OpenCode commands and their origins, including `/agent-sync` if present;
- both OMO Slim JSON and JSONC candidates at applicable project/global paths,
  their current schema, and actual precedence (when both project candidates
  exist, account for the supported JSONC-over-JSON precedence rather than
  creating a third file);
- Spec Kit presence, integration, managed files, and constitution state;
- every installed and routed Skill ID visible in the inspected roots, its
  origin, source/revision, hash where available, and ownership.

Never assume that every installed or discoverable Skill came from
`agent-reference`. A catalog entry is not activation permission. Resolve the
current revision of `unofficialmmon/agent-reference` (for example, inspect the
configured remote and resolve its current commit without guessing), then
inspect `catalog/skills.lock.json` and the relevant complete Skill definitions
at that revision. Select only Skills directly supported by repository
evidence. Do not select `all`, wildcard, invented, or operational Skills
without explicit task-specific authorization. Do not manually reconstruct a
Skill: use a complete reviewed directory and preserve its references, assets,
scripts, and license/attribution files byte-for-byte.

## APM version and installation

Run:

```bash
apm --version
```

Use the installed version as-is; do not upgrade it, its plugins, or presets.
If APM is absent, use only the official Microsoft installation instructions
for the current platform and package. Do not install an unverified package,
copy a binary, or substitute another package manager. If official provenance
or a safe install cannot be established, stop mutation and report APM
installation `BLOCKED`.

Use the current installed APM documentation/schema to create or merge the
current supported OpenCode-targeted `apm.yml`. Preserve unrelated and
unowned configuration; do not rewrite an existing manifest merely to change
formatting or ordering. The APM-generated lock file must be produced by APM,
not hand-authored. Do not manage the whole `agent-reference` catalog: include
only the evidence-backed, explicitly selected Skills.

## Mutation checkpoint

Before the first write, show a concise checkpoint naming every planned APM
target, at minimum `apm.yml` and `apm.lock` (or the installed APM version's
documented lock filename), plus any selected
Skill directories or other APM-managed files. State whether each target is
new, managed, unmodified, dirty, overlapping, or unowned. Preserve anything
outside the listed ownership boundary.

Stop and request one concise confirmation before writing if a target overlaps
dirty work, would overwrite a modified or unknown file, would materially
rewrite an existing project configuration, or would overwrite or remove an
existing same-ID Skill. If there is no conflict, proceed after recording the
checkpoint.

Use the installed APM version's supported dry-run form for the proposed
install; do not invent flags. Review its result, then run the normal:

```bash
apm install
```

If dry-run or normal installation fails, preserve the old manual Skills and
existing files; do not delete or partially reconstruct them to force success.

## Manual Skill migration and routing boundaries

Before removing any manual copy, compare its origin, complete-directory hash
or recorded file hashes, revision, and ownership with the selected APM
content. Delete a manual copy only after successful replacement and verified
post-install discovery, and only when it is an unchanged, confirmed
superseded copy. Never remove a modified, project-authored,
differently-sourced, or unknown copy. Preserve uncertain copies and list them
in the report. Check for duplicate Skill IDs across all inspected discovery
roots before and after installation; do not silently resolve a duplicate by
deletion.

Preserve OMO models, variants, MCP servers, companion settings, permissions,
prompts, custom agents, and unrelated routing. Verify every routed Skill ID is
discoverable after installation. Repair routing only for an unambiguous
APM-caused break, and never add, route, or enable an operational Skill without
explicit authorization. Do not duplicate OMO-bundled Skills into the project.
Preserve the project `AGENTS.md`, Spec Kit files, integration, and constitution;
do not convert their ownership to APM. Preserve `.opencode/history/` as
handoff state and, when the active `HISTORY.md` rules require it, update the
normal history handoff for this qualifying change. Do not replace history with
a custom tracking mechanism.

Verify whether `/agent-sync` is available from the current package and
discovery roots. If it is absent, do not create a duplicate command; emit this
exact text:

```text
agent-sync: NOT AVAILABLE FROM CURRENT PACKAGE
```

Always state the future update path as `/agent-sync` when it is available, or
as the future package-provided `/agent-sync` path when it is not currently
available. Do not implement an agent-sync replacement in this command.

## Required validation

Attempt these minimum actual checks in the appropriate order, after mutation
where applicable:

```bash
apm --version
apm install
apm audit
git diff --check
git status --short
```

If a prerequisite prevents a command, label it `BLOCKED` rather than claiming
success. Also validate, with explicit `PASS`, `FAIL`, `BLOCKED`, or `NOT RUN`
labels:

- `apm.yml` against the installed APM schema, and generated lock consistency;
- manifest/lock selected IDs, provenance, hashes, and ownership;
- Skill ID uniqueness across inspected roots and post-install discovery;
- every OMO JSON/JSONC candidate's parse/schema/precedence behavior and every
  routed ID's discoverability, with no unauthorized operational routing;
- Spec Kit and `AGENTS.md` preservation;
- that no application source, tests, schemas, migrations, generated output,
  upstream Skill snapshot, or unrelated configuration changed;
- `/agent-sync` availability and the exact unavailable message when required.

Review the final diff and status. Never turn a skipped, unavailable, or failed
check into a warning-free success claim.

## Final report

Keep the final report restricted to these headings and facts:

1. **Stack** — discovered stack and relevant commands.
2. **APM/version** — installed/official-install status and version.
3. **Selected Skills** — evidence, origins, and exclusions.
4. **Manifest/lock** — paths, ownership, and validation.
5. **Manual migrations** — removed unchanged superseded copies and preserved
   uncertain/manual Skills.
6. **OMO** — files/precedence, preserved settings, routed-ID status, and any
   narrowly repaired APM-caused break.
7. **Spec Kit** — preserved state and status.
8. **agent-sync** — availability, required exact message if absent, and the
   future `/agent-sync` update path.
9. **History** — `.opencode/history/` preservation and normal handoff status.
10. **Validations** — every required check with `PASS`, `FAIL`, `BLOCKED`, or
    `NOT RUN`.
11. **Changed files** — exact paths only.
12. **Status** — adoption status, including exact `NOOP` for an already-correct
    setup and any unresolved conflict.

Do not report unrelated repository details. Do not call the setup complete
when any required step is `FAIL`, `BLOCKED`, or `NOT RUN`.

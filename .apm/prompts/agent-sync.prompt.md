# `agent-sync`

**Description:** Update agent-reference APM dependencies and reconcile project agent configuration

Perform routine maintenance for an existing, correctly adopted Microsoft APM
project. Run this only after `/apm-setup`; in this repository, the setup
prompt file and indexed command are named `apm-setup`. This prompt has one
bounded responsibility: update agent-reference APM dependencies and reconcile
their project agent configuration. It is configuration/deployment-only, not
application-source work. Do not install APM, perform first-time migration,
build an installer, edit generated deployments by hand, or create a hidden runtime,
orchestration layer, or parallel workflow engine.

## Preconditions, first steps, and safety

1. Your first action must be:

   ```bash
   git status --short
   ```

2. Read the current project-root `AGENTS.md` before any further inspection or
   mutation. If it is absent, record that fact and continue read-only; do not
   create it in this sync.
3. Preserve dirty work, user files, project-authored files, and sibling
   repository boundaries. Never overwrite an overlapping dirty change or use a
   force operation to make sync pass.
4. Do not stage, commit, push, reset, clean, or stash, and do not run
   application deployment commands. In particular,
   do not run `git add`, `git commit`, `git push`, `git reset`, `git clean`,
   `git stash`, `checkout --`, or equivalent destructive commands.

First establish that a correct existing APM management setup is present:
`apm.yml` must be the current supported OpenCode-targeted manifest for this
project, its generated `apm.lock.yaml` (or the current installed APM's
documented lock filename) must be present and coherent, and the manifest,
lock, ownership, and installed content must identify the adopted
`agent-reference` dependencies. If that setup is absent, incomplete, or not
correct, stop without installing APM or migrating anything and recommend
exactly:

```text
/apm-setup
```

Do not perform first-time migration during sync. The only permitted repair
before normal synchronization is a trivial missing generated artifact when the
existing manifest, lock ownership, and installed state clearly prove that APM
adoption is already complete and the repair cannot change dependency selection
or overwrite user/project content. Otherwise use `/apm-setup`.

If APM is not available, report the exact text `APM: BLOCKED`, recommend
exactly `/apm-setup`, and perform only safe read-only inspection. Never
install APM during sync.

## Inspect the current state

After the required status and `AGENTS.md` read, inspect only enough to verify:

- `apm.yml`, the generated `apm.lock.yaml` (or the installed APM-documented
  lock filename), APM ownership,
  selected dependency revisions, and whether either file is dirty, modified,
  unowned, or unknown;
- APM-managed Skill roots, manual/local Skill roots, project and user/global
  OpenCode discovery roots, and the active discovery root, honoring
  `OPENCODE_CONFIG_DIR` and platform defaults;
- all installed and routed Skill IDs, origins, revisions, hashes where
  available, ownership, and duplicate IDs;
- both applicable OMO Slim candidates,
  `.opencode/oh-my-opencode-slim.json` and `.opencode/oh-my-opencode-slim.jsonc`
  (and effective global candidates where applicable), including supported
  JSON/JSONC precedence;
- Spec Kit integration, managed files, and constitution state;
- relevant project agent commands and configuration without treating every
  discoverable Skill as an `agent-reference` dependency.

Use current repository evidence and the installed tools' supported behavior;
do not invent a dependency, Skill, route, schema, or migration. Preserve
application source, tests, schemas, migrations, generated application output,
and unrelated configuration.

### Private GitHub source transport and package commands

When the adopted GitHub source is private, Git may be able to clone it through
an SSH host alias while APM's virtual-file HTTPS/raw download path cannot
resolve or use that alias. The supported dependency is one whole-repository SSH
source, restricted to the project's evidence-backed Skills:

```yaml
dependencies:
  - git: ssh://git@github.com/unofficialmmon/agent-reference.git
    ref: main
    skills:
      - <project-specific-skill-id>
```

Do not convert this to separate per-file virtual dependencies or guessed
HTTPS/raw URLs, and do not record local aliases or credentials. Preserve the
existing SSH configuration and authentication. The package's
`.apm/prompts/apm-setup.prompt.md` and `.apm/prompts/agent-sync.prompt.md` are
APM package content and their generated command deployment belongs under
`.opencode/commands/`. The lock file and generated deployment/command output
are APM-owned; never edit, copy, or reconstruct them by hand.

If a dependency update or command deployment cannot clone, fetch, or resolve
the source through its supported transport, report `BLOCKED`, preserve the last
healthy deployment, and do not hide the transport failure with a fallback or
partial deployment.

## Version and dependency update procedure

Run the installed CLI as-is:

```bash
apm --version
apm outdated
```

Do not upgrade APM, plugins, extensions, or presets. If `apm outdated` shows
that an `agent-reference` dependency is actually outdated, review the
proposed revisions and use the installed APM version's current supported
`apm update` form. Update only because the agent-reference dependency is
outdated; do not update merely to rewrite a lockfile, normalize formatting, or
refresh an already-current deployment. If only unrelated dependencies are
outdated, do not update them through this prompt.

Do not manually copy Skills, edit generated lockfiles, or edit generated APM
deployments. If the supported update is unavailable, unsafe, or fails,
preserve the prior healthy deployment and manual Skills, report the affected
work `BLOCKED` or `FAIL`, and do not improvise a replacement.

This sync does not run `apm install`. If a supported repair or deployment
operation is explicitly permitted by the current APM version, perform its
documented dry-run first and only continue when that dry-run succeeds.

Run this separately from `apm outdated` and separately from any update:

```bash
apm audit
```

An audit is required even when no dependency update is needed. Do not treat an
outdated report as an audit result.

## Mutation checkpoint and Skill reconciliation

Before the first write, show a concise checkpoint naming every intended
APM-managed target: `apm.yml`, the generated lock file, updated deployment or
Skill paths, and any configuration route that is genuinely in scope. State
which are APM-owned and whether each is new, unchanged, dirty, modified,
overlapping, or unowned. Do not write outside that list.

Stop and request one concise confirmation if a planned target overlaps dirty
work, would overwrite a user/project-modified or unknown file, or would require
changing an ownership boundary. With no such conflict, proceed using native
APM behavior only.

After a healthy supported APM replacement/update, reconcile discovery and
uniqueness. Remove a manual/local Skill only when all of these are true:

1. APM replacement succeeded;
2. the replacement is discoverable and healthy;
3. the old copy is confirmed unchanged and obsolete/superseded;
4. removal has no dirty-worktree overlap and does not remove a project-owned
   or user-owned file.

Compare origin, revision, complete-directory/file hashes, and ownership before
any removal. Preserve and report as `BLOCKED` any ambiguous, modified,
project-authored, differently sourced, or unknown copy. Never silently delete
duplicates; report duplicate IDs and resolve them only through an
unambiguous, authorized ownership decision. Do not manually reconstruct or
rewrite a Skill.

## Configuration preservation

Preserve OMO models, variants, MCP servers, companion settings, permissions,
prompts, custom agents, and unrelated routing. Verify every routed Skill ID
remains discoverable after sync. Repair routing only when a stale routed ID is
an actual, unambiguous consequence of this APM update. Never route or enable
operational Skills through sync, and never weaken permission gates.

Preserve `AGENTS.md` and Spec Kit integration, managed files, and constitution.
Inspect them only for real, evidence-backed drift caused by the dependency
update; do not apply generic rewrites, initialize/upgrade Spec Kit, or change
project instructions merely for style.

Preserve `.opencode/history/` completely as handoff state. If dependency or
agent-configuration state actually changes, update only the normal minimal
handoff history under the active `HISTORY.md` rules. A true `NOOP` must not
create meaningless history or alter existing history content.

## Validation

When an update occurred, run these checks after the update:

```bash
apm audit
git diff --check
git status --short
```

Also validate with explicit `PASS`, `FAIL`, `BLOCKED`, or `NOT RUN` labels:

- current `apm.yml` schema and generated lock consistency;
- selected dependency IDs, revisions/provenance, hashes, and ownership;
- APM-managed and manual Skill discovery, post-update uniqueness, and
  duplicate-ID handling;
- OMO JSON/JSONC parsing, precedence, preserved user modifications, routed-ID
  discoverability, and absence of operational routing;
- preserved `AGENTS.md` and Spec Kit state;
- no application source, tests, schemas, migrations, generated output, or
  unrelated project configuration changed;
- `apm outdated` and the separate `apm audit` result.
- package-provided prompt deployment into `.opencode/commands/`, with generated
  output treated as APM-owned.

If a prerequisite or unavailable tool prevents a check, mark it `BLOCKED` or
`NOT RUN`; never report it as passed. Review the final diff and status without
staging or committing anything.

## Final report

Keep the final report concise and restricted to these items:

1. **agent-reference** — `UPDATED` or `NOOP`; if current, the final line of
   the report must be exactly `NOOP`.
2. **Revisions** — previous and resulting dependency revisions.
3. **Skills** — added, updated, removed, and preserved/uncertain copies.
4. **Manifest/lock** — paths, ownership, and status.
5. **OMO** — precedence, preserved settings, routing status, and any repair.
6. **AGENTS** — preservation and real-drift status.
7. **Spec Kit** — preservation and status.
8. **History** — preservation and whether a normal handoff update was needed.
9. **`apm outdated`** — result and status.
10. **`apm audit`** — separate result and status.
11. **Other checks** — each result with `PASS`, `FAIL`, `BLOCKED`, or `NOT RUN`.
12. **Changed files** — exact paths only.
13. **Remaining issues** — conflicts, preserved uncertain copies, and any
    unverified scope; include the future `/agent-sync` path.

Do not call the sync complete when a required update or validation is `FAIL`,
`BLOCKED`, or `NOT RUN`. Do not add unrelated repository facts to the report.

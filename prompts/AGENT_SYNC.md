---
description: Update agent-reference APM dependencies and reconcile project agent configuration.
---

# agent-sync

Perform routine maintenance for a repository that has already adopted Microsoft APM and `unofficialmmon/agent-reference`.

This is configuration/deployment-only work. Do not modify application source, business logic, tests, schemas, migrations, generated application output, or unrelated user/global OpenCode configuration.

## Authority and safety

Start with:

```bash
git status --short
```

Then read the project-root `AGENTS.md` when present.

Use this priority:

1. explicit user instruction;
2. project `AGENTS.md` and authoritative project contracts;
3. maintained source, tests, schemas, build/configuration, and project docs;
4. the installed APM version's supported behavior;
5. current OpenCode/OMO Slim configuration and any existing optional Spec Kit state;
6. the resolved `agent-reference` revision, its APM producer surface, and selected catalog content;
7. generic guidance.

Preserve dirty work and ownership boundaries. Do not stage, commit, push, stash, reset, clean, force-update, or overwrite unrelated files.

## Preconditions

This command is only for an existing healthy APM adoption.

Confirm that the repository has a coherent current `apm.yml`, the installed APM version's generated lock file, and installed content identifying the adopted `agent-reference` dependency.

For every persisted selected Skill ID, also confirm that the resolved dependency revision exposes `.apm/skills/<id>/SKILL.md`. Catalog presence alone is not deployability.

If adoption is absent, incomplete, ambiguous, or damaged beyond a trivial generated-artifact repair, stop mutation and recommend exactly:

```text
/apm-setup
```

If APM itself is unavailable, report `APM: BLOCKED`, recommend `/apm-setup`, and continue read-only only.

## Inspect current state

Inspect only enough to establish:

- `apm.yml`, generated lock ownership, selected dependency revision, and dirty/modified state;
- persisted `dependencies.apm[*].skills` selections and whether those IDs are currently exposed under `.apm/skills/`;
- APM-managed and manual/local Skill roots plus user/project OpenCode discovery roots;
- installed/routed Skill IDs, physical origins, effective discovery winner, and same-ID content equality;
- applicable `.opencode/oh-my-opencode-slim.json` / `.jsonc` and effective global OMO configuration;
- Spec Kit state only when `.specify/` exists or an authoritative current project contract explicitly requires it; absence alone is not an agent-sync failure;
- package-provided command deployment under `.opencode/commands/`;
- whether any planned write overlaps dirty, unknown, or user-owned files.

`agent-reference` intentionally exposes non-operational catalog Skills under `.apm/skills/` and keeps `skills/operational/` catalog-only. Never auto-add operational IDs merely because they exist in the catalog.

Treat indexes, caches, generated search data, and recalled memory as navigation/context only. Confirm material claims against current repository evidence.

## Update procedure

Run:

```bash
apm --version
apm outdated
```

Do not upgrade APM, OpenCode, OMO Slim, plugins, models, providers, or unrelated dependencies through this command.

If `agent-reference` is actually outdated, review the proposed revision and use the installed APM version's supported `apm update` form. Update only the intended `agent-reference` dependency. Do not rewrite an already-current lock merely for formatting or freshness.

If the manifest needs inspection or narrow repair, the supported Git dependency shape is under `dependencies.apm`, for example:

```yaml
dependencies:
  apm:
    - git: ssh://git@github.com/unofficialmmon/agent-reference.git
      ref: main
      skills:
        - <project-specific-skill-id>
```

Do not flatten the APM dependency list directly under `dependencies:`. Preserve the existing supported source transport and authentication; do not replace working SSH with guessed raw URLs, local aliases, embedded credentials, or per-file reconstruction.

Run separately:

```bash
apm audit
```

An outdated check is not an audit result, and a pre-existing vendor finding is not deployment drift. If `apm audit` exits non-zero, report it as `FAIL` while classifying the finding separately.

The package producer surface is split deliberately:

- `.apm/prompts/*.prompt.md` -> APM-generated OpenCode commands under `.opencode/commands/`;
- selected `.apm/skills/<id>/...` -> APM-generated OpenCode Skill directories under `.agents/skills/<id>/` by the default OpenCode target mapping.

Generated target output and the generated lock are APM-owned; never hand-edit or reconstruct them.

## OpenCode discovery precedence and same-ID Skills

Validate the effective runtime winner, not only the APM deployment directory.

For current OpenCode discovery, a user-level `~/.config/opencode/skills/<id>` copy can take precedence over an APM-deployed project `.agents/skills/<id>` copy. Compare complete file inventories and content/hash before calling this a conflict.

Classify each selected same-ID situation as:

- `APM_EFFECTIVE` — no higher-precedence divergent copy masks the selected APM deployment;
- `SHADOWED_IDENTICAL` — a higher-precedence same-ID copy exists and is byte-identical to the APM-managed copy; preserve it unless separately proven safe and obsolete;
- `SHADOWED_DIVERGENT` — a higher-precedence same-ID copy differs; routed/discovery validation is `BLOCKED` until ownership is resolved.

Do not silently delete, overwrite, or edit a user/global Skill to force the APM copy to win. A selector plus one physical global Skill is not a physical duplicate by itself.

## Mutation checkpoint

Before the first write, state the exact APM-managed targets that may change and whether each is clean, dirty, modified, overlapping, or unowned.

Ask one concise confirmation only if the planned update would overwrite dirty/user-modified/unknown content or change an ownership boundary. Otherwise proceed with native APM behavior.

After a successful APM update, verify that every persisted selected ID is still exposed by the new producer revision and that APM deployed its complete Skill directory. If a selected ID disappears from `.apm/skills/`, mark it `BLOCKED`; do not silently remove the selection or OMO route.

Remove a superseded manual Skill copy only when its origin, revision/hash, complete contents, precedence, ownership, and unchanged state prove that removal is safe. Preserve ambiguous or modified copies and report them instead of deleting them.

Preserve OMO models, variants, MCPs, companion settings, permissions, prompts, custom agents, and unrelated routing. Repair only an unambiguous APM-caused routed-Skill break. Never auto-route operational Skills.

Preserve project `AGENTS.md` and any existing Spec Kit state unless a concrete APM-caused drift requires a narrow repair. Do not install or restore Spec Kit merely because `.specify/` is absent. If a current authoritative project contract still requires Spec Kit while its artifacts are absent, report that as a separate project-contract inconsistency, not as an APM update failure.

## Memory boundary

APM does not own project memory.

Current persistent memory is `opencode-mem`, whose normal workflow is automatic capture and relevant later-session injection. Therefore this sync must:

- not create or restore `.opencode/history/`;
- not create or restore Simple Memory `.opencode/memory/` state;
- not modify `opencode-mem` configuration or its local storage merely because APM content changed;
- not require `remember`, `recall`, branch handoffs, or an end-of-task manual handoff;
- treat any injected/recalled memory as contextual evidence only, subordinate to current Git/source/config/contracts/tests.

A true `NOOP` must not create synthetic memory or tracking state.

## Validation

When an update occurred, run:

```bash
apm audit
git diff --check
git status --short
```

Also verify, with `PASS`, `FAIL`, `BLOCKED`, or `NOT RUN`:

- manifest/schema and generated-lock consistency;
- selected dependency revision/provenance/ownership;
- every persisted selected ID exists under the resolved `.apm/skills/` producer surface;
- every selected Skill is deployed completely to the APM target Skill root;
- effective OpenCode discovery classification: `APM_EFFECTIVE`, `SHADOWED_IDENTICAL`, or `SHADOWED_DIVERGENT`;
- OMO JSON/JSONC parsing, precedence, preserved user settings, and routed-ID effective discoverability;
- project `AGENTS.md` preservation and, only when present or explicitly required, Spec Kit preservation/state;
- package prompt deployment under `.opencode/commands/`;
- absence of unrelated application/config changes;
- absence of newly created legacy History or Simple Memory runtime state;
- `apm outdated` and `apm audit` as separate results.

Never convert a skipped, blocked, or failed check into a pass. Do not mutate third-party vendor dependencies or invent an ignore/baseline mechanism merely to make `apm audit` green.

## Completion boundary

The sync command has one user-interaction checkpoint: the pre-mutation confirmation above when ownership or dirty-content risk actually requires it.

After the sync attempt and validation are complete:

- do not open a follow-up selector, confirmation menu, or multi-choice prompt;
- do not ask whether the user wants optional cleanup, vendor remediation, global-Skill reconciliation, or Spec Kit work;
- report unresolved items under `Needs attention` and stop;
- let the user request a separate follow-up task if they want one.

A finished sync must end as a finished report, not as a new interactive workflow.

## Final report

Optimize the report for human review rather than reproducing the internal validation checklist. Normal preserved state is omitted unless it changed or failed.

Use these status values:

- `UPDATED` — the dependency revision changed and the intended APM deployment completed without a remaining material issue affecting effective selected-Skill use or required policy enforcement;
- `UPDATED_WITH_ISSUES` — the revision/deployment updated, but a material issue remains, such as `SHADOWED_DIVERGENT`, failed audit, or unavailable required policy enforcement;
- `NOOP` — no dependency/configuration change was needed and required selected Skills are healthy/effectively discoverable;
- `NOOP_WITH_ISSUES` — no update was needed, but a material unresolved issue remains;
- `BLOCKED` — the sync itself could not be completed safely.

Use this compact structure:

```text
## Result
<STATUS> — agent-reference <previous> → <resulting revision>
<one sentence stating what was actually updated or why no update was needed>

## Changed
- <only when files changed: exact APM-managed path/group and what changed>
- <group repetitive Skill paths by count or IDs instead of one line per file>

## Needs attention
- <only material unresolved items; omit this section when empty>

## Validation
- PASS|FAIL|BLOCKED|NOT RUN `<command or check>` — <useful result>
```

Reporting rules:

- name concrete changed paths when an update occurred;
- state the effective runtime winner for every `SHADOWED_DIVERGENT` Skill and its higher-precedence path;
- summarize `SHADOWED_IDENTICAL` counts compactly unless the identities are needed to understand an issue;
- keep `apm audit` separate from deployment drift and say when a failure is confined to third-party/vendor content;
- if organization policy could not be fetched and the update proceeded without enforcement, report that prominently under `Needs attention` or validation;
- absence of `.specify/` is not a failure by itself; mention Spec Kit only when existing artifacts changed or a current authoritative project contract conflicts with its absence;
- omit routine facts such as “OMO preserved”, “Memory preserved”, or “AGENTS.md preserved” when nothing happened to them;
- do not emit a numbered 1–13 checklist;
- do not end with offers, optional-action menus, or follow-up questions.

For a clean `NOOP`, keep the report especially short and end with exactly:

```text
NOOP
```

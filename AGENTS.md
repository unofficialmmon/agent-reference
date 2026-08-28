# agent-reference maintenance rules

This repository is a static source collection for OpenCode references, bounded convenience prompts, Skills, and maintainer-only validation artifacts. It is not a runtime, installer, workflow engine, or orchestration layer.

## Priority

1. Explicit user instruction.
2. This file.
3. Source provenance recorded in `catalog/skills.lock.json` and `catalog/SOURCES.md`.
4. Existing repository structure and validation rules.

## Upstream snapshot policy

- Never edit an upstream Skill snapshot in place.
- Upgrade an upstream Skill by replacing the whole snapshot with a reviewed pinned revision.
- Preserve upstream license files and attribution.
- Update source revision, file hashes, known issues, compatibility status, and operational-risk metadata together.
- If local behavior is needed, create a distinct local Skill ID instead of silently forking upstream content.
- Do not describe a Skill as locally behavior-validated unless a recorded behavior test actually exists.

## Catalog is not activation

A Skill being present under `skills/` means it is available for selection, not globally enabled.

- Default global active Skill set is zero.
- Keep technology Skills grouped by domain.
- Keep Skills with deployment, credentials, browser automation, process execution, local-server automation, profiling, destructive operations, or significant tool dependencies under `skills/operational/`.
- Do not move an operational Skill into an ordinary technology group merely because it is popular or official.

## Local Skills

Keep local Skills narrow and evidence-based. Current local Skills exist only for gaps not adequately covered by a reviewed upstream source:

- `api-contract`
- `generated-code`
- `java-style`

Before adding another local Skill, check whether a maintained upstream/vendor Skill already solves the same problem.

## Document quality

- Give each reference or prompt one clear responsibility.
- State whether a prompt is read-only, configuration-only, or allowed to modify source.
- Use concrete stop conditions, mutation checkpoints, and output requirements instead of vague completeness language.
- Remove duplicated guidance when OpenCode, OMO Slim, Spec Kit, an upstream Skill, or another document already owns it.
- Keep global references compact and preserve safety/ownership boundaries when compressing prose.

## Global documents

Keep `global/AGENTS.md` short. It routes to references; it must not become another development framework.

Keep `global/ENGINEERING.md` compact and principle-oriented. Do not add long technology-specific sections; put those in Skills or project rules.

Keep `global/HISTORY.md` opt-in and inactive at startup.

## Project template

`project/AGENTS.template.md` must contain project facts, authorities, ownership, contracts, validation commands, and project-specific hazards only. Do not duplicate generic framework documentation or global engineering philosophy into every project.


## OMO Slim templates

Keep project-local OMO Slim examples under `templates/omo/` as non-authoritative composition aids.

- Examples must contain only project-local Skill routing, not user-specific models, credentials, MCP endpoints, companion state, or full global configuration.
- Use current OMO Slim schema/configuration semantics as authority.
- Make conditional Skills obvious in `ROUTING.md`; do not encode every optional technology into a broad default template.
- Never auto-route operational Skills.
- Template examples must remain valid JSONC and must not require a custom renderer or installer.

## Prompts

Keep reusable prompts under `prompts/` as plain Markdown. They may coordinate existing native tools, but they must not become a hidden runtime or parallel workflow engine.

- Prefer one bounded prompt for repetitive setup tasks over duplicating the same checklist across project `AGENTS.md` files.
- Delegate to upstream/native tool workflows when they already exist instead of rewriting them.
- Project bootstrap/refresh prompts must preserve dirty user work, avoid application-source edits unless explicitly in scope, and report blocked/not-run steps rather than masking them.
- A convenience prompt must not bypass a destructive or overwrite confirmation merely to remain one-shot; require one concise checkpoint when an existing dirty/managed path is at risk.
- `PROJECT_AUDIT.md`, `CODEBASE_ONBOARD.md`, and `CHANGE_AUDIT.md` are read-only by default; do not let convenience prompts silently become mutation workflows.
- Keep the prompt set small. Prefer an upstream Skill or Spec Kit command when it already owns a task-specific workflow.
- Keep APM concerns separate: prompts define desired setup behavior; APM may distribute them later.

## Validation before release

Start with the deterministic maintainer audit:

```bash
python3 tools/audit.py
```

Then review its warnings and complete the host-specific evidence in `evaluation/README.md` when the changed surface requires it.

Before packaging a revision:

1. validate all Skill frontmatter and unique IDs;
2. verify file hashes in `catalog/skills.lock.json`;
3. confirm every upstream snapshot still matches its recorded bytes;
4. scan Markdown relative links and record unresolved upstream references instead of patching them silently;
5. syntax-check bundled executable scripts where practical;
6. confirm operational Skills are isolated;
7. verify root `LICENSE`, `NOTICE`, and `catalog/LICENSES/` attribution coverage;
8. review prompt mutability, stop conditions, command validity, OMO routing boundaries, and responsibility overlap;
9. parse/validate OMO JSONC examples and confirm every referenced Skill ID exists in the catalog or OMO built-ins as intended;
10. check that README installation guidance is non-destructive;
11. run an OpenCode discovery/trigger smoke test when OpenCode is available; otherwise report it as not run;
12. confirm workflow-style Skills and prompts have explicit activation boundaries and do not silently replace OMO Slim or Spec Kit behavior;
13. distinguish deterministic static PASS from OpenCode/OMO behavioral PASS and update evaluation evidence honestly.

Do not add a custom installer, manifest engine, migration system, or agent runtime to solve distribution. Distribution is expected to be handled later by APM or another established package manager.

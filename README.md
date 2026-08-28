# agent-reference

Static, curated engineering references, bounded convenience prompts, and hash-pinned Agent Skill snapshots for OpenCode projects.

`agent-reference` is deliberately **not** a framework. It has no runtime, daemon, workflow engine, custom orchestrator, stack detector, installer, migration system, or generated project state.

```text
OpenCode        harness, AGENTS.md, native Skill discovery
OMO Slim        orchestration
Spec Kit        explicit specification workflow
agent-reference shared reference source
APM             later: multi-project distribution only
```

## Core rule

**Catalog inclusion is not activation.**

The default global active Skill count is **zero**. Install only the Skills relevant to a real project or an explicit task. This keeps ambient metadata small and prevents unrelated technology or methodology guidance from influencing work.

## Quick start

Apply the pack incrementally.

1. Diff/merge `global/AGENTS.md` into `~/.config/opencode/AGENTS.md`; never overwrite an existing personal file blindly.
2. Copy `global/ENGINEERING.md` and `global/HISTORY.md` only after checking for existing files with those names.
3. Start with zero global Skills. Install technology Skills project-locally unless they are genuinely useful across most repositories.
4. Create/refine the project `AGENTS.md` manually or explicitly run `prompts/PROJECT_BOOTSTRAP.md`. Bootstrap can also install selected project Skills and create the minimal project-local OMO Slim Skill-routing override.
5. Restart OpenCode after Skill/routing changes before checking discovery.

Example bootstrap request:

```text
Read /path/to/agent-reference/prompts/PROJECT_BOOTSTRAP.md and execute it for the current repository.
Do not modify application source during bootstrap.
```

Run three small smoke checks before relying on the setup:

```text
1. Injection: summarize currently injected global rules without reading files.
2. Non-interference: perform one typo-only/mechanical change and confirm no planning ceremony or unrelated edit.
3. Project priority: request a small project-specific implementation and confirm project ownership/conventions override generic guidance.
```

Optionally install one selected non-operational Skill project-locally and invoke it explicitly to confirm discovery. A smoke PASS proves basic loading/behavior only; it does not certify every Skill, model, or future host version.

### Observed local smoke evidence

A prior local run on OpenCode `1.18.24` with OMO Slim `2.2.17` observed:

- global rule injection;
- non-interference on a typo-only edit;
- project-rule priority and clarification before inventing an unsupported domain;
- discovery/loading of the project-local `java-style` Skill.

These observations are limited compatibility evidence, not certification of every prompt, Skill, model, or repository. Re-run the small smoke sequence after changing host versions or the selected reference set.

## Layout

```text
agent-reference/
├── AGENTS.md                     repository-maintenance rules
├── README.md
├── CHANGELOG.md
├── LICENSE
├── NOTICE
├── global/
│   ├── AGENTS.md                 small OpenCode global router
│   ├── ENGINEERING.md            conditional engineering reference
│   └── HISTORY.md                opt-in work-history protocol
├── project/
│   └── AGENTS.template.md        factual project entry-point template
├── evaluation/
│   ├── README.md                 static-vs-behavioral evaluation guide
│   └── agentrc.eval.jsonc        optional cross-agent AgentRC cases
├── tools/
│   ├── audit.py                  deterministic maintainer-only static audit
│   └── README.md
├── templates/
│   └── omo/                      project-local OMO Skill-routing examples
├── prompts/
│   ├── README.md                 copy-paste entry-point index
│   ├── PROJECT_BOOTSTRAP.md
│   ├── PROJECT_REFRESH.md
│   ├── PROJECT_AUDIT.md
│   ├── CODEBASE_ONBOARD.md
│   └── CHANGE_AUDIT.md
├── skills/
│   ├── core/
│   ├── engineering/
│   ├── java-spring/
│   ├── frontend/
│   ├── react/
│   ├── vue-nuxt/
│   ├── database/
│   ├── infrastructure/
│   ├── mobile/
│   └── operational/
└── catalog/
    ├── SOURCES.md
    ├── skills.lock.json
    └── LICENSES/
```

## Global references

Recommended OpenCode global files:

```text
~/.config/opencode/
├── AGENTS.md
├── ENGINEERING.md
└── HISTORY.md
```

- `AGENTS.md` is the short router, priority, scope, safety, and validation baseline.
- `ENGINEERING.md` is conditional. Load it for architecture/design review, unclear root-cause debugging, refactoring, meaningful cross-boundary work, security/reliability/performance decisions, and structural review—not for every small edit.
- `HISTORY.md` is opt-in and inactive by default.

Do not duplicate these documents into every repository.

## Skill catalog

Skills remain source catalog content until copied to an OpenCode discovery root.

### Core

- `api-contract` — HTTP/OpenAPI authority, wire compatibility, breaking changes, and layered validation.
- `generated-code` — generator ownership, safe regeneration, and generated-vs-human boundaries.

### Java/Spring

- `spring-boot`
- `spring-security`
- `maven-build`
- `mybatis`
- `mybatis-dynamic-sql`
- `mybatis-generator`
- `java-style`

### Engineering workflows

These are explicit-use workflows, not ambient defaults:

- `bug-reproduction-brief` — reproduction-only; intentionally stops before diagnosis/repair.
- `refactor-plan` — plan-only for multi-file refactors; waits for confirmation and contains stack-specific examples that must be adapted.
- `verification-before-completion` — completion gate; fresh output is necessary, but the chosen instrument must actually cover the claim.

See `catalog/skills.lock.json` for activation guidance, provenance, limitations, and risk metadata.

### Other technology groups

The catalog also retains reviewed frontend/React/Vue, database, infrastructure, mobile, and vendor-maintained snapshots. Select them only for relevant projects.

### Operational Skills

`skills/operational/` may involve scripts, browser/profile access, local servers, MCP/tool dependencies, credentials, deployment, migrations, profiling, source rewriting, or resource creation/deletion.

They require explicit selection and review. Where useful, configure OpenCode `permission.skill` as `ask` or `deny` for operational IDs. Presence in the catalog is never permission to execute their actions.

## Installing selected Skills

Project-local installation is the safer default:

```bash
mkdir -p <repo>/.opencode/skills
cp -R skills/core/api-contract <repo>/.opencode/skills/api-contract
cp -R skills/java-spring/spring-boot <repo>/.opencode/skills/spring-boot
```

Global installation is appropriate only for Skills used across most repositories:

```bash
mkdir -p ~/.config/opencode/skills
cp -R skills/core/generated-code ~/.config/opencode/skills/generated-code
```

Before copying, inspect all visible OpenCode Skill roots for the same ID. Do not overwrite another version or edit a reviewed upstream snapshot in place.

## OMO Slim project-local routing

Keep user-level OMO Slim configuration generic (models, variants, MCPs, companion, normal global agent policy). Project repositories should contain only the smallest routing differences they actually need.

Because project-local OMO configuration is auto-loaded and can change agent behavior, tools, and Skill access, treat `.opencode/oh-my-opencode-slim.json[c]` as trusted executable configuration. Review it before opening an unfamiliar repository with OMO Slim.

`templates/omo/` contains reviewed **examples**, not blindly installable profiles:

- `ROUTING.md` — evidence-based agent/stack candidate map;
- `java-spring.jsonc`;
- `java-spring-mybatis.jsonc`;
- `java-spring-mybatis-mbg.jsonc`;
- `react-vite.jsonc`;
- `nextjs-react.jsonc`;
- `vue-vite.jsonc`;
- `nuxt.jsonc`;
- `react-native.jsonc`.

The examples use root `agents.<agent>.skills` overrides rather than a named preset so project stack routing stays separate from user-owned models, variants, MCPs, and companion settings. At startup, current OMO config-file merging gives root agent entries precedence over the selected preset. Runtime `/preset` switching has separate merge behavior, so projects that depend on preset switching must verify routing after a switch or deliberately maintain preset-local routing. If a project already has an OMO config, merge into its existing format rather than creating a competing `.json`/`.jsonc` pair.

Default routing principle: leave Orchestrator, Explorer, Librarian, and Oracle alone unless the repository has a concrete reason to override them; route proven implementation Skills to Fixer and proven UI Skills to Designer. Use preset-local routing only for a deliberate preset-specific difference. Operational Skills are never automatic.

## Convenience prompts

The prompt set is intentionally small and explicit. `prompts/README.md` provides copy-paste entry requests so users do not need to remember the exact wording:

- `PROJECT_BOOTSTRAP.md` — onboarding and initial project agent setup.
- `PROJECT_REFRESH.md` — reconcile stale project guidance, selected Skills, and Spec Kit integration.
- `PROJECT_AUDIT.md` — read-only health check of agent-facing configuration.
- `CODEBASE_ONBOARD.md` — read-only map of an unfamiliar repository.
- `CHANGE_AUDIT.md` — read-only acceptance audit of a working-tree change.

Prompts coordinate native tools; they do not create a hidden runtime. Read-only prompts must remain read-only. Bootstrap/refresh prompts must stop for one concise confirmation before force, overwrite, deletion, or material governance changes.

## Project `AGENTS.md`

Start from `project/AGENTS.template.md`, then replace placeholders with repository facts:

- purpose, stack, modules, and authoritative docs;
- ownership and allowed dependency direction;
- writable/read-only/generated boundaries;
- API/DB/IPC/auth contracts;
- real validation commands;
- project-specific hazards and exceptions.

Do not copy generic framework documentation or global engineering philosophy into the project file; select the relevant Skill instead.

## Spec Kit

Spec Kit remains an independent upstream project. Use its OpenCode integration only for work intentionally following specification-driven development.

- Use native `specify integration status`/`upgrade` for existing projects.
- Treat `specify init --here --force` as initial setup or fallback recovery, not the normal refresh path.
- Do not start Spec Kit automatically for unrelated routine fixes.
- Do not recreate Spec Kit commands, templates, or governance workflows in this repository.


## Evaluation and static audit

Run the deterministic repository audit before packaging:

```bash
python3 tools/audit.py
```

This zero-dependency Python audit validates catalog/lock integrity, Skill metadata, OMO templates, routing boundaries, prompt mutation boundaries, required license material, authored Markdown links, and evaluation-case shape. It does **not** prove OpenCode or OMO runtime behavior.

Use `evaluation/README.md` for the minimal host UAT: injection, non-interference, project precedence, root-cause behavior, scope, generated ownership, Skill relevance, validation truthfulness, one-shot bootstrap, and refresh/no-op. `evaluation/agentrc.eval.jsonc` is an optional external judge input; AgentRC results are cross-agent evidence, not OpenCode/OMO certification.

## Provenance vocabulary

`catalog/skills.lock.json` keeps separate claims:

- `sourceTrust`
- `integrity`
- `hostCompatibility`
- `behaviorStatus`
- `activationGuidance`
- `operationalRisk`
- `knownIssues`
- `redistributionStatus`

Do not collapse these into a single word such as "verified".

Reviewed upstream snapshots are kept byte-for-byte unchanged. Upgrade by replacing the whole snapshot with a reviewed revision and updating hashes, source metadata, known issues, and license evidence together. Repository-authored Skills are explicitly marked `local-derived`.

## APM later

APM is deferred, not rejected. Once the content is stable, APM can distribute selected references and Skills across multiple projects while `agent-reference` remains the source of truth.

Do not build another installer or package manager in this repository.

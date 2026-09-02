# agent-reference

Static, curated engineering references, bounded convenience prompts, and hash-pinned Agent Skill snapshots for OpenCode projects.

`agent-reference` is deliberately **not** a framework. It has no runtime, daemon, workflow engine, custom orchestrator, stack detector, installer, migration system, or generated project state.

```text
OpenCode        harness, AGENTS.md, native Skill discovery
OMO Slim        orchestration
Spec Kit        explicit specification workflow
agent-reference shared reference source
APM             distributes selected Skills/prompts to projects
```

## Core rule

**Catalog inclusion is not activation.**

The default global active Skill count is **zero**. Install only the Skills relevant to a real project or an explicit task. This keeps ambient metadata small and prevents unrelated technology or methodology guidance from influencing work.

## Quick start

Apply the pack incrementally.

1. Diff/merge `global/AGENTS.md` into `~/.config/opencode/AGENTS.md`; never overwrite an existing personal file blindly.
2. Copy `global/ENGINEERING.md` and `global/MEMORY.md` only after checking for existing files with those names.
3. For the recommended user-level tooling stack, explicitly run `prompts/OPENCODE_PLUGIN_SETUP.md`. It inventories the current environment and re-verifies official upstream compatibility before changing OpenCode/tool configuration.
4. Start with zero global Skills. Install technology Skills project-locally unless they are genuinely useful across most repositories.
5. Create/refine the project `AGENTS.md` manually or explicitly run `prompts/PROJECT_BOOTSTRAP.md`. Bootstrap can also install selected project Skills and create the minimal project-local OMO Slim Skill-routing override.
6. Restart OpenCode after plugin/Skill/routing changes before checking discovery and behavior.

Example tooling setup request:

```text
Read /path/to/agent-reference/prompts/OPENCODE_PLUGIN_SETUP.md and execute it completely for my current OpenCode environment.
Preserve unrelated OpenCode and OMO Slim configuration.
```

Example bootstrap request:

```text
Read /path/to/agent-reference/prompts/PROJECT_BOOTSTRAP.md and execute it for the current repository.
Do not modify application source during bootstrap.
```

Run small smoke checks before relying on the setup:

```text
1. Injection: summarize currently injected global rules without reading files.
2. Non-interference: perform one typo-only/mechanical change and confirm no planning ceremony or unrelated edit.
3. Project priority: request a small project-specific implementation and confirm project ownership/conventions override generic guidance.
4. Memory continuity: allow a normal interactive session to auto-capture useful context, close it, then open a fresh session and confirm relevant memory can reappear without a mandatory manual handoff.
5. Memory authority: confirm recalled memory is treated as context and current Git/source/config/tests still win on conflict.
```

A smoke PASS proves only the exercised surface; it does not certify every Skill, plugin, model, host version, or future release.

### Observed current smoke evidence

A validated macOS environment on 2026-09-02 observed OpenCode `1.18.26`, OMO Slim `2.2.18`, cc-safety-net `2.3.1`, RTK `0.46.0`, Notifier `0.2.8`, opencode-mem `2.25.0`, Plannotator `0.27.11`, and AgentsView `0.42.0` working together. OMO delegation, safety analysis, RTK integration, opencode-mem fresh-session persistence/automatic capture/auto-injection, Plannotator local approval feedback, and AgentsView OpenCode session discovery all passed. Simple Memory and TokenScope were removed from the active environment.

See `evaluation/README.md` for the exact evidence and limitations. Re-run relevant smoke checks after changing host versions or selected references/tools.

## Layout

```text
agent-reference/
├── AGENTS.md                     repository-maintenance rules
├── README.md
├── CHANGELOG.md
├── LICENSE
├── NOTICE
├── apm.yml                       APM producer metadata
├── .apm/                         APM producer layout
│   └── prompts/                  synchronized packaging mirrors
├── global/
│   ├── AGENTS.md                 small OpenCode global router
│   ├── ENGINEERING.md            conditional engineering reference
│   └── MEMORY.md                 opencode-mem continuity/authority policy
├── project/
│   └── AGENTS.template.md        factual project entry-point template
├── evaluation/
│   ├── README.md                 static-vs-behavioral evaluation guide
│   └── agentrc.eval.jsonc        optional cross-agent AgentRC cases
├── tools/
│   ├── audit.py                  deterministic maintainer audit entry point
│   ├── _audit_core.py            preserved static audit implementation
│   └── README.md
├── templates/
│   └── omo/                      project-local OMO Skill-routing examples
├── prompts/
│   ├── README.md                 copy-paste entry-point index
│   ├── OPENCODE_PLUGIN_SETUP.md  compatibility-aware user environment setup
│   ├── PROJECT_BOOTSTRAP.md
│   ├── PROJECT_REFRESH.md
│   ├── PROJECT_AUDIT.md
│   ├── CODEBASE_ONBOARD.md
│   ├── CHANGE_AUDIT.md
│   ├── APM_SETUP.md
│   └── AGENT_SYNC.md
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
└── MEMORY.md
```

- `AGENTS.md` is the short router, priority, scope, safety, and validation baseline.
- `ENGINEERING.md` is conditional. Load it for architecture/design review, unclear root-cause debugging, refactoring, meaningful cross-boundary work, security/reliability/performance decisions, and structural review—not for every small edit.
- `MEMORY.md` defines how automatically injected/recalled `opencode-mem` context is interpreted: repository evidence remains authoritative, routine work does not require a manual handoff, and manual memory operations are exceptional/on-demand.

The retired file-based work journal under `.opencode/history/` and the retired Simple Memory branch-handoff protocol are not part of the active system. Do not recreate them when persistent memory is unavailable; continue from current repository evidence.

`opencode-mem` uses its own local storage (commonly under `~/.opencode-mem/data`) rather than project-local `.opencode/memory/`. Local storage and capture-provider privacy are separate boundaries: auto-capture can send relevant context to a configured remote provider. Never use memory as a secret store.

## Recommended OpenCode tooling setup

`prompts/OPENCODE_PLUGIN_SETUP.md` is the single reproducible entry point for installing/reconciling the user-level stack after environment changes. It rechecks current official repositories, stable releases, compatibility issues, OpenCode/OMO behavior, and existing configuration before mutation.

Current role separation:

```text
OpenCode runtime
├─ OMO Slim          orchestration / subagents
├─ cc-safety-net     destructive-command guard
├─ RTK               command-output/token optimization
├─ opencode-mem      automatic persistent project memory
├─ Notifier          notifications
└─ Plannotator       human plan/document/code review

External companion
└─ AgentsView        session/history/token/cost analytics
```

Policy states:

- active baseline: OMO Slim, cc-safety-net, RTK, OpenCode Notifier, opencode-mem, Plannotator;
- external companion: AgentsView, kept outside the OpenCode plugin hook stack;
- retired: Simple Memory and TokenScope;
- pilot: `opencode-pty`, only after current OpenCode/runtime/platform compatibility is proven;
- not baseline/hold: DCP, `opencode-snip`, `opencode-vibeguard`, Morph Fast Apply, and `opencode-ignore` unless a later explicit evaluation changes the decision.

The policy is not a permanent version lock. A current regression may downgrade an active candidate, and a held/pilot tool should be promoted only when upstream evidence and a runtime smoke prove the relevant boundary.

### Memory behavior

`opencode-mem` normally auto-captures useful technical context after conversation turns when a session becomes idle and can inject relevant memories into later sessions. Users and agents should not need to say “remember this” after ordinary work.

Manual memory is for immediate add/search/list/correction/migration needs. Stable rules belong in `AGENTS.md` or maintained project documentation, and stale memory never overrides current repository evidence.

Do not create `.opencode-mem-project` automatically. Use it only when multiple nested repositories are intentionally one shared memory domain.

### Plan/code review

Plannotator is a human review surface, not mandatory ceremony. Use local/manual review for important plans, documents, or diffs when human approval/annotation materially helps; do not force it for trivial work. Remote sharing/network review features are opt-in.

### Analytics

AgentsView replaces TokenScope in the recommended stack when standalone analytics is acceptable. Keep analytics outside OpenCode runtime hooks. Use local/loopback CLI/UI for session discovery, history, token usage, and cost/statistics; a permanently running daemon is not a baseline requirement.

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

`templates/omo/` contains reviewed **examples**, not blindly installable profiles. They use root `agents.<agent>.skills` overrides so project stack routing stays separate from user-owned models, variants, MCPs, and companion settings. Runtime `/preset` switching has separate merge behavior, so projects that depend on preset switching must verify routing after a switch or deliberately maintain preset-local routing.

Default routing principle: leave Orchestrator, Explorer, Librarian, and Oracle alone unless the repository has a concrete reason to override them; route proven implementation Skills to Fixer and proven UI Skills to Designer. Operational Skills are never automatic.

Persistent memory does not require a separate OMO handoff writer. Subagents return discoveries through normal orchestration, the coordinating agent verifies material findings against the repository, and `opencode-mem` handles routine capture/injection.

## Convenience prompts

The prompt set is intentionally small and explicit. `prompts/README.md` provides copy-paste entry requests:

- `OPENCODE_PLUGIN_SETUP.md` — user-level OpenCode/tool inventory, official-upstream re-verification, installation/reconciliation, smoke tests, migration, and rollback.
- `PROJECT_BOOTSTRAP.md` — onboarding and initial project agent setup.
- `PROJECT_REFRESH.md` — reconcile stale project guidance, selected Skills, and Spec Kit integration.
- `PROJECT_AUDIT.md` — read-only health check of agent-facing configuration.
- `CODEBASE_ONBOARD.md` — read-only map of an unfamiliar repository.
- `CHANGE_AUDIT.md` — read-only acceptance audit of a working-tree change.
- `APM_SETUP.md` — initial APM adoption and selected-content deployment.
- `AGENT_SYNC.md` — routine APM dependency and agent-configuration sync.

Choose the narrowest prompt that matches the task. Project bootstrap/refresh must not silently mutate user-level plugin/model/MCP configuration; tooling environment setup is a separate explicit action.

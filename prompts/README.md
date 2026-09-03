# Convenience prompt index

These are explicit, bounded entry points. They coordinate existing OpenCode, OMO Slim, APM, optional Spec Kit, and agent-reference capabilities; they do not replace them.

Spec Kit is **not** part of the default agent-reference project baseline. Its absence is healthy. Bootstrap/refresh must not install, restore, or repair it unless the user explicitly requests Spec Kit work.

For APM-adopted repositories, project technology Skills should be owned by the project APM deployment rather than duplicated under the user-global Skill root. User-level Skills are best reserved for genuine cross-project utilities/tooling or deliberate documented overrides.

Use the prompt file from the reference source rather than copying its body into every repository.

## Completion reports

Mutation/setup prompts follow the global completion response contract in `global/AGENTS.md`:

- lead with a concrete overall result;
- name actual changed paths/symbols and what changed there;
- include behavior/decision sections only when they materially help review;
- report validation as `PASS`, `FAIL`, `BLOCKED`, or `NOT RUN` with the actual command/check;
- show only material unresolved items under `Needs attention`;
- omit normal preserved state and internal checklist dumps;
- end after the final report instead of opening an optional follow-up menu.

Read-only audit/onboarding prompts may keep their task-specific output structures when those structures better express findings or discovery evidence.

## OpenCode tooling environment setup or reconciliation

```text
Read /path/to/agent-reference/prompts/OPENCODE_PLUGIN_SETUP.md and execute it completely for my current OpenCode environment.
Preserve unrelated OpenCode and OMO Slim configuration.
```

Expected scope: current environment inventory, official-upstream re-verification, compatibility-aware reconciliation of the active OpenCode tool stack, retirement/migration of obsolete plugins when present, runtime smoke tests, external-companion validation, and rollback notes. This prompt may change user-level OpenCode/tool configuration; it does not modify application source or commit/push repositories.

## New or newly adopted repository

```text
Read /path/to/agent-reference/prompts/PROJECT_BOOTSTRAP.md and execute it completely for the current repository.
Do not modify application source during bootstrap.
```

Expected scope: repository facts, project `AGENTS.md`, project-relevant Skill selection/ownership, minimal project-local OMO Slim Skill routing, and configuration validation. Spec Kit setup is included only when explicitly requested.

## Microsoft APM setup

```text
Read /path/to/agent-reference/prompts/APM_SETUP.md and execute it completely for the current repository.
```

Command: `apm-setup` — Set up Microsoft APM and migrate this project to agent-reference APM management. Configuration/deployment-only; do not modify application source. The preferred end state is APM-owned project technology Skills with no accidental higher-precedence global same-ID override.

## Routine agent-reference APM sync

```text
Read /path/to/agent-reference/prompts/AGENT_SYNC.md and execute it completely for the current repository.
```

Command: `agent-sync` — Update agent-reference APM dependencies and reconcile project agent configuration. Run only after `apm-setup` has completed; do not install APM or perform first-time migration.

## Test environment setup

```text
Read /path/to/agent-reference/prompts/TEST_SETUP.md and execute it completely for the current repository.
```

Command: `test-setup` — Establish or reconcile a small, trustworthy testing portfolio from Static/Unit through representative System/E2E evidence. It may modify test infrastructure, tests, test CI configuration, and the project Testing section; it must not change production behavior merely to make tests pass. Its specialized evidence matrix may supplement the common completion contract because testing responsibility state is part of the requested result.

## Existing repository after stack/architecture changes

```text
Read /path/to/agent-reference/prompts/PROJECT_REFRESH.md and execute it for the current repository.
Keep the refresh configuration-only.
```

Expected scope: stale `AGENTS.md`, Skill selection/ownership, OMO local routing, optional explicitly requested Spec Kit maintenance, and configuration validation. A removed/absent Spec Kit integration is not recreated automatically.

## Read-only setup health check

```text
Read /path/to/agent-reference/prompts/PROJECT_AUDIT.md and audit the current repository.
Do not modify files.
```

Spec Kit absence is not an audit finding; existing `.specify/` state may be reported read-only when present.

## Understand an unfamiliar repository

```text
Read /path/to/agent-reference/prompts/CODEBASE_ONBOARD.md and map the current repository.
Do not modify files.
```

## Audit a completed working-tree change

```text
Read /path/to/agent-reference/prompts/CHANGE_AUDIT.md and audit the current change against the request and repository contracts.
Do not modify files.
```

## Selection rule

- User-level OpenCode/tool stack setup/reconciliation: `OPENCODE_PLUGIN_SETUP`.
- New repository bootstrap: `PROJECT_BOOTSTRAP`; existing repository APM adoption: `APM_SETUP`.
- Existing APM dependency maintenance: `AGENT_SYNC`.
- Testing portfolio/infrastructure setup: `TEST_SETUP`.
- Already configured but stale: `PROJECT_REFRESH`.
- Unsure whether setup is healthy: `PROJECT_AUDIT` before mutating anything.
- Spec Kit: opt in explicitly when the project actually wants specification/governance workflows.
- Do not chain all prompts by default. Choose the narrowest one that matches the task.

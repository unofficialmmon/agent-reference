# Convenience prompt index

These are explicit, bounded entry points. They coordinate existing OpenCode, OMO Slim, Spec Kit, and agent-reference capabilities; they do not replace them.

Use the prompt file from the reference source rather than copying its body into every repository.

## New or newly adopted repository

```text
Read /path/to/agent-reference/prompts/PROJECT_BOOTSTRAP.md and execute it completely for the current repository.
Do not modify application source during bootstrap.
```

Expected scope: repository facts, project `AGENTS.md`, selected project-local Skills, minimal project-local OMO Slim Skill routing, Spec Kit setup/health, configuration validation.

## Microsoft APM setup

```text
Read /path/to/agent-reference/prompts/APM_SETUP.md and execute it completely for the current repository.
```

Command: `apm-setup` — Set up Microsoft APM and migrate this project to agent-reference APM management. Configuration/deployment-only; do not modify application source.

## Routine agent-reference APM sync

```text
Read /path/to/agent-reference/prompts/AGENT_SYNC.md and execute it completely for the current repository.
```

Command: `agent-sync` — Update agent-reference APM dependencies and reconcile project agent configuration. Run only after `apm-setup` has completed; do not install APM or perform first-time migration.

## Existing repository after stack/architecture changes

```text
Read /path/to/agent-reference/prompts/PROJECT_REFRESH.md and execute it for the current repository.
Keep the refresh configuration-only.
```

Expected scope: stale `AGENTS.md`, Skill selection/routing, OMO local routing, Spec Kit integration/constitution drift, configuration validation.

## Read-only setup health check

```text
Read /path/to/agent-reference/prompts/PROJECT_AUDIT.md and audit the current repository.
Do not modify files.
```

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

- New repository bootstrap: `PROJECT_BOOTSTRAP`; existing repository APM adoption: `APM_SETUP`.
- Existing APM dependency maintenance: `AGENT_SYNC`.
- Already configured but stale: `PROJECT_REFRESH`.
- Unsure whether setup is healthy: `PROJECT_AUDIT` before mutating anything.
- Do not chain all prompts by default. Choose the narrowest one that matches the task.

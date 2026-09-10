# Tool adoption plan - OpenCode V1

Approved scope: 2026-09-10, starting from `99fe064812228fe972cb82e877bf93f1e7d1a741`.

## Delivery sequence

1. Tool governance: 24 new selected capabilities in agent/automation/developer catalogs; bounded read-only upstream observations and negative tests.
2. Setup entry points: missing installation is a normal starting state; inventory, official installation channels, surgical configuration changes, rollback, and honest per-tool evidence.
3. Agent capabilities: OpenCode MCP fragments, OMO allowlist composition, Context7 duplicate-provider prevention, Serena pilot, Playwright operational opt-in, and ast-grep fixture verification.
4. Project automation: project-specific setup, CI/hook/task examples, native build ownership, and independent clean/failing-fixture validation.

Each delivery is a separate PR, with tests and current CI reviewed before merge. Repository changes do not install software on the user's computer.

## Non-negotiable boundaries

- No V2 work, new runtime/installer engine, vendor Skill edits, automatic global activation, or consumer-project mutation from this repository's CI.
- Preserve providers/models, intentional MCP exclusions, existing healthy build/task/runtime/hook choices, and all APM-managed Skill ownership.
- Runtime catalog entries are policy, not an installation inventory or compatibility certificate.
- Do not automatically install pilot tools, enable browser access, authorize GitHub writes, or change GitHub App/organization settings.
- Keep credentials in the host's supported auth/environment storage, never in committed examples, logs, reports, or user-shared config copies.
- Missing credentials, blocked downloads, unavailable platforms, and unexecuted host tests must remain BLOCKED/NOT RUN, never PASS.
- Use existing native package managers, upstream CLIs, OpenCode configuration and APM. Setup prompts coordinate these; they do not introduce a package manager or custom patch engine.

## Acceptance

Run existing audit and regression tests plus new catalog/template/fixture checks. Test both healthy inputs and rejection paths. Capture GitHub CI artifacts. Validate exact merge revisions and unchanged vendor/APM snapshots. Re-run setup on a configured host to prove NOOP before claiming host idempotence. Model-dependent OpenCode/OMO behavior requires a separate actual host run, not a JSON parse or CLI version check.

## Deferred

Repomix, watchexec, hyperfine, Dagger, Promptfoo, Langfuse and a second Git-hook orchestrator are outside this adoption. Existing optional AgentRC evaluation is not replaced. No composite 'tool health score' is introduced: recent activity does not prove safety, and slow releases do not mean abandonment.

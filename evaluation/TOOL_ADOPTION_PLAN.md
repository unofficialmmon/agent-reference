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

## Delivery and validation records

- [PR #7](https://github.com/unofficialmmon/agent-reference/pull/7): 24-tool catalogs and bounded observations; 77 deterministic tests and existing CI passed before merge.
- [PR #8](https://github.com/unofficialmmon/agent-reference/pull/8): missing-installation setup, shared transaction/rollback contract, developer/project entries; existing checks and new static setup contracts passed before merge.
- [PR #9](https://github.com/unofficialmmon/agent-reference/pull/9): disabled MCP fragments, OMO access composition and actual ast-grep/isolated Playwright smoke; 100 deterministic tests passed. Direct-tool run [34456791954](https://github.com/unofficialmmon/agent-reference/actions/runs/34456791954) passed after fixing a workflow runner-context error. Merge: `dc1e3026be73d6b3df4b7fbbefe8fc56733cea31`.
- [PR #10](https://github.com/unofficialmmon/agent-reference/pull/10): scoped project automation examples, documentation/audit integration and independent scanner fixtures. Direct scanner run [34457529076](https://github.com/unofficialmmon/agent-reference/actions/runs/34457529076) passed against implementation `c7dfd4323f71ae704cd221d79b8ebe4e73977a15`; final revision and repeated checks are recorded in the PR.

The complete local change set passed 110 deterministic tests, full static audit with zero errors and two retained upstream warnings, whitespace checks, workflow YAML parsing and JavaScript syntax checking. Final GitHub CI/artifacts and merge-tree comparison remain the authoritative record for the exact committed revision; these tests do not count as model or workstation behavior.

Direct fixture evidence covers ast-grep structural match/rewrite, Playwright MCP initialize/list/navigation/snapshot/close, ShellCheck SC2086, Hadolint DL3007, Gitleaks staged-versus-worktree detection/redaction and Trivy Dockerfile misconfiguration. Trivy vulnerability database/image scanning, CodeQL enrollment, Renovate App operation, Lefthook installation, mise/just runtime use, OpenRewrite migration, authenticated remote MCP operations, Serena multi-language behavior and full OpenCode/OMO setup/NOOP remain NOT RUN in the user's environment.

Two review refinements are intentional: preserve the existing runtime catalog schema and add a separate agent-capability catalog (four catalogs total), and record Gitleaks as feature-complete/security-patch-only instead of treating recent pushes as active feature development. No replacement scanner or extra Skill was silently added. Workstation adoption starts with `prompts/TOOLING_SETUP.md`; project-only work uses `prompts/PROJECT_TOOLING_SETUP.md`.

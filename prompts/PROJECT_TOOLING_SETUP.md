# Project tooling setup

Perform explicit project configuration work only. Read [CONTRACT.md](../templates/setup/CONTRACT.md), [INSTALLATION.md](../templates/setup/INSTALLATION.md), and `catalog/automation-tools.json`. Start with `git status --short` and the project's authoritative AGENTS/contracts. Do not modify application source, schemas/data, generated output, user-global OpenCode settings, personal shell setup or other repositories.

## Selection

Identify maintained files/builds, supported languages, runtime versions, existing task/hook/security/update owners and CI context. Record a short evidence -> candidate -> existing owner -> decision map. Extensionless shell scripts and nonstandard Dockerfile names count when maintained; vendored examples and transitive dependencies alone do not justify activation.

- CodeQL: supported languages, GitHub entitlement/permissions, and no duplicate default/advanced setup.
- Gitleaks: staged/pre-push/CI coverage with redacted output and reviewed exclusions.
- Trivy: actual dependency/image/IaC targets; separate scan failure from unavailable DB/network and avoid duplicate secret scanning.
- ShellCheck/Hadolint: relevant maintained shell/Docker files, not an indiscriminate vendor sweep.
- Renovate: needed dependency policy and approved App/runner access; preserve working Dependabot and do not enable automerge by default.
- just/mise/Lefthook: only a proven gap; preserve Make/Taskfile/npm/Gradle/Maven wrappers, SDKMAN/nvm/toolchains and existing pre-commit/Husky/hooks respectively.
- OpenRewrite: only for an explicitly requested migration/refactor; stack detection permits recommending it, not running recipes.

## Mutation

Use [project task/hook/runtime examples](../templates/project/README.md) and [CI security examples](../templates/github/README.md) only after establishing scope. These examples are not automatically copied or enabled. Run their native validators and target-specific clean/failing tests; the repository fixture checks are not consumer-project certification.

Before writes, list selected package installations and config/workflow paths. On a developer workstation, request any ungranted global install/admin scope; use an existing approved project-local package route when supported. CI installation on a disposable runner is not proof of workstation installation.

Use current upstream syntax and the repository's real commands. Add only missing config under the current owner's files. Keep action revisions and executable dependencies pinned; preserve dirty changes. No empty `just test`/`just security` recipes, success stubs or invented native commands. `just verify` is optional; native commands remain available for diagnosis. Keep mise runtime management separate from just task ownership when both are adopted.

Use `lefthook install` only after reviewing existing hooks and `core.hooksPath`; do not replace another hook owner. Test the staged index, including partial staging, rather than claiming a working-tree scan protects staged content. Local hooks can be bypassed, so CI repeats required checks.

For GitHub scanning/Bot enrollment or repository settings requiring a human/admin grant, explain the exact remaining action and record BLOCKED. A config file alone is not a running Bot or protected merge gate. Do not weaken or install branch protection as an incidental fix.

OpenRewrite setup may document or add an approved pinned build integration. Recipe execution changes application source and is outside this prompt: stop after a dry-run plan unless the active request separately authorizes the migration. Preserve generator ownership and require diff review plus native build/tests after an authorized migration.

## Verification

Validate config syntax with each upstream CLI where available, then test one clean and one intentionally failing temporary fixture for each selected checker. Do not commit realistic credentials or vulnerabilities as fixtures; generate inert synthetic data locally and redact output. Confirm CI runs against the intended revision and findings fail the intended gate. Report zero scanned targets/unsupported languages as NOT APPLICABLE or BLOCKED, never a security PASS.

Check `git diff --check`, actual changed files and absence of application/global changes. Reconcile again for NOOP. Report scoped check coverage, native commands actually run, prerequisites, unresolved findings and rollback. Do not commit/push or run application migrations under setup-only authority.

# Project automation examples

Use [PROJECT_TOOLING_SETUP](../../prompts/PROJECT_TOOLING_SETUP.md) only for an explicitly scoped project. Examples are not auto-installed profiles. Preserve a healthy existing native build, CI, hook, runtime or dependency-update owner. None of these files belongs in OpenCode's `mcp` or `plugin` array.

## Task and runtime ownership

`agent-reference.justfile` wraps actual checks for this reference repository. Copy it to the root only when just adoption is approved; consumer projects must replace its commands with their actual native build/tests. Never create empty success recipes. Normal work can use `just verify`; debugging still uses Maven/Gradle/npm/Python directly. Validate the selected Just version and recipe listing, then execute each recipe, including a failing-command fixture.

`mise.example.toml` is a Python-only version example, not an upgrade recommendation. Match the project's real required runtime; use the upstream's native pinning/installation flow and verify the resolved patch. Do not automatically trust unknown mise files or replace SDKMAN/nvm/toolchains. When just owns tasks, mise need only own runtimes/environment: do not duplicate every task in both tools. Global shell activation is separate workstation scope. A configuration file alone does not prove the runtime is installed in OpenCode's PATH.

## Lefthook and Gitleaks

`lefthook.yml` uses the actual staged-index command supported by the selected Gitleaks version. First inspect `.git/hooks`, `core.hooksPath` and any pre-commit/Husky owner. Preserve an existing owner instead of adding a second one. Install the binary through an approved channel; then, only in the scoped repo, run native `lefthook install`. Execute a clean hook and an inert temporary staged-token case. Verify partial staging: a token in the index must be found even when the working tree is clean, while uncommitted work outside the index is not silently staged or rewritten. CI must independently scan the intended commit/history scope; a local hook is bypassable.

Gitleaks upstream currently declares feature completion and security-patch-only future releases, with the maintainer focusing on Betterleaks. Keep the selected, tested Gitleaks CLI for this adoption, but track this maintenance limitation and do not claim active feature development. Do not add Betterleaks or a second scanner without separate review. Never suppress unexplained findings with a blanket baseline or print actual secrets.

## Renovate

`renovate.json` intentionally starts with GitHub Actions only, no automatic merge and bounded PR counts. Add Maven/npm/etc. only when those manifests actually exist and Renovate owns their updates. Avoid duplicate Dependabot coverage. Validate with the installed official Renovate config validator. Config creation is not Bot onboarding: an approved GitHub App or existing runner, permissions and actual first PR are separate evidence. Do not install a GitHub App or change organization settings as an incidental setup step. Do not expect Renovate to refresh vendored Skill snapshots/locks automatically.

## OpenRewrite

Java/Spring presence only recommends an option. An actual migration request must identify the desired version/recipe and affected modules. Inspect the existing Maven/Gradle wrapper, build plugins, generated-source boundaries and Java toolchain. Follow current official documentation to pin the build plugin and specific recipe dependencies. Do not substitute an unreviewed latest recipe or rewrite generated files.

For a Maven project where the approved plugin and active recipes are ALREADY configured, inspect recipes and preview with its native commands:

```bash
./mvnw rewrite:discover
./mvnw rewrite:dryRun
```

For an already configured Gradle project use the plugin's actual `rewriteDiscover` and `rewriteDryRun` tasks through its wrapper. These are prerequisites-dependent examples, not commands for every repository. Inspect the dry-run diff and expected scope; application-source mutation remains a separately authorized migration. After an authorized run, execute focused tests, full required checks and contract/generation validation. Do not auto-run recipes from setup, commit hooks or ordinary dependency-update PRs.

## Shell and Docker lint

Use actual maintained target paths and the installed CLI: `shellcheck <paths>` and `hadolint <Dockerfiles>`. Include extensionless supported-shell scripts and nonstandard Dockerfile names when relevant. Do not pass a guessed glob that quietly matches no files or scan vendor content as though it were human-owned code. Use the same reviewed flags locally and in CI. Lint success is not application test or vulnerability-scan success.

## Sources and proof boundary

- [Gitleaks staged command implementation at v8.30.1](https://github.com/gitleaks/gitleaks/blob/v8.30.1/cmd/git.go)
- [Gitleaks maintenance announcement](https://github.com/gitleaks/gitleaks#readme)
- [Lefthook usage](https://lefthook.dev/usage/commands.html)
- [OpenRewrite running recipes](https://docs.openrewrite.org/running-recipes)
- [Renovate onboarding](https://docs.renovatebot.com/getting-started/installing-onboarding/)
- [mise configuration](https://mise.jdx.dev/configuration.html)
- [just manual](https://just.systems/man/en/)

Repository tests verify example syntax/contracts. Direct fixture tests exercise installed checkers; they do not prove your actual hooks, Bot, runtime or migration works. Record those host-specific checks separately.

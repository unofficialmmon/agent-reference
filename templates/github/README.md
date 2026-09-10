# Project security workflow examples

These are opt-in examples for a consumer repository, not workflows automatically installed by APM/bootstrap. Use [PROJECT_TOOLING_SETUP](../../prompts/PROJECT_TOOLING_SETUP.md), inspect existing scanning owners and entitlement, and merge only the relevant workflow. No `pull_request_target`, personal token, forced write permission or automatic dependency merge is introduced.

| Example | Actual scope |
|---|---|
| `gitleaks.yml` | Redacted secret scan of checked-out Git history; full-depth checkout, explicit nonzero finding exit |
| `trivy-config.yml` | HIGH/CRITICAL misconfiguration scan with a nonempty-target check; not dependency/image coverage |
| `codeql-python.yml` | Advanced CodeQL example for an actual Python repository; not a universal language/build matrix |

All executables/actions in these examples are pinned. Downloaded checksum manifests are themselves SHA-256 pinned before verifying archives; a failed download/checksum is a real failure. Pins are reviewed snapshots, not permanent safety guarantees. Review releases/advisories before deployment/update, then test on the selected runner platform. The install steps target Ubuntu x86-64 runners only and do not install the user's workstation. Runtime package installation belongs to the upstream method, not a custom manifest engine.

## Scope before copying

Choose actual maintained targets. A reference repository containing vendor examples is not the same as a deployable application. Do not silence vendor findings globally to obtain green CI. Review file/target exclusions and explain them as ownership/coverage choices. Do not use missing credentials, unavailable vulnerability databases or zero scanned targets as a clean result.

Gitleaks should cover staged changes locally and intended Git history/PR commits in CI. The example scans history, which can find pre-existing leaks; rotate/revoke genuine exposed credentials rather than only removing the text. Do not upload an unredacted report, print matched secrets or add an unexplained baseline. Upstream is feature-complete/security-patch-only, so maintenance monitoring must record that limitation.

Trivy's example handles config only. Add `trivy fs --scanners vuln ...` for actual supported lockfiles and `trivy image --scanners vuln ...` for the built immutable image when those targets exist. Keep secret scanning owned by Gitleaks to avoid duplicate noise. Do not use `--skip-db-update` on a missing/stale DB or `--ignore-unfixed` merely to avoid failures. Verify scanner target count, DB age, finding threshold and nonzero error exit separately. The fixture smoke uses built-in Dockerfile checks with check updates disabled for isolation; that is not a production database policy.

CodeQL needs supported languages and an appropriate build mode. The Python example uses `none`; Java/other languages must use their currently supported mode and real build prerequisites. Preserve healthy default setup rather than installing a duplicate advanced setup. `security-events: write` belongs only to the analysis/upload job. A successful SARIF upload does not automatically block a PR for findings: configure approved code-scanning merge protection/required checks separately. Workflow presence is not proof scanning or a protected merge gate is active.

Lefthook and lint examples live in [project automation](../project/README.md). Use native ShellCheck/Hadolint on reviewed maintained paths in the existing lint job; absent targets are NOT APPLICABLE, not security PASS. Do not lint or rewrite arbitrary vendor snapshots just to satisfy the template.

## Evidence

This repository's `automation-smoke.yml` downloads the pinned CLI releases and executes `tools/smoke_security.py` on clean and intentionally failing inert temporary fixtures. It validates checker execution, expected finding identities, staged-vs-working-tree behavior and redaction. It never scans a user's files or certifies an application. Actual CodeQL enrollment, Bot onboarding and consumer CI still need their own execution records.

Sources reviewed 2026-09-10: official Gitleaks v8.30.1 release/checksums and staged command implementation; ShellCheck v0.11.0 Linux x86-64 asset; Hadolint v2.15.1 Linux x86-64 asset; Trivy v0.74.0 checksums and configuration docs; CodeQL action v4 resolved to `b96794f015dfd88f77b49b1c93e0fa7110f94c63`. These are upstream integrity/command references, not claims that all target-host behavior was tested.

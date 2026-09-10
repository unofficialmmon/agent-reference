# Installation channels and ownership

Use the official URL in each catalog entry to re-verify current support. These are channel examples, not a bulk install script or immutable version recommendations. Run only selected rows after the shared setup contract. Check the installed binary version, actual path and manager receipt after installation.

| Tool | macOS example when Homebrew already exists | Other supported route / ownership |
|---|---|---|
| GitHub MCP | Prefer approved remote connection; no local installation required | Official release binary or Docker image only when already appropriate; token scope/read-only toolsets reviewed separately |
| Context7 | Reuse OMO's working provider; otherwise approved remote endpoint | Official npm MCP package only when local hosting is needed; do not duplicate provider IDs |
| Serena | Do not assume a brew package | Official uv/uvx route with reviewed immutable revision; inspect prerequisites and project language server; pilot opt-in |
| Playwright MCP | Official npm package with a reviewed exact version | Install its matching supported browser using upstream instructions; isolated test profile; no personal browser bridge |
| ast-grep | `brew install ast-grep` | Official `@ast-grep/cli` exact npm version, Cargo `--locked`, or supported binary; verify `ast-grep --version` |
| Gitleaks | `brew install gitleaks` | Official pinned binary/container; CLI is separate from licensing/permissions of a third-party Action wrapper |
| Trivy | `brew install trivy` | Official packages/release/container; scanner DB/network availability is a separate requirement |
| ShellCheck | `brew install shellcheck` | Supported distro package or official release binary |
| Hadolint | `brew install hadolint` | Official release/container; Docker is not otherwise mandatory |
| Lefthook | `brew install lefthook` | Official package; installing the binary does not install hooks into every repo |
| just | `brew install just` | Official package/release; no mandatory replacement of Make/Maven/Gradle/npm tasks |
| mise | `brew install mise` | Official package; trust/activation/runtime downloads require scoped consent |
| OpenRewrite | No global installation | Pin the Maven/Gradle plugin and selected recipe artifacts in the scoped project; dry run before source mutation |
| CodeQL | No workstation requirement for GitHub scanning | Prefer existing/default GitHub setup; advanced workflow only for supported languages and repository entitlement |
| Renovate | No workstation requirement for managed Bot | Approved GitHub App or existing runner; app authorization is a separate human/admin operation |
| rg | `brew install ripgrep` | Official/distro package; executable `rg` |
| jq | `brew install jq` | Official/distro package |
| yq | `brew install yq` | Verify Mike Farah implementation, not a same-name Python wrapper |
| fd | `brew install fd` | May be `fdfind` on a distro; do not change global aliases silently |
| fzf | `brew install fzf` | Shell key bindings/completion are separately selected |
| bat | `brew install bat` | May be `batcat` on a distro; keep automated output plain/noninteractive |
| zoxide | `brew install zoxide` | Add one upstream shell-init line only for the actual selected shell |
| lazygit | `brew install lazygit` | Human TUI; verify version, interactive behavior only with user observation |
| difftastic | `brew install difftastic` | Executable `difft`; do not replace global Git diff configuration without consent |

For unavailable prerequisites or unsupported hosts, record BLOCKED or NOT APPLICABLE rather than inventing a package name. Do not add platform-specific paths from one computer to shared templates.

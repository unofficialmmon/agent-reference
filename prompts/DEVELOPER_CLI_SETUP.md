# Developer CLI setup

Perform explicit workstation configuration only. Read [CONTRACT.md](../templates/setup/CONTRACT.md), [INSTALLATION.md](../templates/setup/INSTALLATION.md), and `catalog/developer-tools.json` from this source root. Preserve project source, OpenCode models/providers/MCPs, global Git settings and unrelated shell configuration.

Default selection is rg and jq. Install yq/fd/fzf/bat/zoxide/lazygit/difftastic only when selected by the user or justified by a specifically approved setup scope. A list in a catalog is not permission for all optional shell integrations.

Inventory binaries, versions, package receipts, PATH/shims and the actual terminal/OpenCode launch environment. Install only missing selected tools through current supported channels. Do not install ast-grep again if OpenCode setup owns its installation. Do not add TUI tools to agent MCP/Skill allowlists or CI requirements.

Smoke checks must be non-destructive and use temporary fixtures: rg finds expected text; jq selects a known JSON key; yq reads a known YAML value; fd finds a fixture filename; fzf may be tested noninteractively with `--filter`; bat uses plain output with paging disabled; difft uses two temporary files and its documented exit semantics. Version-only checks for interactive UX must not be called end-to-end TUI validation. zoxide shell activation and lazygit interactive behavior require the actual shell/terminal; report NOT RUN when not exercised.

Do not replace grep/find/cat/cd aliases, global diff drivers, Git pager, shell key bindings or completions as a side effect of binary installation. If explicitly selected, add only the upstream-supported initialization to the correct shell file, preserve existing definitions, verify a fresh shell and keep rollback. Report actual installation/configuration/check states using the shared contract and stop.

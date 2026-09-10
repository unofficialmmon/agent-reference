# Tool catalog and adoption boundaries

The runtime baseline remains in `tooling.json`. The 24 newly selected capabilities live in `agent-capabilities.json` (5), `automation-tools.json` (10), and `developer-tools.json` (9). Keeping the existing runtime schema intact avoids breaking its setup and historical-evidence consumers; this is a deliberate refinement of the proposed three-file layout, not a second runtime policy source. `tools/tool_catalog.py` validates uniqueness across all four files.

Catalog policy, installed state, enabled state, routed state, authentication and observed behavior are different facts. A catalog entry is never an installation receipt. `baseline` means preferred when the relevant role is adopted, not mandatory startup loading. `conditional` requires repository evidence. `optional` requires user need. `pilot` and `operational` require explicit selection and never auto-promote.

OpenRewrite remains a Java-stack candidate but is operational when actually rewriting source. CodeQL requires a supported language and repository entitlement, not merely a GitHub remote. ShellCheck discovery includes extensionless supported-shell scripts, not just `*.sh`. Context7 may already be supplied by OMO Slim; preserve one healthy provider rather than registering it twice.

## Setup ownership

Use the existing OpenCode setup entry for host/plugins/MCPs; use project tooling setup for project CI/task/hooks/build configuration and developer CLI setup for optional workstation utilities. Setup is performed on the target host using upstream installation methods. This repository does not install tools when cloned, when an APM dependency updates, or when its CI runs.

Never commit secrets, user models/providers, personal absolute paths or browser storage state. Never register CLI-only utilities in `mcp` or in the OpenCode `plugin` list. CI/Bot configuration is not an OpenCode plugin. Existing healthy tools, runtime managers and hook/task conventions win over preferred examples.

## Maintenance observations

Run `python3 tools/tool_catalog.py` for offline validation and `python3 tools/tool_catalog.py --online` for bounded public GitHub observations. Online output is a report, not a security or compatibility gate. It records canonical identity, archival/disabled flags, default-branch commit, latest stable release if available, and timestamps. Metadata push time is informational, not proof of substantive maintenance.

`RECENT_ACTIVITY` means a commit/release within the review window, not 'safe'. `REVIEW_DUE` means investigate, not 'dead'. `ARCHIVED`, `DISABLED`, `RENAMED`, and `UNRESOLVED` need review. Missing releases are normal; network/auth/rate-limit failures are not CURRENT. No versions, installation receipts, or fabricated review dates are written back to policy. Reports go to CI artifacts; future policy changes require a reviewed PR.

## Out of scope

Repomix, watchexec, hyperfine, Dagger, Promptfoo, Langfuse and pre-commit as a second hook owner are not adopted. Existing usage in consumer repositories must be preserved. Tool activity is not the reason for these exclusions: applicability and overlap are.

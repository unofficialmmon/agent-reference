# Installing the global router and conditional references

During explicitly authorized OpenCode environment setup, compare the source `global/AGENTS.md`, `global/ENGINEERING.md`, `global/MEMORY.md` and `global/TOOLS.md` with files beside the effective user-global OpenCode rules. Do not overwrite personal files or assume the default configuration path.

Copy a missing conditional reference only after checking for an existing same-name file. For an existing customized reference, propose a small diff and preserve user rules; do not normalize it to the shared template. Add the conditional TOOLS router entry to the existing global AGENTS only when that reference is available. Do not embed every tool's installation procedure in AGENTS or preload all references at startup.

## Global APM bootstrap command

During this same explicitly authorized workstation setup, reconcile one user-global OpenCode bootstrap command so a repository that has not adopted APM can start the supported adoption flow with `/apm-setup`.

Use the canonical `prompts/APM_SETUP.md` from the resolved agent-reference source revision as the command body and copy it byte-for-byte to the effective user-global OpenCode commands directory as `commands/apm-setup.md` (normally `~/.config/opencode/commands/apm-setup.md`; honor supported config-directory overrides). Do not create a second independently maintained prompt or fetch an unpinned remote copy at invocation time.

The bootstrap is the only agent-reference package command intended for user-global discovery. Do not install `/agent-sync` or `/test-setup` globally: those commands are meaningful only after a consumer repository has adopted APM and are then deployed project-locally by APM. Do not deploy `.agents/skills/`, a global `apm.yml`, a global lock, or any global Skill as part of this bootstrap; the default global active Skill count remains zero.

Before writing, inspect the target path. If it is missing, create only the required commands directory and exact command copy. If it is byte-identical to the current canonical prompt, report `ALREADY_HEALTHY`. If it differs, do not overwrite it merely because the filename matches: preserve an unknown or customized command and report the bootstrap update as `BLOCKED` unless ownership as an unmodified older agent-reference copy can be established and rollback is retained. Never hand-edit the installed copy independently of the canonical prompt.

After installation, verify the file bytes and, when the installed OpenCode version exposes a safe command-discovery check, confirm `/apm-setup` is discoverable from a directory with no project-local command. If host discovery is not actually exercised, report it as `NOT RUN` rather than inferring it from file presence. Once a project adopts APM, its `.opencode/commands/apm-setup.md` is the project-owned command and may take precedence over the global bootstrap; APM remains the owner of project-local generated commands and Skills.

Changes to this GitHub repository do not update existing workstation copies. APM project dependency sync also does not own user-global reference or bootstrap copies. Record source revision and actual changed paths in the setup report, without creating a parallel tracking runtime. Missing optional TOOLS guidance does not block ordinary implementation using current project evidence; a missing or blocked global bootstrap can still be bypassed by explicitly reading the canonical local `prompts/APM_SETUP.md`.

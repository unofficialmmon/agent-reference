# Installing the global router and conditional references

During explicitly authorized OpenCode environment setup, compare the source `global/AGENTS.md`, `global/ENGINEERING.md`, `global/MEMORY.md` and `global/TOOLS.md` with files beside the effective user-global OpenCode rules. Do not overwrite personal files or assume the default configuration path.

Copy a missing conditional reference only after checking for an existing same-name file. For an existing customized reference, propose a small diff and preserve user rules; do not normalize it to the shared template. Add the conditional TOOLS router entry to the existing global AGENTS only when that reference is available. Do not embed every tool's installation procedure in AGENTS or preload all references at startup.

Changes to this GitHub repository do not update existing workstation copies. APM project dependency sync also does not own those copies. Record source revision and actual changed paths in the setup report, without creating a parallel tracking runtime. Missing optional TOOLS guidance does not block ordinary implementation using current project evidence.

# Maintainer tools

`tools/` contains deterministic repository-maintenance checks. It is not installed into projects and is not part of OpenCode or OMO runtime behavior.

## Static audit

```bash
python3 tools/audit.py
python3 tools/audit.py --json
```

`audit.py` is the stable entry point. The preserved implementation lives in `_audit_core.py`; the entry point supplies the current required/deprecated artifact policy, active `MEMORY.md` policy, retired History/Simple Memory rejection, and APM producer packaging checks.

The audit uses only the Python standard library. It checks:

- required repository/APM producer files and retired protocol/runtime artifacts;
- OpenCode Skill frontmatter, names, descriptions, and metadata shape;
- Skill ID uniqueness, complete lockfile file inventories, hashes, and trust/status metadata;
- operational Skill isolation;
- `.apm/skills/` completeness for every non-operational canonical Skill;
- absence of operational/unknown Skill IDs from the APM producer surface;
- complete file-set and byte/hash parity between `skills/<category>/<id>/` and `.apm/skills/<id>/`;
- absence of symlinks from APM Skill mirrors;
- byte parity for canonical `APM_SETUP`/`AGENT_SYNC` prompts and their `.apm/prompts/` mirrors;
- OMO JSONC example syntax, routing scope, and referenced Skill IDs;
- prompt mutation boundaries and `NOOP` behavior;
- local/authored Markdown links;
- packaged symlinks and Python cache artifacts.

Expected current packaging metrics are 31 deployable non-operational Skills and 9 excluded operational Skills. The audit derives these counts from the canonical `skills/` tree instead of hard-coding the IDs, so later catalog changes must update the APM surface consistently.

Warnings do not fail the command. Errors return a non-zero exit code.

A static PASS proves repository and packaging consistency only. It does not prove that a specific installed APM version actually deployed selected Skills, which target path won OpenCode discovery precedence, plugin compatibility, model behavior, OMO routing, Spec Kit execution, opencode-mem behavior, Plannotator feedback, AgentsView discovery, or project-specific outcomes. Use `evaluation/README.md`, `/apm-setup` or `/agent-sync`, and the relevant runtime smoke tests for those checks.

# Maintainer tools

`tools/` contains deterministic repository-maintenance checks. It is not installed into projects and is not part of OpenCode or OMO runtime behavior.

## Static audit

```bash
python3 tools/audit.py
python3 tools/audit.py --json
```

`audit.py` is the stable entry point. The preserved implementation lives in `_audit_core.py`; the entry point supplies the current required/deprecated artifact policy, including the active `MEMORY.md` policy and rejection of retired History/Simple Memory runtime artifacts.

The audit uses only the Python standard library. It checks:

- required repository files and retired protocol/runtime artifacts;
- OpenCode Skill frontmatter, names, descriptions, and metadata shape;
- Skill ID uniqueness, complete lockfile file inventories, hashes, and trust/status metadata;
- operational Skill isolation;
- OMO JSONC example syntax, routing scope, and referenced Skill IDs;
- prompt mutation boundaries and `NOOP` behavior;
- local/authored Markdown links;
- packaged symlinks and Python cache artifacts.

Warnings do not fail the command. Errors return a non-zero exit code.

A static PASS proves only repository consistency. It does not prove Skill discovery, plugin compatibility, model behavior, OMO routing, Spec Kit execution, opencode-mem behavior, Plannotator feedback, AgentsView discovery, or project-specific outcomes. Use `evaluation/README.md` and the relevant setup prompt smoke tests for those checks.

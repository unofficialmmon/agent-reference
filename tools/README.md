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

Expected current packaging metrics are 59 deployable non-operational Skills and 19 excluded operational Skills (78 total). The audit derives these counts from the canonical `skills/` tree instead of hard-coding the IDs, so later catalog changes must update the APM surface consistently.

Warnings do not fail the command. Errors return a non-zero exit code.

A static PASS proves repository and packaging consistency only. It does not prove that a specific installed APM version actually deployed selected Skills, which target path won OpenCode discovery precedence, plugin compatibility, model behavior, OMO routing, Spec Kit execution, opencode-mem behavior, Plannotator feedback, AgentsView discovery, or project-specific outcomes. Use `evaluation/README.md`, `/apm-setup` or `/agent-sync`, and the relevant runtime smoke tests for those checks.

## Quality, freshness, and regression tests

Python 3.10+ standard library only; these tools are maintainer-only, not consumer runtime dependencies.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/tests -v
python3 tools/quality.py
python3 tools/freshness.py
python3 tools/eval_gate.py
```

`audit.py` includes the quality registry/projection and evidence-schema checks plus the explicit evaluation instruction-file check. Tests cover valid inputs and failure cases; they do not run a coding model. Keep generated reports outside the checkout (CI uses `RUNNER_TEMP`) and disable bytecode so audit does not encounter self-generated artifacts.

`freshness.py --online` is an explicit read-only upstream check; see [catalog maintenance](../catalog/MAINTENANCE.md) for statuses, limits, and review policy. `quality.py --tooling-table` prints the deterministic README projection without modifying it.

`eval_gate.py --report <native-output.json> --context <run-context.json>` requires the actual AgentRC `--output` artifact, not its summary stdout. Capture context immediately before evaluation using `eval_gate.py --capture-context`; this records revision, suite/instruction hashes and timestamp, not a test result. The gate rejects missing, extra, duplicate, unknown, malformed, or stale-suite evidence and requires all cases to pass. Context mismatch or a missing report cannot pass. This is policy-response evidence only; OpenCode/OMO/APM host checks remain separate.

## Tool adoption maintainers

- `python3 tools/tool_catalog.py`: offline schema/ID/activation checks across runtime and adopted-tool catalogs.
- `python3 tools/tool_catalog.py --online`: read-only upstream metadata/commit/release observations; exit 2 for unresolved/partial results, never install/update.
- `python3 tools/capability_templates.py`: shipped-fragment policy checks, not arbitrary user-config validation.
- `python3 tools/smoke_ast_grep.py`: execute an already installed CLI on temporary structural fixtures.
- `node tools/smoke_playwright.cjs`: direct isolated MCP smoke using the explicitly supplied isolated `CAPABILITY_PREFIX` test installation.
- `python3 tools/smoke_security.py`: installed checker clean/negative/partial-staging tests; no source scan or package installation.

The main audit now includes adopted catalogs and MCP fragments. Tests cover both valid examples and rejected unsafe inputs. Fixture workflows own disposable-runner test dependency installation; these scripts are not workstation installers. Keep generated reports outside the repository and never attach unredacted findings or personal configuration.

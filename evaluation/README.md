# Behavioral evaluation

This directory separates deterministic repository checks from model/runtime behavior.

## Evidence classes

### Static

Run:

```bash
python3 tools/audit.py
```

Static checks verify files, metadata, hashes, references, prompt boundaries, and OMO examples. They do not prove that OpenCode loads content or that an agent follows it.

### Host smoke

Run after changing global/project AGENTS, installed Skills, OpenCode, or OMO Slim:

1. **Global injection** — ask the agent to summarize already-injected global rules without reading files.
2. **Simple-task non-interference** — perform one typo-only/mechanical edit; expect no broad planning, unrelated Skill use, or scope expansion.
3. **Project precedence** — request a small project-specific change; expect project `AGENTS.md` and maintained source to beat generic conventions.
4. **Skill discovery** — explicitly invoke one installed non-operational Skill and confirm it loads from the expected path.
5. **OMO routing** — restart OpenCode after routing changes, delegate one bounded implementation, and confirm the specialist can use only the intended project Skills.

If the user relies on runtime `/preset` switching, add one optional routing check: record effective Fixer/Designer Skill access before and after the switch. Current OMO startup and runtime preset merges are not identical, so do not infer runtime-switch behavior from static config parsing alone.

Record host version, OMO version, model, repository state, and observed result. A single smoke is compatibility evidence, not full certification.

### Behavioral regression

Use the cases in `agentrc.eval.jsonc` as a small reusable rubric. They cover:

- root-cause-first debugging;
- scope/complexity balance;
- generated-source ownership;
- relevant Skill selection;
- validation truthfulness;
- one-shot bootstrap and refresh/no-op behavior.

The cases may be evaluated manually or with AgentRC. AgentRC compares responses with and without instructions using a judge model; it is currently experimental and uses a Copilot-based runner, so its result is optional cross-agent evidence—not OpenCode/OMO runtime certification or a required release gate.

The bundled AgentRC cases are deliberately non-mutating planning/assessment prompts. Actual file edits, Skill loading, bootstrap, and routing behavior remain host-smoke responsibilities.

## Run discipline

- Use the same repository snapshot and prompt when comparing with/without references.
- Keep expected behavior observable; do not score hidden reasoning.
- For critical regressions, prefer two consistent runs before changing shared instructions.
- When a case fails, first identify whether the cause is global guidance, project guidance, a Skill, OMO routing, Spec Kit, model variance, or missing repository evidence.
- Do not add a new rule after one isolated failure.

## Minimal acceptance record

```text
Host:
OMO Slim:
Model:
Repository / commit:
Installed global references:
Installed project Skills:
Project OMO override:

Static audit: PASS | PASS_WITH_WARNINGS | FAIL
Global injection: PASS | FAIL | NOT RUN
Non-interference: PASS | FAIL | NOT RUN
Project precedence: PASS | FAIL | NOT RUN
Skill discovery: PASS | FAIL | NOT RUN
OMO routing: PASS | FAIL | NOT RUN
Behavioral cases: PASS | PARTIAL | FAIL | NOT RUN
Known limitations:
```

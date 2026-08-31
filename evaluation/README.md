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

### Plugin-stack smoke

Run after `prompts/OPENCODE_PLUGIN_SETUP.md` changes the user environment or after a material OpenCode/runtime upgrade:

1. **Resolved configuration** — start a fresh OpenCode process and confirm the effective configuration resolves without plugin-load errors.
2. **Safety Net** — use upstream diagnostics where available; confirm a representative safe Git command is allowed and a representative destructive command shape is blocked without damaging repository state.
3. **Simple Memory** — in a clean temporary directory, exercise `remember -> exact recall -> update -> exact recall -> forget`; confirm the test does not create deprecated History state or unexpected project artifacts.
4. **TokenScope** — run its normal report/command and confirm report output goes to the expected temporary/runtime location rather than dirtying the project. Record optional catalog/metadata fetch failures separately from the core report result.
5. **Notifier** — test the platform notification command/path. Distinguish command success from independently observing visual desktop delivery.
6. **Pilot/Hold discipline** — leave PTY blocked when the published release cannot be shown compatible with the active runtime/loader, and leave Hold candidates uninstalled unless their blocking risks were explicitly re-verified as resolved.

Record exact versions and the selected package/release. Do not convert a blocked pilot into a failure of the baseline stack.

#### Observed plugin-stack evidence — 2026-08-31

One macOS arm64/zsh run with OpenCode `1.18.25`, Bun `1.3.11`, Node `22.23.1`, and OMO Slim `2.2.17` observed:

- cc-safety-net `2.3.0` preserved and verified by its OpenCode doctor; safe Git remained usable and `git reset --hard` was blocked;
- Simple Memory `1.1.1` installed in manual mode and passed `remember -> recall -> update -> recall -> forget` in a cleaned temporary directory;
- TokenScope `1.8.1` preserved and `/tokenscope` completed with its report written to an OS temporary path; the smoke session could not fetch the optional Skill catalog;
- Notifier `0.2.8` preserved with noisy lifecycle/completion events disabled; the native macOS notification command succeeded, while visual desktop delivery was not independently observed;
- `opencode-pty` `0.3.6` remained `BLOCKED` because the published release could not be safely promoted past the Bun-native/Node-host loader risk in that environment;
- Snip and VibeGuard remained `HOLD`;
- no project `.opencode/` artifacts or deprecated `.opencode/history/` state were created.

This is compatibility evidence for that exact environment and date only. It is not a permanent certification of future OpenCode, OMO Slim, Bun/Node, or plugin releases.

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
Plugin stack: PASS | PARTIAL | FAIL | NOT RUN
Behavioral cases: PASS | PARTIAL | FAIL | NOT RUN
Known limitations:
```

# Behavioral evaluation

This directory separates deterministic repository checks from model/runtime behavior.

## Evidence classes

### Static

Run:

```bash
python3 tools/audit.py
```

Static checks verify files, metadata, hashes, references, prompt boundaries, and OMO examples. They do not prove that OpenCode loads content, that a plugin executes correctly, or that an agent follows guidance.

### Host smoke

Run after changing global/project AGENTS, installed Skills, OpenCode, or OMO Slim:

1. **Global injection** — ask the agent to summarize already-injected global rules without reading files.
2. **Simple-task non-interference** — perform one typo-only/mechanical edit; expect no broad planning, unrelated Skill use, or scope expansion.
3. **Project precedence** — request a small project-specific change; expect project `AGENTS.md` and maintained repository evidence to beat generic conventions and recalled memory.
4. **Skill discovery** — explicitly invoke one installed non-operational Skill and confirm it loads from the expected path.
5. **OMO routing** — restart OpenCode after routing changes, delegate one bounded task, and confirm the intended specialist and Skill policy are effective.
6. **Memory authority** — when a recalled/injected memory conflicts with current maintained source/config/tests, expect the current repository to win and the stale memory to be treated as context only.

If the user relies on runtime `/preset` switching, add one optional routing check: record effective Fixer/Designer Skill access before and after the switch. Do not infer runtime-switch behavior from static config parsing alone.

Record host version, OMO version, model, repository state, and observed result. A single smoke is compatibility evidence, not full certification.

### Tool-stack smoke

Run after `prompts/OPENCODE_PLUGIN_SETUP.md` changes the user environment or after a material OpenCode/runtime upgrade.

Distinguish OpenCode runtime plugins/integrations from standalone companions.

1. **Resolved configuration** — start a fresh OpenCode process and confirm the effective configuration resolves without plugin-load errors.
2. **OMO Slim** — complete one real Orchestrator-to-specialist delegation.
3. **Safety Net** — use upstream diagnostics where available; confirm a representative safe/read-only command is allowed and a representative destructive command shape is blocked without damaging repository state.
4. **RTK** — confirm the installed CLI/version and one representative OpenCode integration/rewrite path.
5. **Notifier** — confirm clean startup and a bounded notification path while preserving deliberate disabled/noisy-event choices.
6. **Retired plugins** — prove Simple Memory and TokenScope no longer load when they are being migrated out.
7. **opencode-mem load** — confirm plugin load and basic memory behavior.
8. **opencode-mem persistence** — create/use safe project memory in session A, end the OpenCode process/session, open fresh session B, and prove persistence/retrieval.
9. **opencode-mem automatic capture** — in a normal long-lived interactive session, allow the idle lifecycle to occur and prove an automatic memory record is created. A one-shot CLI process is not sufficient when it never reaches the plugin's normal idle capture path.
10. **opencode-mem fresh-session injection** — open another fresh project session and prove relevant prior context is injected without a mandatory manual recall/handoff step.
11. **Plannotator** — run a local/manual plan or document review and prove approval/feedback returns to the OpenCode agent. Exercise code review when relevant. Do not require remote sharing for the smoke.
12. **AgentsView** — outside the OpenCode plugin list, prove OpenCode session discovery and one usage/history/statistics read. Stop a daemon started only for validation unless the user wants it persistent.
13. **Pilot/Hold discipline** — do not promote `opencode-pty` or another held tool without current compatibility evidence; do not silently install rejected/held tools.

Configuration presence alone is not PASS for a runtime behavior claim.

### Observed current tool-stack evidence — 2026-09-02

One validated macOS environment observed:

- OpenCode `1.18.26` — startup PASS;
- OMO Slim `2.2.18` — PASS, including Orchestrator -> Explorer delegation;
- cc-safety-net `2.3.1` — PASS, including status and destructive-command analysis smoke;
- RTK `0.46.0` — PASS, CLI and OpenCode integration retained;
- OpenCode Notifier `0.2.8` — PASS, fresh plugin startup clean and deliberate disabled-event configuration retained;
- Simple Memory `1.1.1` — retired/removed from active global registry/config/cache;
- TokenScope `1.8.1` — retired/removed from active global registry/command wrapper/cache;
- opencode-mem `2.25.0` — PASS for load, fresh-session persistence, interactive automatic capture, and fresh-session auto-injection; project scope and loopback UI were used; the tested auto-capture provider was Z.AI `glm-5.3`;
- Plannotator `0.27.11` — PASS for the local/manual approval workflow and feedback return;
- AgentsView `0.42.0` — PASS for OpenCode discovery/usage; the validation daemon was stopped afterward;
- no `.opencode-mem-project` marker was needed for the single-repository project identity.

The validated stack intentionally separates responsibilities:

```text
OpenCode runtime
├─ OMO Slim          orchestration / subagents
├─ cc-safety-net     destructive-command guard
├─ RTK               command-output/token optimization
├─ opencode-mem      persistent project memory
├─ Notifier          notifications
└─ Plannotator       human plan/code review

External companion
└─ AgentsView        session/history/token/cost analytics
```

This is evidence for that exact environment/date, not permanent certification of future releases. Re-run the relevant smoke after material host/tool changes.

### Startup-failure isolation evidence

A startup error that mentioned low file descriptors was separately traced to a stale Herdr persistent background-server/macOS protected-folder access context: plain Terminal access worked, Herdr-hosted `ls`/Git/pwd returned `Operation not permitted`, and stopping the Herdr server restored normal behavior. The plugin stack subsequently passed.

Do not generalize this exact cause to every startup failure. The reusable lesson is to isolate terminal/background-host and filesystem-permission boundaries before applying extreme system-wide file-descriptor changes or blaming a plugin.

### Behavioral regression

Use the cases in `agentrc.eval.jsonc` as a small reusable rubric. They cover:

- root-cause-first debugging;
- scope/complexity balance;
- generated-source ownership;
- relevant Skill selection;
- validation truthfulness;
- repository authority over stale memory;
- one-shot bootstrap and refresh/no-op behavior.

The cases may be evaluated manually or with AgentRC. AgentRC compares responses with and without instructions using a judge model; it is optional cross-agent evidence, not OpenCode/OMO runtime certification or a required release gate.

The bundled AgentRC cases are deliberately non-mutating planning/assessment prompts. Actual file edits, Skill loading, plugin behavior, bootstrap, and routing remain host-smoke responsibilities.

## Run discipline

- Use the same repository snapshot and prompt when comparing with/without references.
- Keep expected behavior observable; do not score hidden reasoning.
- For critical regressions, prefer two consistent runs before changing shared instructions.
- When a case fails, first identify whether the cause is global guidance, project guidance, memory, a Skill, OMO routing, Spec Kit, model variance, a runtime plugin, terminal host, or missing repository evidence.
- Do not add a new rule after one isolated failure.

## Minimal acceptance record

```text
Host:
OpenCode:
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
Memory authority: PASS | FAIL | NOT RUN
Tool stack: PASS | PARTIAL | FAIL | NOT RUN
opencode-mem persistence: PASS | PARTIAL | FAIL | NOT RUN
opencode-mem auto-capture: PASS | PARTIAL | FAIL | NOT RUN
opencode-mem injection: PASS | PARTIAL | FAIL | NOT RUN
Plannotator: PASS | PARTIAL | FAIL | NOT RUN
AgentsView: PASS | PARTIAL | FAIL | NOT RUN
Behavioral cases: PASS | PARTIAL | FAIL | NOT RUN
Known limitations:
```

## V1 measured-quality checks

The suite explicitly sets `instructionFile` to `global/AGENTS.md`. Native AgentRC otherwise defaults to a Copilot instructions path and may silently compare against empty instructions when that file is absent. The maintainer gate rejects missing/empty instructions before a model is invoked.

The 17 cases are non-mutating policy-response assessments, not 17 proven host behaviors. Five cases cover scoped instructions, concurrent ownership, evidence-backed recommendations, absent optional Spec Kit, and audit evidence boundaries. These cross-agent results do not establish OpenCode V1 nested discovery, actual Skill loading, editing correctness, or plugin behavior.

### Native optional assessment

Use the manual `behavioral-eval` workflow only after providing an authorized Copilot evaluation token and explicitly accepting provider usage. Pull requests run CLI-contract checks without model credentials; model execution is never a side effect of a PR. The default workflow token is not assumed to grant Copilot access. The workflow pins the evaluated AgentRC revision and Copilot CLI version, uses Node 22, records context, and requires all cases to pass the native result gate.

For an already provisioned local AgentRC/Copilot environment, choose supported response/judge models explicitly and write outputs outside the checkout:

```bash
python3 tools/eval_gate.py --capture-context > /tmp/agentrc-context.json
agentrc eval evaluation/agentrc.eval.jsonc --repo "$PWD" \
  --model "$RESPONSE_MODEL" --judge-model "$JUDGE_MODEL" \
  --output /tmp/agentrc-native-results.json --fail-level 100 --json
python3 tools/eval_gate.py --report /tmp/agentrc-native-results.json \
  --context /tmp/agentrc-context.json
```

The context record binds revision, suite/instruction hashes, and capture time to the results being reviewed. It is not signed attestation. Never use an old successful artifact after changing instructions. Inspect trajectories and repeat material failures; compare the same repository, prompts, models, and tool versions for two consistent runs before claiming improvement. A threshold alone is not a measured improvement over a baseline.

AgentRC source contracts checked for this workflow: `microsoft/agentrc` revision `8d0c05c96dcfe674019359bcebd9ab6b251d2203`, `src/commands/eval.ts`, `packages/core/src/services/evaluator.ts`, and `package.json`. Its package requires Node 22 despite an older CI-doc prerequisite. `--json` stdout is a summary envelope; `--output` contains per-case responses, verdicts, and metrics.

### Evidence retention and privacy

`evidence/tool-stack-2026-09-02.json` transcribes the historical summary above. Unknown model/tested-revision values remain null; no new host PASS is claimed. Fresh host records must include redacted artifacts and their exact environment. Static schema validation cannot authenticate those observations.

Repository CI retains audit/test summaries and a source snapshot for reproduction. Native model responses/trajectories are not uploaded by default: they may contain repository or provider context. The optional workflow retains only gate status and context/version metadata. Keep sensitive transcripts local and explicitly review/redact anything selected for publication.

The expected follow-up host checks after adopting scoped/concurrency guidance are: applicable scoped-rule reading, out-of-scope non-interference, explicit writer ownership, integrated validation, and effective selected-Skill discovery. Mark them `NOT RUN` until actually exercised in the user's OpenCode/OMO/APM environment.

## Tool adoption verification

The 24 newly selected tools are policy entries, not 24 installation receipts. `tools/tool_catalog.py` validates the extended registries and can emit bounded upstream observations; `tools/capability_templates.py` validates shipped fragments only. Both are included in the static audit. [CAPABILITY_SMOKE.md](CAPABILITY_SMOKE.md) separates direct CLI/MCP checks from actual OpenCode/OMO host behavior.

`capability-smoke.yml` exercises installed ast-grep and isolated localhost Playwright MCP in a disposable runner. `automation-smoke.yml` exercises installed ShellCheck, Hadolint, Gitleaks and Trivy on clean/failing inert fixtures, including partial staging and redaction. These do not certify a consumer application, workstation install, CodeQL/App enrollment, recipe migration, or authenticated remote MCP calls. Gitleaks upstream's security-patch-only maintenance state is recorded in the project/tool guidance.

Use [TOOL_ADOPTION_PLAN.md](TOOL_ADOPTION_PLAN.md) for delivery scope and PR records. Preserve old evidence dates; never relabel historical PASS as a new host result. Missing credentials/host access and unexecuted model evaluations remain BLOCKED/NOT RUN.

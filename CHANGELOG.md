# Changelog

## Unreleased

### Added

- Added `global/MEMORY.md` as the `opencode-mem` persistent-context policy: automatic capture/injection by default, repository-state reconciliation, project-scope guidance, optional multi-repo identity, manual-memory exceptions, and explicit local-storage/remote-provider privacy boundaries.
- Added `prompts/OPENCODE_PLUGIN_SETUP.md` as a one-prompt, environment-aware setup/reconciliation workflow that re-verifies official upstreams before reconciling the recommended OpenCode tooling stack and records migration, runtime smoke tests, startup isolation, and rollback.
- Added `evaluation/README.md` with a minimal static-vs-behavioral UAT model and a non-mutating `evaluation/agentrc.eval.jsonc` as optional cross-agent judge input.
- Added zero-dependency maintainer-only `tools/audit.py` and `tools/README.md` for deterministic Skill/lock/template/prompt/license/link/eval checks, with machine-readable JSON output.
- Added `prompts/README.md` with copy-paste one-line entry requests for plugin/tooling setup, bootstrap, refresh, audit, onboarding, and change audit.
- Added APM producer metadata and synchronized `.apm/prompts/` packaging mirrors for `apm-setup` and the routine `agent-sync` prompt.
- Added `templates/omo/` with project-local OMO Slim Skill-routing examples for Java/Spring, Java/Spring/MyBatis, MyBatis+MBG, React/Vite, Next.js/React, Vue/Vite, Nuxt, and React Native plus a conditional routing guide.
- Added five bounded project convenience prompts:
  - `PROJECT_BOOTSTRAP.md` for initial project setup;
  - `PROJECT_REFRESH.md` for configuration reconciliation after repository change;
  - `PROJECT_AUDIT.md` for read-only agent-configuration review;
  - `CODEBASE_ONBOARD.md` for read-only repository orientation;
  - `CHANGE_AUDIT.md` for read-only acceptance review of a working-tree change.
- Added three explicitly activated engineering Skills after source, license, dependency, and scope review:
  - `bug-reproduction-brief`;
  - `refactor-plan`;
  - `verification-before-completion`.
- Added MIT attribution material for `github/awesome-copilot` and `obra/superpowers`.

### Improved

- Retired the interim Simple Memory/TokenScope baseline. Simple Memory's manual branch/worktree handoff (`remember`/exact recall/update, `handoff/<branch>`, single-writer OMO policy, project-local `.opencode/memory/`) is no longer active guidance; TokenScope is replaced by standalone AgentsView analytics.
- Made `opencode-mem` the active memory system. Routine work now relies on idle auto-capture and relevant fresh-session injection, while manual memory is reserved for immediate add/search/correction/migration and current Git/source/configuration/tests remain authoritative.
- Defined the current role-separated tooling policy: OMO Slim, cc-safety-net, RTK, Notifier, opencode-mem, and Plannotator are active runtime/integrations; AgentsView is an external local analytics companion; `opencode-pty` remains a compatibility-gated pilot; DCP, Snip, VibeGuard, Morph Fast Apply, and opencode-ignore are not baseline.
- Recorded current tool-stack host-smoke evidence for macOS on 2026-09-02: OpenCode `1.18.26`, OMO Slim `2.2.18`, cc-safety-net `2.3.1`, RTK `0.46.0`, Notifier `0.2.8`, opencode-mem `2.25.0`, Plannotator `0.27.11`, and AgentsView `0.42.0` passed their defined checks; opencode-mem fresh-session persistence, interactive auto-capture, and auto-injection all passed.
- Added startup-failure isolation guidance after a misleading low-file-descriptor error was traced to a stale Herdr background-server/macOS protected-folder access context rather than the OpenCode plugin stack.
- Removed the retired `.opencode/memory/` ignore from this repository and made the maintainer audit reject reintroduced Simple Memory runtime state alongside the already retired History artifacts.
- Split the static audit into the stable `tools/audit.py` policy entry point and preserved `tools/_audit_core.py` implementation so current required/deprecated artifact policy can evolve without rewriting the validated Skill/hash/OMO/link checks.
- Documented project-local OMO Slim configuration as an auto-loaded trust boundary that can alter agent behavior, tool access, and Skill access; bootstrap, refresh, audit, and evaluation guidance require explicit review and allowlist-preserving composition.
- Changed OMO stack examples to root `agents.<agent>.skills` overrides, reducing named-preset coupling while preserving user-owned models/MCPs. Documented that runtime `/preset` switching uses separate merge behavior and requires its own routing smoke check when used.
- Clarified that OMO agent `skills` arrays are effective allowlists, so bootstrap/refresh must preserve deliberate existing entries rather than assuming additive merge behavior.
- Normalized `activationGuidance` across all 40 Skill lock entries so project-stack, conditional, workflow-gate, and operational selection are machine-readable.
- Added bootstrap/refresh `NOOP` behavior and aligned project `AGENTS.md` generation with OpenCode `/init` quality goals: concise facts, real commands, and only targeted clarification.
- Extended `PROJECT_BOOTSTRAP.md` and `PROJECT_REFRESH.md` to configure only minimal project-local OMO Slim Skill routing while preserving global models, variants, MCPs, companion settings, prompts, and unrelated permissions.
- Extended `PROJECT_AUDIT.md` to detect stale/missing routed Skill IDs, operational Skill leakage, global-config duplication, JSONC precedence issues, and OMO doctor/schema failures.
- Added OMO routing quality rules: existing config format is preserved, templates are evidence-based examples rather than profiles, Orchestrator/global policy is inherited by default, and OpenCode restart is required before behavioral smoke testing.
- Re-audited the pack against current OpenCode Skill/rule discovery, Spec Kit integration management, awesome-copilot, and Superpowers guidance.
- Made bootstrap and refresh resolve catalog/Skill paths from the containing `agent-reference` root and fail safely when that source is unavailable.
- Required complete-directory, byte-preserving Skill copies so references, scripts, assets, and license files are not dropped.
- Added mutation checkpoints before force, overwrite, deletion, duplicate-Skill replacement, or material constitution changes.
- Switched existing Spec Kit maintenance guidance to native `integration status` and manifest-aware `integration upgrade`; `init --here --force` remains initial setup/fallback only.
- Added stale CodeGraph/search-index safeguards across global/project references and read-only prompts.
- Clarified that a passing command proves only the surface it exercises and that verification completion is not verification success.
- Added explicit activation boundaries for reproduction-only, plan-only, and completion-gate workflow Skills.
- Added limited local smoke evidence for OpenCode `1.18.24` + OMO Slim `2.2.17` without overstating it as full certification.
- Reconciled `catalog/skills.lock.json` with all 40 catalog Skills and materialized provenance, integrity, compatibility, activation, risk, known-issue, and redistribution fields.
- Recorded retained upstream reference/rendering issues without modifying the pinned snapshots.

### Reviewed but not vendored

- `acquire-codebase-knowledge` — excluded because reviewed quality reports did not consistently pass Agent Skill metadata compliance; `CODEBASE_ONBOARD.md` covers the narrow read-only need.
- `systematic-debugging` — excluded because its upstream workflow depends on broader Superpowers TDD behavior that this pack does not adopt globally.
- Broad planning, structured-autonomy, and review-and-refactor workflows — excluded where Spec Kit/OMO already own the responsibility or where the workflow would add unnecessary ceremony or scope.

### Deferred

- Additional APM-based distribution beyond the existing bounded prompt package remains intentionally conservative until the reference content and onboarding process are stable in real use.

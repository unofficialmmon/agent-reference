# Changelog

## Unreleased

### Added

- Added `evaluation/README.md` with a minimal static-vs-behavioral UAT model and a non-mutating `evaluation/agentrc.eval.jsonc` as optional cross-agent judge input.
- Added zero-dependency maintainer-only `tools/audit.py` and `tools/README.md` for deterministic Skill/lock/template/prompt/license/link/eval checks, with machine-readable JSON output.
- Added `prompts/README.md` with copy-paste one-line entry requests for bootstrap, refresh, audit, onboarding, and change audit.
- Added APM producer metadata and synchronized `.apm/prompts/` packaging mirrors for `apm-setup` and the routine `agent-sync` prompt.
- Added `templates/omo/` with project-local OMO Slim Skill-routing examples for Java/Spring, Java/Spring/MyBatis, MyBatis+MBG, React/Vite, Next.js/React, Vue/Vite, Nuxt, and React Native plus a conditional routing guide.

- Added five bounded convenience prompts:
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

- Changed work-history handling from opt-in/existing-directory gated to lazy default-on for qualifying project work: global routing now loads `HISTORY.md` at handoff time and creates/updates `.opencode/history/` on the first qualifying change unless the user or project rules explicitly opt out or override the location.
- Documented project-local OMO Slim configuration as an auto-loaded trust boundary that can alter agent behavior, tool access, and Skill access; bootstrap, refresh, audit, and evaluation guidance now require explicit review and allowlist-preserving composition.
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

- APM-based multi-project distribution remains intentionally deferred until the reference content and onboarding process are stable in real use.

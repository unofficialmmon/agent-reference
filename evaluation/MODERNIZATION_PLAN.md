# V1 measured-quality implementation plan

Date: 2026-09-10
Base: `2ad0496d3c9a2fd4d6b16c95e5b0c9943197d2a6`
Scope: maintainer tooling and bounded reference improvements; OpenCode V2 is excluded.

## Invariants

Keep this repository a static reference/APM producer, not an installer, stack detector, agent runtime, or orchestration framework. Preserve all vendored Skill bytes and exact APM mirrors. Keep zero global Skills by default, project selection under APM ownership, operational Skills opt-in, and Spec Kit optional. Do not change the user's local machine or automatically upgrade dependencies.

## Planned work

1. P0: strengthen deterministic regression tests and evaluation evidence contracts; add an explicit, credential-gated native AgentRC evaluation path. Distinguish test-runner correctness, model evaluation, and OpenCode host behavior.
2. P0: add read-only Skill freshness reporting using existing provenance; unknown review dates stay unknown. Upstream changes are review candidates, never automatic snapshot updates.
3. P0: centralize tooling policy and structured historical smoke evidence, with consistency checks against maintained documentation.
4. P1: add conditional module-scoped AGENTS guidance, explicit shared-worktree write ownership, and evidence-backed Skill recommendations to existing prompts without creating a detector or installer.
5. P1: validate registry/evidence/configuration consistency and extend CI to run positive and negative regression tests, retaining inspectable audit artifacts.
6. Document adoption, limitations, actual validation, and rollback in the PR and repository. Defer composite Skill scores, new plugins, analytics ingestion, and SBOM automation until their additional maintenance cost is justified.

## Acceptance

- Existing full static audit still passes, with pre-existing warnings kept visible.
- Tests reject malformed/unknown evidence, false PASS claims, registry drift, and unsafe freshness inputs.
- Network failures never mean CURRENT; metadata migration never fabricates a review or runtime PASS.
- Canonical Skill contents and APM Skill mirrors are unchanged.
- Native AgentRC and OpenCode host tests are reported NOT RUN or BLOCKED when their runtime/authentication is unavailable; deterministic CI must not claim they ran.
- GitHub branch/PR contains the implementation and real validation output. No direct forced update of main; no merge while required checks fail.

## Validation sequence

Review repository rules and upstream command contracts; establish baseline; implement bounded changes; run unit/negative tests and full audit; inspect the diff and hashes; run GitHub CI; publish exact checks and remaining host-specific proof in the PR.

Implementation status and exact check results will be recorded after execution, not predicted here.

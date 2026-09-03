# Skill Sources and Trust Model

`agent-reference` is a curated source catalog. A Skill being included does not mean it is globally active or locally behavior-tested.

## Claims are separated

Use `skills.lock.json` as the machine-readable source of truth.

- `sourceTrust` — who supplied the content.
- `integrity` — whether the vendored bytes are pinned/hash-verified.
- `hostCompatibility` — OpenCode static format vs runtime discovery smoke.
- `behaviorStatus` — upstream claim/local static review vs locally observed behavior.
- `activationGuidance` — whether a Skill is a project-stack capability, conditional contract/generated guidance, an explicit workflow gate, or an operational opt-in.
- `operationalRisk` — network, credential, process, browser, deployment/destructive, or executable effects.
- `knownIssues` — unresolved upstream limitations recorded without modifying the snapshot.
- `redistributionStatus` — license/redistribution evidence status.

Do not summarize all of these as simply "verified".

Current activation values are intentionally coarse and auditable:

- `project-stack-only` — install only in a repository that actually uses the matching stack;
- `conditional-api-contract-work` — select only when an HTTP/API contract boundary is in scope;
- `conditional-generated-source-work` — select only when generator/tool-owned source exists;
- `explicit-reproduction-only`, `explicit-plan-only`, `explicit-completion-gate` — invoke only for that bounded workflow;
- `explicit-opt-in-operational` — requires explicit task-specific review/authorization.

## Snapshot policy

- Upstream snapshots are kept byte-for-byte unchanged from the reviewed source snapshot.
- Never patch an upstream Skill locally to fix prose, links, examples, or behavior.
- Upgrade by replacing the full Skill directory with a reviewed pinned revision and recomputing hashes/metadata.
- If an upstream issue prevents safe use, keep the snapshot as reference with a recorded `knownIssues` entry or exclude it from activation until replaced.
- Local behavior belongs in a distinct local Skill ID.

## Trust classes

### `official-vendor`

Content from an organization that owns or maintains the relevant product/framework/service.

Current sources include:

- `anthropics/skills`
- `cloudflare/skills`
- `MariaDB/skills`
- `redis/agent-skills`
- `supabase/agent-skills`
- `hashicorp/agent-skills`
- `vercel/next.js`
- `vercel-labs/agent-skills`

Official source improves provenance; it does **not** prove OpenCode runtime compatibility or suitability for every project.

### `maintainer-community`

Content from established maintainers or focused ecosystem projects rather than a vendor-wide official source.

Current sources include:

- `antfu/skills`
- `vueuse/skills`
- `AvdLee/*-Agent-Skill`
- `badlogic/pi-skills`
- `github/awesome-copilot` narrow community-contributed Skills retained only after repository quality/spec review
- `obra/superpowers` narrow Skills retained only when they are independently usable without adopting the full methodology

Some of these sources explicitly describe themselves as experimental. Treat source quality and runtime behavior as separate questions.

### `official-doc-derived`

Local narrow Skills curated from official technical documentation in the prior pi-dev-kit:

- `spring-boot`
- `spring-security`
- `maven-build`
- `mybatis`
- `mybatis-dynamic-sql`
- `mybatis-generator`

These are not official vendor Skill snapshots. They are local summaries whose source material was official documentation.

### `local-derived`

Repository-authored Skills:

- `api-contract`
- `generated-code`
- `java-style`

They are intentionally marked local and must not be presented as upstream behavior-validated content.

## Operational isolation

`skills/operational/` contains Skills that can involve consequential actions or dependencies, including browser/profile access, scripts, MCP/tools, local-server automation, deployment, cloud credentials, migrations, infrastructure creation/deletion, profiling, or source rewriting.

Operational Skills require explicit selection. Their presence in the repository is not permission to execute their actions.

## Known upstream issues retained unchanged

The current pinned catalog records, among others:

- `vueuse-functions` — several relative documentation links target paths not present in the vendored snapshot; upstream project is experimental.
- `vercel-react-best-practices` — its upstream `AGENTS.md` has relative links to three rule files not present in the vendored snapshot; its upstream `README.md` also contains a nested triple-backtick example that may render incorrectly. The runtime `SKILL.md` is unaffected.
- Vercel Labs agent-skills snapshots — MIT licensing was declared by the upstream repository at review time, but the vendored Skill directories did not contain a preserved top-level upstream LICENSE file. See `catalog/LICENSES/vercel-labs-agent-skills-LICENSE-EVIDENCE.md`.

These files are not silently patched because that would turn them into local forks.

## Newly reviewed narrow external Skills

The following are included as selectable catalog content, never as default global activation:

- `github/awesome-copilot` `bug-reproduction-brief` — current GitHub quality reports show spec-compliance and valid-reference PASS. Explicit reproduction-only workflow: it stops before diagnosis/repair.
- `github/awesome-copilot` `refactor-plan` — current GitHub quality report shows spec-compliance and valid-reference PASS. Explicit plan-only workflow: it pauses for confirmation even when implementation was requested, and its TypeScript/npm examples must be adapted to the repository.
- `obra/superpowers` `verification-before-completion` — explicit completion gate with evidence-before-claims discipline. Upstream open issues about outcome/instrument coverage are retained in lockfile `knownIssues`; it is not treated as proof that every verification instrument is sufficient.

## Evaluated but not vendored

- `github/awesome-copilot` `acquire-codebase-knowledge` — not vendored because repeated 2026 quality reports fail Agent Skill spec compliance: `metadata.enhancements` is non-string. `prompts/CODEBASE_ONBOARD.md` provides a smaller read-only convenience flow without copying that Skill.
- `obra/superpowers` `systematic-debugging` — not vendored because the upstream Skill explicitly depends on `superpowers:test-driven-development` and `superpowers:verification-before-completion`. The TDD dependency mandates test-first behavior for every feature/bugfix/refactor, which is intentionally not an ambient agent-reference policy. Copying only part of that dependency graph would misrepresent upstream behavior.
- `github/awesome-copilot` broad planning/structured-autonomy/review-and-refactor workflows — not vendored because Spec Kit/OMO already own those responsibilities or because the workflows would introduce unnecessary ceremony/scope expansion.

Add a candidate only after source/license/dependency/risk review. Prefer an immutable revision; when exact upstream revision capture is unavailable, record the local content hash and the limitation explicitly rather than claiming immutable upstream pinning.

## Locally observed compatibility evidence

A limited local smoke run on OpenCode `1.18.24` with OMO Slim `2.2.17` observed global-rule injection, non-interference on a typo-only edit, project-rule priority/clarification behavior, and discovery/loading of the `java-style` Skill.

This evidence is intentionally narrow. It does not certify every Skill, prompt, model, repository, or later host version. The lockfile records runtime evidence only for the specific entry where it was directly observed; other entries remain static-review or upstream-claim status until tested.

## License material

- Root `LICENSE` covers repository-authored content unless a file says otherwise.
- Upstream Skill license files remain inside snapshots when supplied.
- Consolidated source license/attribution material is under `catalog/LICENSES/`.
- Root `NOTICE` maps included sources and highlights incomplete standalone license evidence.

## 2026-09 reviewed expansion sources

Pinned snapshots were added from Android, Expo, Flutter, Vercel/Next.js, Vercel Labs, affaan-m/ECC, wshobson/agents, Kadajett/agent-nestjs-skills, sickn33/agentic-awesome-skills, and vuejs-ai/skills. Exact revisions, paths, file hashes, licenses, risk placement, and activation guidance are recorded in `skills.lock.json`.

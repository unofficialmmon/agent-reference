# OMO Slim Skill routing guide

Use this as a candidate map only. Repository evidence and installed Skill availability decide the final routing. Project examples use root `agents.<agent>.skills` to avoid coupling checked-in stack routing to one named preset during normal startup. If the project uses runtime `/preset` switching, verify effective Skill routing after the switch; use preset-local routing when different presets intentionally require different Skill policies.

## Default routing policy

OMO Slim bundled workflow Skills (for example `simplify`, `codemap`, `deepwork`, `verification-planning`, `reflect`, and `worktrees`) remain owned/installed by OMO Slim. Do not vendor duplicate copies into a project just to route them.

An agent `skills` array is an effective allowlist. Before writing a project override, inspect the effective user/project policy and preserve any intentional non-operational entries that should remain; do not assume the project list appends automatically.


| Agent | Default project-local behavior |
|---|---|
| Orchestrator | Do not override; inherit the global wildcard/policy. |
| Oracle | Do not override by default; keep `simplify` and other global policy intact. Add review/verification Skills only when deliberately selected. |
| Librarian | No technology Skills by default. |
| Explorer | No technology Skills by default. |
| Designer | Add frontend/UI Skills only for projects where design/UI work is in scope. |
| Fixer | Add only implementation Skills proven relevant to the repository. |
| Observer | No project Skill routing unless a concrete use appears. |

## Stack candidates

### Java / Spring Boot / Maven

Fixer candidates:

- `java-style`
- `spring-boot`
- `maven-build`

Conditional:

- `spring-security` — only when Spring Security/authentication/authorization is actually present.
- `api-contract` — only when HTTP/API contract work exists.
- `generated-code` — only when generator-owned output exists.

### MyBatis add-on

Fixer candidates:

- `mybatis`
- `mybatis-dynamic-sql` — only when the repository actually uses Dynamic SQL.
- `mybatis-generator` — only when MBG configuration/tasks/generated ownership exist.
- `generated-code` — when MyBatis/MBG output is generator-owned.

### React + Vite

Fixer candidates:

- `vite`
- `vercel-react-best-practices`
- `vercel-composition-patterns`
- `pnpm` — only when pnpm is the package manager.
- `vitest` — only when Vitest is configured/used.
- `api-contract` — only when frontend API contract work is materially in scope.

Designer candidates:

- `frontend-design`
- `vercel-react-best-practices`
- `vercel-composition-patterns`

Optional/explicit:

- `vercel-react-view-transitions` — only when View Transitions are actually being implemented.

### Next.js / React

Fixer candidates:

- `vercel-react-best-practices`
- `vercel-composition-patterns`
- `pnpm` — only when pnpm is used.
- `api-contract` — only when API contract work is materially in scope.

Designer candidates:

- `frontend-design`
- `vercel-react-best-practices`
- `vercel-composition-patterns`

Do not auto-select the operational `next-cache-components-optimizer`; use it only for an explicit cache-components optimization task after reviewing its side effects and dependencies.

### Vue + Vite

Fixer candidates:

- `vue`
- `vite`
- `pinia` — only when Pinia is present.
- `vueuse-functions` — only when VueUse is present or deliberately being adopted.
- `pnpm` — only when pnpm is used.
- `vitest` — only when Vitest is configured/used.

Designer candidates:

- `frontend-design`
- `vue`

### Nuxt

Fixer candidates:

- `nuxt`
- `vue`
- `pinia` — only when present.
- `vueuse-functions` — only when present or deliberately adopted.
- `pnpm` — only when pnpm is used.

Designer candidates:

- `frontend-design`
- `vue`
- `nuxt`

Do not add the operational `next-cache-components-optimizer` merely because a frontend framework is present.

### React Native

Fixer/Designer candidate:

- `vercel-react-native-skills`

Do not add web-only frontend Skills automatically.

### Database add-ons

Use only when the repository actually owns or tunes the relevant datastore:

- MariaDB: `mariadb-features`, `mariadb-query-optimization`
- Redis: `redis-core`, `redis-connections`
- Supabase/Postgres: `supabase-postgres-best-practices`

Database Skills normally belong to Fixer. Do not install all database Skills just because a dependency appears transitively.

## Explicit workflow Skills

These are not stack defaults:

- `bug-reproduction-brief` — explicit reproduction-only work.
- `refactor-plan` — explicit multi-file refactor planning.
- `verification-before-completion` — explicit completion-evidence check.

Orchestrator already has wildcard access in the common global configuration, so project-local specialist routing is unnecessary unless the project intentionally standardizes one of these workflows.

## Operational boundary

Never auto-route `skills/operational/*`. These may execute tools, access browsers/profiles, run local services, deploy, mutate infrastructure, or depend on credentials. Require explicit user authorization for the specific Skill and task.
OMO routing is not a security boundary by itself. Use OpenCode `permission.skill` (`ask`/`deny`) when consequential Skill loading needs an explicit gate.

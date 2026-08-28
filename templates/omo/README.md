# OMO Slim project-local Skill-routing templates

These files are **reviewed examples**, not profiles to copy blindly.

Project-local `.opencode/oh-my-opencode-slim.json[c]` is auto-loaded by OMO Slim and can change agent behavior, tool access, and Skill access. Treat it as trusted executable configuration: review project changes before running OpenCode, and do not adopt OMO configuration from an untrusted repository.

They intentionally use root `agents.<agent>.skills` overrides instead of a named preset so repository stack routing remains separate from user-owned model/MCP policy. Current OMO startup/config-file merging gives root agent entries precedence over the selected preset. Runtime `/preset` switching follows a separate merge path, so routing must be smoke-tested after a runtime switch when that workflow matters.

## Rules

1. Inspect the repository and the actually installed Skill IDs before choosing an example.
2. Inspect the existing project and user OMO Slim configuration. Never write the user/global config during project setup.
3. Keep the project file minimal: Skill routing only unless the user explicitly requests another project-specific OMO change.
4. Preserve models, variants, MCPs, companion, multiplexer, permissions, custom agents, prompt files, and unrelated settings. Treat each `skills` array as an effective allowlist, not an additive patch: carry forward any intentional existing non-operational Skill entries that must remain.
5. If `.opencode/oh-my-opencode-slim.json` or `.jsonc` already exists, merge into that file; do not create a competing format.
6. Write only Skill IDs that are discoverable after setup.
7. Remove conditional example Skills that the repository does not use.
8. Never install or route `skills/operational/*` automatically.
9. Do not vendor OMO bundled Skills. OMO owns their installation and update.
10. OMO routing does not replace OpenCode `permission.skill`; keep consequential/operational Skill access at `ask` or `deny` where appropriate.
11. Restart OpenCode after changing OMO Skill routing before judging behavior.

## Why root `agents.*`

OMO Slim deep-merges user and project configuration. During startup/config-file preset resolution, root `agents.*` entries override conflicting preset agent fields. Using root `agents.*` for ordinary project Skill routing therefore:

- avoids duplicating the user's active preset name;
- avoids coupling the checked-in example to one named preset at startup;
- keeps project concerns separate from user-owned model/MCP configuration;
- makes the override's intent explicit.

Use a preset-local override only when Skill routing is intentionally different for one preset. Record that reason rather than converting templates mechanically.

## Examples

- `java-spring.jsonc` — Java + Spring Boot + Maven baseline.
- `java-spring-mybatis.jsonc` — adds plain MyBatis.
- `java-spring-mybatis-mbg.jsonc` — adds MBG and generated ownership. Add `mybatis-dynamic-sql` separately only when the repository actually uses Dynamic SQL.
- `react-vite.jsonc` — React + Vite baseline.
- `nextjs-react.jsonc` — Next.js/React baseline; no operational cache optimizer.
- `vue-vite.jsonc` — Vue + Vite baseline.
- `nuxt.jsonc` — Nuxt/Vue baseline.
- `react-native.jsonc` — React Native baseline.

`PROJECT_BOOTSTRAP.md` and `PROJECT_REFRESH.md` should read `ROUTING.md`, use the nearest example only as a candidate, and produce the smallest evidence-backed project override.

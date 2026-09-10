# Scoped project guidance and Skill recommendations

This is a bounded reference for bootstrap, refresh, and read-only project audit. It is not a stack detector, installer, or substitute for native OpenCode/APM behavior.

## Module instructions only when needed

Keep one root AGENTS file when the project is small or module rules are the same. Add a module-local `AGENTS.md` only when maintained source demonstrates a distinct stack, build command, ownership boundary, contract, or hazard. Do not split files merely to imitate a directory tree.

The root file should name the scoped file, its directory, and when to read it. Before a change, read the root and the applicable ancestor/module instructions; do not load unrelated module instructions. More-specific rules refine that scope, not unrelated modules. Conflicts involving contracts, security, or ownership require investigation, not silent precedence guessing. Preserve valid existing child instructions and user edits.

Do not assume nested automatic injection in an untested OpenCode V1 configuration. Explicit on-demand reading through the root router is the fallback. A static path check is not runtime-injection proof. Verify one in-scope and one out-of-scope example on the actual host before claiming automatic routing works.

## Recommendations backed by repository facts

For a new or changed Skill selection, record a compact mapping in the working report:

| Evidence | Candidate | Reason / decision |
|---|---|---|
| Concrete maintained path and dependency/config symbol | Exact catalog ID | Select, retain, or omit; explain relevant boundary |

Inspect actual dependencies, configuration, source usage, and task scope. A `pom.xml` alone does not prove Spring Boot, Spring Security, MyBatis, or MariaDB. An auth boundary may justify security guidance without proving a specific framework. Transitive, example-only, or retired dependencies are not automatic activation signals.

Check `activationGuidance`, source risk, and producer availability. Recommend only the narrowest justified IDs. Recommendations do not install, auto-route, or delete Skills. Apply approved changes through existing APM ownership; preserve documented overrides and never enable operational Skills by inference. Do not create a persistent parallel selection manifest.

## Concurrent changes

Read-only exploration may run in parallel. Before any parallel writes, identify each writer's files and shared contracts. Overlapping files, lockfiles, generated outputs, migrations, and shared test fixtures require a single writer or serialization. Disjoint filenames do not prove semantic independence.

For substantial independent mutations, use native Git worktrees when authorized and available. Worktrees separate files, not ports, databases, credentials, or external services; isolate those explicitly. Do not force-clean worktrees or create commits/merges as an implicit consequence of delegation. The coordinator reviews the integrated diff and runs combined relevant validation; separate subagent PASS reports are not integration proof.

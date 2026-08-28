# Engineering Reference

Stable global defaults for implementation, debugging, architecture, review, formatting, linting, and validation. Project rules and actual repository contracts take precedence.

Use only the sections relevant to the current task. This document is a decision reference, not a mandatory checklist and not permission to expand a small change into architecture review, refactoring, or extra process.

## 1. Decision order

Use this order for engineering trade-offs:

1. Correct scope and contract.
2. Stability, safety, and predictable failure.
3. Simplicity and maintainability.
4. Verification appropriate to risk.
5. Extensibility, reuse, and optimization only when evidence justifies them.

Establish the requested scope first. Apply simplicity inside that scope; do not use minimalism to redefine or omit required behavior.

Prefer proven solutions. A newer pattern, framework, abstraction, or dependency is not an improvement unless it solves a demonstrated problem at acceptable cost.

## 2. Fix causes, not symptoms

A fix should remove or contain the cause at its owning boundary, not merely silence the visible symptom.

Avoid these families of failure:

- **Patch fixes:** band-aid fixes, ad hoc workarounds, symptom-oriented fixing, whack-a-mole debugging.
- **Masking:** exception swallowing, fail-safe masking, fallback abuse, retry-as-a-fix.
- **Wrong-boundary fixes:** fixing the wrong layer, local fix/global complexity, fixing the wrong problem.
- **Exception accumulation:** special-case accumulation, exception-driven architecture, patchwork architecture.

Before changing code for a bug or failure:

1. Reproduce or establish the failing behavior when practical.
2. Read the actual error and trace the relevant data/control path.
3. Identify which component owns the violated invariant or contract.
4. Form one evidence-backed cause hypothesis.
5. Fix the owning cause with the smallest change that preserves the established scope.
6. Rerun the same failing check or scenario before broadening verification.

If several independent patches have failed, stop adding exceptions and reconsider the model, invariant, boundary, or architecture.

Retries are for known transient failures and must be bounded. Fallbacks are for deliberate degraded operation, not for hiding an invalid state.

## 3. Make invalid states difficult to represent

Prefer a clear owning boundary over repeated defensive checks everywhere.

Avoid:

- validation everywhere for conditions already guaranteed at a trusted boundary;
- defensive programming abuse for impossible states without evidence;
- invalid-state accommodation that normalizes corrupted or contradictory state;
- boolean explosion that permits mutually inconsistent combinations;
- flag-argument abuse that turns one API into several unrelated behaviors;
- magic values or strings when a stable closed semantic set exists.

Validate untrusted/external input at the system boundary. Keep business invariants at the layer that owns them. Do not duplicate the same guarantee through every function unless trust actually changes between boundaries.

When a state should never occur, prefer preventing or exposing it over returning `null`, empty values, warnings, or generic success.

## 4. Keep responsibilities and state visible

Prefer explicit ownership, data flow, and side effects.

Watch for:

- hidden global/external state;
- hidden side effects;
- temporal coupling that depends on undocumented call order;
- circular dependencies;
- god classes/objects;
- spaghetti control flow;
- big-ball-of-mud boundaries;
- shotgun surgery where a small change requires many unrelated edits.

A component should have a coherent reason to change. State-changing operations should be visible from the API, name, boundary, or transaction model.

Do not introduce a new layer merely to make architecture diagrams more symmetrical.

## 5. Abstract from evidence

Abstraction exists to reduce change cost or enforce a real boundary, not to make code look sophisticated.

Avoid:

- premature abstraction;
- speculative generality;
- abstraction for abstraction's sake;
- wrong abstractions that couple concepts that change for different reasons;
- DRY abuse and DRY at the expense of locality;
- indirection hell;
- wrapper-on-wrapper designs;
- dependency-injection overuse;
- unnecessary provider/hook/registry/plugin extension points;
- premature frameworkization.

Accept small local duplication when the shared concept is not yet stable. Extract after a repeated semantic pattern and ownership boundary are clear.

Prefer one concrete implementation when only one real implementation exists. Add interfaces, registries, factories, adapters, or plugins when they solve actual variation, isolation, ownership, or testing needs—not hypothetical ones.

## 6. Resist speculative complexity

Avoid framework-first thinking, golden hammers, cargo-cult programming, architecture astronautics, YAGNI violations, and overengineering.

Do not convert ordinary behavior into a configuration language without a concrete need. Watch for configuration explosion and `config-driven everything`, where possible combinations become harder to reason about than code.

Do not turn a focused component into a Swiss Army knife through accumulating modes and options.

Choose an existing mature library or standard when it solves the problem better than a new internal framework. Do not reinvent the wheel without a concrete limitation in the existing solution.

## 7. Control accumulation

Complexity should be removable as well as addable.

Avoid:

- dead-code accumulation;
- lava-flow code whose purpose can no longer be explained;
- permanent compatibility shims with no known consumer;
- special-case and configuration accumulation;
- complexity ratchets where every requirement adds structure but nothing is retired;
- feature creep and scope creep.

Preserve backward compatibility where real users/contracts depend on it. Do not preserve compatibility forever merely because an old path once existed. Removal must be evidence-based and deliberate.

Refactoring is scoped work. During a feature or fix, perform only local cleanup required for correctness or safe implementation unless broader refactoring is explicitly in scope.

## 8. Dependencies and technology

Add a dependency only when its functional value exceeds its maintenance, security, compatibility, operational, and replacement cost.

Prefer repository-proven technology. Introduce a new technology when the current approach has a demonstrated limitation or the new option materially reduces risk/cost.

For unfamiliar or high-impact technology, validate on a realistic bounded use case before broad adoption.

## 9. Performance

Consider performance early for known hot paths, high data volume, network/disk access, memory pressure, or strict latency requirements.

Avoid premature optimization. Optimize from a requirement or measurement, protect correctness with tests, and keep unusual optimized code localized and documented.

## 10. Contracts and generated code

Protect public APIs, IPC contracts, stored data, schemas, serialized formats, and external integrations unless change is explicitly intended.

Do not infer human architecture from generated source. Generated source is authoritative only for what its generator actually owns: generated schema/type/query/client details and related configuration.

When generated/tool-owned output must change, prefer changing its contract/schema/configuration and regenerating. Never treat generation completion as proof that business implementation is complete.

Use the `api-contract` and `generated-code` Skills when those boundaries are relevant.

## 11. Errors and recovery

Classify failures instead of handling every error identically.

- Reject invalid input clearly.
- Preserve a core workflow only when degraded operation is explicitly safe.
- Fail fast when continuing can corrupt or spread invalid state.
- Retry only transient failures with bounded policy.
- Never report success for failed work.

During incidents, balance restoration with containment. Protect data/security before restoring service when continued operation can cause damage.

## 12. Testing and validation

Test according to risk and contract importance, not test count.

Prioritize:

1. user-visible scenarios and contracts;
2. failure/exception paths;
3. state transitions and invalid/boundary input;
4. security/auth/data-integrity behavior;
5. ordinary happy paths.

Run the closest check that proves the actual change. A syntax/format check does not prove behavior; a unit test does not prove deployment; API tests do not prove backward compatibility unless the comparison was actually performed.

A passing command proves only the surface it actually exercises. When a zero-result, success flag, or clean report is decisive, confirm that the instrument could detect the relevant failure or explain why its coverage is sufficient. For consequential side effects, inspect the resulting state through an independent path when practical instead of trusting only the tool's success return.

Report evidence honestly:

- **ACTUAL PASS / ACTUAL FAIL** — a command or scenario was really executed;
- **STATIC** — inspected without execution;
- **NOT RUN** — relevant but not executed;
- **BLOCKED** — could not be executed because of an external/pre-existing constraint.

Completing the verification process is not the same as all checks passing.

## 13. Formatting and linting

Formatting must improve consistency without becoming a hidden refactor.

Precedence:

1. explicit user instruction;
2. project `AGENTS.md`;
3. committed formatter/linter/editor configuration;
4. maintained local code conventions;
5. relevant language/framework Skill;
6. this section.

Rules:

- Use the project's formatter/linter rather than fighting it manually.
- Limit cleanup to active files/scope; avoid whole-repository cosmetic churn.
- Do not rename, move, redesign APIs, rewrite control flow, change DTO semantics, or add abstractions as part of formatting-only work.
- Preserve readable structure in JSON/YAML/TOML/XML/scripts; do not compact nested structure just to reduce lines.
- Keep command stages readable; do not join commands with `&&`/`;` merely to save lines.
- Remove in-scope unused imports/variables, wildcard imports, obvious debug output, empty catch blocks, and swallowed exceptions unless project policy says otherwise.
- Prefer parameterized logging; never log secrets or unnecessary personal data.
- Never manually format generated/vendor code when its owner/tool should regenerate it.

Language-specific details belong in the relevant Skill or project rules, not this global document.

## 14. Security and sensitive operations

Give stronger review to authentication/authorization, secrets, personal/confidential data, external input, process execution, file/network access, database migrations, deployment, and destructive operations.

Do not expose passwords, tokens, cookies, credentials, private hosts, or personal data in source, logs, fixtures, documentation, or responses.

Never weaken a security boundary merely to make a test pass.

## 15. Observability, documentation, and technical debt

Keep enough operational evidence to reconstruct important failures without turning logging into noise. Record operation/category/context needed for diagnosis, but never secrets or unnecessary personal data.

Document information code cannot express reliably: public contracts, architecture/security boundaries, recovery procedures, irreversible decisions, and intentionally unusual behavior. Prefer clear names and structure over comments that restate obvious code.

Make accepted technical debt visible when it affects risk or future change. Record the limitation, impact, and a concrete resolution trigger rather than relying on an indefinite TODO. Prioritize debt by operational/security/data-integrity risk and repeated change cost.

## 16. AI-generated changes

Treat AI-generated code as untrusted until checked against repository reality.

Verify that it:

- solves the requested problem rather than a nearby one;
- uses APIs/files/settings that actually exist;
- respects current contracts and ownership;
- does not add speculative layers or silent fallbacks;
- includes proportional tests/validation;
- does not hide failed or unverified work.

For high-risk contract, DB, auth/security, deployment, or destructive changes, require clear scope and validation criteria before implementation.

## 17. Completion

Work is verified complete only when the requested behavior is implemented within the agreed scope, no known unacceptable risk is hidden, and required validation has actually passed.

If a relevant check is `ACTUAL FAIL`, the work is not verified complete. If required validation is `NOT RUN` or `BLOCKED`, completion is partial or blocked for that scope; state the exact unverified boundary instead of using overall-success wording.

A concise completion report should state what changed, what was actually validated, any failed/not-run/blocked checks, and material remaining risk.

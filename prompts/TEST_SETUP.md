# `test-setup`

**Description:** Establish a small, trustworthy testing portfolio from static/unit evidence through real end-to-end Critical Journeys

Prepare the current repository with a practical, maintainable testing environment that provides trustworthy evidence from isolated logic through the real end-to-end system boundary.

This is a testing-infrastructure and test-portfolio setup task. It may modify test source, test dependencies, test profiles/source sets, test fixtures, test orchestration, test scripts, CI test configuration, and the project-specific Testing section of `AGENTS.md` when required. Do not change production business behavior merely to make tests pass.

The goal is **not** maximum test count, maximum line coverage, or one separate suite per testing label.

The goal is:

> Establish every testing responsibility applicable to the architecture with small, representative executable evidence, and finish with at least one real Critical Journey through the actual system boundary when E2E is applicable.

## Scope

This prompt is self-contained testing setup guidance. Project facts remain authoritative, and existing repository testing tools should be reused when they already provide the required evidence.

## Safety and authority

Use this order:

1. explicit user instruction;
2. project-root `AGENTS.md`;
3. maintained project contracts/specifications;
4. current source, tests, schemas, build/configuration, and CI;
5. project-local conventions and selected Skills;
6. this prompt and generic testing guidance.

Start with:

```bash
git status --short
```

Preserve dirty user work and unrelated changes.

Do not reset, clean, stash, or overwrite existing test infrastructure merely to obtain a uniform layout.

Before materially replacing an existing test framework, existing orchestration topology, overlapping dirty test/config files, or a maintained CI test path, show one concise mutation checkpoint and preserve the current mechanism unless repository evidence justifies replacement.

Do not commit or push unless explicitly requested.

---

# 1. Understand the project before choosing tools

Inspect only enough maintained material to establish:

- language/runtime and build system;
- modules and deployable applications;
- public client/backend entry points;
- Gateway/BFF/API routing;
- service-to-service boundaries;
- databases and canonical schema authority;
- Redis/cache;
- queues/brokers;
- external APIs;
- authentication/authorization boundaries;
- generated contracts/schemas;
- current test frameworks and source sets;
- current test commands and build profiles;
- current Docker/Testcontainers/Compose/test orchestration;
- current CI test stages;
- existing fixtures/seeds and local prerequisites.

Classify existing tests by what they actually execute, not by filename or directory name alone.

Do not assume `*IT`, `*E2E`, `integration/`, or `e2e/` accurately describes the boundary without inspecting it.

Produce a concise architecture/test topology before writing new infrastructure.

Example only:

```text
Client
  |
Gateway
  |
  +--> Core --> MariaDB
  |
  +--> Cargo --> Redis
```

---

# 2. Use two dimensions: responsibilities and coverage goals

Testing **responsibilities** describe the boundary from which evidence is obtained:

- Static
- Unit
- Integration
- Contract
- Component
- System
- E2E

Coverage **goals** describe the risk to protect, for example:

- Endpoint Completeness
- Critical Journey Coverage
- Cross-service Collaboration
- Schema/Data Fidelity
- Security Boundary

Do not conflate these dimensions.

A single executable test may provide evidence for more than one testing responsibility or coverage goal.

---

# 3. Define the testing responsibilities

## Static

Question:

> Is the code structurally valid?

Use the repository's actual format/lint/compile/typecheck/build/static-analysis commands.

Static validation is a quality gate, not behavioral proof.

## Unit

Question:

> Does an isolated piece of business/domain logic behave correctly?

Prefer Unit tests for:

- business rules;
- calculations;
- validation;
- state transitions;
- pure transformations;
- important edge cases that do not require infrastructure.

Do not unit-test trivial framework behavior or simple getters/setters solely to increase coverage.

## Integration

Question:

> Does an important technical boundary work against the real dependency whose semantics matter?

Typical examples:

- repository ↔ real database;
- cache adapter ↔ Redis;
- producer/consumer ↔ broker;
- filesystem integration;
- persistence/query mapping;
- infrastructure-specific serialization/transactions.

Prefer disposable real infrastructure where practical.

Do not replace meaningful persistence/infrastructure evidence with mocks merely because mocks are faster.

## Contract

Question:

> Do independently evolving components still honor their compatibility boundary?

Examples:

- HTTP/OpenAPI;
- gRPC;
- event/message schemas;
- service producer/consumer wire formats.

Contract **responsibility** is applicable when an independently evolving compatibility boundary exists.

A dedicated contract **framework** is not automatically required.

Existing maintained schema validation, focused producer/consumer boundary tests, or another executable compatibility mechanism may satisfy the responsibility when it can detect the claimed incompatibility.

For independently deployed or versioned producers/consumers, prefer explicit contract validation that can fail before full-system E2E.

## Component

Question:

> Does one deployable application work as a complete component?

For a server this may include:

- actual application bootstrap;
- controller/HTTP boundary;
- security/filter chain when relevant;
- serialization;
- service/domain behavior;
- persistence;
- real disposable infrastructure when relevant.

Remote services may be stubbed when the component is intentionally tested in isolation.

## System

Question:

> Do real backend deployables collaborate correctly?

Exercise the actual services needed to prove the collaboration being claimed.

System tests should normally cover only a small number of high-value cross-service flows.

## E2E

Question:

> Can a real client/business Critical Journey enter through the actual system boundary and reach a meaningful final outcome?

For backend-only systems, API E2E through the public Gateway/API is valid when it traverses the real production-like backend path.

For systems with a browser/mobile client, E2E may extend to the UI when that client boundary is part of the required acceptance evidence.

E2E must remain intentionally small and representative.

---

# 4. Do not create one suite per label by default

Each applicable testing responsibility must have:

1. a clear responsibility;
2. representative executable evidence.

A separate test suite is **not required** when an existing test provides the same boundary evidence without reducing diagnosability.

Evidence may satisfy more than one responsibility.

For example, a request that:

- enters the real public Gateway;
- traverses real Core/Cargo services; and
- verifies the meaningful final state

may provide both **System** and **backend E2E** evidence.

Classify the test by its **primary purpose**, not by JUnit, REST Assured, Testcontainers, Docker, folder name, or class suffix.

Do not duplicate the same scenario solely to create separate `System` and `E2E` labels.

---

# 5. Separate Endpoint Completeness from E2E Critical Journeys

Endpoint completeness and E2E journey coverage are separate goals.

## Endpoint Completeness

Endpoint completeness verifies the maintained API surface at the **lowest-cost layer that actually exercises the contract being claimed**.

Do not treat a mocked service-method Unit test as proof that an HTTP method/path/status/request/response contract works.

When the user or project rules explicitly require all-API validation:

1. build an endpoint inventory from the maintained API authority plus current routing/source;
2. account for every maintained method + path;
3. identify relevant request shape, response shape, status behavior, auth boundary, and compatibility-sensitive error behavior;
4. cover every endpoint at an appropriate lower-cost meaningful layer;
5. record intentional exclusions/deprecated/internal endpoints explicitly.

Do **not** force every endpoint into E2E.

## Critical Journey Coverage

E2E verifies a small number of representative real workflows.

Choose Critical Journeys based on business risk and real system topology, for example:

- authenticate → primary business action → verify final state;
- create → retrieve → verify persistence/cross-service result;
- one important authorization failure;
- one other materially critical workflow when justified.

Do not copy the endpoint inventory into the E2E suite.

---

# 6. Assess current evidence before implementing

Create a matrix such as:

| Responsibility | Purpose | Existing evidence | Status | Missing risk |
|---|---|---|---|---|
| Static | structural validity | `<command>` | READY/PARTIAL/MISSING/N/A | `<risk>` |
| Unit | isolated logic | `<tests>` | ... | ... |
| Integration | real technical boundary | `<tests>` | ... | ... |
| Contract | compatibility | `<evidence>` | ... | ... |
| Component | one deployable | `<test>` | ... | ... |
| System | service collaboration | `<test>` | ... | ... |
| E2E | Critical Journey | `<test>` | ... | ... |

Use `N/A` only when the architecture genuinely has no such boundary.

Do not mark a missing or inconvenient test layer `N/A` simply to avoid building it.

A large number of test files does not imply `READY`.

---

# 7. READY has a strict evidence requirement

A testing responsibility is `READY` only when:

1. its responsibility is explicitly defined;
2. at least one representative executable test provides the required evidence; and
3. that test has actually run successfully in the **current repository state**.

Use the following distinctions honestly:

- `READY` — representative evidence ran successfully now;
- `PARTIAL` — useful evidence exists but does not fully prove the responsibility;
- `MISSING` — required responsibility has no meaningful evidence;
- `BLOCKED` — evidence cannot currently run because of a concrete blocker;
- `NOT RUN` — test/evidence exists but was not executed now;
- `N/A` — the architecture genuinely has no such boundary.

`testCompile PASS` is not `test PASS`.

Successful dependency resolution, application startup, test discovery, or compilation is not successful behavioral execution unless that is the actual claim being made.

---

# 8. Design the smallest representative portfolio

Build broad responsibility coverage with minimal duplication.

## Unit

Use detailed cases for important logic branches and edge conditions.

## Integration

Cover infrastructure semantics most likely to regress, especially:

- custom SQL/query behavior;
- persistence mappings;
- transactions;
- cache behavior;
- broker behavior;
- infrastructure-specific adapters.

## Contract

Protect compatibility-sensitive producer/consumer boundaries. Do not add Pact/Spring Cloud Contract merely to have a "Contract" folder.

## Component

Use representative service-level flows proving the deployable actually boots and handles meaningful requests through its important internal boundaries.

## System

Keep only representative multi-service collaboration flows.

## E2E

Keep only representative Critical Journeys.

The same business permutation should not be reimplemented at every layer.

---

# 9. Java / Spring default tool policy

For Java/Spring repositories, prefer the existing project stack first.

When compatible and missing, use the following small core as the default candidate set:

## JUnit 5

Primary runner/test structure.

Reuse the project's existing assertion library, commonly AssertJ or JUnit assertions.

## REST Assured

Prefer for real HTTP evidence at:

- Component;
- System;
- backend/API E2E.

Do not use REST Assured merely to make a Unit test appear higher-fidelity.

## Testcontainers

Prefer for disposable real infrastructure such as:

- MariaDB/PostgreSQL;
- Redis;
- Kafka/RabbitMQ;
- other infrastructure whose real semantics matter.

Testcontainers may also orchestrate service containers when that is simpler and more reproducible than another topology mechanism.

Do not containerize every component automatically.

## Supporting tools

Use only when project evidence supports them:

- Spring Boot Test;
- Mockito;
- AssertJ;
- MockMvc for focused MVC tests;
- WireMock for intentionally stubbed remote HTTP services.

When the claimed evidence includes the real HTTP server boundary, prefer actual HTTP on a real/random port over MockMvc-only evidence.

## Dedicated contract frameworks

Spring Cloud Contract or Pact are conditional.

Before adding one, inspect:

- existing OpenAPI/schema authority;
- producer/consumer independence;
- deployment/versioning model;
- existing contract/boundary evidence;
- whether a dedicated framework would materially catch incompatibility earlier.

Do not add both without a concrete requirement.

---

# 10. Database synchronization policy

Use the project's **canonical repository schema authority** as the default test source of truth.

This may be:

- Flyway migrations;
- Liquibase changelogs;
- maintained DDL/schema files;
- another repository-owned schema authority.

Policy:

1. canonical repository schema authority is the default test schema source;
2. deterministic repository-owned test seed data is preferred;
3. database dumps/backups are for schema-drift investigation, compatibility/migration validation, or recovery when no maintained canonical schema exists;
4. do not use a developer's shared database dump as the default E2E fixture;
5. mutation System/E2E must use a disposable or explicitly isolated database;
6. do not silently treat a shared staging/production-like database as disposable test state.

If local-only authentication/bootstrap seed material is required:

- identify it as a prerequisite;
- document how to obtain or generate it;
- document where it belongs;
- document the exact test command that consumes it;
- do not claim clean-checkout reproducibility while the prerequisite remains undocumented.

Project-specific image-build/schema/seed commands belong in the project's maintained Testing documentation, not in this generic prompt.

---

# 11. Test data and isolation

Prefer small explicit fixtures created by the test or deterministic repository-owned seeds.

Avoid dependencies on:

- arbitrary developer-local rows;
- test execution order;
- mutable shared staging data;
- huge opaque dumps as the normal path;
- uncontrolled wall-clock time;
- hidden machine-specific files.

Use fixture builders/factories only where they materially improve clarity.

Do not build a large internal testing framework for a small portfolio.

---

# 12. Authentication and security evidence

When auth/security is a meaningful boundary, cover it at the lowest appropriate level and retain representative real-boundary evidence.

Representative higher-level evidence normally includes only high-value cases such as:

- valid authentication;
- missing/invalid authentication;
- one important authorization restriction.

Detailed permission combinations should generally live in lower-cost focused tests rather than being multiplied through E2E.

---

# 13. Choose one maintainable System/E2E orchestration model

Use the simplest reproducible mechanism that matches current architecture.

## Testcontainers

Prefer when:

- disposable infrastructure is important;
- service images already exist or are natural build artifacts;
- lifecycle/network control from the test runner is practical;
- per-run isolation is useful.

## Docker Compose

Prefer an existing maintained Compose topology when many real services already start together there and duplicating it in Testcontainers would create a second topology source.

## Existing project-native mechanism

Prefer an existing healthy harness over introducing a parallel mechanism.

Do not maintain equivalent service topology independently in Testcontainers, Compose, and shell scripts without a concrete reason.

---

# 14. Record clean-checkout prerequisites and commands

The final testing environment must clearly document what is required to reproduce System/E2E from a clean checkout.

Record, when applicable:

- required application/package builds;
- required Docker image build/tag commands;
- canonical schema/migration application;
- deterministic seed/bootstrap inputs;
- local-only auth fixtures and how to obtain/generate them;
- service host mappings;
- required environment variables without embedding secrets in documentation;
- exact test profile/command;
- required Docker/runtime tooling.

Do not hide a required manual prerequisite behind an unexplained failure.

---

# 15. Expose clear project-native commands

Use the repository's natural build system and existing conventions.

The final project should make the applicable evidence discoverable, for example conceptually:

```text
Static       -> <real command>
Unit         -> <real command>
Integration  -> <real command>
Contract     -> <real command/evidence>
Component    -> <real command/evidence>
System       -> <real command/evidence>
E2E          -> <real command/evidence>
Full acceptance -> <real command or documented sequence>
```

Do not create a different Maven/Gradle profile for every responsibility when shared commands/source sets provide clearer evidence.

A responsibility may point to the same command/test as another responsibility when the same executable evidence genuinely proves both.

---

# 16. Establish the normal AI coding test cycle

Future implementation work should use a risk-based cycle:

```text
Understand change
      |
Identify realistic regression risk
      |
Select lowest-cost evidence that proves it
      |
Run focused tests
      |
Run affected boundary evidence
      |
Run required static/build gates
      |
Run System/E2E when the changed risk crosses those boundaries
```

Examples are guidance, not mandatory mappings:

- business-rule change -> focused Unit + required static/build;
- SQL/MyBatis/persistence change -> relevant Unit + real Integration + static/build;
- service API compatibility change -> Contract evidence + affected lower layers + Component as needed;
- Gateway/auth/routing change -> Component + representative System/backend-E2E evidence;
- cross-service business workflow change -> affected lower layers + System + relevant Critical Journey E2E.

Do not blindly run every expensive layer after every mechanical edit.

Do not skip high-level acceptance evidence when the change actually affects the real system path.

---

# 17. CI integration

Inspect existing CI before changing it.

If this task is expected to leave the testing environment CI-ready and the repository already has maintained CI, integrate the new commands minimally.

Prefer staged feedback rather than an oversized matrix:

- Fast: Static + Unit;
- Boundary: relevant Integration/Contract/Component;
- Acceptance: representative System/E2E.

Adapt stages/frequency to actual execution cost and repository rules.

Do not weaken existing mandatory checks.

If CI ownership or environment prerequisites cannot be resolved safely, leave CI unchanged and report the setup as locally executable with CI integration `BLOCKED` or `NOT RUN` rather than guessing.

---

# 18. Flaky-test policy

Treat flakiness as a testing-system defect.

Do not normalize:

- arbitrary sleeps;
- blind retries;
- ignored failures;
- order dependence;
- permanent quarantine of critical scenarios without root-cause tracking.

When eventual consistency/timing is intrinsic, prefer bounded condition-based waiting over fixed sleeps.

Do not hide unstable tests behind success wording.

---

# 19. Update project testing documentation

After the setup is working, update the project `AGENTS.md` with only durable project-specific testing facts.

Do not copy this prompt wholesale into the project.

Recommended shape:

```md
## Testing

### Topology and responsibilities

- Static — `<responsibility/evidence>`
- Unit — `<responsibility/evidence>`
- Integration — `<real boundaries/evidence>`
- Contract — `<contract authority/evidence or N/A reason>`
- Component — `<deployables/evidence>`
- System — `<topology/evidence>`
- E2E — `<Critical Journeys/evidence>`

### Coverage goals

- Endpoint completeness: `<scope/authority or not required>`
- Critical Journeys: `<small representative list>`
- Schema/data authority: `<path/mechanism>`
- Security boundary: `<important evidence>`

### Commands and prerequisites

- Static: `<command>`
- Unit: `<command>`
- Integration: `<command>`
- Contract: `<command/evidence>`
- Component: `<command/evidence>`
- System: `<command/evidence>`
- E2E: `<command/evidence>`
- Full acceptance: `<command or sequence>`
- Prerequisites: `<image/seed/runtime/local-only requirements>`

### Selection rule

Use the lowest-cost test that proves the changed risk. Do not duplicate the same assertion at every layer. Endpoint completeness and E2E Critical Journeys are separate goals.
```

Only document commands/evidence that actually exist.

---

# 20. Validate the setup itself

Do not stop after creating dependencies, source sets, or test files.

Execute representative evidence for every applicable responsibility where the environment permits it.

Report independently:

```text
Static       READY / PARTIAL / MISSING / BLOCKED / NOT RUN / N/A
Unit         READY / PARTIAL / MISSING / BLOCKED / NOT RUN / N/A
Integration  READY / PARTIAL / MISSING / BLOCKED / NOT RUN / N/A
Contract     READY / PARTIAL / MISSING / BLOCKED / NOT RUN / N/A
Component    READY / PARTIAL / MISSING / BLOCKED / NOT RUN / N/A
System       READY / PARTIAL / MISSING / BLOCKED / NOT RUN / N/A
E2E          READY / PARTIAL / MISSING / BLOCKED / NOT RUN / N/A
```

Remember:

> A responsibility is READY only when its purpose is explicit, representative executable evidence exists, and that evidence ran successfully in the current repository state.

If one executed test provides both System and backend E2E evidence, it may make both responsibilities READY when it genuinely proves both. Do not create a duplicate solely for the table.

If the user required full API validation, also report endpoint inventory coverage separately from E2E Critical Journey coverage.

---

# Completion criteria

The setup is complete when, for the actual architecture:

1. testing responsibilities and coverage goals are documented separately;
2. every applicable responsibility has clear executable evidence, without forcing unnecessary separate suites;
3. detailed logic is protected at low cost;
4. infrastructure-sensitive behavior uses real disposable dependencies where meaningful;
5. independently evolving contracts have meaningful compatibility evidence;
6. important deployables have Component-level evidence where useful;
7. multi-service collaboration has representative System evidence where applicable;
8. at least one real Critical Journey reaches the actual system boundary and passes when E2E is applicable;
9. endpoint completeness, when required, is tracked independently from E2E journeys;
10. canonical repository schema authority is used by default for test databases;
11. mutation System/E2E uses disposable or explicitly isolated data;
12. local-only prerequisites are documented with reproducible commands;
13. the portfolio avoids redundant copies of the same scenario across labels;
14. project-native commands are documented;
15. actual execution results are reported honestly using the READY rule;
16. production behavior and unrelated user work were not changed merely to satisfy the testing setup.

Do not describe the testing environment as complete while an applicable E2E path is still unimplemented or unexecuted unless the user explicitly scoped E2E out.

---

# Final report

Report only:

1. detected architecture and deployables;
2. previous evidence matrix;
3. resulting responsibility/evidence matrix;
4. coverage goals, including endpoint completeness separately from Critical Journeys;
5. tools reused and tools added;
6. representative tests/evidence created;
7. database/schema/seed strategy;
8. System/E2E orchestration and any evidence shared between them;
9. commands and clean-checkout prerequisites established;
10. `AGENTS.md`/CI changes;
11. actual validation executed;
12. `READY`, `PARTIAL`, `MISSING`, `BLOCKED`, `NOT RUN`, or `N/A` items;
13. files changed;
14. remaining material testing risks.

Keep the final report concise.

The target is not "many tests."

The target is a small, trustworthy portfolio that covers the full applicable path from isolated logic to a real Critical Journey.

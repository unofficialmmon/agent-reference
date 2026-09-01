---
description: Establish or reconcile a small, trustworthy testing portfolio through real end-to-end Critical Journeys.
---

# test-setup

Prepare the current repository with a practical, maintainable automated testing environment.

The goal is not maximum test count, arbitrary coverage percentages, or one separate suite for every testing label.

The goal is:

> Establish every testing responsibility applicable to the architecture with small, representative executable evidence, and finish with at least one real Critical Journey through the actual system boundary when E2E is applicable.

This is a repository mutation task. It may modify test source, test dependencies, test profiles/source sets, fixtures, orchestration, test scripts, CI test configuration, and the project-specific Testing section of `AGENTS.md` when required. Do not change production business behavior merely to make tests pass.

## Authority and safety

Use this priority:

1. explicit user instruction;
2. project-root `AGENTS.md`;
3. maintained project contracts/specifications;
4. current source, tests, schemas, build/configuration, and CI;
5. project-local conventions and selected Skills;
6. this prompt and generic testing guidance.

Start with `git status --short` and preserve dirty user work and unrelated changes.

Do not reset, clean, stash, overwrite unrelated files, replace a healthy testing stack without evidence, or commit/push unless explicitly requested.

Before materially replacing an existing framework, orchestration topology, dirty test/config file, or maintained CI test path, preserve the current mechanism unless repository evidence justifies replacement.

## 1. Inspect the current project

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

Classify existing tests by what they actually execute, not by filename or directory name alone. Do not assume names such as `*IT`, `*E2E`, `integration/`, or `e2e/` prove the boundary.

Produce a concise architecture/test topology before adding infrastructure.

## 2. Separate testing responsibilities from coverage goals

Testing responsibilities describe the boundary from which evidence is obtained:

- Static
- Unit
- Integration
- Contract
- Component
- System
- E2E

Coverage goals describe the risk being protected, for example:

- Endpoint Completeness
- Critical Journey Coverage
- Cross-service Collaboration
- Schema/Data Fidelity
- Security Boundary

Do not conflate these dimensions. One executable test may provide evidence for more than one responsibility or coverage goal.

## 3. Responsibility definitions

### Static

Question: Is the code structurally valid?

Use the repository's actual format, lint, compile, typecheck, build, and static-analysis commands. Static validation is a quality gate, not behavioral proof.

### Unit

Question: Does an isolated piece of business/domain logic behave correctly?

Prefer Unit tests for business rules, calculations, validation, state transitions, pure transformations, and important infrastructure-free edge cases.

Do not unit-test trivial framework behavior or getters/setters merely to increase coverage.

### Integration

Question: Does an important technical boundary work against the real dependency whose semantics matter?

Typical examples include repository to database, cache adapter to Redis, producer/consumer to broker, persistence/query mapping, filesystem integration, transactions, and infrastructure-specific serialization.

Prefer disposable real infrastructure where practical. Do not replace meaningful persistence/infrastructure evidence with mocks merely because mocks are faster.

### Contract

Question: Do independently evolving components still honor their compatibility boundary?

Typical boundaries include HTTP/OpenAPI, gRPC, event/message schemas, and service producer/consumer wire formats.

Contract responsibility is applicable when an independently evolving compatibility boundary exists. A dedicated Pact or Spring Cloud Contract suite is not automatically required.

Existing maintained schema validation, focused producer/consumer boundary tests, or another executable compatibility mechanism may satisfy the responsibility when it can detect the incompatibility being claimed.

For independently deployed or versioned producers and consumers, prefer explicit contract validation that can fail before full-system E2E.

### Component

Question: Does one deployable application work as a complete component?

For a server this may include actual application bootstrap, HTTP/controller boundary, security/filter chain, serialization, service/domain behavior, persistence, and real disposable infrastructure where relevant.

Remote services may be stubbed when the component is intentionally tested in isolation.

### System

Question: Do real backend deployables collaborate correctly?

Exercise the actual services required to prove the collaboration. Keep System tests to a small number of high-value cross-service flows.

### E2E

Question: Can a real client/business Critical Journey enter through the actual system boundary and reach a meaningful final outcome?

For backend-only systems, API E2E through the public Gateway/API is valid when the request traverses the real production-like backend path.

For systems with a real browser/mobile client, E2E may extend to that UI when the client boundary is part of required acceptance evidence.

E2E must remain intentionally small and representative.

## 4. Do not create one suite per label

Each applicable testing responsibility must have:

1. a clear responsibility; and
2. representative executable evidence.

A separate test suite is not required when an existing test provides the same boundary evidence without reducing diagnosability.

Evidence may satisfy more than one responsibility.

For example, one request that enters the real public Gateway, traverses real Core/Cargo services, and verifies meaningful final state may provide both System and backend E2E evidence.

Classify a test by its primary purpose, not by JUnit, REST Assured, Testcontainers, Docker, folder name, or class suffix.

Do not duplicate the same scenario solely to create separate System and E2E labels.

## 5. Separate Endpoint Completeness from E2E Critical Journeys

Endpoint completeness and E2E journey coverage are separate goals.

### Endpoint Completeness

Endpoint completeness verifies the maintained API surface at the lowest-cost layer that actually exercises the contract being claimed.

Do not treat a mocked service-method Unit test as proof that HTTP method/path/status/request/response behavior works.

When the user or project rules explicitly require all-API validation:

1. build an endpoint inventory from the maintained API authority plus current routing/source;
2. account for every maintained method and path;
3. identify relevant request shape, response shape, status behavior, auth boundary, and compatibility-sensitive errors;
4. cover every endpoint at an appropriate lower-cost meaningful layer;
5. record intentional exclusions, deprecated endpoints, and internal-only endpoints explicitly.

Do not force every endpoint into E2E.

### Critical Journey Coverage

E2E verifies a small number of representative real workflows.

Choose Critical Journeys based on business risk and actual topology, for example:

- authenticate -> primary business action -> verify final state;
- create -> retrieve -> verify persistence/cross-service result;
- one important authorization failure;
- another materially critical workflow only when justified.

Do not copy the endpoint inventory into the E2E suite.

## 6. Assess existing evidence before implementation

Build an evidence matrix:

| Responsibility | Purpose | Existing evidence | Status | Missing risk |
|---|---|---|---|---|
| Static | structural validity | `<command>` | READY/PARTIAL/MISSING/N/A | `<risk>` |
| Unit | isolated logic | `<tests>` | ... | ... |
| Integration | real technical boundary | `<tests>` | ... | ... |
| Contract | compatibility | `<evidence>` | ... | ... |
| Component | one deployable | `<test>` | ... | ... |
| System | service collaboration | `<test>` | ... | ... |
| E2E | Critical Journey | `<test>` | ... | ... |

Use `N/A` only when the architecture genuinely has no such boundary. Do not mark a missing or inconvenient responsibility `N/A` simply to avoid building it.

A large number of test files does not imply READY.

## 7. READY requires fresh execution evidence

A testing responsibility is `READY` only when:

1. its responsibility is explicitly defined;
2. at least one representative executable test provides the required evidence; and
3. that test has actually run successfully in the current repository state.

Use these states honestly:

- `READY` - representative evidence ran successfully now;
- `PARTIAL` - useful evidence exists but does not fully prove the responsibility;
- `MISSING` - required responsibility has no meaningful evidence;
- `BLOCKED` - evidence cannot run because of a concrete blocker;
- `NOT RUN` - evidence exists but was not executed now;
- `N/A` - the architecture genuinely has no such boundary.

`testCompile PASS` is not `test PASS`.

Dependency resolution, application startup, test discovery, or compilation is not successful behavioral execution unless that is the actual claim being made.

## 8. Build the smallest representative portfolio

Use detailed cases at lower-cost layers and representative collaboration/journeys at higher layers.

- Unit: important logic branches and edge cases.
- Integration: infrastructure semantics most likely to regress, such as custom SQL, mappings, transactions, cache, broker, and adapters.
- Contract: compatibility-sensitive producer/consumer boundaries.
- Component: representative service-level flows proving one deployable boots and handles meaningful requests.
- System: representative multi-service collaboration flows only.
- E2E: representative Critical Journeys only.

Do not reimplement the same business permutation at every layer.

## 9. Java/Spring default tool policy

For Java/Spring repositories, reuse the existing project stack first.

When compatible and missing, use this small default candidate set:

### JUnit 5

Use as the primary runner/test structure. Reuse the project's current assertion library, commonly AssertJ or JUnit assertions.

### REST Assured

Prefer for real HTTP evidence at Component, System, and backend/API E2E layers.

Do not use REST Assured merely to make a Unit test appear higher-fidelity.

### Testcontainers

Prefer for disposable real infrastructure such as MariaDB/PostgreSQL, Redis, Kafka/RabbitMQ, and other infrastructure whose real semantics matter.

Testcontainers may also orchestrate service containers when that is simpler and more reproducible than another topology mechanism. Do not containerize every component automatically.

### Supporting tools

Use only when project evidence supports them:

- Spring Boot Test;
- Mockito;
- AssertJ;
- MockMvc for focused MVC tests;
- WireMock for intentionally stubbed remote HTTP services.

When the claimed evidence includes the real HTTP server boundary, prefer actual HTTP on a real/random port over MockMvc-only evidence.

### Dedicated contract frameworks

Spring Cloud Contract and Pact are conditional. Before adding one, inspect the existing OpenAPI/schema authority, producer/consumer independence, deployment/versioning model, existing boundary evidence, and whether a dedicated framework catches incompatibility materially earlier.

Do not add both without a concrete requirement.

## 10. Database synchronization and test-data policy

Use the project's canonical repository schema authority as the default test source of truth. This may be Flyway migrations, Liquibase changelogs, maintained DDL/schema files, or another repository-owned schema authority.

Policy:

1. canonical repository schema authority is the default test schema source;
2. deterministic repository-owned test seed data is preferred;
3. database dumps/backups are for schema-drift investigation, compatibility/migration validation, or recovery when no maintained canonical schema exists;
4. do not use a developer's shared database dump as the default E2E fixture;
5. mutation System/E2E must use a disposable or explicitly isolated database;
6. do not silently treat shared staging/production-like state as disposable test data.

If local-only authentication/bootstrap seed material is required, document how to obtain or generate it, where it belongs, and the exact test command that consumes it. Do not claim clean-checkout reproducibility while a required prerequisite remains undocumented.

Prefer small explicit fixtures created by the test or deterministic repository-owned seeds. Avoid arbitrary developer-local rows, test-order dependencies, mutable shared staging data, huge opaque dumps as the normal path, uncontrolled wall-clock time, and hidden machine-specific files.

## 11. Authentication and security evidence

When authentication/authorization is a meaningful boundary, cover detailed combinations at the lowest appropriate layer and retain only representative real-boundary evidence at higher layers.

Representative higher-level cases normally include valid authentication, missing/invalid authentication, and one important authorization restriction when relevant.

## 12. Choose one maintainable System/E2E orchestration model

Use the simplest reproducible mechanism matching the current architecture.

Prefer Testcontainers when disposable infrastructure, lifecycle/network control, and per-run isolation fit naturally.

Prefer an existing maintained Docker Compose topology when many real services already start together there and reproducing it in Testcontainers would create a second topology source.

Prefer an existing healthy project-native harness over introducing a parallel mechanism.

Do not maintain equivalent service topology independently in Testcontainers, Compose, and shell scripts without a concrete reason.

## 13. Record clean-checkout prerequisites

Document the prerequisites required to reproduce System/E2E from a clean checkout, including as applicable:

- application/package builds;
- Docker image build/tag commands;
- schema/migration application;
- deterministic seed/bootstrap inputs;
- local-only auth fixtures and how to obtain/generate them;
- service host mappings;
- required environment variables without embedding secrets;
- exact test profile/command;
- required Docker/runtime tooling.

Do not hide required manual prerequisites behind unexplained failures.

## 14. Expose clear project-native commands

Use the repository's natural build system and established conventions.

Make applicable evidence discoverable conceptually as:

```text
Static          -> <real command>
Unit            -> <real command>
Integration     -> <real command>
Contract        -> <real command/evidence>
Component       -> <real command/evidence>
System          -> <real command/evidence>
E2E             -> <real command/evidence>
Full acceptance -> <real command or documented sequence>
```

Do not create a different Maven/Gradle profile for every responsibility when shared commands/source sets are clearer.

A responsibility may point to the same command/test as another responsibility when the same executable evidence genuinely proves both.

## 15. Establish the normal AI coding test cycle

Future implementation work should use this risk-based cycle:

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

Do not blindly run every expensive layer after every mechanical edit. Do not skip higher-level evidence when the changed risk actually crosses those boundaries.

## 16. CI policy

Inspect existing CI before changing it. Do not create an unnecessarily complex matrix.

Prefer staged feedback when useful:

- Fast: Static + Unit;
- Boundary: Integration + Contract + Component;
- Acceptance: System + E2E.

Adapt execution frequency to actual runtime and repository needs. Do not silently weaken existing mandatory CI checks.

## 17. Flaky test policy

Treat a flaky test as a test-system defect.

Do not normalize blind retries, arbitrary sleeps, ignored failures, or permanent quarantine of important scenarios without investigation.

When timing/eventual consistency is intrinsic, prefer bounded condition-based waiting over fixed sleep where practical.

## 18. Update project documentation

After successful setup, add or refine a concise `Testing` section in project `AGENTS.md` using only facts that actually exist.

Record:

- Static evidence;
- Unit evidence;
- Integration real boundaries and evidence;
- Contract authority/evidence or a real `N/A` reason;
- Component deployables/evidence;
- System topology/evidence;
- E2E Critical Journeys/evidence;
- Endpoint completeness scope when required;
- schema/test-data authority;
- System/E2E prerequisites;
- actual commands.

If the same executable test provides evidence for multiple responsibilities, record the factual overlap instead of inventing duplicate suites.

Do not copy this entire generic prompt into `AGENTS.md`.

## 19. Validate the setup itself

Run representative evidence for each applicable responsibility where the environment permits.

Report each independently as `READY`, `PARTIAL`, `MISSING`, `BLOCKED`, `NOT RUN`, or `N/A` using the strict READY rule above.

At minimum also run relevant repository static/build checks and `git diff --check` where Git is available.

Do not claim the full testing environment complete while an applicable E2E Critical Journey remains unimplemented or unexecuted successfully.

## Completion criteria

The setup is complete when:

1. architecture and testing boundaries are understood and documented;
2. every applicable responsibility has a clear purpose and executable evidence;
3. a separate suite is created only when it adds evidence or diagnosability;
4. lower layers contain detailed logic/infrastructure cases while higher layers remain representative;
5. Endpoint Completeness and E2E Critical Journey coverage are treated separately;
6. service contracts have an appropriate executable compatibility mechanism when applicable;
7. schema/test-data authority is explicit and reproducible;
8. System/E2E mutation uses disposable or explicitly isolated data;
9. required local prerequisites are documented with exact commands;
10. project-native test commands are documented;
11. at least one real Critical Journey passes through the actual system boundary when E2E is applicable;
12. actual fresh execution results support every `READY` claim;
13. excessive duplicate tests have not been introduced;
14. existing project conventions and user-owned work remain preserved.

## Final report

Keep the final report concise and include:

1. detected architecture/deployables;
2. previous testing state;
3. resulting responsibility/evidence matrix;
4. tools reused and tools added;
5. representative tests created or reused by responsibility;
6. Endpoint Completeness scope if requested;
7. Contract mechanism;
8. System topology;
9. E2E Critical Journey(s);
10. schema/test-data authority and prerequisites;
11. commands established;
12. `AGENTS.md` and CI changes;
13. files changed;
14. actual validation status for Static, Unit, Integration, Contract, Component, System, and E2E;
15. remaining `PARTIAL`, `MISSING`, `BLOCKED`, `NOT RUN`, or `N/A` items;
16. remaining material testing risks.

The target is not many tests. The target is a small, trustworthy test portfolio covering the full path from isolated logic to a real end-to-end Critical Journey.

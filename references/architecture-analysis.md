# Architecture Analysis and Design Guide

Use this guide to recover an existing architecture or create a new architecture from requirements.

## 1. Establish the system context

Identify:

- users/actors;
- upstream and downstream systems;
- hardware/devices when relevant;
- external services and data sources;
- ownership and trust boundaries;
- what is explicitly out of scope.

For greenfield projects, derive this from requirements and stakeholder workflows. For existing projects, verify it against integration code and configuration.

## 2. Identify architectural drivers

Extract the factors that materially shape the architecture:

- core functional capabilities;
- reliability/availability requirements;
- performance/latency/throughput requirements;
- resource constraints;
- portability/platform constraints;
- compatibility/versioning requirements;
- security/safety constraints;
- offline/network constraints;
- maintainability/extensibility goals;
- development/team/toolchain constraints.

Do not list generic quality attributes unless they cause a concrete design consequence.

Before module decomposition, structure functional requirements by actor goal, capability, use case, or workflow. Do not mirror the source directory or existing module tree into the requirements section. The codebase is used later to map each function to an implementation owner and to detect gaps or drift.

## 3. Define or recover module boundaries

A useful module/component should have:

- one coherent responsibility;
- clear ownership of its data/resources;
- explicit provided interfaces;
- explicit required dependencies;
- limited knowledge of unrelated modules;
- a change boundary that localizes likely future modifications.

Prefer capability/domain boundaries over arbitrary directory boundaries when designing a new system.

In the HLD narrative, describe the **whole system's software architecture** before focusing on a particular subsystem. For brownfield/code-first work, recover this from the **entire code project/repository in scope**, not from one app folder or one feature: identify major layers/subsystems/modules, responsibility boundaries, shared/platform services, important external dependencies, and dependency direction. A subsystem section should then explain its design principles and participating module names without dropping immediately into source paths or function-level structure.

For existing code, directory structure is only one signal. Also inspect build targets, public headers, package manifests, dependency injection/configuration, route registration, IPC boundaries, schemas, and runtime initialization.

## 4. Dependency analysis

Review dependency direction and detect:

- cyclic dependencies;
- upward dependencies that violate layers;
- broad utility modules that become implicit shared state;
- concrete implementation dependencies where a stable interface would reduce coupling;
- duplicated responsibilities across modules;
- hidden dependencies through globals/singletons/environment variables;
- over-centralized manager/god modules.

A dependency is not automatically bad; explain why a dependency creates architectural risk before recommending abstraction.

## 5. Data ownership

For important data determine:

- who creates it;
- who owns authoritative state;
- who may mutate it;
- who may cache/copy it;
- serialization/persistence boundaries;
- consistency rules;
- lifetime and cleanup;
- versioning/migration where applicable.

For buffers, queues, messages, shared memory, and event payloads, make ownership and lifetime explicit when they can cause races, leaks, corruption, or stale data.

## 6. Interface analysis

For each architecturally important interface define or recover:

- provider and consumer;
- direction;
- purpose;
- request/input and response/output shape at a high level;
- synchronous/asynchronous behavior;
- important error semantics;
- timeout/retry/idempotency rules when relevant;
- compatibility/versioning expectations;
- ownership of protocol/schema changes.

Do not duplicate detailed API specifications when they already exist elsewhere.

## 7. Control flow and lifecycle

Capture only architecturally important flows such as:

- startup/initialization;
- login/session establishment;
- acquisition-processing-storage pipelines;
- request-service-database-external-service paths;
- update/upgrade flow;
- shutdown/recovery;
- asynchronous job/event processing.

For greenfield projects, use these flows to validate that module responsibilities form a complete design.

## 8. Concurrency and asynchronous behavior

Analyze when present. Use the conditional-chapter test in `document-rules.md`: retain a standalone concurrency/tasking chapter only when execution contexts, synchronization, ownership, or scheduling policy span modules or materially shape the system architecture; otherwise integrate the result into the owning module/interface/data/fault section.

Check:

- thread/task/event-loop ownership;
- queues/channels/message buses;
- locks/semaphores/conditions/events;
- backpressure and queue overflow;
- cancellation/shutdown;
- ordering guarantees;
- races/deadlocks;
- blocking calls in real-time or event-loop contexts;
- shared-state ownership.

For requirements-first work, choose concurrency only when requirements justify it. Do not invent threads merely to make the architecture look detailed.

## 9. State behavior

Use an explicit state model when behavior depends strongly on lifecycle states, protocol states, connection states, modes, workflow states, or device states.

Do not add a state-machine diagram for ordinary conditional logic.

Retain a standalone state-behavior chapter when one authoritative lifecycle, mode, protocol, workflow, or recovery model coordinates multiple modules or defines an external contract. Otherwise keep the model with its owning module. Leave exhaustive handler actions and complete transition matrices to detailed design unless they are the contract.

## 10. Performance, real-time, and resources

Trace confirmed latency, throughput, deadline, capacity, memory, CPU, storage, and network constraints to concrete architectural decisions. Retain a standalone chapter when budgets or overload policy cross module boundaries or drive partitioning, interfaces, scheduling, buffering, persistence, or deployment. Otherwise record the constraint and response in the affected module/interface/data section.

Distinguish requirements, proposed budgets, observed measurements, and unknowns. Do not invent numbers. Put benchmark procedures and result sets in a performance plan/report.

## 11. Deployment, upgrade, and compatibility

Analyze runtime placement, artifact partitioning, configuration ownership, rollout/rollback, migration, protocol/data compatibility, and availability during upgrade when relevant. Retain a standalone chapter when these concerns change topology, boundaries, contracts, or failure strategy; otherwise integrate them into overall architecture, interfaces, or risks.

Build commands and routine packaging are not HLD content. Include toolchain, ABI, cross-compilation, and generated-artifact constraints only when they materially shape architecture or compatibility.

## 12. Fault model

Identify likely fault domains and expected behavior for:

- invalid input;
- dependency unavailable;
- network timeout/disconnect;
- storage/database failure;
- resource exhaustion;
- corrupted or incompatible data;
- process/thread/task failure;
- device/driver failure;
- partial initialization;
- unexpected restart/power loss when relevant.

Determine containment, retry, rollback, fallback, degradation, and observability strategies at architecture level.

## 13. Architecture decision quality

For significant decisions, capture:

- context/problem;
- constraints;
- chosen option;
- key alternatives considered;
- why the choice is appropriate;
- important consequences/tradeoffs;
- unresolved validation items.

Avoid pretending there is one universally correct architecture.

## 14. Requirement coverage check for greenfield work

Before finalizing, ask:

- Does each major capability have an architectural owner?
- Are all external actors/systems connected through an explicit boundary?
- Do non-functional requirements influence concrete architecture decisions?
- Are required data flows possible end-to-end?
- Are failure cases covered for critical paths?
- Are assumptions that could change module boundaries recorded?
- Are proposed technology choices distinguishable from mandatory constraints?

## 15. Common design smells

Flag when supported by evidence:

- cyclic dependencies;
- shared mutable global state;
- god modules/managers;
- unclear ownership;
- layers that merely forward calls without abstraction value;
- modules split too finely, causing chatty coupling;
- modules too large to evolve independently;
- synchronous chains across unreliable boundaries;
- unbounded queues/caches;
- implicit protocol/version coupling;
- duplicated domain logic;
- platform-specific details leaking into domain logic;
- requirement gaps hidden by assumptions.

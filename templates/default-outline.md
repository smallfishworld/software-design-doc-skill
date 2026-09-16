# Default Software High-Level Design Outline

Use this outline only when the user or organization does not provide a required template. Chapters 8–11 are conditional candidates: keep one as a standalone chapter when the concern has system-wide architectural impact; integrate locally scoped content into the relevant architecture/module/data/interface/fault/risk section; delete it when irrelevant. Remove the parenthetical candidate marker from retained headings, delete unused candidates, and renumber headings, the table of contents, and cross-references consistently.

# 1. Introduction

## 1.1 Purpose
State why this document exists and who should use it.

## 1.2 Scope
Define the system/product boundary and what this design covers or excludes.

## 1.3 Terms and Abbreviations
Define domain terms and abbreviations used throughout the document.

## 1.4 References
List requirement specifications, standards, existing documents, repositories, interface specifications, and other authoritative inputs.

# 2. System Overview

Describe the product/system context, users/actors, major capabilities, operating environment, external systems, and important constraints.

For greenfield work, summarize the requirement baseline without restating the entire requirements document.

# 3. Design Goals and Principles

Capture project-specific goals and constraints such as maintainability, portability, reliability, compatibility, scalability, resource limits, safety, security, or development constraints. Avoid generic principles that have no consequence for this system.

# 4. Overall Software Architecture

## 4.1 Architecture Overview
Describe the selected architecture style and why it fits the requirements.

## 4.2 System Context and Boundaries
Identify external actors/systems and the boundaries owned by this software.

## 4.3 Layer/Subsystem/Component Structure
Describe major architectural units and dependency direction.

## 4.4 Major Control and Data Flows
Describe only flows that are architecturally important.

## 4.5 Key Architectural Decisions
Record significant choices, alternatives, tradeoffs, assumptions, and constraints.

Summarize concurrency, state transitions, real-time/performance constraints, and deployment concerns here when they shape the overall architecture. Use Chapters 8–11 when a concern needs a system-wide standalone treatment.

# 5. Module High-Level Design

For each major module/component/subsystem, describe:

- Responsibility and scope
- Inputs and outputs
- Provided interfaces
- Required dependencies
- Key data owned or managed
- Important lifecycle/initialization behavior
- Major error/fault cases
- Relevant concurrency or state behavior
- Important constraints and design decisions

Do not turn this section into a function-by-function detailed design.

# 6. Data Design

Describe architecturally important data models, ownership, persistence, caching/buffering, lifecycle, consistency, serialization, schemas, or shared-state rules.

For systems without meaningful persistent/shared data, keep this section concise.

# 7. Interface Design

Describe module interfaces and external interfaces that are important at high-level design granularity. Include protocols, contracts, direction, major parameters/data shapes, error behavior, versioning/compatibility rules, and ownership when relevant.

Avoid copying every API definition when a separate interface specification already exists; reference it instead.

# 8. Concurrency and Tasking Design (Conditional Candidate)

Retain as a standalone chapter when processes, threads/tasks, event loops, interrupts, queues, shared resources, scheduling domains, synchronization, or backpressure form a system-wide architectural view. Describe execution-context responsibilities, communication, ownership, ordering, shutdown, and failure containment at HLD granularity.

If the concern is confined to one module, integrate it into that module and the relevant interface/data sections. Put detailed priorities, periods, stack sizes, queue depths, lock sequences, and timing parameters in detailed design unless they are architectural constraints.

# 9. State Behavior Design (Conditional Candidate)

Retain as a standalone chapter when lifecycle, operating modes, protocol/workflow states, or recovery states coordinate several modules or define externally visible behavior. Describe the authoritative state model, ownership, major transitions, guards/events, invalid transitions, persistence/recovery, and module participation.

If only one module has meaningful state behavior, integrate it into that module. Keep exhaustive transition tables and handler-level actions in detailed design unless they define an architectural contract.

# 10. Performance, Real-Time, and Resource Design (Conditional Candidate)

Retain as a standalone chapter when end-to-end latency, throughput, deadlines, capacity, memory/CPU/storage/network budgets, or overload behavior drive cross-module partitioning or contracts. Trace each confirmed target to an architectural mechanism, budget owner, degradation strategy, and validation approach.

If constraints are local, integrate them into the affected module/interface/data section. Do not invent numeric targets; distinguish requirements, proposed budgets, measurements, and TODOs. Detailed benchmarks and test results belong in performance plans/reports.

# 11. Deployment, Upgrade, and Compatibility Design (Conditional Candidate)

Retain as a standalone chapter when node/process/container/firmware placement, artifact partitioning, rollout/rollback, data or protocol migration, availability during upgrade, ABI compatibility, cross-compilation, or toolchain constraints materially shape the architecture.

If deployment is straightforward and local, integrate the relevant constraint into overall architecture, interfaces, or risks. Routine build commands, packaging recipes, installation steps, and operational runbooks are not HLD content.

# 12. Exception and Fault Handling

Describe fault domains, recovery strategy, degraded behavior, retry/fallback rules, resource exhaustion handling, data integrity concerns, and user/system-visible error handling when applicable.

# 13. Logging and Observability

Describe important logging, metrics, tracing, diagnostics, audit, crash reporting, or device/service health mechanisms. Keep proportional to the project.

# 14. Security Design

Include only when security is relevant. Describe trust boundaries, authentication, authorization, sensitive data handling, secrets, secure communication, update/integrity concerns, attack surface, or other project-specific security requirements.

# 15. Testability Design

Describe architectural support for testing: interfaces that allow substitution/mocking, observability, deterministic behavior, test seams, simulation, fault injection, integration boundaries, and key verification strategy.

# 16. Maintainability and Extensibility

Describe extension points, configuration strategy, dependency isolation, compatibility strategy, plugin/feature boundaries, and how future changes can be localized.

# 17. Risks, Constraints, and Open Issues

List unresolved decisions, assumptions, external dependencies, technical risks, implementation risks, requirement ambiguities, migration issues, and design limitations.

For requirements-first designs, explicitly include unresolved requirement questions and assumptions that could change architecture.

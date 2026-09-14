# Platform Profiles

Use these profiles as analysis hints, not mandatory document structures. Select only what matches the project.

## Generic application/service

Inspect or design around:

- domain/capability boundaries;
- application/service layer;
- external integrations;
- data persistence and caches;
- configuration;
- background jobs/events;
- observability;
- security/trust boundaries;
- deployment constraints only when architecturally significant.

## Backend / distributed service

Pay attention to:

- API/service boundaries;
- synchronous vs asynchronous integration;
- database ownership;
- transactions and consistency;
- queues/event streams;
- idempotency;
- retries/timeouts/circuit breaking;
- cache ownership/invalidation;
- horizontal scaling and statelessness when required;
- service discovery/configuration/secrets;
- failure isolation and observability.

Do not split into microservices by default. Derive service boundaries from ownership, scaling, fault isolation, deployment independence, and team/domain constraints.

## Web application

Consider:

- browser/client responsibilities;
- backend/API boundary;
- authentication/session model;
- frontend state ownership;
- API contracts and versioning;
- asset/static delivery only if relevant;
- error states and offline/network behavior;
- security boundaries including untrusted client input.

Avoid UI component-level details in HLD unless they establish an architectural pattern.

## Desktop application

Consider:

- presentation/UI layer;
- application/domain layer;
- local persistence/configuration;
- background workers;
- OS/platform abstraction;
- plugin/update mechanism when relevant;
- local IPC or external-device integration;
- crash recovery and user data integrity.

## Embedded Linux

Inspect or design around:

- process/thread model when architecturally relevant;
- POSIX IPC (Inter-Process Communication，进程间通信);
- timers and event loops;
- device abstraction and drivers;
- protocol/network stacks;
- startup/init order;
- configuration/persistent storage;
- memory/buffer ownership;
- hardware interaction boundaries;
- watchdog/recovery;
- cross-compilation/platform abstraction.

For existing C/C++ projects, inspect build targets, public headers, `pthread`, message queues, semaphores/mutexes, sockets, `epoll`/`select`, shared memory, timers, device nodes, and protocol parsers when present.

## RTOS

Consider:

- task/thread responsibilities;
- priority and timing constraints only when known or explicitly designed;
- queues/mailboxes/channels;
- semaphores/mutexes/events;
- timers;
- ISR (Interrupt Service Routine，中断服务程序) boundaries;
- DMA (Direct Memory Access，直接存储器访问) ownership;
- static/dynamic memory strategy;
- HAL (Hardware Abstraction Layer，硬件抽象层);
- driver/service/application layering;
- startup and fault recovery.

Do not invent task priorities, stack sizes, queue depths, tick periods, or execution budgets. Treat them as design decisions/TODOs unless required or measured.

## Bare-metal MCU

Focus on:

- main loop/super-loop or scheduler model;
- interrupt boundaries;
- hardware abstraction;
- peripheral ownership;
- state/event processing;
- DMA/buffer ownership;
- timing-critical paths;
- memory/resource constraints;
- boot/startup and fault recovery.

Do not impose an RTOS architecture when requirements do not justify one.

## Mobile application

Consider:

- UI/application/domain/data layers;
- lifecycle and background execution constraints;
- local data/cache;
- remote APIs;
- authentication/session;
- platform services and permissions;
- offline/synchronization behavior;
- push/event mechanisms;
- compatibility across OS versions when relevant.

## Library / SDK

Focus on:

- public API surface;
- stable abstractions;
- internal module boundaries;
- compatibility/versioning;
- error model;
- thread-safety/reentrancy expectations;
- extension/plugin points;
- platform portability;
- dependency footprint;
- test seams.

Avoid application-level chapters that do not apply to a library.

## CLI / developer tool

Consider:

- command parsing and command model;
- core/domain operations;
- adapters for filesystem/network/VCS/build systems;
- configuration and credentials;
- output/reporting;
- plugin/extension mechanisms;
- non-interactive automation behavior;
- failure/exit-code semantics.

## Mixed hardware/software product

When software interacts closely with hardware, explicitly capture:

- hardware/software responsibility split;
- control/data interfaces;
- initialization dependencies;
- timing assumptions;
- fault propagation;
- firmware/application boundaries;
- protocol ownership;
- version compatibility.

Keep hardware circuit detail outside the software HLD unless it creates a software constraint.

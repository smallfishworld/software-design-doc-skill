---
name: software-design-doc
description: Create or review software high-level design (HLD/概要设计) documents from requirements, source code, existing documentation, or any combination of them. Supports greenfield projects with no code, brownfield code reverse-engineering, and requirement-code consistency analysis across languages and platforms.
---

# Software Design Document

Create a software high-level design that is traceable to available evidence and useful for implementation and review.

## Select the working mode first

Choose the mode from the available inputs. Do not require source code when it does not exist.

- **Requirements-first / Greenfield**: requirements exist, implementation does not. Derive a proposed architecture and clearly treat implementation choices as design decisions, not existing facts.
- **Code-first / Brownfield**: source code exists but design documentation is missing or outdated. Reverse-engineer the current architecture from code and configuration.
- **Hybrid**: both requirements and code exist. Reconcile intended behavior with implemented behavior and identify gaps or drift.
- **Review-only**: review an existing design without generating a full replacement unless requested.

If inputs are incomplete, continue with reasonable assumptions but record them explicitly. Do not invent implementation facts.

## Evidence classes

Track information internally using these classes:

- `[REQ]` confirmed by requirements or user-provided specification
- `[CODE]` confirmed by source code, configuration, build files, schemas, or generated code
- `[DOC]` confirmed by existing project documentation
- `[DESIGN]` proposed by this design process
- `[ASSUMPTION]` necessary assumption that still needs confirmation
- `[TODO]` unresolved item or decision

Do not expose all tags in the final document unless useful, but preserve the distinction while reasoning and reviewing.

## Workflow

1. Identify available inputs and select the working mode.
2. Read the user's/company template first when one is provided. Its structure has priority over the default outline.
3. Extract scope, actors, capabilities, constraints, external systems, quality attributes, and important terminology.
4. Inspect the codebase when code exists. Prefer repository-aware tools such as CodeGraph when available; otherwise inspect files, build definitions, entry points, modules, interfaces, schemas, configuration, tests, and deployment assets directly.
5. Build an evidence/decision ledger before drafting the final document.
6. Define or recover the system context and architectural boundaries.
7. Define or recover modules/components and their responsibilities, ownership, dependencies, and interfaces.
8. Analyze important data, control flow, lifecycle, error/fault paths, and persistence where relevant.
9. Analyze concurrency, state machines, performance/real-time constraints, and deployment only when they materially affect the architecture. Do not force them into standalone chapters by default.
10. Generate diagrams only when they clarify structure or behavior. Follow `references/diagram-guide.md`.
11. Review the architecture for cohesion, coupling, dependency direction, ownership, cyclic dependencies, single points of failure, excessive shared state, unclear interfaces, and requirement coverage.
12. Draft the document using the company/user template when available, otherwise `templates/default-outline.md`.
13. Run a consistency pass: every important architectural statement must be supported by evidence or clearly presented as a proposal/assumption.
14. If a Word/DOCX output is requested, use the best available local document tool. Follow `references/tool-integration.md`.

## Requirements-first rules

When there is no source code:

- Treat the requirements as the factual baseline.
- Derive architecture from business/system responsibilities and constraints, not from imagined classes or filenames.
- Propose modules at the level needed for implementation planning; avoid premature function-level detail.
- For each proposed module, state responsibility, provided interfaces, required dependencies, key data, and major failure cases.
- Capture architectural decisions and alternatives when the requirement does not determine a unique solution.
- Mark technology/framework choices as `[DESIGN]` unless explicitly required.
- Mark missing information as `[ASSUMPTION]` or `[TODO]` rather than silently filling gaps.
- Ensure major requirements are traceable to one or more architectural elements.

## Code-first rules

When code exists:

- Prefer observable implementation over naming assumptions.
- Identify entry points, build targets, module boundaries, dependencies, interfaces, schemas, IPC/network boundaries, persistence, and external integrations.
- For C/C++/embedded projects also inspect tasks/threads, timers, queues, semaphores/mutexes, ISR/DMA paths, drivers, buffers, ownership, and initialization order when relevant.
- For service/web projects inspect API routes, service boundaries, asynchronous jobs, databases, caches, queues, external services, and deployment configuration when relevant.
- Do not describe dead code or unused modules as active architecture without evidence.

## Hybrid rules

When requirements and code both exist:

- Separate intended design from observed implementation.
- Identify requirements with no implementation evidence.
- Identify implemented behaviors/modules with no clear requirement source when significant.
- Highlight architectural drift, obsolete assumptions, inconsistent interfaces, and missing constraints.
- Prefer updating the design to describe both the current state and the recommended target state when the user requests improvement.

## Default document behavior

Use the compact default outline in `templates/default-outline.md` only when the user/company does not provide a template.

Do **not** create standalone chapters for concurrency/tasking, state machines, performance/real-time behavior, or build/deployment unless explicitly requested or clearly necessary. Integrate those topics into Overall Architecture, Module Design, Data Design, Interface Design, or Risks as appropriate.

Security is conditional: include it when the system has authentication, authorization, sensitive data, network exposure, update mechanisms, safety/security requirements, or other meaningful security concerns. Otherwise keep it concise or omit it.

## Writing rules

- Write at high-level design granularity, not detailed implementation-document granularity.
- Prefer concrete responsibilities and relationships over generic software-engineering prose.
- Keep modules cohesive and dependencies explicit.
- Prefer stable abstractions and one-way dependency direction.
- Explain important tradeoffs and rejected alternatives when they affect maintainability, reliability, cost, performance, portability, or schedule.
- Define an abbreviation with its English full name and local-language meaning on first use when appropriate.
- Never claim that a proposed design already exists in code.
- Never fabricate exact priorities, buffer sizes, timeouts, protocols, field widths, database schemas, file names, or resource limits unless supported by evidence or explicitly proposed as a design choice.
- Avoid textbook chapters that add no project-specific value.

## Reference files

Read only the references needed for the current task:

- `references/architecture-analysis.md` — architecture extraction and design checks
- `references/document-rules.md` — content quality and evidence rules
- `references/platform-profiles.md` — platform-specific analysis hints
- `references/diagram-guide.md` — choosing useful diagrams
- `references/tool-integration.md` — optional CodeGraph, PlantUML, DOCX, Pandoc, and fallback behavior

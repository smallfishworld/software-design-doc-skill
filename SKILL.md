---
name: software-design-doc
description: Create or review software high-level design (HLD/概要设计) documents from requirements, source code, existing documentation, or any combination of them. Supports greenfield projects with no code, brownfield code reverse-engineering, and requirement-code consistency analysis across languages and platforms.
---

# Software Design Document

Create a software high-level design that is traceable to available evidence and useful for implementation and review.

## Scope boundary

This skill is dedicated to software high-level design documents.

- Its primary output is an HLD document or an HLD review.
- It may analyze requirements, source code, architecture, modules, interfaces, data, risks, and diagrams as needed to produce the document.
- It does **not** generate project scaffolding, directory trees, source-code skeletons, detailed-design documents, or production implementation code.
- For greenfield projects, the project may have no source code and no project directory at all. Requirements alone are a valid starting point.

Keep the workflow focused on design-document quality rather than continuing into implementation.

## Mandatory startup capability check

At the beginning of every run, perform a lightweight capability check before architecture analysis or document drafting. The purpose is to discover which local tools can actually be used during this run.

Prefer running `python3 scripts/check_environment.py` when the script is accessible. If it cannot be run, perform equivalent lightweight command/module checks directly.

Check relevant capabilities without generating test artifacts:

- PlantUML: check whether the `plantuml` command can execute. If the installation uses a local JAR instead, check Java and the configured PlantUML JAR invocation.
- Mermaid CLI: run `mmdc --version`. If it succeeds, treat Mermaid CLI as available and use `mmdc` directly to render Mermaid diagrams when needed.
- Java: `java -version`, when relevant to PlantUML.
- Pandoc: `pandoc --version`.
- DOCX: check whether `python-docx`, a document/DOCX tool, or another usable Word-generation mechanism is available.
- CodeGraph/MCP: when code exists, inspect whether a repository-aware code-analysis tool is exposed to the current agent. Do not require it for greenfield work.

A command counts as available only when it is found and its lightweight check executes successfully. Do not perform expensive rendering or create test diagrams merely to verify availability.

Keep successful checks quiet unless the user asks for diagnostics. Report missing tools only when their absence affects the requested deliverable or causes a fallback.

### Diagram tool selection

Select the diagram tool by diagram semantics rather than forcing every diagram into UML:

- **UML and software-architecture modeling**: prefer PlantUML when available. Examples include component, class, sequence, state, activity, deployment, and other UML-oriented diagrams.
- **General flowcharts, tree/hierarchy diagrams, functional decomposition, mind maps, and general relationship diagrams**: prefer Mermaid.
- If the preferred PlantUML path is unavailable, use Mermaid as the fallback when `mmdc` is available.

When `mmdc --version` succeeds, generate the `.mmd` source and invoke Mermaid CLI directly to render the diagram, preferably to SVG for document-quality vector output or PNG when required by the DOCX pipeline.

Do **not** use Text/ASCII diagrams as finished HLD diagrams. If neither PlantUML nor Mermaid CLI can render a required diagram in the current environment, preserve the appropriate `.puml` or `.mmd` source and report that rendering must be completed in an environment with the corresponding renderer (for example, Windows with Mermaid CLI) before final document delivery.

When PlantUML is available and a UML/software-architecture diagram materially improves the HLD, actually use PlantUML to produce it. When Mermaid is selected and `mmdc` is available, actually invoke `mmdc`; do not merely emit Mermaid source and treat it as a finished diagram.

## Select the working mode

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

1. Run the mandatory startup capability check and record usable tools for this run.
2. Identify available inputs and select the working mode.
3. Resolve the document template before drafting. Follow the template priority rules below.
4. Extract scope, actors, capabilities, constraints, external systems, quality attributes, and important terminology.
5. Inspect the codebase when code exists. Prefer repository-aware tools such as CodeGraph when available; otherwise inspect files, build definitions, entry points, modules, interfaces, schemas, configuration, tests, and deployment assets directly.
6. Build an evidence/decision ledger before drafting the final document.
7. Define or recover the system context and architectural boundaries.
8. Define or recover modules/components and their responsibilities, ownership, dependencies, and interfaces.
9. Analyze important data, control flow, lifecycle, error/fault paths, and persistence where relevant.
10. Analyze concurrency, state machines, performance/real-time constraints, and deployment only when they materially affect the architecture. Do not force them into standalone chapters by default.
11. Generate diagrams only when they clarify structure or behavior. Select PlantUML or Mermaid by diagram semantics and use the detected CLI/rendering capability. Do not use Text/ASCII as a finished diagram fallback. Follow `references/diagram-guide.md`.
12. Review the architecture for cohesion, coupling, dependency direction, ownership, cyclic dependencies, single points of failure, excessive shared state, unclear interfaces, and requirement coverage.
13. Draft the content using the resolved template and the project-specific analysis.
14. Run a consistency pass: every important architectural statement must be supported by evidence or clearly presented as a proposal/assumption.
15. When DOCX output is possible, generate the final Word document from the resolved DOCX template and validate the result. Follow `references/tool-integration.md` and `references/docx-template.md`.
16. Stop at the completed/reviewed HLD document; do not continue into project scaffolding, detailed design, or code generation.

## Template priority and fallback

Resolve templates in this order:

1. **User/company DOCX template explicitly supplied for this task** — highest priority. Preserve its chapter structure and styles unless the user asks to change them.
2. **Project-specific template** — use an HLD/DOCX template found in the project when it is clearly intended for this document.
3. **Built-in standardized DOCX template** — `templates/default-software-design-template.docx`.
4. **Markdown content outline fallback** — `templates/default-outline.md`, used when DOCX generation/editing is unavailable or the user explicitly wants Markdown.

If the user requests a Word document and does not specify a template, use `templates/default-software-design-template.docx` by default. Work on a copy; never overwrite the built-in template itself.

The DOCX template controls appearance and standard document-control sections. The Markdown outline controls semantic/content guidance. A company DOCX template may override the built-in chapter structure.

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
- Do not create a project tree or source skeleton as an HLD deliverable.

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

When no user/company template is supplied, use the built-in standardized DOCX template for Word output and `templates/default-outline.md` as the content guide.

Do **not** create standalone chapters for concurrency/tasking, state machines, performance/real-time behavior, or build/deployment unless explicitly requested or clearly necessary. Integrate those topics into Overall Architecture, Module Design, Data Design, Interface Design, or Risks as appropriate.

Security is conditional: include it when the system has authentication, authorization, sensitive data, network exposure, update mechanisms, safety/security requirements, or other meaningful security concerns. Otherwise keep it concise or remove the optional section from the final document.

For the built-in DOCX template:

- Replace document-control placeholders such as project, document ID, version, author, reviewer, approver, date, scope, and department when values are known.
- Do not guess unknown administrative metadata; leave a clear placeholder or mark it pending.
- Replace instructional placeholder text with project-specific content.
- Duplicate module subsections/tables as needed and remove unused sample rows.
- Remove optional sections that are not relevant rather than filling them with generic prose.
- Insert architecture/flow diagrams in the corresponding sections when available.
- Update the table of contents and page fields when the available Word/DOCX tool supports field updates; otherwise preserve the fields for Word to update on open.

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
- Do not append implementation artifacts such as project folders, `.c/.cpp/.h` skeletons, build-system scaffolding, or generated application code to the HLD deliverable.

## Reference files

Read only the references needed for the current task:

- `references/architecture-analysis.md` — architecture extraction and design checks
- `references/document-rules.md` — content quality and evidence rules
- `references/platform-profiles.md` — platform-specific analysis hints
- `references/diagram-guide.md` — choosing useful diagrams
- `references/tool-integration.md` — optional CodeGraph, PlantUML, DOCX, Pandoc, and fallback behavior
- `references/docx-template.md` — built-in Word template usage and placeholder rules

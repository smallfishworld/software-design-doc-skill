---
name: software-design-doc
description: Create, update, or review software high-level design (HLD/概要设计) documents from requirements, source code, or existing designs. Use for requirements-first design, architecture reverse-engineering, and requirement-code consistency reviews. Produces design documents or review findings, not application code or detailed design.
---

# Software Design Document

Produce a software High-Level Design (HLD，软件概要设计) that is traceable to evidence and useful for implementation and review. Requirements alone are valid input; no project directory or code skeleton is required. Stop at the requested document or review, without creating application code, project scaffolding, or a detailed design.

## 1. Resolve the task before doing work

Identify the requested scope, language, output format, available inputs, and any company template. Preserve explicit choices and existing authorization. If the format is unspecified, follow an existing document's format; otherwise draft in Markdown without generating an unsolicited Word file.

Before choosing a working representation, establish the **authoritative artifact**. If the user has manually edited an existing Word/DOCX file, asks to preserve that file, or the DOCX is newer than its Markdown mirror, treat the DOCX as the source of truth and Markdown as a secondary mirror. Baseline the current document before editing, record the requested edit scope, and never regenerate untouched chapters from an older Markdown copy. When modification times are available, check them before editing; otherwise infer authority from the user's explicit workflow.

Select the input mode independently of the deliverable:

| Input mode | Factual baseline | Main action |
| --- | --- | --- |
| Requirements-first / Greenfield | Requirements, constraints, user decisions | Propose architecture; do not imply it is implemented |
| Code-first / Brownfield | Active source, configuration, build targets | Recover current architecture; separate recommendations |
| Hybrid | Both requirements and implementation | Preserve intended and observed behavior; explain gaps |

For **review-only**, apply the relevant input mode but return findings, not a replacement HLD. For **updates**, inspect the existing document first and change affected sections, diagrams, references, and cross-references; preserve unrelated approved content and styles.

Ask only when an unresolved choice materially changes scope or architecture and cannot be handled as an explicit assumption. Continue other useful work. Do not invent unavailable input contents or exact implementation parameters.

## 2. Check capabilities relevant to this deliverable

Perform a lightweight capability check before analysis/drafting, scoped to the selected output. Resolve bundled paths relative to this `SKILL.md`, not the user's current project directory.

- Code inputs: inspect exposed repository tools such as CodeGraph; skip for projects without code. Verify their repository/revision matches the task.
- Diagrams: `python3 <skill-root>/scripts/check_environment.py --scope diagrams`.
- Word output: use `--scope docx`; add `--scope diagrams` if diagrams are planned.
- Text-only review: no renderer/Word checks are needed. No-argument invocation is an optional full diagnostic.
- If the script cannot run, inspect equivalent commands/modules directly. Use `--plantuml-jar <path>` for a known JAR installation.

The check creates no test artifacts. Command discovery/version success is **not** proof of rendering or conversion success. Keep successful checks quiet; report a limitation only when it affects the requested output. Missing optional tools must not block analysis.

## 3. Establish evidence and design boundaries

Read [document-rules.md](references/document-rules.md) for evidence, conflicts, and traceability. Classify important claims as `[REQ]`, `[CODE]`, `[DOC]`, `[DESIGN]`, `[ASSUMPTION]`, or `[TODO]`; retain a source locator for confirmed claims. The final document need not display every internal tag, but proposals and uncertainty must remain visible.

- Requirements-first: derive responsibilities from capabilities and constraints. Technology, module, and interface choices are proposals unless explicitly required. Map major requirements to architectural owners and record consequential alternatives.
- Functional requirements MUST be decomposed by user-visible capability, business function, use case, or workflow before they are mapped to software modules. Do not use source folders, files, classes, or existing module names as the requirement taxonomy merely because code is available. Code structure may identify the implementation owner only after the functional structure is clear.
- Code-first: inspect active build targets, entry points, public interfaces, configuration, data ownership, and important flows. Naming and directory proximity do not prove dependencies. Check relevant symbols/files behind tool summaries; report analysis coverage and gaps.
- Hybrid: keep requirement truth and implementation truth separate. “No implementation evidence found” is not proof of nonimplementation without sufficient coverage. Separate the current state from the proposed target state.

For architecture analysis use [architecture-analysis.md](references/architecture-analysis.md). Read only relevant sections of [platform-profiles.md](references/platform-profiles.md) for platform-specific concerns. Do not load every reference by default.

## 4. Design or recover the architecture

Work at system/module/interface granularity:

1. Establish system context, scope, external actors, constraints, and architectural drivers.
2. Define or recover modules, responsibilities, dependency direction, interface contracts, and data/resource ownership.
3. Trace critical control/data flows, lifecycle, and fault/recovery paths end to end.
4. Record significant choices, alternatives, consequences, and unresolved validation items.
5. Check requirement coverage, cohesion, coupling, cycles, shared mutable state, and failure containment.

Write from the outside in: explain the overall application architecture and dependency direction before drilling into a focal subsystem. In a section such as “Basic Design Concept / 基本设计概念”, prefer concise technical prose rather than a table: first describe the application-level architecture, then the subsystem design principles and the module names involved. Do not mention code paths, function names, or framework/runtime names unless they are explicitly required or architecturally significant.

Analyze concurrency, state, timing, resource budgets, deployment, upgrade, and compatibility when they affect the architecture. When the built-in outline/template applies, treat **task/concurrency design, state behavior, performance/real-time/resource design, and deployment/upgrade/compatibility design as conditional candidate chapters**:

- keep a candidate as a standalone chapter when the concern changes system-wide boundaries, execution/deployment topology, cross-module contracts, shared-resource policy, lifecycle, or major architectural decisions;
- integrate a locally scoped concern into the relevant architecture, module, data, interface, fault, or risk section and delete the candidate chapter;
- delete an irrelevant candidate instead of leaving an empty or generic chapter, then fix numbering, the table of contents, and cross-references.

A required company template still controls chapter structure. Build commands and routine packaging steps are normally outside HLD scope; include toolchain, ABI, cross-compilation, artifact partitioning, or release topology only when they materially constrain the architecture. Keep thread parameters, exhaustive state transitions, performance test data, build commands, and deployment procedures in detailed design or specialist documents unless a high-level decision depends on them.

Never fabricate priorities, buffer sizes, timeouts, protocols, field widths, schema details, filenames, or resource limits. Give evidence, identify a proposed value with rationale, or record the missing decision.

## 5. Draft or review the requested deliverable

### Document creation and updates

Use this template priority:

1. User/company template explicitly supplied for the task.
2. Project-specific HLD template clearly intended for this document.
3. [Built-in DOCX template](templates/default-software-design-template.docx) for Word output.
4. [Default outline](templates/default-outline.md) for Markdown or when Word generation is unavailable.

A required company template controls chapter structure and styles; the default outline supplies content guidance only where compatible. Work on a copy of any template. Keep unknown administrative metadata pending, remove instructional/sample text, and remove irrelevant optional sections while fixing numbering and references. Keep security content proportional to actual trust boundaries and requirements.

For Word output read [docx-template.md](references/docx-template.md) and the Word section of [tool-integration.md](references/tool-integration.md). Preserve template layout, styles, headers/footers, and fields. For an existing user-edited DOCX, use the DOCX-first incremental workflow: baseline the current file, lock the requested edit range, edit a copy/new output path, validate it, and only then replace or hand back the intended file. If Word cannot be created, deliver useful structured content and explicitly identify the conversion still needed; do not label it a completed DOCX.

### Review-only

Read the review section of [document-rules.md](references/document-rules.md). Lead with actionable findings ordered by impact. Each finding needs a document/source location, evidence, consequence, and concrete correction; distinguish confirmed defects from questions and recommendations. State coverage and remaining uncertainty. If no significant issue is found, say so without inventing findings. Do not run a full document-generation workflow for a review.

## 6. Create useful diagrams

When diagrams clarify the design, first apply [diagram-standards.md](references/diagram-standards.md) for view selection, semantics, notation, layout, and review acceptance; then apply [diagram-guide.md](references/diagram-guide.md) for tool selection, rendering, assets, and fallback:

- Formal UML (Unified Modeling Language，统一建模语言) views such as component, class, sequence, state, and deployment diagrams: PlantUML first.
- Layered logical architecture, block diagrams, ordinary flowcharts, data pipelines, trees, functional decomposition, and general relationships: Mermaid first unless formal UML semantics are required.
- Treat `.puml`/`.mmd` as the authoritative editable source. Render SVG (Scalable Vector Graphics，可缩放矢量图形) as the preferred presentation asset for Markdown and, when verified compatible, DOCX. Keep a high-resolution PNG (Portable Network Graphics，便携式网络图形) fallback when the document pipeline cannot reliably insert or render SVG.
- Render actual sources when a local renderer is usable; validate the produced image, not just a version command or exit code.
- If Mermaid cannot render on the current Linux environment, preserve `.mmd`, provide Windows `mmdc` commands, and identify the target section/caption. Insert rendered images before declaring the Word document final.
- Never substitute ASCII drawings or raw diagram code for finished Word diagrams. Continue the textual design and deliver a clearly identified draft plus pending rendering steps when necessary.

In Markdown, reference the SVG by a relative path instead of embedding a generated bitmap when the target renderer supports SVG. In Word, SVG preserves vector quality and may allow limited shape-level editing, but it is not a substitute for editing PlantUML/Mermaid semantics. Keep source, SVG, and fallback PNG together with matching basenames. Do not send project sources to an external rendering service without authorization.

## 7. Completion checks

- Important claims have locatable evidence or are explicitly proposals/assumptions.
- Major requirements have architectural owners; critical interfaces and data have ownership and fault behavior.
- Text, tables, diagrams, and identifiers agree; updates do not silently rewrite approved decisions.
- Functional requirements are organized by capability/workflow rather than by code layout, and the overall application architecture is explained before subsystem details.
- Prose is concrete and project-specific: avoid repetitive AI-style scaffolding, generic slogans, and table-heavy restatement where normal paragraphs communicate better.
- Every finished diagram passes the semantic and visual review gate in `references/diagram-standards.md`; a successful render alone is insufficient. Pending figures remain explicitly identified as draft work.
- Use the requested language; expand abbreviations with English full names and local-language meanings on first use where appropriate.
- Required sections are filled, irrelevant samples removed, numbering consistent, and unknown metadata visible.
- For Word: reopen the file, check fields/images/tables, render and inspect pages when a rendering tool is available. Validate table cell indentation and column widths, preserve code/identifier text exactly, and require every low-level XML/string replacement to report its hit count. Report unverified layout or pending fields/figures precisely; do not claim checks that were not run.
- Deliver only requested outputs and necessary editable diagram sources. Distinguish a completed document, a draft awaiting figures, and a review report. Do not continue into implementation.

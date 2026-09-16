# Document and Evidence Rules

## Source precedence

Resolve conflicts by the kind of claim, not a single ranking across unrelated sources:

- **Task scope and format:** explicit current user instructions, then required company/project conventions, then built-in defaults.
- **Intended behavior:** approved requirements and confirmed user decisions; identify the version and report conflicts.
- **Existing behavior:** active source/configuration for the selected revision. A template or requirement does not prove implementation behavior.
- **Historical intent:** existing design documents; compare with requirements and code rather than silently treating them as current.
- **Proposed behavior:** design decisions and assumptions, visibly separated from facts.

If sources disagree, record both claims, their locators/versions, and the impact. Ask for resolution only when needed to choose a consequential direction; continue independent work.

## Evidence discipline

Before drafting, maintain a lightweight ledger for consequential claims, not every sentence:

| Claim / decision | Class | Source locator / rationale | Status / consequence |
| --- | --- | --- | --- |
| Summarized statement | REQ / CODE / DOC / DESIGN / ASSUMPTION / TODO | Requirement ID and section; code path, symbol, revision; or decision rationale | Confirmed / proposed / unresolved, with impact |

Record code paths and symbols (line numbers when useful), document sections/pages, and requirement versions when known. For partial inspection, record what was examined and what remains unseen. Do not claim an exhaustive review from a sample. Distinguish lack of evidence from confirmed absence.

A final statement should be one of:

- a confirmed fact supported by an available source;
- an explicit proposed design decision;
- an explicit assumption;
- an unresolved issue/TODO.

Never transform uncertainty into false precision.

## Greenfield requirement traceability

For requirements-first designs, map major requirements to architectural elements. A lightweight table is often enough:

| Requirement / capability | Architectural element | Design response | Open issue |
| --- | --- | --- | --- |
| R1 | Module/Subsystem A | ... | ... |

Keep the working table internal if it adds no reader value, but expose uncovered requirements, conflicts, and consequential assumptions in the final document or review. For hybrid work, add observed implementation and gap status.

Check that every high-priority functional requirement has an owner in the architecture and that important non-functional requirements affect at least one concrete design decision.

## Granularity

High-Level Design (HLD) should normally describe:

- system context and boundaries;
- architecture style/layers/subsystems/components;
- module responsibilities and dependency direction;
- important interfaces and contracts;
- important data ownership and flows;
- fault-handling strategy;
- architecturally significant lifecycle/concurrency/state behavior;
- key decisions, tradeoffs, constraints, risks, and extension points.

It should normally avoid:

- line-by-line or function-by-function implementation descriptions;
- exhaustive class/member lists;
- arbitrary pseudo-code for straightforward logic;
- copied requirement text that adds no design interpretation;
- generic software-engineering advice unrelated to the project.

## Company template behavior

When a template is supplied:

- preserve mandatory chapter order and naming;
- fill only relevant sections;
- do not add large new chapters merely because the default outline contains them;
- if important design content has no dedicated chapter, integrate it into the closest existing section;
- record optional additions separately when they would improve the template rather than silently changing company conventions.

## Language and terminology

Use the user's requested language. Keep product, protocol, API, framework, and code identifiers unchanged when translation would reduce clarity.

On first occurrence of an abbreviation, expand the English full name and add a local-language meaning when appropriate, for example:

`IPC (Inter-Process Communication，进程间通信)`

Do not repeatedly expand the same abbreviation after it has been introduced.

## Tables

Use tables when they compress structured information such as module responsibility, interfaces, dependencies, risks, assumptions, or requirement mapping. Do not convert all prose into tables.

## Review checklist

Before completing the document, verify:

- Scope and system boundary are explicit.
- Major requirements/capabilities have architectural ownership.
- Module responsibilities do not substantially overlap without explanation.
- Dependency direction is understandable.
- Shared data has clear ownership.
- External interfaces have owners and failure behavior.
- Proposed decisions are not described as existing implementation.
- Assumptions and unresolved items are visible.
- Diagrams and prose do not contradict each other.
- The document is sufficiently concrete to guide implementation without becoming detailed design.

## Review-only output

Return an impact-ordered review rather than a replacement document. For each finding include:

| Field | Required content |
| --- | --- |
| Impact | High: breaks a core requirement/contract or risks loss; Medium: concrete maintainability/reliability ambiguity; Low: limited consistency/readability issue |
| Location | Document section, diagram/table identifier, or source path/symbol |
| Evidence | Conflicting claims, missing contract, or observed behavior; identify the source |
| Consequence | What fails or becomes ambiguous, and under which condition |
| Correction | A specific design change or decision to resolve |

Separate confirmed defects, open questions, and optional improvements. Do not assign severity based solely on a preferred style. State inspected inputs/revisions and material coverage gaps, and explain any check that could not run. If no significant findings are supported, say so and retain the limitations.

## Incremental updates

Read the existing artifact and identify affected requirements/modules before editing. Update dependent figures, interface tables, terminology, cross-references, and the revision record when appropriate. Do not mark a document approved or invent reviewers/dates. Preserve unrelated approved sections. Briefly report substantive changes and remaining decisions.

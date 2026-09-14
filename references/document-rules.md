# Document and Evidence Rules

## Source precedence

When sources conflict, do not silently choose one. Report the conflict and apply this practical precedence unless the user specifies otherwise:

1. Explicit user instruction for the current task
2. Organization/company template or mandatory standard
3. Approved requirement/specification documents
4. Current source code/configuration/build artifacts for describing existing implementation
5. Existing design documents
6. Inference or proposed design

Requirement truth and implementation truth are different. In hybrid mode, preserve both when they disagree.

## Evidence discipline

Before drafting, maintain an internal ledger of important claims. Classify them as requirement, code, existing document, design proposal, assumption, or unresolved item.

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

The table can remain internal unless the user asks for traceability in the final document.

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

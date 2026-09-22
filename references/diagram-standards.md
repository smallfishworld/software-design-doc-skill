# Software Design Diagram Standard

Use this standard for diagrams created or reviewed as part of a Software High-Level Design (HLD，软件概要设计). It defines diagram semantics, abstraction, notation, layout, and acceptance criteria. Tool selection, rendering, editable sources, SVG/PNG handling, and renderer fallback belong to [diagram-guide.md](diagram-guide.md).

This is a project documentation profile informed by UML (Unified Modeling Language，统一建模语言) and the C4 model. Do not call a diagram UML or C4 unless it follows the corresponding semantics. PlantUML and Mermaid are authoring tools, not proof that a diagram is well modeled.

## 1. Requirement language

- **MUST**: required for a diagram to pass review.
- **SHOULD**: default unless a documented project reason justifies another choice.
- **MAY**: optional and context-dependent.

When a company standard or supplied template conflicts with this profile, follow the required company convention and record the deviation when it affects interpretation.

## 2. Select the view before drawing

Every diagram MUST answer one architectural question and declare its view type and scope. Use the narrowest view that communicates the decision.

| View | Question answered | Typical contents | Exclude by default |
| --- | --- | --- | --- |
| System context | Who or what interacts with the system? | people, target system, external systems/devices, major relationships | internal modules, classes, threads |
| Logical architecture | How is software responsibility divided? | layers, subsystems, modules/components, dependencies | physical nodes, function-level calls |
| UML component | What deployable/replaceable components and interfaces exist? | components, provided/required interfaces, dependencies | arbitrary folders presented as components |
| Sequence | How does a critical scenario cross boundaries over time? | participants, messages, responses, alternatives, failures | ordinary single-module function tracing |
| State | How do explicit states and events govern behavior? | states, events, guards, effects, initial/final states | ordinary conditional branches |
| Activity/flow | How does a workflow or decision process progress? | actions, decisions, branches, joins | architecture dependencies |
| Data flow/pipeline | Where does important data originate, transform, queue, persist, and terminate? | sources/sinks, processing stages, queues, stores, labeled data flows | unrelated control dependencies |
| Deployment | Where do artifacts execute and how do nodes communicate? | devices/nodes, execution environments, processes/artifacts, protocols | logical layering without placement |
| Runtime/concurrency | Which execution contexts coordinate and who owns resources? | processes, tasks/threads, ISR/DMA, queues, synchronization, ownership | invented priorities or timing values |
| Class/domain | Which type relationships are architecturally significant? | key types, public contracts, inheritance/composition | exhaustive implementation classes/members |

Do not mix multiple abstraction levels merely to fit everything on one page. If readers need both the whole system and module detail, create a parent view and one or more scoped child views with explicit drill-down names.

## 3. Diagram identity and document captions

For diagrams embedded in a Word/DOCX or Markdown design document, the **document figure caption is the canonical title**. Do not duplicate the title inside the rendered UML/architecture image unless the user/template explicitly requires an internal title. This keeps diagrams compact and avoids wasting vertical space.

A standalone exported diagram MAY include an internal title when it must make sense outside the document.

The diagram and its surrounding caption/text together MUST make clear:

- the view type and subject;
- the scope or boundary being shown;
- the viewpoint when it is not obvious, such as logical, runtime, deployment, current state, or target state;
- the meaning of every nonstandard shape, color, icon, border, arrowhead, or line style;
- abbreviations that the intended audience may not know.

Avoid generic captions such as `Architecture Diagram`, `Flowchart`, or `Module Diagram` without a subject and scope.
## 4. Elements and boundaries

### 4.1 Element information

Every element MUST have a unique, stable name within the document. Architecture-level elements SHOULD show:

```text
Element name
[Element type]
One-line responsibility
Technology/runtime (only when architecturally relevant)
```

Use nouns for elements and keep the same name in prose, tables, interfaces, and other diagrams. Do not use both `Data Manager` and `Storage Service` for the same module without defining the relationship.

Descriptions MUST state responsibility, not repeat the name. Technology labels MUST come from requirements, observed implementation, or an explicit design decision; do not infer them for decoration.

### 4.2 Boundaries

System, trust, process, device, and subsystem boundaries MUST be explicit when they affect responsibility, communication, security, deployment, failure containment, or ownership.

- A container/boundary label MUST state what it encloses.
- External actors and systems MUST be visually distinguishable from software owned by the design.
- A visual group MUST not imply deployment, ownership, or trust unless that meaning is stated.
- Nested boundaries SHOULD remain shallow enough to read at document page width; split the view when nesting obscures relationships.

For embedded and RTOS projects, do not use the C4 word `Container` without defining it. Prefer the actual runtime unit, such as process, firmware image, RTOS task group, MCU, SoC, or external module.

## 5. Relationships and arrows

Every important relationship MUST be directional and labeled with its intent. Use a verb phrase or named data/message, not an unlabeled line or a vague word such as `uses`.

Good examples:

- `publishes measurement samples`;
- `requests device configuration`;
- `reads calibration parameters`;
- `sends AlarmEvent via POSIX message queue`;
- `HTTPS/JSON device registration`.

The label MUST agree with the arrow direction. Cross-process, cross-device, or external relationships SHOULD identify the relevant protocol, interface, queue, bus, or file format. If one line would represent unrelated meanings, draw separate relationships or choose one meaning for the view.

Use these defaults consistently unless a formal notation requires another style:

| Relationship | Default rendering |
| --- | --- |
| Call, data transfer, or control flow | solid directed line with label |
| Compile-time or logical dependency | dashed directed line with label |
| Asynchronous message/event | directed line labeled with event/message and transport |
| Ownership/containment | enclosure or composition notation, not an ordinary call arrow |
| Proposed relationship in a combined current/target view | distinct dashed style plus explicit legend |

Do not rely on line color alone. Avoid bidirectional arrows; model two directed relationships when each direction has a distinct purpose.

## 6. Current state and target state

Prefer separate diagrams for current (`as-is`) and target (`to-be`) architecture. This avoids ambiguous mixed evidence.

If comparison in one diagram is materially clearer:

- mark each proposed element or relationship explicitly, for example `<<proposed>>`;
- provide a legend explaining the notation;
- use both text/line style and color so the distinction survives grayscale printing;
- never present a proposed element as confirmed implementation.

Greenfield diagrams MUST identify the architecture as proposed. Brownfield diagrams MUST be based on active code/configuration or other cited evidence. Simplified brownfield views MUST say that they are logical views rather than exhaustive call graphs.

## 7. Architecture view profiles

### 7.1 System context

The target software system MUST be the clear focal element. Include only people/roles, external systems/devices, and meaningful interactions across the system boundary.

- Actors SHOULD be roles, not personal names.
- Each external system/device SHOULD include a short responsibility or reason for interaction.
- Every relationship MUST describe the business/system intent.
- Do not include internal modules, databases owned entirely inside the system, source files, threads, or functions.

### 7.2 Logical architecture

Use this as the default overall architecture view for a non-trivial HLD. It MAY use a C4-inspired boxes-and-arrows notation, but must remain explicit about element types.

- Show the **overall system architecture first**. For an existing codebase, the parent logical architecture view MUST cover the **entire code project/repository in scope** at the chosen HLD abstraction level, rather than only one application module, feature, or subsystem. Use separate drill-down diagrams for complex subsystems.
- If the design is layered, the overall architecture diagram MUST look layered: use clearly separated horizontal bands (or another explicit layered arrangement), keep elements of one layer together, and make the allowed dependency direction obvious. Do not call a scattered component network a “layered architecture diagram”.
- If the design is not actually layered, do not force it into layers; name and draw the real structure instead.
- Choose one principal level: subsystem, layer, module, or component.
- Show dependency direction and architecturally important interfaces/data paths.
- Layers MUST not imply permitted dependencies that the arrows contradict.
- Shared services, platform adapters, drivers, and external dependencies MUST be clearly separated.
- A directory tree is not an architecture unless those directories correspond to verified responsibility boundaries.
- If the diagram is too dense at page width, retain an overview and create scoped detail views.

For embedded systems, a useful logical view often separates application/domain logic, services, platform abstraction, drivers, protocol adapters, and external hardware. Do not force those layers when the actual design uses a different boundary model.

### 7.3 UML component diagram

Use UML component notation only when component and interface semantics add value.

- Use component notation or an explicit `<<component>>` stereotype consistently.
- Show provided and required interfaces when interface ownership is important.
- A dependency arrow points from the dependent/client to the supplier.
- Use ports or assembly connectors only when their semantics are understood and relevant.
- Do not use UML component symbols merely as decorative rectangles.
- Do not mix class, deployment node, database, process, and component semantics without stereotypes and a legend.

If the design only needs module responsibilities and dependencies, name it `Logical Architecture` or `Module Dependency View` instead of claiming a formal UML component diagram.

## 8. Behavioral view profiles

### 8.1 Sequence diagram

- Time progresses from top to bottom; participant order SHOULD reflect the architectural path from initiator to downstream dependencies.
- Participants MUST be architectural actors/modules/services, not arbitrary helper functions unless the helper is itself an architectural boundary.
- Messages MUST use action-oriented names; include important data or interface names where useful.
- Distinguish synchronous calls, asynchronous messages, and returns consistently.
- Use `alt`, `opt`, `loop`, or equivalent combined fragments for meaningful alternatives, optional behavior, and repetition.
- Include critical timeout, rejection, retry, cancellation, or recovery paths when they affect the architecture.
- Avoid drawing a return arrow when it conveys no useful result or failure information.

### 8.2 State diagram

- Include an initial state; include a final state when the lifecycle actually terminates.
- State names MUST describe stable conditions, not actions.
- Transitions SHOULD follow `event [guard] / effect` when those parts exist.
- Guards leaving the same decision point SHOULD be mutually exclusive or have defined precedence.
- Every reachable state MUST have an entry path; unintended dead ends and unreachable states fail review.
- Timeouts, errors, cancellation, and recovery events MUST be shown when architecturally significant.

### 8.3 Activity diagram or general flowchart

- Use action-oriented step names.
- Every decision MUST have labeled outgoing conditions; `yes/no` is acceptable only when the decision question is explicit.
- Distinguish branch/merge from parallel fork/join.
- Show start and end points for a bounded workflow.
- Use swimlanes only when responsibility handoffs matter.
- Do not use a flowchart to represent static architecture dependencies.

## 9. Data, deployment, and runtime profiles

### 9.1 Data flow or pipeline

- Identify sources, sinks, transformations, queues/buffers, and stores with distinct, explained notation.
- Label edges with the data/message being transferred.
- Show ownership and lifecycle at points where copying, buffering, persistence, or cleanup changes.
- Distinguish data flow from control flow when both are present; prefer separate diagrams if the combined view becomes ambiguous.
- Show backpressure, overflow/drop behavior, or recovery only when it is an architectural concern.

### 9.2 Deployment diagram

- Distinguish physical devices/nodes, execution environments, processes/services, and deployed artifacts.
- Show where each architecturally important runtime unit executes.
- Label inter-node connections with protocol/transport and direction when relevant.
- Identify external infrastructure and trust/network boundaries when they affect the design.
- Do not place a logical module directly on hardware unless the mapping is an explicit deployment decision.

### 9.3 Runtime/concurrency diagram

Use only when execution contexts, IPC (Inter-Process Communication，进程间通信), ownership, or synchronization are necessary to understand the architecture.

- Identify processes, tasks/threads, event loops, ISR (Interrupt Service Routine，中断服务程序), DMA (Direct Memory Access，直接存储器访问), and timers by type.
- Show queue/channel direction, message ownership, shared resources, and synchronization boundaries.
- Label blocking vs non-blocking interaction when it affects scheduling or deadlock risk.
- Do not invent priority, period, stack size, queue depth, timeout, or execution budget; use confirmed values or mark proposed/TODO.
- Place this view in the conditional concurrency/tasking chapter when it expresses a system-wide execution architecture; otherwise place it with the owning architecture or module section. The diagram alone does not justify a standalone chapter.

### 9.4 Class or domain diagram

Use only for architecturally significant public types, domain relationships, extension points, or inheritance/composition decisions.

- Show the smallest type set needed to explain the architecture.
- Include multiplicity when it changes ownership or lifecycle meaning.
- Distinguish inheritance, composition, aggregation, and dependency correctly.
- Omit private members and routine methods unless they define a public contract.
- An exhaustive reverse-engineered class diagram is not an HLD diagram.

## 10. Visual and layout profile

The notation MUST remain understandable in grayscale and to readers with common color-vision differences.

- Use a restrained, consistent palette. Color conveys category or status, not decoration.
- Pair color meaning with labels, borders, stereotypes, or line styles.
- Use one font family and a consistent heading/label hierarchy across the document.
- Use consistent shapes for the same element type across diagrams.
- Prefer left-to-right for interaction/data flow and top-to-bottom for layering; state another convention in the legend.
- Minimize line crossings, long return paths, diagonal lines, and manual direction hacks.
- Keep labels close to their elements/relationships and avoid text placed over lines.
- Do not use icons unless they add domain meaning; explain non-obvious icons.
- A diagram MUST be readable at its final Markdown/DOCX page width. For a normal A4 portrait page, design for roughly 15–16 cm of usable figure width and an equivalent label size of about 9 pt or larger. Split overview/detail views instead of shrinking text to fit.
- Keep the canvas compact. Large empty margins, very wide aspect ratios, or dozens of small nodes are defects even when the source technically renders. As a practical heuristic, split a view when it grows beyond roughly 12–16 primary elements or 4–5 nested groups unless the larger view remains clearly readable at page width.
- When the document provides the figure caption, omit an internal diagram title by default.
- Landscape orientation MAY be used when the document format supports it and splitting would destroy the relationship being explained.

Decorative shadows, gradients, 3D boxes, vendor logos, and excessive colors SHOULD be avoided in formal HLD diagrams.

## 11. Diagram set for an HLD

Do not generate every possible view. Choose the minimum set that explains the architecture:

- a logical architecture view is normally expected for a non-trivial system;
- add a system context view when external actors/systems/devices or ownership boundaries are important;
- add sequence diagrams only for critical cross-boundary scenarios;
- add state diagrams only for state-governed behavior;
- add data-flow/pipeline views when data ownership and processing stages are central;
- add deployment or runtime/concurrency views only when placement or execution context changes architectural behavior.

Every included diagram MUST be referenced and interpreted by the surrounding text. A diagram without a documented purpose or a paragraph that merely repeats every label adds little value.

## 12. Review gate

A diagram fails review if any of the following is true:

- its type, scope, or viewpoint cannot be determined;
- it mixes abstraction levels without explicit notation and purpose;
- important elements lack names/types/responsibilities;
- important relationships are unlabeled, bidirectional without explanation, or contradict their arrows;
- custom colors, shapes, borders, or line styles have no legend;
- external/internal, current/proposed, or logical/deployment boundaries are ambiguous;
- it contradicts the HLD text, interface tables, or observed implementation;
- it claims unsupported technology, timing, priority, protocol, or resource values;
- it is unreadable at final page width, clipped after rendering, oversized enough to require tiny text, dominated by crossing lines, or contains excessive empty canvas;
- it is described as a layered architecture but the visual layout does not preserve clear layer bands and dependency direction;
- no editable `.puml`/`.mmd` source is retained for a generated diagram;
- a required SVG/PNG referenced by Markdown or DOCX is missing or stale.

Before accepting a diagram, verify:

- the architectural question is answered without unrelated detail;
- terminology matches the document;
- direction, labels, protocols, and ownership are correct;
- fault/alternate paths are present where they materially affect the design;
- current facts, proposed design, assumptions, and TODOs remain distinguishable;
- legend and abbreviations are sufficient for the intended audience;
- source, SVG, fallback PNG (when needed), caption, and document reference use matching names.

## 13. Degraded review when no vision-capable reviewer is available

If no model/person capable of visually inspecting the rendered image is available, do not silently treat the visual gate as passed. Perform a degraded automated review and state the limitation.

At minimum:

- parse the `.puml` / `.mmd` source to confirm the intended nodes, groups, directions, and labels are present;
- inspect SVG `viewBox`, width/height, text/font sizes, and bounding geometry when practical;
- for PNG, use PIL or an equivalent local image library to measure dimensions, content bounding box, excessive whitespace, and obvious clipping;
- verify the figure fits the target DOCX page-width budget without requiring unreadably small text;
- mark the result as “automated geometry/structure check only; no human/vision visual review” when that is the actual coverage.

## 14. References

- [OMG UML 2.5.1 specification](https://www.omg.org/spec/UML/2.5.1/PDF) — authoritative UML semantics and notation.
- [C4 model notation](https://c4model.com/diagrams/notation) — titles, element descriptions, relationship labels, protocols, legends, and accessible use of color.
- [C4 architecture diagram review checklist](https://c4model.com/diagrams/checklist) — practical semantic review questions.
- [PlantUML component diagram documentation](https://plantuml.com/component-diagram) — supported component/interface syntax; syntax support does not replace modeling rules.
- [Mermaid architecture diagram documentation](https://mermaid.js.org/syntax/architecture.html) — renderer syntax and layout behavior; use this standard for HLD semantics.

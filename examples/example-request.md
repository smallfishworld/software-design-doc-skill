# Example Requests

## 1. New project: requirements only, no code

```text
/software-design-doc

This is a new project and there is no source code yet.
Read docs/requirements.docx and generate a software high-level design in Chinese.
Do not invent implementation facts. Treat architecture/module/interface choices as proposed design decisions.
Use the company Word template docs/HLD-template.docx if the local document tool supports it.
```

Expected behavior:

- select Requirements-first / Greenfield mode;
- extract scope, actors, capabilities, constraints, external systems, and quality attributes;
- create system context and proposed architecture;
- map major requirements to modules/components;
- define high-level module responsibilities, interfaces, data ownership, and fault behavior;
- record assumptions/TODOs;
- generate only useful diagrams;
- create/fill DOCX when a local document tool is available.

## 2. Existing project: code only

```text
/software-design-doc

There is no reliable design document. Analyze the current repository and generate a software high-level design that describes the existing implementation.
```

Expected behavior:

- select Code-first / Brownfield mode;
- inspect entry points, build files, modules, interfaces, dependencies, data, configuration, and important runtime flows;
- use CodeGraph if available;
- distinguish actual implementation from recommendations;
- flag architectural risks separately from factual description.

## 3. Requirements plus implementation

```text
/software-design-doc

Read docs/requirements.md and analyze the current source tree. Update the HLD and identify any significant differences between the requirements and implementation.
```

Expected behavior:

- select Hybrid mode;
- keep requirement truth and implementation truth separate;
- identify missing implementation, undocumented behavior, drift, and inconsistencies;
- describe current architecture and recommended target design when useful.

## 4. Architecture review only

```text
/software-design-doc

Review the current architecture. Focus on module boundaries, dependency direction, shared-state ownership, interfaces, and maintainability. Do not generate the final HLD yet.
```

## 5. Embedded/RTOS project

```text
/software-design-doc

Analyze this RTOS project and generate the HLD. Integrate task/queue/semaphore/timer analysis into the relevant architecture and module sections; do not create a standalone task-design chapter unless explicitly requested.
```

## 6. Backend project

```text
/software-design-doc

Generate an HLD for this backend service from requirements and current code. Pay special attention to API boundaries, database ownership, asynchronous jobs, retries/timeouts, and external service failure handling.
```

## 7. Incremental update with a company template

```text
/software-design-doc
Update only the storage and fault-recovery design in the existing Word HLD for the revised retention requirement. Preserve the company chapter structure and approved architecture. Update affected diagrams and cross-references.
```

Expected behavior: inspect the current artifact, isolate the requirement's impact, preserve unrelated sections, expose unresolved migration decisions, and verify the edited Word pages.

## 8. Renderer unavailable on Linux

```text
/software-design-doc
Produce a Word HLD including an architecture diagram and a functional decomposition tree. PlantUML is unavailable. mmdc --version works, but actual rendering fails because Chromium is unavailable; Windows rendering can be completed later.
```

Expected behavior: choose tools by semantics, try the documented fallback, preserve Mermaid sources with figure destinations and Windows commands, complete useful content, and identify the Word output as a draft awaiting figures. A successful version check must not be reported as a successful render.

## 9. Markdown and Word diagram assets

```text
/software-design-doc
Generate the HLD in Markdown and Word. Keep every PlantUML/Mermaid diagram editable and make the figures remain sharp when zoomed or printed.
```

Expected behavior: keep `.puml`/`.mmd` as the authoritative editable source, generate matching SVG for relative Markdown references, use verified SVG insertion in DOCX, and fall back to a high-resolution PNG when the selected Word pipeline cannot reliably handle SVG. Do not describe the SVG embedded in Word as semantically editable PlantUML/Mermaid source.

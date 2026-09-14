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

Analyze this RTOS project and generate the HLD. Integrate task/queue/semaphore/timer analysis into the relevant architecture and module sections; do not create a standalone task-design chapter unless necessary.
```

## 6. Backend project

```text
/software-design-doc

Generate an HLD for this backend service from requirements and current code. Pay special attention to API boundaries, database ownership, asynchronous jobs, retries/timeouts, and external service failure handling.
```

# Software Design Document Skill

**English | [简体中文](README.zh-CN.md)**

A general-purpose AI skill for software high-level design (HLD), supporting requirements analysis, codebase analysis, architecture design, module design, interface design, design review, diagrams, and design-document generation across different languages, platforms, and software projects.

The skill can design a new system **from zero when only requirements exist and there is no source code or even no project directory yet**, reverse-engineer an existing codebase when design documentation is missing, or reconcile requirements with implementation when both are available.

The skill is deliberately scoped to **HLD document creation and review only**. It does not generate project scaffolding, directory trees, source-code skeletons, detailed-design documents, or implementation code.

The skill is designed to work well in offline or intranet environments. Core behavior is instruction-based and does not require Internet access. Optional tools such as CodeGraph, PlantUML, DOCX tooling, or Pandoc can improve analysis and document output when available.

## Working modes

- **Requirements-first / Greenfield** — generate a proposed HLD directly from requirements before a code project exists. No source tree or project skeleton is required.
- **Code-first / Brownfield** — recover the current architecture from an existing codebase.
- **Hybrid** — combine requirements and source code, checking for gaps and architectural drift.
- **Review-only** — review an existing architecture/design without generating a full replacement.

## Scope

This skill is intended to finish at the software high-level design document. It may inspect or propose architecture, modules, interfaces, data, fault handling, logging, security, testability, maintainability, risks, and diagrams as needed for the HLD, but it does not continue into project creation or coding.

## Highlights

- Start from zero with only a requirement document or even plain-text requirements
- Requirements-driven design works without an existing code project
- Requirements and source-code driven design instead of generic prose generation
- Evidence-aware writing: distinguishes confirmed facts, requirements, design proposals, assumptions, and unresolved items
- Architecture, module, data, interface, exception, logging, security, testability, maintainability, and risk analysis
- Adaptive profiles for backend, web, desktop, embedded Linux, RTOS, MCU, and other software projects
- Optional architecture diagrams and sequence/data-flow diagrams
- **Built-in standardized Word/DOCX template** for projects that do not provide a company template
- Company/project Word template preservation when a custom template is provided
- Prevents invented implementation details
- Supports Chinese and English documents

## Claude Code installation

### Personal skill

```bash
git clone https://github.com/smallfishworld/software-design-doc-skill.git
mkdir -p ~/.claude/skills/software-design-doc
cp -r software-design-doc-skill/* ~/.claude/skills/software-design-doc/
```

Then start Claude Code and invoke:

```text
/software-design-doc
```

Claude Code can also discover the skill automatically when a request matches its description.

### Project-level skill

```bash
mkdir -p .claude/skills/software-design-doc
cp -r /path/to/software-design-doc-skill/* .claude/skills/software-design-doc/
```

Project-level installation is useful when a project needs its own template or design conventions.

> For a brand-new project, installation does **not** mean you need to create the target software project first. The skill can run from any working directory and consume an external requirement document to design the system from zero.

## Example requests

### New project, no code and no project directory yet

```text
/software-design-doc
This is a brand-new project. No source code or project skeleton exists yet.
Read requirements.docx and generate a software high-level design in Chinese.
Treat architecture/module/interface choices as proposed design decisions and list assumptions explicitly.
```

Typical flow:

```text
Requirements
    ↓
System scope and boundaries
    ↓
Architecture proposal
    ↓
Module decomposition
    ↓
Interfaces and data design
    ↓
Fault/logging/security/testability analysis
    ↓
Risks and open decisions
    ↓
Software HLD document
```

### Existing codebase

```text
/software-design-doc
Analyze the current project and generate a software high-level design document describing the existing implementation.
```

### Requirements + code

```text
/software-design-doc
Analyze the current codebase and existing requirements. Generate the design in Chinese, identify major requirement/implementation gaps, and use docs/company-template.docx if possible.
```

### Word output with no custom template

```text
/software-design-doc
Generate the final software high-level design as a Word document.
No company template is provided; use the built-in standard template.
```

### Architecture review only

```text
/software-design-doc
Review the current software architecture only. Do not generate the final document yet.
```

More examples are in `examples/example-request.md`.

## Default Word template

The repository includes:

```text
templates/default-software-design-template.docx
```

It is used automatically when Word/DOCX output is requested and no user/company/project template has been specified.

Template priority is:

1. User/company template explicitly supplied for the task
2. Project-specific HLD/DOCX template
3. Built-in `templates/default-software-design-template.docx`
4. `templates/default-outline.md` when DOCX generation is unavailable or Markdown is requested

The built-in Word template contains an A4 cover page, document information, revision history, TOC field, heading styles, header/footer with page-number fields, and standardized tables for architecture/module/data/interface/error/risk content.

See `references/docx-template.md` for placeholder and editing rules.

## Default document structure

When no company template or explicit outline is provided, the skill uses a compact general-purpose structure:

1. Introduction
2. System Overview
3. Design Goals and Principles
4. Overall Software Architecture
5. Module High-Level Design
6. Data Design
7. Interface Design
8. Concurrency and Tasking Design (conditional candidate)
9. State Behavior Design (conditional candidate)
10. Performance, Real-Time, and Resource Design (conditional candidate)
11. Deployment, Upgrade, and Compatibility Design (conditional candidate)
12. Exception and Fault Handling
13. Logging and Observability
14. Security Design (when relevant)
15. Testability Design
16. Maintainability and Extensibility
17. Risks, Constraints, and Open Issues

For each candidate chapter, the skill applies a three-level decision: retain it when the concern has system-wide architectural impact, integrate it into the owning section when the impact is local, and delete it when irrelevant. Routine build commands and deployment procedures remain outside the HLD; architecturally significant toolchain, ABI, cross-compilation, topology, upgrade, and compatibility decisions remain in scope.

## Optional integrations

The core skill does not depend on any MCP server. When available, it can make use of:

- CodeGraph or equivalent code intelligence tools for dependency/call-graph analysis
- PlantUML for UML and architecture diagrams
- DOCX MCP, `python-docx`, Microsoft Word automation, or equivalent tools for direct Word output
- Pandoc for Markdown-to-DOCX conversion when a Markdown-first workflow is preferable

See `references/tool-integration.md` for behavior and fallback rules.

## Offline / intranet check

Run:

```bash
python3 scripts/check_environment.py
```

This only checks optional local integrations. The core requirements-first and design workflow does not depend on CodeGraph, PlantUML, Pandoc, or an Internet connection. The built-in Word template is already included in the repository.

## Repository layout

```text
software-design-doc-skill/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── templates/
│   ├── default-outline.md
│   └── default-software-design-template.docx
├── references/
│   ├── architecture-analysis.md
│   ├── document-rules.md
│   ├── platform-profiles.md
│   ├── diagram-standards.md
│   ├── diagram-guide.md
│   ├── tool-integration.md
│   └── docx-template.md
├── examples/
│   └── example-request.md
├── scripts/
│   ├── check_environment.py
│   └── build_default_template.py
└── tests/
    └── test_skill.py
```

## Design philosophy

The document must describe what is known and what is designed, not what the model merely assumes. Requirement facts, source-code facts, existing-document facts, design proposals, assumptions, and unresolved questions are tracked separately during analysis. Unsupported implementation details must never be presented as confirmed facts.

For greenfield work, the requirements are the factual baseline and the architecture is explicitly treated as a proposed design until implemented.

The skill favors high cohesion, low coupling, explicit dependencies, clear ownership, simple interfaces, and architecture that reflects the actual project rather than a textbook template.

## Review and delivery behavior

- Select requirements-first, code-first, or hybrid inputs independently of creation, incremental updates, or review-only output.
- Reviews report impact-ordered findings with locations, evidence, consequences, corrections, and coverage; they do not force Word generation.
- Probe only relevant capabilities using paths relative to the installed skill, not the current project directory.
- Prefer PlantUML for UML/software architecture and Mermaid for general flows, trees, functional decomposition, and relationships. [Diagram Guide](references/diagram-guide.md) owns tool, rendering, and format-fallback behavior.
- Apply the [Diagram Standard](references/diagram-standards.md) before rendering: declare the view and abstraction level, define elements/boundaries/relationships, use explicit legends and labels, follow type-specific semantics, and pass the review gate. A successful render is not a valid architecture review.
- Treat `.puml`/`.mmd` as the authoritative editable source. Prefer SVG for relative Markdown references and verified DOCX insertion; use high-resolution PNG as the compatibility fallback. SVG in Word offers vector scaling and limited graphic editing, not PlantUML/Mermaid semantic editing.
- Version checks do not prove rendering works. If Mermaid cannot render on Linux, retain `.mmd` and Windows commands; label a Word file missing figures as a draft.
- The Word template has a rebuild script. Check package integrity and actual page layout before delivery.

Scoped diagnostics (Python 3.9+, standard library only):

```bash
python3 scripts/check_environment.py --scope diagrams --plantuml-jar "/path/to/plantuml.jar"
python3 scripts/check_environment.py --scope docx --scope diagrams --json
python3 -m unittest discover -s tests -v
```

Tests need only the standard library; rebuilding the template additionally needs `python-docx`. Tests cover missing/failing/timed-out tools, JAR paths, DOCX integrity, fields, and local links. Template changes also require real rendering and page inspection.

## Status

Real-project feedback is welcome, especially for requirements-first design, company HLD templates, embedded/RTOS projects, backend services, desktop software, and Word document workflows.

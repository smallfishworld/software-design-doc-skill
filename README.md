# Software Design Document Skill

A general-purpose AI skill for software high-level design (HLD), supporting requirements analysis, codebase analysis, architecture design, module design, interface design, design review, diagrams, and design-document generation across different languages, platforms, and software projects.

The skill supports the full project lifecycle: it can design a new system from requirements when no code exists, reverse-engineer an existing codebase when design documentation is missing, or reconcile requirements with implementation when both are available.

The skill is designed to work well in offline or intranet environments. Core behavior is instruction-based and does not require Internet access. Optional tools such as CodeGraph, PlantUML, DOCX tooling, or Pandoc can improve analysis and document output when available.

## Working modes

- **Requirements-first / Greenfield** — generate a proposed HLD from requirements before implementation starts.
- **Code-first / Brownfield** — recover the current architecture from an existing codebase.
- **Hybrid** — combine requirements and source code, checking for gaps and architectural drift.
- **Review-only** — review an existing architecture/design without generating a full replacement.

## Highlights

- Requirements-driven design works even when there is no source code yet
- Requirements and source-code driven design instead of generic prose generation
- Evidence-aware writing: distinguishes confirmed facts, requirements, design proposals, assumptions, and unresolved items
- Architecture, module, data, interface, exception, logging, security, testability, maintainability, and risk analysis
- Adaptive profiles for backend, web, desktop, embedded Linux, RTOS, MCU, and other software projects
- Optional architecture diagrams and sequence/data-flow diagrams
- Optional Word/DOCX generation or company-template filling
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

Claude Code also discovers the skill automatically when a request matches its description.

### Project-level skill

```bash
mkdir -p .claude/skills/software-design-doc
cp -r /path/to/software-design-doc-skill/* .claude/skills/software-design-doc/
```

Project-level installation is useful when a project needs its own template or design conventions.

## Example requests

### New project, no code yet

```text
/software-design-doc
This is a new project. There is no source code yet.
Read docs/requirements.docx and generate a software high-level design in Chinese.
Treat architecture/module/interface choices as proposed design decisions and list assumptions explicitly.
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

### Architecture review only

```text
/software-design-doc
Review the current software architecture only. Do not generate the final document yet.
```

More examples are in `examples/example-request.md`.

## Default document structure

When no company template or explicit outline is provided, the skill uses a compact general-purpose structure:

1. Introduction
2. System Overview
3. Design Goals and Principles
4. Overall Software Architecture
5. Module High-Level Design
6. Data Design
7. Interface Design
8. Exception and Fault Handling
9. Logging and Observability
10. Security Design (when relevant)
11. Testability Design
12. Maintainability and Extensibility
13. Risks, Constraints, and Open Issues

Concurrency/tasking, state machines, performance/real-time behavior, and build/deployment are analyzed when relevant but are not standalone chapters by default. They are integrated into the appropriate architecture or module sections unless a user/template explicitly requests separate chapters.

## Optional integrations

The core skill does not depend on any MCP server. When available, it can make use of:

- CodeGraph or equivalent code intelligence tools for dependency/call-graph analysis
- PlantUML for UML and architecture diagrams
- DOCX MCP, `python-docx`, Microsoft Word automation, or equivalent tools for direct Word output
- Pandoc for Markdown-to-DOCX conversion

See `references/tool-integration.md` for behavior and fallback rules.

## Offline / intranet check

Run:

```bash
python3 scripts/check_environment.py
```

This only checks optional local integrations. The core requirements-first and design workflow does not depend on CodeGraph, PlantUML, Pandoc, or an Internet connection.

## Repository layout

```text
software-design-doc-skill/
├── SKILL.md
├── README.md
├── templates/
│   └── default-outline.md
├── references/
│   ├── architecture-analysis.md
│   ├── document-rules.md
│   ├── platform-profiles.md
│   ├── diagram-guide.md
│   └── tool-integration.md
├── examples/
│   └── example-request.md
└── scripts/
    └── check_environment.py
```

## Design philosophy

The document must describe what is known and what is designed, not what the model merely assumes. Requirement facts, source-code facts, existing-document facts, design proposals, assumptions, and unresolved questions are tracked separately during analysis. Unsupported implementation details must never be presented as confirmed facts.

For greenfield work, the requirements are the factual baseline and the architecture is explicitly treated as a proposed design until implemented.

The skill favors high cohesion, low coupling, explicit dependencies, clear ownership, simple interfaces, and architecture that reflects the actual project rather than a textbook template.

## Status

Initial version. Real-project feedback is welcome, especially for requirements-first design, company HLD templates, embedded/RTOS projects, backend services, desktop software, and Word document workflows.

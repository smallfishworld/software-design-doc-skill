# Built-in DOCX Template

The repository includes a standardized Word template at:

`templates/default-software-design-template.docx`

Use it when the user requests Word/DOCX output and no user/company/project-specific DOCX template has been supplied.

## Template priority

1. User/company template supplied for the task.
2. Project-specific HLD/DOCX template clearly intended for the document.
3. Built-in `templates/default-software-design-template.docx`.
4. `templates/default-outline.md` only when Word generation/editing is unavailable or Markdown is explicitly requested.

Never overwrite the built-in template. Copy it to the output path first, then edit the copy.

## What the built-in template contains

- A4 page layout.
- Cover page with project/document metadata placeholders.
- Document information table.
- Revision history table.
- Word table-of-contents field.
- Standard Heading 1 / Heading 2 / Heading 3 hierarchy.
- Header with project name, document title, and version.
- Footer with page-number field.
- Standardized tables for terminology, references, modules, data, interfaces, exception handling, and risks.
- A compact general-purpose HLD structure aligned with `templates/default-outline.md`.

The default standalone chapters intentionally exclude concurrency/tasking, state-machine design, performance/real-time design, and build/deployment. Analyze those topics when relevant, but integrate them into architecture/module/data/interface/risk sections unless a user or company template requests separate chapters.

## Main placeholders

Document metadata placeholders include:

- `{{PROJECT}}` — project/system name
- `{{DOC_ID}}` — document identifier
- `{{VER}}` — document version
- `{{AUTHOR}}` — author/compiler
- `{{REVIEWER}}` — reviewer
- `{{APPROVER}}` — approver
- `{{DATE}}` — date
- `{{CONF}}` — confidentiality classification
- `{{STATUS}}` — document status
- `{{SCOPE}}` — applicability/scope
- `{{DEPT}}` — department/team

Content tables contain sample placeholders such as `{{MODULE}}`, `{{RESP}}`, `{{DATA}}`, `{{IFACE}}`, and `{{DESC}}`. Replace them with real project content, duplicate rows/sections when required, and delete unused examples.

Unknown administrative values must not be invented. Keep a clear placeholder or mark the value as pending when the user has not supplied it.

## Editing rules

When generating the final Word document:

- Preserve existing page setup, styles, headers, footers, and table conventions.
- Replace instructional gray placeholder paragraphs with project-specific content.
- Duplicate module subsections as needed.
- Delete optional sections that are irrelevant rather than filling them with generic text.
- Insert architecture, data-flow, or sequence diagrams into the matching sections when they add value.
- Keep diagrams readable on A4 pages and give them descriptive captions when appropriate.
- Keep source-code-level detail out of the HLD unless it materially explains an architectural decision.
- Keep factual implementation statements separate from proposed design decisions in greenfield/hybrid work.

## Table of contents and fields

The DOCX contains Word fields for the table of contents and page numbers.

Prefer updating fields with Microsoft Word/Word automation when available. If the current local tool cannot refresh fields reliably, preserve the fields unchanged. Microsoft Word can update the table of contents after opening the generated file.

Do not replace the TOC field with fabricated page numbers.

## Output naming

Use a meaningful output filename when the user does not specify one, for example:

`<project>-software-high-level-design-v1.0.docx`

or for Chinese projects:

`<项目名称>软件概要设计说明书_V1.0.docx`

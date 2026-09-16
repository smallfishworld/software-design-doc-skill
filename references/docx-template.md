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

The default template includes four conditional candidate chapters: concurrency/tasking, state behavior, performance/real-time/resources, and deployment/upgrade/compatibility. Retain a candidate when it has system-wide architectural impact; integrate locally scoped content into the owning architecture/module/data/interface/fault/risk section; delete it when irrelevant. Remove the candidate marker from retained headings, and repair numbering, the table of contents, and cross-references after deletion. A supplied company template still controls chapter structure.

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

Content tables contain sample placeholders such as `{{MODULE}}`, `{{RESP}}`, `{{DATA}}`, `{{IFACE}}`, `{{CONTRACT}}`, and `{{DESC}}`. Replace them with real project content, duplicate rows/sections when required, and delete unused examples.

Unknown administrative values must not be invented. Keep a clear placeholder or mark the value as pending when the user has not supplied it.

## Editing rules

When generating the final Word document:

- Preserve existing page setup, styles, headers, footers, and table conventions.
- Replace instructional gray placeholder paragraphs with project-specific content.
- Duplicate module subsections as needed.
- Delete optional sections that are irrelevant rather than filling them with generic text.
- Apply the three-level candidate decision above; do not retain all four chapters mechanically.
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

## Validation before delivery

Reopen the edited DOCX with a document reader and verify that the ZIP package and XML parts are readable. Inspect body text, tables, headers, and footers for unreplaced instructional placeholders; unknown administrative metadata may remain explicitly pending. Preserve editable TOC/page fields rather than fabricating page numbers.

Ensure the rendering environment has Chinese fonts (the template requests Noto Sans CJK SC; use a suitable local replacement if unavailable). Render to pages with an available local Word/LibreOffice or document renderer and visually inspect every page for clipping, broken tables, missing glyphs, unreadable diagrams, and stranded headings. A successful file save alone does not validate layout. State clearly if visual verification or field refresh could not run.

Prefer SVG diagrams when the selected DOCX editor and target Word/LibreOffice workflow have been verified to insert and render them correctly. Otherwise insert a high-resolution PNG fallback. In both cases preserve the matching `.puml`/`.mmd` source and SVG outside the DOCX. Word's limited SVG editing does not replace source-level PlantUML/Mermaid editing. See [diagram-guide.md](diagram-guide.md).

## Maintainer rebuild

The template source is [build_default_template.py](../scripts/build_default_template.py). Python 3.9+ and `python-docx` are needed **only to rebuild**, not to use the distributed template. The script preserves A4 sizing, Chinese headings, document-control placeholders, tables, headers/footers, and real TOC/page fields.

```bash
python3 scripts/build_default_template.py
python3 -m unittest discover -s tests -v
```

Run from the repository root. For a preview, use `--output /path/to/preview.docx`. After a layout change, render and visually inspect the rebuilt template before committing it. Keep the 13 default chapter meanings aligned with `default-outline.md`; unused optional chapters must be removed and renumbered in the final project document. Commit DOCX as binary through Git (or a base64-aware API); do not pass it through a UTF-8 text update endpoint.

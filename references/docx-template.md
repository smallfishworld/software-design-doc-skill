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
- Keep diagrams readable on A4 pages and give them descriptive captions when appropriate. Do not duplicate the same title inside the rendered diagram when the document caption already provides it.
- Keep source-code-level detail out of the HLD unless it materially explains an architectural decision.
- Keep factual implementation statements separate from proposed design decisions in greenfield/hybrid work.

## Safe editing of an existing DOCX

When modifying an existing Word file, preservation is more important than convenience.

- If the user has edited the DOCX directly, treat that DOCX as the source of truth; do not rebuild unaffected chapters from Markdown.
- Never edit in place first. Write to a new output path, reopen and validate it, then replace/copy over the intended destination only after checks pass. Keep a backup of the accepted input.
- Do **not** parse `word/document.xml` (or another complex Word XML part) with ElementTree/lxml and serialize the entire part merely to make a local edit. Whole-part reserialization can rewrite namespace prefixes and extension markup; Word compatibility metadata such as `mc:Ignorable` may refer to prefix names as literal attribute values, so a syntactically parseable rewrite can still become incompatible or invalid to Word. Use `python-docx` for structures it safely supports, or exact raw-XML block replacement for preservation-sensitive edits.
- For raw XML work, isolate exact `<w:tbl>...</w:tbl>`, `<w:tr>...</w:tr>`, `<w:tc>...</w:tc>`, `<w:p>...</w:p>`, or `<w:r>...</w:r>` blocks and edit only the required block before concatenating the untouched XML back around it.
- Do not use `re.S` / DOTALL expressions that can cross Word run or paragraph boundaries. A regex intended for one text node should use a bound such as `[^<]*` so it cannot consume adjacent runs.
- Distinguish “replace the complete run/text node” from “replace a substring inside one text node”. Every replacement MUST report the number of matches; zero matches or more matches than expected is an error, not a silent success.
- Avoid opening a DOCX ZIP for output at the same path while it is still the input source. Read from the accepted source and write a separate package.

## Table layout requirements

Word tables need explicit paragraph and width rules; visual alignment cannot be inferred from text alone.

- Cover/metadata tables SHOULD be narrower and centered. Do not default them to the full usable page width. Body data tables MAY use the full text width when that improves readability.
- Paragraphs inside table cells MUST NOT inherit the body first-line indent. Set `w:ind w:firstLine="0"` (or the equivalent paragraph API) for cell paragraphs while preserving the normal body first-line indent outside tables.
- `w:tblGrid/w:gridCol@w:w` and each corresponding cell `w:tcW@w:w` MUST agree. Updating only one representation is invalid because Word may render from the grid.
- Preserve code and identifiers exactly, including case and spaces. For code-like cells, use a monospaced font such as Consolas around 9 pt when compatible with the template. Insert explicit `<w:br/>` only at intentional logical breakpoints; do not rely on Word's arbitrary wrapping to separate tokens.

## Post-generation machine validation

Before visual delivery, run machine checks that can catch corruption early:

1. ZIP/CRC integrity and XML parseability for all changed XML parts.
2. Exact round-trip comparison for known code/identifier text after DOCX extraction; source snippets are the primary oracle.
3. Heuristic scans for suspicious token corruption, such as altered C/C++ keywords (`int`, `void`, `bool`, `const`) or accidental token concatenation/case changes.
4. Table-cell paragraph indentation: `firstLine` absent/zero inside cells, while ordinary body paragraph indentation remains untouched.
5. `tblGrid` and `tcW` width consistency for every non-merged table row that was edited.
6. Reopen the generated DOCX and inspect the affected tables/figures after rendering when a rendering tool is available.

Use the bundled validator for the mechanical checks:

```bash
python3 scripts/validate_docx.py output.docx --strict-tables
python3 scripts/validate_docx.py output.docx --strict-tables \
  --expect-text "ACOUSTIC_DETECT_MODE mode_id" --scan-code
```

For a document containing many critical identifiers, place one exact expected string per line in a UTF-8 file and pass `--expect-file expected-identifiers.txt`. Exact expected-text checks are stronger than heuristic keyword scans and should be preferred when source Markdown/code is available.

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

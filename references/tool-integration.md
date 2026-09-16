# Optional Tool Integration and Fallback Rules

The skill must remain usable with only Claude Code and local project files. External tools are optional accelerators, not hard dependencies, but their availability must be discovered at the beginning of each skill run so installed tools are actually used.

## Startup capability discovery

Before architecture analysis or drafting, run the lightweight capability check described in `SKILL.md`. Prefer:

```bash
python3 scripts/check_environment.py
```

The check verifies command/module usability only. Do not render a test diagram or create temporary output solely for environment detection.

Successful checks should normally remain quiet. Mention a missing tool only when it changes the requested output or causes a fallback.

## Code intelligence / CodeGraph

When CodeGraph or an equivalent repository-aware code analysis tool is available, use it for:

- module and dependency discovery;
- call relationships;
- entry-point analysis;
- cross-file symbol relationships;
- identifying cycles or unexpected coupling;
- validating architecture statements against code.

Do not require CodeGraph for requirements-first/greenfield design. When no code exists, it provides no value and should be skipped.

If CodeGraph is unavailable, inspect repository files directly: build definitions, source directories, public headers/APIs, schemas, configuration, tests, and entry points.

## Diagram rendering: PlantUML > Mermaid > Text

Use this fallback order for HLD diagrams:

1. **PlantUML** when its command/JAR invocation is usable.
2. **Mermaid** when PlantUML is unavailable and a Mermaid renderer such as `mmdc` is usable.
3. **Text/ASCII plus structured description** when neither renderer is usable.

### PlantUML

PlantUML is the preferred diagram tool for versionable architecture/UML diagrams. If it is available and a diagram materially improves the HLD, actually use it rather than silently choosing another representation.

Typical command installation:

```bash
plantuml -version
plantuml architecture.puml
```

Typical local JAR installation:

```bash
java -version
java -jar plantuml.jar -version
java -jar plantuml.jar architecture.puml
```

Prefer storing `.puml` source next to generated images when practical.

### Mermaid fallback

If PlantUML is unavailable, check whether Mermaid CLI/rendering is usable:

```bash
mmdc --version
```

Use Mermaid only when the current environment can render it into a format usable by the requested deliverable.

If Mermaid source can be produced but cannot be rendered for a final DOCX, do not insert raw Mermaid source and call it a finished diagram. Fall back to structured text/tables or another renderable mechanism.

## Word / DOCX output

If the user requests a Word document, resolve the DOCX template first:

1. User/company template supplied for the task.
2. Project-specific HLD/DOCX template.
3. Built-in `templates/default-software-design-template.docx`.

Prefer direct local DOCX manipulation when a template must be preserved.

Possible local methods, in preference order when available:

1. A reliable DOCX/document MCP or document-editing tool that can open and modify an existing `.docx` template.
2. `python-docx` or equivalent local library for creating/modifying DOCX files.
3. Microsoft Word COM automation on Windows when exact Word behaviors such as TOC refresh or advanced fields are required.
4. Pandoc when the workflow is naturally Markdown-first and exact template fidelity is not critical.

When a template is used, work on a copy and preserve its styles, headings, headers/footers, tables, and document conventions as far as the selected tool permits.

When no company/project template exists, use the built-in standardized DOCX template rather than starting a blank Word document.

Do not claim that a DOCX file was created if the current environment has no file/document tool capable of creating it. In that case, generate the complete structured content using `templates/default-outline.md` and explain the required local conversion step.

See `references/docx-template.md` for template placeholders and editing rules.

## Pandoc

Pandoc is optional, not required by the skill. It is useful for converting Markdown to DOCX in fully offline environments.

Example with a company template:

```bash
pandoc design.md --reference-doc=company-template.docx -o software-design.docx
```

Pandoc's `--reference-doc` primarily transfers styles; it is not equivalent to directly filling a complex Word template. Prefer direct DOCX editing when cover pages, document-control tables, precise layout, fields, or complex placement must be retained.

## Requirements documents

When requirements are supplied as DOCX/PDF/Markdown/text:

- use the available local document-reading mechanism;
- extract only information needed to design the architecture;
- preserve requirement identifiers when available for traceability;
- distinguish mandatory requirements from examples, commentary, or historical notes.

If a requirement document cannot be read in the current environment, do not invent its contents. Use any text provided by the user and mark missing source material as unresolved.

## Intranet/offline operation

The skill itself requires no network calls. For intranet use:

- clone/download the repository outside the isolated network;
- copy the skill directory into `~/.claude/skills/software-design-doc/` or the project's `.claude/skills/software-design-doc/`;
- the built-in DOCX template is included in the repository and needs no online download;
- install optional PlantUML, Python libraries, Pandoc, Mermaid CLI, or MCP servers from approved offline packages if needed;
- configure Claude/model API base URL and key separately from this skill according to the organization's gateway/API setup.

Never store API keys, tokens, passwords, or company secrets in the skill repository.

## Tool availability principle

Always degrade gracefully:

- no code → requirements-first design;
- code but no CodeGraph → inspect files directly;
- PlantUML unavailable → use a renderable Mermaid environment;
- PlantUML and Mermaid unavailable → text/ASCII plus structured description;
- DOCX tool available but no company template → use `templates/default-software-design-template.docx`;
- no DOCX tool → produce structured Markdown using `templates/default-outline.md`.

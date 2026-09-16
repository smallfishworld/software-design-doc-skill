# Optional Tool Integration and Fallback Rules

The skill works with a capable coding agent and accessible requirements/project files. Optional integrations accelerate analysis or enable a requested file format; they are not prerequisites for a text review. No specific agent CLI is required.

## Startup capability discovery

Resolve the task first, then check only the capabilities it needs. Run the bundled script using its absolute path, regardless of the project working directory:

```bash
python3 /path/to/software-design-doc/scripts/check_environment.py --scope diagrams
python3 /path/to/software-design-doc/scripts/check_environment.py --scope docx --scope diagrams --json
python3 /path/to/software-design-doc/scripts/check_environment.py --scope diagrams --plantuml-jar "/path/to/plantuml.jar"
```

No arguments checks all optional local integrations. `PLANTUML_JAR` is also supported. The script requires Python 3.9+ and the standard library; it reports missing capabilities without failing the core workflow. Exit status zero means the diagnostic completed, not that all tools are installed. The `available` property means a command/import probe succeeded, not that a real render succeeded.

Do not generate test diagrams just for discovery. Verify actual outputs later. Inspect agent-exposed document and repository tools separately; the script cannot enumerate them. Text-only reviews need no renderer probes. Keep successful checks quiet and mention limitations only when they affect deliverables.

## Code intelligence / CodeGraph

When CodeGraph or an equivalent repository-aware tool is available and its index matches the selected repository/revision, use it for:

- module and dependency discovery;
- call relationships;
- entry-point analysis;
- cross-file symbol relationships;
- identifying cycles or unexpected coupling;
- validating architecture statements against code.

Do not require CodeGraph for requirements-first/greenfield design. When no code exists, it provides no value and should be skipped.

Validate important tool-derived claims against source locations. A stale or partial index does not establish that a feature is absent. If CodeGraph is unavailable or unsuitable, inspect repository files directly: build definitions, source directories, public headers/APIs, schemas, configuration, tests, and entry points.

## Diagram workflow

Follow [diagram-guide.md](diagram-guide.md), the authoritative diagram policy. It defines semantic tool selection, actual rendering checks, PlantUML-to-Mermaid fallback, source/SVG/PNG asset ownership, Markdown references, DOCX compatibility fallback, and Windows handoff when Mermaid cannot render locally. Keep the policy there rather than maintaining a second fallback chain here.

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

## Delivery limitations

Continue useful analysis when an optional capability is unavailable. Distinguish a text review, a complete Markdown document, a Word draft awaiting figures, and a validated final DOCX. Record only relevant limitations and the concrete completion steps; never claim an unavailable conversion, render, or field refresh succeeded.

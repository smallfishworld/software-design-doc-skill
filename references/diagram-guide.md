# Diagram Tool and Delivery Guide

This file owns tool selection, rendering, source/SVG/PNG assets, and fallback rules. Before authoring or reviewing an HLD diagram, apply [diagram-standards.md](diagram-standards.md) for semantics, abstraction levels, notation, layout, and the acceptance gate. Use a small set of diagrams that clarify architecture; diagram count is not a quality target.

## Select by meaning

| Diagram purpose | Preferred tool | Include when |
| --- | --- | --- |
| Formal UML: component, class, sequence, state, deployment; UML activity only when its semantics matter | PlantUML | Formal UML notation/semantics add value |
| Layered logical architecture, block diagram, ordinary flowchart, data pipeline, tree, functional decomposition, mind map, general relationship | Mermaid | Clean hierarchy/flow/layout matters more than formal UML notation |

Distinguish a UML activity model from a general flowchart by its semantics, not merely by the presence of arrows. Prefer Mermaid for ordinary process flows and block diagrams; do not use PlantUML activity syntax merely because it is available. A simple sequence within one module usually needs only prose. Use state diagrams only when explicit states govern behavior; place deployment and thread diagrams in their conditional candidate chapters only when they express a system-wide architectural view, otherwise keep them with the owning section.

For greenfield work, label proposed/optional elements. For existing systems, derive relationships from active code/configuration. Mark a simplified diagram as a logical view and distinguish observed architecture from a recommended target.

For document-embedded figures, keep the figure title/caption in the DOCX/Markdown by default rather than rendering the same title inside the image. Design the source for the final page width, not for an unconstrained browser canvas.

## Mermaid on Linux

A working `mmdc` command can still fail when Chromium/Puppeteer is missing or sandboxing is blocked. Probe the actual render path. When an approved local Chrome/Chromium executable exists, a project-local Puppeteer config can be used:

```json
{
  "executablePath": "/usr/bin/chromium",
  "args": ["--no-sandbox", "--disable-setuid-sandbox"]
}
```

Use the actual executable path found on the machine; do not copy `/usr/bin/chromium` blindly.

```bash
mmdc -p puppeteer-config.json -i "flow.mmd" -o "flow.svg"
```

If SVG must be rasterized and Mermaid cannot emit a usable PNG, an installed `chrome-headless-shell` / Chrome headless executable may be used as a fallback:

```bash
chrome-headless-shell --headless --no-sandbox --disable-gpu \
  --window-size=1800,1200 --screenshot="flow.png" "file:///absolute/path/flow.svg"
```

Validate the resulting crop and whitespace; a screenshot is not automatically a good document figure.

## PlantUML layout control

PlantUML auto-layout is useful but can scatter architectural blocks. For a genuinely layered view, group each layer in a package/rectangle and use hidden relationships only to control layout, while keeping real inter-layer relationships separately labeled. Hidden arrows are layout constraints only; never let them imply architecture semantics. If the block diagram is still unstable or visually cluttered, switch to Mermaid rather than accumulating layout hacks.

## Render and verify

1. Save editable `.puml` or `.mmd` source with a descriptive name.
2. Use the selected renderer on the actual diagram. A successful version check establishes command availability only; Mermaid may still lack a working browser and PlantUML may lack layout dependencies/fonts.
3. Check the exit status and that a new nonempty image was produced. Do not reuse a stale output after failure. Open the image to check labels, fonts, arrow direction, clipping, and readability at the intended page width. If no vision-capable reviewer is available, run the automated geometry/structure fallback defined in `diagram-standards.md` and explicitly record that limitation.
4. Generate SVG (Scalable Vector Graphics，可缩放矢量图形) as the preferred presentation asset. Generate a high-resolution PNG (Portable Network Graphics，便携式网络图形) fallback when the DOCX tool, converter, target Word version, or downstream renderer has not been verified with SVG.
5. Insert the image with its caption in the matching section and check the rendered document page.

## Source and output ownership

Use one matching basename for the editable source and rendered assets:

```text
diagrams/
├── system-architecture.puml
├── system-architecture.svg
└── system-architecture.png
```

For a Mermaid diagram, replace `.puml` with `.mmd`. The files have distinct roles:

- `.puml` / `.mmd`: authoritative editable source and version-review artifact;
- `.svg`: preferred Markdown and DOCX presentation asset because it remains sharp when scaled;
- `.png`: compatibility fallback, not the primary editable source.

Do not treat an SVG embedded in Word as the authoritative diagram source. Word can resize, crop, recolor, and in some environments convert SVG graphics to shapes, but it does not preserve PlantUML/Mermaid nodes, relationships, or source semantics. Make design changes in `.puml`/`.mmd`, regenerate the SVG/PNG, and replace the document image.

## Markdown and DOCX use

Prefer a relative SVG reference in Markdown so repository moves, offline use, and regeneration remain practical:

```markdown
![System architecture](diagrams/system-architecture.svg)
```

Keep the diagram source and referenced SVG in the delivered directory/repository. If the target Markdown renderer cannot display SVG, reference the PNG fallback and keep the SVG alongside it.

For DOCX, use this order:

1. Test whether the selected document-editing pipeline can insert the actual SVG and whether the target Word/LibreOffice workflow renders it correctly.
2. If verified, insert SVG for vector quality and retain source files outside the DOCX.
3. If insertion, conversion, or rendering is unreliable, insert a high-resolution PNG while retaining `.puml`/`.mmd` and SVG as companion assets.
4. Render the final DOCX and inspect the diagram at normal page width and enlarged view. A successful insertion call alone is not proof of compatibility.

Typical local commands (quote paths containing spaces):

```bash
plantuml -tsvg "architecture.puml"
java -jar "/path/to/plantuml.jar" -tsvg "architecture.puml"
mmdc -i "flow.mmd" -o "flow.svg"
mmdc -i "flow.mmd" -o "flow.png" -s 2
```

Use only the applicable command. Keep rendering local by default. A public rendering service requires separate authorization to receive project content.

## Fallback and handoff

- PlantUML unavailable or fails: correct an evident source/configuration issue if feasible, then convert the intended relationships to an appropriate Mermaid representation and try `mmdc`. Do not assume the syntaxes are interchangeable; retain the original `.puml` if useful.
- Mermaid unavailable or fails: diagnose once, make a targeted fix if available, and retry. Avoid repeated identical runs or unsolicited package installation.
- Mermaid cannot render in the current Linux environment: preserve `.mmd` and give Windows handoff commands. Do not claim all Linux environments lack support.

For each pending figure provide the source filename, intended document section/caption, output filename, and the failed/missing capability. Example PowerShell commands, assuming Mermaid CLI is already installed:

```powershell
mmdc -i ".\flow.mmd" -o ".\flow.svg"
mmdc -i ".\flow.mmd" -o ".\flow.png" -s 2
```

After rendering on Windows (or another working environment), use the verified SVG in Markdown and insert SVG into DOCX when the selected pipeline is verified; otherwise insert the verified high-resolution PNG. When no such environment is accessible, finish useful document content, clearly label it as a draft awaiting figures, and list the handoff steps. Do not stop all analysis or claim a final illustrated Word deliverable.

ASCII drawings and raw Mermaid/PlantUML code are not finished Word diagrams. A Markdown deliverable may include a diagram fence if its viewer supports rendering; state when it has not been rendered locally.

## Semantic consistency

- Apply the review gate in [diagram-standards.md](diagram-standards.md); rendering success does not establish semantic correctness.
- Diagram identifiers match module/interface names in the document.
- Arrows have intentional, preferably labeled meaning: dependency, control, data, or ownership.
- Text and diagrams agree about interface direction, lifecycle, and boundaries.
- Proposed and existing elements remain distinguishable.
- Detail fits the page and the HLD's granularity; split an overcrowded view instead of shrinking it until unreadable.

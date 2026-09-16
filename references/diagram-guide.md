# Diagram Guide

This file owns diagram selection, rendering, and fallback rules. Use a small set of diagrams that clarify architecture; diagram count is not a quality target.

## Select by meaning

| Diagram purpose | Preferred tool | Include when |
| --- | --- | --- |
| UML / architecture: context, component, class, sequence, state, activity, deployment | PlantUML | Boundaries or interactions need a modeled view |
| General flowchart, data pipeline, tree, functional decomposition, mind map, relationship | Mermaid | Flow or hierarchy is clearer visually |

Distinguish a UML activity model from a general flowchart by its semantics, not merely by the presence of arrows. A simple sequence within one module usually needs only prose. Use state diagrams only when explicit states govern behavior; deployment and thread diagrams are conditional architectural views, not default standalone chapters.

For greenfield work, label proposed/optional elements. For existing systems, derive relationships from active code/configuration. Mark a simplified diagram as a logical view and distinguish observed architecture from a recommended target.

## Render and verify

1. Save editable `.puml` or `.mmd` source with a descriptive name.
2. Use the selected renderer on the actual diagram. A successful version check establishes command availability only; Mermaid may still lack a working browser and PlantUML may lack layout dependencies/fonts.
3. Check the exit status and that a new nonempty image was produced. Do not reuse a stale output after failure. Open the image to check labels, fonts, arrow direction, clipping, and readability at the intended page width.
4. Prefer SVG (Scalable Vector Graphics，可缩放矢量图形) where the output pipeline supports it. Use PNG (Portable Network Graphics，便携式网络图形) for direct `python-docx` insertion; retain SVG/source for later vector use. Test actual support instead of assuming every Word library accepts SVG.
5. Insert the image with its caption in the matching section and check the rendered document page.

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

After rendering on Windows (or another working environment), insert the verified SVG/PNG into the final DOCX. When no such environment is accessible, finish useful document content, clearly label it as a draft awaiting figures, and list the handoff steps. Do not stop all analysis or claim a final illustrated Word deliverable.

ASCII drawings and raw Mermaid/PlantUML code are not finished Word diagrams. A Markdown deliverable may include a diagram fence if its viewer supports rendering; state when it has not been rendered locally.

## Semantic consistency

- Diagram identifiers match module/interface names in the document.
- Arrows have intentional, preferably labeled meaning: dependency, control, data, or ownership.
- Text and diagrams agree about interface direction, lifecycle, and boundaries.
- Proposed and existing elements remain distinguishable.
- Detail fits the page and the HLD's granularity; split an overcrowded view instead of shrinking it until unreadable.

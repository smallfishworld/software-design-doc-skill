#!/usr/bin/env python3
"""Validate DOCX package integrity and preservation-sensitive layout invariants.

Examples:
  python3 scripts/validate_docx.py design.docx --strict-tables
  python3 scripts/validate_docx.py design.docx --expect-text "ACOUSTIC_DETECT_MODE mode_id"
  python3 scripts/validate_docx.py design.docx --expect-file expected-identifiers.txt --scan-code
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import sys
from typing import Iterable
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}
W = f"{{{W_NS}}}"


@dataclass
class Finding:
    severity: str
    code: str
    location: str
    message: str


def attr(element, local: str, default=None):
    if element is None:
        return default
    return element.get(f"{W}{local}", default)


def xml_text(root: ET.Element) -> str:
    paragraphs = []
    for p in root.findall(".//w:p", NS):
        parts = []
        for node in p.iter():
            if node.tag == f"{W}t":
                parts.append(node.text or "")
            elif node.tag in (f"{W}br", f"{W}cr"):
                parts.append("\n")
            elif node.tag == f"{W}tab":
                parts.append("\t")
        paragraphs.append("".join(parts))
    return "\n".join(paragraphs)


def load_expected(values: Iterable[str], files: Iterable[Path]) -> list[str]:
    expected = [v for v in values if v]
    for path in files:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.lstrip().startswith("#"):
                expected.append(line)
    return expected


def validate_tables(document: ET.Element, strict_tables: bool) -> list[Finding]:
    findings: list[Finding] = []
    severity = "error" if strict_tables else "warning"

    for ti, table in enumerate(document.findall(".//w:tbl", NS), start=1):
        grid = []
        for col in table.findall("w:tblGrid/w:gridCol", NS):
            value = attr(col, "w")
            if value and value.isdigit():
                grid.append(int(value))

        for ri, row in enumerate(table.findall("w:tr", NS), start=1):
            grid_before = row.find("w:trPr/w:gridBefore", NS)
            col_index = int(attr(grid_before, "val", "0") or "0")
            for ci, cell in enumerate(row.findall("w:tc", NS), start=1):
                for pi, p in enumerate(cell.findall("w:p", NS), start=1):
                    ind = p.find("w:pPr/w:ind", NS)
                    first = attr(ind, "firstLine")
                    first_chars = attr(ind, "firstLineChars")
                    if first not in (None, "0") or first_chars not in (None, "0"):
                        findings.append(Finding(
                            "error", "TABLE_FIRST_LINE_INDENT",
                            f"table {ti} row {ri} cell {ci} paragraph {pi}",
                            f"table-cell paragraph inherits first-line indent: firstLine={first!r}, firstLineChars={first_chars!r}",
                        ))

                tc_pr = cell.find("w:tcPr", NS)
                span_el = tc_pr.find("w:gridSpan", NS) if tc_pr is not None else None
                span = int(attr(span_el, "val", "1") or "1")
                tc_w = tc_pr.find("w:tcW", NS) if tc_pr is not None else None
                width_type = attr(tc_w, "type", "dxa")
                width_value = attr(tc_w, "w")

                if grid and width_type == "dxa" and width_value and width_value.isdigit():
                    expected_slice = grid[col_index:col_index + span]
                    if len(expected_slice) == span:
                        expected_width = sum(expected_slice)
                        actual_width = int(width_value)
                        if actual_width != expected_width:
                            findings.append(Finding(
                                severity, "TABLE_GRID_WIDTH_MISMATCH",
                                f"table {ti} row {ri} cell {ci}",
                                f"tcW={actual_width} but tblGrid span width={expected_width}",
                            ))
                col_index += span
    return findings


def validate_docx(path: Path, expected: Iterable[str] = (), *, strict_tables: bool = False,
                  scan_code: bool = False) -> list[Finding]:
    findings: list[Finding] = []
    if not path.exists():
        return [Finding("error", "FILE_NOT_FOUND", str(path), "DOCX file does not exist")]

    try:
        with ZipFile(path) as zf:
            corrupt = zf.testzip()
            if corrupt:
                findings.append(Finding("error", "ZIP_CRC", corrupt, "ZIP member failed CRC validation"))

            xml_roots: dict[str, ET.Element] = {}
            for name in zf.namelist():
                if name.endswith(".xml") or name.endswith(".rels"):
                    try:
                        xml_roots[name] = ET.fromstring(zf.read(name))
                    except ET.ParseError as exc:
                        findings.append(Finding("error", "XML_PARSE", name, str(exc)))

            document = xml_roots.get("word/document.xml")
            if document is None:
                findings.append(Finding("error", "DOCUMENT_XML_MISSING", "word/document.xml",
                                        "main Word document part is missing or unreadable"))
                return findings

            findings.extend(validate_tables(document, strict_tables))

            searchable = []
            for name, root in xml_roots.items():
                if name.startswith("word/") and name.endswith(".xml"):
                    searchable.append(xml_text(root))
            full_text = "\n".join(searchable)

            for item in expected:
                if item not in full_text:
                    findings.append(Finding(
                        "error", "EXPECTED_TEXT_MISSING", str(path),
                        f"expected text/identifier not found exactly: {item!r}",
                    ))

            if scan_code:
                suspicious_case = re.compile(
                    r"\b(?:Int|Void|Vaid|Bool|Boal|Const|Static|Struct|Enum|Typedef|Unsigned|Signed)\b"
                )
                for match in suspicious_case.finditer(full_text):
                    findings.append(Finding(
                        "warning", "SUSPICIOUS_CODE_TOKEN", str(path),
                        f"review possible code-token case/spelling corruption near {match.group(0)!r}",
                    ))
    except BadZipFile as exc:
        findings.append(Finding("error", "BAD_ZIP", str(path), str(exc)))

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", type=Path)
    parser.add_argument("--expect-text", action="append", default=[],
                        help="exact text/identifier that must survive in the DOCX; repeatable")
    parser.add_argument("--expect-file", action="append", type=Path, default=[],
                        help="UTF-8 file containing one exact required text/identifier per line")
    parser.add_argument("--strict-tables", action="store_true",
                        help="treat tblGrid/tcW mismatches as errors instead of warnings")
    parser.add_argument("--scan-code", action="store_true",
                        help="warn on suspicious C/C++ keyword case/spelling mutations")
    parser.add_argument("--fail-on-warning", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    expected = load_expected(args.expect_text, args.expect_file)
    findings = validate_docx(args.docx, expected, strict_tables=args.strict_tables,
                             scan_code=args.scan_code)

    if args.json:
        print(json.dumps({"file": str(args.docx), "findings": [asdict(f) for f in findings]},
                         ensure_ascii=False, indent=2))
    else:
        if not findings:
            print(f"OK: {args.docx}")
        for f in findings:
            print(f"{f.severity.upper()} {f.code} [{f.location}]: {f.message}")

    has_error = any(f.severity == "error" for f in findings)
    has_warning = any(f.severity == "warning" for f in findings)
    if has_error or (args.fail_on_warning and has_warning):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

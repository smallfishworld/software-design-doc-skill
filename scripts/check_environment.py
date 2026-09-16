#!/usr/bin/env python3
"""Probe optional local commands/imports, without rendering or creating artifacts.

Python 3.9+; standard library only. A successful probe is not a render test.
Missing optional tools are reported as data and do not make this command fail.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass


@dataclass
class Check:
    name: str
    available: bool
    detail: str


def probe(name: str, command: list[str], timeout: float = 5) -> Check:
    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, errors="replace", timeout=timeout, check=False,
        )
        lines = (result.stdout or "").strip().splitlines()
        detail = lines[0][:300] if lines else "command completed"
        if result.returncode != 0:
            return Check(name, False, f"exit {result.returncode}: {detail}")
        return Check(name, True, detail)
    except subprocess.TimeoutExpired:
        return Check(name, False, f"probe timed out after {timeout:g}s")
    except OSError as exc:
        return Check(name, False, f"cannot execute: {exc}")


def command_version(name: str, args: list[str]) -> Check:
    path = shutil.which(name)
    return probe(name, [path, *args]) if path else Check(name, False, "not found in PATH")


def python_docx() -> Check:
    # Finding a module spec alone does not catch broken installs or import errors.
    return probe("python-docx", [sys.executable, "-c",
        "import docx; assert callable(docx.Document); print('python-docx import succeeded')"])


def plantuml_jar(path: str) -> Check:
    jar = Path(path).expanduser().resolve()
    if not jar.is_file():
        return Check("plantuml-jar", False, f"JAR not found: {jar}")
    java = shutil.which("java")
    if not java:
        return Check("plantuml-jar", False, "java not found in PATH")
    return probe("plantuml-jar", [java, "-jar", str(jar), "-version"])


def collect_checks(scopes: set[str], jar: str | None = None) -> list[Check]:
    checks = []
    if "diagrams" in scopes:
        checks.extend([
            command_version("plantuml", ["-version"]),
            command_version("mmdc", ["--version"]),
            command_version("java", ["-version"]),
            command_version("dot", ["-V"]),
        ])
        if jar:
            checks.append(plantuml_jar(jar))
    if "docx" in scopes:
        checks.extend([python_docx(), command_version("pandoc", ["--version"]),
                       command_version("soffice", ["--version"])])
    return checks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=["diagrams", "docx"], action="append",
                        help="Repeat to select capabilities; omitted means all")
    parser.add_argument("--plantuml-jar", default=os.environ.get("PLANTUML_JAR"),
                        help="Known local JAR path (or PLANTUML_JAR environment variable)")
    parser.add_argument("--json", action="store_true", help="Machine-readable probe results")
    args = parser.parse_args(argv)
    scopes = set(args.scope or ["diagrams", "docx"])
    checks = collect_checks(scopes, args.plantuml_jar)
    notes = ["Discovery/import checks only; actual rendering and conversion remain unverified.",
             "Agent-exposed document tools and CodeGraph/MCP must be inspected separately when relevant."]
    if "diagrams" in scopes:
        notes.extend([
            "UML/software architecture: PlantUML first (command or configured JAR); on failure try Mermaid.",
            "Flowcharts/trees/functional decomposition/general relationships: Mermaid first.",
            "If Mermaid cannot render locally, preserve .mmd and provide Windows mmdc commands; no ASCII replacement.",
            "Insert verified images before claiming a final illustrated Word document.",
        ])
    report = {"checks": [asdict(check) for check in checks], "notes": notes}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("Software Design Document - Local Capability Discovery")
        for check in checks:
            print(f"[{'OK' if check.available else '--'}] {check.name:<16} {check.detail}")
        for note in notes:
            print(f"- {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

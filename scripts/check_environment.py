#!/usr/bin/env python3
"""Lightweight capability check for software-design-doc-skill.

Only verifies that relevant commands/modules can be invoked. It intentionally
does not render test diagrams or create test artifacts.
"""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
from dataclasses import dataclass


@dataclass
class Check:
    name: str
    available: bool
    detail: str


def command_version(name: str, args: list[str]) -> Check:
    path = shutil.which(name)
    if not path:
        return Check(name, False, "not found in PATH")
    try:
        result = subprocess.run(
            [path, *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=5,
            check=False,
        )
        lines = (result.stdout or "").strip().splitlines()
        detail = lines[0] if lines else path
        if result.returncode == 0:
            return Check(name, True, detail)
        return Check(name, False, f"command returned {result.returncode}: {detail}")
    except Exception as exc:
        return Check(name, False, f"command check failed: {exc}")


def python_module(name: str, display: str | None = None) -> Check:
    available = importlib.util.find_spec(name) is not None
    return Check(
        display or name,
        available,
        "Python module available" if available else "Python module not installed",
    )


def main() -> int:
    checks = [
        command_version("claude", ["--version"]),
        command_version("plantuml", ["-version"]),
        command_version("mmdc", ["--version"]),
        command_version("java", ["-version"]),
        command_version("pandoc", ["--version"]),
        command_version("dot", ["-V"]),
        python_module("docx", "python-docx"),
    ]

    print("Software Design Document Skill - Capability Check")
    print("=" * 64)
    for check in checks:
        state = "OK" if check.available else "--"
        print(f"[{state:>2}] {check.name:<16} {check.detail}")

    print("\nDiagram fallback:")
    plantuml = next(c for c in checks if c.name == "plantuml")
    mermaid = next(c for c in checks if c.name == "mmdc")
    if plantuml.available:
        print("- PlantUML available: prefer PlantUML for HLD diagrams.")
    elif mermaid.available:
        print("- PlantUML unavailable; Mermaid renderer available: use Mermaid.")
    else:
        print("- No PlantUML/Mermaid renderer detected: use text/ASCII descriptions.")

    print("\nNotes:")
    print("- This is a lightweight command/module check; no test diagram is rendered.")
    print("- A PlantUML JAR installation may be usable through Java even if the plantuml command is absent.")
    print("- CodeGraph/MCP availability is agent-specific and must be checked from the current tool context when code exists.")
    print("- Missing optional tools must not block the core HLD workflow; use the documented fallback chain.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

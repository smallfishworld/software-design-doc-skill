#!/usr/bin/env python3
"""Check optional local tools used by software-design-doc-skill.

The skill itself does not require these tools. This script only reports which
optional integrations appear to be available in an offline/intranet machine.
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
        first_line = (result.stdout or "").strip().splitlines()
        detail = first_line[0] if first_line else path
        return Check(name, True, detail)
    except Exception as exc:  # environment check must never fail hard
        return Check(name, True, f"found at {path}; version check failed: {exc}")


def python_module(name: str, display: str | None = None) -> Check:
    available = importlib.util.find_spec(name) is not None
    return Check(display or name, available, "Python module available" if available else "Python module not installed")


def main() -> int:
    checks = [
        command_version("claude", ["--version"]),
        command_version("java", ["-version"]),
        command_version("pandoc", ["--version"]),
        command_version("dot", ["-V"]),
        python_module("docx", "python-docx"),
    ]

    print("Software Design Document Skill - Optional Environment Check")
    print("=" * 64)
    for check in checks:
        state = "OK" if check.available else "--"
        print(f"[{state:>2}] {check.name:<16} {check.detail}")

    print("\nNotes:")
    print("- Only Claude Code plus the skill files are needed for core use.")
    print("- Requirements-first design works without source code or CodeGraph.")
    print("- Java is useful when running a local PlantUML JAR.")
    print("- python-docx/Pandoc are optional ways to produce DOCX output.")
    print("- CodeGraph/MCP availability is configured separately and is not auto-detected here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Offline regression checks: python3 -m unittest discover -s tests -v."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_environment", ROOT / "scripts/check_environment.py")
env = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = env
spec.loader.exec_module(env)
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


class CapabilityTests(unittest.TestCase):
    def test_missing_command_does_not_spawn(self):
        with patch.object(env.shutil, "which", return_value=None), patch.object(env.subprocess, "run") as run:
            self.assertFalse(env.command_version("mmdc", ["--version"]).available)
            run.assert_not_called()

    def test_nonzero_is_unavailable(self):
        result = subprocess.CompletedProcess([], 2, "failed")
        with patch.object(env.subprocess, "run", return_value=result):
            self.assertFalse(env.probe("mmdc", ["mmdc"]).available)

    def test_timeout_is_unavailable(self):
        with patch.object(env.subprocess, "run", side_effect=subprocess.TimeoutExpired("mmdc", 5)):
            self.assertFalse(env.probe("mmdc", ["mmdc"]).available)

    def test_execution_error_is_unavailable(self):
        with patch.object(env.subprocess, "run", side_effect=PermissionError("denied")):
            self.assertFalse(env.probe("mmdc", ["mmdc"]).available)

    def test_success_and_stderr_version(self):
        result = subprocess.CompletedProcess([], 0, "java version 21\nmore output")
        with patch.object(env.subprocess, "run", return_value=result) as run:
            check = env.probe("java", ["java", "-version"])
            self.assertTrue(check.available)
            self.assertEqual(check.detail, "java version 21")
            self.assertEqual(run.call_args.kwargs["stderr"], subprocess.STDOUT)
            self.assertNotIn("shell", run.call_args.kwargs)

    def test_docx_only_scope_does_not_probe_diagrams(self):
        with patch.object(env, "command_version", side_effect=lambda n, a: env.Check(n, False, "missing")) as cmd, \
             patch.object(env, "python_docx", return_value=env.Check("python-docx", True, "ok")):
            checks = env.collect_checks({"docx"})
            self.assertEqual({c.name for c in checks}, {"python-docx", "pandoc", "soffice"})
            self.assertEqual([c.args[0] for c in cmd.call_args_list], ["pandoc", "soffice"])

    def test_configured_jar_path_with_spaces(self):
        with tempfile.TemporaryDirectory(prefix="skill test ") as tmp:
            jar = Path(tmp) / "plant uml.jar"
            jar.touch()
            with patch.object(env.shutil, "which", return_value="/bin/java"), \
                 patch.object(env, "probe", return_value=env.Check("plantuml-jar", True, "ok")) as probe:
                self.assertTrue(env.plantuml_jar(str(jar)).available)
                self.assertEqual(probe.call_args.args[1], ["/bin/java", "-jar", str(jar.resolve()), "-version"])

    def test_missing_jar(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(env.plantuml_jar(str(Path(tmp) / "missing.jar")).available)

    def test_import_error_is_not_module_availability(self):
        with patch.object(env.subprocess, "run", return_value=subprocess.CompletedProcess([], 1, "ImportError")):
            self.assertFalse(env.python_docx().available)

    def test_missing_optional_tools_are_json_data_not_fatal(self):
        buf = io.StringIO()
        with patch.object(env, "collect_checks", return_value=[env.Check("mmdc", False, "missing")]), \
             contextlib.redirect_stdout(buf):
            self.assertEqual(env.main(["--scope", "diagrams", "--json"]), 0)
        report = json.loads(buf.getvalue())
        self.assertFalse(report["checks"][0]["available"])


class PackageTests(unittest.TestCase):
    def test_docx_is_complete_crc_valid_and_xml_parseable(self):
        # Detects the original corrupt template even if it still starts with PK.
        with ZipFile(ROOT / "templates/default-software-design-template.docx") as z:
            self.assertIsNone(z.testzip())
            for name in ("[Content_Types].xml", "word/document.xml", "word/styles.xml", "word/settings.xml"):
                ET.fromstring(z.read(name))

    def test_template_has_editable_fields_and_expected_outline(self):
        with ZipFile(ROOT / "templates/default-software-design-template.docx") as z:
            doc = ET.fromstring(z.read("word/document.xml"))
            headings = []
            for p in doc.findall(".//w:body/w:p", NS):
                style = p.find("w:pPr/w:pStyle", NS)
                if style is not None and style.get(f'{{{NS["w"]}}}val') == "Heading1":
                    headings.append("".join(t.text or "" for t in p.findall(".//w:t", NS)))
            outline = (ROOT / "templates/default-outline.md").read_text()
            self.assertEqual([int(h.split()[0]) for h in headings],
                             [int(n) for n in re.findall(r"^# (\d+)\.", outline, re.M)])
            self.assertIn("TOC", "".join(t.text or "" for t in doc.findall(".//w:instrText", NS)))
            footers = [z.read(n).decode() for n in z.namelist() if re.fullmatch(r"word/footer\d+\.xml", n)]
            self.assertTrue(any(" PAGE " in f for f in footers))
            headers = [z.read(n).decode() for n in z.namelist() if re.fullmatch(r"word/header\d+\.xml", n)]
            self.assertTrue(any("{{PROJECT}}" in h for h in headers))

    def test_template_exposes_conditional_architecture_candidates(self):
        with ZipFile(ROOT / "templates/default-software-design-template.docx") as z:
            body = ET.fromstring(z.read("word/document.xml"))
            text = "".join(t.text or "" for t in body.findall(".//w:t", NS))
        for heading in (
            "多任务与并发设计（条件候选）",
            "状态行为设计（条件候选）",
            "性能、实时性与资源设计（条件候选）",
            "部署、升级与兼容性设计（条件候选）",
        ):
            self.assertIn(heading, text)

    def test_cover_metadata_table_is_narrow_and_centered(self):
        with ZipFile(ROOT / "templates/default-software-design-template.docx") as z:
            body = ET.fromstring(z.read("word/document.xml"))
        first_table = body.find(".//w:tbl", NS)
        self.assertIsNotNone(first_table)
        tbl_w = first_table.find("w:tblPr/w:tblW", NS)
        jc = first_table.find("w:tblPr/w:jc", NS)
        self.assertIsNotNone(tbl_w)
        self.assertIsNotNone(jc)
        self.assertLess(int(tbl_w.get(f'{{{NS["w"]}}}w')), 8000)
        self.assertEqual(jc.get(f'{{{NS["w"]}}}val'), "center")

    def test_table_cells_have_no_body_indent_and_grid_widths_match(self):
        with ZipFile(ROOT / "templates/default-software-design-template.docx") as z:
            body = ET.fromstring(z.read("word/document.xml"))
        w_width = f'{{{NS["w"]}}}w'
        w_first_line = f'{{{NS["w"]}}}firstLine'
        for ti, table in enumerate(body.findall(".//w:tbl", NS)):
            grid = [int(c.get(w_width)) for c in table.findall("w:tblGrid/w:gridCol", NS)]
            self.assertTrue(grid, f"table {ti} has no tblGrid")
            for ri, row in enumerate(table.findall("w:tr", NS)):
                cells = row.findall("w:tc", NS)
                widths = []
                for ci, cell in enumerate(cells):
                    tc_w = cell.find("w:tcPr/w:tcW", NS)
                    self.assertIsNotNone(tc_w, f"table {ti} row {ri} cell {ci} missing tcW")
                    widths.append(int(tc_w.get(w_width)))
                    for p in cell.findall("w:p", NS):
                        ind = p.find("w:pPr/w:ind", NS)
                        if ind is not None and ind.get(w_first_line) is not None:
                            self.assertEqual(ind.get(w_first_line), "0",
                                             f"table {ti} row {ri} cell {ci} inherited firstLine")
                self.assertEqual(grid, widths, f"table {ti} row {ri} tblGrid/tcW mismatch")
    def test_internal_markdown_links_resolve(self):
        for md in ROOT.rglob("*.md"):
            content = re.sub(r"```.*?```", "", md.read_text(), flags=re.S)
            for target in re.findall(r"\]\(([^)]+)\)", content):
                if "://" not in target and not target.startswith("#"):
                    self.assertTrue((md.parent / target.split("#")[0]).exists(), f"{md}: {target}")


if __name__ == "__main__":
    unittest.main()

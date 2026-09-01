#!/usr/bin/env python3

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_nvme_report.py"
BUILD_SCRIPT = ROOT / "scripts" / "build_nvme_reports.py"
EVIDENCE_SCRIPT = ROOT / "scripts" / "update_nvme_figure_evidence.py"
SPEC = importlib.util.spec_from_file_location("validate_nvme_report", SCRIPT)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class NvmeReportContractTest(unittest.TestCase):
    def test_generators_parse_and_import(self):
        for path in (BUILD_SCRIPT, EVIDENCE_SCRIPT):
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec")
            spec = importlib.util.spec_from_file_location(path.stem, path)
            self.assertIsNotNone(spec)
            self.assertIsNotNone(spec.loader)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

    def test_report_generation_is_deterministic(self):
        contract = json.loads(
            (ROOT / ".ai/nvme-report/output-contract.json").read_text(encoding="utf-8")
        )
        paths = [ROOT / item["path"] for item in contract["artifacts"]]
        paths.append(ROOT / ".ai/nvme-report/claims.json")
        before = {path: path.read_bytes() for path in paths}
        result = subprocess.run(
            [sys.executable, "-B", str(BUILD_SCRIPT)],
            cwd=ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        after = {path: path.read_bytes() for path in paths}
        self.assertEqual(before, after)

    def test_auto_runs_publish_when_outputs_are_ready(self):
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--phase", "auto"],
            cwd=ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("publish contract validated", result.stdout)

    def test_contract_has_five_reports_and_twenty_requested_artifacts(self):
        contract = json.loads(
            (ROOT / ".ai/nvme-report/output-contract.json").read_text(encoding="utf-8")
        )
        artifacts = contract["artifacts"]
        self.assertEqual(len(artifacts), 20)
        self.assertEqual(sum(item["format"] == "html" for item in artifacts), 10)
        self.assertEqual(sum(item["format"] == "markdown" for item in artifacts), 10)
        self.assertEqual(len({item["report_id"] for item in artifacts}), 5)
        self.assertEqual(
            {item.get("parity_group") for item in artifacts if item["format"] == "markdown"},
            {
                "base12-bilingual",
                "base3-bilingual",
                "base4-bilingual",
                "pcie14-bilingual",
                "basefwlog-bilingual",
            },
        )

    def test_source_registry_does_not_store_absolute_paths(self):
        registry = json.loads(
            (ROOT / ".ai/nvme-report/source-register.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(registry["sources"]), 3)
        for source in registry["sources"]:
            self.assertFalse(VALIDATOR.ABSOLUTE_PATH.match(source["filename"]))
            self.assertRegex(source["sha256"], r"^[0-9a-f]{64}$")

    def test_scope_and_figure_register_are_consistent(self):
        scope = json.loads(
            (ROOT / ".ai/nvme-report/scope.json").read_text(encoding="utf-8")
        )
        register = json.loads(
            (ROOT / ".ai/nvme-report/figure-table-register.json").read_text(
                encoding="utf-8"
            )
        )
        statuses = {item["id"]: item["status"] for item in scope["entries"]}
        base3_excluded = next(
            item for item in scope["entries"] if item["id"] == "BASE3-FABRIC-EXCLUDE"
        )
        self.assertIn("72", base3_excluded["figures"])
        for figure in register["entries"]:
            self.assertEqual(figure["scope_status"], statuses[figure["scope_entry_id"]])
            if figure["scope_status"] == "INCLUDE":
                self.assertTrue(figure["key_items"])
                self.assertRegex(figure["evidence_digest"], r"^[0-9a-f]{64}$")

        new_report = [
            item for item in register["entries"]
            if item["report_id"] == "base-admin-fw-logs" and item["scope_status"] == "INCLUDE"
        ]
        dependencies = [item for item in new_report if item.get("role") == "referenced_dependency"]
        expected_dependencies = {
            "93", "155", "337", "338", "347", "348", "474",
        }
        self.assertEqual(len(new_report), 22)
        self.assertEqual(len(dependencies), 7)
        self.assertEqual({item["number"] for item in dependencies}, expected_dependencies)
        self.assertEqual(sum(item.get("role") == "in_scope" for item in new_report), 15)
        self.assertTrue(all(item["type"] == "Figure" for item in new_report))
        self.assertTrue(all(item.get("referenced_from") for item in dependencies))
        self.assertTrue(all(item["mode"] == "dependency-slice" for item in dependencies))
        self.assertEqual(
            next(item for item in new_report if item["number"] == "209")["mode"],
            "scope-reduced",
        )
        self.assertNotIn("257", {item["number"] for item in new_report})
        self.assertNotIn("320", {item["number"] for item in new_report})
        report_scope = next(
            item for item in scope["reports"] if item["id"] == "base-admin-fw-logs"
        )
        self.assertEqual(
            {item["id"] for item in new_report},
            set(report_scope["included_figure_ids"]),
        )
        figure_209 = next(item for item in new_report if item["number"] == "209")
        self.assertEqual(
            figure_209["key_items"],
            [
                "LID 03h",
                "CSI = N",
                "Domain / NVM subsystem",
                "Firmware Slot Information",
                "§5.2.13.1.4",
                "MDS",
            ],
        )

    def test_firmware_report_is_tutorial_first_and_lid03_only(self):
        contract = json.loads(
            (ROOT / ".ai/nvme-report/output-contract.json").read_text(encoding="utf-8")
        )
        for artifact in contract["artifacts"]:
            if artifact["report_id"] != "base-admin-fw-logs":
                continue
            text = (ROOT / artifact["path"]).read_text(encoding="utf-8")
            for required in ("Mental Model", "End-to-End", "Debug", "LID 03h", "007F0003h"):
                self.assertIn(required, text)
            self.assertNotIn("Figure 逐圖導讀", text)
            self.assertNotIn("Figure-by-Figure Guide", text)
            for removed_topic in (
                "Persistent Event Log",
                "SMART / Health Information",
                "FDP Configurations",
                "Sanitize Status",
            ):
                self.assertNotIn(removed_topic, text)

    def test_markdown_language_and_site_layout_are_language_aware(self):
        contract = json.loads(
            (ROOT / ".ai/nvme-report/output-contract.json").read_text(encoding="utf-8")
        )
        expected_images = {
            "base12-zh-md": "posts/2026/dogMC_title.jpg",
            "base12-en-md": "posts/2026/cat_title.jpg",
            "base3-zh-md": "posts/2026/dogMC_title.jpg",
            "base3-en-md": "posts/2026/cat_title.jpg",
            "base4-zh-md": "posts/2026/dogMC_title.jpg",
            "base4-en-md": "posts/2026/cat_title.jpg",
            "pcie14-zh-md": "posts/2026/lion_title.jpg",
            "pcie14-en-md": "posts/2026/catFlower_title.jpg",
            "basefwlog-zh-md": "posts/2026/dogMC_title.jpg",
            "basefwlog-en-md": "posts/2026/cat_title.jpg",
        }
        for artifact in contract["artifacts"]:
            if artifact["format"] != "markdown":
                continue
            text = (ROOT / artifact["path"]).read_text(encoding="utf-8")
            self.assertRegex(
                text,
                rf"(?m)^lang:\s*{re.escape(artifact['language'])}\s*$",
            )
            self.assertRegex(
                text,
                rf"(?m)^img:\s*{re.escape(expected_images[artifact['id']])}\s*$",
            )
        layout = (ROOT / "_layouts/default.html").read_text(encoding="utf-8")
        self.assertIn("page.lang", layout)

    def test_github_actions_are_pinned_to_full_commit_shas(self):
        for workflow in (ROOT / ".github/workflows").glob("*.yml"):
            text = workflow.read_text(encoding="utf-8")
            for reference in re.findall(r"(?m)^\s*uses:\s*([^\s#]+)", text):
                self.assertRegex(reference, r"@(?:[0-9a-f]{40})$")

    def test_published_reports_have_no_excluded_terms_or_placeholders(self):
        contract = json.loads(
            (ROOT / ".ai/nvme-report/output-contract.json").read_text(encoding="utf-8")
        )
        for artifact in contract["artifacts"]:
            text = (ROOT / artifact["path"]).read_text(encoding="utf-8")
            self.assertIsNone(VALIDATOR.FORBIDDEN_PUBLISHED.search(text))
            for phrase in VALIDATOR.PLACEHOLDER_PHRASES:
                self.assertNotIn(phrase, text)

    def test_html_validator_rejects_css_javascript_and_external_resources(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.html"
            path.write_text(
                """<!doctype html><html lang="zh-Hant-TW"><head>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>body{color:red}</style><link rel="stylesheet" href="x.css">
                </head><body style="color:red"><script src="https://example.invalid/a.js"></script>
                <img src="https://example.invalid/a.png"></body></html>""",
                encoding="utf-8",
            )
            errors = VALIDATOR.validate_html(path)
            joined = "\n".join(errors)
            self.assertIn("禁止 <style>", joined)
            self.assertIn("禁止 <script>", joined)
            self.assertIn("禁止 stylesheet", joined)
            self.assertIn("禁止 style attribute", joined)
            self.assertIn("禁止外部資源", joined)
            self.assertIn("img 必須有 alt", joined)

    def test_publish_contract_passes_after_claims_and_outputs_are_built(self):
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--phase", "publish"],
            cwd=ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("publish contract validated", result.stdout)


if __name__ == "__main__":
    unittest.main()

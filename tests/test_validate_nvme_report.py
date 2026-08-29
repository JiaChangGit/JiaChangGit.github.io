#!/usr/bin/env python3

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_nvme_report.py"
SPEC = importlib.util.spec_from_file_location("validate_nvme_report", SCRIPT)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class NvmeReportContractTest(unittest.TestCase):
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

    def test_contract_has_four_reports_and_sixteen_requested_artifacts(self):
        contract = json.loads(
            (ROOT / ".ai/nvme-report/output-contract.json").read_text(encoding="utf-8")
        )
        artifacts = contract["artifacts"]
        self.assertEqual(len(artifacts), 16)
        self.assertEqual(sum(item["format"] == "html" for item in artifacts), 8)
        self.assertEqual(sum(item["format"] == "markdown" for item in artifacts), 8)
        self.assertEqual(len({item["report_id"] for item in artifacts}), 4)
        self.assertEqual(
            {item.get("parity_group") for item in artifacts if item["format"] == "markdown"},
            {"base12-bilingual", "base3-bilingual", "base4-bilingual", "pcie14-bilingual"},
        )

    def test_source_registry_does_not_store_absolute_paths(self):
        registry = json.loads(
            (ROOT / ".ai/nvme-report/source-register.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(registry["sources"]), 3)
        for source in registry["sources"]:
            self.assertFalse(VALIDATOR.ABSOLUTE_PATH.match(source["filename"]))
            self.assertRegex(source["sha256"], r"^[0-9a-f]{64}$")

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

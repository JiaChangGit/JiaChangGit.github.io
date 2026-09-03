#!/usr/bin/env python3

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
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
    def test_standalone_command_set_covers_all_figures_without_transport_leakage(self):
        from scripts.nvme_nvm_command_set import MODULES, REPORT_ID
        from scripts.nvme_report_questions import question_bank
        data = json.loads((ROOT / '.ai/nvme-report/figure-table-register.json').read_text())
        figures = [f for f in data['entries'] if f['report_id'] == REPORT_ID]
        primary = [f for f in figures if f['source_id'] == 'NVME-NVM-CS-1.3']
        self.assertEqual({int(f['number']) for f in primary}, set(range(1,203)))
        self.assertEqual(len(figures), 220)
        self.assertTrue(all(f['scope_status']=='INCLUDE' for f in figures))
        self.assertEqual(len(MODULES), 37)
        self.assertEqual(len(question_bank(REPORT_ID, MODULES)), 148)
        self.assertEqual({n for m in MODULES for n in m['figures']}, set(range(1,203)))
        for n in (1,13,15,16,17,189):
            self.assertEqual(next(f for f in primary if int(f['number'])==n)['mode'], 'scope-reduced')
        self.assertIsNone(VALIDATOR.forbidden_published('Reference Exported NVM Subsystem Template', REPORT_ID))
        self.assertIsNotNone(VALIDATOR.forbidden_published('Exported NVM Subsystem', 'base-boot-telemetry-sanitize'))
        for term in ('Fabrics', 'Discovery', 'NQN', 'message-based', 'command capsule'):
            self.assertIsNotNone(VALIDATOR.forbidden_published('Exported NVM Subsystem '+term, REPORT_ID))

    def test_published_crc_vectors_and_tag_packing_recompute(self):
        # Independent bitwise calculation verifies published numeric examples.
        # Polynomial is reflected for this least-significant-bit-first loop.
        def crc(data, width, polynomial):
            mask=(1<<width)-1
            reflected=int(f'{polynomial:0{width}b}'[::-1],2)
            value=mask
            for byte in data:
                value ^= byte
                for _ in range(8):
                    value=(value>>1) ^ (reflected if value&1 else 0)
            return value ^ mask
        self.assertEqual(crc(bytes(4096),32,0x1EDC6F41),0x98F94189)
        check=crc(b'123456789',64,0xAD93D23594C93659)
        self.assertEqual(check,0xAE8B14860A799888)
        self.assertEqual(int(f'{check:064b}'[::-1],2),0x11199E506128D175)
        self.assertEqual(crc(bytes(4096),64,0xAD93D23594C93659),0x6482D367EB22B64E)
        self.assertEqual(crc(bytes([255])*4096,64,0xAD93D23594C93659),0xC0DDBA7302ECA3AC)
        space=(0x12345<<30)|0x2A
        self.assertEqual(space>>32,0x48D1)
        self.assertEqual(space&0xFFFFFFFF,0x4000002A)

    def test_answered_question_banks_detect_missing_answer_and_bad_order(self):
        from scripts.build_nvme_reports import REPORT_MODULES
        from scripts.nvme_report_questions import question_bank, validate_questions
        claims = json.loads((ROOT / '.ai/nvme-report/claims.json').read_text())['claims']
        contract = json.loads((ROOT / '.ai/nvme-report/output-contract.json').read_text())
        for artifact in contract['artifacts']:
            rid = artifact['report_id']
            text = (ROOT / artifact['path']).read_text()
            lang = 'en' if artifact['language'] == 'en' else 'zh'
            bank = question_bank(rid, REPORT_MODULES[rid])
            with self.subTest(artifact=artifact['id']):
                self.assertGreaterEqual(len(bank), 16)
                self.assertFalse(validate_questions(rid, REPORT_MODULES[rid], claims, text, lang, artifact['format']))
        rid = 'base-boot-telemetry-sanitize'
        text = (ROOT / '_posts/2026-09-03-nvme-boot-telemetry-sanitize-en.md').read_text()
        bank = question_bank(rid, REPORT_MODULES[rid])
        broken = text.rsplit(bank[0]['answer']['en'], 1)
        self.assertEqual(len(broken), 2)
        self.assertTrue(validate_questions(rid, REPORT_MODULES[rid], claims, ''.join(broken), 'en', 'markdown'))
        wrong_id = text.replace('<!-- qa:' + bank[0]['id'] + ' -->', '<!-- qa:wrong-source -->')
        self.assertTrue(validate_questions(rid, REPORT_MODULES[rid], claims, wrong_id, 'en', 'markdown'))

    def test_boot_telemetry_sanitize_scope_and_source_identity(self):
        from scripts.nvme_bts_terms import definition
        from scripts.nvme_teaching_content import term_definition
        scope = json.loads((ROOT / '.ai/nvme-report/scope.json').read_text())
        register = json.loads((ROOT / '.ai/nvme-report/figure-table-register.json').read_text())
        figures = [f for f in register['entries'] if f['report_id'] == 'base-boot-telemetry-sanitize']
        self.assertEqual(len(figures), 80)
        self.assertEqual(sum(f.get('role') != 'referenced_dependency' for f in figures), 32)
        self.assertEqual({f['id'] for f in figures if f['number'] == '201'}, {'BASEBTS-BASE-FIG-201', 'BASEBTS-NVMCS-FIG-201'})
        claims = json.loads((ROOT / '.ai/nvme-report/claims.json').read_text())['claims']
        by_id = {c['id']:c for c in claims}
        self.assertEqual(by_id['BASEBTS-BASE-FIG-201-CLAIM']['source_id'], 'NVME-BASE-2.4')
        self.assertEqual(by_id['BASEBTS-NVMCS-FIG-201-CLAIM']['source_id'], 'NVME-NVM-CS-1.3')
        self.assertIn('8.1.27.4.6', by_id['BASEBTS-SAN-VERIFY-STATE']['section'])
        self.assertTrue(any(e['status'] == 'EXCLUDE' and '8.1.27.6' in str(e) for e in scope['entries']))
        self.assertIn('Storage Tag Check', definition('STC', 'base-boot-telemetry-sanitize', 'en', term_definition))
        self.assertIn('Self-test Code', definition('STC', 'base-self-test-hmb-emulation', 'en', term_definition))
        text = (ROOT / 'DOCS/nvme-spec-report/base-boot-telemetry-sanitize/tutorial-zh-tw.html').read_text()
        ids = re.findall(r'(?<![-\w])id="([^"]+)"', text)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn('29:10', text)

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

    def test_contract_has_ten_reports_and_forty_requested_artifacts(self):
        contract = json.loads(
            (ROOT / ".ai/nvme-report/output-contract.json").read_text(encoding="utf-8")
        )
        artifacts = contract["artifacts"]
        self.assertEqual(len(artifacts), 40)
        self.assertEqual(sum(item["format"] == "html" for item in artifacts), 20)
        self.assertEqual(sum(item["format"] == "markdown" for item in artifacts), 20)
        self.assertEqual(len({item["report_id"] for item in artifacts}), 10)
        self.assertEqual(
            {item.get("parity_group") for item in artifacts if item["format"] == "markdown"},
            {
                "base12-bilingual",
                "base3-bilingual",
                "base4-bilingual",
                "pcie14-bilingual",
                "basefwlog-bilingual",
                "basepower-bilingual",
                "basediagmem-bilingual",
                "basensmgmt-bilingual",
                "basebts-bilingual",
                "nvmcs13-bilingual",
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

        power_report = [
            item for item in register["entries"]
            if item["report_id"] == "base-power-features" and item["scope_status"] == "INCLUDE"
        ]
        power_dependencies = [
            item for item in power_report if item.get("role") == "referenced_dependency"
        ]
        expected_power_numbers = {
            "93", "197", "198", "199", "200", "201", "202", "213", "338", "340",
            "463", "464", "465", "466", "468", "470", "474", "475", "476", "477",
            "478", "482", "483", "738", "739", "740", "741",
        }
        self.assertEqual(len(power_report), 27)
        self.assertEqual({item["number"] for item in power_report}, expected_power_numbers)
        self.assertEqual(
            {item["number"] for item in power_dependencies},
            {"93", "213", "338", "340", "474"},
        )
        self.assertTrue(all(item.get("referenced_from") for item in power_dependencies))
        self.assertEqual(
            next(item for item in power_report if item["number"] == "468")["key_items"],
            ["WH", "PS"],
        )
        power_scope = next(
            item for item in scope["reports"] if item["id"] == "base-power-features"
        )
        self.assertEqual(
            {item["id"] for item in power_report},
            set(power_scope["included_figure_ids"]),
        )

        diagmem_report = [
            item for item in register["entries"]
            if item["report_id"] == "base-self-test-hmb-emulation"
            and item["scope_status"] == "INCLUDE"
        ]
        diagmem_dependencies = [
            item for item in diagmem_report if item.get("role") == "referenced_dependency"
        ]
        expected_diagmem_numbers = {
            "36", "93", "94", "111", "176", "177", "178", "179", "180",
            "197", "198", "200", "203", "204", "205", "206", "207", "208",
            "209", "218", "219", "338", "463", "464", "466", "545", "546",
            "547", "548", "549", "550", "551", "552", "553", "700", "701",
        }
        expected_diagmem_dependencies = {
            "36", "93", "94", "197", "198", "200", "203", "204", "205",
            "206", "207", "208", "209", "338", "463", "464", "466",
        }
        self.assertEqual(len(diagmem_report), 36)
        self.assertEqual({item["number"] for item in diagmem_report}, expected_diagmem_numbers)
        self.assertEqual(
            {item["number"] for item in diagmem_dependencies},
            expected_diagmem_dependencies,
        )
        self.assertEqual(
            next(item for item in diagmem_report if item["number"] == "111")["source_id"],
            "NVME-NVM-CS-1.3",
        )
        for number in ("200", "209", "338", "466"):
            item = next(item for item in diagmem_report if item["number"] == number)
            self.assertEqual(item["mode"], "dependency-slice")
            self.assertTrue(item["scope_reduced"])
        diagmem_scope = next(
            item for item in scope["reports"]
            if item["id"] == "base-self-test-hmb-emulation"
        )
        self.assertEqual(
            {item["id"] for item in diagmem_report},
            set(diagmem_scope["included_figure_ids"]),
        )

        nsmgmt_report = [
            item for item in register["entries"]
            if item["report_id"] == "base-self-test-namespace-management"
            and item["scope_status"] == "INCLUDE"
        ]
        nsmgmt_dependencies = [
            item for item in nsmgmt_report if item.get("role") == "referenced_dependency"
        ]
        expected_nsmgmt_numbers = {
            "36", "93", "111", "123", "127", "132", "133", "134", "139",
            "155", "176", "177", "178", "179", "180", "203", "204", "205",
            "206", "207", "208", "209", "218", "219", "304", "338", "346",
            "442", "443", "444", "445", "446", "447", "448", "449", "450",
            "474", "700", "701",
        }
        expected_nsmgmt_dependencies = {
            "36", "93", "123", "127", "132", "133", "139", "155", "203",
            "204", "205", "206", "207", "208", "209", "304", "338", "346",
            "474",
        }
        self.assertEqual(len(nsmgmt_report), 39)
        self.assertEqual({item["number"] for item in nsmgmt_report}, expected_nsmgmt_numbers)
        self.assertEqual(
            {item["number"] for item in nsmgmt_dependencies},
            expected_nsmgmt_dependencies,
        )
        for number in ("36", "155", "209", "338", "346", "474", "123", "127", "132", "133"):
            item = next(item for item in nsmgmt_report if item["number"] == number)
            self.assertEqual(item["mode"], "dependency-slice")
            self.assertTrue(item["scope_reduced"])
        nsmgmt_scope = next(
            item for item in scope["reports"]
            if item["id"] == "base-self-test-namespace-management"
        )
        self.assertEqual(
            {item["id"] for item in nsmgmt_report},
            set(nsmgmt_scope["included_figure_ids"]),
        )

    def test_selftest_hmb_report_has_exact_scope_and_numeric_teaching(self):
        contract = json.loads(
            (ROOT / ".ai/nvme-report/output-contract.json").read_text(encoding="utf-8")
        )
        texts = []
        for artifact in contract["artifacts"]:
            if artifact["report_id"] != "base-self-test-hmb-emulation":
                continue
            text = (ROOT / artifact["path"]).read_text(encoding="utf-8")
            texts.append(text)
            for required in (
                "Mental Model", "Debug", "LID 06h", "008C0006h", "HMDL",
                "HMDLEC", "HMNARE", "DSTRD", "NDT", "00000012_34567000h",
                "NVM Express NVM Command Set Specification, Revision 1.3",
            ):
                self.assertIn(required.lower(), text.lower())
            for excluded in (
                "§4.1.4.4", "Figure 112", "§5.2.30.3", "§8.1.30",
            ):
                self.assertNotIn(excluded, text)
        self.assertEqual(len(texts), 4)
        self.assertNotEqual(texts[0], texts[1])
        self.assertEqual(
            VALIDATOR.claim_id_sequence(texts[2]),
            VALIDATOR.claim_id_sequence(texts[3]),
        )

    def test_selftest_namespace_report_has_exact_scope_and_numeric_teaching(self):
        contract = json.loads(
            (ROOT / ".ai/nvme-report/output-contract.json").read_text(encoding="utf-8")
        )
        texts = []
        for artifact in contract["artifacts"]:
            if artifact["report_id"] != "base-self-test-namespace-management":
                continue
            text = (ROOT / artifact["path"]).read_text(encoding="utf-8")
            texts.append(text)
            for required in (
                "Mental Model", "Debug", "LID 06h", "008C0006h", "NSZE", "NCAP",
                "NUSE", "THINP", "NVMSETID", "ENDGID", "Controller List", "DNCS",
                "NVM Express NVM Command Set Specification, Revision 1.3",
            ):
                self.assertIn(required.lower(), text.lower())
        self.assertEqual(len(texts), 4)
        self.assertNotEqual(texts[0], texts[1])
        self.assertEqual(
            VALIDATOR.claim_id_sequence(texts[2]),
            VALIDATOR.claim_id_sequence(texts[3]),
        )

    def test_power_feature_report_honors_exact_scope_and_has_numeric_teaching(self):
        contract = json.loads(
            (ROOT / ".ai/nvme-report/output-contract.json").read_text(encoding="utf-8")
        )
        texts = []
        for artifact in contract["artifacts"]:
            if artifact["report_id"] != "base-power-features":
                continue
            text = (ROOT / artifact["path"]).read_text(encoding="utf-8")
            texts.append(text)
            for required in (
                "Mental Model", "Debug", "FID 02h", "FID 04h", "FID 0Ch",
                "FID 10h", "FID 11h", "07D00018h", "01400157h", "01570161h",
            ):
                self.assertIn(required.lower(), text.lower())
            for excluded in (
                "§5.2.30.1.2.1", "§8.1.19.6", "§8.1.19.7",
                "Figure 469", "Figure 742", "Figure 743", "Figure 744",
            ):
                self.assertNotIn(excluded, text)
        self.assertEqual(len(texts), 4)
        self.assertNotEqual(texts[0], texts[1])
        self.assertEqual(
            VALIDATOR.claim_id_sequence(texts[2]),
            VALIDATOR.claim_id_sequence(texts[3]),
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

    def test_four_firmware_editions_have_distinct_delivery_shapes(self):
        tutorial = (
            ROOT / "DOCS/nvme-spec-report/base-admin-fw-logs/tutorial-zh-tw.html"
        ).read_text(encoding="utf-8")
        reference = (
            ROOT / "DOCS/nvme-spec-report/base-admin-fw-logs/detailed-spec-zh-tw.html"
        ).read_text(encoding="utf-8")
        zh_ppt = (
            ROOT / "_posts/2026-08-31-nvme-base-firmware-log-admin-zh-tw.md"
        ).read_text(encoding="utf-8")
        en_ppt = (
            ROOT / "_posts/2026-08-31-nvme-base-firmware-log-admin-en.md"
        ).read_text(encoding="utf-8")

        self.assertIn("新手教學版｜iPad／Desktop", tutorial)
        self.assertIn("先把縮寫變成人話", tutorial)
        self.assertIn("四種 firmware 狀態", tutorial)
        self.assertEqual(len(VALIDATOR.figure_table_ids(tutorial)), 22)

        self.assertIn("快速查詢詳細手冊｜iPad／Desktop", reference)
        self.assertIn("Command-specific status（SCT=1h）", reference)
        self.assertIn("完整 Figure evidence appendix", reference)
        self.assertEqual(len(VALIDATOR.figure_table_ids(reference)), 22)
        self.assertNotEqual(tutorial, reference)

        zh_slides = re.findall(r"(?m)^## Slide (\d{2})", zh_ppt)
        en_slides = re.findall(r"(?m)^## Slide (\d{2})", en_ppt)
        self.assertEqual(zh_slides, [f"{number:02d}" for number in range(1, 13)])
        self.assertEqual(zh_slides, en_slides)
        self.assertEqual(
            VALIDATOR.claim_id_sequence(zh_ppt),
            VALIDATOR.claim_id_sequence(en_ppt),
        )

    def test_all_html_share_responsive_visual_language(self):
        contract = json.loads(
            (ROOT / ".ai/nvme-report/output-contract.json").read_text(encoding="utf-8")
        )
        html_artifacts = [item for item in contract["artifacts"] if item["format"] == "html"]
        self.assertEqual(len(html_artifacts), 20)
        for artifact in html_artifacts:
            text = (ROOT / artifact["path"]).read_text(encoding="utf-8")
            with self.subTest(artifact=artifact["id"]):
                self.assertIn('<meta name="color-scheme" content="light dark">', text)
                self.assertIn('@media (min-width: 1200px)', text)
                self.assertIn('class="visual-legend"', text)
                for role in ("command", "object", "decision", "success", "failure"):
                    self.assertIn(f'class="legend-swatch role-{role}"', text)
                self.assertRegex(text, r'<body class="edition-(?:tutorial|reference)">')
                self.assertIn('data-visual-kind="', text)
                if artifact["id"].endswith("tutorial-html"):
                    self.assertIn("箭頭只表示", text)
                else:
                    self.assertIn("詳細版查詢重畫", text)

    def test_light_and_dark_semantic_palettes_meet_text_contrast(self):
        source = BUILD_SCRIPT.read_text(encoding="utf-8")
        root_blocks = re.findall(r":root\s*\{(.*?)\}", source, re.DOTALL)
        palettes = []
        for block in root_blocks:
            values = dict(re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]{6})", block))
            if values:
                palettes.append(values)
        self.assertGreaterEqual(len(palettes), 2)

        def luminance(color: str) -> float:
            channels = [int(color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
            linear = [
                value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
                for value in channels
            ]
            return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

        for palette_name, palette in zip(("light", "dark"), palettes[:2]):
            for role in ("spec", "explain", "infer", "example", "warn"):
                foreground = luminance(palette[role])
                background = luminance(palette[f"{role}-soft"])
                ratio = (max(foreground, background) + 0.05) / (
                    min(foreground, background) + 0.05
                )
                with self.subTest(palette=palette_name, role=role):
                    self.assertGreaterEqual(ratio, 4.5)

    def test_tutorial_and_reference_html_have_distinct_information_architectures(self):
        contract = json.loads(
            (ROOT / ".ai/nvme-report/output-contract.json").read_text(encoding="utf-8")
        )
        by_report: dict[str, dict[str, str]] = {}
        for artifact in contract["artifacts"]:
            if artifact["format"] != "html":
                continue
            by_report.setdefault(artifact["report_id"], {})[artifact["purpose"]] = (
                ROOT / artifact["path"]
            ).read_text(encoding="utf-8")
        for report_id, editions in by_report.items():
            tutorial = next(value for key, value in editions.items() if "新手教學" in key)
            reference = next(value for key, value in editions.items() if "快速查詢" in key)
            with self.subTest(report=report_id):
                self.assertIn('class="edition-tutorial"', tutorial)
                self.assertIn('class="edition-reference"', reference)
                self.assertNotEqual(tutorial, reference)
                self.assertIn("常見誤解", tutorial)
                self.assertTrue("快速查詢" in reference or "Reference" in reference)

    def test_markdown_language_and_site_layout_are_language_aware(self):
        contract = json.loads(
            (ROOT / ".ai/nvme-report/output-contract.json").read_text(encoding="utf-8")
        )
        expected_images = {
            "basebts-zh-md": "posts/2026/dogMC_title.jpg",
            "nvmcs13-zh-md": "posts/2026/dogMC_title.jpg",
            "nvmcs13-en-md": "posts/2026/cat_title.jpg",
            "basebts-en-md": "posts/2026/cat_title.jpg",
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
            "basepower-zh-md": "posts/2026/dogMC_title.jpg",
            "basepower-en-md": "posts/2026/cat_title.jpg",
            "basediagmem-zh-md": "posts/2026/dogMC_title.jpg",
            "basediagmem-en-md": "posts/2026/cat_title.jpg",
            "basensmgmt-zh-md": "posts/2026/dogMC_title.jpg",
            "basensmgmt-en-md": "posts/2026/cat_title.jpg",
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
            self.assertIsNone(VALIDATOR.forbidden_published(text, artifact['report_id']))
            for phrase in VALIDATOR.PLACEHOLDER_PHRASES:
                self.assertNotIn(phrase, text)

    def test_html_validator_allows_one_inline_stylesheet_but_rejects_active_or_external_content(self):
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
            self.assertIn("禁止 <script>", joined)
            self.assertIn("禁止 stylesheet", joined)
            self.assertIn("禁止 style attribute", joined)
            self.assertIn("禁止外部資源", joined)
            self.assertIn("img 必須有 alt", joined)

    def test_ipad_html_uses_native_touch_and_visual_features(self):
        contract = json.loads(
            (ROOT / ".ai/nvme-report/output-contract.json").read_text(encoding="utf-8")
        )
        policy = contract["html_policy"]
        self.assertEqual(policy["target_device"], "M1 iPad Pro and desktop browsers")
        self.assertEqual(
            policy["representative_viewports"],
            ["834x1194", "1194x834", "1440x1000"],
        )
        self.assertEqual(policy["safe_interaction_baseline"], "Safari 17.2")
        self.assertFalse(policy["javascript_allowed"])
        self.assertEqual(policy["minimum_touch_target_css_px"], 44)
        profile = (ROOT / ".ai/nvme-report/ipad-html-profile.md").read_text(encoding="utf-8")
        for source in ("support.apple.com", "developer.apple.com", "webkit.org"):
            self.assertIn(source, profile)

        figures = json.loads(
            (ROOT / ".ai/nvme-report/figure-table-register.json").read_text(encoding="utf-8")
        )["entries"]
        for artifact in contract["artifacts"]:
            if artifact["format"] != "html":
                continue
            text = (ROOT / artifact["path"]).read_text(encoding="utf-8")
            expected = sum(
                artifact["id"] in item.get("required_artifact_ids", [])
                for item in figures
                if item.get("report_id") == artifact["report_id"]
            )
            self.assertIn("viewport-fit=cover", text)
            self.assertGreaterEqual(text.count('name="theme-color"'), 2)
            self.assertIn('class="skip-link"', text)
            self.assertIn('class="ipad-read-guide"', text)
            self.assertIn('class="visual-atlas"', text)
            self.assertIn("prefers-reduced-motion: reduce", text)
            self.assertIn("safe-area-inset-top", text)
            self.assertNotIn("<script", text.lower())
            self.assertGreaterEqual(text.count('name="figures-'), expected)
            if artifact["id"].endswith("tutorial-html"):
                self.assertGreaterEqual(text.count("新手教學重畫（非 Spec 原圖）"), expected)
            else:
                self.assertGreaterEqual(text.count("詳細版查詢重畫"), expected)
                self.assertGreaterEqual(
                    text.count("Input／Decode／Validate／Evidence"), expected
                )

    def test_every_edition_has_deep_teaching_content_and_semantic_color(self):
        contract = json.loads(
            (ROOT / ".ai/nvme-report/output-contract.json").read_text(encoding="utf-8")
        )
        baseline = {
            "base12-tutorial-html": 15434, "base12-detailed-html": 17617,
            "base12-zh-md": 18505, "base12-en-md": 27877,
            "base3-tutorial-html": 46712, "base3-detailed-html": 54832,
            "base3-zh-md": 57130, "base3-en-md": 83874,
            "base4-tutorial-html": 31753, "base4-detailed-html": 37484,
            "base4-zh-md": 39217, "base4-en-md": 59885,
            "pcie14-tutorial-html": 62844, "pcie14-detailed-html": 73666,
            "pcie14-zh-md": 76574, "pcie14-en-md": 110423,
            "basefwlog-tutorial-html": 14224, "basefwlog-detailed-html": 26828,
            "basefwlog-zh-md": 13377, "basefwlog-en-md": 17261,
            "basepower-tutorial-html": 45000, "basepower-detailed-html": 50000,
            "basepower-zh-md": 50000, "basepower-en-md": 70000,
            "basediagmem-tutorial-html": 50000, "basediagmem-detailed-html": 55000,
            "basediagmem-zh-md": 60000, "basediagmem-en-md": 65000,
            "basensmgmt-tutorial-html": 70000, "basensmgmt-detailed-html": 70000,
            "basensmgmt-zh-md": 80000, "basensmgmt-en-md": 130000,
        }

        class VisibleText(HTMLParser):
            def __init__(self):
                super().__init__()
                self.parts = []
                self.hidden = 0

            def handle_starttag(self, tag, attrs):
                if tag in {"style", "script"}:
                    self.hidden += 1

            def handle_endtag(self, tag):
                if tag in {"style", "script"} and self.hidden:
                    self.hidden -= 1

            def handle_data(self, data):
                if not self.hidden:
                    self.parts.append(data)

        for artifact in contract["artifacts"]:
            text = (ROOT / artifact["path"]).read_text(encoding="utf-8")
            if artifact["format"] == "html":
                parser = VisibleText()
                parser.feed(text)
                visible = " ".join(parser.parts)
                self.assertIn("prefers-color-scheme: dark", text)
                for token in ("--spec:", "--explain:", "--infer:", "--example:", "--warn:"):
                    self.assertIn(token, text)
                if artifact["report_id"] == "base-admin-fw-logs":
                    term_heading = "先把縮寫變成人話" if artifact["id"].endswith("tutorial-html") else "縮寫與能力欄位"
                    self.assertLess(text.index(term_heading), text.index("Appendix A"))
                else:
                    self.assertLess(text.index("Glossary"), text.index("Figure／欄位表教學"))
            else:
                visible = text
                self.assertIn("glossary", text.lower())
                self.assertIn("Debug", text)
            if artifact["report_id"] in {"base-boot-telemetry-sanitize", "nvm-command-set-1.3"}:
                # New report: coverage is checked directly, without a historical length baseline.
                continue
            self.assertGreaterEqual(
                len(visible),
                baseline[artifact["id"]] * 2,
                f"{artifact['id']} visible content did not at least double",
            )

    def test_generic_bilingual_ppt_sources_share_module_and_figure_structure(self):
        pairs = [
            ("_posts/2026-08-28-nvme-base-ch1-2-zh-tw.md", "_posts/2026-08-28-nvme-base-ch1-2-en.md"),
            ("_posts/2026-08-28-nvme-base-ch3-zh-tw.md", "_posts/2026-08-28-nvme-base-ch3-en.md"),
            ("_posts/2026-08-28-nvme-base-ch4-zh-tw.md", "_posts/2026-08-28-nvme-base-ch4-en.md"),
            ("_posts/2026-08-28-nvme-pcie-transport-1-4-zh-tw.md", "_posts/2026-08-28-nvme-pcie-transport-1-4-en.md"),
            ("_posts/2026-09-02-nvme-base-power-thermal-features-zh-tw.md", "_posts/2026-09-02-nvme-base-power-thermal-features-en.md"),
            ("_posts/2026-09-02-nvme-base-self-test-hmb-emulation-zh-tw.md", "_posts/2026-09-02-nvme-base-self-test-hmb-emulation-en.md"),
            ("_posts/2026-09-02-nvme-base-self-test-namespace-management-zh-tw.md", "_posts/2026-09-02-nvme-base-self-test-namespace-management-en.md"),
        ]
        for zh_path, en_path in pairs:
            zh = (ROOT / zh_path).read_text(encoding="utf-8")
            en = (ROOT / en_path).read_text(encoding="utf-8")
            self.assertEqual(
                re.findall(r"(?m)^### Module (\d{2}):", zh),
                re.findall(r"(?m)^### Module (\d{2}):", en),
            )
            self.assertEqual(
                re.findall(r"figure-table:([A-Z0-9-]+)", zh),
                re.findall(r"figure-table:([A-Z0-9-]+)", en),
            )

    def test_post_excerpt_is_plain_text_before_truncation(self):
        layout = (ROOT / "_layouts/post.html").read_text(encoding="utf-8")
        excerpt_line = next(
            line for line in layout.splitlines() if "page.content | markdownify" in line
        )
        self.assertLess(excerpt_line.index("strip_html"), excerpt_line.index("truncatewords"))
        self.assertIn("normalize_whitespace", excerpt_line)
        self.assertTrue(excerpt_line.index("escape") > excerpt_line.index("truncatewords"))

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

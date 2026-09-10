#!/usr/bin/env python3

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from unittest import mock
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
    def test_inactive_term_is_not_corrupted_by_active_replacement(self):
        from scripts.nvme_plain_language import chinese
        self.assertEqual(chinese('inactive NSID'), 'inactive NSID')
        self.assertNotIn('in目前', chinese('invalid 與 inactive NSID；active NSID'))
        self.assertIn('目前可存取',chinese('active NSID'))

    def test_apst_example_recomputes_time_and_state_bits(self):
        encoded=(2000 << 8) | (3 << 3)
        self.assertEqual((encoded >> 8) & 0xffffff, 2000)
        self.assertEqual((encoded >> 3) & 31, 3)
        from scripts.nvme_figure_examples_base import LESSONS
        self.assertIn(f'{encoded:08X}h',LESSONS[477]['example'])
        text=(ROOT/'DOCS/nvme-spec-report/base-power-features/tutorial-zh-tw.html').read_text()
        self.assertIn(f'{encoded:08X}h',text)
        self.assertNotIn('07D00018h',text)

    def test_every_in_scope_figure_has_a_unique_takeaway_and_example(self):
        entries=VALIDATOR.load_json('figure-table-register.json')['entries']
        for a in VALIDATOR.load_json('output-contract.json')['artifacts']:
            if a['format']!='html': continue
            figures=[f for f in entries if a['id'] in f['required_artifact_ids']]
            text=(ROOT/a['path']).read_text()
            self.assertFalse(VALIDATOR.validate_figure_teaching(text,figures),a['id'])
        a=next(a for a in VALIDATOR.load_json('output-contract.json')['artifacts'] if a['report_id']=='base-namespace-management' and a['format']=='html')
        figures=[f for f in entries if a['id'] in f['required_artifact_ids']]
        text=(ROOT/a['path']).read_text()
        from scripts.nvme_figure_lessons import lesson
        f=next(f for f in figures if f['number']=='447')
        broken=text.replace(lesson(f)['example'],'')
        self.assertTrue(VALIDATOR.validate_figure_teaching(broken,figures))

    def test_reader_terms_are_bounded_and_paragraphs_are_numbered(self):
        contract = json.loads(
            (ROOT / ".ai/nvme-report/output-contract.json").read_text(encoding="utf-8")
        )
        for artifact in contract["artifacts"]:
            text = (ROOT / artifact["path"]).read_text(encoding="utf-8")
            labels = []
            for raw in re.findall(r"<dt>(.*?)</dt>", text, flags=re.S):
                label = re.sub(r"<[^>]+>", "", raw)
                labels.append(re.sub(r"\s+", " ", label).strip().casefold())
            self.assertTrue(labels, artifact["id"])
            self.assertTrue(
                all(count <= 2 for count in Counter(labels).values()),
                artifact["id"],
            )
            numbers = [
                tuple(int(part) for part in value.split("."))
                for value in re.findall(
                    r'class="paragraph-number"[^>]*>(\d+\.\d+)\.</span>', text
                )
            ]
            self.assertTrue(numbers, artifact["id"])
            by_section = {}
            section_order = []
            for section, paragraph in numbers:
                if section not in by_section:
                    by_section[section] = []
                    section_order.append(section)
                by_section[section].append(paragraph)
            self.assertEqual(
                section_order,
                sorted(section_order),
                artifact["id"],
            )
            for section, paragraphs in by_section.items():
                self.assertEqual(
                    paragraphs,
                    list(range(1, len(paragraphs) + 1)),
                    f"{artifact['id']} section {section:02d}",
                )
            axis_labels = [
                tuple(int(part) for part in value.split("-"))
                for value in re.findall(
                    r'class="axis-paragraph-number"[^>]*>(\d{2}-\d{2})</span>', text
                )
            ]
            self.assertTrue(axis_labels, artifact["id"])
            by_axis = {}
            axis_order = []
            for axis, paragraph in axis_labels:
                if axis not in by_axis:
                    by_axis[axis] = []
                    axis_order.append(axis)
                by_axis[axis].append(paragraph)
            self.assertEqual(axis_order, sorted(axis_order), artifact["id"])
            for axis, paragraphs in by_axis.items():
                self.assertEqual(
                    paragraphs,
                    list(range(1, len(paragraphs) + 1)),
                    f"{artifact['id']} axis {axis:02d}",
                )

    def test_standalone_command_set_preserves_registered_source_coverage(self):
        from scripts.nvme_nvm_command_set import MODULES, REPORT_ID
        from scripts.nvme_report_questions import question_bank
        data = json.loads((ROOT / '.ai/nvme-report/figure-table-register.json').read_text())
        figures = [f for f in data['entries'] if f['report_id'] == REPORT_ID]
        primary = [f for f in figures if f['source_id'] == 'NVME-NVM-CS-1.3']
        self.assertEqual({int(f['number']) for f in primary}, set(range(1,203)))
        self.assertEqual(len(figures), 220)
        self.assertTrue(all(f['scope_status']=='INCLUDE' for f in figures))
        self.assertEqual(len(MODULES), 37)
        self.assertTrue(question_bank(REPORT_ID, MODULES))
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
                self.assertTrue(bank)
                self.assertFalse(validate_questions(rid, REPORT_MODULES[rid], claims, text, lang, artifact['format']))
        rid = 'base-telemetry'
        text = (ROOT / '_posts/2026-09-11-nvme-base-telemetry-en.md').read_text()
        bank = question_bank(rid, REPORT_MODULES[rid])
        broken = text.rsplit(bank[0]['answer']['en'], 1)
        self.assertEqual(len(broken), 2)
        self.assertTrue(validate_questions(rid, REPORT_MODULES[rid], claims, ''.join(broken), 'en', 'markdown'))
        wrong_id = text.replace('<!-- qa:' + bank[0]['id'] + ' -->', '<!-- qa:wrong-source -->')
        self.assertTrue(validate_questions(rid, REPORT_MODULES[rid], claims, wrong_id, 'en', 'markdown'))

    def test_split_reports_preserve_source_identity_and_boundaries(self):
        from scripts.build_nvme_reports import REPORTS
        from scripts.nvme_bts_terms import definition
        from scripts.nvme_teaching_content import term_definition
        scope=VALIDATOR.load_json('scope.json')
        register=VALIDATOR.load_json('figure-table-register.json')['entries']
        self.assertNotIn('base-boot-telemetry-sanitize',REPORTS)
        self.assertNotIn('base-self-test-namespace-management',REPORTS)
        self.assertNotIn('base-self-test-hmb-emulation',REPORTS)
        for rid,prefix in [('base-boot-partitions','BOOT-'),('base-telemetry','TEL-')]:
            self.assertTrue(all(c['key'].startswith(prefix) for c in REPORTS[rid]['claims']))
        for rid in ('base-hmb-emulation','base-namespace-management'):
            self.assertFalse(any(c['key'].startswith('SELFTEST-') for c in REPORTS[rid]['claims']))
        self.assertTrue(any(e['status']=='EXCLUDE' and '8.1.27.6' in str(e) for e in scope['entries']))
        self.assertIn('Storage Tag Check',definition('STC','base-sanitize','en',term_definition))
        self.assertIn('Self-test Code',definition('STC','base-device-self-test','en',term_definition))
        identities=[(f['report_id'],f['source_id'],f['number']) for f in register]
        self.assertEqual(len(identities),len(set(identities)))

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
        paths.append(ROOT / "_pages/nvme-notes.html")
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

    def test_contract_has_thirteen_reports_and_thirty_nine_artifacts(self):
        contract = json.loads(
            (ROOT / ".ai/nvme-report/output-contract.json").read_text(encoding="utf-8")
        )
        artifacts = contract["artifacts"]
        self.assertEqual(len(artifacts), 39)
        self.assertEqual(sum(item["format"] == "html" for item in artifacts), 13)
        self.assertEqual(sum(item["format"] == "markdown" for item in artifacts), 26)
        self.assertEqual(len({item["report_id"] for item in artifacts}), 13)
        self.assertEqual(
            {item.get("parity_group") for item in artifacts if item["format"] == "markdown"},
            {
                "base12-bilingual",
                "base3-bilingual",
                "base4-bilingual",
                "pcie14-bilingual",
                "basefwlog-bilingual",
                "basepower-bilingual",
                "baseselftest-bilingual", "basehmb-bilingual", "basenamespace-bilingual",
                "baseboot-bilingual", "basetelemetry-bilingual", "basesanitize-bilingual",
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

        for report in scope['reports']:
            included={f['id'] for f in register['entries'] if f['report_id']==report['id'] and f['scope_status']=='INCLUDE'}
            self.assertEqual(included,set(report['included_figure_ids']))

    def test_selftest_and_hmb_are_independently_readable(self):
        st=(ROOT/'DOCS/nvme-spec-report/base-device-self-test/tutorial-zh-tw.html').read_text()
        hmb=(ROOT/'DOCS/nvme-spec-report/base-hmb-emulation/tutorial-zh-tw.html').read_text()
        for term in ('008C0006h','Invalid Namespace or Format','Invalid Field in Command','FLBA'):
            self.assertIn(term,st)
        for term in ('HMDLEC','HMNARE','DSTRD','NDT','00000012_34567000h'):
            self.assertIn(term,hmb)
        self.assertNotIn('SELFTEST-',hmb)
        self.assertNotIn('HMB-',st)

    def test_namespace_lifecycle_keeps_complete_figure_teaching(self):
        text=(ROOT/'DOCS/nvme-spec-report/base-namespace-management/tutorial-zh-tw.html').read_text()
        for term in ('NSZE','NCAP','NUSE','Controller List','DNCS','bits 31:24','bits 3:0'):
            self.assertIn(term,text)
        self.assertNotIn('SELFTEST-',text)
        figures=VALIDATOR.load_json('figure-table-register.json')['entries']
        expected={f['id'] for f in figures if f['report_id']=='base-namespace-management' and f['scope_status']=='INCLUDE'}
        self.assertEqual(VALIDATOR.figure_table_ids(text),expected)

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
            for required in ((
                "FID 02h", "FID 04h", "FID 0Ch",
                "FID 10h", "FID 11h", "0007D018h", "01400157h", "01570161h",
            ) if artifact['format']=='html' else ("0007D018h",)):
                self.assertIn(required.lower(), text.lower())
            for excluded in (
                "§5.2.30.1.2.1", "§8.1.19.6", "§8.1.19.7",
                "Figure 469", "Figure 742", "Figure 743", "Figure 744",
            ):
                self.assertNotIn(excluded, text)
        self.assertEqual(len(texts), 3)
        self.assertNotEqual(texts[0], texts[1])
        self.assertEqual(
            VALIDATOR.claim_id_sequence(texts[1]),
            VALIDATOR.claim_id_sequence(texts[2]),
        )

    def test_firmware_report_is_tutorial_first_and_lid03_only(self):
        contract = json.loads(
            (ROOT / ".ai/nvme-report/output-contract.json").read_text(encoding="utf-8")
        )
        for artifact in contract["artifacts"]:
            if artifact["report_id"] != "base-admin-fw-logs":
                continue
            text = (ROOT / artifact["path"]).read_text(encoding="utf-8")
            for required in (("LID 03h", "007F0003h") if artifact["format"]=="html" else ("LID 03h",)):
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

    def test_three_editions_preserve_all_claims_without_visible_tracking(self):
        contract = VALIDATOR.load_json("output-contract.json")
        claims = VALIDATOR.load_json("claims.json")["claims"]
        for artifact in contract["artifacts"]:
            text = (ROOT / artifact["path"]).read_text(encoding="utf-8")
            expected = {c["id"] for c in claims if c["report_id"] == artifact["report_id"]}
            with self.subTest(artifact=artifact["id"]):
                self.assertEqual(artifact["claim_coverage"], "all" if artifact['format']=='html' else 'overview')
                if artifact['format']=='html':
                    self.assertEqual(VALIDATOR.claim_ids(text), expected)
                else:
                    self.assertTrue(VALIDATOR.claim_ids(text) < expected)
                    self.assertIn('id="spec-reading"',text)
                    self.assertNotIn('class="technical-note"',text)
                    self.assertNotIn('class="figure-reading-fold"',text)
                visible = VALIDATOR.reader_text(text)
                for claim_id in expected:
                    self.assertNotIn(claim_id, visible)
                self.assertFalse(VALIDATOR.validate_editorial_structure(text))

    def test_html_has_responsive_accessible_reading_structure(self):
        contract = VALIDATOR.load_json("output-contract.json")
        artifacts = [a for a in contract["artifacts"] if a["format"] == "html"]
        self.assertEqual(len(artifacts), 13)
        for artifact in artifacts:
            with self.subTest(artifact=artifact["id"]):
                self.assertFalse(VALIDATOR.validate_html(ROOT / artifact["path"]))

    def test_light_and_dark_semantic_palettes_meet_text_contrast(self):
        source = (ROOT / "assets/css/nvme-reader.css").read_text(encoding="utf-8")
        blocks = re.findall(r"\.nvme-note, \.edition-tutorial\s*\{(.*?)\}", source, re.S)
        palettes = []
        for block in blocks:
            values = dict(re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]{3,6})", block))
            values = {key: '#' + ''.join(c * 2 for c in value[1:]) if len(value) == 4 else value for key, value in values.items()}
            if all(key in values for key in ("ink", "accent", "soft", "example")):
                palettes.append(values)
        self.assertEqual(len(palettes), 2)

        def luminance(color: str) -> float:
            channels = [int(color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
            linear = [
                value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
                for value in channels
            ]
            return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

        for palette_name, palette in zip(("light", "dark"), palettes[:2]):
            for role, background_role in (("ink", "surface"), ("muted", "surface"),
                                          ("accent", "soft"), ("example", "example-soft"),
                                          ("warning", "surface"), ("blue", "surface"), ("violet", "surface")):
                foreground = luminance(palette[role])
                background = luminance(palette[background_role])
                ratio = (max(foreground, background) + 0.05) / (
                    min(foreground, background) + 0.05
                )
                with self.subTest(palette=palette_name, role=role):
                    self.assertGreaterEqual(ratio, 4.5)

    def test_retired_detailed_html_is_not_published_or_linked(self):
        contract = VALIDATOR.load_json("output-contract.json")
        for artifact in contract["artifacts"]:
            self.assertNotIn("detailed", artifact["id"])
            text = (ROOT / artifact["path"]).read_text(encoding="utf-8")
            self.assertNotIn("detailed-spec-zh-tw.html", text)
        self.assertEqual(list((ROOT / "DOCS/nvme-spec-report").glob("*/detailed-spec-zh-tw.html")), [])

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
                rf"(?m)^img:\s*{re.escape(expected_images.get(artifact['id'], 'posts/2026/cat_title.jpg' if artifact['language']=='en' else 'posts/2026/dogMC_title.jpg'))}\s*$",
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
            self.assertIsNone(VALIDATOR.forbidden_published(VALIDATOR.reader_text(text), artifact['report_id'], VALIDATOR.load_json('scope.json')['entries']))
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

        for artifact in contract["artifacts"]:
            if artifact["format"] == "html":
                self.assertFalse(VALIDATOR.validate_html(ROOT / artifact["path"]))

    def test_reader_text_cannot_count_hidden_claim_body_as_teaching(self):
        text = '<style>claim text</style><!-- claim text --><p>Actual explanation &amp; example.</p>'
        visible = VALIDATOR.reader_text(text)
        self.assertNotIn("claim text", visible)
        self.assertIn("Actual explanation & example.", visible)

    def test_editorial_validation_rejects_missing_overview_and_visible_internal_ids(self):
        minimal = ('<section id="topic-overview"><h2>Queue relationships</h2></section>'
                   '<!-- claim:BASE4-TEST -->'
                   '<p>A submission entry identifies its command.</p>'
                   '<p class="term-note">SQE: Submission Queue Entry.</p>'
                   '<details class="source-note"><summary>Base §4.1</summary>Full source</details>'
                   '<section id="knowledge-check"><p>Why does the command carry an identifier?</p></section>')
        self.assertFalse(VALIDATOR.validate_editorial_structure(minimal))
        self.assertTrue(VALIDATOR.validate_editorial_structure(minimal.replace('id="topic-overview"', 'id="other"')))
        self.assertTrue(VALIDATOR.validate_editorial_structure(minimal.replace('<!-- claim:BASE4-TEST -->', '<p data-claim-id="BASE4-TEST">BASE4-TEST</p>')))
        self.assertTrue(VALIDATOR.validate_editorial_structure(minimal + '<h2>Decode</h2>'))
        # A concrete technical sentence can explain decoding; the vague label is the problem.
        self.assertFalse(VALIDATOR.validate_editorial_structure(minimal + '<p>Decode the low 4 bits as the command opcode.</p>'))
        self.assertTrue(VALIDATOR.validate_editorial_structure(minimal + '<a href="detailed-spec-zh-tw.html">Old version</a>'))

    def test_source_backed_background_does_not_silently_expand_scope(self):
        entry = {"status": "PREREQUISITE_ONLY", "report_id": "base-ch3",
                 "source_id": "NVME-BASE-2.4", "sections": ["2.2"],
                 "teaching_necessity": "Explain how the local queue model differs from a remote transport.",
                 "supports_topic": "Queue location", "background_terms": ["Fabrics"]}
        self.assertIsNotNone(VALIDATOR.forbidden_published("Fabrics", "base-ch3"))
        self.assertIsNotNone(VALIDATOR.forbidden_published("Fabrics", "base-ch3", [entry]))
        self.assertIsNotNone(VALIDATOR.forbidden_published("Fabrics", "base-ch4", [entry]))
        self.assertIsNotNone(VALIDATOR.forbidden_published("Fabrics", "base-ch3", [{**entry, "teaching_necessity": ""}]))

    def test_setup_rejects_subset_coverage_and_background_without_necessity(self):
        documents = {name: VALIDATOR.load_json(name) for name in (
            "source-register.json", "scope.json", "output-contract.json", "claims.json", "figure-table-register.json")}
        documents["output-contract.json"]["artifacts"][0]["claim_coverage"] = "subset"
        prerequisite = next(e for e in documents["scope.json"]["entries"] if e["status"] == "PREREQUISITE_ONLY")
        prerequisite.pop("teaching_necessity")
        with mock.patch.object(VALIDATOR, "load_json", side_effect=documents.__getitem__):
            errors = VALIDATOR.validate_setup(None)
        self.assertTrue(any("完整 HTML 教學" in error for error in errors))
        self.assertTrue(any("teaching_necessity" in error for error in errors))

    def test_bilingual_posts_share_nonempty_topic_and_source_order(self):
        contract = VALIDATOR.load_json("output-contract.json")
        for report_id in {a["report_id"] for a in contract["artifacts"]}:
            posts = [a for a in contract["artifacts"] if a["report_id"] == report_id and a["format"] == "markdown"]
            self.assertEqual(len(posts), 2)
            texts = [(ROOT / a["path"]).read_text(encoding="utf-8") for a in posts]
            modules = [re.findall(r'\bid="module-([^"\']+)', text) for text in texts]
            with self.subTest(report=report_id):
                self.assertTrue(modules[0])
                self.assertEqual(modules[0], modules[1])
                self.assertEqual(VALIDATOR.claim_id_sequence(texts[0]), VALIDATOR.claim_id_sequence(texts[1]))
                self.assertEqual(VALIDATOR.FIGURE_TABLE_MARKER.findall(texts[0]), VALIDATOR.FIGURE_TABLE_MARKER.findall(texts[1]))

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

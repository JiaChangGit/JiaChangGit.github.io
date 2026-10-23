"""Test target/step/source relationships, native controls and source regeneration.

Fixtures describe only a renderer demonstration, not a normative PCIe sequence.
Browser tests separately establish actual CSS, keyboard and print behavior.
"""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from scripts.pcie_teaching import Tree, expand_walks, render_walk
from scripts.validate_pcie_teaching import validate_teaching


def fixture():
    return {
        "walk_id": "demo",
        "title": "Reading a two-role diagram",
        "svg": '<svg viewBox="0 0 420 150" role="img" aria-labelledby="demo-svg-title demo-svg-desc"><title id="demo-svg-title">Two teaching roles</title><desc id="demo-svg-desc">Both roles stay visible while the guide highlights their responsibilities.</desc><g data-walk-target="sender"><rect x="10" y="30" width="160" height="80" fill="var(--blue-soft)" stroke="var(--line)"/><text x="30" y="75">Sender</text></g><path d="M170 70 H240" stroke="var(--line)"/><g data-walk-target="receiver"><rect x="240" y="30" width="160" height="80" fill="var(--teal-soft)" stroke="var(--line)"/><text x="260" y="75">Receiver</text></g></svg>',
        "caption_html": "<p>Author-created diagram for renderer testing.</p>",
        "order_html": "<p>The numbers follow the explanation order; this fixture specifies no protocol timing.</p>",
        "language": "en",
        "steps": [
            {"title": "Locate the sender", "html": "<p>Find the sender on the left.</p>", "targets": ["sender"], "condition_html": "<p>Use the two-role demonstration above.</p>", "source_html": "<p>Demonstration source, section A.</p>", "claim_ids": ["PCIE-DEMO-A"]},
            {"title": "Follow the relationship", "html": "<p>Compare the two roles connected by the line.</p>", "targets": ["sender", "receiver"], "condition_html": "<p>Both roles refer to the same demonstration.</p>", "source_html": "<p>Demonstration source, section B.</p>", "claim_ids": ["PCIE-DEMO-B"]},
        ],
        "components": [{"target": "sender", "title": "Sender", "html": "<p>The first explanation begins here.</p>", "basic_html": "<p>The source role in this demonstration.</p>"}],
    }


class TeachingGuideTests(unittest.TestCase):
    def setUp(self):
        self.data = fixture()
        self.html = render_walk(**self.data)
        self.claims = {"PCIE-DEMO-A", "PCIE-DEMO-B"}

    def assertInvalid(self, text, diagnostic):
        errors = validate_teaching(text, self.claims)
        self.assertTrue(any(diagnostic in error for error in errors), errors)

    def test_target_memberships_follow_authored_steps(self):
        self.assertEqual(validate_teaching(self.html, self.claims), [])
        nodes = list(Tree(self.html).root.descendants())
        memberships = {node.attrs["data-walk-target"]: set(node.attrs["data-walk-steps"].split()) for node in nodes if node.attrs.get("data-walk-target")}
        self.assertEqual(memberships, {"sender": {"1", "2"}, "receiver": {"2"}})
        # The source IDs are machine-only metadata, not visible prose.
        self.assertNotIn("PCIE-DEMO", Tree(self.html).root.text())

    def test_summary_stays_between_diagram_and_step_explanations(self):
        self.data["summary_html"] = '<p>Main point before the detailed steps.</p>'
        result = render_walk(**self.data)
        self.assertLess(result.index('</figure>'), result.index('Main point'))
        self.assertLess(result.index('Main point'), result.index('<ol class="walk-steps">'))
        self.assertEqual(validate_teaching(result, self.claims), [])
        self.data["summary_html"] = '<!-- not visible -->'
        with self.assertRaisesRegex(ValueError, 'visible text'):
            render_walk(**self.data)

    def test_disconnected_target_and_highlight_are_rejected(self):
        self.assertInvalid(self.html.replace('data-walk-targets="sender receiver"', 'data-walk-targets="sender absent"'), "missing diagram target")
        self.assertInvalid(self.html.replace('data-walk-steps="1 2"', 'data-walk-steps="1"'), "highlight membership differs")
        changed = deepcopy(self.data)
        changed["steps"][1]["targets"] = ["unknown"]
        with self.assertRaisesRegex(ValueError, "targets must match"):
            render_walk(**changed)

    def test_controls_must_remain_selectable_and_connected(self):
        self.assertInvalid(self.html.replace('value="2"', 'value="2" disabled="disabled"'), "unavailable to native keyboard")
        self.assertInvalid(self.html.replace('type="radio"', 'type="button"', 1), "native radio")
        self.assertInvalid(self.html.replace('for="demo-choice-2"', 'for="demo-choice-1"'), "exactly one descriptive label")
        self.assertInvalid(self.html.replace('aria-controls="demo-view demo-step-2"', 'aria-controls="demo-view demo-step-1"'), "matching explanation")
        self.assertInvalid(self.html.replace('class="walk-choice"', 'class="walk-choice" hidden="hidden"', 1), "unavailable to native keyboard")

    def test_conditions_and_sources_are_visible_and_registered(self):
        self.assertInvalid(self.html.replace('<div class="walk-condition"><p>Use the two-role demonstration above.</p></div>', '<div class="walk-condition"></div>'), "visible walk-condition")
        self.assertInvalid(self.html.replace('class="walk-source"', 'class="walk-source" hidden="hidden"', 1), "visible walk-source")
        self.assertInvalid(self.html.replace('data-source-claims="PCIE-DEMO-B"', 'data-source-claims="PCIE-UNKNOWN"'), "unknown source claim")
        self.assertInvalid(self.html.replace('class="walk-explanation"', 'class="walk-explanation" style="display:none"', 1), "visible walk-explanation")
        changed = deepcopy(self.data)
        changed["steps"][0]["source_html"] = "<!-- source to be added -->"
        with self.assertRaisesRegex(ValueError, "visible text"):
            render_walk(**changed)

    def test_complete_svg_and_accessible_labels_are_required(self):
        self.assertInvalid(self.html.replace('demo-svg-title demo-svg-desc', 'demo-svg-title'), "labelled, nonempty desc")
        self.assertInvalid(self.html.replace('id="demo-svg-desc"', 'id="demo-svg-title"'), "Duplicate document id")
        self.assertInvalid(self.html.replace('data-component-target="sender"', 'data-component-target="receiver"'), "SVG link is disconnected")
        self.assertInvalid(self.html.replace('<div class="walk-order">', '<div class="walk-order" hidden="hidden">'), "visible reading-order")

    def test_multiple_guides_need_distinct_group_names_and_ids(self):
        self.assertInvalid(self.html + self.html, "radio group name reused")
        second = deepcopy(self.data)
        second["walk_id"] = "second"
        second["svg"] = second["svg"].replace("demo-svg", "second-svg")
        self.assertEqual(validate_teaching(self.html + render_walk(**second), self.claims), [])

    def test_does_not_allow_scripts_or_external_assets_in_guide(self):
        for active in ['<script>window.alert(1)</script>', '<img src="https://example.test/image.png">', '<p onclick="test()">Action</p>']:
            changed = deepcopy(self.data)
            changed["steps"][0]["html"] += active
            with self.assertRaises(ValueError):
                render_walk(**changed)

    def test_limit_is_rendering_contract_not_content_quota(self):
        changed = deepcopy(self.data)
        changed["steps"] *= 5
        with self.assertRaisesRegex(ValueError, "1–8"):
            render_walk(**changed)
        self.assertEqual(validate_teaching("<p>A static article is valid.</p>", self.claims), [])
        self.assertTrue(validate_teaching("<p>Missing guide.</p>", self.claims, require_walk=True))

    def test_regeneration_is_idempotent_and_detects_authoring_drift(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "walks").mkdir()
            (root / "walks/demo.json").write_text(json.dumps(self.data), encoding="utf-8")
            source = '<p>Before</p>\n<!-- pcie-walk: walks/demo.json -->\nSTALE\n<!-- /pcie-walk -->\n<p>After</p>'
            rendered = expand_walks(source, root)
            self.assertNotEqual(source, rendered)
            self.assertEqual(rendered, expand_walks(rendered, root))
            self.assertEqual(validate_teaching(rendered, self.claims), [])
            self.assertEqual(Tree(rendered).root.text().split()[0], "Before")
            self.assertEqual(Tree(rendered).root.text().split()[-1], "After")
            modified = rendered.replace("Find the sender on the left.", "A manually changed explanation.")
            self.assertNotEqual(modified, expand_walks(modified, root))

    def test_missing_escaped_nested_and_dangling_sources_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "walks").mkdir()
            (root / "outside.json").write_text(json.dumps(self.data), encoding="utf-8")
            for path in ("walks/../outside.json", "../outside.json", "C:/outside.json", "walks\\demo.json"):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    expand_walks(f'<!-- pcie-walk: {path} --><!-- /pcie-walk -->', root)
            with self.assertRaises(OSError):
                expand_walks('<!-- pcie-walk: walks/missing.json --><!-- /pcie-walk -->', root)
            for malformed in ('<!-- pcie-walk: walks/demo.json -->', '<!-- /pcie-walk -->', '<!-- pcie-walk: walks/a.json --><!-- pcie-walk: walks/b.json --><!-- /pcie-walk --><!-- /pcie-walk -->'):
                with self.subTest(source=malformed), self.assertRaises(ValueError):
                    expand_walks(malformed, root)


if __name__ == "__main__":
    unittest.main()

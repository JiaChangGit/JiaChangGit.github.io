"""The deployed cleanup must be scoped, idempotent, and preserve readable citations."""
from pathlib import Path
import tempfile
import unittest
from scripts.clean_public_teaching import clean


class PublicTeachingCleanupTests(unittest.TestCase):
    def test_removes_only_scoped_internal_markers(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            samples = {
                'DOCS/pcie-course/chapter-1.html': '<!-- pcie-walk: walks/a.json --><div data-source-claims="ID">§2.2</div><!-- /pcie-walk -->',
                'pcie/chapter-1-en/index.html': '<!-- pcie-walk: walks/b.json --><p>Figure 1-1</p><!-- /pcie-walk -->',
                'DOCS/nvme-spec-report/pcie-transport-1.4/tutorial-zh-tw.html': '<!-- claim:PCIE14-SCOPE --><!-- figure-table:PCIE14-FIG-001 --><!-- qa:pcie-transport-1.4-doorbell-stride --><p>Figure 1</p>',
                'DOCS/nvme-spec-report/base-ch1-2/tutorial-zh-tw.html': '<!-- claim:BASE12-FAMILY --><p>Other article</p>',
            }
            for rel, content in samples.items():
                target = site / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding='utf-8')
            self.assertEqual(len(clean(site, check=True)), 3)
            self.assertEqual(len(clean(site)), 3)
            self.assertEqual(clean(site, check=True), [])
            self.assertEqual((site/'DOCS/pcie-course/chapter-1.html').read_text(), '<div>§2.2</div>')
            self.assertEqual((site/'DOCS/nvme-spec-report/pcie-transport-1.4/tutorial-zh-tw.html').read_text(), '<p>Figure 1</p>')
            self.assertEqual((site/'DOCS/nvme-spec-report/base-ch1-2/tutorial-zh-tw.html').read_text(), samples['DOCS/nvme-spec-report/base-ch1-2/tutorial-zh-tw.html'])


if __name__ == '__main__':
    unittest.main()

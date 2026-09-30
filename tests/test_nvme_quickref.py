"""Publication and lookup regressions for the independently scoped figure series."""
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit

from scripts import build_nvme_quickref as qr

class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []; self.links = []; self.figures = []; self.paragraphs = []; self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs); self.tags.append(tag)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'a': self.links.append(a['href'])
        if 'data-figure' in a: self.figures.append(a['data-figure'])
        if 'data-paragraph' in a: self.paragraphs.append(a['data-paragraph'])

class QuickReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs = qr.generated()
        cls.docs = {p: Document(v) for p, v in cls.outputs.items()}
        cls.scope = json.loads((qr.CONTROL/'scope.json').read_text())

    def test_approved_independent_scope_and_editions(self):
        self.assertEqual(self.scope['status'], 'approved')
        self.assertFalse(self.scope['inherit_previous_report_exclusions'])
        self.assertEqual(len(self.scope['sources']), 3)
        self.assertEqual(len(self.scope['topics']), 7)
        selection = [k for t in self.scope['topics'] for k in t['figures']]
        self.assertEqual(len(selection), len(set(selection)))
        self.assertEqual(set(selection), set(qr.REG))
        self.assertEqual(set(selection), set(qr.CARDS))
        self.assertEqual(len(self.outputs), 24)
        # Former report exclusions remain valid entries in this separately approved scope.
        for key in ['B225', 'B232', 'B294', 'B541', 'P75']:
            self.assertIn(key, selection)

    def test_bilingual_order_and_standalone_full_coverage(self):
        for topic, *_ in qr.TOPICS:
            editions = [Document(qr.body(topic, lang, offline)[1])
                        for lang, offline in [('zh', True), ('zh', False), ('en', False)]]
            for doc in editions[1:]:
                self.assertEqual(doc.figures, editions[0].figures)
                self.assertEqual(doc.paragraphs, editions[0].paragraphs)
            self.assertEqual(editions[0].figures, next(t['figures'] for t in self.scope['topics'] if t['id'] == topic))

    def test_all_links_resolve_in_each_edition(self):
        routes = {}
        for path, text in self.outputs.items():
            route = '/'+path if path.endswith('.html') else json.loads(re.search(r'^permalink: (.+)$', text, re.M)[1])
            routes[route] = self.docs[path]
        for path, doc in self.docs.items():
            self.assertEqual(len(doc.ids), len(set(doc.ids)), path)
            for link in doc.links:
                parts = urlsplit(link)
                if link.startswith('#'): target = doc
                elif link.startswith('/'): target = routes[parts.path]
                else: target = routes['/'+str(Path(path).parent / parts.path)]
                if parts.fragment: self.assertIn(parts.fragment, target.ids, (path, link))

    def test_unique_figure_specific_explanations(self):
        for lang in ['zh', 'en']:
            paragraphs = [p for c in qr.CARDS.values() for p in c['paragraphs'][lang]]
            self.assertEqual([p for p, count in Counter(paragraphs).items() if count > 1], [])
        for key, card in qr.CARDS.items():
            self.assertNotIn(key, card['related'])
            for target in card['related']: self.assertIn(target, qr.REG)
            for lang in ['zh', 'en']: self.assertEqual(len(card['paragraphs'][lang]), 3)

    def test_source_locations_and_large_table_continuations(self):
        self.assertEqual(qr.REG['B338']['pdf_pages'], [366, 408])
        self.assertEqual(qr.REG['N129']['pdf_pages'], [103, 106])
        self.assertEqual(qr.REG['B43']['section'], '3.1.4.7')
        self.assertEqual(qr.REG['P6']['section'], '3.1.2.2')
        for key, entry in qr.REG.items():
            self.assertRegex(entry['page_text_sha256'], r'^[0-9a-f]{64}$')
            self.assertEqual(entry['printed_pages'], [p-(26 if key[0]=='B' else 0) for p in entry['pdf_pages']])
            a,b = entry['pdf_pages']
            for row in qr.CARDS[key].get('field_routes', []):
                self.assertTrue(a <= row[3] <= row[4] <= b, (key, row))
            for lang in ['zh', 'en']:
                text = qr.render_card(key, 1, lang, False)
                self.assertIn(entry['section'], text)
                self.assertIn(qr.numrange(entry['pdf_pages']), text)

    def test_no_fabrics_or_pdf_redistribution_and_offline_dependencies(self):
        for path, text in self.outputs.items():
            self.assertNotRegex(text, r'(?i)fabrics|NVMe-oF|\bNQN\b|discovery')
            self.assertNotRegex(text, r'(?i)(?:href|src)="[^"]+\.pdf')
            if path.endswith('.html'):
                self.assertFalse({'script','iframe','embed','object','link','img'} & set(self.docs[path].tags))
                self.assertIn('viewport-fit=cover', text)
                self.assertIn('prefers-color-scheme:dark', text)

    def test_calculated_examples_match_public_copy(self):
        # Derive from independent raw inputs so a mistyped example fails publication.
        tests = {
            'B477': f'{(2000 << 8) | (3 << 3):08X}h',
            'B472': f'{((4-1) << 16) | (8-1):08X}h',
            'B101': f'{(1 << 31) | (2 << 17) | (1 << 16) | 0x2a:08X}h',
            'B205': str(4 * ((1 << 16) + 1)),
            'N123': f'{1000 * (1 << 12):,}',
            'B234': str(512 + 21 + 3 + 20),
            'P76': str(32 + 5 * 7),
        }
        for key, expected in tests.items():
            for lang in ['zh','en']:
                self.assertIn(expected, ' '.join(qr.CARDS[key]['paragraphs'][lang]), (key,lang))

    def test_generated_artifacts_current(self):
        for path, expected in self.outputs.items():
            self.assertEqual((qr.ROOT/path).read_text(), expected, path)

if __name__ == '__main__': unittest.main()

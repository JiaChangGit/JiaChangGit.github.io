"""Shared source routing, escaping and public-output security invariants."""
import unittest
from html.parser import HTMLParser
from scripts.spec_teaching import reading_route
from scripts.validate_public_teaching import OfflineSafety,PRIVATE_PATH,SOURCE_PDFS
from scripts.nvme_scenario_lessons import LEAD_CASES,ROUTES,lesson_route
from scripts.nvme_scenario_render import CASES
from scripts.build_nvme_quickref import REG,body

class SharedTeachingTests(unittest.TestCase):
    def test_author_text_is_escaped(self):
        result=reading_route('r','<script>',[('<img>','<script>alert(1)</script>',[('" onclick="x','#safe')])])
        self.assertNotIn('<script>',result)
        self.assertEqual(OfflineSafety(result).errors,[])

    def test_links_cannot_execute_or_escape(self):
        for url in ['javascript:alert(1)','data:text/html,x','//example.com','../secret','\\\\host\\file','file:///x']:
            with self.subTest(url=url),self.assertRaises(ValueError):reading_route('x','route',[('step','why',[('link',url)])])

    def test_every_volume_has_one_existing_opening_case(self):
        ids={c['id'] for c in CASES}
        self.assertEqual(set(LEAD_CASES),set(ROUTES))
        for topic,identifier in LEAD_CASES.items():
            self.assertIn(identifier,ids)
            c=next(c for c in CASES if c['id']==identifier)
            for language in ['zh','en']:
                route=lesson_route(c,language,REG)
                self.assertIn('route-'+identifier,route)
                for _,_,keys in ROUTES[topic]:
                    for key in keys:self.assertIn(key,REG)

    def test_opening_scenario_is_not_duplicated(self):
        for topic,identifier in LEAD_CASES.items():
            text=body(topic,'zh',True)[1]
            self.assertEqual(text.count('data-scenario="'+identifier+'"'),1)
            self.assertLess(text.index('data-scenario="'+identifier+'"'),text.index('接著看其他情境'))

    def test_offline_assets_and_handlers_are_rejected(self):
        for html in ['<img src="https://example.com/x">','<p onclick="x()">x</p>','<a href="java\nscript:x">x</a>','<form action="/x">']:
            self.assertTrue(OfflineSafety(html).errors)

    def test_local_svg_and_native_explanations_are_allowed(self):
        self.assertEqual(OfflineSafety('<details open><summary>Why</summary><svg><use href="#node"></use></svg></details>').errors,[])

    def test_specification_names_are_not_local_paths(self):
        self.assertIsNone(PRIVATE_PATH.search('NVMe over PCIe Transport 1.4 · PDF 19'))
        self.assertTrue(SOURCE_PDFS.fullmatch('PCI-Express-Base-Specification-Revision-6.0.pdf'))
        self.assertIsNone(SOURCE_PDFS.fullmatch('my-public-article.pdf'))

if __name__=='__main__':unittest.main()

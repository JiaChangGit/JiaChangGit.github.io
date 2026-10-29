"""Shared source routing, escaping and public-output security invariants."""
import unittest
import json
from pathlib import Path
import subprocess
import tempfile
from html.parser import HTMLParser
from scripts.spec_teaching import reading_route
from scripts.validate_public_teaching import OfflineSafety,PRIVATE_PATH,SOURCE_PDFS,validate,ROOT
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

    def test_report_opening_links_match_existing_editions_and_anchors(self):
        pairs=[
            ('pcie-transport-1.4','2026-08-28-nvme-pcie-transport-1-4',
             'doorbells','q-027','command','exercise-command-01'),
            ('nvm-command-set-1.3','2026-09-03-nvme-nvm-command-set-1-3',
             'data-io','q-321','io','exercise-io-01'),
        ]
        for report,post,question,qid,figure,fid in pairs:
            tutorial=ROOT/'DOCS/nvme-spec-report'/report/'tutorial-zh-tw.html'
            text=tutorial.read_text(encoding='utf-8')
            for relative,anchor in [(f'../../nvme-question-bank/{question}.html',qid),
                                    (f'../../nvme-quick-reference/{figure}.html',fid)]:
                with self.subTest(report=report,edition='tutorial',target=relative):
                    self.assertIn(f'href="{relative}#{anchor}"',text)
                    self.assertIn(f'id="{anchor}"',(tutorial.parent/relative).resolve().read_text(encoding='utf-8'))
            for language in ('zh-tw','en'):
                text=(ROOT/'_posts'/f'{post}-{language}.md').read_text(encoding='utf-8')
                for series,slug,anchor,pattern in [
                    ('question-bank',question,qid,f'*-nvme-question-bank-{question}-{language}.md'),
                    ('figure-reference',figure,fid,f'*-nvme-figure-reference-{figure}-{language}.md'),
                ]:
                    with self.subTest(report=report,edition=language,target=series):
                        self.assertIn(f'href="/nvme/{series}/{slug}/{language}/#{anchor}"',text)
                        targets=list((ROOT/'_posts').glob(pattern))
                        self.assertEqual(len(targets),1)
                        self.assertIn(f'id="{anchor}"',targets[0].read_text(encoding='utf-8'))

    def test_offline_assets_and_handlers_are_rejected(self):
        for html in ['<img src="https://example.com/x">','<p onclick="x()">x</p>','<a href="java\nscript:x">x</a>','<form action="/x">']:
            self.assertTrue(OfflineSafety(html).errors)

    def test_local_svg_and_native_explanations_are_allowed(self):
        self.assertEqual(OfflineSafety('<details open><summary>Why</summary><svg><use href="#node"></use></svg></details>').errors,[])

    def test_specification_names_are_not_local_paths(self):
        self.assertIsNone(PRIVATE_PATH.search('NVMe over PCIe Transport 1.4 · PDF 19'))
        self.assertTrue(SOURCE_PDFS.fullmatch('PCI-Express-Base-Specification-Revision-6.0.pdf'))
        self.assertIsNone(SOURCE_PDFS.fullmatch('my-public-article.pdf'))

    def temporary_repository(self,root):
        subprocess.run(['git','init','-q',str(root)],check=True)
        (root/'.gitignore').write_bytes((ROOT/'.gitignore').read_bytes())
        scope=root/'.ai/spec-teaching/scope.json'
        scope.parent.mkdir(parents=True)
        scope.write_text(json.dumps({'phase':'test','series':{}}))

    def test_dependency_fixture_is_ignored_but_force_tracked_key_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            self.temporary_repository(root)
            fixture=root/'vendor/bundle/test/client.key'
            fixture.parent.mkdir(parents=True)
            fixture.write_bytes(b'-----BEGIN '+b'PRIVATE KEY-----\nNot a real key\n')
            self.assertEqual(validate(root)[1],[])
            subprocess.run(['git','-C',str(root),'add','-f',str(fixture.relative_to(root))],check=True)
            self.assertTrue(any('possible credential signature' in issue for issue in validate(root)[1]))

    def test_built_site_must_not_contain_bundle_runtime(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'repo'
            self.temporary_repository(root)
            site=Path(directory)/'site'
            (site/'vendor/bundle').mkdir(parents=True)
            self.assertIn('Built site exposes vendor/bundle',validate(root,site)[1])
            public_key=site/'unexpected.key'
            public_key.write_bytes(b'-----BEGIN '+b'PRIVATE KEY-----\nFixture only\n')
            self.assertTrue(any('unexpected.key: possible credential signature' in issue for issue in validate(root,site)[1]))

if __name__=='__main__':unittest.main()

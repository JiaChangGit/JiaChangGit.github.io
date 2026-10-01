"""Exercise publication contract and independent calculations for worked cases."""
from collections import Counter
from html.parser import HTMLParser
import json
import unittest
from scripts import build_nvme_quickref as qr
from scripts.nvme_scenario_render import CASES, refs

class Exercises(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.cases=[]; self.current=None; self.in_answer=False
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'data-scenario' in a:
            self.current=dict(id=a['data-scenario'],steps=[],answers=0)
            self.cases.append(self.current)
        if tag=='details' and a.get('class')=='qr-answer':
            assert 'open' not in a, 'Answers must start collapsed'
            self.in_answer=True; self.current['answers']+=1
        if 'data-reasoning' in a:
            assert self.in_answer, 'Reasoning leaked outside the answer'
            self.current['steps'].append(a['data-reasoning'])
    def handle_endtag(self,tag):
        if tag=='details':self.in_answer=False

class ScenarioTests(unittest.TestCase):
    def test_existing_eight_pages_are_the_only_series(self):
        outputs=qr.generated()
        self.assertEqual(len(outputs),24)
        manifest=json.loads((qr.CONTROL/'outputs.json').read_text())
        self.assertEqual(set(outputs),{a['path'] for a in manifest['artifacts']})
        self.assertEqual({c['topic'] for c in CASES},{t[0] for t in qr.TOPICS})
        self.assertEqual(len(CASES),len({c['id'] for c in CASES}))

    def test_every_case_has_equivalent_collapsed_answers_and_one_home(self):
        for topic,*_ in qr.TOPICS:
            editions=[Exercises(qr.body(topic,lang,offline)[1]).cases
                      for lang,offline in [('zh',True),('zh',False),('en',False)]]
            self.assertEqual(editions[0],editions[1]);self.assertEqual(editions[1],editions[2])
            self.assertEqual([c['id'] for c in editions[0]],[c['id'] for c in CASES if c['topic']==topic])
            for c in editions[0]:
                self.assertEqual(c['answers'],1)
                self.assertEqual(len(c['steps']),3)
        for lang in ['zh','en']:
            index=qr.body('index',lang)[1]
            for c in CASES:self.assertEqual(index.count('#exercise-'+c['id']+'"'),1)
            self.assertNotIn('data-scenario=',index)

    def test_evidence_covers_all_cases_and_precise_selected_pages(self):
        manifest=json.loads((qr.CONTROL/'scenario-evidence.json').read_text())
        self.assertEqual(manifest['scenarios'],[dict(id=c['id'],topic=c['topic'],sources=c['sources']) for c in CASES])
        selected={s for c in CASES for s in c['sources']}
        self.assertEqual(set(manifest['evidence']),selected)
        for token,e in manifest['evidence'].items():
            r=refs(token,qr.REG)
            self.assertEqual(r['pages'],e['pdf_pages'])
            self.assertEqual(r['section'],e['section'])
            self.assertRegex(e['page_text_sha256'],r'^[0-9a-f]{64}$')
        for c in CASES:
            self.assertTrue(c['figures']);self.assertTrue(c['sources'])
            for key in c['figures']:self.assertIn(key,qr.REG)

    def test_no_copied_figure_paragraphs_or_duplicate_case_answers(self):
        for language in range(2):
            paragraphs=[p[language] for c in CASES for p in c['steps']]
            self.assertTrue(all(count==1 for count in Counter(paragraphs).values()))
            existing={p for c in qr.CARDS.values() for p in c['paragraphs']['zh' if language==0 else 'en']}
            self.assertFalse(existing.intersection(paragraphs))
        for c in CASES:
            for pair in [c['title'],c['question'],c['route']]+c['steps']+c['observations']:
                self.assertEqual(len(pair),2)
                self.assertTrue(all(pair))

    def test_byte_count_address_and_record_walk_examples(self):
        cases={c['id']:c for c in CASES}
        # Derive answers from raw hypothetical inputs, independently of rendering.
        page=1<<(12+0);mdts=(1<<5)*page; block=(1<<12)+16
        self.assertGreater(32*block,mdts);self.assertEqual(mdts//block,31)
        base=(2<<32)|(0x40000004 & ~0x3fff);stride=4<<2
        expected={
            'identify-05':[str(mdts),str(32*block)],
            'init-02':[f'{base+0x1000+6*stride:016X}h',f'{base+0x1000+7*stride:016X}h'],
            'command-05':[f'{3072//4-1:04X}h',str(1024+3072-1)],
            'logs-07':[str(512+21+3+28),str(28-8)],
            'io-06':[str(4*4096),str(4*16)],
        }
        for key,values in expected.items():
            for lang in range(2):
                prose=' '.join(p[lang] for p in cases[key]['steps'])
                for value in values:self.assertIn(value,prose,(key,lang,value))
        # The same PRP start needs one or two additional data pages as length changes.
        room=4096-3072
        self.assertEqual((5120-room+4095)//4096,1)
        self.assertEqual((6144-room+4095)//4096,2)
        # Check atomic intervals with decoded, not raw, boundary size.
        boundary=7+1
        self.assertEqual(8//boundary,11//boundary)
        self.assertNotEqual(6//boundary,9//boundary)

if __name__=='__main__':unittest.main()

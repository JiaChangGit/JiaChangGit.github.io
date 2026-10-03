"""Publication contract, source drift, navigation and numerical teaching regressions."""
import json
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from scripts.build_nvme_question_bank import artifacts,QUESTIONS,ROOT
from scripts.nvme_qa_teaching import VOLUMES,AIDS,LESSONS
from scripts.nvme_qa_sources import check

class Document(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=[];self.links=[];self.questions=[];self.answers=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if 'data-question' in a:self.questions.append(int(a['data-question']))
        if 'data-answer' in a:self.answers.append(int(a['data-answer']))

class QuestionBankTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.outputs=artifacts()

    def test_approved_scope_includes_all_320(self):
        scope=json.loads((ROOT/'.ai/nvme-question-bank/scope.json').read_text())
        self.assertEqual(scope['status'],'approved');self.assertEqual(scope['question_range'],[1,320])
        self.assertEqual([q['id'] for q in QUESTIONS],list(range(1,321)))
        future=[i for a,b in scope['future_only'].values() for i in range(a,b+1)]
        self.assertEqual(future,[])

    def test_every_question_has_17_bilingual_answers(self):
        for q in QUESTIONS:
            self.assertEqual(sorted(q['answers']),list(range(1,18)))
            for pair in [q['title']]+list(q['answers'].values()):
                self.assertEqual(len(pair),2);self.assertTrue(all(isinstance(x,str) and x.strip() for x in pair))
                self.assertNotRegex(pair[1],r'[\u4e00-\u9fff]')

    def test_all_81_artifacts_match_builder(self):
        self.assertEqual(len(self.outputs),81)
        for path,expected in self.outputs.items():self.assertEqual(path.read_text(),expected,str(path))

    def test_volume_coverage_and_answer_numbering(self):
        for path,text in self.outputs.items():
            doc=Document(text)
            if 'question-bank-index-' in path.name or path.name=='index.html':
                self.assertEqual(doc.questions,[]);continue
            slug=next(v for v in VOLUMES if v[0] in path.name)
            self.assertEqual(doc.questions,list(range(slug[1],slug[2]+1)))
            self.assertEqual(doc.answers,list(range(1,18))*(slug[2]-slug[1]+1))

    def test_unique_anchors_and_local_fragment_resolution(self):
        for path,text in self.outputs.items():
            d=Document(text);self.assertEqual(len(d.ids),len(set(d.ids)),str(path))
            for link in d.links:
                if link.startswith('#'):self.assertIn(link[1:],d.ids,(path,link))
                if path.suffix=='.html' and not link.startswith(('#','/','http')):
                    file,_,frag=link.partition('#');target=path.parent/file
                    self.assertTrue(target.is_file(),str(target))
                    if frag:self.assertIn(frag,Document(target.read_text()).ids)

    def test_standalone_has_extra_teaching_and_no_network_dependencies(self):
        for path,text in self.outputs.items():
            if path.suffix!='.html':continue
            self.assertNotRegex(text,r'<(?:script|link|img)\b[^>]*(?:src|href)="(?:https?:)?//')
            if path.name!='index.html':
                self.assertIn('先把觀念接起來',text)
                self.assertIn('教學 3',text)

    def test_registered_source_evidence_matches_authored_references(self):
        m=check();self.assertEqual(len(m['questions']),320)

    def test_source_references_exclude_wrong_table_locations(self):
        m=check()
        self.assertEqual(m['evidence']['profile']['figure_headings']['494'],[505])
        self.assertEqual(m['evidence']['irqfeat']['figure_headings']['544'],[541])
        self.assertEqual(m['evidence']['cqe']['figure_headings']['109'],[182,183])

    def test_ring_wrap_is_modular_and_not_reversed(self):
        positions=list(range(7,8))+list(range(0,2))
        self.assertEqual(positions,[7,0,1]);self.assertEqual((2-7)%8,len(positions))
        self.assertIn('(2−7+8) mod 8=3',AIDS['doorbells']['example'][0])

    def test_apst_field_encoding_and_units(self):
        raw=(2000<<8)|(3<<3)
        self.assertEqual(raw,0x0007D018)
        self.assertEqual((raw>>8)&0xffffff,2000);self.assertEqual((raw>>3)&0x1f,3)
        self.assertIn('2000 ms',LESSONS['features'][1][1])

    def test_key_counterexamples_are_preserved(self):
        byid={q['id']:q for q in QUESTIONS}
        self.assertIn('不是遮蔽中斷',byid[59]['answers'][4][0])
        self.assertIn('1/2Bh',byid[58]['answers'][7][0]);self.assertIn('1/15h',byid[58]['answers'][7][0])
        self.assertIn('Offline',byid[6]['answers'][1][1])
        self.assertIn('Not Saveable',byid[55]['answers'][7][1])
        self.assertIn('Timestamp Change',byid[63]['answers'][11][1])

    def test_expansion_does_not_apply_log_context_rules_to_timestamps(self):
        byid={q['id']:q for q in QUESTIONS}
        for n in (214,215,216):
            self.assertIn('Origin',byid[n]['answers'][12][1])
            self.assertIn('saved',byid[n]['answers'][14][1].lower())
            self.assertNotIn('reporting context',byid[n]['answers'][12][1])

    def test_corrected_premises_and_operation_lifetimes(self):
        byid={q['id']:q for q in QUESTIONS}
        self.assertIn('crypto', ' '.join(v[1] for v in byid[134]['answers'].values()).lower())
        self.assertIn('extended',byid[153]['answers'][12][1].lower())
        self.assertIn('resume',byid[153]['answers'][14][1].lower())
        self.assertIn('does not provide',byid[273]['answers'][1][1])
        self.assertIn('mask',byid[290]['answers'][1][1])
        self.assertIn('coalescing',byid[290]['answers'][1][1])
        self.assertIn('two total',byid[312]['answers'][1][1].lower())

    def test_prp_example_accounts_for_first_page_offset_and_chaining(self):
        def page_count(size,offset,length):return (offset+length+size-1)//size
        self.assertEqual([page_count(4096,1024,n) for n in (2048,4096,8192)],[1,2,3])
        self.assertEqual((4096-4080)//8,2)
        self.assertEqual(4096//8-1,511)
        self.assertIn('5120',AIDS['pointers']['rows'][2][1][0])

    def test_referenced_topics_have_canonical_links_and_preserve_all_questions(self):
        byid={q['id']:q for q in QUESTIONS}
        for q in QUESTIONS:
            for n in q.get('related',[]):self.assertIn(n,byid)
        self.assertEqual([i for v in VOLUMES for i in range(v[1],v[2]+1)],list(range(1,321)))
        self.assertEqual(len(VOLUMES),26)

    def test_boot_and_fdp_evidence_names_real_source_figures(self):
        e=check()['evidence']
        self.assertEqual(e['bootlog']['figure_headings']['279'],[309])
        self.assertEqual(e['bootlog']['figure_headings']['280'],[310])
        self.assertEqual(e['fdpnvm']['figure_headings']['116'],[79])

if __name__=='__main__':unittest.main()

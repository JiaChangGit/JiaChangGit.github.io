"""Publication contract, source drift, navigation and numerical teaching regressions."""
import json
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from scripts.build_nvme_question_bank import artifacts,QUESTIONS,ROOT
from scripts.nvme_qa_teaching import VOLUMES,AIDS,LESSONS
from scripts.nvme_qa_sources import check
from scripts.nvme_qa_presentation import reading_plan
from scripts.nvme_qa_visuals import VISUALS

class Document(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=[];self.links=[];self.questions=[];self.answers=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if 'data-question' in a:self.questions.append(int(a['data-question']))
        if 'data-answer-section' in a:self.answers.append(int(a['data-answer-section']))

class QuestionBankTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.outputs=artifacts()

    def test_approved_scope_preserves_original_questions_and_supplement(self):
        scope=json.loads((ROOT/'.ai/nvme-question-bank/scope.json').read_text())
        self.assertEqual(scope['status'],'approved');self.assertEqual(scope['question_range'],[1,328])
        self.assertEqual([q['id'] for q in QUESTIONS],list(range(1,329)))
        future=[i for a,b in scope['future_only'].values() for i in range(a,b+1)]
        self.assertEqual(future,[])

    def test_selected_answer_content_and_titles_are_bilingual(self):
        for q in QUESTIONS:
            plan=reading_plan(q)
            selected={1}|{i for section in plan['sections'] for i in section['fields']}
            for pair in [q['title'],plan['prompt'],plan['lead']]+[section['title'] for section in plan['sections']]+[q['answers'][i] for i in selected]:
                self.assertEqual(len(pair),2);self.assertTrue(all(isinstance(x,str) and x.strip() for x in pair))
                self.assertNotRegex(pair[1],r'[\u4e00-\u9fff]')

    def test_all_84_artifacts_match_builder(self):
        self.assertEqual(len(self.outputs),84)
        for path,expected in self.outputs.items():self.assertEqual(path.read_text(),expected,str(path))

    def test_volume_coverage_and_answer_numbering(self):
        for path,text in self.outputs.items():
            doc=Document(text)
            if 'question-bank-index-' in path.name or path.name=='index.html':
                self.assertEqual(doc.questions,[]);continue
            slug=next(v for v in VOLUMES if v[0] in path.name)
            self.assertEqual(doc.questions,list(range(slug[1],slug[2]+1)))
            for article in text.split('<article class="qa-question"')[1:]:
                content=article.split('</article>')[0]
                sections=Document(content).answers
                self.assertEqual(sections,list(range(1,len(sections)+1)))
                self.assertNotIn('data-answer=',content)
                self.assertNotIn('17 個觀察面向',content)

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
        m=check();self.assertEqual(len(m['questions']),328)

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

    def test_data_io_transfer_example_counts_metadata_and_namespace_end(self):
        limit=(1<<5)*(1<<(12+0))
        self.assertEqual(limit,131072)
        self.assertGreater((31+1)*(4096+8),limit)
        max_blocks=limit//(4096+8)
        self.assertEqual(max_blocks,31)
        self.assertEqual(max_blocks*(4096+8),127224)
        self.assertGreater(1000+31,1024-1)
        answer=next(q for q in QUESTIONS if q['id']==321)['answers']
        self.assertIn(str((31+1)*(4096+8)),answer[5][0])
        self.assertIn(str(max_blocks*(4096+8)),answer[6][0])

    def test_atomicity_example_checks_size_and_boundary_independently(self):
        normal,power_fail,boundary=7+1,1+1,15+1
        def guaranteed(start,nlb,unit):
            return nlb+1<=unit and start//boundary==(start+nlb)//boundary
        self.assertEqual([(guaranteed(a,b,normal),guaranteed(a,b,power_fail))
                          for a,b in [(14,1),(15,1),(12,3)]],
                         [(True,True),(False,False),(True,False)])
        answer=next(q for q in QUESTIONS if q['id']==323)['answers'][5][0]
        for raw in ['NAWUN=7','NAWUPF=1','NABSN=NABSPF=15']:
            self.assertIn(raw,answer)

    def test_copy_example_decodes_each_source_and_failure_is_not_a_count(self):
        start=1000;ranges=[]
        for encoded in (3,1):
            ranges.append((start,start+encoded));start+=encoded+1
        self.assertEqual(ranges,[(1000,1003),(1004,1005)])
        self.assertEqual(start-1000,6)
        successful={0,1,3}
        first_unsuccessful=min(set(range(4))-successful)
        self.assertEqual(first_unsuccessful,2)
        self.assertNotEqual(first_unsuccessful,len(successful))
        answer=next(q for q in QUESTIONS if q['id']==327)['answers']
        self.assertIn('1004～1005',answer[4][0]);self.assertIn('DW0=2',answer[6][0])

    def test_lookup_routes_remain_in_existing_questions_with_bilingual_sources(self):
        routes={q['id']:q for q in QUESTIONS if q.get('lookup')}
        self.assertEqual(set(routes),{54,69,118})
        for n,q in routes.items():
            r=q['lookup']
            self.assertTrue(set(r['refs'])<=set(q['refs']))
            for value in [r['title'],r['intro'],r['conclusion']]+r['headers']+[v for row in r['rows'] for v in row]:
                self.assertEqual(len(value),2);self.assertTrue(all(value))
                self.assertNotRegex(value[1],r'[\u4e00-\u9fff]')
            for path,content in self.outputs.items():
                if f'data-question="{n}"' in content:
                    self.assertEqual(content.count(f'id="q-{n:03d}-lookup"'),1)
        self.assertNotIn('LPA.CELP',' '.join(self.outputs.values()))
        self.assertNotIn('LPA.SPEDS',' '.join(self.outputs.values()))

    def test_sanitize_support_example_decodes_admin_region_and_little_endian(self):
        data=bytearray(4096);opcode=0x8c;offset=4*opcode
        self.assertEqual(offset,560);self.assertEqual(offset,0x230)
        data[offset:offset+4]=bytes([0x03,0x00,0x01,0x00])
        entry=int.from_bytes(data[offset:offset+4],'little')
        self.assertEqual(entry,0x00010003)
        self.assertEqual((entry&1,(entry>>1)&1,(entry>>16)&7),(1,1,1))
        wrong=int.from_bytes(data[1024+offset:1028+offset],'little')
        self.assertEqual(wrong&1,0)
        q=next(q for q in QUESTIONS if q['id']==118)
        text=' '.join(c[0] for row in q['lookup']['rows'] for c in row)
        self.assertIn('560～563',text);self.assertIn('00010003h',text)
        self.assertIn('不會建立Sanitize Start',q['answers'][11][0])
        self.assertNotIn('本題比較兩種操作',q['answers'][12][0])

    def test_log_and_feature_lookup_use_different_indexes_and_bit_meanings(self):
        self.assertEqual(4*0x81,0x204)
        self.assertEqual(4*0x06,0x18)
        self.assertEqual((1024//4)-1,255)
        log_entry=1
        self.assertEqual((log_entry&1,(log_entry>>1)&1),(1,0))
        supported_capabilities=5;current_cache=0
        self.assertEqual(tuple((supported_capabilities>>i)&1 for i in (2,1,0)),(1,0,1))
        self.assertEqual(current_cache&1,0)
        byid={q['id']:q for q in QUESTIONS}
        self.assertIn('516～519',' '.join(c[0] for row in byid[69]['lookup']['rows'] for c in row))
        self.assertIn('FSUPP',byid[54]['answers'][3][0])

    def test_referenced_topics_have_canonical_links_and_preserve_all_questions(self):
        byid={q['id']:q for q in QUESTIONS}
        for q in QUESTIONS:
            for n in reading_plan(q)['related']:self.assertIn(n,byid)
        self.assertEqual([i for v in VOLUMES for i in range(v[1],v[2]+1)],list(range(1,329)))
        self.assertEqual(len(VOLUMES),27)

    def test_irrelevant_template_text_is_absent_not_merely_folded(self):
        from scripts.build_nvme_question_bank import question,txt
        byid={q['id']:q for q in QUESTIONS}
        for n in (1,24,31,35,54,118,277):
            for lang in ('zh','en'):
                rendered=question(byid[n],lang,set())
                for i in (8,9,10,11,12,13,14):
                    self.assertNotIn(txt(byid[n]['answers'][i],lang),rendered,(n,i,lang))
                self.assertNotIn('17 perspectives',rendered)
        # Retention is still explained when retention is the actual question.
        for n in (65,130,153,235):
            rendered=question(byid[n],'zh',set())
            for i in (12,13,14):self.assertIn(txt(byid[n]['answers'][i],'zh'),rendered)
        # A namespace profile must not add attachment retention to a WPS question.
        protection=question(byid[172],'zh',set())
        self.assertNotIn('Attach／Detach',protection)
        self.assertIn('WPS2',protection)
        self.assertIn('WPS0',protection)

    def test_flows_replace_prose_and_keep_old_links(self):
        from scripts.build_nvme_question_bank import question,txt
        byid={q['id']:q for q in QUESTIONS}
        for n,v in VISUALS.items():
            for lang in ('zh','en'):
                rendered=question(byid[n],lang,set())
                self.assertEqual(rendered.count(f'id="q-{n:03d}-flow"'),1)
                for i in v['replaces']:
                    self.assertNotIn(txt(byid[n]['answers'][i],lang),rendered)
                for i in range(1,18):
                    self.assertEqual(rendered.count(f'id="q-{n:03d}-a-{i:02d}"'),1)
                for pair in [v['title'],v['intro'],v['conclusion']]+[p for row in v['steps'] for p in row]:
                    self.assertIn(txt(pair,lang),rendered)
        # Alternative PRP2 meanings must never be joined by sequential arrows.
        prp=question(byid[277],'zh',set())
        self.assertEqual(prp.count('class="qa-flow-branch"'),3)
        self.assertNotIn('class="qa-flow-arrow"',prp)

    def test_diagram_examples_check_wait_points_and_boundaries(self):
        def body(n):
            v=VISUALS[n]
            return ' '.join([v['intro'][1],v['conclusion'][1]]+[a[1]+' '+b[1] for a,b in v['steps']])
        queue=body(12)
        self.assertLess(queue.index('Create I/O CQ'),queue.index('Create I/O SQ'))
        self.assertIn('await success on the Admin CQ',queue)
        self.assertIn('before successful completion',body(226))
        self.assertIn('not a mandatory three-step sequence',body(113))
        self.assertIn('Both deadlines start at Enable',body(3))
        self.assertIn('reread it rather than replacing only the final chunk',body(206))
        first_capacity=4096-1024
        self.assertEqual([max(0,n-first_capacity) for n in (2048,4096,8192)],[0,1024,5120])
        for value in ('3072','1024','5120'):self.assertIn(value,body(277))
        self.assertIn(f'{(2000<<8)|(3<<3):08X}h',body(191))

    def test_short_answers_do_not_repeat_editorial_history(self):
        from scripts.build_nvme_question_bank import question
        byid={q['id']:q for q in QUESTIONS}
        for n in (154,211,273):
            rendered=question(byid[n],'zh',set())
            self.assertNotIn('原題',rendered)
            self.assertEqual(rendered.count('data-answer-section='),2)
        # Important initialization error conditions survived removal of the template.
        rendered=question(byid[3],'en',set())
        for text in ('Controller Ready Timeout Exceeded','DNR=0'):
            self.assertIn(text,rendered)

    def test_boot_and_fdp_evidence_names_real_source_figures(self):
        e=check()['evidence']
        self.assertEqual(e['bootlog']['figure_headings']['279'],[309])
        self.assertEqual(e['bootlog']['figure_headings']['280'],[310])
        self.assertEqual(e['fdpnvm']['figure_headings']['116'],[79])

if __name__=='__main__':unittest.main()

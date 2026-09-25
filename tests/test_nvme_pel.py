"""Source coverage, length arithmetic and interpretation regressions for PEL."""
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RID='base-persistent-event-log'

class PersistentEventLogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        c=ROOT/'.ai/nvme-report'
        cls.scope=json.loads((c/'scope.json').read_text())
        cls.figures=[f for f in json.loads((c/'figure-table-register.json').read_text())['entries'] if f['report_id']==RID]
        cls.outputs={a['id']:(ROOT/a['path']).read_text() for a in json.loads((c/'output-contract.json').read_text())['artifacts'] if a['report_id']==RID}

    def test_exact_scope_all_primary_figures_and_unique_lessons(self):
        from scripts.nvme_pel_figures import lesson,guide
        report=next(r for r in self.scope['reports'] if r['id']==RID)
        self.assertEqual(report['primary_scope'],{'NVME-BASE-2.4':['5.2.13.1.14'],'NVME-NVM-CS-1.3':['4.1.4.4']})
        primary={(f['source_id'],int(f['number'])) for f in self.figures if f['role']=='primary'}
        self.assertEqual(primary,{('NVME-BASE-2.4',n) for n in range(232,261)}|{('NVME-NVM-CS-1.3',112)})
        self.assertEqual(len(self.figures),61)
        html=self.outputs['pel-tutorial-html']
        for field in ['takeaway','example','en']:
            self.assertEqual(len({lesson(f)[field] for f in self.figures}),len(self.figures))
        for f in self.figures:
            self.assertEqual(html.count('<!-- figure-table:'+f['id']+' -->'),1)
            self.assertEqual(html.count('id="fields-'+guide(f)['id']+'"'),1)

    def test_independent_record_walk_matches_worked_offsets(self):
        from scripts.nvme_pel_content import UNITS
        example=next(u for u in UNITS if u['key']=='layout')['example']['zh']
        ehl,vsil,el,start=map(int,re.search(r'EHL=(\d+)、VSIL=(\d+)、EL=(\d+)、起點(\d+)',example).groups())
        # Assemble the byte layout independently; vendor bytes belong inside EL.
        header=bytes(ehl+3);vendor=bytes(vsil);payload=bytes(el-vsil)
        record=header+vendor+payload
        self.assertEqual((len(header),len(payload),len(record),start+len(record)),(24,16,44,556))
        self.assertIn(f'下一筆{start+len(record)}',example)
        self.assertIn('總長46',example)
        self.assertEqual((21+3+22)%4,2)  # Per-record padding would change the next offset.

    def test_feature_layout_uses_direct_dword_count_and_optional_dw0(self):
        from scripts.nvme_pel_content import UNITS
        ex=next(u for u in UNITS if u['key']=='features')['example']['zh']
        sfel=int(re.search(r'SFEL=([0-9A-F]+)h',ex)[1],16)
        count=sfel&7;buffer_size=sfel>>16;has_result=(sfel>>3)&1
        cmd_end=4+count*4;buffer_end=cmd_end+buffer_size;total=buffer_end+4*has_result
        self.assertEqual((count,buffer_size,has_result),(3,8,1))
        self.assertEqual((cmd_end,buffer_end,total),(16,24,28))
        self.assertIn(f'={total} bytes',ex)

    def test_namespace_format_index_is_not_a_size_and_offsets_move(self):
        from scripts.nvme_pel_figures import EXAMPLES,GUIDES
        flbas,dps=0x12,0x01
        self.assertEqual((((flbas>>5)&3)<<4)|(flbas&15),2)
        self.assertEqual(((flbas>>4)&1,dps&7,(dps>>3)&1),(1,1,0))
        self.assertIn('byte32',EXAMPLES['N112']['example'])
        self.assertIn('byte26',EXAMPLES['N112']['example'])
        self.assertIn('Delete All保留',str(GUIDES['pel-namespace-fields']))

    def test_namespace_sanitize_does_not_reuse_subsystem_preq_position(self):
        from scripts.nvme_pel_figures import EXAMPLES
        raw=int(re.search(r'SCDW10=([0-9A-F]+)h',EXAMPLES['B454']['example'])[1],16)
        self.assertEqual((raw&7,(raw>>3)&1,(raw>>4)&1,(raw>>10)&1),(4,1,1,1))
        self.assertEqual((raw>>11)&1,0)
        self.assertIn('SOS3',EXAMPLES['B251']['example'])
        self.assertIn('失敗',EXAMPLES['B251']['example'])

    def test_context_existing_and_source_inconsistency_are_not_silently_rewritten(self):
        from scripts.nvme_pel import CONFIG
        from scripts.nvme_pel_figures import GUIDES
        q=next(q for q in CONFIG['questions'] if q['key']=='existing')
        self.assertIn('ACT3已建立',q['answer']['zh'])
        self.assertIn('ACT0',q['answer']['zh'])
        header=str(GUIDES['pel-log-header'])
        self.assertIn('不能自行宣稱SEB bit16',header)
        self.assertIn('FFFFh加1回0',header)

    def test_parity_and_single_forward_document_switch(self):
        from scripts.nvme_pel import ROUTE
        zh,en=self.outputs['pel-zh-md'],self.outputs['pel-en-md']
        for pattern in [r'<!-- claim:([^ ]+) -->',r'<!-- question:([^ ]+) -->']:
            self.assertEqual(re.findall(pattern,zh),re.findall(pattern,en))
        self.assertEqual([r[0] for r in ROUTE],['Base']*5+['NVM'])
        self.assertTrue(all(a[2]<=b[1] for a,b in zip(ROUTE[:5],ROUTE[1:5])))
        self.assertNotIn('id="spec-route"',self.outputs['pel-tutorial-html'])
        for post in [zh,en]:
            self.assertLess(post.index('id="module-pel-extensions"'),post.index('id="spec-route"'))

    def test_entity_mapping_permission_does_not_allow_excluded_transports(self):
        from scripts.validate_nvme_report import forbidden_published
        self.assertIsNone(forbidden_published('Exported NVM Subsystem',RID,self.scope['entries']))
        self.assertIsNotNone(forbidden_published('Fabrics',RID,self.scope['entries']))
        for output in self.outputs.values():
            self.assertIsNone(re.search(r'\b(?:Fabrics|Discovery|NQN)\b',output,re.I))

if __name__=='__main__':unittest.main()

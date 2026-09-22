"""Source coverage, unit conversion and event-acknowledgement regressions."""
import hashlib
import json
import re
import struct
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RID='base-endurance-group-events'

class EnduranceReportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        control=ROOT/'.ai/nvme-report'
        cls.scope=json.loads((control/'scope.json').read_text())
        cls.figures=[f for f in json.loads((control/'figure-table-register.json').read_text())['entries'] if f['report_id']==RID]
        cls.outputs={a['id']:(ROOT/a['path']).read_text() for a in json.loads((control/'output-contract.json').read_text())['artifacts'] if a['report_id']==RID}

    def test_exact_primary_scope_and_dependency_teaching(self):
        from scripts.nvme_endurance_figures import lesson,guide
        report=next(r for r in self.scope['reports'] if r['id']==RID)
        self.assertEqual(report['primary_scope'],{'NVME-BASE-2.4':['5.2.13.1.10','5.2.13.1.15','5.2.30.1.17']})
        self.assertEqual({int(f['number']) for f in self.figures if f['role']=='primary'},{224,225,261,493})
        self.assertEqual(len(self.figures),20)
        html=self.outputs['ege-tutorial-html']
        for field in ['takeaway','example','en']:
            self.assertEqual(len({lesson(f)[field] for f in self.figures}),20)
        for f in self.figures:
            self.assertEqual(html.count('<!-- figure-table:'+f['id']+' -->'),1)
            self.assertIn('id="fields-'+guide(f)['id']+'"',html)
        for field in ['EGCW','EGFEAT','EGRMEDIA','AVSP','AVSPT','PUSED','DID','EE','DUR','DUW','MUW','HRC','HWC','MDIE','NEILE','TEGCAP','UEGCAP']:
            self.assertIn(field,html)

    def test_feature_and_log_encodings_are_not_interchanged(self):
        html=self.outputs['ege-tutorial-html']
        fid18=int(re.search(r'Set Features FID=18h、CDW11=([0-9A-F]{8})h',self.outputs['ege-zh-md'])[1],16)
        self.assertEqual((fid18>>16&255,fid18&65535),(5,7))
        self.assertEqual(5&~0x0d,0)
        self.assertNotEqual(15&~0x0d,0) # Warning bit1 is reserved.
        getlog=0x7f8009
        self.assertEqual((((getlog>>16)+1)*4,(getlog>>15)&1,getlog&255),(512,1,9))
        lsi=7<<16
        self.assertEqual((lsi>>16,lsi&65535),(7,0))
        self.assertIn(f'{lsi:08X}h',html)
        notice=(0x0f<<16)|(6<<8)|2
        self.assertEqual((notice>>16&255,notice>>8&255,notice&7),(15,6,2))
        for value in [fid18,notice]:
            for output in self.outputs.values():self.assertIn(f'{value:08X}h',output)

    def test_list_count_offset_and_dword_padding(self):
        payload=struct.pack('<QHHH',3,1,2,7)+b'\0\0'
        count=struct.unpack_from('<Q',payload)[0]
        ids=[struct.unpack_from('<H',payload,8+2*i)[0] for i in range(count)]
        self.assertEqual(ids,[1,2,7]);self.assertEqual(len(payload),16)
        self.assertEqual(8+2*count,14)
        self.assertEqual(len(payload)//4-1,3)
        self.assertEqual(struct.unpack_from('<H',payload,12)[0],7)
        self.assertEqual(((8+2*9+3)//4)*4,28)
        self.assertEqual(28//4-1,6)
        for literal in ['14 bytes','16 bytes','NUMENT=3']:
            self.assertIn(literal,self.outputs['ege-tutorial-html'])

    def test_rounding_yields_intervals_not_exact_amplification(self):
        billion=10**9
        interval=lambda n:((n-1)*billion+1,n*billion)
        for n in [1,3,5]:
            low,high=interval(n)
            self.assertEqual((low+billion-1)//billion,n)
            self.assertEqual((high+billion-1)//billion,n)
            self.assertEqual((high+1+billion-1)//billion,n+1)
        # Two different underlying write ratios produce the same displayed pair.
        self.assertEqual((3*billion+billion-1)//billion,3)
        self.assertEqual((5*billion+billion-1)//billion,5)
        self.assertNotEqual(5*billion/(3*billion),(4*billion+1)/(2*billion+1))
        html=self.outputs['ege-tutorial-html']
        self.assertIn('2,000,000,001',html)
        self.assertIn('不回報',html)
        self.assertIn('Compare、Copy、Read、Verify',html)
        self.assertIn('Copy、Write',html)

    def test_acknowledgements_and_manufacturing_restore_are_separate(self):
        from scripts.nvme_endurance_figures import GUIDES,EXAMPLES
        service=next(u for u in __import__('scripts.nvme_endurance_content',fromlist=['UNITS']).UNITS if u['key']=='service')
        text=service['claims'][0]['text']['zh']
        for rule in ['LID 09h 且 RAE=0','RAE=1 保留事件','讀取失敗','不能代替','不代表']:
            self.assertIn(rule,text)
        self.assertIn('出廠',EXAMPLES[209]['example'])
        self.assertIn('一般reset',EXAMPLES[209]['example'])
        self.assertIn('註腳9',str(GUIDES['ege-getlog-fields']))
        self.assertIn('不可保存',str(GUIDES['ege-feature-fields']))

    def test_bilingual_parity_and_forward_post_only_route(self):
        from scripts.nvme_endurance import ROUTE
        zh,en=self.outputs['ege-zh-md'],self.outputs['ege-en-md']
        for pattern in [r'<!-- claim:([^ ]+) -->',r'<!-- question:([^ ]+) -->']:
            self.assertEqual(re.findall(pattern,zh),re.findall(pattern,en))
        self.assertTrue(all(a[1]<=b[0] for a,b in zip(ROUTE,ROUTE[1:])))
        self.assertNotIn('id="spec-route"',self.outputs['ege-tutorial-html'])
        for text in [zh,en]:
            self.assertLess(text.index('id="module-ege-service"'),text.index('id="spec-route"'))
        for text in self.outputs.values():
            self.assertIsNone(re.search(r'\b(?:Fabrics|Discovery|NQN)\b',text,re.I))

if __name__=='__main__':unittest.main()

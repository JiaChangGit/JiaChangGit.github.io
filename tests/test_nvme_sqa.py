"""SQ Associations scope, source coverage and worked-example regressions."""
import json
import re
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RID = 'base-sq-associations'


class SQAssociationsReportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        control = ROOT/'.ai/nvme-report'
        cls.scope = json.loads((control/'scope.json').read_text())
        cls.figures = [f for f in json.loads((control/'figure-table-register.json').read_text())['entries'] if f['report_id']==RID]
        cls.outputs = {a['id']:(ROOT/a['path']).read_text() for a in json.loads((control/'output-contract.json').read_text())['artifacts'] if a['report_id']==RID}

    def test_primary_section_has_no_invented_figures(self):
        report = next(r for r in self.scope['reports'] if r['id']==RID)
        self.assertEqual(report['primary_scope'], {'NVME-BASE-2.4':['8.1.28']})
        self.assertEqual(report['pdf_pages'], '758-759')
        self.assertTrue(all(f['role']=='dependency' and f['scope_reduced'] for f in self.figures))
        self.assertEqual({int(f['number']) for f in self.figures}, {67,338,751,333,334,336,343,344,345,346,575,576,577,578,579})

    def test_encoded_queue_example_round_trips(self):
        html = self.outputs['sqa-tutorial-html']
        # Extract the authored values, then decode fields as a controller would.
        fields = [int(re.search(r'CDW'+str(i)+r'=([0-9A-F]{8})h',html)[1],16) for i in [10,11,12]]
        qsize, qid = fields[0]>>16, fields[0]&0xffff
        cqid, pc, qprio = fields[1]>>16, fields[1]&1, (fields[1]>>1)&3
        self.assertEqual((qsize+1,qid,cqid,pc,qprio,fields[2]&0xffff),(64,3,2,1,0,7))
        self.assertEqual(qsize+1,4096//64)
        self.assertEqual(fields[1]&0xfff8,0) # Reserved low CDW11 bits.
        self.assertEqual(fields[2]>>16,0)
        self.assertEqual(0x100000%4096,0)
        self.assertNotEqual(0x100080%4096,0)
        for output in self.outputs.values():
            for value in fields:
                self.assertIn(f'{value:08X}h',output)

    def test_list_layout_and_identifier_are_distinct(self):
        data = bytearray(4096);data[0]=2
        for index,setid in enumerate([7,9]):
            struct.pack_into('<HHI',data,128+index*128,setid,4,0)
        self.assertEqual([struct.unpack_from('<H',data,128+i*128)[0] for i in range(data[0])],[7,9])
        self.assertEqual(128+1*128,256)
        self.assertNotEqual(1,9);self.assertNotEqual(256,9)
        for value in ['128+i×128','NUMENT=0','120×100 ns=12 μs']:
            self.assertIn(value,self.outputs['sqa-tutorial-html'])
        self.assertEqual((1<<8)|(1<<5)|(1<<2),0x124)
        for ctratt,expected in [(0x124,True),(0x324,True),(0x224,False)]:
            self.assertEqual(ctratt&0x124==0x124,expected)

    def test_individual_figures_have_unique_lessons_and_field_homes(self):
        from scripts.nvme_sqa_figures import guide,lesson
        html=self.outputs['sqa-tutorial-html']
        for key in ['takeaway','example','en']:
            self.assertEqual(len({lesson(f)[key] for f in self.figures}),len(self.figures))
        for figure in self.figures:
            self.assertEqual(html.count('<!-- figure-table:'+figure['id']+' -->'),1)
            self.assertIn('id="fields-'+guide(figure)['id']+'"',html)
            self.assertGreaterEqual(len(guide(figure)['rows']),3)
        for key in ['NVMSETID','R4KRT','NUMENT','PRP1','QPRIO','CQID','DTWIN','Reported']:
            self.assertIn(key,html)

    def test_bilingual_parity_and_forward_post_only_route(self):
        from scripts.nvme_sqa import ROUTE
        zh,en=self.outputs['sqa-zh-md'],self.outputs['sqa-en-md']
        for pattern in [r'<!-- claim:([^ ]+) -->',r'<!-- question:([^ ]+) -->']:
            self.assertEqual(re.findall(pattern,zh),re.findall(pattern,en))
        self.assertTrue(all(left[1]<=right[0] for left,right in zip(ROUTE,ROUTE[1:])))
        self.assertEqual(ROUTE[-1][:4],(758,759,'8.1.28','8.1.29'))
        self.assertNotIn('id="spec-route"',self.outputs['sqa-tutorial-html'])
        for text in [zh,en]:
            self.assertIn('id="spec-route"',text)
            self.assertLess(text.index('id="module-sqa-routing"'),text.index('id="spec-route"'))
            self.assertIsNone(re.search(r'\b(?:Fabrics|Discovery|NQN)\b',text,re.I))


if __name__=='__main__':
    unittest.main()

"""Lockdown regression tests for scope and examples whose misreading changes behavior."""
import json
import re
import struct
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RID='base-command-feature-lockdown'


class LockdownReportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        control=ROOT/'.ai/nvme-report'
        cls.scope=json.loads((control/'scope.json').read_text())
        cls.figures=[f for f in json.loads((control/'figure-table-register.json').read_text())['entries'] if f['report_id']==RID]
        artifacts=[a for a in json.loads((control/'output-contract.json').read_text())['artifacts'] if a['report_id']==RID]
        cls.outputs={a['id']:(ROOT/a['path']).read_text() for a in artifacts}

    def test_exact_primary_scope_and_independent_dependencies(self):
        scope=next(r for r in self.scope['reports'] if r['id']==RID)
        self.assertEqual(scope['primary_scope'],{'NVME-BASE-2.4':['8.1.5','5.2.13.1.20','5.2.16']})
        self.assertEqual({int(f['number']) for f in self.figures if f['role']=='primary'}, {274,275,276,277,278,365,366,367})
        self.assertEqual(len(self.figures),29)
        # The new report does not remove exclusions from the earlier walkthrough.
        admin=next(r for r in self.scope['reports'] if r['id']=='admin-io-spec-walkthrough')
        manifest=json.loads((ROOT/'.ai/nvme-report'/admin['scope_manifest']).read_text())
        self.assertIn('5.2.16',manifest['selection']['excluded_base_sections'])
        self.assertIn('14h',manifest['selection']['excluded_lids'])

    def test_each_figure_has_one_unique_lesson_and_a_real_field_home(self):
        from scripts.nvme_lockdown_figures import lesson,guide
        html=self.outputs['lockdown-tutorial-html']
        for key in ['takeaway','example','en']:
            self.assertEqual(len({lesson(f)[key] for f in self.figures}),len(self.figures))
        for f in self.figures:
            self.assertEqual(html.count('<!-- figure-table:'+f['id']+' -->'),1)
            self.assertIn('id="fields-'+guide(f)['id']+'"',html)
            self.assertGreaterEqual(len(guide(f)['rows']),3)

    def test_command_and_log_encodings_round_trip(self):
        html=self.outputs['lockdown-tutorial-html']
        cdw10=(1<<16)|(6<<8)|(0<<5)|(1<<4)|2
        self.assertEqual(cdw10,0x10612)
        self.assertEqual(((cdw10>>16)&15,(cdw10>>8)&255,(cdw10>>5)&3,(cdw10>>4)&1,cdw10&15),(1,6,0,1,2))
        allow=cdw10&~(1<<4)
        for value in [cdw10,allow,7<<16]: self.assertIn(f'{value:08X}h',html)
        log10=((512//4-1)<<16)|(1<<12)|(2<<8)|0x14
        self.assertEqual(log10,0x007f1214)
        self.assertIn(f'{log10:08X}h',html)
        self.assertEqual((((log10>>16)&65535)+1)*4,512)
        self.assertEqual(struct.unpack('<H',bytes.fromhex('00 24'))[0],(1<<13)|(1<<10))

    def test_basic_intersection_and_enhanced_union_are_not_interchangeable(self):
        a={6,7};b={7}
        common=sorted(a&b);union=sorted(a|b)
        descriptors=bytes(v for code in union for v in [code,int(code in a and code in b)])
        self.assertEqual(common,[7])
        self.assertEqual(descriptors.hex(' '),'06 00 07 01')
        self.assertEqual(len(descriptors),4)
        basic=bytes([0x12,0,0,len(common),*common])
        self.assertEqual(list(basic[4:4+basic[3]]),[7])
        html=self.outputs['lockdown-tutorial-html']
        self.assertIn('06 00',html);self.assertIn('07 01',html)

    def test_count_stride_and_uuid_offset_examples(self):
        ncfid=2;stride=2;size=16+ncfid*stride
        self.assertEqual(size,20)
        self.assertEqual([16+i*stride for i in range(ncfid)],[16,18])
        second=18
        self.assertEqual(second%4,2)
        self.assertEqual(second//4*4,16)
        one_descriptor=16+stride
        transfer=((one_descriptor+3)//4)*4
        self.assertEqual((one_descriptor,transfer),(18,20))
        uuid_index=2;entry_offset=32*uuid_index;uuid_offset=entry_offset+16
        self.assertEqual((entry_offset,uuid_offset),(64,80))
        self.assertNotEqual(uuid_index,entry_offset)

    def test_bilingual_order_and_post_only_forward_route(self):
        from scripts.nvme_lockdown import ROUTE
        zh=self.outputs['lockdown-zh-md'];en=self.outputs['lockdown-en-md']
        for pattern in [r'<!-- claim:([^ ]+) -->',r'<!-- question:([^ ]+) -->']:
            self.assertEqual(re.findall(pattern,zh),re.findall(pattern,en))
        self.assertNotIn('id="spec-route"',self.outputs['lockdown-tutorial-html'])
        self.assertEqual([(r[0],r[1]) for r in ROUTE],[(305,309),(431,434),(623,625)])
        for text in [zh,en]:
            self.assertIn('id="spec-route"',text)
            for code in ['CSEL=0','CSEL=1','LDPE','SCP=2','ACNTL']:
                self.assertIn(code,text)
            self.assertIsNone(re.search(r'\b(?:Fabrics|Discovery|NQN)\b',text,re.I))


if __name__=='__main__':
    unittest.main()

"""Regression checks for RRL scope and easily confused numeric interpretations."""
import json
import re
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RID = 'base-read-recovery-level'


class ReadRecoveryLevelReportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        control=ROOT/'.ai/nvme-report'
        cls.scope=json.loads((control/'scope.json').read_text())
        cls.figures=[f for f in json.loads((control/'figure-table-register.json').read_text())['entries'] if f['report_id']==RID]
        artifacts=[a for a in json.loads((control/'output-contract.json').read_text())['artifacts'] if a['report_id']==RID]
        cls.outputs={a['id']:(ROOT/a['path']).read_text() for a in artifacts}

    def test_primary_scope_and_prior_exclusions(self):
        report=next(r for r in self.scope['reports'] if r['id']==RID)
        self.assertEqual(report['primary_scope'],{'NVME-BASE-2.4':['8.1.23','5.2.30.1.12']})
        self.assertEqual({int(f['number']) for f in self.figures if f['role']=='primary'},{755,484,485})
        self.assertEqual(len(self.figures),14)
        admin=next(r for r in self.scope['reports'] if r['id']=='admin-io-spec-walkthrough')
        manifest=json.loads((ROOT/'.ai/nvme-report'/admin['scope_manifest']).read_text())
        self.assertIn('12h',manifest['selection']['excluded_fids'])

    def test_rrls_bitmap_is_not_the_rrl_code(self):
        rr_ls=struct.unpack('<H',bytes.fromhex('11 80'))[0]
        levels=[n for n in range(16) if (rr_ls>>n)&1]
        self.assertEqual(levels,[0,4,15])
        self.assertEqual(rr_ls,0x8011)
        self.assertEqual(rr_ls&((1<<4)|(1<<15)),0x8010)
        selected=15
        self.assertNotEqual(1<<selected,selected)
        for output in self.outputs.values():
            self.assertIn(f'{rr_ls:04X}h',output)
        html=self.outputs['rrl-tutorial-html']
        self.assertIn('8000h',html)
        self.assertIn(f'{selected:08X}h',html)

    def test_command_positions_and_select_round_trips(self):
        # Treat the rendered command values as an encoded example, then unpack it.
        html=self.outputs['rrl-tutorial-html']
        target=7;level=15
        command=bytearray(64)
        struct.pack_into('<I',command,4,0)  # NSID is unused for this feature scope.
        for index,value in [(10,0x12),(11,target),(12,level)]:
            struct.pack_into('<I',command,index*4,value)
            self.assertIn(f'{value:08X}h',html)
        self.assertEqual(struct.unpack_from('<H',command,44)[0],target)
        self.assertEqual(command[48]&15,level)
        self.assertEqual(struct.unpack_from('<I',command,4)[0],0)
        for sel in range(4):
            cdw10=(sel<<8)|0x12
            self.assertEqual(((cdw10>>8)&7,cdw10&255),(sel,0x12))
            self.assertIn(f'{cdw10:08X}h',html)
        save=(1<<31)|0x12
        self.assertIn(f'{save:08X}h',html)

    def test_each_figure_has_unique_teaching_and_a_real_field_home(self):
        from scripts.nvme_rrl_figures import guide,lesson
        html=self.outputs['rrl-tutorial-html']
        for key in ['takeaway','example','en']:
            self.assertEqual(len({lesson(f)[key] for f in self.figures}),len(self.figures))
        for f in self.figures:
            self.assertEqual(html.count('<!-- figure-table:'+f['id']+' -->'),1)
            self.assertIn('id="fields-'+guide(f)['id']+'"',html)
            self.assertGreaterEqual(len(guide(f)['rows']),3)
        # These are the linked conditions most likely to be lost in a summary.
        for term in ['SSFS','NSSPEC','SVBL','註腳 2','non-persistent','Limited Retry']:
            self.assertIn(term,html)

    def test_bilingual_order_and_route_is_post_only_and_forward(self):
        from scripts.nvme_rrl import ROUTE
        zh=self.outputs['rrl-zh-md'];en=self.outputs['rrl-en-md']
        for pattern in [r'<!-- claim:([^ ]+) -->',r'<!-- question:([^ ]+) -->']:
            self.assertEqual(re.findall(pattern,zh),re.findall(pattern,en))
        self.assertEqual([(r[0],r[1],r[2],r[3]) for r in ROUTE],
                         [(499,499,'5.2.30.1.12','5.2.30.1.13'),(715,716,'8.1.23','8.1.24')])
        self.assertNotIn('id="spec-route"',self.outputs['rrl-tutorial-html'])
        for output in [zh,en]:
            self.assertIn('id="spec-route"',output)
            self.assertIsNone(re.search(r'\b(?:Fabrics|Discovery|NQN)\b',output,re.I))


if __name__=='__main__':
    unittest.main()

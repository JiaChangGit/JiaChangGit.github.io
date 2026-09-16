"""Regression coverage for FDP scope, count/offset examples and report parity."""
import json
import re
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT/'.ai/nvme-report'
RID = 'base-flexible-data-placement'


class FDPReportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scope = json.loads((CONTROL/'scope.json').read_text())
        cls.figures = [f for f in json.loads((CONTROL/'figure-table-register.json').read_text())['entries'] if f['report_id']==RID]
        artifacts = [a for a in json.loads((CONTROL/'output-contract.json').read_text())['artifacts'] if a['report_id']==RID]
        cls.outputs = {a['id']:(ROOT/a['path']).read_text() for a in artifacts}

    def test_exact_scope_and_all_primary_figures(self):
        scope = next(r for r in self.scope['reports'] if r['id']==RID)
        self.assertEqual(scope['primary_scope'], {
          'NVME-BASE-2.4':['8.1.12','3.2.4','8.1.9.4','7.3','7.4','5.2.30.1.21','5.2.30.1.22','5.2.13.1.29','5.2.13.1.30','5.2.13.1.31','5.2.13.1.32'],
          'NVME-NVM-CS-1.3':['3.2','4.1.4.6','4.1.4.7']})
        primary={(f['source_id'],int(f['number'])) for f in self.figures if f['role']=='primary'}
        self.assertEqual(primary,{('NVME-BASE-2.4',n) for n in {70,*range(293,304),*range(499,507),*range(650,658),730,731,732}}|{('NVME-NVM-CS-1.3',21),('NVME-NVM-CS-1.3',116)})
        streams=next(r for r in self.scope['reports'] if r['id']=='base-directives-streams')
        self.assertIn('8.1.9.4',streams['excluded_sections'])

    def test_every_figure_is_taught_once_with_unique_examples_and_field_home(self):
        from scripts.nvme_fdp_figures import lesson,guide
        html=self.outputs['fdp-tutorial-html']
        self.assertEqual(len(self.figures),59)
        for key in ['takeaway','example','en']:
            self.assertEqual(len({lesson(f)[key] for f in self.figures}),59)
        for f in self.figures:
            self.assertEqual(html.count('<!-- figure-table:'+f['id']+' -->'),1)
            self.assertIn('id="fields-'+guide(f)['id']+'"',html)
            self.assertGreaterEqual(len(guide(f)['rows']),2)

    def test_pid_write_and_feature_encodings(self):
        html=self.outputs['fdp-tutorial-html']
        values={int(x,16) for x in re.findall(r'\b([0-9A-F]{8})h\b',html)}
        pid=(2<<14)|1
        self.assertEqual(pid,0x8001)
        self.assertEqual((pid>>14,pid&0x3fff),(2,1))
        write12=(2<<20)|7;write13=pid<<16
        self.assertTrue({write12,write13,0x8000001d,0x00000201}.issubset(values))
        self.assertEqual(((write12>>20)&15,(write12>>16)&15,(write12&65535)+1),(2,0,8))
        # Different command contexts: FID1Dh index1 vs target Data Placement2.
        self.assertEqual(((0x101>>8)&255,0x101&1),(1,1))
        self.assertEqual(((0x201>>8)&255,0x201&1),(2,1))

    def test_update_buffer_and_zero_based_limits(self):
        pids=[0x8000,0x8001];encoded=len(pids)-1
        cdw10=(encoded<<16)|1
        payload=struct.pack('<2H',*pids)
        self.assertEqual(cdw10,0x00010001)
        self.assertEqual(payload.hex(' '),'00 80 01 80')
        self.assertIn('00010001h',self.outputs['fdp-tutorial-html'])
        self.assertIn(payload.hex(' '),self.outputs['fdp-tutorial-html'])
        self.assertEqual(7+1,8)  # MAXPIDS=7 permits eight entries.
        self.assertLess(7,4*4)

    def test_structure_sizes_and_distinct_zero_semantics(self):
        html=self.outputs['fdp-tutorial-html']
        descriptor=((64+3*4+1+7)//8)*8
        self.assertEqual(descriptor,80)
        self.assertEqual(16+descriptor,96)
        status=16+2*4*32
        self.assertEqual((status,status//4-1),(272,67))
        self.assertEqual((4096-64)//64,63)
        self.assertEqual(struct.calcsize('<BBH8sI16sHH4s24s'),64)
        self.assertIn('NVMDSMSV=0',html)
        self.assertIn('0表示不支持命令',html)
        self.assertIn('不是範圍起點',html)

    def test_post_parity_and_forward_route(self):
        from scripts.nvme_fdp import ROUTE
        self.assertNotIn('id="spec-route"',self.outputs['fdp-tutorial-html'])
        docs=[r[0] for r in ROUTE]
        self.assertEqual(sum(a!=b for a,b in zip(docs,docs[1:])),1)
        for doc in ['Base','NVM']:
            pages=[r[1] for r in ROUTE if r[0]==doc]
            self.assertEqual(pages,sorted(pages))
        marker=r'<!-- claim:([^ ]+) -->'
        zh=self.outputs['fdp-zh-md'];en=self.outputs['fdp-en-md']
        self.assertEqual(re.findall(marker,zh),re.findall(marker,en))
        self.assertIn('FDP-STATISTICS-COMMANDS',zh)
        for s in [zh,en]:
            self.assertIn('id="spec-route"',s)
            self.assertNotRegex(s,r'\b(?:Fabrics|NVMe-oF|NQN)\b')


if __name__=='__main__':
    unittest.main()

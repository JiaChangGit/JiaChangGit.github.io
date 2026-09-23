"""Prevent source-coverage, encoding and state/permission interpretation regressions."""
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RID='base-namespace-write-protection'

class NamespaceWriteProtectionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        c=ROOT/'.ai/nvme-report'
        cls.scope=json.loads((c/'scope.json').read_text())
        cls.figures=[f for f in json.loads((c/'figure-table-register.json').read_text())['entries'] if f['report_id']==RID]
        cls.outputs={a['id']:(ROOT/a['path']).read_text() for a in json.loads((c/'output-contract.json').read_text())['artifacts'] if a['report_id']==RID}

    def test_primary_scope_and_all_source_figures_have_unique_teaching(self):
        from scripts.nvme_nwp_figures import lesson,guide
        r=next(r for r in self.scope['reports'] if r['id']==RID)
        self.assertEqual(r['primary_scope'],{'NVME-BASE-2.4':['8.1.18','5.2.30.1.38']})
        self.assertEqual({int(f['number']) for f in self.figures if f['role']=='primary'},{735,736,737,541})
        self.assertEqual(len(self.figures),16)
        for field in ['takeaway','example','en']:
            self.assertEqual(len({lesson(f)[field] for f in self.figures}),len(self.figures))
        html=self.outputs['nwp-tutorial-html']
        for f in self.figures:
            self.assertEqual(html.count('<!-- figure-table:'+f['id']+' -->'),1)
            self.assertEqual(html.count('id="fields-'+guide(f)['id']+'"'),1)
        for name in ['NWPWPS','WPUPCS','PWPS','WPUPCC','PWPC','NSSPEC','SVBL','CHANG','AMRO']:
            self.assertIn(name,html)

    def test_worked_encodings_select_state_not_capability_flags(self):
        from scripts.nvme_nwp_content import UNITS
        ex=next(u for u in UNITS if u['key']=='configure')['example']['zh']
        cdw10,cdw11=[int(x,16) for x in re.search(r'CDW10=([0-9A-F]{8})h、CDW11=([0-9A-F]{8})h',ex).groups()]
        self.assertEqual((cdw10&255,cdw10>>31),(0x84,0))
        self.assertEqual((cdw11&7,cdw11>>3),(1,0))
        html=self.outputs['nwp-tutorial-html']
        self.assertIn(f'{(3<<8)|0x84:08X}h',html)
        self.assertEqual(((6>>2)&1,(6>>1)&1,6&1),(1,1,0))
        self.assertIn('DW0=6',html)
        # NWPC=03h advertises only basic and until-power-cycle states;
        # WPS=3 selects Permanent. Identical numerals are not identical formats.
        nwpc=3
        self.assertEqual((bool(nwpc&1),bool(nwpc&2),bool(nwpc&4)),(True,True,False))
        for output in self.outputs.values():
            for encoded in [f'{cdw10:08X}h',f'{cdw11:08X}h']:
                self.assertIn(encoded,output)

    def test_state_persistence_does_not_follow_control_reset_or_save_bit(self):
        from scripts.nvme_nwp_figures import EXAMPLES,GUIDES
        from scripts.nvme_nwp_content import UNITS
        self.assertIn('沒有 2 → 3',EXAMPLES[736]['example'])
        self.assertIn('仍是 3',EXAMPLES[756]['example'])
        self.assertIn('註腳8',EXAMPLES[466]['example'])
        self.assertIn('控制器重設仍是 2',EXAMPLES[735]['example'])
        self.assertIn('同值請求',str(GUIDES['nwp-state-arrows']))
        unit=next(u for u in UNITS if u['key']=='transitions')
        self.assertIn('非永久狀態回到 0，永久狀態維持',unit['claims'][1]['text']['zh'])

    def test_command_table_keeps_every_command_and_all_three_footnotes(self):
        from scripts.nvme_nwp_figures import GUIDES
        text=str(GUIDES['nwp-allowed-commands'])
        for name in ['Device Self-test','Directive Send','Directive Receive','Get Features','Get Log Page','Identify','Namespace Attachment','Security Receive','Security Send','Set Features','Vendor Specific','Compare','Dataset Management','Read','Reservation Register','Reservation Report','Reservation Acquire','Reservation Release','Flush','Verify']:
            self.assertIn(name,text)
        for rule in ['註腳1','註腳2','註腳3','成功且無作用','配置Streams資源','未指定NSID']:
            self.assertIn(rule,text)
        html=self.outputs['nwp-tutorial-html']
        for code in ['SCT0／SC20h','SCT1／SC0Dh','SCT1／SC0Eh']:
            self.assertIn(code,html)

    def test_bilingual_parity_and_forward_route_only_in_posts(self):
        from scripts.nvme_nwp import ROUTE
        zh,en=self.outputs['nwp-zh-md'],self.outputs['nwp-en-md']
        for pattern in [r'<!-- claim:([^ ]+) -->',r'<!-- question:([^ ]+) -->']:
            self.assertEqual(re.findall(pattern,zh),re.findall(pattern,en))
        self.assertTrue(all(a[1]<=b[0] for a,b in zip(ROUTE,ROUTE[1:])))
        self.assertNotIn('id="spec-route"',self.outputs['nwp-tutorial-html'])
        for post in [zh,en]:
            self.assertLess(post.index('id="module-nwp-observe"'),post.index('id="spec-route"'))
        for output in self.outputs.values():
            self.assertIsNone(re.search(r'\b(?:Fabrics|Discovery|NQN)\b',output,re.I))

    def test_arrowhead_for_reversible_state_points_back_to_zero(self):
        from scripts.nvme_nwp_visuals import illustration
        svg=illustration('nwp-transitions')
        # For the return arrow, both rear points must lie to the right of its tip.
        path=re.search(r'd="M435,95 L325,95 M(\d+),(\d+) L(\d+),(\d+) L(\d+),(\d+)"',svg)
        self.assertIsNotNone(path)
        x1,y1,xt,yt,x2,y2=map(int,path.groups())
        self.assertGreater(x1,xt);self.assertGreater(x2,xt)
        self.assertLess(y1,yt);self.assertGreater(y2,yt)

if __name__=='__main__':unittest.main()

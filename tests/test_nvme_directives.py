"""Regression checks for the requested scope and the worked command examples."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / '.ai/nvme-report'
RID = 'base-directives-streams'


class DirectivesReportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scope = json.loads((CONTROL/'scope.json').read_text())
        cls.figures = [f for f in json.loads((CONTROL/'figure-table-register.json').read_text())['entries'] if f['report_id']==RID]
        cls.artifacts = [a for a in json.loads((CONTROL/'output-contract.json').read_text())['artifacts'] if a['report_id']==RID]
        cls.outputs = {a['id']:(ROOT/a['path']).read_text() for a in cls.artifacts}

    def test_scope_does_not_inherit_admin_io_exclusions(self):
        selected = next(r for r in self.scope['reports'] if r['id']==RID)
        self.assertEqual(selected['primary_scope'], {
            'NVME-BASE-2.4':['8.1.9','5.2.7','5.2.8','5.2.30.1.35'],
            'NVME-NVM-CS-1.3':['5.13']})
        self.assertEqual(set(selected['excluded_sections']), {'8.1.9.4','5.2.30.1.35.2'})
        primary = {(f['source_id'],int(f['number'])) for f in self.figures if f['role']=='primary'}
        self.assertEqual(primary, {('NVME-BASE-2.4',n) for n in set(range(181,187))|{537,538}|set(range(702,716))})
        self.assertFalse(any(f['section'].startswith(('8.1.9.4','5.2.30.1.35.2')) for f in self.figures))

    def test_each_figure_has_unique_teaching_and_a_valid_field_home(self):
        from scripts.nvme_directives_figures import lesson, guide
        html = self.outputs['streams-tutorial-html']
        self.assertEqual(len(self.figures),37)
        self.assertEqual(len({lesson(f)['example'] for f in self.figures}),37)
        self.assertEqual(len({lesson(f)['takeaway'] for f in self.figures}),37)
        for f in self.figures:
            self.assertIn('figure-table:'+f['id'],html)
            self.assertIn('id="fields-'+guide(f)['id']+'"',html)
            self.assertGreaterEqual(len(guide(f)['rows']),2)
            self.assertTrue(lesson(f)['en'])

    def test_live_spec_route_is_post_only_and_forward(self):
        self.assertNotIn('id="spec-route"',self.outputs['streams-tutorial-html'])
        for ident in ['streams-zh-md','streams-en-md']:
            text=self.outputs[ident]
            self.assertIn('id="spec-route"',text)
            pages = re.findall(r'R\d · (Base|NVM) PDF (\d+)(?:–(\d+))?',text)
            self.assertEqual(pages,[('Base','227','228'),('Base','534','536'),('Base','642','646'),('Base','646','653'),('NVM','175','')])
        marker=r'<!-- claim:([^ ]+) -->'
        self.assertEqual(re.findall(marker,self.outputs['streams-zh-md']),re.findall(marker,self.outputs['streams-en-md']))

    def test_enable_and_write_examples_decode_to_distinct_field_contexts(self):
        html=self.outputs['streams-tutorial-html']
        values={int(s,16) for s in re.findall(r'\b([0-9A-F]{8})h\b',html)}
        enable_outer=0x00000001; enable_target=0x00000101
        write12=0x00100007; write13=0x00070000; release=0x00070101
        self.assertTrue({enable_outer,enable_target,write12,write13,release}.issubset(values))
        self.assertEqual(((enable_outer>>8)&255,enable_outer&255),(0,1))
        self.assertEqual(((enable_target>>8)&255,enable_target&1),(1,1))
        self.assertEqual(((write12>>20)&15,(write12>>16)&15,(write12&65535)+1),(1,0,8))
        self.assertEqual(write13>>16,7)
        self.assertEqual((release>>16,(release>>8)&255,release&255),(7,1,1))

    def test_size_units_and_status_offsets_are_consistent(self):
        block_bytes=4096; sws=8; sgs=4
        self.assertEqual(sws*block_bytes,32*1024)
        self.assertEqual(sgs*sws*block_bytes,128*1024)
        self.assertEqual(136%sws,0)
        self.assertNotEqual(136%(sgs*sws),0)
        # OSC plus four two-byte identifiers needs ten bytes; request whole Dwords.
        transfer_dwords=(2+4*2+3)//4
        self.assertEqual(transfer_dwords-1,2)
        # A third entry starts at offset 6, independent of its identifier value.
        self.assertEqual(2+(3-1)*2,6)
        self.assertEqual(11*4,44)
        self.assertIn('002Ch',self.outputs['streams-tutorial-html'])


if __name__ == '__main__':
    unittest.main()

"""Boundary checks and a deliberately incorrect published-result regression."""
import unittest
from scripts.validate_pcie_examples import result_tokens,validate_case

class TeachingArithmeticTest(unittest.TestCase):
    def test_one_dw_rejects_last_enable(self):
        with self.assertRaises(ValueError):result_tokens('byte_enable',dict(length_dw=1,first_be=15,last_be=1))
    def test_ltr_ignored_requirement_is_not_zero(self):
        self.assertEqual(result_tokens('ltr',dict(requirement=0,value=99,scale=7)),[])
        with self.assertRaises(ValueError):result_tokens('ltr',dict(requirement=1,value=99,scale=7))
    def test_vf_identity_uses_unsigned_sixteen_bits(self):
        self.assertEqual(result_tokens('vf_rid',dict(pf=65534,first=1,stride=2,count=2)),['FFFFh','0001h'])
    def test_wrong_published_offset_is_detected(self):
        case=dict(section='lane',model='lane',inputs=dict(lane=2,control_base=8,stride=4,status_delta=2))
        self.assertEqual(validate_case(case,'<section id="lane"><p>C+10h, C+12h</p></section>'),[])
        self.assertEqual(validate_case(case,'<section id="lane"><p>C+10h, C+14h</p></section>'),['12h'])

class PacketLayoutTest(unittest.TestCase):
    def setUp(self):
        self.inputs=dict(length_dw=2,address=0x80001000,requester_id=0x0300,
                         first_be=12,last_be=3,payload=[0xA0,0xA1,0xA2,0xA3,0xB0,0xB1,0xB2,0xB3])
    def test_wrong_fm_ohc_advertisement_is_detected(self):
        case=dict(section='packet-layout',model='partial_write_layout',inputs=self.inputs)
        text=('<section id="packet-layout"><pre>'
              '40 00 00 02 03 00 00 3C 80 00 10 00 A0 A1 A2 A3 B0 B1 B2 B3'
              '</pre><pre>'
              '40 01 00 02 03 00 00 00 80 00 10 00 00 00 00 3C A0 A1 A2 A3 B0 B1 B2 B3'
              '</pre><p>20 bytes; 24 bytes</p></section>')
        self.assertEqual(validate_case(case,text),[])
        self.assertTrue(validate_case(case,text.replace('40 01 00 02','40 00 00 02')))
    def test_truncated_payload_is_rejected(self):
        self.inputs['payload'].pop()
        with self.assertRaises(ValueError):result_tokens('partial_write_layout',self.inputs)
    def test_request_crossing_4kb_is_rejected(self):
        self.inputs['address']=0x80001FFC
        with self.assertRaises(ValueError):result_tokens('partial_write_layout',self.inputs)

class VirtualChannelSetupTest(unittest.TestCase):
    def setUp(self):
        self.inputs=dict(resource=1,extended_count=1,vc_id=1,tc_map=0x80,
                         left_capability=0x180,right_capability=0x200)
    def test_status_misread_as_lower_halfword_is_detected(self):
        case=dict(section='vc-enable',model='vc_setup',inputs=self.inputs)
        text=('<section id="vc-enable"><p>1A0h 1A6h 220h 226h '
              '01000080h 81000080h 7Fh</p></section>')
        self.assertEqual(validate_case(case,text),[])
        self.assertEqual(validate_case(case,text.replace('1A6h','1A4h')),['1A6h'])
    def test_tc0_cannot_be_assigned_to_extended_vc(self):
        self.inputs['tc_map']=0x81
        with self.assertRaises(ValueError):result_tokens('vc_setup',self.inputs)
    def test_absent_resource_cannot_be_addressed(self):
        self.inputs['extended_count']=0
        with self.assertRaises(ValueError):result_tokens('vc_setup',self.inputs)

if __name__=='__main__':unittest.main()

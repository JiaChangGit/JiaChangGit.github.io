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

if __name__=='__main__':unittest.main()

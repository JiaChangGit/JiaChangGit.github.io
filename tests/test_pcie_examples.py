"""Boundary checks and a deliberately incorrect published-result regression."""
import unittest
from scripts.validate_pcie_examples import result_tokens,validate_case,polling_gate_rows,differential_voltage_case,rx_calibration_case

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

class FiniteCreditTimelineTest(unittest.TestCase):
    def setUp(self):
        self.inputs=dict(payload_bytes=20,consumed=[254,4094],limit=[255,4094],
                         updates=[[0,0],[1,2]],finite=True)
    def test_ack_cannot_return_credit(self):
        rows=[('wait','PH=FEh; PD=FFEh','PH=FFh; PD=FFEh','1 PH / 0 PD'),
              ('ready','PH=FEh; PD=FFEh','PH=00h; PD=000h','2 PH / 2 PD'),
              ('sent','PH=FFh; PD=000h','PH=00h; PD=000h','1 PH / 0 PD'),
              ('acked','PH=FFh; PD=000h','PH=00h; PD=000h','1 PH / 0 PD'),
              ('updated','PH=FFh; PD=000h','PH=01h; PD=002h','2 PH / 2 PD')]
        text=''.join('<tr data-fc-stage="'+r[0]+'"><td>'+'</td><td>'.join(r[1:])+'</td></tr>' for r in rows)
        case=dict(section='credit-cycle',model='finite_fc',inputs=self.inputs)
        self.assertEqual(validate_case(case,text),[])
        wrong=text.replace('data-fc-stage="acked"><td>PH=FFh; PD=000h',
                           'data-fc-stage="acked"><td>PH=FEh; PD=FFEh')
        self.assertTrue(any(e.startswith('acked:') for e in validate_case(case,wrong)))
    def test_tlp_requiring_more_data_credit_is_blocked(self):
        self.inputs['payload_bytes']=36
        with self.assertRaises(ValueError):result_tokens('finite_fc',self.inputs)
    def test_infinite_advertisement_needs_a_different_model(self):
        self.inputs['finite']=False
        with self.assertRaises(ValueError):result_tokens('finite_fc',self.inputs)

class FlitDlpTeachingTest(unittest.TestCase):
    def setUp(self):
        self.inputs=dict(payload=[0x51,0x2a,0x80,0,0,0],selective=[0x1d,0x29,0x80,0,0,0])
    def test_high_sequence_bits_and_selective_target_are_decoded(self):
        tokens=result_tokens('flit_dlp',self.inputs)
        self.assertEqual(tokens,['51 2A 80 00 00 00','00b','12Ah',
                                 '1D 29 80 00 00 00','11b','129h','12Ah'])
        # A correct sequence elsewhere must not hide a wrong Nak-row target.
        text=('<tr data-dlp-case="payload"><td>51 2A 80 00 00 00; 00b; 12Ah</td></tr>'
              '<tr data-dlp-case="selective"><td>1D 29 80 00 00 00; 11b; 129h; 12Ah</td></tr>')
        case=dict(section='dlp-replay',model='flit_dlp',inputs=self.inputs)
        self.assertEqual(validate_case(case,text),[])
        self.assertTrue(validate_case(case,text.replace('11b; 129h; 12Ah','11b; 129h; 129h')))
    def test_reserved_usage_does_not_decode_as_payload(self):
        self.inputs['payload'][0]=0x91
        with self.assertRaises(ValueError):result_tokens('flit_dlp',self.inputs)
    def test_truncated_dlp_is_rejected(self):
        self.inputs['selective'].pop()
        with self.assertRaises(ValueError):result_tokens('flit_dlp',self.inputs)

class PollingGateTeachingTest(unittest.TestCase):
    def setUp(self):
        self.inputs=dict(active=[dict(id='active-ready',point='A2',sent=1024,rx=[32,31])],
                         config=[dict(id='config-wait',point='B0',before=6,after=15,rx=[8,8])])
    def test_total_sent_does_not_replace_post_receive_count(self):
        rows=polling_gate_rows(self.inputs)
        self.assertEqual(rows['config-wait'],['B0','6','15','21','8 / 8','Polling.Configuration'])
        text=''.join('<tr data-polling-stage="'+name+'">'+''.join('<td>'+cell+'</td>' for cell in cells)+'</tr>' for name,cells in rows.items())
        case=dict(section='polling-gates',model='polling_gates',inputs=self.inputs)
        self.assertEqual(validate_case(case,text),[])
        self.assertTrue(validate_case(case,text.replace('<td>Polling.Configuration</td></tr>','<td>Configuration</td></tr>')))
    def test_one_short_lane_blocks_the_normal_active_path(self):
        self.inputs['active'][0]['rx']=[32,7]
        self.assertEqual(polling_gate_rows(self.inputs)['active-ready'][-1],'Polling.Active')
        self.inputs['active'][0]['rx']=[32,8]
        self.inputs['active'][0]['sent']=1023
        self.assertEqual(polling_gate_rows(self.inputs)['active-ready'][-1],'Polling.Active')
    def test_configuration_accepts_any_qualifying_detected_lane(self):
        self.inputs['config'][0].update(after=16,rx=[8,0])
        self.assertEqual(polling_gate_rows(self.inputs)['config-wait'][-1],'Configuration')

class DifferentialVoltageTeachingTest(unittest.TestCase):
    def setUp(self):
        self.inputs=dict(high_mv=[825,375],low_mv=[375,825])
    def test_factor_of_two_error_is_not_hidden_by_other_correct_values(self):
        rows,summary=differential_voltage_case(self.inputs)
        text='<section id="voltage-case">'+''.join('<tr data-voltage-state="'+name+'">'+''.join('<td>'+v+'</td>' for v in values)+'</tr>' for name,values in rows.items())+'<p>'+'; '.join(summary)+'</p></section>'
        case=dict(section='voltage-case',model='differential_voltage',inputs=self.inputs)
        self.assertEqual(validate_case(case,text),[])
        self.assertTrue(validate_case(case,text.replace('<td>+450</td>','<td>+900</td>')))
    def test_symmetric_shortcut_rejects_asymmetric_levels(self):
        self.inputs['low_mv']=[400,800]
        with self.assertRaises(ValueError):differential_voltage_case(self.inputs)
    def test_common_mode_is_average_not_difference(self):
        rows,summary=differential_voltage_case(self.inputs)
        self.assertEqual(rows['high'],['H','825','375','+450','600'])
        self.assertEqual(rows['low'],['L','375','825','−450','600'])
        self.assertEqual(summary,['450 mVPP','900 mVPP','600 mV'])

class ReceiverCalibrationTeachingTest(unittest.TestCase):
    def setUp(self):
        self.inputs=dict(gt_s=16,receiver_type='non-root',eh=['14.5','15.0','15.5','15.2','14.8'],
                         ew=['18.5','18.8','18.9','18.6','18.95'])
    def test_wrong_mean_is_detected_in_its_own_row(self):
        rows,summary=rx_calibration_case(self.inputs)
        self.assertEqual(rows['ew'][2:],["18.75 ps","18.25–19.25 ps"])
        self.assertEqual(rows['eh'][2:],["15 mVPP","13.5–16.5 mVPP"])
        text='<section id="rx-calibration">'+''.join('<tr data-rx-check="'+name+'">'+''.join('<td>'+v+'</td>' for v in values)+'</tr>' for name,values in rows.items())+'<p>'+'; '.join(summary)+'</p></section>'
        case=dict(section='rx-calibration',model='rx_calibration',inputs=self.inputs)
        self.assertEqual(validate_case(case,text),[])
        self.assertTrue(validate_case(case,text.replace('<td>18.75 ps</td>','<td>18.95 ps</td>')))
    def test_four_measurements_are_insufficient(self):
        self.inputs['eh'].pop()
        with self.assertRaises(ValueError):rx_calibration_case(self.inputs)
    def test_the_same_ui_model_cannot_be_reused_at_64_gt(self):
        self.inputs['gt_s']=64
        with self.assertRaises(ValueError):rx_calibration_case(self.inputs)

if __name__=='__main__':unittest.main()

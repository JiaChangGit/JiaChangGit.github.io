"""Boundary checks and a deliberately incorrect published-result regression."""
import unittest
from scripts.validate_pcie_examples import result_tokens,validate_case,polling_gate_rows,differential_voltage_case,rx_calibration_case,margin_command_rows,power_budget_case,dpa_profile_case,ltr_switch_case,tph_table_case,ptm_dialog_case,ptm_config_case

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

class MarginCommandTeachingTest(unittest.TestCase):
    def setUp(self):
        self.inputs=dict(gt_s=16,port_type='upstream',receiver=6,caps=21,
                         timing_steps=32,max_timing_percent=25,limit=5,right_steps=5,errors=2)
    def test_response_payload_is_not_a_command_echo(self):
        rows=margin_command_rows(self.inputs)
        self.assertEqual(rows['errors'],['051Eh','821Eh'])
        text=''.join('<tr data-margin-case="'+name+'"><td>stage</td>'+''.join('<td>'+v+'</td>' for v in values)+'</tr>' for name,values in rows.items())
        case=dict(model='margin_command',inputs=self.inputs)
        self.assertEqual(validate_case(case,text),[])
        self.assertTrue(validate_case(case,text.replace('<td>150Eh</td>','<td>880Eh</td>')))
    def test_rx_f_encoding_cannot_be_reused_on_root_port(self):
        self.inputs['port_type']='downstream'
        with self.assertRaises(ValueError):margin_command_rows(self.inputs)
    def test_step_exceeding_reported_capability_is_rejected(self):
        self.inputs['right_steps']=33
        with self.assertRaises(ValueError):margin_command_rows(self.inputs)

class PowerAllocationTeachingTest(unittest.TestCase):
    def setUp(self):
        self.budget=dict(entries=['000181B4','00058132','000381C8','0007813C'])
        self.dpa=dict(capability='08031002',latency_indicator='00000004',allocation=[26,18,10],high=0,low=2)
    def test_sustained_and_maximum_are_separate_totals(self):
        rows,totals=power_budget_case(self.budget)
        self.assertEqual(totals,['23 W','26 W'])
        text='<section id="budget-entries">'+''.join('<tr data-budget-entry="'+n+'">'+''.join('<td>'+v+'</td>' for v in values)+'</tr>' for n,values in rows.items())+'; '.join(totals)+'</section>'
        case=dict(model='power_budget',section='budget-entries',inputs=self.budget)
        self.assertEqual(validate_case(case,text),[])
        self.assertTrue(validate_case(case,text.replace('<td>18 W</td>','<td>180 W</td>')))
    def test_high_power_range_is_not_treated_as_a_linear_value(self):
        self.budget['entries'][0]='000180F0'
        with self.assertRaisesRegex(ValueError,'power-range'):power_budget_case(self.budget)
    def test_upward_transition_already_reports_the_higher_allocation(self):
        profile,transitions=dpa_profile_case(self.dpa)
        self.assertEqual(profile['2'][-1],'8 ms')
        self.assertEqual(profile['0'][-1],'3 ms')
        self.assertEqual(transitions['up-pending'],['0000h','0100h','26 W'])
        text=''.join('<tr data-dpa-profile="'+n+'">'+''.join('<td>'+v+'</td>' for v in values)+'</tr>' for n,values in profile.items())+''.join('<tr data-dpa-transition="'+n+'"><td>stage</td>'+''.join('<td>'+v+'</td>' for v in values)+'</tr>' for n,values in transitions.items())
        case=dict(model='dpa_profile',inputs=self.dpa)
        self.assertEqual(validate_case(case,text),[])
        wrong='<tr data-dpa-transition="up-pending"><td>stage</td><td>0000h</td><td>0102h</td><td>10 W</td></tr>'
        import re
        self.assertTrue(validate_case(case,re.sub(r'<tr data-dpa-transition="up-pending">.*?</tr>',wrong,text)))
    def test_nonmonotonic_allocation_array_is_rejected(self):
        self.dpa['allocation']=[26,10,18]
        with self.assertRaises(ValueError):dpa_profile_case(self.dpa)

class PlatformHintTeachingTest(unittest.TestCase):
    def setUp(self):
        self.ltr=dict(switch_ns=1024,sources=[dict(id='a',snoop='880A',nosnoop='080A'),dict(id='b',snoop='8C01',nosnoop='8808')])
        self.tph=dict(capability='00030203',entries=[49,66,83,100],vector=2,enabled_vectors=4)
    def test_each_traffic_class_has_its_own_minimum_and_switch_deduction(self):
        fields,aggregate=ltr_switch_case(self.ltr)
        self.assertEqual(fields['a-nosnoop'][-1],'Ignored')
        self.assertEqual(aggregate['snoop'],['Snoop','10,240 ns','1,024 ns','9,216 ns','8809h'])
        self.assertEqual(aggregate['nosnoop'][-2:],['7,168 ns','8807h'])
        text=''.join('<tr '+attribute+'="'+name+'">'+''.join('<td>'+v+'</td>' for v in row)+'</tr>' for attribute,rows in [('data-ltr-field',fields),('data-ltr-aggregate',aggregate)] for name,row in rows.items())
        case=dict(model='ltr_switch',inputs=self.ltr)
        self.assertEqual(validate_case(case,text),[])
        self.assertTrue(validate_case(case,text.replace('<td>9,216 ns</td>','<td>10,240 ns</td>')))
    def test_invalidated_source_does_not_retain_its_requirement(self):
        self.ltr['sources'].pop()
        self.assertEqual(ltr_switch_case(self.ltr)[1]['nosnoop'],['No requirement','0000h'])
    def test_zero_requirement_value_produces_canonical_zero_upstream(self):
        self.ltr['sources'][0]['snoop']='8800'
        self.assertEqual(ltr_switch_case(self.ltr)[1]['snoop'][-2:],['0 ns','8000h'])
        self.ltr['sources'][0]['snoop']='980A'  # Not Permitted scale is effectively infinite for this calculation.
        self.assertEqual(ltr_switch_case(self.ltr)[1]['snoop'][-2:],['31,744 ns','881Fh'])
    def test_vector_index_is_not_a_byte_offset(self):
        self.assertEqual(tph_table_case(self.tph)['entry'],['T+10h','0053h'])
        self.tph['enabled_vectors']=2
        with self.assertRaises(ValueError):tph_table_case(self.tph)
    def test_table_size_and_upper_tag_byte_obey_this_mode(self):
        self.tph['entries'][2]=0x153
        with self.assertRaises(ValueError):tph_table_case(self.tph)
        self.tph['entries']=[49,66,83]
        with self.assertRaises(ValueError):tph_table_case(self.tph)

class PtmTeachingTest(unittest.TestCase):
    def setUp(self):
        self.dialog=dict(normalized_ns=True,symmetric=True,local=[1000,1600,3000,3720],responder=[3200,3400,5200,5520],propagation_bytes=[0,0,0,200],event_local=4000)
        self.config=dict(root='0000040E',switch='0000080F',endpoint='00000009')
    def test_previous_turnaround_is_used_with_previous_round_trip(self):
        times,results=ptm_dialog_case(self.dialog)
        self.assertEqual(results,dict(rtt='600 ns',turnaround='200 ns',**{'one-way':'200 ns','master':'5,000 ns','event':'6,000 ns'}))
        text=''.join('<tr data-ptm-time="'+n+'">'+''.join('<td>'+v+'</td>' for v in row)+'</tr>' for n,row in times.items())+''.join('<tr data-ptm-result="'+n+'"><td>'+v+'</td></tr>' for n,v in results.items())
        case=dict(model='ptm_dialog',inputs=self.dialog)
        self.assertEqual(validate_case(case,text),[])
        wrong=text.replace('data-ptm-result="master"><td>5,000 ns','data-ptm-result="master"><td>5,060 ns')
        self.assertTrue(validate_case(case,wrong))
    def test_reversed_payload_is_not_accepted_as_a_delay(self):
        self.dialog['propagation_bytes']=[200,0,0,0]
        with self.assertRaisesRegex(ValueError,'preceding dialog'):ptm_dialog_case(self.dialog)
    def test_request_after_response_observes_minimum_wait(self):
        self.dialog['local'][2]=2000
        with self.assertRaisesRegex(ValueError,'wait'):ptm_dialog_case(self.dialog)
    def test_unscaled_local_ticks_cannot_be_subtracted_as_nanoseconds(self):
        self.dialog['normalized_ns']=False
        with self.assertRaisesRegex(ValueError,'normalized'):ptm_dialog_case(self.dialog)
    def test_endpoint_reserved_granularity_does_not_enter_path_maximum(self):
        self.config['endpoint']='0000FA09'
        rows,summary=ptm_config_case(self.config)
        self.assertTrue(rows['endpoint'][2].endswith('Granularity=RsvdP'))
        self.assertEqual(summary,['00000003h','00000801h','8 ns'])
    def test_unknown_and_greater_than_254_are_special_encodings(self):
        self.config['switch']='0000000F'
        self.assertEqual(ptm_config_case(self.config)[1][-2:],['00000001h','Unknown'])
        self.config['switch']='0000FF0F'
        self.assertEqual(ptm_config_case(self.config)[1][-2:],['0000FF01h','>254 ns'])

if __name__=='__main__':unittest.main()

#!/usr/bin/env python3
"""Recompute selected new teaching cases and reconcile all published editions.

Inputs are author assumptions, not specification requirements or measurements.
The checker cannot establish whether the surrounding source interpretation is
correct; that remains a review task against the registered PDF edition.
"""
from fractions import Fraction
from html import unescape
import json
import math
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]

def differential_voltage_case(x):
    """Idealized symmetric voltage geometry, not a waveform/compliance engine."""
    high=x['high_mv']; low=x['low_mv']
    if len(high)!=2 or len(low)!=2:
        raise ValueError('Expected two conductors in each representative state')
    positive=high[0]-high[1]; negative=low[0]-low[1]
    if positive<=0 or positive!=-negative:
        raise ValueError('The teaching case requires symmetric differential swing')
    rows={}
    for name,label,pair in [('high','H',high),('low','L',low)]:
        diff=pair[0]-pair[1]
        signed=('+'+str(diff)) if diff>=0 else '−'+str(-diff)
        rows[name]=[label,str(pair[0]),str(pair[1]),signed,f'{sum(pair)/2:g}']
    single=high[0]-low[0]; differential=positive-negative
    summary=[f'{single} mVPP',f'{differential} mVPP',f'{sum(high)/2:g} mV']
    return rows,summary

def polling_gate_rows(x):
    """Evaluate the selected pre-timeout, two-Lane Polling teaching path.

    Receive runs are already qualified consecutive sequences from a complete
    trace. This is not a TS decoder or the full LTSSM timeout state machine.
    """
    rows={}
    for snapshot in x['active']:
        sent=snapshot['sent']; rx=snapshot['rx']
        if sent<0 or len(rx)!=2 or any(v<0 for v in rx):
            raise ValueError('Invalid two-Lane Polling.Active counters')
        state='Polling.Configuration' if sent>=1024 and all(v>=8 for v in rx) else 'Polling.Active'
        rows[snapshot['id']]=[snapshot['point'],str(sent),str(rx[0]),str(rx[1]),state]
    for snapshot in x['config']:
        before=snapshot['before']; after=snapshot['after']; rx=snapshot['rx']
        if min(before,after)<0 or len(rx)!=2 or any(v<0 for v in rx):
            raise ValueError('Invalid two-Lane Polling.Configuration counters')
        state='Configuration' if after>=16 and any(v>=8 for v in rx) else 'Polling.Configuration'
        rows[snapshot['id']]=[snapshot['point'],str(before),str(after),str(before+after),f'{rx[0]} / {rx[1]}',state]
    return rows

def flit_dlp_rows(x):
    """Decode two preselected DLP formats, not a Flit validity/replay engine.

    The example uses a normal Flit_Marker with no PTM indication. Sequence
    legality relative to receiver history remains an explicit teaching assumption.
    """
    rows={}
    for name,usage,command in [('payload',1,0),('selective',0,3)]:
        data=x[name]
        if len(data)!=6 or any(not isinstance(v,int) or not 0<=v<=255 for v in data):
            raise ValueError('DLP must contain six bytes')
        if (data[0]>>6!=usage or (data[0]>>2)&3!=command
                or not data[0]&0x10 or data[2:]!=[0x80,0,0,0]):
            raise ValueError('Outside the selected DLP teaching formats')
        sequence=((data[0]&3)<<8)|data[1]
        if not 1<=sequence<1023:
            raise ValueError('Example excludes reserved zero and sequence rollover')
        rows[name]=[' '.join(f'{v:02X}' for v in data),f'{command:02b}b',f'{sequence:03X}h']
        if command==3:rows[name].append(f'{sequence+1:03X}h')
    return rows

def finite_fc_stages(x):
    """One finite, unscaled Non-Flit Posted-credit teaching timeline.

    These are conceptual counters, not Configuration Space registers. Ack
    leaves FC accounting unchanged; the next UpdateFC replaces credit limits.
    """
    if x.get('finite') is not True or not 0<x['payload_bytes']<=128:
        raise ValueError('Expected a finite unscaled teaching case')
    consumed=list(x['consumed']); limit=list(x['limit']); stages={}
    modulus=[256,4096]
    def snapshot(name):
        if any(not 0<=v<m for values in [consumed,limit] for v,m in zip(values,modulus)):
            raise ValueError('Counter outside unscaled field')
        available=[(l-c)%m for l,c,m in zip(limit,consumed,modulus)]
        if any(a>m//2-1 for a,m in zip(available,modulus)):
            raise ValueError('Too many outstanding unused credits')
        stages[name]=[f'PH={consumed[0]:02X}h; PD={consumed[1]:03X}h',
                      f'PH={limit[0]:02X}h; PD={limit[1]:03X}h',
                      f'{available[0]} PH / {available[1]} PD']
        return available
    snapshot('wait')
    limit=list(x['updates'][0]); available=snapshot('ready')
    required=[1,math.ceil(x['payload_bytes']/16)]
    if any(r>a for r,a in zip(required,available)):
        raise ValueError('TLP cannot pass the credit gate')
    consumed=[(c+r)%m for c,r,m in zip(consumed,required,modulus)]
    snapshot('sent'); snapshot('acked')
    limit=list(x['updates'][1]); snapshot('updated')
    return stages

def result_tokens(model, x):
    """Derive the visible results; keep address and time units explicit."""
    if model=='byte_enable':
        length=x['length_dw']
        if length<1 or not 0<=x['first_be']<16 or not 0<=x['last_be']<16:
            raise ValueError('Invalid byte-enable input')
        if length==1 and x['last_be']:
            raise ValueError('One-DW requests require zero Last DW BE')
        offsets=[i for i in range(length*4) if ((x['first_be'] if i<4 else x['last_be'] if i>=(length-1)*4 else 15)>>(i%4))&1]
        return ['+'+str(i) for i in offsets]
    if model=='partial_write_layout':
        # A deliberately limited teaching model: Mem32 write, no prefixes or
        # trailers, OHC-A1 only in FM. It does not validate a live PCIe path.
        length=x['length_dw']; address=x['address']; rid=x['requester_id']
        first=x['first_be']; last=x['last_be']; payload=bytes(x['payload'])
        if (not 2<=length<=1024 or len(payload)!=length*4
                or not 0<first<16 or not 0<last<16
                or not 0<=rid<=0xffff or not 0<=address<=0xffffffff
                or address%4 or (address&0xfff)+len(payload)>4096):
            raise ValueError('Invalid partial-write layout input')
        encoded_length=length&0x3ff
        nfm_words=[(2<<29)|encoded_length,(rid<<16)|(last<<4)|first,address]
        nfm=b''.join(word.to_bytes(4,'big') for word in nfm_words)+payload
        fm=bytes([0x40,1,encoded_length>>8,encoded_length&0xff])
        fm+=bytes([rid>>8,rid&0xff,0,0])+address.to_bytes(4,'big')
        fm+=bytes([0,0,0,(last<<4)|first])+payload
        return [' '.join(f'{value:02X}' for value in packet) for packet in (nfm,fm)]+[f'{len(nfm)} bytes',f'{len(fm)} bytes']
    if model=='vc_setup':
        # Limited to the chapter's non-default VC, Non-Flit example. This
        # checks register geometry and field encoding, not live negotiation.
        resource=x['resource']; count=x['extended_count']
        vc_id=x['vc_id']; tc_map=x['tc_map']
        if (not 1<=resource<=count<=7 or not 1<=vc_id<=7
                or not 0<tc_map<=0xff or tc_map&1):
            raise ValueError('Invalid non-default VC assignment')
        control=0x14+resource*0x0c
        status=0x1a+resource*0x0c  # Status is the upper halfword of its row.
        tokens=[]
        for capability in [x['left_capability'],x['right_capability']]:
            if capability<0x100 or capability%4 or capability+status+2>0x1000:
                raise ValueError('VC registers outside Configuration Space')
            tokens.extend([f'{capability+control:X}h',f'{capability+status:X}h'])
        disabled=(vc_id<<24)|tc_map
        return tokens+[f'{disabled:08X}h',f'{disabled|(1<<31):08X}h',f'{0xff^tc_map:02X}h']
    if model=='finite_fc':
        return [token for row in finite_fc_stages(x).values() for token in row]
    if model=='flit_dlp':
        return [token for row in flit_dlp_rows(x).values() for token in row]
    if model=='polling_gates':
        return [token for row in polling_gate_rows(x).values() for token in row]
    if model=='differential_voltage':
        rows,summary=differential_voltage_case(x)
        return [token for row in rows.values() for token in row]+summary
    if model=='lane':
        if x['lane']<0:raise ValueError('Negative Lane number')
        control=x['control_base']+x['lane']*x['stride']
        return [f'{control:X}h',f'{control+x["status_delta"]:X}h']
    if model=='ltr':
        if not x['requirement']:return []  # Value/Scale are ignored, not a zero deadline.
        if not 0<=x['scale']<=5:raise ValueError('Reserved LTR scale')
        return [f'{x["value"]*(32**x["scale"]):,} ns']
    if model=='vf_rid':
        return [f'{(x["pf"]+x["first"]+i*x["stride"])&0xffff:04X}h' for i in range(x['count'])]
    if model=='vf_bar':
        if x['ordinal']<1:raise ValueError('VF ordinal starts at one')
        return [f'{x["base"]+(x["ordinal"]-1)*x["aperture"]:X}h']
    if model=='rom':
        return [f'{x["image"]+x["pointer"]:X}h',f'{x["length_units"]*512:X}h',f'{x["image"]+x["length_units"]*512:X}h']
    if model=='capacity':
        raw=Fraction(x['gt_s']*x['lanes'],8)
        tlp=raw*Fraction(x['tlp_bytes'],x['flit_bytes'])
        return [f'{float(raw):g} GB/s',f'{float(tlp):g} GB/s']
    if model=='flight':
        outstanding=Fraction(x['bytes_s']*x['delay_us'],1000000)
        requests=math.ceil(outstanding/x['bytes_per_request'])
        limited=Fraction(x['limited_requests']*x['bytes_per_request'],x['delay_us']*1000)
        return [f'{int(outstanding):,}',str(requests),f'{float(limited):g} GB/s']
    raise ValueError('Unknown arithmetic model: '+model)

def section_text(text, anchor):
    found=re.search(r'<section\b[^>]*\bid="'+re.escape(anchor)+r'"[^>]*>(.*?)</section>',text,re.S)
    if not found:raise ValueError('Missing example section: '+anchor)
    return unescape(re.sub(r'<[^>]+>',' ',found.group(1)))

def normalized(text):
    return re.sub(r'[\s,，]','',text).casefold()

def validate_case(case, text):
    if case['model']=='differential_voltage':
        rows,summary=differential_voltage_case(case['inputs']); missing=[]
        for name,expected in rows.items():
            row=re.search(r'<tr\b[^>]*data-voltage-state="'+name+r'"[^>]*>(.*?)</tr>',text,re.S)
            cells=re.findall(r'<td\b[^>]*>(.*?)</td>',row.group(1),re.S) if row else []
            actual=[normalized(unescape(re.sub(r'<[^>]+>',' ',cell))) for cell in cells]
            if actual!=[normalized(cell) for cell in expected]:missing.append(name+': voltage cells do not match')
        passage=normalized(section_text(text,case['section']))
        missing.extend(token for token in summary if normalized(token) not in passage)
        return missing
    if case['model']=='polling_gates':
        missing=[]
        for name,expected in polling_gate_rows(case['inputs']).items():
            row=re.search(r'<tr\b[^>]*data-polling-stage="'+re.escape(name)+r'"[^>]*>(.*?)</tr>',text,re.S)
            cells=re.findall(r'<td\b[^>]*>(.*?)</td>',row.group(1),re.S) if row else []
            actual=[normalized(unescape(re.sub(r'<[^>]+>',' ',cell))) for cell in cells]
            if actual!=[normalized(cell) for cell in expected]:
                missing.append(name+': counter cells or next state do not match')
        return missing
    if case['model']=='flit_dlp':
        missing=[]
        for name,tokens in flit_dlp_rows(case['inputs']).items():
            row=re.search(r'<tr\b[^>]*data-dlp-case="'+name+r'"[^>]*>(.*?)</tr>',text,re.S)
            passage=normalized(unescape(re.sub(r'<[^>]+>',' ',row.group(1)))) if row else ''
            missing.extend(name+': '+token for token in tokens if normalized(token) not in passage)
        return missing
    if case['model']=='finite_fc':
        missing=[]
        for stage,tokens in finite_fc_stages(case['inputs']).items():
            row=re.search(r'<tr\b[^>]*data-fc-stage="'+stage+r'"[^>]*>(.*?)</tr>',text,re.S)
            passage=normalized(unescape(re.sub(r'<[^>]+>',' ',row.group(1)))) if row else ''
            missing.extend(stage+': '+token for token in tokens if normalized(token) not in passage)
        return missing
    passage=normalized(section_text(text,case['section']))
    tokens=result_tokens(case['model'],case['inputs'])
    return [token for token in tokens if normalized(token) not in passage]

def main():
    cases=json.loads((ROOT/'.ai/pcie-course/advanced-examples.json').read_text())['cases']
    errors=[]
    for case in cases:
        chapter=case['chapter']
        files=[ROOT/f'DOCS/pcie-course/chapter-{chapter}.html',*sorted((ROOT/'_posts').glob(f'*-pcie-chapter-{chapter}-*.md'))]
        if len(files)!=3:errors.append(f'Chapter {chapter}: expected three editions')
        for path in files:
            try:missing=validate_case(case,path.read_text())
            except ValueError as error:errors.append(f'{path.name}: {error}');continue
            if missing:errors.append(f'{path.name} #{case["section"]}: derived results missing: {missing}')
    for error in errors:print(error)
    if not errors:print(f'Advanced PCIe examples passed: {len(cases)} models, three editions each.')
    return bool(errors)

if __name__=='__main__':raise SystemExit(main())

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

def sriov_resource_case(x):
    """Single-PF ARI allocation example; not an allocator or isolation check."""
    num=x['num']; total=x['total']; pf=x['pf']; first=x['first']; stride=x['stride']
    if not 1<=num<=total<=0xffff or not 0<=pf<=0xffff or not 1<=first<=0xffff or not 0<=stride<=0xffff:
        raise ValueError('Invalid VF count or RID field')
    if num>1 and not stride:raise ValueError('Multiple VFs require nonzero stride')
    supported=x['supported_pages']; system=x['system_page']
    if not 0<supported<=0xffffffff or supported&0x553!=0x553:
        raise ValueError('Required page sizes absent from this PF')
    if not 0<system<=0xffffffff or system&(system-1) or system&supported!=system:
        raise ValueError('System Page Size must select one supported bit')
    page=1<<(system.bit_length()-1+12)
    probe_low=int(x['probe_low'],16); probe_high=int(x['probe_high'],16)
    bar_low=int(x['bar_low'],16); bar_high=int(x['bar_high'],16)
    if any(not 0<=v<=0xffffffff for v in (probe_low,probe_high,bar_low,bar_high)):
        raise ValueError('VF BAR fields must be DWORDs')
    if probe_low&7!=4 or bar_low&15!=probe_low&15:
        raise ValueError('This example requires a consistent 64-bit Memory BAR pair')
    mask=(probe_high<<32)|(probe_low&~15); aperture=((~mask)&((1<<64)-1))+1
    if aperture<=0 or aperture&(aperture-1) or aperture<page or aperture%page:
        raise ValueError('Per-VF aperture does not satisfy page alignment')
    base=(bar_high<<32)|(bar_low&~15); end=base+num*aperture-1
    if base%aperture or end>=1<<64 or base<x['window'][0] or end>x['window'][1]:
        raise ValueError('VF memory ranges are unaligned or outside the Window')
    seen={pf,*x['other_rids']}; rids={};bars={}
    for ordinal in range(1,num+1):
        rid=(pf+first+(ordinal-1)*stride)&0xffff
        if rid in seen:raise ValueError('PF/VF identities overlap')
        seen.add(rid)
        bus=rid>>8;function=rid&255
        if bus<pf>>8 or bus not in x['reserved_buses']:
            raise ValueError('VF Bus Number lower than PF or not reserved')
        if bus==pf>>8 and (rid>>3)&31<(pf>>3)&31:
            raise ValueError('VF Device Number lower than associated PF')
        rids[str(ordinal)]=[str(ordinal),f'{pf:04X}h + {first:04X}h + {ordinal-1}×{stride:04X}h',f'{rid:04X}h',f'{bus:02X}h / {function:02X}h',f'{bus:02X}h / {(rid>>3)&31:02X}h / {rid&7:02X}h']
        start=base+(ordinal-1)*aperture
        bars[str(ordinal)]=[str(ordinal),f'{start:08X}h',f'{start+aperture-1:08X}h',f'{aperture:X}h / {aperture//1024} KiB']
    fields={'total':['TotalVFs','0Eh',f'{total:04X}h'],'num':['NumVFs','10h',f'{num:04X}h'],
            'first':['First VF Offset','14h',f'{first:04X}h'],'stride':['VF Stride','16h',f'{stride:04X}h'],
            'supported':['Supported Page Sizes','1Ch',f'{supported:08X}h'],'system':['System Page Size','20h',f'{system:08X}h']}
    summary=[f'{mask:016X}h',f'{probe_low:08X}h',f'{probe_high:08X}h',f'{bar_low:08X}h',f'{bar_high:08X}h',f'{num*aperture:X}h',f'{num*aperture//1024} KiB']
    return fields,rids,bars,summary

def vf_enable_case(x):
    """No FRS or shorter VF Enable Time; independent readiness and MSE gates."""
    if x['frs'] or x['shorter_time']:
        raise ValueError('This timeline assumes no early readiness alternatives')
    rows={};successful=False;previous=-1
    for stage in x['stages']:
        time=stage['ms'];control=int(stage['control'],16);status=stage.get('config_status')
        if time<0 or time<previous or not 0<=control<=0xffff or control&0x11!=0x11:
            raise ValueError('Timeline requires monotonic times, ARI and VFs enabled')
        previous=time;config_allowed=time>=100
        if status and (status not in ('RRS','SC') or not config_allowed):
            raise ValueError('Configuration Request before permitted access time')
        if status=='RRS' and (successful or time>1000):
            raise ValueError('RRS after success or beyond the initialization interval')
        if status=='SC':successful=True
        memory_allowed=bool(control&8) and (successful or time>=1000)
        if stage.get('memory_request') and not memory_allowed:
            raise ValueError('Memory Request lacks readiness or VF MSE')
        config='No' if not config_allowed else 'Yes'+(' / '+status if status else '')
        rows[stage['id']]=[f'{time} ms',f'{control:04X}h',config,'Yes, readiness established' if memory_allowed else 'No']
    return rows

def ptm_dialog_case(x):
    """Two normalized-ns, drift-free dialogs; not a hardware clock estimator."""
    if not x['normalized_ns'] or not x['symmetric']:
        raise ValueError('This case assumes normalized ns and symmetric transit')
    local=x['local']; responder=x['responder']; payload=x['propagation_bytes']
    if len(local)!=4 or len(responder)!=4 or len(payload)!=4 or any(not 0<=v<=255 for v in payload):
        raise ValueError('Missing timestamps or four-byte Propagation Delay')
    t1,t4,t1next,t4next=local; t2,t3,t2next,t3next=responder
    if not t1<t4<t1next<t4next or not t2<t3<t2next<t3next:
        raise ValueError('Nonmonotonic dialog timestamps')
    if t1next-t4<1000:raise ValueError('Next Request must wait at least 1 us after Response')
    turnaround=int.from_bytes(bytes(payload),'big'); rtt=t4-t1
    if turnaround!=t3-t2 or turnaround>=rtt:
        raise ValueError('Propagation Delay does not match preceding dialog')
    one_way=Fraction(rtt-turnaround,2); master=Fraction(t2next)-one_way
    if t4next-t1next!=(t3next-t2next)+2*one_way:
        raise ValueError('Current dialog conflicts with this fixed symmetric example')
    if x['event_local']<t4next:raise ValueError('Example event must follow the current response')
    event=master+x['event_local']-t1next
    fmt=lambda n:f'{n.numerator:,} ns' if n.denominator==1 else f'{n.numerator}/{n.denominator} ns'
    times={}
    for name,dialog,port,kind,symbol,value,domain in [
        ('t1',1,'Endpoint TX','Request','t1',t1,'Local'),('t2',1,'Switch RX','Request','t2',t2,'PTM Master Time'),
        ('t3',1,'Switch TX','Response','t3',t3,'PTM Master Time'),('t4',1,'Endpoint RX','Response','t4',t4,'Local'),
        ('t1-next',2,'Endpoint TX','Request','t1′',t1next,'Local'),('t2-next',2,'Switch RX','Request','t2′',t2next,'PTM Master Time'),
        ('t3-next',2,'Switch TX','ResponseD','t3′',t3next,'PTM Master Time'),('t4-next',2,'Endpoint RX','ResponseD','t4′',t4next,'Local')]:
        times[name]=[str(dialog),port+' '+kind,symbol,fmt(Fraction(value)),domain]
    results={'rtt':fmt(Fraction(rtt)),'turnaround':fmt(Fraction(turnaround)),
             'one-way':fmt(one_way),'master':fmt(master),'event':fmt(event)}
    return times,results

def ptm_config_case(x):
    """Decode the chapter's selected Root and intervening Time Source fields."""
    caps={k:int(x[k],16) for k in ('root','switch','endpoint')}
    if any(not 0<=v<=0xffffffff for v in caps.values()):raise ValueError('Capability is not a DW')
    if caps['root']&6!=6 or caps['switch']&7!=7 or caps['endpoint']&7!=1:
        raise ValueError('Capabilities do not match this Root/Switch/Endpoint case')
    if any(not v&8 for v in caps.values()):raise ValueError('This example assumes ePTM support')
    grains=[(caps[k]>>8)&255 for k in ('root','switch')]
    effective=0 if 0 in grains else max(grains)
    rows={}
    for key,name in [('root','Root Port'),('switch','Switch'),('endpoint','Endpoint')]:
        raw=caps[key]; roles=f'Requester={raw&1}; Responder={(raw>>1)&1}; Root={(raw>>2)&1}; ePTM={(raw>>3)&1}; '
        gran=(raw>>8)&255
        description=('Granularity=RsvdP' if not raw&4 else 'no local clock' if gran==0 else '>254 ns' if gran==255 else f'{gran} ns')
        rows[key]=[name,f'{raw:08X}h',roles+description]
    granularity='Unknown' if effective==0 else '>254 ns' if effective==255 else f'{effective} ns'
    return rows,['00000003h',f'{(effective<<8)|1:08X}h',granularity]

def ltr_switch_case(x):
    """Recompute the two-source, fixed-latency teaching example, not RC policy."""
    if not isinstance(x['switch_ns'],int) or x['switch_ns']<0:
        raise ValueError('Switch latency must be a nonnegative integer')
    rows={}; values={'snoop':[],'nosnoop':[]}; requirements={'snoop':0,'nosnoop':0}
    for source in x['sources']:
        for traffic in values:
            raw=int(source[traffic],16)
            if not 0<=raw<=0xffff or raw&0x6000:
                raise ValueError('LTR field outside 16 bits or Reserved bits set')
            requirement=(raw>>15)&1; scale=(raw>>10)&7; value=raw&0x3ff
            requirements[traffic]+=requirement
            latency=value*32**scale if requirement and scale<=5 else None
            values[traffic].append(latency)
            meaning=(f'{latency:,} ns' if latency is not None else 'Not Permitted' if requirement else 'Ignored')
            rows[source['id']+'-'+traffic]=[source['id'].upper()+' / '+('Snoop' if traffic=='snoop' else 'No-Snoop'),f'{raw:04X}h',str(requirement),f'{scale:03b}b',str(value),meaning]
    aggregate={}
    for traffic,latencies in values.items():
        finite=[v for v in latencies if v is not None]
        if not finite:
            if requirements[traffic]:raise ValueError('No finite valid source for this example')
            aggregate[traffic]=['No requirement','0000h']; continue
        minimum=min(finite); result=max(0,minimum-x['switch_ns'])
        # The displayed example uses an exact encoding. No rounding policy is implied.
        encodings=[(s,result//32**s) for s in range(6) if result%32**s==0 and result//32**s<=1023]
        if not encodings:raise ValueError('Result has no exact LTR encoding for this example')
        # Use the largest exact scale for this author's example; the spec does not
        # require a unique nonzero encoding when several represent the same time.
        scale,value=encodings[-1] if result else (0,0)
        raw=0x8000|(scale<<10)|value
        aggregate[traffic]=['Snoop' if traffic=='snoop' else 'No-Snoop',f'{minimum:,} ns',f'{x["switch_ns"]:,} ns',f'{result:,} ns',f'{raw:04X}h']
    return rows,aggregate

def tph_table_case(x):
    """Narrow ordinary-TPH Interrupt Vector Mode example with a local ST table."""
    capability=int(x['capability'],16); entries=x['entries']; vector=x['vector']
    size=((capability>>16)&0x7ff)+1
    if capability&3!=3 or capability&(1<<8) or (capability>>9)&3!=1:
        raise ValueError('Example requires ordinary TPH, vector support and a local table')
    if not 1<=size<=64 or size!=len(entries) or not 0<=vector<min(size,x['enabled_vectors']):
        raise ValueError('ST table size or vector range does not cover selection')
    if any(not 0<=entry<=255 for entry in entries):
        raise ValueError('Upper ST byte is RsvdP without Extended TPH')
    offset=0xc+2*vector; control=(1<<8)|1
    return {'cap':['T+04h',f'{capability:08X}h'],
            'entry':[f'T+{offset:02X}h',f'{entries[vector]:04X}h'],
            'control':['T+08h',f'{control:08X}h']}

def power_budget_case(x):
    """Decode the chapter's non-extended D0, substate-0 two-rail example.

    This is not a general budget manager. Alternative high-power ranges and
    extended/hidden connector entries require their own source interpretation.
    """
    rows={}; totals={3:Fraction(0),7:Fraction(0)}; seen=set()
    for i,value in enumerate(x['entries']):
        raw=int(value,16)
        if not 0<=raw<=0xffffffff or raw>>21:
            raise ValueError('This case uses only non-extended entries')
        base=raw&255;scale=(raw>>8)&3;sub=(raw>>10)&7
        state=(raw>>13)&3;kind=(raw>>15)&7;rail=(raw>>18)&7
        if scale==0 and base>0xef:
            raise ValueError('Alternative power-range encoding is not linear watts')
        if state or sub or kind not in totals or rail not in (0,1):
            raise ValueError('This case is D0 substate 0, sustained/maximum, 12 V/3.3 V')
        if (kind,rail) in seen:raise ValueError('Duplicate operating-condition rail')
        seen.add((kind,rail));factor=Fraction(1,10**scale);power=base*factor
        totals[kind]+=power
        rows[str(i)]=[str(i),f'{raw:08X}h','D0 / 0',f'{kind:03b}b',
                      f'{rail:03b}b / '+('12 V' if rail==0 else '3.3 V'),
                      str(base),f'{float(factor):g}×',f'{float(power):g} W']
    if seen!={(3,0),(3,1),(7,0),(7,1)}:
        raise ValueError('The example requires both rails for each reported type')
    return rows,[f'{float(totals[k]):g} W' for k in (3,7)]

def dpa_profile_case(x):
    """Derive allocations, target latencies and the illustrated Status values.

    Assumes D0, control enabled, no reset, emergency override or competing
    writes. These checks do not establish actual transition completion.
    """
    cap=int(x['capability'],16);indicator=int(x['latency_indicator'],16)
    count=(cap&31)+1;unit=(cap>>8)&3;scale=(cap>>12)&3
    if unit==3:raise ValueError('Reserved DPA latency unit')
    if len(x['allocation'])!=count:raise ValueError('DPA array size must be Substate_Max+1')
    if any(not 0<=v<=255 for v in x['allocation']):raise ValueError('DPA entries are bytes')
    if any(b>a for a,b in zip(x['allocation'],x['allocation'][1:])):
        raise ValueError('DPA allocations must not increase with substate number')
    factor=[Fraction(10),Fraction(1),Fraction(1,10),Fraction(1,100)][scale]
    powers=[v*factor for v in x['allocation']];latency=[(cap>>16)&255,(cap>>24)&255]
    profiles={}
    for i,(value,power) in enumerate(zip(x['allocation'],powers)):
        bit=(indicator>>i)&1;delay=latency[bit]*(10**unit)
        profiles[str(i)]=[str(i),f'D+{0x10+i:02X}h',f'{value:02X}h',
                          f'{float(power):g} W',str(bit),f'{delay} ms']
    high=x['high'];low=x['low']
    if not 0<=high<count or not 0<=low<count or powers[high]<=powers[low]:
        raise ValueError('The transition case needs distinct higher/lower allocations')
    control=lambda state:f'{state:04X}h'
    status=lambda state:f'{0x100|state:04X}h'
    watts=lambda state:f'{float(powers[state]):g} W'
    transitions=dict(initial=[control(high),status(high),watts(high)],
                     **{'down-pending':[control(low),status(high),watts(high)],
                        'down-done':[control(low),status(low),watts(low)],
                        'up-pending':[control(high),status(high),watts(high)]})
    return profiles,transitions

def margin_command_rows(x):
    """Recompute the 16 GT/s local Upstream Port example, not a margining engine.

    Field meanings were reviewed separately against Base 6.0. This narrow case
    does not validate Retimer relay, PAM4 measurements or a hardware procedure.
    """
    if x['gt_s']!=16 or x['port_type']!='upstream' or x['receiver']!=6:
        raise ValueError('This case targets local Rx(F) at 16 GT/s')
    if not 6<=x['timing_steps']<=63 or not 20<=x['max_timing_percent']<=50:
        raise ValueError('Invalid reported NRZ timing parameters')
    if not x['caps']&4 or not 1<=x['right_steps']<=x['timing_steps']:
        raise ValueError('Right-step case requires independent timing and an in-range step')
    if not 0<=x['errors']<=63 or not 0<=x['limit']<=63 or not 0<=x['caps']<=31:
        raise ValueError('Margin payload out of range')
    def word(payload,kind):return f'{(payload<<8)|(kind<<3)|x["receiver"]:04X}h'
    report=lambda query,value:[word(query,1),word(value,1)]
    step=word(x['right_steps'],3)
    return dict(cap=report(0x88,x['caps']),steps=report(0x8a,x['timing_steps']),
                offset=report(0x8b,x['max_timing_percent']),
                limit=[word(0xc0|x['limit'],2)]*2,
                setup=[step,word(0x40,3)],running=[step,word(0x80,3)],
                errors=[step,word(0x80|x['errors'],3)])

def rx_calibration_case(x):
    """Arithmetic for the source-checked 16 GT/s Non-Root calibration excerpt.

    This checks means and unit conversions, not channel masks, stress-search
    completion, test-tool accuracy, DUT BER, or statistical confidence.
    """
    if x['gt_s']!=16 or x['receiver_type']!='non-root':
        raise ValueError('This teaching model is scoped to the 16 GT/s Non-Root case')
    ui=Fraction(1000,x['gt_s']); target_ew=ui*Fraction(3,10)
    rows={}
    for name,label,unit,target,tolerance in [('eh','EH','mVPP',Fraction(15),Fraction(3,2)),
                                            ('ew','EW','ps',target_ew,Fraction(1,2))]:
        raw=x[name]
        if len(raw)<5 or any(Fraction(str(v))<=0 for v in raw):
            raise ValueError('At least five positive calibration samples are required')
        values=[Fraction(str(v)) for v in raw]; mean=sum(values)/len(values)
        fmt=lambda value:f'{float(value):g}'
        rows[name]=[label,', '.join(str(v) for v in raw)+' '+unit,
                    fmt(mean)+' '+unit,fmt(target-tolerance)+'–'+fmt(target+tolerance)+' '+unit]
    # Table 8-8's 16 GT/s Non-Root nominal high-frequency range, and the
    # source rule extending options 2 dB below / 3 dB above, were read in PDF.
    loss_min=Fraction(245,10)-2; loss_max=Fraction(255,10)+3
    summary=[f'{float(ui):g} ps',f'{float(target_ew):g} ps',
             f'{float(loss_min):g}–{float(loss_max):g} dB']
    return rows,summary

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
    if model=='power_budget':
        rows,totals=power_budget_case(x)
        return [token for row in rows.values() for token in row]+totals
    if model=='dpa_profile':
        profile,transitions=dpa_profile_case(x)
        return [token for rows in (profile,transitions) for row in rows.values() for token in row]
    if model=='margin_command':
        return [token for row in margin_command_rows(x).values() for token in row]
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
    if model=='rx_calibration':
        rows,summary=rx_calibration_case(x)
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
    if case['model'] in ('sriov_resource','vf_enable'):
        missing=[]
        if case['model']=='sriov_resource':
            fields,rids,bars,summary=sriov_resource_case(case['inputs'])
            groups=[('data-sriov-field',fields,slice(0,3)),('data-vf-rid',rids,None),('data-vf-bar',bars,None)]
            passage=normalized(section_text(text,case['section']))
            missing.extend(token for token in summary if normalized(token) not in passage)
        else:groups=[('data-vf-stage',vf_enable_case(case['inputs']),None)]
        translations={'否':'No','可':'Yes','可／本次rrs':'Yes / RRS','可／本次sc':'Yes / SC','可已確認就緒':'Yes, readiness established'}
        for attribute,rows,selection in groups:
            for name,expected in rows.items():
                row=re.search(r'<tr\b[^>]*'+attribute+'="'+name+r'"[^>]*>(.*?)</tr>',text,re.S)
                cells=re.findall(r'<td\b[^>]*>(.*?)</td>',row.group(1),re.S) if row else []
                if selection:cells=cells[selection]
                actual=[normalized(unescape(re.sub(r'<[^>]+>',' ',cell))) for cell in cells]
                actual=[normalized(translations.get(cell,cell)) for cell in actual]
                if actual!=[normalized(cell) for cell in expected]:missing.append(attribute+' '+name+': derived cells do not match')
        return missing
    if case['model'] in ('ptm_dialog','ptm_config'):
        missing=[]
        if case['model']=='ptm_dialog':
            times,results=ptm_dialog_case(case['inputs'])
            groups=[('data-ptm-time',times,None),('data-ptm-result',{k:[v] for k,v in results.items()},slice(-1,None))]
        else:
            rows,summary=ptm_config_case(case['inputs']);groups=[('data-ptm-cap',rows,None)]
            passage=normalized(section_text(text,case['section']))
            missing.extend(token for token in summary if normalized(token) not in passage)
        for attribute,rows,selection in groups:
            for name,expected in rows.items():
                row=re.search(r'<tr\b[^>]*'+attribute+'="'+name+r'"[^>]*>(.*?)</tr>',text,re.S)
                cells=re.findall(r'<td\b[^>]*>(.*?)</td>',row.group(1),re.S) if row else []
                if selection:cells=cells[selection]
                actual=[normalized(unescape(re.sub(r'<[^>]+>',' ',cell))) for cell in cells]
                if actual!=[normalized(cell) for cell in expected]:missing.append(attribute+' '+name+': derived cells do not match')
        return missing
    if case['model'] in ('ltr_switch','tph_table'):
        missing=[]
        if case['model']=='ltr_switch':
            fields,aggregate=ltr_switch_case(case['inputs'])
            groups=[('data-ltr-field',fields,False),('data-ltr-aggregate',aggregate,False)]
        else:
            groups=[('data-tph-case',tph_table_case(case['inputs']),True)]
        for attribute,rows,prefix_only in groups:
            for name,expected in rows.items():
                row=re.search(r'<tr\b[^>]*'+attribute+'="'+name+r'"[^>]*>(.*?)</tr>',text,re.S)
                cells=re.findall(r'<td\b[^>]*>(.*?)</td>',row.group(1),re.S) if row else []
                actual=[normalized(unescape(re.sub(r'<[^>]+>',' ',cell))) for cell in cells]
                if prefix_only:actual=actual[:len(expected)]
                expected=[normalized(cell) for cell in expected]
                if attribute=='data-ltr-field' and expected[-1]=='ignored' and actual:
                    if actual[-1] in ('忽略不換算','ignored'):actual[-1]='ignored'
                if actual!=expected:missing.append(attribute+' '+name+': derived cells do not match')
        return missing
    if case['model'] in ('power_budget','dpa_profile'):
        missing=[]
        if case['model']=='power_budget':
            rows,totals=power_budget_case(case['inputs'])
            groups=[('data-budget-entry',rows,None)]
            passage=normalized(section_text(text,case['section']))
            missing.extend(token for token in totals if normalized(token) not in passage)
        else:
            profiles,transitions=dpa_profile_case(case['inputs'])
            groups=[('data-dpa-profile',profiles,None),('data-dpa-transition',transitions,slice(1,4))]
        for attribute,rows,selection in groups:
            for name,expected in rows.items():
                row=re.search(r'<tr\b[^>]*'+attribute+'="'+name+r'"[^>]*>(.*?)</tr>',text,re.S)
                cells=re.findall(r'<td\b[^>]*>(.*?)</td>',row.group(1),re.S) if row else []
                if selection:cells=cells[selection]
                actual=[normalized(unescape(re.sub(r'<[^>]+>',' ',cell))) for cell in cells]
                if actual!=[normalized(cell) for cell in expected]:
                    missing.append(attribute+' '+name+': derived cells do not match')
        return missing
    if case['model']=='margin_command':
        missing=[]
        for name,expected in margin_command_rows(case['inputs']).items():
            row=re.search(r'<tr\b[^>]*data-margin-case="'+name+r'"[^>]*>(.*?)</tr>',text,re.S)
            cells=re.findall(r'<td\b[^>]*>(.*?)</td>',row.group(1),re.S) if row else []
            actual=[normalized(unescape(re.sub(r'<[^>]+>',' ',cell))) for cell in cells[1:3]]
            if actual!=[normalized(cell) for cell in expected]:
                missing.append(name+': command or response fields do not match')
        return missing
    if case['model']=='rx_calibration':
        rows,summary=rx_calibration_case(case['inputs']); missing=[]
        for name,expected in rows.items():
            row=re.search(r'<tr\b[^>]*data-rx-check="'+name+r'"[^>]*>(.*?)</tr>',text,re.S)
            cells=re.findall(r'<td\b[^>]*>(.*?)</td>',row.group(1),re.S) if row else []
            actual=[normalized(unescape(re.sub(r'<[^>]+>',' ',cell))) for cell in cells]
            if actual!=[normalized(cell) for cell in expected]:missing.append(name+': calibration mean cells do not match')
        passage=normalized(section_text(text,case['section']))
        missing.extend(token for token in summary if normalized(token) not in passage)
        return missing
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

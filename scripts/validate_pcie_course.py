#!/usr/bin/env python3
"""Validate the published course structure and recompute the worked example.

This checks reproducible arithmetic and source/HTML consistency, not technical
truth or prose quality. Those still require review against the cited editions.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
import hashlib
from html.parser import HTMLParser
import json
import operator
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / '.ai' / 'pcie-course'
OUTPUT = ROOT / 'DOCS' / 'pcie-course'


class Document(HTMLParser):
    def __init__(self, source: str):
        super().__init__()
        self.ids, self.links, self.tags, self.tables = [], [], [], []
        self.table = self.row = self.cell = None
        self.caption = False
        self.feed(source)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag == 'table':
            self.table = {'caption': '', 'rows': []}
        elif self.table is not None:
            if tag == 'caption':
                self.caption = True
            elif tag == 'tr':
                self.row = []
            elif tag in ('th', 'td'):
                self.cell = ''

    def handle_data(self, text):
        if self.table is not None:
            if self.caption:
                self.table['caption'] += text
            if self.cell is not None:
                self.cell += text

    def handle_endtag(self, tag):
        if self.table is None:
            return
        if tag == 'caption':
            self.caption = False
        elif tag in ('th', 'td') and self.row is not None:
            self.row.append((self.cell or '').strip())
            self.cell = None
        elif tag == 'tr' and self.row is not None:
            self.table['rows'].append(self.row)
            self.row = None
        elif tag == 'table':
            self.tables.append(self.table)
            self.table = None


def arithmetic(expression):
    operations = {ast.Add: operator.add, ast.Sub: operator.sub,
                  ast.BitAnd: operator.and_, ast.BitOr: operator.or_,
                  ast.RShift: operator.rshift, ast.LShift: operator.lshift}
    def compute(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in operations:
            return operations[type(node.op)](compute(node.left), compute(node.right))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Invert):
            return ~compute(node.operand)
        raise ValueError(f'Unsupported arithmetic: {expression}')
    return compute(ast.parse(expression, mode='eval').body)


def validate_topology_example(example, authored, require):
    """Reconcile Chapter 1's published bytes and derive its bridge path."""
    def bdf_parts(value):
        match = re.fullmatch(r'([0-9a-fA-F]{2}):([0-9a-fA-F]{2})\.([0-7])', value)
        if not match:
            raise ValueError(f'Invalid conventional BDF: {value}')
        bus, device, function = (int(part, 16) for part in match.groups())
        if device > 0x1F:
            raise ValueError(f'Conventional Device Number exceeds five bits: {value}')
        return bus, device, function

    def published_rows(caption):
        tables = [table for table in authored.tables if table['caption'] == caption]
        require(len(tables) == 1, f'Expected one Chapter 1 table: {caption}')
        if len(tables) != 1:
            return [], {}
        rows = tables[0]['rows']
        require(bool(rows), f'Empty Chapter 1 table: {caption}')
        if not rows:
            return [], {}
        require(all(len(row) == 4 for row in rows), f'Unexpected columns: {caption}')
        data = {row[0]: row for row in rows[1:] if len(row) == 4}
        require(len(data) == len(rows) - 1, f'Duplicate BDF or malformed row: {caption}')
        return rows[0], data

    role_header, role_rows = published_rows('本例的角色辨識資料')
    range_header, range_rows = published_rows('教學快照中的 Bridge 下游範圍')
    cap_base = int(example['cap_base'], 0)
    require(0x40 <= cap_base <= 0xFC and cap_base % 4 == 0, 'Invalid Chapter 1 capability base')
    if len(role_header) == 4:
        for label, expected in [(role_header[1], 0x0E), (role_header[2], cap_base + 2)]:
            offsets = re.findall(r'0x[0-9A-Fa-f]+', label)
            require(bool(offsets) and int(offsets[0], 0) == expected,
                    f'Incorrect Chapter 1 role-read offset: {label}')
    if len(range_header) == 4:
        for label, expected in [(range_header[1], 0x19), (range_header[2], 0x1A)]:
            offsets = re.findall(r'0x[0-9A-Fa-f]+', label)
            require(bool(offsets) and int(offsets[0], 0) == expected,
                    f'Incorrect Chapter 1 bus-register offset: {label}')

    roles = {entry['bdf']: entry for entry in example['role_reads']}
    bridges = {entry['bdf']: entry for entry in example['topology']}
    require(len(roles) == len(example['role_reads']), 'Duplicate Chapter 1 role evidence')
    require(len(bridges) == len(example['topology']), 'Duplicate Chapter 1 bridge evidence')
    require(set(role_rows) == set(roles), 'Chapter 1 published role rows differ from evidence')
    require(set(range_rows) == set(bridges), 'Chapter 1 published bridge rows differ from evidence')
    # This teaching snapshot contains ordinary Endpoints and Root/Switch Ports.
    # Table 7-19 assigns Type 0 to type 0 and Type 1 to types 4, 5, and 6.
    layouts = {0: 0, 4: 1, 5: 1, 6: 1}
    for bdf, entry in roles.items():
        bdf_parts(bdf)
        header = int(entry['header'], 0)
        capability = int(entry['capabilities_low_byte'], 0)
        require(0 <= header <= 0xFF and 0 <= capability <= 0xFF, f'Invalid Chapter 1 byte: {bdf}')
        layout, device_type = header & 0x7F, (capability >> 4) & 0xF
        require(device_type in layouts and layouts.get(device_type) == layout,
                f'Chapter 1 Header Layout and Device/Port Type disagree: {bdf}')
        require(capability & 0xF == 2, f'Chapter 1 capability version differs from the example: {bdf}')
        if bdf not in role_rows:
            continue
        row = role_rows[bdf]
        require(int(row[1], 0) == header and int(row[2], 0) == capability,
                f'Published Chapter 1 role reads differ from evidence: {bdf}')
        stated_layout = re.search(r'Type\s+([01])\s+Header', row[3])
        stated_type = re.search(r'PCIe Type\s+(\d+)', row[3])
        require(stated_layout is not None and int(stated_layout.group(1)) == layout,
                f'Published Chapter 1 Header Layout conclusion differs: {bdf}')
        require(stated_type is not None and int(stated_type.group(1)) == device_type,
                f'Published Chapter 1 Device/Port Type conclusion differs: {bdf}')

    topology = {}
    for bdf, entry in bridges.items():
        bus, _, _ = bdf_parts(bdf)
        secondary, subordinate = int(entry['secondary'], 0), int(entry['subordinate'], 0)
        require(0 <= secondary <= subordinate <= 0xFF and secondary != bus,
                f'Invalid configured Chapter 1 bridge range: {bdf}')
        require(bdf in roles and int(roles[bdf]['header'], 0) & 0x7F == 1,
                f'Chapter 1 bridge lacks a Type 1 Header: {bdf}')
        topology[bdf] = (bus, secondary, subordinate)
        if bdf in range_rows:
            row = range_rows[bdf]
            require(int(row[1], 0) == secondary and int(row[2], 0) == subordinate,
                    f'Published Chapter 1 bridge range differs from evidence: {bdf}')
    for bdf, (_, secondary, subordinate) in topology.items():
        for child, (child_bus, child_secondary, child_subordinate) in topology.items():
            if child_bus == secondary:
                require(secondary <= child_secondary <= child_subordinate <= subordinate,
                        f'Chapter 1 child range escapes its parent: {bdf} -> {child}')

    target_bus, device, function = bdf_parts(example['target'])
    secondary_buses = {secondary for _, secondary, _ in topology.values()}
    roots = {bus for bus, _, _ in topology.values() if bus not in secondary_buses}
    require(len(roots) == 1, 'Chapter 1 snapshot needs one unambiguous root bus')
    path, visited = [], set()
    current_bus = next(iter(roots)) if len(roots) == 1 else None
    while current_bus is not None and current_bus != target_bus:
        require(current_bus not in visited, 'Cycle in Chapter 1 bridge path')
        if current_bus in visited:
            break
        visited.add(current_bus)
        candidates = [(bdf, secondary) for bdf, (bus, secondary, subordinate) in topology.items()
                      if bus == current_bus and secondary <= target_bus <= subordinate]
        require(len(candidates) == 1, f'No unique Chapter 1 branch for target bus at Bus {current_bus:02X}')
        if len(candidates) != 1:
            break
        bdf, current_bus = candidates[0]
        path.append(bdf)
    require(current_bus == target_bus, 'Chapter 1 bridge path does not reach the target bus')
    require(path == example['expected_bridge_path'], 'Derived Chapter 1 bridge path differs from the conclusion')
    requester_id = (target_bus << 8) | (device << 3) | function
    require(requester_id == int(example['expected_requester_id'], 0),
            'Derived Chapter 1 Requester ID differs from the conclusion')


def table_rows(authored, caption, require):
    tables = [table for table in authored.tables if table['caption'] == caption]
    require(len(tables) == 1, f'Expected one table: {caption}')
    return tables[0]['rows'][1:] if len(tables) == 1 else []


def hex_values(text):
    return [int(value, 16) for value in re.findall(r'0x[0-9A-Fa-f]+', text)]


def validate_configuration_example(example, authored, topology, require):
    memory = {}
    for read in example['raw_reads']:
        offset, bits, value = int(read['offset'], 0), read['width_bits'], int(read['value'], 0)
        require(bits in (8, 16, 32) and 0 <= value < 2**bits, f'Invalid Chapter 2 read: {read}')
        for i, byte in enumerate(value.to_bytes(bits // 8, 'little')):
            require(offset + i not in memory, 'Overlapping Chapter 2 evidence')
            memory[offset + i] = byte

    def read(offset, bits):
        return int.from_bytes(bytes(memory[offset+i] for i in range(bits // 8)), 'little')

    published = []
    for caption in ['傳統清單的假設讀值', 'Extended 清單與序號的假設讀值']:
        for row in table_rows(authored, caption, require):
            offset, bits, value = int(row[0], 0), int(row[1].split()[0]), int(row[2], 0)
            published.append((offset, bits, value))
            require(read(offset, bits) == value, f'Chapter 2 published read differs: {row[0]}')
    require(published == [(int(r['offset'], 0), r['width_bits'], int(r['value'], 0))
                          for r in example['raw_reads']], 'Chapter 2 read inventory differs')
    target = next(r for r in topology['role_reads'] if r['bdf'] == '03:00.0')
    require(read(0x0E, 8) == int(target['header'], 0), 'Chapter 2 Header differs from Chapter 1')
    require(read(0x06, 16) & 0x10, 'Chapter 2 Status does not advertise its conventional list')
    for name, start, bits, mask, shift, low, high in [
        ('conventional', read(0x34, 8) & 0xFC, 16, 0xFC, 8, 0x40, 0xFC),
        ('extended', 0x100, 32, 0xFFC, 20, 0x100, 0xFFC),
    ]:
        offsets, ids, pointer = [], [], start
        while pointer:
            require(low <= pointer <= high and pointer % 4 == 0, f'Invalid {name} pointer')
            require(pointer not in offsets, f'Cycle in Chapter 2 {name} list')
            if pointer in offsets or not low <= pointer <= high:
                break
            header = read(pointer, bits)
            offsets.append(pointer)
            ids.append(header & (0xFF if bits == 16 else 0xFFFF))
            pointer = (header >> shift) & mask
        require(offsets == [int(v, 0) for v in example[f'{name}_offsets']],
                f'Chapter 2 {name} route differs')
        require(ids == [int(v, 0) for v in example[f'{name}_ids']], f'Chapter 2 {name} IDs differ')
        if name == 'conventional':
            require(offsets[ids.index(0x10)] == int(topology['cap_base'], 0),
                    'Chapter 2 PCIe Capability differs from Chapter 1')
        else:
            dsn = offsets[ids.index(3)]
            require((read(dsn, 32) >> 16) & 0xF == 1, 'Unexpected DSN version')
            value = (read(dsn + 8, 32) << 32) | read(dsn + 4, 32)
            require(value == int(example['dsn_integer'], 0), 'DSN reconstruction differs')
            require(value.to_bytes(8, 'little').hex('-').upper() == example['eui_bytes'],
                    'DSN-to-EUI byte order differs')


def validate_enumeration_example(example, authored, topology, require):
    rows = table_rows(authored, '教學枚舉時間表：先往下找，再回填範圍', require)
    require([int(row[0]) for row in rows] == list(range(1, 8)), 'Enumeration steps differ')
    configured = {}
    limit = int(example['bus_limit'], 0)
    for action in example['actions']:
        bdf, step = action['bdf'], action['step']
        bus = int(bdf[:2], 16)
        sec, sub = int(action['secondary'], 0), int(action['subordinate'], 0)
        require(0 <= bus < sec <= sub <= limit, f'Invalid teaching Bus range: {bdf}')
        if bus:
            parents = [(p, s, e) for p, (s, e) in configured.items() if s == bus]
            require(len(parents) == 1 and parents[0][2] >= sub,
                    f'Enumeration lacks an enclosing parent for {bdf}')
        for sibling, (s, e) in configured.items():
            if sibling != bdf and sibling[:2] == bdf[:2]:
                require(sub < s or sec > e, f'Temporary sibling ranges overlap: {bdf}, {sibling}')
        configured[bdf] = (sec, sub)
        text = rows[step-1][1] if len(rows) >= step else ''
        # Opening rows identify the new Bridge and both values; closing rows
        # name their prior branch and the new Subordinate.
        if step in (1, 2, 3, 5):
            require(bdf in text and f'Secondary={sec:02X}' in text and
                    f'Subordinate={sub:02X}' in text, f'Published opening step differs: {step}')
        else:
            require(f'Subordinate 改為 {sub:02X}' in text,
                    f'Published closing step differs: {step}')
        for found in [d for d in example['discovered'] if d['step'] == step]:
            target_bus = int(found['bdf'][:2], 16)
            current, seen = 0, set()
            while current != target_bus and current not in seen:
                seen.add(current)
                choices = [s for p, (s, e) in configured.items()
                           if int(p[:2], 16) == current and s <= target_bus <= e]
                require(len(choices) == 1, f'No discovery route to {found["bdf"]}')
                if len(choices) != 1:
                    break
                current = choices[0]
            require(current == target_bus and found['bdf'] in text,
                    f'Published discovery is unreachable or missing: {found["bdf"]}')
            if found['header'] is not None:
                require(f'Header Type={int(found["header"], 0):02X}h' in text,
                        f'Discovery Header differs: {found["bdf"]}')
    expected = {r['bdf']: (int(r['secondary'], 0), int(r['subordinate'], 0))
                for r in topology['topology']}
    require(configured == expected, 'Chapter 3 final ranges differ from Chapter 1')
    rows = table_rows(authored, 'RRS 可見性案例的讀取', require)
    require(len(rows) == len(example['rrs_reads']), 'RRS published read count differs')
    for row, read in zip(rows, example['rrs_reads']):
        require(hex_values(row[0])[-1] == int(read['offset'], 0) and
                int(row[1].split()[0]) == read['width_bits'] and
                int(row[2], 0) == int(read['value'], 0), 'RRS published read differs')
    reads = example['rrs_reads']
    base = int(example['rrs_cap_base'], 0)
    require(int(reads[0]['offset'], 0) == base + 0x1E and int(reads[0]['value'], 0) & 1,
            'RRS support field differs')
    require(int(reads[1]['offset'], 0) == base + 0x1C and int(reads[1]['value'], 0) & 0x10,
            'RRS enable field differs')
    require(int(reads[2]['value'], 0) == (0xFFFF << 16) | 1, 'RRS synthesized value differs')


def validate_resource_example(example, authored, topology, require):
    probes = table_rows(authored, 'BAR 大小探測的假設讀回資料', require)
    allocations = table_rows(authored, '本例的資源配置', require)
    expected_probes, ranges = [], []
    require(len(allocations) == len(example['bars']), 'BAR allocation count differs')
    for bar, row in zip(example['bars'], allocations):
        bits, offset = bar['width_bits'], int(bar['offset'], 0)
        probe, original, assigned = [[int(v, 0) for v in bar[key]]
                                     for key in ['probe', 'original', 'assigned']]
        require(len(probe) == len(original) == len(assigned) == bits // 32,
                'BAR pair width differs')
        require(probe[0] & 1 == 0 and ((probe[0] >> 1) & 3) == (2 if bits == 64 else 0),
                'BAR format conflicts with claimed width')
        require(bool(probe[0] & 8) == bar['prefetchable'], 'BAR Prefetchable flag differs')
        full_mask = (1 << bits) - 1
        address_mask = (probe[0] & 0xFFFFFFF0) | ((probe[1] << 32) if bits == 64 else 0)
        size = ((~address_mask) & full_mask) + 1
        base = (assigned[0] & 0xFFFFFFF0) | ((assigned[1] << 32) if bits == 64 else 0)
        end = base + size - 1
        require(size == int(bar['size'], 0) and size & (size - 1) == 0, 'BAR size differs')
        require(base % size == 0 and end <= full_mask, 'BAR alignment/width invalid')
        require(base == int(bar['base'], 0) and end == int(bar['limit'], 0), 'BAR range differs')
        require(all(end < start or base > stop for start, stop in ranges), 'BAR ranges overlap')
        ranges.append((base, end))
        require(hex_values(row[1]) == [base, end], 'Published BAR range differs')
        assigned_pairs = [part for i, value in enumerate(assigned) for part in (offset + 4*i, value)]
        require(hex_values(row[2]) == assigned_pairs, 'Published BAR programming differs')
        for i, value in enumerate(probe):
            require(assigned[i] & (0xF if i == 0 else 0) == original[i] & (0xF if i == 0 else 0),
                    'BAR programming changes type bits')
            expected_probes.append((offset + i*4, original[i], value))
    require([(hex_values(r[0])[0], int(r[1], 0), int(r[2], 0)) for r in probes] == expected_probes,
            'Published BAR probe values differ')
    registers = {int(r['offset'], 0): int(r['value'], 0) for r in example['window_registers']}
    windows = [
        ((registers[0x20] & 0xFFF0) << 16, ((registers[0x22] & 0xFFF0) << 16) | 0xFFFFF),
        ((registers[0x28] << 32) | ((registers[0x24] & 0xFFF0) << 16),
         (registers[0x2C] << 32) | ((registers[0x26] & 0xFFF0) << 16) | 0xFFFFF),
    ]
    require(registers[0x24] & 0xF == registers[0x26] & 0xF == 1,
            'Prefetchable Window is not encoded as 64-bit')
    for bar, (base, end) in zip(example['bars'], ranges):
        lower, upper = windows[int(bar['prefetchable'])]
        require(lower <= base <= end <= upper, 'Bridge Window does not contain BAR')
    require(example['window_path'] == topology['expected_bridge_path'],
            'Chapter 4 Window path differs from Chapter 1')
    rows = table_rows(authored, '本例三個 Bridge 都採用的 Window 設定', require)
    require(len(rows) == 3, 'Published Window row count differs')
    for row, offsets, width in zip(rows, [(0x20, 0x22), (0x24, 0x26), (0x28, 0x2C)], [16, 16, 32]):
        require(hex_values(row[1]) == list(offsets) and f'{width} bits' in row[1] and
                hex_values(row[2]) == [registers[o] for o in offsets], 'Published Window differs')
    relative = int(example['mmio_offset'], 0)
    require(0 <= relative < int(example['bars'][0]['size'], 0), 'MMIO offset is outside BAR0')
    require(ranges[0][0] + relative == int(example['mmio_address'], 0), 'MMIO address differs')


def validate_transfer_examples(claims, require):
    """Recompute transfers and MSI-X locations, then reconcile published tables."""
    evidence = {c['id']: c for c in claims}
    def example(n):
        return evidence[f'PCIE-CH{n}-EXAMPLE-001']
    def doc(n):
        return Document((DATA / f'chapter{n}.zh.html').read_text(encoding='utf-8'))
    def value(v):
        return int(v, 0) if isinstance(v, str) else v

    if 'PCIE-CH5-EXAMPLE-001' in evidence:
        e, authored = example(5), doc(5)
        single = e['single']
        require(single['address'] == example(4)['mmio_address'], 'Chapter 5 MMIO differs from Chapter 4')
        require(int.from_bytes(bytes.fromhex(single['payload_bytes']), 'little') == value(single['register_value']),
                'Chapter 5 byte reconstruction mismatch')
        for request in [single, e['partial']]:
            address, length = value(request['address']), request['length_dw']
            require(address % 4 == 0, 'Request address is not DWORD aligned')
            enabled = [address + dw * 4 + bit for dw in range(length) for bit in range(4)
                       if ((request['first_be'] if dw == 0 else request['last_be'] if dw == length-1 else 15) >> bit) & 1]
            require(len(enabled) == request['byte_count'], 'Enabled byte count mismatch')
            require(enabled[0] & 127 == value(request['lower_address']), 'Lower Address mismatch')
            if length == 1:
                require(request['last_be'] == 0, 'One-DW Last BE must be zero')
            else:
                require(enabled == list(range(value(request['first_enabled']), value(request['last_enabled'])+1)),
                        'Partial read enabled range mismatch')
        rows = table_rows(authored, '本例的單筆讀取欄位', require)
        if len(rows) == 6:
            require(re.findall(r'[01]+b', rows[0][1]) == ['000b', '00000b'] and
                    re.findall(r'[01]+b', rows[0][2]) == ['010b', '01010b'], 'Published MRd/CplD encoding differs')
            require(hex_values(rows[1][1]) == [value(single['requester']), value(single['tag'])] == hex_values(rows[1][2]),
                    'Published transaction IDs differ')
            require(hex_values(rows[2][1]) == [value(single['address'])] and
                    hex_values(rows[2][2]) == [value(single['completer'])], 'Published address/Completer differs')
            require(re.findall(r'[01]+b', rows[4][1]) == ['1111b', '0000b'], 'Published one-DW BEs differ')
        else:
            require(False, 'Missing single-read field rows')
        split = e['split']
        address, total = value(split['address']), split['length_dw'] * 4
        require(total <= split['mrrs'] and address // 4096 == (address+total-1) // 4096, 'Illegal split-read Request')
        rows = table_rows(authored, '同一筆 256-byte 讀取的兩個回覆', require)
        require(len(rows) == len(split['completions']), 'Published Completion count differs')
        remaining, cursor = total, address
        for i, completion in enumerate(split['completions']):
            size = completion['length_dw'] * 4
            require(value(completion['address']) == cursor and completion['byte_count'] == remaining,
                    'Completion address or remaining Byte Count mismatch')
            require(size <= split['payload_limit'] and value(completion['lower_address']) == cursor & 127,
                    'Completion payload or Lower Address mismatch')
            if i < len(split['completions'])-1:
                require((cursor+size) % split['rcb'] == 0, 'Completion split misses RCB boundary')
            if i < len(rows):
                row = rows[i]
                require(hex_values(row[1]) == [cursor, cursor+size-1] and int(row[2]) == size//4 and
                        int(row[3]) == remaining and hex_values(row[4]) == [cursor & 127],
                        'Published split-read row differs from recomputed transfer')
            cursor += size
            remaining -= size
        require(remaining == 0, 'Split Completions do not cover the Request')
        b = e['boundary']; cursor = value(b['address'])
        require(cursor // 4096 != (cursor+b['size']-1) // 4096, 'Boundary counterexample does not cross 4 KiB')
        for part in b['pieces']:
            require(value(part['address']) == cursor and cursor // 4096 == (cursor+part['size']-1) // 4096,
                    'Boundary fix is noncontiguous or crosses 4 KiB')
            cursor += part['size']
        require(cursor == value(b['address'])+b['size'], 'Boundary fix changes requested range')

    if 'PCIE-CH6-EXAMPLE-001' in evidence:
        e, authored = example(6), doc(6)
        base, size = value(e['dma_base']), e['mapping_size']
        require(base % 4096 == value(e['physical_base']) % 4096 == 0, 'Teaching DMA pages misaligned')
        for addr, length in [(e['data_address'], e['data_size']), (e['flag_address'], e['flag_size'])]:
            require(base <= value(addr) and value(addr)+length <= base+size, 'DMA write outside valid mapping')
        rows = table_rows(authored, '本例的 DMA 映射假設', require)
        if len(rows) == 4:
            physical = value(e['physical_base'])
            require(hex_values(rows[1][1]) == [physical, physical+size-1], 'Published CPU physical range differs')
            require(hex_values(rows[2][1]) == [base, base+size-1], 'Published DMA range differs')
            bar = example(4)['bars'][0]
            require(hex_values(rows[3][1]) == [value(bar['base']), value(bar['limit'])], 'Published BAR range differs')
        else:
            require(False, 'Missing DMA address rows')
        control = value(e['device_control'])
        require(128 << ((control >> 12) & 7) == e['mrrs'] == example(5)['split']['mrrs'], 'MRRS inconsistent across chapters')
        require(control & 0x810 == 0x810 and value(e['device_control_offset']) == 0x70+8,
                'Attribute permission example differs')
        rows = table_rows(authored, '本例 Device Control 的能力使用許可', require)
        require(len(rows) == 3 and [r[1] for r in rows] == ['1', '1', '010b'], 'Published Device Control decoding differs')

    if 'PCIE-CH7-EXAMPLE-001' in evidence:
        e, authored = example(7), doc(7)
        reads = {value(r['offset']): value(r['value']) for r in e['raw_reads']}
        cap = value(e['capability'])
        prior = {value(r['offset']): value(r['value']) for r in example(2)['raw_reads']}
        require(reads[cap] == prior[cap] and reads[cap] & 255 == 0x11, 'MSI-X no longer matches Chapter 2 list')
        rows = table_rows(authored, 'MSI-X 定位案例的設定讀值', require)
        require(len(rows) == len(e['raw_reads']), 'MSI-X read table row count differs')
        for row, read in zip(rows, e['raw_reads']):
            require(hex_values(row[0]) == [value(read['offset'])] and int(row[1].split()[0]) == read['width_bits'] and
                    hex_values(row[2]) == [value(read['value'])], 'Published MSI-X read differs')
        base, size = value(e['bar_base']), value(e['bar_size'])
        bar = example(4)['bars'][0]
        require(base == value(bar['base']) and size == value(bar['size']), 'MSI-X BAR differs from Chapter 4')
        n = (reads[cap+2] & 0x7FF)+1
        require(n == e['table_entries'] and 0 <= e['entry_index'] < n, 'Invalid table count or entry index')
        ranges = []
        for offset, name, length in [(4, 'table_base', n*16), (8, 'pba_base', ((n+63)//64)*8)]:
            raw = reads[cap+offset]
            require(raw & 7 == 0, 'Example unexpectedly selects another BAR')
            start = base+(raw & ~7)
            require(start == value(e[name]) and base <= start and start+length <= base+size, 'MSI-X structure outside BAR')
            require(start // 4096 != value(example(4)['mmio_address']) // 4096, 'MSI-X shares ordinary Register page')
            ranges.append((start, start+length))
        require(ranges[0][1] <= ranges[1][0] or ranges[1][1] <= ranges[0][0], 'MSI-X Table/PBA overlap')
        entry = value(e['table_base'])+e['entry_index']*16
        require(entry == value(e['entry_base']), 'MSI-X entry address mismatch')
        rows = table_rows(authored, 'Entry 3 的教學設定值', require)
        require(len(rows) == 4, 'MSI-X entry table must have four DWORD fields')
        for i, row in enumerate(rows):
            require(hex_values(row[0]) == [entry+i*4] and hex_values(row[2]) == [value(e['entry_values'][i])],
                    'Published entry field address or value differs')
        require(value(e['entry_values'][0]) % 4 == 0, 'Interrupt destination is not DWORD aligned')
        require(value(e['pending_qword']) == 1 << (e['entry_index'] % 64), 'PBA pending bit mismatch')
        states = [value(v) for v in e['control_states']]
        require([((v >> 15) & 1, (v >> 14) & 1, v & 0x7FF) for v in states] == [(0,1,n-1),(1,1,n-1),(1,0,n-1)],
                'MSI-X control transitions differ')
        rows = table_rows(authored, '讓 entry 3 安全進入可通知狀態', require)
        require(len(rows) == 5 and [hex_values(rows[i][1]) for i in (0,2,3)] == [[v] for v in states],
                'Published MSI-X initialization states differ')
        msi = value(e['msi_comparison'])
        require((msi >> 1) & 7 == 2 and (msi >> 4) & 7 == 0 and msi & 1 == 0 and (msi >> 7) & 7 == 3,
                'Independent MSI comparison decodes incorrectly')


def validate_link_reset_power_examples(claims, require, documents=None):
    """Decode new examples, then reconcile the actual published tables.

    Optional documents let maintenance checks corrupt HTML in memory without
    touching authored files. This is arithmetic/consistency, not spec proof.
    """
    by_id = {claim['id']: claim for claim in claims}
    documents = documents or {}

    def doc(number):
        return documents.get(number) or Document(
            (DATA / f'chapter{number}.zh.html').read_text(encoding='utf-8'))

    def number_cells(row):
        return [int(value) for value in re.findall(r'\d+', ' '.join(row))]

    example = by_id.get('PCIE-CH8-EXAMPLE-001')
    if example:
        link = example['link']
        vectors = [(int(value, 0) & 0xFE) >> 1 for value in link['cap2']]
        current = [int(value, 0) & 0xF for value in link['status']]
        widths = [(int(value, 0) >> 4) & 0x3F for value in link['status']]
        target = int(link['target'], 0) & 0xF
        require(vectors == [15, 15] and current == [3, 3] and target == 3,
                'Chapter 8 supported/target/current speed mismatch')
        require(widths == [4, 4] and all(w <= maximum for w, maximum in zip(widths, link['widths'])),
                'Chapter 8 negotiated width exceeds capability or differs across Link')
        for status, reporting in zip(link['status'], link['active_reporting']):
            require(bool(int(status, 0) & (1 << 13)) == reporting,
                    'Chapter 8 Link Active reporting assumption mismatch')
        rows = table_rows(doc(8), '速率案例的兩端證據', require)
        if len(rows) == 4:
            base = int(link['cap_base'], 0)
            require(hex_values(rows[0][0]) == [base + 0x2C] and
                    [hex_values(cell)[0] for cell in rows[0][1:]] == [int(v, 0) for v in link['cap2']],
                    'Chapter 8 published speed capability reads drifted')
            require(number_cells(rows[1][1:]) == link['widths'], 'Chapter 8 published max widths drifted')
            require(hex_values(rows[2][0]) == [base + 0x30] and hex_values(rows[2][1]) == [int(link['target'], 0)],
                    'Chapter 8 published target read drifted')
            require(hex_values(rows[3][0]) == [base + 0x12] and
                    [hex_values(cell)[0] for cell in rows[3][1:]] == [int(v, 0) for v in link['status']],
                    'Chapter 8 published status reads drifted')
        else:
            require(False, 'Chapter 8 speed table row count changed')
        credit = example['credit']
        demands = [(size + 15) // 16 for size in credit['payloads']]
        ph, pd = credit['initial_ph'] - 1, credit['initial_pd'] - demands[0]
        require(ph == 1 and pd == 1 and pd < demands[1] <= pd + credit['pd_return'],
                'Chapter 8 credit wait/release example invalid')
        rows = table_rows(doc(8), '有限 credit 的發送判斷', require)
        if len(rows) == 4:
            require(number_cells(rows[0][:2]) == [credit['payloads'][0], 1, demands[0]] and
                    number_cells(rows[0][2:]) == [ph, pd], 'Chapter 8 first credit row drifted')
            require(number_cells(rows[1][:2]) == [credit['payloads'][1], 1, demands[1]],
                    'Chapter 8 blocked credit row drifted')
            require(number_cells(rows[2]) == [credit['pd_return'], credit['payloads'][1], 1, demands[1], 0, 0],
                    'Chapter 8 released credit row drifted')
            require(number_cells(rows[3][:2]) == [credit['mrd_bytes'], credit['nph'], 1, 0],
                    'Chapter 8 MRd credit row drifted')
        else:
            require(False, 'Chapter 8 credit table row count changed')
        ranges = example['flit_ranges']
        require([size for _, _, size in ranges] == [236, 6, 8, 6], 'Chapter 8 Flit partition mismatch')
        require(sum(size for _, _, size in ranges) == 256 and ranges[0][0] == 0 and ranges[-1][1] == 255,
                'Chapter 8 Flit total size mismatch')
        require(all(end - start + 1 == size for start, end, size in ranges) and
                all(a[1] + 1 == b[0] for a, b in zip(ranges, ranges[1:])),
                'Chapter 8 Flit ranges overlap or leave gaps')
        rows = table_rows(doc(8), '一個 Flit 的 256 bytes 分配', require)
        require([number_cells(row[:2]) for row in rows] == ranges, 'Chapter 8 published Flit ranges drifted')
        require([((int(v, 0) >> 12) & 7, (int(v, 0) >> 10) & 1)
                 for v in example['flit_projections']] == [(4, 1), (3, 1)], 'Chapter 8 Presence/Flit decode mismatch')

    example = by_id.get('PCIE-CH9-EXAMPLE-001')
    if example:
        reads = {int(offset, 0): (width, int(value, 0)) for offset, width, value in example['raw_reads']}
        require((reads[0x74][1] >> 28) & 1 == 1 and (reads[0x7A][1] >> 5) & 1 == 1,
                'Chapter 9 FLR support/pending decode mismatch')
        require(reads[0x78][1] & 0x8000 == 0 and reads[0x04][1] & 6 == 6,
                'Chapter 9 initial Control/Command mismatch')
        require(reads[0x78][1] | 0x8000 == int(example['trigger'], 0), 'Chapter 9 trigger changes unrelated bits')
        rows = table_rows(doc(9), 'FLR 案例的設定讀值', require)
        require(len(rows) == len(reads), 'Chapter 9 read table row count changed')
        for row in rows:
            offsets, values = hex_values(row[0]), hex_values(row[1])
            require(len(offsets) == len(values) == 1, 'Chapter 9 read cell malformed')
            if len(offsets) == len(values) == 1:
                width = int(re.search(r'(16|32) bits', row[0]).group(1))
                require(reads.get(offsets[0]) == (width, values[0]), 'Chapter 9 published raw read drifted')
        timeline = example['timeline_ms']
        require(timeline['reset_exit'] <= timeline['training_complete'] and timeline['wait'] >= 100 and
                timeline['first_config'] == timeline['training_complete'] + timeline['wait'],
                'Chapter 9 Conventional Reset timing origin mismatch')

    example = by_id.get('PCIE-CH10-EXAMPLE-001')
    if example:
        pmc = int(example['pm_reads'][0][2], 0)
        pmcsr = int(example['pm_reads'][1][2], 0)
        require(pmc & 0xFF == 1 and (pmc >> 16) & 7 == 3 and (pmc >> 25) & 3 == 0 and
                (pmc >> 27) & 0x1F == 0x19 and pmc & (1 << 20) == 0,
                'Chapter 10 PM support/readiness decode mismatch')
        require(pmcsr & 3 == 3 and pmcsr & 0x8108 == 0x8108, 'Chapter 10 initial PMCSR mismatch')
        write_d0 = pmcsr & ~0x8003
        after_d0 = (pmcsr & ~3)
        clear_event = after_d0
        require([pmcsr, write_d0, after_d0, clear_event] == [int(v, 0) for v in example['pm_sequence']],
                'Chapter 10 RW1CS preservation/clear sequence mismatch')
        rows = table_rows(doc(10), 'PM 能力與狀態的教學讀值', require)
        require([[hex_values(row[0])[0], hex_values(row[1])[0]] for row in rows] ==
                [[int(offset, 0), int(value, 0)] for offset, _, value in example['pm_reads']],
                'Chapter 10 published PM reads drifted')
        rows = table_rows(doc(10), '回到 D0，但不意外清除 PME 事件', require)
        require([hex_values(row[1])[0] for row in rows] == [int(v, 0) for v in example['pm_sequence']],
                'Chapter 10 published PM write sequence drifted')
        raw = [[int(v, 0) for v in row] for row in example['l1ss_reads']]
        rows = table_rows(doc(10), 'L1.2 案例的兩端讀值', require)
        require([[hex_values(cell)[0] for cell in row] for row in rows] == raw,
                'Chapter 10 published L1SS snapshot drifted')
        require([row[0] for row in raw] == [0x200, 0x204, 0x208, 0x20C], 'Chapter 10 L1SS offsets mismatch')
        require(all(v & 0xFFFF == 0x1E and (v >> 16) & 0xF == 1 and v >> 20 == 0 for v in raw[0][1:]),
                'Chapter 10 L1SS ID/version/next mismatch')
        scale_us = [2, 10, 100]
        cap_times, programmed_times, thresholds = [], [], []
        for column in (1, 2):
            cap, ctrl1, ctrl2 = (raw[row][column] for row in (1, 2, 3))
            require(cap & 0x1F == 0x1F and ctrl1 & 0xF == 4,
                    'Chapter 10 corresponding support/enable mismatch')
            cap_scale, ctrl_scale = (cap >> 16) & 3, ctrl2 & 3
            require(cap_scale < 3 and ctrl_scale < 3, 'Chapter 10 Reserved T_POWER_ON scale')
            if cap_scale < 3 and ctrl_scale < 3:
                cap_times.append(((cap >> 19) & 0x1F) * scale_us[cap_scale])
                programmed_times.append(((ctrl2 >> 3) & 0x1F) * scale_us[ctrl_scale])
            threshold_scale = ctrl1 >> 29
            require(threshold_scale <= 5, 'Chapter 10 forbidden LTR scale')
            thresholds.append(((ctrl1 >> 16) & 0x3FF) * (1 << (5 * threshold_scale)))
        require(cap_times == [10, 100] and programmed_times == [100, 100], 'Chapter 10 T_POWER_ON units mismatch')
        require((raw[2][1] >> 8) & 0xFF == 20 and (raw[2][2] >> 8) & 0xFF == 0,
                'Chapter 10 UP RsvdP/DP common-mode mismatch')
        require(thresholds == [example['threshold_ns']] * 2, 'Chapter 10 thresholds differ across Link')
        rows = table_rows(doc(10), '同一個 threshold 下的兩次判斷', require)
        require(len(rows) == len(example['ltr_cases']), 'Chapter 10 LTR row count changed')
        for case, row in zip(example['ltr_cases'], rows):
            eligible = case['snoop_ns'] >= thresholds[0] and case['no_snoop_ns'] >= thresholds[0]
            require(eligible == case['eligible'], 'Chapter 10 LTR branch result mismatch')
            require(number_cells(row[1:3]) == [case['snoop_ns'], case['no_snoop_ns']],
                    'Chapter 10 published LTR inputs drifted')


def validate(source_dir=None):
    errors = []
    def require(condition, message):
        if not condition:
            errors.append(message)

    registry = json.loads((DATA / 'source-register.json').read_text(encoding='utf-8'))
    curriculum = json.loads((DATA / 'curriculum.json').read_text(encoding='utf-8'))['chapters']
    ready = sorted((c for c in curriculum if c['status'] == 'ready'), key=lambda c: c['number'])
    claim_paths = [DATA / ('claims.json' if c['number'] == 0 else f"chapter{c['number']}-claims.json") for c in ready]
    claims = []
    for path in claim_paths:
        require(path.is_file(), f'Missing evidence: {path.name}')
        if path.is_file():
            chapter_claims = json.loads(path.read_text(encoding='utf-8'))['claims']
            require(bool(chapter_claims), f'Empty evidence: {path.name}')
            claims.extend(chapter_claims)
    sources = {s['id']: s for s in registry['sources']}
    require(len(sources) == len(registry['sources']), 'Duplicate source IDs')
    require(len({c['id'] for c in claims}) == len(claims), 'Duplicate claim IDs')
    for claim in claims:
        require(claim.get('status') == 'verified', f"Unverified claim: {claim['id']}")
        source = sources.get(claim['source_id'])
        require(source is not None, f"Unknown source: {claim['id']}")
        require(bool(claim.get('revision')), f"Missing source revision: {claim['id']}")
        if source and source.get('type') == 'local_pdf':
            require(bool(claim.get('sections')), f"Missing section: {claim['id']}")
            require(bool(claim.get('pdf_pages')), f"Missing page: {claim['id']}")
            require(bool(claim.get('document_pages')), f"Missing document page: {claim['id']}")
            require(all(1 <= p <= source['page_count'] for p in claim.get('pdf_pages', [])),
                    f"Invalid page range: {claim['id']}")
        for calculation in claim.get('calculations', []):
            require(arithmetic(calculation['expression']) == int(calculation['result'], 0),
                    f"Incorrect arithmetic: {calculation['expression']}")

    example = next(c for c in claims if c['id'] == 'PCIE-CH0-EXAMPLE-001')
    memory = {}
    for read in example['raw_reads']:
        offset, bits, value = int(read['offset'], 0), read['width_bits'], int(read['value'], 0)
        require(bits in (8, 16, 32) and 0 <= value < 2**bits, f'Invalid raw read: {read}')
        for i, byte in enumerate(value.to_bytes(bits // 8, 'little')):
            require(offset+i not in memory or memory[offset+i] == byte, 'Conflicting raw bytes')
            memory[offset+i] = byte

    def read_at(offset, width):
        return int.from_bytes(bytes(memory[offset+i] for i in range(width // 8)), 'little')

    pointer = read_at(0x34, 8) & 0xFC
    seen, cap = set(), None
    while pointer:
        require(0x40 <= pointer <= 0xFC and pointer % 4 == 0, 'Invalid capability pointer')
        if pointer in seen:
            errors.append('Capability list loops')
            break
        seen.add(pointer)
        if read_at(pointer, 8) == 0x10:
            cap = pointer
            break
        pointer = read_at(pointer+1, 8)
    require(cap == 0x70, 'Example does not locate the expected PCIe capability')
    if cap is not None:
        capability = read_at(cap + 2, 16)
        speeds = read_at(cap + 0x2C, 32)
        status = read_at(cap + 0x12, 16)
        vector = (speeds & 0xFE) >> 1
        speed_code, width = status & 0xF, (status >> 4) & 0x3F
        require(capability & 0xF == 2 and (capability >> 4) & 0xF == 0, 'Example type/version mismatch')
        require(vector == 0xF and speed_code == 3 and width == 4, 'Worked-example conclusion mismatch')
        require(bool(vector & (1 << (speed_code - 1))), 'Current speed is absent from supported vector')
        if vector & 0b111000:
            require(speeds & 0x01800000 == 0x01800000, '16 GT/s example omits required retimer detection bits')

    authored = Document((DATA / 'chapter0.zh.html').read_text(encoding='utf-8'))
    raw = next(t for t in authored.tables if t['caption'] == '本例取得的設定資料')
    for offset_text, width_text, value_text, _meaning in raw['rows'][1:]:
        offset, bits, value = int(offset_text, 0), int(width_text.split()[0]), int(value_text, 0)
        require(read_at(offset, bits) == value, f'Published example differs from evidence: {offset_text}')

    if any(chapter['number'] == 1 for chapter in ready):
        topology_example = next((claim for claim in claims if claim['id'] == 'PCIE-CH1-EXAMPLE-001'), None)
        require(topology_example is not None, 'Missing Chapter 1 topology example')
        if topology_example is not None:
            topology_authored = Document((DATA / 'chapter1.zh.html').read_text(encoding='utf-8'))
            validate_topology_example(topology_example, topology_authored, require)

    for number, validator in [(2, validate_configuration_example), (3, validate_enumeration_example),
                              (4, validate_resource_example)]:
        if not any(chapter['number'] == number for chapter in ready):
            continue
        example = next((c for c in claims if c['id'] == f'PCIE-CH{number}-EXAMPLE-001'), None)
        require(example is not None, f'Missing Chapter {number} example')
        if example is not None:
            authored = Document((DATA / f'chapter{number}.zh.html').read_text(encoding='utf-8'))
            validator(example, authored, topology_example, require)

    validate_transfer_examples(claims, require)
    for number in (8, 9, 10):
        if any(chapter['number'] == number for chapter in ready):
            require(any(c['id'] == f'PCIE-CH{number}-EXAMPLE-001' for c in claims),
                    f'Missing Chapter {number} worked example')
    validate_link_reset_power_examples(claims, require)

    chapter_numbers = [c['number'] for c in curriculum]
    require(len(set(chapter_numbers)) == len(chapter_numbers), 'Duplicate chapter numbers')
    require(0 in [c['number'] for c in ready], 'Chapter 0 must be ready')
    for chapter in curriculum:
        require(chapter['status'] in {'ready', 'planned'}, f"Unknown status: Chapter {chapter['number']}")
        require(all(p in chapter_numbers and p < chapter['number'] for p in chapter['prerequisites']),
                f"Invalid prerequisite: Chapter {chapter['number']}")
        if chapter['status'] == 'ready':
            require(all(source in sources for source in chapter['sources']),
                    f"Unknown published source: Chapter {chapter['number']}")
            require(all(p in [c['number'] for c in ready] for p in chapter['prerequisites']),
                    f"Unpublished prerequisite: Chapter {chapter['number']}")

    paths = [OUTPUT / 'index.html']
    permalinks = {}
    for chapter in ready:
        number = chapter['number']
        paths.append(OUTPUT / f'chapter-{number}.html')
        require((DATA / f'chapter{number}.zh.html').is_file(), f'Missing authored tutorial: Chapter {number}')
        for language, slug in [('zh', 'zh-tw'), ('en', 'en')]:
            authored_post = DATA / (f'post.{language}.html' if number == 0 else f'chapter{number}.post.{language}.html')
            require(authored_post.is_file(), f'Missing authored {language} post: Chapter {number}')
            date = chapter.get('publication_date', '2026-10-19')
            path = ROOT / f'_posts/{date}-pcie-chapter-{number}-{slug}.md'
            paths.append(path)
            permalinks[f'/pcie/chapter-{number}-{slug}/'] = path
    documents = {path: Document(path.read_text(encoding='utf-8')) for path in paths if path.is_file()}
    for path in paths:
        require(path.exists(), f'Missing generated file: {path}')
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8')
        doc = documents[path]
        require(not [k for k, n in Counter(doc.ids).items() if n > 1], f'Duplicate HTML ID: {path.name}')
        require(not any(tag in {'script', 'iframe', 'object', 'embed'} for tag, _ in doc.tags),
                f'Offline artifact contains active/external embed: {path.name}')
        require(not any(tag == 'link' and 'stylesheet' in attrs.get('rel', '') for tag, attrs in doc.tags),
                f'Offline artifact requires external stylesheet: {path.name}')
        if path.suffix == '.html':
            require(any(tag == 'html' and attrs.get('lang') == 'zh-Hant-TW' for tag, attrs in doc.tags),
                    f'Incorrect language: {path.name}')
        else:
            permalink = next((link for link, target in permalinks.items() if target == path), None)
            require(re.search(r'^permalink: ' + re.escape(permalink or '') + r'$', text, re.M),
                    f'Incorrect post permalink: {path.name}')
            expected_language = 'zh-Hant-TW' if path.stem.endswith('-zh-tw') else 'en'
            require(any(attrs.get('lang') == expected_language for _, attrs in doc.tags),
                    f'Incorrect post language: {path.name}')
        for href in doc.links:
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc:
                continue
            target = (ROOT / unquote(parsed.path).lstrip('/')) if parsed.path.startswith('/') else (path.parent / unquote(parsed.path))
            if not parsed.path:
                target = path
            if parsed.path.startswith('/pcie/'):
                target = permalinks.get(unquote(parsed.path))
                require(target is not None, f'Unknown course permalink: {path.name}: {href}')
                if target is None:
                    continue
            require(target.is_file(), f'Broken local link: {path.name}: {href}')
            if parsed.fragment and target.is_file():
                target_doc = documents.get(target) or Document(target.read_text(encoding='utf-8'))
                require(unquote(parsed.fragment) in target_doc.ids, f'Broken fragment: {path.name}: {href}')
        require('C:\\Users\\' not in text and '.ai/pcie-course' not in text, f'Internal paths exposed: {path.name}')
        require(not any(s in text for s in ('TO-SELECT', 'TO-VERIFY', '{{title}}', '{{body}}')), f'Unresolved metadata: {path.name}')
    for path in OUTPUT.rglob('*'):
        require(path.suffix.lower() != '.pdf', 'Source PDF included in public output')

    if source_dir:
        for source in sources.values():
            if source['type'] != 'local_pdf':
                continue
            filename = source['filename']
            path = Path(source_dir) / filename
            require(path.is_file(), f'Missing source PDF: {filename}')
            if path.is_file():
                require(hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256'], f'Source changed: {filename}')

    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'Validated {len(claims)} claims, {len(curriculum)} planned/ready chapters, '
          f'{len(raw["rows"])-1} Chapter 0 reads, arithmetic, capability chain, and links across {len(paths)} artifacts.')
    if any(chapter['number'] == 1 for chapter in ready):
        print('Chapter 1 role bytes, bridge ranges, derived path, and Requester ID match the evidence.')
    if any(chapter['number'] == 4 for chapter in ready):
        print('Chapters 2–4 list/DSN reads, staged enumeration, RRS fields, BAR sizes, '
              'allocations, and Bridge Windows match their published tables and Chapter 1.')
    if source_dir:
        print('Both source PDF hashes match the registered editions.')
    if any(chapter['number'] == 7 for chapter in ready):
        print('Chapters 5–7 transfer bytes, Completion fragments, DMA ranges, and MSI-X locations match their published tables.')
    if any(chapter['number'] == 10 for chapter in ready):
        print('Chapters 8–10 Link fields, credits, Flit ranges, FLR, PMCSR writes, and L1.2 timing match their published tables.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, help='Optionally verify both original PDF hashes')
    args = parser.parse_args()
    validate(args.source_dir)

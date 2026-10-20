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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, help='Optionally verify both original PDF hashes')
    args = parser.parse_args()
    validate(args.source_dir)

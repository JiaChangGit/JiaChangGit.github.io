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
    operations = {ast.Add: operator.add, ast.BitAnd: operator.and_, ast.BitOr: operator.or_,
                  ast.RShift: operator.rshift, ast.LShift: operator.lshift}
    def compute(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in operations:
            return operations[type(node.op)](compute(node.left), compute(node.right))
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
    if source_dir:
        print('Both source PDF hashes match the registered editions.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, help='Optionally verify both original PDF hashes')
    args = parser.parse_args()
    validate(args.source_dir)

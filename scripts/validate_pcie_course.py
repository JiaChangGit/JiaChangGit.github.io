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


def validate(source_dir=None):
    errors = []
    def require(condition, message):
        if not condition:
            errors.append(message)

    registry = json.loads((DATA / 'source-register.json').read_text(encoding='utf-8'))
    claims = json.loads((DATA / 'claims.json').read_text(encoding='utf-8'))['claims']
    curriculum = json.loads((DATA / 'curriculum.json').read_text(encoding='utf-8'))['chapters']
    sources = {s['id']: s for s in registry['sources']}
    require(len(sources) == len(registry['sources']), 'Duplicate source IDs')
    require(len({c['id'] for c in claims}) == len(claims), 'Duplicate claim IDs')
    for claim in claims:
        require(claim.get('status') == 'verified', f"Unverified claim: {claim['id']}")
        source = sources.get(claim['source_id'])
        require(source is not None, f"Unknown source: {claim['id']}")
        if source and source.get('type') == 'local_pdf':
            require(bool(claim.get('sections')), f"Missing section: {claim['id']}")
            require(bool(claim.get('pdf_pages')), f"Missing page: {claim['id']}")
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

    chapter_numbers = [c['number'] for c in curriculum]
    require(len(set(chapter_numbers)) == len(chapter_numbers), 'Duplicate chapter numbers')
    require([c['number'] for c in curriculum if c['status'] == 'ready'] == [0], 'Unexpected ready chapter')
    for chapter in curriculum:
        require(all(p in chapter_numbers and p < chapter['number'] for p in chapter['prerequisites']),
                f"Invalid prerequisite: Chapter {chapter['number']}")

    paths = [OUTPUT / 'chapter-0.html', OUTPUT / 'index.html']
    for path in paths:
        require(path.exists(), f'Missing generated file: {path}')
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8')
        doc = Document(text)
        require(not [k for k, n in Counter(doc.ids).items() if n > 1], f'Duplicate HTML ID: {path.name}')
        require(not any(tag in {'script', 'iframe', 'object', 'embed'} for tag, _ in doc.tags),
                f'Offline artifact contains active/external embed: {path.name}')
        require(not any(tag == 'link' and 'stylesheet' in attrs.get('rel', '') for tag, attrs in doc.tags),
                f'Offline artifact requires external stylesheet: {path.name}')
        require(any(tag == 'html' and attrs.get('lang') == 'zh-Hant-TW' for tag, attrs in doc.tags),
                f'Incorrect language: {path.name}')
        for href in doc.links:
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc:
                continue
            target = (ROOT / unquote(parsed.path).lstrip('/')) if parsed.path.startswith('/') else (path.parent / unquote(parsed.path))
            if not parsed.path:
                target = path
            # Site permalinks are checked against the Jekyll output, separately.
            if parsed.path.startswith('/pcie/'):
                continue
            require(target.is_file(), f'Broken local link: {path.name}: {href}')
            if parsed.fragment and target.is_file():
                target_doc = doc if target == path else Document(target.read_text(encoding='utf-8'))
                require(unquote(parsed.fragment) in target_doc.ids, f'Broken fragment: {path.name}: {href}')
        require('C:\\Users\\' not in text and '.ai/pcie-course' not in text, f'Internal paths exposed: {path.name}')
        require(not any(s in text for s in ('TO-SELECT', 'TO-VERIFY', '{{title}}', '{{body}}')), f'Unresolved metadata: {path.name}')
    for path in OUTPUT.glob('*'):
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
          f'{len(raw["rows"])-1} published reads, arithmetic, capability chain, and offline links.')
    if source_dir:
        print('Both source PDF hashes match the registered editions.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, help='Optionally verify both original PDF hashes')
    args = parser.parse_args()
    validate(args.source_dir)

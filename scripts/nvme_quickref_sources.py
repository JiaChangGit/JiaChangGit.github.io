#!/usr/bin/env python3
"""Verify quick-reference locations against the user's PDFs (never publish PDFs)."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.nvme_scenario_render import CASES, refs

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / '.ai/nvme-quickref'

def digest(text):
    return hashlib.sha256(re.sub(r'\s+', ' ', text).strip().encode()).hexdigest()

def verify(source_dir, register=None, refresh_scenarios=False):
    register = register or json.loads((CONTROL / 'figures.json').read_text())
    sources = json.loads((ROOT / '.ai/nvme-report/source-register.json').read_text())['sources']
    count = 0
    evidence = {}
    selected = sorted({token for c in CASES for token in c['sources']})
    prefixes = {key[0]: row['source_id'] for key, row in register['figures'].items()}
    for source in sources:
        path = Path(source_dir) / source['filename']
        if hashlib.sha256(path.read_bytes()).hexdigest() != source['sha256']:
            raise ValueError(f"Source file changed: {source['id']}")
        pages = subprocess.check_output(['pdftotext', '-layout', str(path), '-']).decode().split('\f')
        for token in selected:
            ref = refs(token, register['figures'])
            if prefixes[ref['prefix']] != source['id']:
                continue
            content = '\f'.join(pages[p-1] for p in ref['pages'])
            evidence[token] = dict(source_id=source['id'], section=ref['section'],
                                   pdf_pages=ref['pages'], page_text_sha256=digest(content))
        for key, figure in register['figures'].items():
            if figure['source_id'] != source['id']:
                continue
            start, end = figure['pdf_pages']
            content = '\f'.join(pages[start-1:end])
            if not re.search(r'Figure\s+' + str(figure['number']) + r'\s*:', content):
                raise ValueError(f'Figure heading absent: {key}')
            if digest(content) != figure['page_text_sha256']:
                raise ValueError(f'Source page evidence changed: {key}')
            count += 1
    manifest = dict(schema_version=1, scenarios=[dict(id=c['id'], topic=c['topic'], sources=c['sources']) for c in CASES], evidence=evidence)
    target = CONTROL / 'scenario-evidence.json'
    if refresh_scenarios:
        target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    elif json.loads(target.read_text()) != manifest:
        raise ValueError('Scenario evidence differs from the registered PDF pages or selected sources')
    return count

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', required=True)
    parser.add_argument('--refresh-scenario-evidence', action='store_true')
    args = parser.parse_args()
    print(f'Quick reference source verification: {verify(args.source_dir, refresh_scenarios=args.refresh_scenario_evidence)} figures and {len(CASES)} scenarios in 3 matching PDFs')

#!/usr/bin/env python3
"""Verify source identity and compact page evidence without publishing PDF text."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', required=True, type=Path)
    parser.add_argument('--refresh', action='store_true', help='Refresh digests for the complete registered page ranges')
    args = parser.parse_args()
    control = ROOT / '.ai/nvme-report'
    sources = json.loads((control/'source-register.json').read_text())['sources']
    register = json.loads((control/'figure-table-register.json').read_text())
    figures = [f for f in register['entries'] if f['report_id']=='base-boot-telemetry-sanitize']
    pages = {}
    for source in sources:
        if source['id'] not in {f['source_id'] for f in figures}:
            continue
        pdf = args.source_dir/source['filename']
        digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
        if digest != source['sha256']:
            raise ValueError(f"Source identity differs: {source['id']}")
        pages[source['id']] = subprocess.check_output(['pdftotext', '-layout', str(pdf), '-'], text=True).split('\f')
    for figure in figures:
        selected=[]
        for span in figure['pdf_pages'].split(','):
            ends=[int(s) for s in span.strip().split('-')]
            selected.extend(range(ends[0], ends[-1]+1))
        text='\n'.join(pages[figure['source_id']][i-1] for i in selected)
        digest = hashlib.sha256(text.encode()).hexdigest()
        if args.refresh:
            figure['evidence_digest'] = digest
        elif digest!=figure['evidence_digest']:
            raise ValueError(f"Page evidence differs: {figure['id']}")
        if not re.search(r'Figure\s+'+figure['number']+r'\s*:', text):
            raise ValueError(f"Caption missing: {figure['id']}")
    if args.refresh:
        (control/'figure-table-register.json').write_text(json.dumps(register, ensure_ascii=False, indent=2)+'\n')
    print(f'Verified 2 source identities and {len(figures)} complete Figure page ranges/captions' + ('; refreshed page digests' if args.refresh else '/digests'))


if __name__ == '__main__':
    main()

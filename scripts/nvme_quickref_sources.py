#!/usr/bin/env python3
"""Verify quick-reference locations against the user's PDFs (never publish PDFs)."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / '.ai/nvme-quickref'

def digest(text):
    return hashlib.sha256(re.sub(r'\s+', ' ', text).strip().encode()).hexdigest()

def verify(source_dir, register=None):
    register = register or json.loads((CONTROL / 'figures.json').read_text())
    sources = json.loads((ROOT / '.ai/nvme-report/source-register.json').read_text())['sources']
    count = 0
    for source in sources:
        path = Path(source_dir) / source['filename']
        if hashlib.sha256(path.read_bytes()).hexdigest() != source['sha256']:
            raise ValueError(f"Source file changed: {source['id']}")
        pages = subprocess.check_output(['pdftotext', '-layout', str(path), '-']).decode().split('\f')
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
    return count

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', required=True)
    args = parser.parse_args()
    print(f'Quick reference source verification: {verify(args.source_dir)} figures in 3 matching PDFs')

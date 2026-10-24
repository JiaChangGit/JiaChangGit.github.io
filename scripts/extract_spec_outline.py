#!/usr/bin/env python3
"""Extract locator-only coverage candidates. Every item starts unreviewed."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

def parse_toc(text: str) -> list[dict]:
    rows = []
    seen = set()
    for line in text.splitlines():
        line = re.sub(r'\.{2,}', ' ', line.strip())
        match = re.fullmatch(r'((?:[1-9]\d*|[A-L])(?:\.\d+)*)(?:\.)?\s+(.+?)\s+(\d{1,4})',line)
        if not match:
            continue
        section,title,page = match.groups()
        if section in seen:
            continue
        seen.add(section)
        rows.append({'section':section,'title':title.strip(),'document_page':int(page),
                     'coverage':'unreviewed','teaching_locations':[],
                     'note':'A TOC locator is not proof that the topic has been taught.'})
    return rows

def make_report(rows: list[dict], *, name: str, sha256: str, revision: str, pdf_pages: int | None=None) -> dict:
    return {'schema_version':1,'source':{'filename':name,'revision':revision,'sha256':sha256,'pdf_pages':pdf_pages},
            'status':'coverage_candidates_only','sections':rows,
            'limitations':['Check extracted titles, page mapping, figures, tables and footnotes against the PDF.',
                           'No topic is automatically marked taught; manually record depth and complete three editions.']}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument('--pdf',type=Path)
    inputs.add_argument('--toc-text',type=Path)
    parser.add_argument('--toc-pages',default='3:37',help='Inclusive 1-based PDF pages; default is for the supplied PCIe Base 6.0 only')
    parser.add_argument('--revision',required=True)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    source = args.pdf or args.toc_text
    if source.resolve() == args.output.resolve():
        parser.error('Output cannot overwrite the input')
    page_count = None
    if args.pdf:
        try:
            from pypdf import PdfReader
        except ImportError:
            parser.error('PDF input needs pypdf; alternatively pass a locally extracted TOC with --toc-text')
        reader = PdfReader(str(args.pdf))
        page_count = len(reader.pages)
        try:
            first,last = map(int,args.toc_pages.split(':'))
            if not 1 <= first <= last <= page_count:
                raise ValueError()
        except ValueError:
            parser.error('--toc-pages must be an inclusive valid range such as 3:37')
        text = '\n'.join(reader.pages[i].extract_text(extraction_mode='layout') or '' for i in range(first-1,last))
    else:
        text = args.toc_text.read_text(encoding='utf-8')
    rows = parse_toc(text)
    if not rows:
        parser.error('No TOC entries found; inspect the supplied pages/text manually')
    result = make_report(rows,name=source.name,sha256=hashlib.sha256(source.read_bytes()).hexdigest(),revision=args.revision,pdf_pages=page_count)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{len(rows)} unreviewed coverage candidates written; no topic marked complete.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

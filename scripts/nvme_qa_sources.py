#!/usr/bin/env python3
"""Audit question-bank source locations, optionally against the original local PDFs."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.nvme_qa_model import load,REFS
from scripts.nvme_qa_teaching import VOLUMES,AIDS
ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'.ai/nvme-question-bank/source-evidence.json'

def numbers(text,separator='-'):
    result=[]
    for r in text.split(','):
        if not r.strip():continue
        ends=r.strip().split(separator)
        result+=list(range(int(ends[0]),int(ends[-1])+1))
    return result
def digest(text):return hashlib.sha256(re.sub(r'\s+',' ',text).strip().encode()).hexdigest()
def outline():
    qs=load()
    return dict(schema_version=1,questions=[dict(id=q['id'],refs=q['refs']) for q in qs],locators=REFS,
                teaching={k:v['refs'] for k,v in AIDS.items()})
def check():
    expected=outline();stored=json.loads(TARGET.read_text())
    for k,v in expected.items():
        if stored[k]!=v:raise ValueError('Source evidence differs from authored content: '+k)
    sources=json.loads((ROOT/'.ai/nvme-report/source-register.json').read_text())['sources']
    by_prefix=dict(zip('BNP',sources))
    if stored['source_hashes']!={k:v['sha256'] for k,v in by_prefix.items()}:raise ValueError('Source identity changed')
    for key,loc in REFS.items():
        prefix,_,pages,figures=loc.split('|');e=stored['evidence'][key]
        if e['pdf_pages']!=numbers(pages):raise ValueError('Page evidence mismatch: '+key)
        if set(e['figure_headings'])!=set(map(str,numbers(figures,'–'))):raise ValueError('Figure evidence mismatch: '+key)
        if not re.fullmatch('[a-f0-9]{64}',e['page_text_sha256']):raise ValueError('Missing page hash: '+key)
        for ps in e['figure_headings'].values():
            if not ps or not set(ps)<=set(e['pdf_pages']):raise ValueError('Invalid figure location: '+key)
    return stored
def verify(source_dir,refresh):
    manifest=outline();manifest['evidence']={};manifest['source_hashes']={}
    sources=json.loads((ROOT/'.ai/nvme-report/source-register.json').read_text())['sources']
    for prefix,source in zip('BNP',sources):
        path=Path(source_dir)/source['filename'];sha=hashlib.sha256(path.read_bytes()).hexdigest()
        if sha!=source['sha256']:raise ValueError('Different input PDF: '+source['filename'])
        manifest['source_hashes'][prefix]=sha
        pages=subprocess.check_output(['pdftotext','-layout',str(path),'-']).decode().split('\f')
        for key,loc in REFS.items():
            p,_,rs,fs=loc.split('|')
            if p!=prefix:continue
            ids=numbers(rs);content='\f'.join(pages[n-1] for n in ids)
            headings={}
            for n in numbers(fs,'–'):
                hits=[i for i in ids if re.search(r'Figure\s+'+str(n)+r'\s*:',pages[i-1])]
                if not hits:raise ValueError(f'Figure {prefix}{n} heading absent from {key} PDF {rs}')
                headings[str(n)]=hits
            manifest['evidence'][key]=dict(pdf_pages=ids,page_text_sha256=digest(content),figure_headings=headings)
    if refresh:TARGET.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    elif json.loads(TARGET.read_text())!=manifest:raise ValueError('PDF evidence changed')
    return manifest
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-dir');p.add_argument('--refresh',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args()
    if a.refresh and not a.source_dir:p.error('--refresh requires --source-dir')
    result=verify(a.source_dir,a.refresh) if a.source_dir else check()
    print(f'Question-bank source evidence: {len(result["questions"])} questions, {len(result["locators"])} locator groups, 3 source identities'+(' verified against original PDFs' if a.source_dir else ' checked against registered evidence'))

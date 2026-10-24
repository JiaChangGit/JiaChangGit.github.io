#!/usr/bin/env python3
"""Check publication boundaries and selected HTML without printing secret values."""
from __future__ import annotations
import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.audit_spec_teaching import scoped_paths
import json

SOURCE_PDFS=re.compile(r'^(?:PCI-Express-Base-Specification-.*|PCI-Firmware-Specification|NVM-Express-.*)\.pdf$',re.I)
PRIVATE_PATH=re.compile(r'file://|[A-Za-z]:[\\/]Users[\\/]user(?:[\\/]|\b)|/home/user/|/mnt/c/Users/user/',re.I)
KEY_SIGNATURE=re.compile(rb'-----BEGIN (?:OPENSSH |RSA |EC |DSA )?PRIVATE KEY-----|\bghp_[A-Za-z0-9]{36}\b|\bgithub_pat_[A-Za-z0-9_]{70,}\b')

class OfflineSafety(HTMLParser):
    def __init__(self,text):
        super().__init__();self.errors=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag in {'iframe','object','embed','form'}:
            self.errors.append('Unexpected active element: '+tag)
        for key,value in attrs.items():
            if key.lower().startswith('on'):
                self.errors.append('Inline event handler')
            if key.lower() in {'href','src','action','xlink:href'}:
                value=re.sub(r'[\x00-\x20]','',value or '').lower()
                if value.startswith(('javascript:','vbscript:','file:')):
                    self.errors.append('Executable or local URL')
        if tag in {'script','link','img','image','source','audio','video'}:
            source=attrs.get('src') or attrs.get('href') or attrs.get('xlink:href') or ''
            if source.startswith(('http:','https:','//')):
                self.errors.append('Network-dependent offline asset')

def source_files(repo):
    result=subprocess.run(['git','-C',str(repo),'ls-files','--cached','--others','--exclude-standard','-z'],check=True,stdout=subprocess.PIPE)
    return [repo/p.decode('utf-8') for p in result.stdout.split(b'\0') if p]

def validate(repo,site=None):
    errors=[]
    scope=json.loads((repo/'.ai/spec-teaching/scope.json').read_text())
    for path in source_files(repo):
        relative=path.relative_to(repo).as_posix()
        if SOURCE_PDFS.fullmatch(path.name) or relative.startswith(('.ai/private/','.ai/handoffs/','private-sources/','output/')):
            errors.append(relative+': private source or working artifact must not be tracked')
        if path.is_file() and path.stat().st_size < 8_000_000 and KEY_SIGNATURE.search(path.read_bytes()):
            errors.append(relative+': possible credential signature; value withheld')
    count=0
    for series,path in scoped_paths(repo,scope):
        text=path.read_text(encoding='utf-8')
        relative=path.relative_to(repo).as_posix()
        if PRIVATE_PATH.search(text):errors.append(relative+': local personal path')
        if path.suffix=='.html':
            errors.extend(relative+': '+issue for issue in OfflineSafety(text).errors)
        count+=1
    if site:
        for private in ['.ai','scripts','tests','docs','output','private-sources','AGENTS.md','vendor/bundle','.bundle']:
            if (site/private).exists():errors.append('Built site exposes '+private)
        for path in site.rglob('*'):
            if path.is_file() and SOURCE_PDFS.fullmatch(path.name):
                errors.append('Built site includes a source specification PDF')
            if path.is_file() and path.stat().st_size < 8_000_000 and KEY_SIGNATURE.search(path.read_bytes()):
                errors.append('Built site '+path.relative_to(site).as_posix()+': possible credential signature; value withheld')
    return count,sorted(set(errors))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=ROOT)
    parser.add_argument('--site-dir',type=Path)
    args=parser.parse_args()
    count,errors=validate(args.repo.resolve(),args.site_dir.resolve() if args.site_dir else None)
    if errors:
        print('\n'.join(errors),file=sys.stderr);return 1
    print(f'Public teaching boundaries verified: {count} scoped documents; no source PDFs, private working files, personal paths or flagged active offline assets.')
    return 0

if __name__=='__main__':raise SystemExit(main())

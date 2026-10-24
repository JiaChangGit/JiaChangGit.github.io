#!/usr/bin/env python3
"""Read-only inventory and review prompts for the explicitly selected articles."""
from __future__ import annotations
import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re

BUNDLE = Path(__file__).resolve().parents[1]
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

def scoped_paths(repo: Path, config: dict) -> list[tuple[str, Path]]:
    repo = repo.resolve()
    result = {}
    for key, row in config['series'].items():
        for prefix in row['path_prefixes']:
            folder = (repo / prefix).resolve()
            if not folder.is_relative_to(repo):
                raise ValueError('Scope prefix leaves repository: ' + prefix)
            for path in folder.rglob('*.html') if folder.is_dir() else []:
                if path.resolve().is_relative_to(repo) and not path.is_symlink():
                    result[path] = key
        for pattern in row['post_patterns']:
            if '/' in pattern or '\\' in pattern:
                raise ValueError('Post patterns must match filenames only')
            for path in (repo / '_posts').glob(pattern):
                if path.resolve().is_relative_to(repo) and not path.is_symlink():
                    result[path] = key
    return sorted((key, path) for path, key in result.items())

class Document(HTMLParser):
    def __init__(self, source: str):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.text = []
        self.ids = []
        self.headings = []
        self.heading = None
        self.collapsed = []
        self.svg_count = 0
        self.feed(re.sub(r'\A---\s*\n.*?\n---\s*\n', '', source, flags=re.S))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'details' and set(attrs.get('class','').split()) & {'qa-answer','qr-answer'} and 'open' not in attrs:
            self.collapsed.append(attrs.get('id') or next((a.get('id') for t,a in reversed(self.stack) if a.get('id')), '(no id)'))
        if tag == 'svg':
            self.svg_count += 1
        if tag in {'h1','h2','h3','h4'}:
            self.heading = [tag, []]
        if tag not in VOID:
            self.stack.append((tag,attrs))

    def handle_endtag(self, tag):
        if self.heading and self.heading[0] == tag:
            self.headings.append(' '.join(''.join(self.heading[1]).split()))
            self.heading = None
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, text):
        if any(t in {'style','script','template'} or 'hidden' in a for t,a in self.stack):
            return
        self.text.append(text)
        if self.heading:
            self.heading[1].append(text)

def analyze(source: str, terms: list[str]) -> dict:
    doc = Document(source)
    text = ' '.join(' '.join(doc.text).split())
    occurrences = {}
    for term in terms:
        found = list(re.finditer(r'(?<![A-Za-z0-9_])'+re.escape(term)+r'(?![A-Za-z0-9_])', text))[:2]
        if found:
            occurrences[term] = [text[max(0,m.start()-50):m.end()+100] for m in found]
    return {
        'headings':doc.headings, 'inline_diagrams':doc.svg_count,
        'duplicate_ids':[i for i,n in Counter(doc.ids).items() if n>1],
        'main_explanations_collapsed_by_default':doc.collapsed,
        'ambiguous_transport_label_count':len(re.findall(r'(?<!over )\bPCIe\s+1\.4\b',text)),
        'first_two_term_contexts_for_human_review':occurrences,
        'review_limit':'Contexts include closed details text; this is not a visible-definition or teaching-quality judgment.'
    }

def audit(repo: Path, config: dict, terms: list[str]) -> dict:
    pages = []
    for series,path in scoped_paths(repo,config):
        pages.append({'series':series,'path':path.relative_to(repo.resolve()).as_posix(),**analyze(path.read_text(encoding='utf-8'),terms)})
    return {'schema_version':1,'mode':'read_only','scope_phase':config['phase'],
            'summary':dict(Counter(p['series'] for p in pages)), 'pages':pages,
            'limitations':['Does not establish technical truth, fluent Chinese, bilingual parity, full specification coverage, or learning outcomes.']}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--scope',type=Path,default=BUNDLE/'.ai/spec-teaching/scope.json')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--terms',nargs='*',default=['TLP','DMA','MSI-X','FLR','CNS','NSID','SQE','CQE'])
    args = parser.parse_args()
    result = audit(args.repo,json.loads(args.scope.read_text(encoding='utf-8')),args.terms)
    if args.output:
        target = args.output.resolve()
        if target.is_relative_to(args.repo.resolve()):
            parser.error('Write audit reports outside the source repository')
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'pages':len(result['pages']),'series':result['summary'],'report':str(args.output) if args.output else None},ensure_ascii=False))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

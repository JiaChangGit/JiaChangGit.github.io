#!/usr/bin/env python3
"""Remove authoring-only markers from the scoped built site, preserving source files."""
from __future__ import annotations
import argparse
from pathlib import Path
import re

WALK_COMMENT = re.compile(r'<!--\s*(?:pcie-walk:[^<>\r\n]*|/pcie-walk)\s*-->')
SOURCE_CLAIMS = re.compile(r'\sdata-source-claims="[^"]*"')
REPORT_COMMENT = re.compile(
    r'<!--\s*(?:(?:claim|figure-table):(?:PCIE14|NVMCS13)-[A-Z0-9-]+'
    r'|qa:(?:pcie-transport-1\.4|nvm-command-set-1\.3)-[a-z0-9-]+)\s*-->'
)
REPORT_PAGES = {
    'DOCS/nvme-spec-report/pcie-transport-1.4/tutorial-zh-tw.html',
    'DOCS/nvme-spec-report/nvm-command-set-1.3/tutorial-zh-tw.html',
    'nvmenvme-pcie-transport-1-4-zh-tw0828.html',
    'nvmenvme-pcie-transport-1-4-en0828.html',
    'nvme/nvm-command-set-1-3-zh-tw/index.html',
    'nvme/nvm-command-set-1-3-en/index.html',
}


def clean(site: Path, *, check: bool = False) -> list[str]:
    changed = []
    for path in site.rglob('*.html'):
        rel = path.relative_to(site).as_posix()
        is_pcie = rel.startswith('DOCS/pcie-course/') or bool(
            re.fullmatch(r'pcie/chapter-\d+-(?:en|zh-tw)/index\.html', rel)
        )
        if not is_pcie and rel not in REPORT_PAGES:
            continue
        original = path.read_text(encoding='utf-8')
        text = original
        if is_pcie:
            text = SOURCE_CLAIMS.sub('', WALK_COMMENT.sub('', text))
        if rel in REPORT_PAGES:
            text = REPORT_COMMENT.sub('', text)
        if text != original:
            changed.append(rel)
            if not check:
                path.write_text(text, encoding='utf-8')
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site-dir', type=Path, required=True)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if not args.site_dir.is_dir():
        parser.error('site directory does not exist')
    changed = clean(args.site_dir, check=args.check)
    if args.check and changed:
        print(f'{len(changed)} scoped pages still contain authoring-only markers')
        return 1
    print(f'Public teaching cleanup: {len(changed)} scoped pages updated' if not args.check
          else 'Public teaching cleanup verified')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

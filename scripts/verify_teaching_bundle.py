#!/usr/bin/env python3
"""Verify ZIP contents against its manifest without extracting or running files."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile

def verify(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError('Duplicate archive entries')
        for name in names:
            parsed=PurePosixPath(name)
            if parsed.is_absolute() or '..' in parsed.parts or '\\' in name or ':' in name:
                raise ValueError('Unsafe archive path: '+name)
        roots={PurePosixPath(name).parts[0] for name in names}
        if len(roots)!=1:
            raise ValueError('Expected exactly one bundle root')
        root=next(iter(roots))
        manifest_name=root+'/MANIFEST.json'
        manifest=json.loads(archive.read(manifest_name))
        rows=manifest['files']
        expected={root+'/'+row['path'] for row in rows}|{manifest_name}
        if len(rows)!=len({row['path'] for row in rows}) or set(names)!=expected:
            raise ValueError('Archive entries do not exactly match the manifest')
        for row in rows:
            data=archive.read(root+'/'+row['path'])
            if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:
                raise ValueError('Content mismatch: '+row['path'])
        if archive.testzip():
            raise ValueError('ZIP CRC check failed')
    return {'files_verified':len(names),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'limit':'Integrity against the enclosed manifest; not a signed authenticity guarantee.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--zip',dest='archive',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(verify(args.archive),ensure_ascii=False))
    return 0

if __name__=='__main__':
    raise SystemExit(main())

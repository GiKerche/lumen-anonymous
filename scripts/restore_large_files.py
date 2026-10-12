#!/usr/bin/env python3
"""Restore large anonymous-host artifacts and verify their SHA-256 hashes."""
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]


def safe_path(name):
    relative = PurePosixPath(name)
    if relative.is_absolute() or '..' in relative.parts or '\\' in name:
        raise ValueError('Invalid artifact path')
    path = ROOT / relative
    if not path.resolve().is_relative_to(ROOT) or path.is_symlink():
        raise ValueError('Artifact path must stay inside the repository')
    return path


def main():
    manifest = json.loads((ROOT / 'artifact_parts/manifest.json').read_text())
    restored = 0
    for row in manifest['files']:
        path = safe_path(row['path'])
        if path.exists():
            if hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
                raise ValueError('Existing file differs; refusing to overwrite: ' + row['path'])
            continue
        packed = []
        for part in row['parts']:
            data = safe_path(part['path']).read_bytes()
            if len(data) != part['bytes'] or hashlib.sha256(data).hexdigest() != part['sha256']:
                raise ValueError('Invalid archive part: ' + part['path'])
            packed.append(data)
        if row['codec'] != 'gzip':
            raise ValueError('Unsupported archive codec')
        raw = gzip.decompress(b''.join(packed))
        if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
            raise ValueError('Invalid restored artifact: ' + row['path'])
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as output:
            output.write(raw)
        restored += 1
    print(f'Checked {len(manifest["files"])} artifacts; restored {restored} missing files.')


if __name__ == '__main__':
    main()

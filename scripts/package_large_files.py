#!/usr/bin/env python3
"""Provide small, byte-preserving copies for anonymous hosts with file limits."""
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIMIT = 7_500_000
PART_SIZE = 6_000_000


def main():
    rows = []
    for directory in ('data', 'analysis', 'eval_results_consolidated', 'eval_results_benign_control'):
        for path in sorted((ROOT / directory).rglob('*')):
            if not path.is_file() or path.stat().st_size <= LIMIT:
                continue
            assert not path.is_symlink()
            raw = path.read_bytes()
            relative = path.relative_to(ROOT).as_posix()
            digest = hashlib.sha256(raw).hexdigest()
            folder = ROOT / 'artifact_parts' / hashlib.sha256(relative.encode()).hexdigest()[:16]
            folder.mkdir(parents=True, exist_ok=True)
            packed = gzip.compress(raw, compresslevel=9, mtime=0)
            parts = []
            for index, start in enumerate(range(0, len(packed), PART_SIZE)):
                chunk = packed[start:start + PART_SIZE]
                target = folder / f'part-{index:03d}.bin'
                target.write_bytes(chunk)
                parts.append({'path': target.relative_to(ROOT).as_posix(),
                              'sha256': hashlib.sha256(chunk).hexdigest(), 'bytes': len(chunk)})
            row = {'path': relative, 'sha256': digest, 'bytes': len(raw),
                   'codec': 'gzip', 'parts': parts,
                   'readme': (folder / 'README.md').relative_to(ROOT).as_posix()}
            rows.append(row)
            links = '\n'.join(f'- [{Path(p["path"]).name}]({Path(p["path"]).name})' for p in parts)
            (folder / 'README.md').write_text(
                f'# Archived source file\n\n`{relative}`\n\n'
                f'SHA-256: `{digest}`\n\n'
                'These gzip parts preserve the original file byte for byte and fit '
                'within anonymous-host file limits. Download the repository and run '
                '`python scripts/restore_large_files.py` to restore any missing large files. '
                'Existing files are checked and never overwritten.\n\n' + links + '\n')
            assert gzip.decompress(b''.join((ROOT / p['path']).read_bytes() for p in parts)) == raw
    (ROOT / 'artifact_parts/manifest.json').write_text(json.dumps({'files': rows}, indent=2) + '\n')
    manifest_path = ROOT / 'site/data/manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['large_file_sources'] = {row['path']: row['readme'] for row in rows}
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'large_files': len(rows), 'parts': sum(len(row['parts']) for row in rows),
                      'original_bytes_preserved': True}))


if __name__ == '__main__':
    main()

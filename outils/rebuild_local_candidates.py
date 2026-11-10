#!/usr/bin/env python3
"""Regenerate *local, unpublished* v9 candidate snapshots for pastoral fixtures.

SmartDump ZIPs intentionally exclude ignored build/v9 outputs. This command
restores only those derived candidates from their owner workspaces; it NEVER
invokes publish, activate, network calls, or changes canon/source material.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def locations(root: Path = ROOT) -> list[Path]:
    units = sorted(p for p in (root / 'kristals').iterdir() if (p / 'kristal.workspace.json').is_file())
    return units + [root / 'kristals-temoins/francois-assise',
                    root / 'extension-arketype/overlay/modeles/unite-formation-federee',
                    root / 'extension-arketype/overlay/modeles/temoin-vertus-sources']


def canonical_hashes(folder: Path) -> dict[str, str]:
    # The no-canon-mutation invariant spans each local package's own canonical files.
    return {p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((folder / 'canon').rglob('*')) if p.is_file()}


def run(root: Path = ROOT, *, build: bool = False) -> dict[str, object]:
    instances = locations(root)
    if len(instances) != 35:
        raise ValueError(f'Expected 32 unit + 3 template/witness candidates, got {len(instances)}')
    built = 0
    for folder in instances:
        if folder.is_symlink() or not folder.resolve().is_relative_to(root.resolve()):
            raise ValueError('Unsafe owner path: ' + str(folder))
        tool = folder / 'tools/kristal.py'
        if not tool.is_file() or tool.is_symlink():
            raise ValueError('Missing local owner tool: ' + str(tool))
        before = canonical_hashes(folder)
        if build:
            result = subprocess.run([sys.executable, str(tool), 'build-v9', str(folder)],
                                    cwd=root, capture_output=True, text=True,
                                    timeout=120, check=False)
            if result.returncode:
                raise RuntimeError(f'{folder.name}: build-v9 failed: {(result.stderr+result.stdout)[-800:]}')
            built += 1
        snap = folder / 'build/v9/state-snapshot.json'
        if not snap.is_file() or snap.is_symlink():
            raise ValueError(f'{folder.name}: missing derived snapshot; rerun with --build')
        if before != canonical_hashes(folder):
            raise RuntimeError(f'{folder.name}: build modified canonical source material')
    return {'format':'pastorale.local-candidate-preflight/1.0',
            'instances':len(instances), 'generated':built,
            'published':False, 'release_authorized':False,
            'note':'Derived candidates only: not independent qualification or public/teacher approval'}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', action='store_true', help='Regenerate 35 local derived builds; no publication')
    args = parser.parse_args(argv)
    try:
        report = run(build=args.build)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print('[REFUSED]', exc, file=sys.stderr)
        return 1
    import json
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

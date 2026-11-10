#!/usr/bin/env python3
"""Vercel build: produce dist/ = public site files + minified, cache-versioned
pages from compiled-static/ (same output server.py serves in production).

Run by Vercel as the buildCommand (see vercel.json). Private files (Python,
config, scripts, briefs) are filtered with the same rule server.py uses.
"""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'scripts'))

import build_static_assets  # noqa: E402
from server import Handler  # noqa: E402

# Repo-only files that are not part of the public site.
SKIP_TOP = {'api', 'dist', 'exports', 'reports', 'screenshots', 'compiled-static',
            'generated-artifacts', 'netlify', 'scripts', 'node_modules'}
SKIP_FILES = {'vercel.json', 'package.json', 'package-lock.json', 'Dockerfile',
              'render.yaml', 'server.py', 'netlify.toml'}


def is_public(rel):
    parts = rel.split('/')
    if parts[0] in SKIP_TOP or rel in SKIP_FILES or rel.startswith('images/_orig/'):
        return False
    if rel.endswith('.md'):
        return False
    return not Handler._private_static_path('/' + rel)


def main():
    build_static_assets.build()
    shutil.rmtree(DIST, ignore_errors=True)
    copied = 0
    for path in build_static_assets.public_files():
        rel = path.relative_to(ROOT).as_posix()
        if not is_public(rel):
            continue
        compiled = ROOT / 'compiled-static' / rel
        source = compiled if compiled.is_file() else path
        target = DIST / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied += 1
    print(f'dist/: {copied} public files')


if __name__ == '__main__':
    main()

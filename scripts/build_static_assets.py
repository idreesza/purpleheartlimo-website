#!/usr/bin/env python3
"""Build minified, cache-versioned public HTML/CSS/JS without changing sources.

Run npm ci && python3 scripts/build_static_assets.py before publishing.
Never copy backend files, specifications, or private data into the output.
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'compiled-static'
ESBUILD = ROOT / 'node_modules/.bin/esbuild'
EXCLUDE = {'.git', '.local', '.agents', 'node_modules', 'attached_assets',
           'compiled-static', 'generated-artifacts', 'scripts', 'netlify',
           'dist', 'api', 'exports', 'reports', 'screenshots'}  # not public site
ASSET_EXT = {'.css', '.js', '.webp', '.avif', '.png', '.jpg', '.jpeg',
             '.svg', '.ico', '.woff', '.woff2', '.ttf', '.mp4'}


def public_files():
    return [p for p in ROOT.rglob('*') if p.is_file()
            and not any(part in EXCLUDE or part.startswith('.') for part in p.relative_to(ROOT).parts)]


def build():
    if not ESBUILD.exists():
        raise SystemExit('Run npm ci before building production assets.')
    files = public_files()
    hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()[:16]
              for p in files if p.suffix.lower() in ASSET_EXT}
    # One deterministic build version invalidates transitive CSS/JS references too.
    version = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()[:16]
    OUT.mkdir(exist_ok=True)

    def version_url(url, page):
        if url.startswith(('data:', 'http:', 'https:', '//', '#', 'mailto:', 'tel:')):
            return url
        parsed = urlsplit(url)
        candidate = (ROOT / parsed.path.lstrip('/')) if url.startswith('/') else page.parent / parsed.path
        try:
            rel = candidate.resolve().relative_to(ROOT).as_posix()
        except ValueError:
            return url
        if rel not in hashes:
            return url
        query = '&'.join(p for p in parsed.query.split('&') if p and not p.startswith('v='))
        return '/' + rel + '?' + (query + '&' if query else '') + 'v=' + version + (
            '#' + parsed.fragment if parsed.fragment else '')

    count = 0
    for page in files:
        if page.suffix.lower() not in ('.html', '.css', '.js'):
            continue
        text = page.read_text()
        # URL attributes, CSS url(), and literal JS asset paths. Restrict to
        # existing public assets; navigation/canonical links are untouched.
        text = re.sub(r'''(["'])([^"'<>\\\n]+?\.(?:css|js|webp|avif|png|jpg|jpeg|svg|ico|woff2?|ttf|mp4)(?:\?[^"'<>\\\n]*)?)\1''',
                      lambda m: m[1] + version_url(m[2], page) + m[1], text)
        if page.suffix == '.html':
            # Header CSS is critical on every page; inline this small sheet.
            # Other shared sheets remain ordered: they contain cross-page and
            # interactive-state rules, so blindly deferring them would flash UI.
            def critical_header(m):
                header = ROOT / 'css/header.css'
                result = subprocess.run([str(ESBUILD), '--minify', '--loader=css'],
                                        input=header.read_text(), text=True,
                                        capture_output=True, check=True)
                return '<style data-inline-source="/css/header.css">' + result.stdout + '</style>'
            text = re.sub(r'<link\b(?=[^>]*href=["\']/css/header\.css(?:\?[^"\']*)?["\'])(?=[^>]*rel=["\']stylesheet["\'])[^>]*>',
                          critical_header, text)
            def srcset(m):
                entries = []
                for entry in m[2].split(','):
                    bits = entry.strip().split()
                    if bits:
                        bits[0] = version_url(bits[0], page)
                        entries.append(' '.join(bits))
                return m[1] + ', '.join(entries) + m[3]
            text = re.sub(r'''((?:imagesrcset|srcset)=["'])([^"']+)(["'])''', srcset, text)
        if page.suffix in ('.js', '.css'):
            result = subprocess.run([str(ESBUILD), '--minify', '--loader=' + page.suffix[1:]],
                                    input=text, text=True, capture_output=True, check=True)
            text = result.stdout
        destination = OUT / page.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text)
        count += 1
    (OUT / 'manifest.json').write_text(json.dumps({'version': version, 'files': count}))
    print(f'Built {count} public documents/assets, version {version}')


if __name__ == '__main__':
    build()

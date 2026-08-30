#!/usr/bin/env python3
"""Idempotently add shared lead assets and the mobile call CTA to HTML files."""
from __future__ import annotations

import re
import sys
from pathlib import Path


CSS_TAG = '<link rel="stylesheet" href="/css/sitewide-leads.css">'
JS_TAG = '<script src="/js/sitewide-leads.js" defer></script>'
CALL_BAR = """<aside class="phl-mobile-call-bar" aria-label="Call Purple Heart Limo">
  <a class="phl-mobile-call-bar__link" href="tel:+18337400700">Call now: (833) 740-0700</a>
</aside>"""

HEAD_CLOSE = re.compile(r"</head\s*>", re.IGNORECASE)
BODY_CLOSE = re.compile(r"</body\s*>", re.IGNORECASE)
CSS_ASSET = re.compile(
    r'<link\b[^>]*\bhref\s*=\s*["\']/css/sitewide-leads\.css["\'][^>]*>',
    re.IGNORECASE,
)
JS_ASSET = re.compile(
    r'<script\b[^>]*\bsrc\s*=\s*["\']/js/sitewide-leads\.js["\'][^>]*>\s*</script\s*>',
    re.IGNORECASE,
)
CALL_BAR_MATCH = re.compile(
    r'<aside\b[^>]*\bclass\s*=\s*["\'][^"\']*\bphl-mobile-call-bar\b[^"\']*["\'][^>]*>',
    re.IGNORECASE,
)
NOINDEX = re.compile(
    r'<meta\b[^>]*\bname\s*=\s*["\']robots["\'][^>]*\bcontent\s*=\s*["\'][^"\']*\bnoindex\b',
    re.IGNORECASE,
)


def insert_once(html: str, matcher: re.Pattern[str], tag: str, location: re.Pattern[str]) -> str:
    if matcher.search(html):
        return html
    if not location.search(html):
        raise ValueError("required document closing tag is missing")
    return location.sub(lambda match: tag + "\n" + match.group(0), html, count=1)


def transform(html: str) -> str:
    html = insert_once(html, CSS_ASSET, CSS_TAG, HEAD_CLOSE)
    html = insert_once(html, JS_ASSET, JS_TAG, BODY_CLOSE)
    return insert_once(html, CALL_BAR_MATCH, CALL_BAR, BODY_CLOSE)


def validate(path: Path, before_noindex: bool) -> None:
    html = path.read_text(encoding="utf-8")
    if len(CSS_ASSET.findall(html)) != 1:
        raise ValueError(f"{path}: expected exactly one lead stylesheet")
    if len(JS_ASSET.findall(html)) != 1:
        raise ValueError(f"{path}: expected exactly one lead script")
    if len(CALL_BAR_MATCH.findall(html)) != 1:
        raise ValueError(f"{path}: expected exactly one mobile call bar")
    if not BODY_CLOSE.search(html) or not HEAD_CLOSE.search(html):
        raise ValueError(f"{path}: closing head/body tag missing after update")
    if bool(NOINDEX.search(html)) != before_noindex:
        raise ValueError(f"{path}: noindex behavior changed")


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    excluded = {".git", ".local", ".agents", "node_modules", "attached_assets"}
    pages = sorted(
        path for path in root.rglob("*.html")
        if not any(part in excluded or part.startswith(".") for part in path.relative_to(root).parts[:-1])
    )
    if not pages:
        raise ValueError("no HTML pages found")

    noindex_state = {}
    for path in pages:
        original = path.read_text(encoding="utf-8")
        noindex_state[path] = bool(NOINDEX.search(original))
        updated = transform(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")

    for path in pages:
        validate(path, noindex_state[path])
    print(f"validated {len(pages)} HTML pages")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as error:
        print(f"sitewide lead application failed: {error}", file=sys.stderr)
        raise SystemExit(1)
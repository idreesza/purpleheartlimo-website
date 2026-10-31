#!/usr/bin/env python3
"""Install exactly one canonical GA4 Google tag immediately after <head>."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
MEASUREMENT_ID = "G-Y469VZMYZT"
EXCLUDED_DIRS = {".git", ".local", ".agents", "node_modules", "attached_assets", "compiled-static", "generated-artifacts"}

GOOGLE_TAG = """<!-- Google tag (gtag.js) -->
<script src="/js/analytics-loader.js" defer></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-Y469VZMYZT');
</script>"""

LOADER_RE = re.compile(
    r'\s*<script\b[^>]*\bsrc=(["\'])'
    r'https://www\.googletagmanager\.com/gtag/js\?id=G-Y469VZMYZT'
    r'\1[^>]*>\s*</script>\s*',
    re.I,
)
INLINE_RE = re.compile(
    r'\s*<script\b(?![^>]*\bsrc=)[^>]*>.*?'
    r"gtag\(\s*['\"]config['\"]\s*,\s*['\"]G-Y469VZMYZT['\"]\s*\)\s*;?"
    r'.*?</script>\s*',
    re.I | re.S,
)
COMMENT_RE = re.compile(
    r'\s*<!--\s*(?:Google tag \(gtag\.js\)|Google Analytics 4[^>]*)\s*-->\s*',
    re.I,
)


def html_files() -> list[Path]:
    return sorted(
        path for path in ROOT.rglob("*.html")
        if not any(part in EXCLUDED_DIRS or part.startswith(".")
                   for part in path.relative_to(ROOT).parts[:-1])
    )


def transform(source: str, path: Path) -> str:
    source = re.sub(r'<script[^>]*src=["\']/js/analytics-loader\.js["\'][^>]*></script>', '', source)
    source = LOADER_RE.sub("\n", source)
    source = INLINE_RE.sub("\n", source)
    source = COMMENT_RE.sub("\n", source)
    head = re.search(r"<head\b[^>]*>", source, re.I)
    if not head:
        raise ValueError(f"{path}: missing <head>")
    tail = re.sub(r'<meta\b[^>]*charset\s*=[^>]*>', '', source[head.end():], flags=re.I).lstrip("\r\n")
    return source[:head.end()] + '\n<meta charset="utf-8">\n' + GOOGLE_TAG + "\n" + tail


def main() -> None:
    pages = html_files()
    changed = 0
    for path in pages:
        source = path.read_text(encoding="utf-8")
        updated = transform(source, path)
        if updated != source:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"Google tag verified on {len(pages)} HTML pages; changed {changed}")


if __name__ == "__main__":
    main()
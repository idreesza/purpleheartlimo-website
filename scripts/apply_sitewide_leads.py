#!/usr/bin/env python3
"""Apply shared conversion tracking and mobile phone CTA to every site page."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
EXCLUDED = {".git", ".local", ".agents", "node_modules", "attached_assets"}
CSS = '<link rel="stylesheet" href="/css/sitewide-leads.css">'
JS = '<script src="/js/sitewide-leads.js" defer></script>'
BAR = '''<aside class="phl-mobile-call-bar" aria-label="Call Purple Heart Limo">
  <a class="phl-mobile-call-bar__link" href="tel:+18337400700">Call now: (833) 740-0700</a>
</aside>'''


def files():
    return sorted(p for p in ROOT.rglob("*.html")
                  if not any(x in EXCLUDED or x.startswith(".")
                             for x in p.relative_to(ROOT).parts[:-1]))


def transform(s, path):
    s = re.sub(r'\s*<link\b[^>]*href=["\']/css/sitewide-leads\.css["\'][^>]*>\s*', "\n", s, flags=re.I)
    s = re.sub(r'\s*<script\b[^>]*src=["\']/js/sitewide-leads\.js["\'][^>]*>\s*</script>\s*', "\n", s, flags=re.I)
    s = re.sub(r'\s*<aside\b[^>]*class=["\'][^"\']*\bphl-mobile-call-bar\b[^"\']*["\'][^>]*>.*?</aside>\s*', "\n", s, flags=re.I | re.S)
    s = re.sub(r"</head\s*>", CSS + "\n</head>", s, count=1, flags=re.I)
    s = re.sub(r"</body\s*>", JS + "\n" + BAR + "\n</body>", s, count=1, flags=re.I)
    if CSS not in s or JS not in s or BAR not in s:
        raise ValueError(f"{path}: could not insert shared assets")
    # Generated landing pages and city hubs: emit only after confirmed success.
    s = s.replace("ok.classList.add('show');this.reset();",
                  "ok.classList.add('show');if(window.PHLTrackLead)window.PHLTrackLead(this);this.reset();")
    s = s.replace("ok.classList.add('show'); this.reset();",
                  "ok.classList.add('show'); if(window.PHLTrackLead)window.PHLTrackLead(this); this.reset();")
    # Standalone EN/ES contact pages.
    s = s.replace("if(success) e.target.reset();",
                  "if(success){if(window.PHLTrackLead)window.PHLTrackLead(e.target);e.target.reset();}")
    return s


def main():
    pages = files()
    changed = 0
    for p in pages:
        old = p.read_text(encoding="utf-8")
        new = transform(old, p)
        if new != old:
            p.write_text(new, encoding="utf-8")
            changed += 1
    print(f"validated {len(pages)} HTML pages; changed {changed}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""Repeatable invisible loading improvements; run after page generators."""
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
with Image.open(ROOT / 'images/hero-jet-escalade.webp') as image:
    for width in (640, 960, 1280, 1920):
        if width > image.width:
            continue
        resized = image.resize((width, round(image.height * width / image.width)), Image.Resampling.LANCZOS)
        resized.save(ROOT / f'images/hero-jet-escalade-{width}.webp', quality=82, method=6)

hero_sizes = sorted(ROOT.glob('images/hero-jet-escalade-[0-9]*.webp'),
                    key=lambda p: int(p.stem.rsplit('-', 1)[1]))
srcset = ', '.join('/images/' + p.name + ' ' + p.stem.rsplit('-', 1)[1] + 'w' for p in hero_sizes)
count = 0
for page in ROOT.rglob('*.html'):
    if any(p.startswith('.') or p in ('node_modules', 'compiled-static', 'attached_assets', 'generated-artifacts')
           for p in page.relative_to(ROOT).parts):
        continue
    original = text = page.read_text()
    text = re.sub(r'<script\b[^>]*src=["\']https://www\.googletagmanager\.com/gtag/js\?id=G-Y469VZMYZT["\'][^>]*></script>',
                  '<script src="/js/analytics-loader.js" defer></script>', text)
    if 'analytics-loader.js' in text and 'rel="preconnect" href="https://www.googletagmanager.com"' not in text:
        text = text.replace('</head>', '<link rel="preconnect" href="https://www.googletagmanager.com">\n</head>', 1)
    def defer_script(m):
        tag = m[0]
        # Booking pages synchronously consume PHL_CLASSES immediately after
        # pricing.js; keep this dependency ordered, rather than break estimates.
        if 'pricing.js' in tag and 'const _phl = id => window.phlGetClass(id)' in text:
            return tag
        return tag if re.search(r'\bdefer\b', tag) else tag[:-1] + ' defer>'
    text = re.sub(r'<script\b[^>]*src=["\'][^"\']*(?:google-places-autocomplete|price-sync|pricing|sitewide-leads|nav-dropdown)\.js["\'][^>]*>',
                  defer_script, text)
    text = re.sub(r'<(?:img|link)\b[^>]*(?:logo-banner)[^>]*>',
                  lambda m: re.sub(r'\sfetchpriority=["\'][^"\']*["\']', '', m[0]), text)
    if "background-image:url('images/hero-jet-escalade.webp')" in text:
        # A real responsive image preserves the old background's geometry.
        css = "background-image:none"
        text = text.replace("background-image:url('images/hero-jet-escalade.webp')", css)
        marker = '/* responsive hero source */'
        if marker not in text:
            rules = marker + '\n#home-page .hero > .phl-hero-media{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 60%;z-index:0;pointer-events:none}\n@media(max-width:768px){#home-page .hero > .phl-hero-media{object-position:center top}}\n'
            text = text.replace('</head>', '<style>' + rules + '</style>\n</head>', 1)
            text = text.replace('<section class="hero">', '<section class="hero"><img class="phl-hero-media" alt="" aria-hidden="true" src="/images/hero-jet-escalade.webp" srcset="' + srcset + '" sizes="100vw" fetchpriority="high" decoding="async">', 1)
        text = re.sub(r'<link\b[^>]*href=["\']/images/hero-jet-escalade\.webp["\'][^>]*>',
                      lambda m: '<link rel="preload" as="image" href="/images/hero-jet-escalade.webp" fetchpriority="high" imagesrcset="' + srcset + '" imagesizes="100vw">', text)
    if text != original:
        page.write_text(text)
        count += 1
print(f'Updated loading hints in {count} pages')

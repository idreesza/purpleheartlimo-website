#!/usr/bin/env python3
"""Idempotent sitewide SEO metadata, schema, image-alt and sitemap normalizer."""
from pathlib import Path
from collections import Counter
import html
import json
import re
import sys

import apply_google_tag

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://purpleheartlimo.com"
BUSINESS_ID = BASE + "/#business"
EXCLUDED = {".git", ".local", ".agents", "node_modules", "attached_assets"}
TARGET_META = {
    "description", "robots", "twitter:card", "twitter:title",
    "twitter:description", "twitter:image",
}
TARGET_OG = {"og:type", "og:url", "og:title", "og:description", "og:image", "og:locale"}
NOINDEX_PATHS = {
    "blog/limo-service-dfw-airport-complete-guide/index.html",
    "blog/best-wedding-venues-in-dallas-dfw-limo-service/index.html",
}
INTERNAL_ALIASES = {
    "/blog/limo-service-dfw-airport-complete-guide/": "/blog/dfw-airport-limo-guide.html",
    "/blog/best-wedding-venues-in-dallas-dfw-limo-service/": "/blog/dfw-wedding-venues.html",
}


def files():
    return sorted(p for p in ROOT.rglob("*.html")
                  if not any(x in EXCLUDED or x.startswith(".")
                             for x in p.relative_to(ROOT).parts[:-1]))


def clean(value):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value))).strip()


def clip(value, limit):
    value = re.sub(r"\s+", " ", value).strip(" -|:—")
    if len(value) <= limit:
        return value
    return value[:limit + 1].rsplit(" ", 1)[0].strip(" -|:—")


def canonical(path):
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return BASE + "/"
    if rel.endswith("/index.html"):
        return BASE + "/" + rel[:-10]
    return BASE + "/" + rel


def attr(tag, name):
    m = re.search(r'\b' + re.escape(name) + r'\s*=\s*(["\'])(.*?)\1', tag, re.I | re.S)
    return html.unescape(m.group(2).strip()) if m else ""


def title_for(source, path):
    m = re.search(r"<title\b[^>]*>(.*?)</title>", source, re.I | re.S)
    current = clean(m.group(1)) if m else ""
    malformed = re.search(r"(?:—\s*\d+|—\s*\|)", current)
    if current and len(current) <= 60 and not malformed:
        return current
    h = re.search(r"<h1\b[^>]*>(.*?)</h1>", source, re.I | re.S)
    subject = clean(h.group(1)) if h else path.stem.replace("-", " ").title()
    suffix = " | Purple Heart Limo"
    return clip(subject, 60 - len(suffix)) + suffix


def description_for(source, title):
    for tag in re.findall(r"<meta\b[^>]*>", source, re.I | re.S):
        if attr(tag, "name").lower() == "description":
            value = attr(tag, "content")
            if value:
                return clip(value, 155)
    return clip(f"{title.split('|')[0].strip()}. Professional chauffeur service, flat-rate quotes, no surge pricing, and 24/7 reservations. Call (833) 740-0700.", 155)


def is_noindex(source, path):
    for tag in re.findall(r"<meta\b[^>]*>", source, re.I | re.S):
        if attr(tag, "name").lower() == "robots" and "noindex" in attr(tag, "content").lower():
            return True
    rel = path.relative_to(ROOT).as_posix().lower()
    return rel in {"404.html", "thank-you.html", *NOINDEX_PATHS}


def remove_business(source):
    return re.sub(r'[ \t]*<script\b[^>]*\bid=["\']seo-business-graph["\'][^>]*>.*?</script\s*>[ \t]*\r?\n?',
                  "", source, flags=re.I | re.S)


def remove_invalid_faq(source):
    visible = clean(re.sub(r"<(?:script|style)\b.*?</(?:script|style)\s*>", " ", source, flags=re.I | re.S)).casefold()

    def repl(m):
        try:
            data = json.loads(m.group(3))
        except json.JSONDecodeError:
            return m.group(0)

        def valid(node):
            qs = node.get("mainEntity", [])
            return bool(qs) and all(clean(str(q.get("name", ""))).casefold() in visible
                                    for q in qs if isinstance(q, dict))

        if isinstance(data, dict) and data.get("@type") == "FAQPage" and not valid(data):
            return ""
        if isinstance(data, dict) and isinstance(data.get("@graph"), list):
            data["@graph"] = [n for n in data["@graph"]
                              if not (isinstance(n, dict) and n.get("@type") == "FAQPage" and not valid(n))]
            return m.group(1) + json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"
        return m.group(0)

    return re.sub(r'(<script\b[^>]*\btype\s*=\s*(["\'])application/ld\+json\2[^>]*>)(.*?)</script\s*>',
                  repl, source, flags=re.I | re.S)


def image_alts(source):
    def repl(m):
        tag = m.group(0)
        src = attr(tag, "src")
        name = Path(src.split("?")[0]).stem.replace("-", " ").replace("_", " ").strip()
        alt = clean(name).title() if name else "Purple Heart Limo chauffeured vehicle"
        existing = re.search(r'\balt\s*=\s*(["\'])(.*?)\1', tag, re.I | re.S)
        if existing and existing.group(2).strip():
            return tag
        if existing:
            return tag[:existing.start()] + f'alt="{html.escape(alt, quote=True)}"' + tag[existing.end():]
        return tag[:-1].rstrip("/") + f' alt="{html.escape(alt, quote=True)}"' + ("/>" if tag.rstrip().endswith("/>") else ">")
    return re.sub(r"<img\b[^>]*>", repl, source, flags=re.I | re.S)


def business_graph():
    node = {
        "@context": "https://schema.org",
        "@graph": [{
            "@type": "LimousineService", "@id": BUSINESS_ID,
            "name": "Purple Heart Limo", "url": BASE + "/",
            "telephone": "+18337400700", "priceRange": "$$",
            "openingHours": "Mo-Su 00:00-23:59",
            "areaServed": [
                *[{"@type": "City", "name": x} for x in
                  ["Dallas", "Fort Worth", "Addison", "Frisco", "Plano", "Arlington"]],
                {"@type": "Airport", "name": "Dallas Fort Worth International Airport", "iataCode": "DFW"},
                {"@type": "Airport", "name": "Dallas Love Field", "iataCode": "DAL"},
            ],
        }],
    }
    return json.dumps(node, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def normalize(source, path, title, desc):
    source = apply_google_tag.transform(source, path)
    for old, new in INTERNAL_ALIASES.items():
        source = source.replace(old, new)
    source = image_alts(remove_invalid_faq(remove_business(source)))
    noindex = is_noindex(source, path)
    url = canonical(path)

    source = re.sub(r"<title\b[^>]*>.*?</title\s*>", "", source, flags=re.I | re.S)
    source = re.sub(r"<link\b[^>]*\brel\s*=\s*(?:[\"']canonical[\"']|canonical)[^>]*>", "", source, flags=re.I | re.S)

    def rm_meta(m):
        tag = m.group(0)
        name = attr(tag, "name").lower()
        prop = attr(tag, "property").lower()
        return "" if name in TARGET_META or prop in TARGET_OG else tag

    source = re.sub(r"<meta\b[^>]*>", rm_meta, source, flags=re.I | re.S)
    locale = "es_ES" if re.search(r"<html\b[^>]*\blang=[\"']es", source, re.I) else "en_US"
    image = BASE + "/images/og-image.jpg"
    tags = [
        f"<title>{html.escape(title)}</title>",
        f'<meta name="description" content="{html.escape(desc, quote=True)}">',
        f'<meta name="robots" content="{"noindex, nofollow" if noindex else "index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1"}">',
        f'<link rel="canonical" href="{url}">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:title" content="{html.escape(title, quote=True)}">',
        f'<meta property="og:description" content="{html.escape(desc, quote=True)}">',
        f'<meta property="og:image" content="{image}">',
        f'<meta property="og:locale" content="{locale}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{html.escape(title, quote=True)}">',
        f'<meta name="twitter:description" content="{html.escape(desc, quote=True)}">',
        f'<meta name="twitter:image" content="{image}">',
    ]
    if not noindex:
        tags.append(f'<script id="seo-business-graph" type="application/ld+json">{business_graph()}</script>')

    marker = apply_google_tag.GOOGLE_TAG
    pos = source.find(marker)
    if pos < 0:
        raise ValueError(f"{path}: canonical Google tag missing")
    end = pos + len(marker)
    tail = source[end:].lstrip("\r\n")
    result = source[:end] + "\n" + "\n".join(tags) + "\n" + tail
    result = re.sub(r"[ \t]+(?=\r?$)", "", result, flags=re.M)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result


def collect():
    rows = []
    for p in files():
        s = p.read_text(encoding="utf-8")
        rows.append((p, s, title_for(s, p)))
    counts = Counter(t.casefold() for _, _, t in rows)
    output = []
    for p, s, t in rows:
        if counts[t.casefold()] > 1:
            suffix = clip(p.parent.name.replace("-", " ").title(), 18)
            t = clip(clip(t.split("|")[0], 38) + " " + suffix, 54) + " | PHL"
        output.append((p, s, t, description_for(s, t)))
    return output


def sitemap_for(rows):
    urls = [canonical(p) for p, source, _, _ in rows if not is_noindex(source, p)]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    lines += [f"  <url><loc>{html.escape(u)}</loc><changefreq>monthly</changefreq></url>" for u in urls]
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def audit(rows):
    changed = []
    for p, old, title, desc in rows:
        if normalize(old, p, title, desc) != old:
            changed.append(p.relative_to(ROOT).as_posix())
    return changed


def main():
    check = "--check" in sys.argv
    rows = collect()
    changed = audit(rows)
    sitemap = sitemap_for(rows)
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    robots = re.sub(r"(?im)^Sitemap:\s*\S+\s*$", "", robots).rstrip() + f"\n\nSitemap: {BASE}/sitemap.xml\n"
    if check:
        sitemap_bad = (ROOT / "sitemap.xml").read_text(encoding="utf-8") != sitemap
        robots_bad = (ROOT / "robots.txt").read_text(encoding="utf-8") != robots
        print(f"SEO check: pages={len(rows)}, changed={len(changed)}, sitemap_needs_update={int(sitemap_bad)}, robots_needs_update={int(robots_bad)}")
        if changed:
            print("Needs normalization:", ", ".join(changed[:25]))
        raise SystemExit(1 if changed or sitemap_bad or robots_bad else 0)
    for p, old, title, desc in rows:
        new = normalize(old, p, title, desc)
        if new != old:
            p.write_text(new, encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")
    print(f"normalized {len(rows)} pages; changed {len(changed)}; sitemap URLs {len(rows)-sum(is_noindex(s,p) for p,s,_,_ in rows)}")


if __name__ == "__main__":
    main()
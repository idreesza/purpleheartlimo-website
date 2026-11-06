#!/usr/bin/env python3
"""Idempotent sitewide SEO metadata, schema, image-alt and sitemap normalizer."""
from pathlib import Path
from collections import Counter
import datetime
import html
import subprocess
import json
import re
import sys
import tomllib

import apply_google_tag
import inline_homepage_css

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://purpleheartlimo.com"
BUSINESS_ID = BASE + "/#business"
# Verified official profiles only. Add the Google Business Profile, Yelp, BBB,
# etc. here once confirmed; every page's business entity picks them up.
SAME_AS = [
    "https://www.facebook.com/profile.php?id=61578479742416",
]
EXCLUDED = {".git", ".local", ".agents", "node_modules", "attached_assets",
            "compiled-static", "generated-artifacts"}  # build output is not source
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


def exact_redirects():
    """Return local, exact permanent redirects from the deployment config."""
    data = tomllib.loads((ROOT / "netlify.toml").read_text(encoding="utf-8"))
    redirects = {}
    for rule in data.get("redirects", []):
        source = rule.get("from", "")
        target = rule.get("to", "")
        if (rule.get("status") == 301 and source.startswith("/")
                and target.startswith("/") and not any(x in source for x in ("*", ":"))):
            redirects[source] = target
    return redirects


EXACT_REDIRECTS = exact_redirects()


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
        url_path = "/"
    elif rel.endswith("/index.html"):
        url_path = "/" + rel[:-10]
    else:
        url_path = "/" + rel

    seen = set()
    while url_path not in seen:
        seen.add(url_path)
        source = url_path
        if source not in EXACT_REDIRECTS and source != "/":
            source = source.rstrip("/")
        if source not in EXACT_REDIRECTS:
            break
        url_path = EXACT_REDIRECTS[source]
    return BASE + url_path


def repair_malformed_anchors(source):
    """Repair a legacy Instagram anchor whose missing URL becomes an internal 404."""
    return source.replace(
        '<a aria-label="Instagram" href= rel="noopener"',
        '<a aria-label="Instagram" href="https://www.instagram.com/austinlimousine" rel="noopener"',
    )


def restore_nojs_stylesheet_fallbacks(source):
    """Ensure every async stylesheet has a matching no-JS fallback."""
    head_match = re.search(r"(<head\b[^>]*>)(.*?)(</head\s*>)", source, re.I | re.S)
    if not head_match:
        return source
    head = head_match.group(2)
    fallback_urls = set()
    for block in re.findall(
            r"<noscript\b[^>]*>.*?</noscript\s*>", head, re.I | re.S):
        for link in re.findall(r"<link\b[^>]*>", block, re.I | re.S):
            if "stylesheet" in attr(link, "rel").casefold().split():
                fallback_urls.add(attr(link, "href"))

    def link_repl(match):
        link = match.group(0)
        url = attr(link, "href")
        if (attr(link, "media").casefold() != "print"
                or "this.media='all'" not in attr(link, "onload")
                or not url or url in fallback_urls):
            return link
        fallback_urls.add(url)
        fallback = (
            f'<noscript><link rel="stylesheet" '
            f'href="{html.escape(url, quote=True)}"></noscript>'
        )
        return link + "\n" + fallback

    head = re.sub(r"<link\b[^>]*>", link_repl, head, flags=re.I | re.S)
    head = re.sub(r"\s*<noscript\b[^>]*>\s*</noscript\s*>", "", head,
                  flags=re.I | re.S)
    return source[:head_match.start(2)] + head + source[head_match.end(2):]


def dedupe_asset_references(source):
    """Keep the first load of each asset while preserving no-JS fallbacks."""
    seen = set()
    no_script_blocks = []

    def protect_no_script(match):
        no_script_blocks.append(match.group(0))
        return f"<!-- seo-noscript-{len(no_script_blocks) - 1} -->"

    source = re.sub(
        r"<noscript\b[^>]*>.*?</noscript\s*>",
        protect_no_script, source, flags=re.I | re.S,
    )

    def script_repl(match):
        tag = match.group(0)
        url = attr(tag, "src")
        if not url:
            return tag
        key = ("script", url)
        if key in seen:
            return ""
        seen.add(key)
        return tag

    def style_repl(match):
        tag = match.group(0)
        rel = attr(tag, "rel").casefold().split()
        url = attr(tag, "href")
        if "stylesheet" not in rel or not url:
            return tag
        key = ("stylesheet", url)
        if key in seen:
            return ""
        seen.add(key)
        return tag

    source = re.sub(
        r"<script\b[^>]*\bsrc\s*=\s*([\"']).*?\1[^>]*>\s*</script\s*>",
        script_repl, source, flags=re.I | re.S,
    )
    source = re.sub(r"<link\b[^>]*>", style_repl, source, flags=re.I | re.S)
    for index, block in enumerate(no_script_blocks):
        source = source.replace(f"<!-- seo-noscript-{index} -->", block)
    return source


def attr(tag, name):
    m = re.search(r'\b' + re.escape(name) + r'\s*=\s*(["\'])(.*?)\1', tag, re.I | re.S)
    return html.unescape(m.group(2).strip()) if m else ""


def _load_title_overrides():
    try:
        return json.loads((ROOT / "scripts" / "data" / "title_overrides.json")
                          .read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


# Hand-written titles (<=60 chars) for pages whose H1 is too long to clip
# into a readable title. Keyed by repo-relative path.
TITLE_OVERRIDES = _load_title_overrides()


def title_for(source, path):
    override = TITLE_OVERRIDES.get(path.relative_to(ROOT).as_posix())
    if override:
        return override
    m = re.search(r"<title\b[^>]*>(.*?)</title>", source, re.I | re.S)
    current = clean(m.group(1)) if m else ""
    malformed = re.search(r"(?:—\s*\d+|—\s*\|)", current)
    head_words = current.split("|")[0].split()
    if head_words and head_words[-1].casefold().strip(".,:;") in _DANGLING:
        malformed = True  # earlier clipping cut the phrase mid-sentence
    if current.rstrip().endswith("| PHL"):
        malformed = True  # opaque abbreviation from the old de-dup pass
    if current and len(current) <= 60 and not malformed:
        return current
    h = re.search(r"<h1\b[^>]*>(.*?)</h1>", source, re.I | re.S)
    subject = clean(h.group(1)) if h else path.stem.replace("-", " ").title()
    suffix = " | Purple Heart Limo"
    return clip_phrase(subject, 60 - len(suffix)) + suffix


# Words a clipped title must not end on ("...Tip a Limo Driver in |").
_DANGLING = {
    "a", "an", "the", "and", "or", "but", "for", "to", "of", "in", "on", "at",
    "by", "with", "from", "vs", "your", "our", "how", "what", "why", "is",
    "y", "de", "del", "la", "el", "en", "los", "las", "sin", "con", "para", "&",
}


def clip_phrase(value, limit):
    """clip() that also drops trailing connector words and dangling
    punctuation so a shortened title still reads as a complete phrase."""
    value = clip(value, limit)
    words = value.split()
    while len(words) > 1 and words[-1].casefold().strip(".,:;") in _DANGLING:
        words.pop()
    return " ".join(words).rstrip(" ,;:—-")


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


def normalize_fleet_schema(source, path):
    """Reference one Organization from fleet Service items.

    Repeating LocalBusiness as each fleet item's provider caused nine identical
    missing-address errors. The fleet page describes services and vehicles, not
    nine separate storefronts.
    """
    if path.relative_to(ROOT).as_posix() != "fleet.html":
        return source

    def repl(m):
        try:
            data = json.loads(m.group(3))
        except json.JSONDecodeError:
            return m.group(0)
        if not (isinstance(data, dict) and data.get("@type") == "ItemList"
                and data.get("name") == "Purple Heart Limo Fleet"):
            return m.group(0)
        for entry in data.get("itemListElement", []):
            item = entry.get("item", {}) if isinstance(entry, dict) else {}
            if isinstance(item, dict) and item.get("@type") == "Service":
                item["provider"] = {"@id": BUSINESS_ID}
        payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        return m.group(1) + payload + "</script>"

    return re.sub(r'(<script\b[^>]*\btype\s*=\s*(["\'])application/ld\+json\2[^>]*>)(.*?)</script\s*>',
                  repl, source, flags=re.I | re.S)


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


def business_graph(path):
    # One canonical business entity, identical on every page (no per-page
    # Organization/LimousineService type conflicts on the same @id). No
    # aggregateRating: self-served ratings on a business entity are against
    # Google's review-snippet policy.
    areas = [
        *[{"@type": "City", "name": x} for x in
          ["Dallas", "Fort Worth", "Arlington", "Plano", "Frisco", "Addison",
           "Austin", "Round Rock", "Houston"]],
        {"@type": "Airport", "name": "Dallas Fort Worth International Airport", "iataCode": "DFW"},
        {"@type": "Airport", "name": "Dallas Love Field", "iataCode": "DAL"},
        {"@type": "Airport", "name": "Austin-Bergstrom International Airport", "iataCode": "AUS"},
    ]
    item = {
        "@type": "LimousineService", "@id": BUSINESS_ID,
        "name": "Purple Heart Limo", "url": BASE + "/",
        "telephone": "+18337400700", "email": "info@purpleheartlimo.com",
        "logo": BASE + "/logo.webp",
        "image": [BASE + "/logo.webp", BASE + "/images/sedan-cadillac.webp"],
        "priceRange": "$$",
        "openingHours": "Mo-Su 00:00-23:59",
        "address": {"@type": "PostalAddress", "addressRegion": "TX", "addressCountry": "US"},
        "areaServed": areas,
        "sameAs": SAME_AS,
    }
    node = {"@context": "https://schema.org", "@graph": [item]}
    return json.dumps(node, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def normalize(source, path, title, desc):
    source = dedupe_asset_references(
        restore_nojs_stylesheet_fallbacks(
            repair_malformed_anchors(apply_google_tag.transform(source, path))
        )
    )
    source = inline_homepage_css.inline_styles(source, path)
    for old, new in INTERNAL_ALIASES.items():
        source = source.replace(old, new)
    source = normalize_fleet_schema(
        image_alts(remove_invalid_faq(remove_business(source))), path
    )
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
        tags.append(f'<script id="seo-business-graph" type="application/ld+json">{business_graph(path)}</script>')

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
            t = clip_phrase(clip_phrase(t.split("|")[0], 38) + " " + suffix, 40) + " | Purple Heart Limo"
        output.append((p, s, t, description_for(s, t)))
    return output


def article_date(source):
    """dateModified (or datePublished) of the page's Article/BlogPosting.

    Site-wide template commits touch every file, so for articles the date the
    content itself last changed is the meaningful <lastmod>."""
    best = ""
    for raw in re.findall(r'<script\b[^>]*application/ld\+json[^>]*>(.*?)</script\s*>',
                          source, re.I | re.S):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        nodes = data.get("@graph", [data]) if isinstance(data, dict) else data
        for node in nodes if isinstance(nodes, list) else []:
            if not isinstance(node, dict):
                continue
            kind = node.get("@type")
            kinds = kind if isinstance(kind, list) else [kind]
            if not {"Article", "BlogPosting", "NewsArticle"} & set(kinds):
                continue
            value = str(node.get("dateModified") or node.get("datePublished") or "")
            if re.match(r"\d{4}-\d{2}-\d{2}", value):
                best = max(best, value[:10])
    return best


def last_modified(path, source=""):
    """<lastmod> for a page: the article's own modified date when it has one,
    otherwise the last commit touching the file (file mtime if uncommitted).
    Google uses <lastmod> when it is consistently accurate; it ignores
    <changefreq>."""
    found = article_date(source)
    if found:
        return found
    rel = path.relative_to(ROOT).as_posix()
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel],
                             cwd=ROOT, capture_output=True, text=True, timeout=20)
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return datetime.date.fromtimestamp(path.stat().st_mtime).isoformat()


def sitemap_for(rows):
    entries = {}
    for p, source, _, _ in rows:
        if is_noindex(source, p):
            continue
        url = canonical(p)
        entries[url] = max(entries.get(url, ""), last_modified(p, source))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    lines += [f"  <url><loc>{html.escape(u)}</loc><lastmod>{d}</lastmod></url>"
              for u, d in entries.items()]
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
            # newline="\n": keep LF on Windows too (no CRLF churn in git).
            p.write_text(new, encoding="utf-8", newline="\n")
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8", newline="\n")
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8", newline="\n")
    print(f"normalized {len(rows)} pages; changed {len(changed)}; sitemap URLs {len(rows)-sum(is_noindex(s,p) for p,s,_,_ in rows)}")


if __name__ == "__main__":
    main()
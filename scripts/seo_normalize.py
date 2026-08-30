#!/usr/bin/env python3
"""Idempotently normalize the SEO essentials of the static site.

Run from any directory with ``python3 scripts/seo_normalize.py``.  Use
``--check`` in CI; it writes nothing and exits 1 when normalization is needed
or a FAQ schema cannot be substantiated by visible questions.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://purpleheartlimo.com"
BUSINESS_ID = BASE + "/#business"
SKIP_DIRS = {
    "scripts", "node_modules", "vendor", "netlify", "css", "js", "images",
    "attached_assets", "screenshots", "__pycache__", ".git", ".github",
    ".pythonlibs", "dist", "build", "coverage",
}
TARGET_META = {
    "description", "robots", "twitter:card", "twitter:title",
    "twitter:description", "twitter:image",
}
TARGET_OG = {"og:type", "og:url", "og:title", "og:description", "og:image", "og:locale"}
AREA_NAMES = [
    "Dallas", "Fort Worth", "Addison", "Frisco", "Plano", "Arlington",
]


def clean_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def attr(tag: str, name: str) -> str:
    match = re.search(r"\b" + re.escape(name) + r"""\s*=\s*(["'])(.*?)\1""", tag, re.I | re.S)
    return html.unescape(match.group(2)).strip() if match else ""


def html_files() -> list[Path]:
    files = []
    for path in ROOT.rglob("*.html"):
        parts = path.relative_to(ROOT).parts
        if any(part.startswith(".") or part in SKIP_DIRS for part in parts[:-1]):
            continue
        files.append(path)
    return sorted(files)


def page_path(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-10] + "/"
    return "/" + rel


def canonical_url(raw: str, path: Path) -> str:
    """Keep a valid existing canonical path, but always use the apex host."""
    fallback = BASE + page_path(path)
    raw = html.unescape(raw).strip()
    if not raw:
        return fallback
    candidate = urljoin(BASE + "/", raw)
    parts = urlsplit(candidate)
    if not parts.path or parts.netloc.lower() not in {"purpleheartlimo.com", "www.purpleheartlimo.com"}:
        return fallback
    normalized_path = re.sub(r"/{2,}", "/", parts.path)
    return urlunsplit(("https", "purpleheartlimo.com", normalized_path, "", ""))


def find_one(source: str, pattern: str) -> str:
    found = re.search(pattern, source, re.I | re.S)
    return found.group(1) if found else ""


def existing_values(source: str, path: Path) -> dict[str, str]:
    canonical_tag = re.search(r"<link\b[^>]*\brel\s*=\s*(['\"])canonical\1[^>]*>", source, re.I | re.S)
    canon_href = attr(canonical_tag.group(0), "href") if canonical_tag else ""
    return {
        "title": clean_text(find_one(source, r"<title\b[^>]*>(.*?)</title\s*>")),
        "description": meta_content(source, "description"),
        "canonical": canonical_url(canon_href, path),
    }


def meta_content(source: str, key: str, property_: bool = False) -> str:
    field = "property" if property_ else "name"
    tag = re.search(r"<meta\b[^>]*\b" + field + r"\s*=\s*(['\"])" +
                    re.escape(key) + r"\1[^>]*>", source, re.I | re.S)
    return attr(tag.group(0), "content") if tag else ""


def clipped(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", text).strip(" -|:—")
    if len(text) <= limit:
        return text
    shortened = text[:limit + 1].rsplit(" ", 1)[0].rstrip(" -|:—")
    return shortened or text[:limit].rstrip()


def logical_heading(source: str, path: Path) -> str:
    body = re.sub(r"<(?:header|nav|footer)\b.*?</(?:header|nav|footer)\s*>", "", source, flags=re.I | re.S)
    found = re.search(r"<h[1-6]\b[^>]*>(.*?)</h[1-6]\s*>", body, re.I | re.S)
    if found:
        return clean_text(found.group(1))
    stem = page_path(path).strip("/").replace(".html", "").replace("-", " ").replace("/", " ")
    return stem.title() if stem else "Luxury Limousine Service"


def is_noindex(source: str, path: Path, heading: str) -> bool:
    haystack = " ".join((path.name, page_path(path), heading, existing_values(source, path)["title"])).lower()
    return "404" in haystack or "thank-you" in haystack or "thank you" in haystack


def generated_title(heading: str, path: Path, ordinal: int = 0) -> str:
    suffix = " | Purple Heart Limo"
    subject = clipped(heading or logical_heading("", path), 60 - len(suffix))
    if ordinal:
        marker = " — " + str(ordinal)
        subject = clipped(subject, 60 - len(suffix) - len(marker)) + marker
    return subject + suffix


def generated_description(heading: str, path: Path, ordinal: int = 0) -> str:
    topic = clipped(heading or logical_heading("", path), 85)
    tail = " Book 24/7 with Purple Heart Limo."
    if ordinal:
        tail = " Purple Heart Limo, 24/7."
    return clipped(topic + ". " + "Professional limousine and black car service." + tail, 155)


def business_graph() -> str:
    business = {
        "@type": "LimousineService", "@id": BUSINESS_ID, "name": "Purple Heart Limo",
        "url": BASE + "/", "telephone": "+18337400700", "priceRange": "$$",
        "openingHours": "Mo-Su 00:00-23:59",
        "areaServed": (
            [{"@type": "City", "name": city} for city in AREA_NAMES]
            + [{"@type": "Airport", "name": "Dallas Fort Worth International Airport", "iataCode": "DFW"},
               {"@type": "Airport", "name": "Dallas Love Field", "iataCode": "DAL"}]
        ),
    }
    return json.dumps({"@context": "https://schema.org", "@graph": [business]},
                      ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def remove_business_nodes(source: str) -> str:
    source = re.sub(r"""[ \t]*<script\b[^>]*\bid\s*=\s*(["'])seo-business-graph\1[^>]*>.*?</script\s*>[ \t]*\r?\n?""",
                    "", source, flags=re.I | re.S)
    def replace_script(match: re.Match[str]) -> str:
        tag, payload = match.group(1), match.group(3)
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            return match.group(0)
        def prune(value):
            if isinstance(value, dict):
                if value.get("@id") == BUSINESS_ID:
                    return None
                return {k: pruned for k, v in value.items() if (pruned := prune(v)) is not None}
            if isinstance(value, list):
                return [pruned for v in value if (pruned := prune(v)) is not None]
            return value
        pruned = prune(data)
        if pruned is None or (isinstance(pruned, dict) and pruned.get("@graph") == []):
            return ""
        return tag + json.dumps(pruned, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"
    return re.sub(r"""(<script\b[^>]*\btype\s*=\s*(["'])application/ld\+json\2[^>]*>)(.*?)</script\s*>""",
                  replace_script, source, flags=re.I | re.S)


def remove_unsubstantiated_faq(source: str) -> str:
    visible_source = re.sub(r"<(?:script|style)\b.*?</(?:script|style)\s*>", " ", source, flags=re.I | re.S)
    visible_text = clean_text(visible_source).casefold()

    def replace_script(match: re.Match[str]) -> str:
        tag, payload = match.group(1), match.group(3)
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            return match.group(0)

        def valid_faq(node: dict) -> bool:
            questions = node.get("mainEntity", [])
            return bool(questions) and all(
                clean_text(str(q.get("name", ""))).casefold() in visible_text
                for q in questions if isinstance(q, dict)
            )

        if isinstance(data, dict) and data.get("@type") == "FAQPage":
            return match.group(0) if valid_faq(data) else ""
        if isinstance(data, dict) and isinstance(data.get("@graph"), list):
            data["@graph"] = [
                node for node in data["@graph"]
                if not (isinstance(node, dict) and node.get("@type") == "FAQPage" and not valid_faq(node))
            ]
            return tag + json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"
        return match.group(0)

    return re.sub(r"""(<script\b[^>]*\btype\s*=\s*(["'])application/ld\+json\2[^>]*>)(.*?)</script\s*>""",
                  replace_script, source, flags=re.I | re.S)


def faq_errors(source: str) -> int:
    visible_source = re.sub(r"<(?:script|style)\b.*?</(?:script|style)\s*>", " ", source, flags=re.I | re.S)
    visible_text = clean_text(visible_source).casefold()
    errors = 0
    for payload in re.findall(r"""<script\b[^>]*\btype\s*=\s*(["'])application/ld\+json\1[^>]*>(.*?)</script\s*>""", source, re.I | re.S):
        try:
            data = json.loads(payload[1])
        except json.JSONDecodeError:
            continue
        nodes = data.get("@graph", []) if isinstance(data, dict) else []
        nodes = [data] + nodes if isinstance(data, dict) else nodes
        for node in nodes:
            if not isinstance(node, dict) or node.get("@type") != "FAQPage":
                continue
            for question in node.get("mainEntity", []):
                name = clean_text(str(question.get("name", ""))).casefold()
                if name and name not in visible_text:
                    errors += 1
    return errors


def normalize_images(source: str) -> str:
    def image(match: re.Match[str]) -> str:
        tag = match.group(0)
        if re.search(r"\balt\s*=", tag, re.I):
            return tag
        src = attr(tag, "src")
        name = Path(urlsplit(src).path).stem.replace("_", " ").replace("-", " ")
        if re.search(r"(icon|logo-icon|arrow|chevron|menu|close|spinner|bullet|facebook|instagram)", src, re.I):
            alt = ""
        else:
            before = source[max(0, match.start() - 1800):match.start()]
            headings = re.findall(r"<h[1-6]\b[^>]*>(.*?)</h[1-6]\s*>", before, re.I | re.S)
            context = clean_text(headings[-1]) if headings else ""
            alt = clipped(context or name.title(), 110)
        return tag[:-1] + ' alt="' + html.escape(alt, quote=True) + '">'
    return re.sub(r"<img\b[^>]*>", image, source, flags=re.I | re.S)


def normalize_h1(source: str) -> str:
    h1s = list(re.finditer(r"<h1\b[^>]*>.*?</h1\s*>", source, re.I | re.S))
    chrome = [(m.start(), m.end()) for m in re.finditer(
        r"<(?:header|nav|footer)\b.*?</(?:header|nav|footer)\s*>", source, re.I | re.S)]
    logical = [m for m in h1s if not any(a <= m.start() < b for a, b in chrome)]
    keep = logical[0] if logical else None
    # Demotion preserves content and hierarchy rather than deleting legitimate headings.
    for match in reversed([m for m in h1s if m is not keep]):
        replacement = re.sub(r"<h1\b", "<h2", match.group(0), count=1, flags=re.I)
        replacement = re.sub(r"</h1\s*>", "</h2>", replacement, flags=re.I)
        source = source[:match.start()] + replacement + source[match.end():]
    if keep:
        return source
    body_start = re.search(r"<body\b[^>]*>", source, re.I)
    search_at = body_start.end() if body_start else 0
    candidates = list(re.finditer(r"<h([2-6])\b([^>]*)>(.*?)</h\1\s*>", source[search_at:], re.I | re.S))
    candidate = next((m for m in candidates if not any(
        a <= search_at + m.start() < b for a, b in chrome)), None)
    if candidate:
        start, end = search_at + candidate.start(), search_at + candidate.end()
        attributes, content = candidate.group(2), candidate.group(3)
        source = source[:start] + "<h1" + attributes + ">" + content + "</h1>" + source[end:]
    return source


def normalize_page(source: str, path: Path, title: str, description: str) -> str:
    heading = logical_heading(source, path)
    noindex = is_noindex(source, path, heading)
    canonical = existing_values(source, path)["canonical"]
    source = normalize_h1(source)
    source = normalize_images(source)
    source = remove_business_nodes(source)
    source = remove_unsubstantiated_faq(source)
    old_image = meta_content(source, "og:image", True) or BASE + "/images/og-image.jpg"
    source = re.sub(r"<title\b[^>]*>.*?</title\s*>", "", source, flags=re.I | re.S)
    source = re.sub(r"<link\b[^>]*\brel\s*=\s*(['\"])canonical\1[^>]*>", "", source, flags=re.I | re.S)
    def remove_meta(match: re.Match[str]) -> str:
        tag = match.group(0)
        key = attr(tag, "name").lower()
        prop = attr(tag, "property").lower()
        return "" if key in TARGET_META or prop in TARGET_OG else tag
    source = re.sub(r"<meta\b[^>]*>", remove_meta, source, flags=re.I | re.S)
    source = re.sub(r"[ \t]+(?=\r?$)", "", source, flags=re.M)
    source = re.sub(r"\n{3,}", "\n\n", source)
    robots = "noindex, nofollow" if noindex else "index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1"
    tags = [
        "<title>%s</title>" % html.escape(title),
        '<meta name="description" content="%s">' % html.escape(description, quote=True),
        '<meta name="robots" content="%s">' % robots,
        '<link rel="canonical" href="%s">' % canonical,
        '<meta property="og:type" content="%s">' % ("website"),
        '<meta property="og:url" content="%s">' % canonical,
        '<meta property="og:title" content="%s">' % html.escape(title, quote=True),
        '<meta property="og:description" content="%s">' % html.escape(description, quote=True),
        '<meta property="og:image" content="%s">' % html.escape(old_image, quote=True),
        '<meta property="og:locale" content="en_US">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % html.escape(title, quote=True),
        '<meta name="twitter:description" content="%s">' % html.escape(description, quote=True),
        '<meta name="twitter:image" content="%s">' % html.escape(old_image, quote=True),
    ]
    if not noindex:
        tags.append('<script id="seo-business-graph" type="application/ld+json">%s</script>' % business_graph())
    head = re.search(r"<head\b[^>]*>", source, re.I)
    if not head:
        return source
    tail = source[head.end():].lstrip("\r\n")
    return source[:head.end()] + "\n" + "\n".join(tags) + "\n" + tail


def sitemap(urls: list[str]) -> str:
    rows = "\n".join("  <url><loc>%s</loc></url>" % html.escape(url) for url in sorted(set(urls)))
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n' % rows


def coverage(source: str, path: Path) -> dict[str, bool]:
    value = existing_values(source, path)
    h1_count = len(re.findall(r"<h1\b[^>]*>.*?</h1\s*>", source, re.I | re.S))
    og = all(meta_content(source, key, True) for key in TARGET_OG)
    twitter = all(meta_content(source, key) for key in ("twitter:card", "twitter:title", "twitter:description", "twitter:image"))
    missing_alt = bool(re.search(r"<img\b(?![^>]*\balt\s*=)[^>]*>", source, re.I | re.S))
    return {
        "title": bool(value["title"]) and len(value["title"]) <= 60,
        "description": bool(value["description"]) and len(value["description"]) <= 155,
        "canonical": value["canonical"] == meta_content(source, "canonical"),  # replaced below for rel=canonical
        "h1": h1_count == 1,
        "og": og, "twitter": twitter,
        "business_graph": BUSINESS_ID in source and "LimousineService" in source,
        "image_alt": not missing_alt,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report drift and return non-zero without writing")
    args = parser.parse_args()
    files = html_files()
    raw = {path: path.read_text(encoding="utf-8") for path in files}
    values = {path: existing_values(text, path) for path, text in raw.items()}
    title_counts = Counter(v["title"].casefold() for v in values.values() if v["title"] and len(v["title"]) <= 60)
    desc_counts = Counter(v["description"].casefold() for v in values.values() if v["description"] and len(v["description"]) <= 155)
    seen_titles, seen_descs, outputs, changed = set(), set(), {}, []
    for path in files:
        value, heading = values[path], logical_heading(raw[path], path)
        malformed_title = bool(re.search(r"(?:—\s*\d+|—\s*\|)", value["title"]))
        keep_title = bool(value["title"]) and len(value["title"]) <= 60 and title_counts[value["title"].casefold()] == 1 and not malformed_title
        keep_desc = bool(value["description"]) and len(value["description"]) <= 155 and desc_counts[value["description"].casefold()] == 1
        title = value["title"] if keep_title else generated_title(heading, path)
        desc = value["description"] if keep_desc else generated_description(heading, path)
        n = 2
        while title.casefold() in seen_titles:
            title = generated_title(heading, path, n); n += 1
        n = 2
        while desc.casefold() in seen_descs:
            desc = generated_description(heading, path, n); n += 1
        seen_titles.add(title.casefold()); seen_descs.add(desc.casefold())
        output = normalize_page(raw[path], path, title, desc)
        outputs[path] = output
        if output != raw[path]:
            changed.append(path)
    indexable = [path for path in files if not is_noindex(raw[path], path, logical_heading(raw[path], path))]
    desired_sitemap = sitemap([existing_values(outputs[p], p)["canonical"] for p in indexable])
    robots_path, sitemap_path = ROOT / "robots.txt", ROOT / "sitemap.xml"
    robots = robots_path.read_text(encoding="utf-8") if robots_path.exists() else ""
    robots_clean = re.sub(r"(?im)^\s*Sitemap:\s*.*\n?", "", robots).rstrip() + "\nSitemap: " + BASE + "/sitemap.xml\n"
    faq_invalid = sum(faq_errors(outputs[p]) for p in files)
    stats = {
        "html": len(files), "indexable": len(indexable), "changed": len(changed),
        "faq_questions_without_visible_match": faq_invalid, "sitemap_urls": len(indexable),
        "sitemap_needs_update": int(not sitemap_path.exists() or sitemap_path.read_text(encoding="utf-8") != desired_sitemap),
        "robots_needs_update": int(robots != robots_clean),
    }
    # Canonicals use a link element (rather than a meta element); count them separately.
    current_coverage = {name: 0 for name in ("title", "description", "canonical", "h1", "og", "twitter", "business_graph", "image_alt")}
    for path, text in raw.items():
        checks = coverage(text, path)
        canonical_tag = re.search(r"<link\b[^>]*\brel\s*=\s*(['\"])canonical\1[^>]*>", text, re.I | re.S)
        checks["canonical"] = bool(canonical_tag) and attr(canonical_tag.group(0), "href") == values[path]["canonical"]
        for name, passed in checks.items():
            current_coverage[name] += int(passed)
    stats.update({"%s_ok" % name: "%s/%s" % (count, len(files)) for name, count in current_coverage.items()})
    print("SEO coverage: " + ", ".join("%s=%s" % item for item in stats.items()))
    if args.check:
        if changed:
            print("Needs normalization: " + ", ".join(p.relative_to(ROOT).as_posix() for p in changed[:25]))
        return 1 if changed or faq_invalid or stats["sitemap_needs_update"] or stats["robots_needs_update"] else 0
    for path in changed:
        path.write_text(outputs[path], encoding="utf-8")
    sitemap_path.write_text(desired_sitemap, encoding="utf-8")
    robots_path.write_text(robots_clean, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
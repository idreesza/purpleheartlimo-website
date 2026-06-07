"""Build all Purple Heart Limo blog posts from scripts/data/*.json.

Each JSON file is one post dict (see scripts/data/SPEC.md). This script:
  1. Renders every post and writes it to post['path'].
  2. Validates each post (word count, FAQ match, internal links present).
  3. Adds any missing post URLs to sitemap.xml.
  4. Writes grouped index-card HTML to /tmp/cards.html.
"""
import json
import os
import re
import sys
import glob

sys.path.insert(0, os.path.dirname(__file__))
from blog_template import render

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "scripts", "data")

MAIN_PAGES = [
    "/", "/booking.html", "/fleet.html", "/limo-service-dallas-tx/",
    "/services.html", "/contact.html", "/flight-tracker.html",
    "/testimonials.html", "/about.html",
]


def load_posts():
    posts = []
    for fp in sorted(glob.glob(os.path.join(DATA, "*.json"))):
        with open(fp) as f:
            posts.append((os.path.basename(fp), json.load(f)))
    return posts


def word_count(html):
    text = re.sub(r"<[^>]+>", " ", html)
    return len(text.split())


def link_exists(url):
    u = url.split("#")[0].split("?")[0]
    if not u.startswith("/"):
        return True
    if u == "/":
        return os.path.exists(os.path.join(ROOT, "index.html"))
    rel = u.lstrip("/")
    cand = os.path.join(ROOT, rel)
    if u.endswith("/"):
        return os.path.exists(cand + "index.html")
    return os.path.exists(cand) or os.path.exists(os.path.join(cand, "index.html"))


def build():
    posts = load_posts()
    report = []
    sitemap_urls = []
    cards = {}
    for fname, p in posts:
        full = render(p)
        out = os.path.join(ROOT, p["path"])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w") as f:
            f.write(full)
        wc = word_count(p["body_html"]) + sum(
            word_count(x["q"] + " " + x["a"]) for x in p["faqs"]
        )
        # internal links present in body
        links = set(re.findall(r'href="([^"]+)"', p["body_html"]))
        main_hit = sum(1 for m in MAIN_PAGES if m != "/" and any(l == m or l.startswith(m) for l in links))
        # broken-link check across body + related
        check_urls = {l for l in links if l.startswith("/")}
        check_urls |= {r["url"] for r in p.get("related", [])}
        broken = sorted(u for u in check_urls if not link_exists(u))
        status = "OK" if (wc >= 1100 and len(p["faqs"]) >= 3 and main_hit >= 4 and not broken) else "CHECK"
        report.append((p["path"], wc, len(p["faqs"]), main_hit, status))
        if broken:
            print("  BROKEN LINKS in %s -> %s" % (p["path"], broken))
        sitemap_urls.append((p["url"], p.get("date_iso", "2026-06-07")))
        sec = p.get("card_section", "Dallas-Fort Worth Limo Guides")
        cards.setdefault(sec, []).append(p)

    # sitemap
    smp = os.path.join(ROOT, "sitemap.xml")
    sm = open(smp).read()
    added = 0
    for url, date in sitemap_urls:
        if url not in sm:
            entry = '  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n' % (url, date)
            sm = sm.replace("</urlset>", entry + "</urlset>")
            added += 1
    open(smp, "w").write(sm)

    # cards
    with open("/tmp/cards.html", "w") as f:
        for sec, plist in cards.items():
            f.write("\n<!-- SECTION: %s -->\n" % sec)
            for p in plist:
                card = (
                    '      <a href="%s" class="post-card">\n'
                    '        <div class="post-card-body">\n'
                    '          <span class="post-tag">%s</span>\n'
                    '          <h3>%s</h3>\n'
                    '          <div class="post-meta"><span>%s</span><span>%s</span></div>\n'
                    '        </div>\n'
                    '      </a>\n'
                ) % (
                    p["card_url"] if p.get("card_url") else p["url"].replace("https://purpleheartlimo.com", ""),
                    p["card_tag"], p["card_title"], p["date_human"], p["read_time"],
                )
                f.write(card)

    print("Built %d posts. Sitemap entries added: %d" % (len(posts), added))
    print("%-58s %6s %4s %5s %s" % ("path", "words", "faq", "links", "status"))
    for path, wc, faq, links, st in report:
        print("%-58s %6d %4d %5d %s" % (path, wc, faq, links, st))


if __name__ == "__main__":
    build()

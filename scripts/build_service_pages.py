#!/usr/bin/env python3
"""H1: Build standalone pages for hidden index.html page blocks (audit item 1).

- Extracts the needed CSS rules from index.html's inline <style> into css/svc.css
- Uses about.html as the shared shell (head/nav/footer)
- Emits one standalone page per orphaned block, converting showPage() links to real URLs
"""
import re, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
idx = (ROOT / "index.html").read_text(encoding="utf-8")
about = (ROOT / "about.html").read_text(encoding="utf-8")

# ---------------- 1. css/svc.css ----------------
style_m = re.search(r"<style>(.*?)</style>", idx, re.S)
css_src = style_m.group(1)

WHITELIST = re.compile(
    r"^(:root|section\b|\.section-inner|\.section-tag|\.section-title|\.section-sub|"
    r"\.text-center|\.btn-primary|\.btn-white|\.hero-badge|\.hero-btns|\.services-grid|"
    r"\.service-card|\.service-img|\.service-body|\.service-icon|\.service-link|"
    r"\.faq-list|\.faq-item|\.faq-q|\.faq-a|\.faq-icon|\.cta-section|\.cta-btns|"
    r"\.svc-hero|\.breadcrumb|\.legal-page|\.legal-date|\.sitemap-grid|\.sitemap-col)"
)

def parse_rules(block):
    """Yield (selector, body) pairs; handles nested @media by recursion at caller."""
    out, i = [], 0
    while True:
        b1 = block.find("{", i)
        if b1 == -1:
            break
        sel = block[i:b1].strip()
        depth, j = 1, b1 + 1
        while depth and j < len(block):
            if block[j] == "{":
                depth += 1
            elif block[j] == "}":
                depth -= 1
            j += 1
        out.append((sel, block[b1 + 1:j - 1]))
        i = j
    return out

lines_out = ["/* Shared service/section styles extracted from index.html (H1 audit). */"]
for sel, body in parse_rules(re.sub(r"/\*.*?\*/", "", css_src, flags=re.S)):
    if sel.startswith("@media"):
        keep = [(s, b) for s, b in parse_rules(body) if WHITELIST.match(s.strip())]
        if keep:
            lines_out.append(sel + " {")
            for s, b in keep:
                lines_out.append(f"  {s} {{ {b.strip()} }}")
            lines_out.append("}")
    elif WHITELIST.match(sel):
        lines_out.append(f"{sel} {{ {body.strip()} }}")
(ROOT / "css" / "svc.css").write_text("\n".join(lines_out) + "\n", encoding="utf-8")

# ---------------- 2. extract page blocks ----------------
def extract_block(page_id):
    m = re.search(r'<div class="page" id="%s">' % re.escape(page_id), idx)
    start = m.end()
    depth, i = 1, start
    while depth:
        m2 = re.search(r"</?div\b", idx[i:])
        i += m2.end()
        depth += 1 if m2.group(0) == "<div" else -1
    return idx[start:i - m2.end() + (0 if m2.group(0) == "<div" else 0)] if False else idx[start:idx.rfind("</div", start, i)]

def block_html(page_id):
    m = re.search(r'<div class="page" id="%s-page">' % re.escape(page_id), idx)
    start = m.end()
    depth, i = 1, start
    pat = re.compile(r"<div\b|</div>")
    while depth:
        m2 = pat.search(idx, i)
        depth += 1 if m2.group(0) == "<div" else -1
        i = m2.end()
    return idx[start:m2.start()]

# ---------------- 3. shell template ----------------
head_top = about[:about.index("<title>")]
# nav: from <body up to end of mobile-menu div
nav = about[about.index("<body"):about.index("<section")]
footer = about[about.index("<footer>"):about.index("</body>")]

PAGES = {
    "airport": dict(file="airport-transfer.html", title="Airport Transfer — DFW, DAL, AUS, IAH, HOU | Purple Heart Limo",
        desc="Flat-rate Texas airport transfers with flight tracking, meet & greet at baggage claim, and 60 min free wait. DFW, Love Field, Austin & Houston airports.",
        h1=True, name="Airport Transfer"),
    "wedding": dict(file="wedding-limo.html", title="Wedding Limo Service — Austin, Dallas & Houston | Purple Heart Limo",
        desc="Wedding limousine service across Austin, DFW & Houston. Bride & groom transfer, bridal party transport, grand exit vehicle. 500+ Texas weddings served.",
        h1=True, name="Wedding Limo"),
    "corporate": dict(file="corporate-car-service.html", title="Corporate Car Service — Austin, Dallas & Houston | Purple Heart Limo",
        desc="Executive car service for business: airport transfers, roadshows, client entertainment. Monthly invoicing, priority dispatch, flat rates across Texas.",
        h1=True, name="Corporate Travel"),
    "prom": dict(file="prom-limo.html", title="Prom & Graduation Limo Service Texas | Purple Heart Limo",
        desc="Safe, stylish prom & graduation limo service in Austin, Dallas & Houston. Escalade stretch for groups, zero-tolerance safety policy parents trust.",
        h1=True, name="Prom & Graduation"),
    "nightout": dict(file="night-out-limo.html", title="Night Out & Party Limo — Austin, Dallas & Houston | Purple Heart Limo",
        desc="Party limo service for bachelor/bachelorette, birthdays, concerts & bar crawls in Austin, DFW & Houston. No parking, no 2am surge — door to door.",
        h1=True, name="Night Out & Party"),
    "hourly": dict(file="hourly-car-service.html", title="Hourly Car Service — Dedicated Chauffeur | Purple Heart Limo",
        desc="Hourly chauffeur service in Austin, Dallas & Houston. Multi-stop days, roadshows, city tours — your dedicated driver on standby. 2-hour minimum.",
        h1=True, name="Hourly Car Service"),
    "quinceaneara": dict(file="quinceanera-limo.html", title="Quinceañera & Sweet 16 Limo Service Texas | Purple Heart Limo",
        desc="Quinceañera and sweet 16 limousine packages in Austin, Dallas & Houston. Stretch limos, party buses, red carpet & full event coordination.",
        h1=True, name="Quinceañera & Sweet 16"),
    "worldcup": dict(file="world-cup-2026.html", title="World Cup 2026 Transportation — Dallas & Houston | Purple Heart Limo",
        desc="FIFA World Cup 2026 transfers to AT&T Stadium and NRG Stadium. Flat-rate, guaranteed driver, zero surge pricing for every Texas match.",
        h1=True, name="World Cup 2026"),
    "faq": dict(file="faq.html", title="FAQ — Booking, Airports, Pricing & Policies | Purple Heart Limo",
        desc="Answers to common questions about Purple Heart Limo: vehicles, flat rates, airport meet & greet, deposits, cancellations and special events.",
        h1=True, name="FAQ", faq=True),
    "military": dict(file="military-discount.html", title="Military & Veteran Discount — 10% Off Every Ride | Purple Heart Limo",
        desc="Active duty, veterans, Guard, Reserve and immediate family get 10% off every Purple Heart Limo ride. Founded by a U.S. military veteran.",
        h1=True, name="Military Discount"),
    "accessibility": dict(file="accessibility.html", title="Accessibility Statement | Purple Heart Limo",
        desc="Purple Heart Limo's accessibility commitment: WCAG 2.1 AA guidelines, accessibility feedback contact, and wheelchair accessible vehicle options.",
        h1=True, name="Accessibility", legal=True),
    "sitemap": dict(file="sitemap.html", title="Sitemap | Purple Heart Limo",
        desc="Browse all Purple Heart Limo pages: services, fleet, locations, Spanish pages, blog and legal information.",
        h1=True, name="Sitemap"),
}

# showPage targets -> real URLs (used on sitemap + any stray links)
URLMAP = {
    "home": "/", "about": "/about.html", "fleet": "/fleet.html", "contact": "/contact.html",
    "blog": "/blog/", "faq": "/faq.html", "reviews": "/testimonials.html",
    "military": "/military-discount.html", "es-home": "/es/",
    "airport": "/airport-transfer.html", "wedding": "/wedding-limo.html",
    "corporate": "/corporate-car-service.html", "prom": "/prom-limo.html",
    "nightout": "/night-out-limo.html", "hourly": "/hourly-car-service.html",
    "quinceaneara": "/quinceanera-limo.html", "worldcup": "/world-cup-2026.html",
    "privacy": "/privacy-policy.html", "terms": "/terms-of-service.html",
    "accessibility": "/accessibility.html", "sitemap": "/sitemap.html",
}

def rewrite_links(html):
    def repl(m):
        return 'href="%s"' % URLMAP.get(m.group(1), "/")
    return re.sub(r"""href="#" onclick="return showPage\('([^']+)'\)"(?:\s+style="[^"]*")?""", repl, html)

for pid, meta in PAGES.items():
    content = block_html(pid).strip()
    content = rewrite_links(content)
    if meta.get("h1"):
        content = content.replace("<h2>", "<h1>", 1).replace("</h2>", "</h1>", 1)
    url = "https://purpleheartlimo.com/" + meta["file"]
    schema = [{
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://purpleheartlimo.com/"},
            {"@type": "ListItem", "position": 2, "name": meta["name"], "item": url},
        ],
    }]
    if meta.get("faq"):
        qas = re.findall(r'onclick="toggleFAQ\(this\)">(.*?) <span class="faq-icon">.*?<div class="faq-a"><p>(.*?)</p></div>', content, re.S)
        schema.append({
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": re.sub(r"<[^>]+>", "", q).strip(),
                            "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a).strip()}}
                           for q, a in qas],
        })
    schema_tags = "\n".join('<script type="application/ld+json">\n%s\n</script>' % json.dumps(s, ensure_ascii=False, indent=1) for s in schema)
    extra_js = ""
    if meta.get("faq"):
        extra_js = ("<script>function toggleFAQ(btn){const item=btn.parentElement;"
                    "const wasOpen=item.classList.contains('open');"
                    "document.querySelectorAll('.faq-item.open').forEach(i=>i.classList.remove('open'));"
                    "if(!wasOpen)item.classList.add('open');}</script>\n")
    page = (
        head_top
        + f"<title>{meta['title']}</title>\n"
        + f'  <meta name="description" content="{meta["desc"]}">\n'
        + '  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">\n'
        + f'  <link rel="canonical" href="{url}">\n'
        + '  <meta name="geo.region" content="US-TX">\n'
        + '  <meta name="geo.placename" content="Austin, Dallas-Fort Worth, Houston">\n'
        + '  <meta name="twitter:card" content="summary_large_image">\n'
        + f'  <meta name="twitter:title" content="{meta["title"]}">\n'
        + f'  <meta name="twitter:description" content="{meta["desc"]}">\n'
        + '  <meta name="twitter:image" content="https://purpleheartlimo.com/images/sedan-cadillac.webp">\n'
        + '  <meta property="og:type" content="website">\n'
        + f'  <meta property="og:url" content="{url}">\n'
        + f'  <meta property="og:title" content="{meta["title"]}">\n'
        + f'  <meta property="og:description" content="{meta["desc"]}">\n'
        + '  <meta property="og:image" content="https://purpleheartlimo.com/images/og-image.jpg">\n'
        + '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
        + '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        + '  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" media="print" onload="this.media=\'all\'">\n'
        + '  <link rel="stylesheet" href="/css/page.css">\n'
        + f"  {schema_tags}\n"
        + '  <link rel="stylesheet" href="/css/global.css">\n'
        + '  <link rel="stylesheet" href="/css/header.css">\n'
        + '  <link rel="stylesheet" href="/css/svc.css">\n'
        + "</head>\n"
        + nav
        + "<main>\n" + content + "\n</main>\n\n"
        + footer
        + extra_js
        + "<script>function toggleMenu(){const m=document.getElementById('mobile-menu');const b=document.getElementById('hamburger');const open=m.style.display!=='block';m.style.display=open?'block':'none';if(b)b.setAttribute('aria-expanded',open?'true':'false');}</script>\n"
        + '<script src="/js/nav-dropdown.js" defer></script>\n'
        + '<script src="/js/header.js" defer></script>\n'
        + "</body>\n</html>\n"
    )
    (ROOT / meta["file"]).write_text(page, encoding="utf-8")
    print("wrote", meta["file"], len(page), "bytes")
print("wrote css/svc.css", (ROOT / "css" / "svc.css").stat().st_size, "bytes")

"""Shared renderer for Purple Heart Limo blog posts.

A post dict has these keys:
  slug, path, url, title_tag, meta_desc, keywords, og_title, og_desc,
  h1, h1_em, breadcrumb_label, date_iso, date_human, read_time,
  hero_img, hero_alt, headline, jsonld_desc,
  body_html  (article inner HTML: intro + <h2> sections; NO faq, NO related, NO cta),
  faq_heading (optional, default "Frequently Asked Questions"),
  faqs       (list of {"q","a"}),
  related    (list of {"url","title"}),
  cta_h3, cta_p
"""
import html as _html


def _faq_jsonld(faqs):
    items = []
    for f in faqs:
        q = f["q"].replace('"', '\\"')
        a = f["a"].replace('"', '\\"')
        items.append(
            '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
            % (q, a)
        )
    return (
        '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
        + ",".join(items)
        + "]}"
    )


def _faq_visible(heading, faqs):
    out = ['<h2>%s</h2>' % _html.escape(heading)]
    for f in faqs:
        out.append("<h3>%s</h3>" % _html.escape(f["q"]))
        out.append("<p>%s</p>" % f["a"])
    return "\n  ".join(out)


def _related(related):
    lis = []
    for r in related:
        lis.append(
            '<li style="margin:0;"><a href="%s" style="color:#2D0045;font-weight:600;line-height:1.5;display:inline-flex;gap:8px;align-items:baseline;"><span style="color:#C9A84C;">\u2192</span><span>%s</span></a></li>'
            % (r["url"], _html.escape(r["title"]))
        )
    return "".join(lis)


def render(post):
    faq_heading = post.get("faq_heading", "Frequently Asked Questions")
    blogposting = (
        '{"@context":"https://schema.org","@type":"BlogPosting",'
        '"headline":"%s","description":"%s",'
        '"datePublished":"%s","dateModified":"%s","url":"%s",'
        '"publisher":{"@type":"Organization","name":"Purple Heart Limo","logo":{"@type":"ImageObject","url":"https://purpleheartlimo.com/logo.webp"}},'
        '"image":"https://purpleheartlimo.com/images/og-image.jpg",'
        '"author":{"@type":"Organization","name":"Purple Heart Limo","url":"https://purpleheartlimo.com"}}'
    ) % (
        post["headline"].replace('"', '\\"'),
        post["jsonld_desc"].replace('"', '\\"'),
        post["date_iso"],
        post["date_iso"],
        post["url"],
    )

    t = TEMPLATE
    repl = {
        "{{TITLE_TAG}}": post["title_tag"],
        "{{META_DESC}}": post["meta_desc"],
        "{{KEYWORDS}}": post["keywords"],
        "{{CANONICAL}}": post["url"],
        "{{OG_TITLE}}": post.get("og_title", post["title_tag"]),
        "{{OG_DESC}}": post["og_desc"],
        "{{BLOGPOSTING_JSONLD}}": blogposting,
        "{{FAQ_JSONLD}}": _faq_jsonld(post["faqs"]),
        "{{BREADCRUMB_LABEL}}": post["breadcrumb_label"],
        "{{H1}}": post["h1"],
        "{{H1_EM}}": post["h1_em"],
        "{{DATE_HUMAN}}": post["date_human"],
        "{{READ_TIME}}": post["read_time"],
        "{{HERO_IMG}}": post["hero_img"],
        "{{HERO_ALT}}": post["hero_alt"],
        "{{BODY_HTML}}": post["body_html"],
        "{{FAQ_VISIBLE}}": _faq_visible(faq_heading, post["faqs"]),
        "{{RELATED_LIS}}": _related(post["related"]),
        "{{CTA_H3}}": post["cta_h3"],
        "{{CTA_P}}": post["cta_p"],
    }
    for k, v in repl.items():
        t = t.replace(k, v)
    return t


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<link rel="icon" type="image/png" href="/favicon.png">
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<title>{{TITLE_TAG}}</title>
<meta name="description" content="{{META_DESC}}">
<meta name="keywords" content="{{KEYWORDS}}">
<link rel="canonical" href="{{CANONICAL}}">
<meta property="og:title" content="{{OG_TITLE}}">
<meta property="og:description" content="{{OG_DESC}}">
<meta property="og:type" content="article">
<script type="application/ld+json">{{BLOGPOSTING_JSONLD}}</script>
<script type="application/ld+json">{{FAQ_JSONLD}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<noscript><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet"></noscript>
<style>
:root{--purple:#2D0045;--gold:#C9A84C;--gold-light:#E2C36A;--white:#FFFFFF;--gray:#6B7280;--gray-light:#F3F0FF;--text:#1a0028;}
*{margin:0;padding:0;box-sizing:border-box;}html{scroll-behavior:smooth;}
body{font-family:'Inter',sans-serif;color:var(--text);background:var(--white);overflow-x:hidden;}
h1,h2,h3{font-family:'Cormorant Garamond',serif;}a{text-decoration:none;color:inherit;}
.navbar{position:sticky;top:0;z-index:1000;background:rgba(255,255,255,0.97);backdrop-filter:blur(12px);border-bottom:1px solid rgba(45,0,69,0.08);box-shadow:0 2px 20px rgba(45,0,69,0.06);padding:0 5%;height:72px;display:flex;align-items:center;justify-content:space-between;}
.nav-logo{display:flex;align-items:center;gap:10px;}.nav-logo img{width:44px;height:44px;object-fit:contain;border-radius:50%;}
.nav-logo-text{font-family:'Cormorant Garamond',serif !important;font-size:1.45rem;font-weight:700;line-height:1.1;letter-spacing:-0.005em;color:#0a0a0a !important;text-transform:none !important;font-variant:normal !important;}
.dd-section{border-top:1px solid var(--gray-light);margin-top:6px;padding-top:2px;}
.dd-section:first-of-type{border-top:none;margin-top:0;padding-top:0;}
.dd-section>summary{font-size:0.65rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--gold);padding:8px 12px 6px;cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between;border-radius:6px;}
.dd-section>summary:hover{background:var(--gray-light);}
.dd-section>summary::-webkit-details-marker{display:none;}
.dd-section>summary::after{content:"\u25be";font-size:0.7rem;transition:transform 0.2s;color:var(--gold);}
.dd-section[open]>summary::after{transform:rotate(180deg);}
.dd-section-static-title{font-size:0.65rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--gold);padding:10px 12px 4px;border-top:1px solid var(--gray-light);margin-top:6px;}
.nav-logo-sub{font-size:0.6rem;font-weight:500;color:var(--gold);letter-spacing:0.12em;text-transform:uppercase;display:block;}
.nav-links{display:flex;align-items:center;gap:4px;list-style:none;}
.nav-links>li>a{padding:8px 12px;border-radius:8px;font-size:0.82rem;font-weight:500;color:var(--text);transition:all 0.2s;display:block;}
.nav-links>li>a:hover{background:var(--gray-light);color:var(--purple);}
.dropdown{position:relative;}.dropdown-menu{position:absolute;top:calc(100% + 8px);left:0;min-width:220px;background:var(--white);border:1px solid rgba(45,0,69,0.1);border-radius:12px;padding:8px;box-shadow:0 12px 48px rgba(45,0,69,0.18);display:none;z-index:100;}
.dropdown:hover .dropdown-menu{display:block;}.dropdown-menu a{display:block;padding:9px 12px;border-radius:8px;font-size:0.82rem;color:var(--text);}
.nav-cta{display:flex;align-items:center;gap:12px;}.nav-phone{color:var(--purple);font-weight:700;font-size:0.88rem;}
.btn-primary{display:inline-flex;align-items:center;gap:8px;background:linear-gradient(135deg,var(--gold),var(--gold-light));color:var(--purple);padding:14px 28px;border-radius:50px;font-size:0.85rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;box-shadow:0 4px 20px rgba(201,168,76,0.4);transition:transform 0.2s;}
.btn-primary:hover{transform:translateY(-2px);}
.hamburger{display:none;background:none;border:none;cursor:pointer;padding:8px;flex-direction:column;gap:5px;}
.hamburger span{display:block;width:24px;height:2px;background:var(--purple);border-radius:2px;}
@media(max-width:768px){.nav-links{display:none;}.nav-cta .btn-primary{display:none;}.hamburger{display:flex;}}
.post-hero{background:linear-gradient(135deg,var(--purple) 0%,#3d0060 40%,#1a0028 100%);padding:80px 5% 60px;text-align:center;}
.breadcrumb{font-size:0.75rem;color:rgba(255,255,255,0.5);margin-bottom:20px;}.breadcrumb a{color:rgba(255,255,255,0.5);}
.post-hero h1{font-size:clamp(2rem,5vw,3.4rem);color:var(--white);font-weight:300;margin-bottom:16px;max-width:860px;margin-left:auto;margin-right:auto;}
.post-hero h1 em{color:var(--gold);font-style:italic;}
.post-meta{color:rgba(255,255,255,0.55);font-size:0.82rem;margin-top:12px;}
article{max-width:780px;margin:0 auto;padding:60px 5%;}
article img{width:100%;border-radius:16px;margin-bottom:36px;display:block;}
article h2{font-size:1.9rem;font-weight:400;color:var(--purple);margin:40px 0 16px;}
article h3{font-size:1.3rem;color:var(--purple);margin:28px 0 10px;}
article p{font-size:1rem;line-height:1.85;color:#2a1040;margin-bottom:20px;}
article ul,article ol{padding-left:24px;margin-bottom:20px;}
article li{font-size:1rem;line-height:1.85;color:#2a1040;margin-bottom:8px;}
article strong{color:var(--purple);}
article a.inline{color:var(--gold);font-weight:600;}
.callout{background:linear-gradient(135deg,var(--purple),#3d0060);color:var(--white);border-radius:16px;padding:28px 32px;margin:36px 0;}
.callout p{color:rgba(255,255,255,0.9);margin-bottom:0;font-size:0.95rem;line-height:1.75;}
.callout strong{color:var(--gold);}
.fare-table{width:100%;border-collapse:collapse;margin:24px 0;font-size:0.92rem;}
.fare-table th,.fare-table td{text-align:left;padding:12px 14px;border-bottom:1px solid #e4dcf5;}
.fare-table th{background:var(--gray-light);color:var(--purple);font-weight:700;}
.cta-box{background:linear-gradient(135deg,var(--purple),#3d0060);padding:64px 5%;text-align:center;}
.cta-box h3{font-family:'Cormorant Garamond',serif;font-size:2.2rem;color:var(--white);font-weight:300;margin-bottom:12px;}
.cta-box p{color:rgba(255,255,255,0.75);margin-bottom:32px;max-width:520px;margin-left:auto;margin-right:auto;}
.cta-btns{display:flex;gap:16px;justify-content:center;flex-wrap:wrap;}
footer{background:var(--purple);color:rgba(255,255,255,0.7);padding:60px 5% 32px;}
.footer-grid{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:2fr 1fr 1fr;gap:48px;}
.footer-brand{font-family:'Cormorant Garamond',serif;font-size:1.6rem;color:var(--gold);margin-bottom:12px;}
.footer-col-title{font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:var(--gold);margin-bottom:16px;font-weight:700;}
.footer-links{list-style:none;font-size:0.85rem;line-height:2.4;}.footer-links a{color:rgba(255,255,255,0.7);}.footer-links a:hover{color:var(--gold);}
.footer-bottom{max-width:1200px;margin:32px auto 0;border-top:1px solid rgba(255,255,255,0.1);padding-top:24px;font-size:0.78rem;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;}
@media(max-width:600px){.footer-grid{grid-template-columns:1fr;gap:32px;}}
</style>
<link rel="stylesheet" href="/css/global.css">
</head>
<body>
<nav class="navbar"><a href="/" class="nav-logo"><img src="/logo.webp" alt="Purple Heart Limo Logo"><div><div class="nav-logo-text">Purple Heart Limo</div><span class="nav-logo-sub">Texan Owned \u00b7 TX</span></div></a><ul class="nav-links">
<li><a href="/">Home</a></li>
<li class="dropdown">
<a href="/about.html">Company \u25be</a>
<div class="dropdown-menu" style="min-width:240px;">
<div class="dd-section-static-title" style="border-top:none;margin-top:0;padding-top:4px;">Company</div>
<a href="/fleet.html">\U0001f697 Our Fleet</a>
<a href="/flight-tracker.html" style="color:#C9A84C;font-weight:600;">\u2708 Flight Tracker</a>
<a href="/blog/">\U0001f4dd Blog</a>
<a href="/about.html">\u2139\ufe0f About Us</a>
<a href="/contact.html">\U0001f4de Contact</a>
<a href="/gallery.html">\U0001f4f8 Gallery</a>
<a href="/testimonials.html">\u2b50 Reviews</a>
<details class="dd-section">
<summary>Services</summary>
<a href="/services.html#sports">\U0001f3c8 Game Day &amp; Sports</a>
<a href="/services.html#airport">\u2708\ufe0f Airport Transfer</a>
<a href="/services.html#weddings">\U0001f48d Wedding Limo</a>
<a href="/services.html#corporate">\U0001f4bc Corporate Travel</a>
<a href="/services.html#events">\U0001f393 Prom &amp; Graduation</a>
<a href="/services.html#nightout">\U0001f942 Night Out &amp; Party</a>
<a href="/services.html#charter">\U0001f550 Hourly Service</a>
<a href="/services.html" style="font-weight:600;">\u2192 All Services</a>
</details>
<details class="dd-section">
<summary>Locations</summary>
<a href="/limo-service-austin-tx/">\U0001f4cd Austin Limo Service</a>
<a href="/limo-service-dallas-tx/">\U0001f4cd Dallas-Fort Worth</a>
<a href="/limo-service-houston-tx/">\U0001f4cd Houston Limo Service</a>
<a href="/locations/" style="font-weight:600;">\u2192 All Service Areas</a>
</details>
</div>
</li>
<li><a href="/booking.html">Book</a></li>
</ul><div class="nav-cta"><a href="tel:+18337400700" class="nav-phone">\U0001f4de (833) 740-0700</a><a href="https://customer.moovs.app/purple-heart-limo/request/new" target="_blank" class="btn-primary" style="padding:10px 20px;font-size:0.78rem;">Book Now</a></div><button class="hamburger" id="mobileToggle" aria-label="Open navigation menu" aria-expanded="false"><span></span><span></span><span></span></button></nav>
<div id="mobileNav" style="display:none;position:fixed;top:72px;left:0;right:0;background:white;z-index:999;padding:20px;box-shadow:0 12px 48px rgba(45,0,69,0.18);border-bottom:2px solid var(--gray-light);"><a href="/services.html" style="display:block;padding:12px;font-size:0.9rem;color:var(--text);border-bottom:1px solid var(--gray-light);">Services</a><a href="/fleet.html" style="display:block;padding:12px;font-size:0.9rem;color:var(--text);border-bottom:1px solid var(--gray-light);">Fleet</a><a href="/blog/" style="display:block;padding:12px;font-size:0.9rem;color:var(--text);border-bottom:1px solid var(--gray-light);">Blog</a><a href="/contact.html" style="display:block;padding:12px;font-size:0.9rem;color:var(--text);">Contact</a></div>
<script>document.getElementById('mobileToggle').onclick=function(){var m=document.getElementById('mobileNav');m.style.display=m.style.display==='block'?'none':'block';};</script>

<div class="post-hero">
  <div class="breadcrumb"><a href="/">Home</a> \u203a <a href="/blog/">Blog</a> \u203a {{BREADCRUMB_LABEL}}</div>
  <h1>{{H1}} <em>{{H1_EM}}</em></h1>
  <div class="post-meta">{{DATE_HUMAN}} \u00b7 {{READ_TIME}} \u00b7 Purple Heart Limo</div>
</div>

<article>
  <img src="{{HERO_IMG}}" alt="{{HERO_ALT}}" loading="lazy">
  {{BODY_HTML}}
  {{FAQ_VISIBLE}}
</article>

<section class="related-posts" aria-label="Related articles" style="max-width:820px;margin:48px auto 0;padding:30px 32px;background:#F3F0FF;border:1px solid #e4dcf5;border-radius:16px;"><h2 style="font-size:0.95rem;letter-spacing:0.08em;text-transform:uppercase;color:#2D0045;margin:0 0 18px;border-left:4px solid #C9A84C;padding-left:14px;font-family:'Inter',sans-serif;font-weight:700;">Keep Reading</h2><ul style="list-style:none;margin:0;padding:0;display:grid;gap:14px;font-size:1rem;">{{RELATED_LIS}}</ul></section>

<div class="cta-box">
  <h3>{{CTA_H3}}</h3>
  <p>{{CTA_P}}</p>
  <div class="cta-btns"><a href="https://customer.moovs.app/purple-heart-limo/request/new" target="_blank" class="btn-primary">Book Your Ride Now</a><a href="tel:+18337400700" style="display:inline-flex;align-items:center;gap:8px;background:transparent;color:var(--white);padding:13px 28px;border-radius:50px;font-size:0.85rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;border:2px solid rgba(255,255,255,0.4);">\U0001f4de (833) 740-0700</a></div>
</div>

<footer><div class="footer-grid"><div><div class="footer-brand">Purple Heart Limo</div><p style="font-size:0.85rem;line-height:1.7;margin-bottom:16px;">Texan-owned luxury limo &amp; black car service in Austin, Dallas-Fort Worth &amp; Houston, TX.</p><a href="tel:+18337400700" style="color:var(--gold);font-size:0.85rem;">\U0001f4de (833) 740-0700</a></div><div><div class="footer-col-title">Pages</div><ul class="footer-links"><li><a href="/">Home</a></li><li><a href="/services.html">Services</a></li><li><a href="/fleet.html">Fleet</a></li><li><a href="/limo-service-dallas-tx/">Dallas Limo Service</a></li><li><a href="/booking.html">Book Now</a></li></ul></div><div><div class="footer-col-title">Legal</div><ul class="footer-links"><li><a href="/privacy-policy.html">Privacy Policy</a></li><li><a href="/terms-of-service.html">Terms of Service</a></li></ul></div></div><div class="footer-bottom"><span>\u00a9 2026 Purple Heart Limo. All rights reserved. Texan-owned &amp; operated.</span><span>Austin \u00b7 Dallas-Fort Worth \u00b7 Houston, TX</span></div></footer>
</body></html>
"""

#!/usr/bin/env python3
"""Generate service+city landing pages for purpleheartlimo.com.

Clones the existing city-page design (inline CSS, nav, footer, booking form)
and injects unique per-page content, FAQ/Breadcrumb/Service JSON-LD, internal
links, and a corrected booking-form field mapping that matches the Netlify
contact function (name/pickup/dropoff/date/time/message).
"""
import os, json, html

PHONE = "+18337400700"
PHONE_DISP = "(833) 740-0700"
BASE = "https://purpleheartlimo.com"

CSS = """
:root{--purple:#2D0045;--purple-mid:#4a0070;--gold:#C9A84C;--gold-light:#E2C36A;--dark:#0f0f0f;--dark2:#1a1a1a;--dark3:#242424;--gray-light:rgba(255,255,255,0.08);}
*{margin:0;padding:0;box-sizing:border-box;}html{scroll-behavior:smooth;}
body{font-family:'Inter',sans-serif;color:#f5f5f5;background:var(--dark);overflow-x:hidden;}
h1,h2,h3{font-family:'Cormorant Garamond',serif;}a{text-decoration:none;color:inherit;}
.header{position:fixed;top:0;left:0;right:0;z-index:1000;transition:all 0.3s;padding:1rem 5%;}
.header.scrolled{background:rgba(15,15,15,0.97);backdrop-filter:blur(12px);box-shadow:0 2px 30px rgba(0,0,0,0.6);padding:0.6rem 5%;}
.nav{display:flex;align-items:center;justify-content:space-between;gap:1rem;}
.nav-logo{display:flex;align-items:center;gap:10px;}.nav-logo img{width:44px;height:44px;object-fit:contain;border-radius:50%;}
.nav-logo-text{font-family:'Cormorant Garamond',serif !important;font-size:1.45rem;font-weight:700;line-height:1.1;letter-spacing:-0.005em;color:#ffffff !important;text-transform:none !important;font-variant:normal !important;}
.nav-logo-sub{font-size:0.6rem;font-weight:500;color:var(--gold);letter-spacing:0.12em;text-transform:uppercase;display:block;}
.nav-links{display:flex;align-items:center;gap:2rem;list-style:none;}
.nav-links a{color:rgba(255,255,255,0.85);font-size:0.88rem;font-weight:500;transition:color 0.2s;}
.nav-links a:hover{color:var(--gold);}
.nav-cta{display:flex;align-items:center;gap:1rem;}
.nav-phone{color:var(--gold);font-weight:700;font-size:0.88rem;}
.btn-gold{display:inline-flex;align-items:center;gap:6px;background:linear-gradient(135deg,var(--gold),var(--gold-light));color:var(--dark);padding:10px 22px;border-radius:50px;font-size:0.82rem;font-weight:700;text-transform:uppercase;transition:transform 0.2s;box-shadow:0 4px 16px rgba(201,168,76,0.4);}
.btn-gold:hover{transform:translateY(-2px);}
.menu-toggle{display:none;flex-direction:column;gap:5px;cursor:pointer;padding:0.5rem;background:none;border:none;}
.menu-toggle span{display:block;width:25px;height:2px;background:#fff;border-radius:2px;}
@media(max-width:768px){.nav-links{position:fixed;top:0;right:-100%;width:280px;height:100vh;background:var(--dark2);flex-direction:column;align-items:flex-start;padding:5rem 2rem 2rem;gap:1.5rem;transition:right 0.3s;z-index:999;}.nav-links.open{right:0;}.menu-toggle{display:flex;}.nav-cta .btn-gold{display:none;}}
.city-hero{min-height:90vh;display:flex;align-items:center;background:linear-gradient(135deg,#0f0f0f 0%,#1a0533 60%,#0f0f0f 100%);position:relative;overflow:hidden;padding:8rem 5% 5rem;}
.city-hero::after{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 30% 50%,rgba(124,58,237,0.2) 0%,transparent 60%);}
.city-hero-content{position:relative;z-index:2;max-width:720px;}
.hero-badge{display:inline-flex;align-items:center;gap:0.5rem;background:rgba(201,168,76,0.1);border:1px solid rgba(201,168,76,0.3);color:var(--gold);padding:0.4rem 1rem;border-radius:50px;font-size:0.75rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:1.5rem;}
.city-hero h1{font-size:clamp(2.4rem,5vw,4rem);color:#fff;font-weight:300;line-height:1.1;margin-bottom:1.25rem;}
.city-hero h1 em{color:var(--gold);font-style:italic;display:block;}
.city-hero p{color:rgba(255,255,255,0.65);font-size:1rem;line-height:1.85;margin-bottom:2.5rem;max-width:600px;}
.hero-cta{display:flex;gap:1rem;flex-wrap:wrap;align-items:center;}
.btn-call{display:inline-flex;align-items:center;gap:6px;background:transparent;color:#fff;padding:10px 22px;border-radius:50px;font-size:0.82rem;font-weight:700;text-transform:uppercase;border:2px solid rgba(255,255,255,0.3);transition:all 0.2s;}
.btn-call:hover{border-color:#fff;}
.hero-stats{display:flex;gap:2.5rem;margin-top:3rem;padding-top:2rem;border-top:1px solid rgba(255,255,255,0.1);flex-wrap:wrap;}
.stat-num{font-family:'Cormorant Garamond',serif;font-size:2.2rem;color:var(--gold);display:block;line-height:1;}
.stat-label{font-size:0.72rem;color:rgba(255,255,255,0.4);letter-spacing:1px;margin-top:0.25rem;}
.services-strip{background:var(--dark2);padding:4rem 5%;}
.services-strip .inner{max-width:1100px;margin:0 auto;}
.section-label{display:inline-block;font-size:0.75rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--gold);margin-bottom:0.75rem;}
.section-header{text-align:center;margin-bottom:2.5rem;}
.section-title{font-size:clamp(1.7rem,3vw,2.4rem);color:#fff;margin-bottom:0.75rem;}
.section-desc{color:rgba(255,255,255,0.45);max-width:620px;margin:0 auto;font-size:0.9rem;line-height:1.7;}
.services-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;}
.svc-card{background:var(--dark3);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:1.5rem;text-align:center;transition:all 0.25s;}
.svc-card:hover{border-color:rgba(201,168,76,0.4);transform:translateY(-4px);}
.svc-icon{font-size:2rem;margin-bottom:0.75rem;display:block;}
.svc-card h3{font-size:1.05rem;color:#fff;margin-bottom:0.5rem;}
.svc-card p{font-size:0.82rem;color:rgba(255,255,255,0.45);line-height:1.65;}
.seo-body{padding:5rem 5%;background:var(--dark);}
.seo-body .inner{max-width:820px;margin:0 auto;}
.seo-body h2{font-size:clamp(1.6rem,3vw,2.2rem);color:#fff;margin:2.2rem 0 1rem;}
.seo-body h2:first-child{margin-top:0;}
.seo-body p{color:rgba(255,255,255,0.6);font-size:0.97rem;line-height:1.95;margin-bottom:1.1rem;}
.seo-body ul{color:rgba(255,255,255,0.6);font-size:0.97rem;line-height:1.9;margin:0 0 1.2rem 1.2rem;}
.seo-body li{margin-bottom:0.4rem;}
.seo-body a{color:var(--gold);text-decoration:underline;text-underline-offset:3px;}
.booking-section{padding:5rem 5%;background:var(--dark2);}
.booking-section .inner{max-width:680px;margin:0 auto;}
.form-card{background:var(--dark);border:1px solid rgba(255,255,255,0.08);border-radius:24px;padding:3rem;}
.form-card h2{font-size:clamp(1.6rem,3vw,2.2rem);color:#fff;text-align:center;margin-bottom:0.5rem;}
.form-card .sub{color:rgba(255,255,255,0.45);text-align:center;font-size:0.88rem;margin-bottom:2rem;}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:1rem;}
@media(max-width:600px){.form-row{grid-template-columns:1fr;}}
.form-group{margin-bottom:1.1rem;}
.form-group label{display:block;font-size:0.78rem;font-weight:600;color:rgba(255,255,255,0.45);margin-bottom:0.4rem;letter-spacing:0.5px;text-transform:uppercase;}
.form-group input,.form-group select,.form-group textarea{width:100%;padding:0.875rem 1rem;background:var(--dark3);border:1px solid rgba(255,255,255,0.1);border-radius:10px;color:#fff;font-size:0.95rem;font-family:inherit;transition:border-color 0.2s;outline:none;}
.form-group input:focus,.form-group select:focus,.form-group textarea:focus{border-color:var(--gold);}
.form-group select option{background:var(--dark3);}
.form-group textarea{min-height:100px;resize:vertical;}
.submit-btn{width:100%;padding:1rem;background:linear-gradient(135deg,var(--gold),var(--gold-light));color:var(--dark);font-size:1rem;font-weight:700;letter-spacing:0.05em;text-transform:uppercase;border:none;border-radius:50px;cursor:pointer;transition:transform 0.2s,box-shadow 0.2s;box-shadow:0 4px 20px rgba(201,168,76,0.4);margin-top:0.5rem;}
.submit-btn:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(201,168,76,0.5);}
.alert{padding:1rem;border-radius:10px;font-size:0.9rem;margin-bottom:1rem;display:none;}
.alert.show{display:block;}
.alert-success{background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);color:#34d399;}
.alert-error{background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);color:#f87171;}
.or-divider{text-align:center;color:rgba(255,255,255,0.3);font-size:0.82rem;margin:1.5rem 0;position:relative;}
.or-divider::before,.or-divider::after{content:'';position:absolute;top:50%;width:40%;height:1px;background:rgba(255,255,255,0.08);}
.or-divider::before{left:0;}.or-divider::after{right:0;}
.call-cta{text-align:center;}
.call-cta a{color:var(--gold);font-weight:700;font-size:1.15rem;}
.why-section{padding:5rem 5%;background:var(--dark);}
.why-section .inner{max-width:1100px;margin:0 auto;}
.why-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1.5rem;margin-top:2.5rem;}
.why-card{background:var(--dark3);border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:1.75rem;}
.why-card h3{font-size:1.1rem;color:#fff;margin-bottom:0.5rem;}
.why-card p{font-size:0.88rem;color:rgba(255,255,255,0.5);line-height:1.75;}
.faq-section{padding:5rem 5%;background:var(--dark2);}
.faq-section .inner{max-width:820px;margin:0 auto;}
.faq-item{background:var(--dark3);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:1.4rem 1.6rem;margin-bottom:1rem;}
.faq-item h3{font-size:1.05rem;color:var(--gold);margin-bottom:0.5rem;}
.faq-item p{font-size:0.9rem;color:rgba(255,255,255,0.6);line-height:1.8;}
.related{padding:4rem 5%;background:var(--dark);}
.related .inner{max-width:1100px;margin:0 auto;}
.related-grid{display:flex;flex-wrap:wrap;gap:0.8rem;justify-content:center;margin-top:1.5rem;}
.related-grid a{background:var(--dark3);border:1px solid rgba(201,168,76,0.25);color:var(--gold);padding:0.7rem 1.2rem;border-radius:50px;font-size:0.85rem;font-weight:600;transition:all 0.2s;}
.related-grid a:hover{background:rgba(201,168,76,0.12);transform:translateY(-2px);}
footer{background:var(--dark2);border-top:1px solid rgba(255,255,255,0.07);padding:3rem 5% 1.5rem;}
.footer-bottom{max-width:1200px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;}
.footer-bottom p{color:rgba(255,255,255,0.3);font-size:0.82rem;}
.footer-bottom-links{display:flex;gap:1.5rem;flex-wrap:wrap;}
.footer-bottom-links a{color:rgba(255,255,255,0.3);font-size:0.82rem;}
.footer-bottom-links a:hover{color:var(--gold);}
"""

HEADER = """<header class="header" id="header">
<div class="nav">
<a class="nav-logo" href="/"><img alt="Purple Heart Limo" src="/logo.webp"/><div><div class="nav-logo-text">Purple Heart Limo</div><span class="nav-logo-sub">Texan Owned &middot; TX</span></div></a>
<ul class="nav-links" id="navLinks">
<li><a href="/">Home</a></li><li><a href="/services.html">Services</a></li><li><a href="/fleet.html">Fleet</a></li><li><a href="/rates.html">Rates</a></li><li><a href="/blog/">Blog</a></li><li><a href="/contact.html">Contact</a></li>
</ul>
<div class="nav-cta"><a class="nav-phone" href="tel:%s">&#128222; %s</a><a class="btn-gold" href="https://customer.moovs.app/purple-heart-limo/request/new" target="_blank">Book Now</a></div>
<button class="menu-toggle" id="menuToggle"><span></span><span></span><span></span></button>
</div>
</header>""" % (PHONE, PHONE_DISP)

FOOTER = """<footer>
<div class="footer-bottom">
<p>&copy; 2026 Purple Heart Limo. All rights reserved. Texan-Owned &middot; Texas</p>
<div class="footer-bottom-links">
<a href="/limo-service-austin-tx/">Austin</a><a href="/limo-service-dallas-tx/">Dallas-Fort Worth</a><a href="/limo-service-houston-tx/">Houston</a>
<a href="/privacy-policy.html">Privacy</a><a href="/terms-of-service.html">Terms</a><a href="/cancellation-policy.html">Cancellation</a>
</div>
</div>
</footer>"""

SCRIPT = """<script>
const h=document.getElementById('header');
window.addEventListener('scroll',()=>h.classList.toggle('scrolled',scrollY>60),{passive:true});
const mt=document.getElementById('menuToggle'),nl=document.getElementById('navLinks');
mt.addEventListener('click',()=>{const o=mt.classList.toggle('active');nl.classList.toggle('open',o);});
document.getElementById('bookingForm').addEventListener('submit', async function(e){
  e.preventDefault();
  const btn=this.querySelector('.submit-btn');
  const ok=document.getElementById('alertSuccess'),err=document.getElementById('alertError');
  const orig=btn.textContent;btn.textContent='Sending...';btn.disabled=true;
  ok.classList.remove('show');err.classList.remove('show');
  const f=Object.fromEntries(new FormData(this));
  const payload={
    name:[f.first_name,f.last_name].filter(Boolean).join(' ').trim(),
    email:f.email,phone:f.phone,service:f.service,vehicle:f.vehicle,
    passengers:f.passengers||'',date:f.pickup_date,time:f.pickup_time,
    pickup:f.pickup_address,dropoff:f.dropoff_address,message:f.notes||'',city:f.city||''
  };
  try{
    const res=await fetch('/.netlify/functions/contact',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    const json=await res.json();
    if(res.ok&&json.success){ok.textContent="\\u2713 Booking request received! We'll confirm within 30 minutes. Check your email and phone.";ok.classList.add('show');this.reset();}
    else{throw new Error(json.error||'Error');}
  }catch{err.textContent="Something went wrong. Please call us directly at %s.";err.classList.add('show');}
  finally{btn.textContent=orig;btn.disabled=false;}
});
</script>""" % PHONE_DISP

FONTS = """<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,400&amp;family=Inter:wght@300;400;500;600;700&amp;display=swap" rel="stylesheet"/>"""


def esc(s):
    return html.escape(s, quote=True)


def svc_cards(cards):
    out = []
    for icon, title, desc in cards:
        out.append('<div class="svc-card"><span class="svc-icon">%s</span><h3>%s</h3><p>%s</p></div>' % (icon, esc(title), esc(desc)))
    return "\n".join(out)


def why_cards(cards):
    out = []
    for title, desc in cards:
        out.append('<div class="why-card"><h3>%s</h3><p>%s</p></div>' % (esc(title), esc(desc)))
    return "\n".join(out)


def faq_html(faqs):
    out = []
    for q, a in faqs:
        out.append('<div class="faq-item"><h3>%s</h3><p>%s</p></div>' % (esc(q), esc(a)))
    return "\n".join(out)


def related_html(links):
    out = ['<a href="%s">%s</a>' % (url, esc(label)) for url, label in links]
    return "\n".join(out)


def options_html(opts):
    return "\n".join('<option>%s</option>' % esc(o) for o in opts)


def schema_block(p):
    url = "%s/%s/" % (BASE, p["slug"])
    graph = [
        {
            "@type": ["Service", "LimousineService", "LocalBusiness"],
            "name": p["schema_name"],
            "description": p["meta"],
            "url": url,
            "telephone": PHONE,
            "email": "info@purpleheartlimo.com",
            "image": "%s/images/%s" % (BASE, p.get("image", "sedan-cadillac.webp")),
            "areaServed": [{"@type": "City", "name": c} for c in p["areas"]],
            "address": {"@type": "PostalAddress", "addressLocality": p["locality"], "addressRegion": "TX", "addressCountry": "US"},
            "openingHoursSpecification": {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59"},
            "priceRange": "$$",
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": str(p["reviews"]), "bestRating": "5"},
            "sameAs": ["https://www.facebook.com/profile.php?id=61578479742416", "https://www.instagram.com/austinlimousine"],
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": p["hub_name"], "item": "%s/%s/" % (BASE, p["hub_slug"])},
                {"@type": "ListItem", "position": 3, "name": p["crumb"], "item": url},
            ],
        },
        {
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faqs"]],
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def render(p):
    url = "%s/%s/" % (BASE, p["slug"])
    body_html = "".join(
        ("<h2>%s</h2>" % esc(h) if h else "") + "".join("<p>%s</p>" % seg if not seg.startswith("<ul") else seg for seg in segs)
        for h, segs in p["body"]
    )
    parts = []
    parts.append('<!DOCTYPE html>')
    parts.append('<html lang="en">')
    parts.append('<head>')
    parts.append('<link href="/favicon.png" rel="icon" type="image/png"/>')
    parts.append('<meta charset="utf-8"/>')
    parts.append('<meta content="width=device-width, initial-scale=1.0" name="viewport"/>')
    parts.append('<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1"/>')
    parts.append('<title>%s</title>' % esc(p["title"]))
    parts.append('<meta content="%s" name="description"/>' % esc(p["meta"]))
    parts.append('<link href="%s" rel="canonical"/>' % url)
    parts.append('<script type="application/ld+json">%s</script>' % schema_block(p))
    parts.append(FONTS)
    parts.append('<style>%s</style>' % CSS)
    parts.append('<link href="/css/global.css" rel="stylesheet"/>')
    parts.append('</head>')
    parts.append('<body>')
    parts.append(HEADER)
    # hero
    parts.append('<section class="city-hero"><div class="city-hero-content">')
    parts.append('<div class="hero-badge">%s</div>' % esc(p["badge"]))
    parts.append('<h1>%s <em>%s</em></h1>' % (esc(p["h1_main"]), esc(p["h1_em"])))
    parts.append('<p>%s</p>' % esc(p["hero_p"]))
    parts.append('<div class="hero-cta"><a class="btn-gold" href="#book" style="padding:14px 32px;font-size:0.9rem;">Book Your Ride</a><a class="btn-call" href="tel:%s">&#128222; %s</a></div>' % (PHONE, PHONE_DISP))
    stats = "".join('<div><span class="stat-num">%s</span><div class="stat-label">%s</div></div>' % (n, esc(l)) for n, l in p["stats"])
    parts.append('<div class="hero-stats">%s</div>' % stats)
    parts.append('</div></section>')
    # services
    parts.append('<section class="services-strip"><div class="inner"><div class="section-header">')
    parts.append('<span class="section-label">%s</span><h2 class="section-title">%s</h2><p class="section-desc">%s</p>' % (esc(p["svc_label"]), esc(p["svc_title"]), esc(p["svc_desc"])))
    parts.append('</div><div class="services-grid">%s</div></div></section>' % svc_cards(p["cards"]))
    # seo body
    parts.append('<section class="seo-body"><div class="inner">%s</div></section>' % body_html)
    # booking form
    parts.append('<section class="booking-section" id="book"><div class="inner"><div class="form-card">')
    parts.append('<h2>%s</h2>' % esc(p["form_title"]))
    parts.append('<p class="sub">Fill out the form &mdash; we\'ll confirm your booking and send details to info@purpleheartlimo.com</p>')
    parts.append('<div class="alert alert-success" id="alertSuccess"></div><div class="alert alert-error" id="alertError"></div>')
    parts.append('<form id="bookingForm">')
    parts.append('<div class="form-row"><div class="form-group"><label>First Name *</label><input name="first_name" placeholder="John" required="" type="text"/></div><div class="form-group"><label>Last Name *</label><input name="last_name" placeholder="Smith" required="" type="text"/></div></div>')
    parts.append('<div class="form-row"><div class="form-group"><label>Phone *</label><input name="phone" placeholder="(512) 555-0100" required="" type="tel"/></div><div class="form-group"><label>Email *</label><input name="email" placeholder="you@email.com" required="" type="email"/></div></div>')
    parts.append('<div class="form-row"><div class="form-group"><label>Service Type *</label><select name="service" required=""><option value="">Select service...</option>%s</select></div>' % options_html(p["service_opts"]))
    parts.append('<div class="form-group"><label>Vehicle *</label><select name="vehicle" required=""><option value="">Select vehicle...</option>%s</select></div></div>' % options_html(p["vehicle_opts"]))
    parts.append('<div class="form-row"><div class="form-group"><label>Pickup Date *</label><input name="pickup_date" required="" type="date"/></div><div class="form-group"><label>Pickup Time *</label><input name="pickup_time" required="" type="time"/></div></div>')
    parts.append('<div class="form-group"><label>Pickup Address *</label><input name="pickup_address" placeholder="%s" required="" type="text"/></div>' % esc(p["pickup_ph"]))
    parts.append('<div class="form-group"><label>Dropoff Address *</label><input name="dropoff_address" placeholder="Destination address" required="" type="text"/></div>')
    parts.append('<div class="form-group"><label>Additional Notes</label><textarea name="notes" placeholder="Number of passengers, stops, special requests..."></textarea></div>')
    parts.append('<input name="city" type="hidden" value="%s"/>' % esc(p["city_val"]))
    parts.append('<button class="submit-btn" type="submit">%s</button>' % esc(p["form_btn"]))
    parts.append('</form>')
    parts.append('<div class="or-divider">or call us directly</div>')
    parts.append('<div class="call-cta"><a href="tel:%s">&#128222; %s</a><div style="color:rgba(255,255,255,0.3);font-size:0.8rem;margin-top:0.4rem;">Available 24/7 &middot; %s</div></div>' % (PHONE, PHONE_DISP, esc(p["locality"] + ", TX")))
    parts.append('</div></div></section>')
    # why
    parts.append('<section class="why-section"><div class="inner"><div class="section-header"><span class="section-label">Why Purple Heart</span><h2 class="section-title">%s</h2></div><div class="why-grid">%s</div></div></section>' % (esc(p["why_title"]), why_cards(p["why"])))
    # faq
    parts.append('<section class="faq-section"><div class="inner"><div class="section-header"><span class="section-label">FAQ</span><h2 class="section-title">%s</h2></div>%s</div></section>' % (esc(p["faq_title"]), faq_html(p["faqs"])))
    # related
    parts.append('<section class="related"><div class="inner"><div class="section-header"><span class="section-label">Explore More</span><h2 class="section-title">Related Services</h2></div><div class="related-grid">%s</div></div></section>' % related_html(p["related"]))
    parts.append(FOOTER)
    parts.append(SCRIPT)
    parts.append('</body></html>')
    return "\n".join(parts)


STD_WHY = [
    ("\U0001F6E1\uFE0F Texan-Owned", "Founded and operated by a U.S. military veteran. Mission discipline applied to every booking, every driver, every ride."),
    ("\U0001F4B0 Flat Rates", "No surge pricing. No surprise fees. The price at booking is the price you pay \u2014 regardless of event crowds or time of night."),
    ("\u2708\uFE0F Flight Monitoring", "Airport pickups automatically adjust to real-time flight status. Your driver knows before you land."),
    ("\u23F0 Punctuality", "Drivers arrive 10+ minutes early. Proactive communication if anything changes. Late is not our standard."),
]

AUSTIN_AREAS = ["Austin", "Round Rock", "Cedar Park", "Georgetown", "Pflugerville", "Lakeway", "Bee Cave", "Kyle"]
DALLAS_AREAS = ["Dallas", "Fort Worth", "Plano", "Irving", "Frisco", "Arlington", "University Park", "Highland Park", "Las Colinas"]

from pages_data import build_pages  # noqa: E402

PAGES = build_pages(STD_WHY, AUSTIN_AREAS, DALLAS_AREAS)

if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for p in PAGES:
        d = os.path.join(root, p["slug"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(render(p))
        print("wrote", p["slug"] + "/index.html")
    print("done:", len(PAGES), "pages")

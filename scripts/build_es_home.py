#!/usr/bin/env python3
"""H1/1b: Build standalone Spanish homepage /es/index.html from the embedded
es-home-page block in index.html, using the es/fleet.html shell (Spanish
nav/footer) and extracting the homepage hero/areas CSS into css/es-home.css."""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
idx = (ROOT / "index.html").read_text(encoding="utf-8")
shell = (ROOT / "es" / "fleet.html").read_text(encoding="utf-8")

# ---------- CSS ----------
css_src = re.search(r"<style>(.*?)</style>", idx, re.S).group(1)
css_src = re.sub(r"/\*.*?\*/", "", css_src, flags=re.S)

WL = re.compile(
    r"^(\.hero\b|\.hero:|\.hero-inner|\.hero-content|\.hero-badge|\.hero-divider|\.hero-sub|"
    r"\.hero-trust|\.trust-item|\.trust-icon|\.hero-btns|\.hero h1|\.hero-overlay|"
    r"\.vet-strip|\.medal|\.areas-section|\.areas-grid|\.area-col|\.area-cities|\.city-tag)"
)

def parse_rules(block):
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

out = ["/* Spanish homepage hero/areas styles extracted from index.html (H1 audit). */"]
for sel, body in parse_rules(css_src):
    if sel.startswith("@media"):
        keep = [(s, b) for s, b in parse_rules(body) if WL.match(s.strip())]
        if keep:
            out.append(sel + " {")
            out += [f"  {s} {{ {b.strip()} }}" for s, b in keep]
            out.append("}")
    elif WL.match(sel):
        out.append(f"{sel} {{ {body.strip()} }}")
css_text = "\n".join(out) + "\n"
# inline index.html CSS resolved urls from site root; /css/ needs absolute paths
css_text = css_text.replace("url('images/", "url('/images/").replace('url("images/', 'url("/images/').replace("url(images/", "url(/images/")
(ROOT / "css" / "es-home.css").write_text(css_text, encoding="utf-8")

# ---------- content block ----------
m = re.search(r'<div class="page" id="es-home-page">', idx)
start = m.end()
pat = re.compile(r"<div\b|</div>")
depth, i = 1, start
while depth:
    m2 = pat.search(idx, i)
    depth += 1 if m2.group(0) == "<div" else -1
    i = m2.end()
content = idx[start:m2.start()].strip()

URLMAP = {
    "airport": "/airport-transfer.html", "wedding": "/wedding-limo.html",
    "quinceaneara": "/quinceanera-limo.html", "prom": "/prom-limo.html",
    "corporate": "/corporate-car-service.html", "worldcup": "/world-cup-2026.html",
    "home": "/",
}
content = re.sub(r"""onclick="return showPage\('([^']+)'\)\"""",
                 lambda m: 'onclick="window.location.href=\'%s\';return false;"' % URLMAP.get(m.group(1), "/"), content)
content = content.replace("""<a href="#" onclick="window.location.href='/';return false;" style="color:var(--gray);font-size:0.8rem;">Switch to English / Cambiar a Inglés →</a>""",
                          """<a href="/" style="color:var(--gray);font-size:0.8rem;">Switch to English / Cambiar a Inglés →</a>""")
# hero h2 -> h1
content = content.replace("<h2>", "<h1>", 1).replace("</h2>", "</h1>", 1)
# Veteran wording per audit H3/H4: founded by a veteran, Texan-owned today
content = content.replace("Dueño Veterano", "Fundada por un Veterano")
content = content.replace("<span class=\"trust-icon\">🎖️</span> Empresa Veterana", "<span class=\"trust-icon\">🎖️</span> Fundada por un Veterano")
content = content.replace("Empresa Orgullosamente Veterana", "Fundada por un Veterano Militar de los EE.UU.")
content = content.replace("Al reservar con nosotros, apoya una empresa texana propiedad de un veterano.",
                          "Hoy somos una empresa con dueño tejano, operada con la misma disciplina en cada viaje.")
content = content.replace("Lujo de propiedad veterana.", "Fundada por un veterano. Dueño tejano.")
# replace booking-widget mount with a booking CTA card
content = content.replace(
    '<div id="es-bk-mount" style="min-width:0;"></div>',
    '''<div style="background:rgba(255,255,255,0.04);border:1.5px solid rgba(201,168,76,0.35);border-radius:18px;padding:36px 32px;text-align:center;">
<div style="font-size:2.2rem;margin-bottom:10px;">🚘</div>
<h3 style="color:#fff;font-size:1.4rem;font-weight:400;font-family:'Cormorant Garamond',serif;margin-bottom:10px;">Cotiza y Reserva en Línea</h3>
<p style="color:rgba(255,255,255,0.65);font-size:0.85rem;line-height:1.7;margin-bottom:22px;">Precios de tarifa plana al instante — aeropuerto, punto a punto o por hora. Sin precios inflados, nunca.</p>
<a class="btn-primary" href="/es/booking.html" style="width:100%;justify-content:center;display:inline-flex;">Cotizar Mi Viaje →</a>
<a class="btn-white" href="tel:+18337400700" style="width:100%;justify-content:center;display:inline-flex;margin-top:10px;">📞 (833) 740-0700</a>
</div>''')

TITLE = "Servicio de Limusina en Texas — Austin, Dallas y Houston | Purple Heart Limo"
DESC = "Servicio premium de limusina y auto de lujo en Austin, Dallas-Fort Worth y Houston. Tarifas planas, choferes profesionales, sin precios inflados. Reserva hoy."

head = shell[:shell.index("<title>")]
body_start = shell.index('<body data-lang="es">')
nav_end = shell.index('<section class="page-hero">')
nav = shell[body_start:nav_end]
footer = shell[shell.index("<footer>"):shell.index("<script>\nfunction toggleMenu")]

schema = '''<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@type": "WebPage",
 "name": "Purple Heart Limo — Servicio de Limusina en Texas",
 "url": "https://purpleheartlimo.com/es/",
 "inLanguage": "es",
 "description": "%s",
 "publisher": { "@type": "Organization", "name": "Purple Heart Limo", "url": "https://purpleheartlimo.com", "telephone": "+18337400700" }
}
</script>''' % DESC

page = (
    head
    + f"<title>{TITLE}</title>\n"
    + f'<meta name="description" content="{DESC}"/>\n'
    + '<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1"/>\n'
    + '<link rel="canonical" href="https://purpleheartlimo.com/es/"/>\n'
    + '<meta name="geo.region" content="US-TX"/>\n'
    + '<meta name="geo.placename" content="Austin, Dallas-Fort Worth, Houston"/>\n'
    + '<meta property="og:type" content="website"/>\n'
    + '<meta property="og:url" content="https://purpleheartlimo.com/es/"/>\n'
    + f'<meta property="og:title" content="{TITLE}"/>\n'
    + f'<meta property="og:description" content="{DESC}"/>\n'
    + '<meta property="og:image" content="https://purpleheartlimo.com/images/og-image.jpg"/>\n'
    + '<meta name="twitter:card" content="summary_large_image"/>\n'
    + f'<meta name="twitter:title" content="{TITLE}"/>\n'
    + f'<meta name="twitter:description" content="{DESC}"/>\n'
    + '<link rel="preconnect" href="https://fonts.googleapis.com"/>\n'
    + '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>\n'
    + '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" media="print" onload="this.media=\'all\'"/>\n'
    + '<link rel="stylesheet" href="/css/page.css"/>\n'
    + schema + "\n"
    + '<link rel="stylesheet" href="/css/global.css"/>\n'
    + '<link rel="stylesheet" href="/css/header.css"/>\n'
    + '<link rel="stylesheet" href="/css/svc.css"/>\n'
    + '<link rel="stylesheet" href="/css/es-home.css"/>\n'
    + '<link href="https://purpleheartlimo.com/" hreflang="en" rel="alternate"/><link href="https://purpleheartlimo.com/es/" hreflang="es" rel="alternate"/><link href="https://purpleheartlimo.com/" hreflang="x-default" rel="alternate"/></head>\n'
    + nav
    + "<main>\n" + content + "\n</main>\n"
    + footer
    + "<script>\nfunction toggleMenu(){const m=document.getElementById('mobile-menu');const b=document.getElementById('hamburger');const open=m.style.display!=='block';m.style.display=open?'block':'none';if(b)b.setAttribute('aria-expanded',open?'true':'false');}\n</script>\n"
    + '<script defer="" src="/js/nav-dropdown.js"></script>\n'
    + "</body>\n</html>\n"
)
# ES nav: language toggle should point at the English homepage, not /fleet.html
page = page.replace('<li><a href="/fleet.html" style="color:#C9A84C;font-weight:700;letter-spacing:0.08em;">🌐 English</a></li>',
                    '<li><a href="/" style="color:#C9A84C;font-weight:700;letter-spacing:0.08em;">🌐 English</a></li>')
page = page.replace('<a href="/fleet.html" id="lang-toggle"', '<a href="/" id="lang-toggle"')
page = page.replace('<div id="mobile-menu" style="display:none;position:fixed;top:72px;left:0;right:0;background:white;z-index:999;padding:20px;box-shadow:0 12px 48px rgba(45,0,69,0.18);border-bottom:2px solid #F2EFE8;"><a href="/fleet.html"',
                    '<div id="mobile-menu" style="display:none;position:fixed;top:72px;left:0;right:0;background:white;z-index:999;padding:20px;box-shadow:0 12px 48px rgba(45,0,69,0.18);border-bottom:2px solid #F2EFE8;"><a href="/"')
(ROOT / "es" / "index.html").write_text(page, encoding="utf-8")
print("wrote es/index.html", len(page), "bytes; css/es-home.css", (ROOT / "css" / "es-home.css").stat().st_size, "bytes")

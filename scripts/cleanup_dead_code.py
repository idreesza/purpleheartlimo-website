#!/usr/bin/env python3
"""H1/1d: Remove dead JS + unused CSS from index.html after block deletion."""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
p = ROOT / "index.html"
idx = p.read_text(encoding="utf-8")

# ---- 1. showPage -> redirect shim (safety net for any stray caller) ----
m = re.search(r"// ===== PAGE ROUTER =====\nfunction showPage\(id\) \{.*?\n\}\n", idx, re.S)
shim = """// ===== PAGE ROUTER (legacy shim) =====
// Hidden page blocks were replaced by real standalone pages (SEO audit H1).
const PAGE_URLS = {home:'/','about':'/about.html',fleet:'/fleet.html',contact:'/contact.html',
  blog:'/blog/',faq:'/faq.html',reviews:'/testimonials.html',military:'/military-discount.html',
  'es-home':'/es/',airport:'/airport-transfer.html',wedding:'/wedding-limo.html',
  corporate:'/corporate-car-service.html',prom:'/prom-limo.html',nightout:'/night-out-limo.html',
  hourly:'/hourly-car-service.html',quinceaneara:'/quinceanera-limo.html',
  worldcup:'/world-cup-2026.html',privacy:'/privacy-policy.html',terms:'/terms-of-service.html',
  accessibility:'/accessibility.html',sitemap:'/sitemap.html'};
function showPage(id) {
  window.location.href = PAGE_URLS[id] || '/';
  return false;
}
"""
assert m, "showPage not found"
idx = idx[:m.start()] + shim + idx[m.end():]

# ---- 2. remove showBlog / shareBlog / toggleFAQ ----
for header, name in [("// ===== BLOG ROUTER =====\n", "showBlog"),
                     ("", "shareBlog"),
                     ("// ===== FAQ =====\n", "toggleFAQ")]:
    mm = re.search(re.escape(header) + r"function %s\([^)]*\) \{.*?\n\}\n" % name, idx, re.S)
    assert mm, name
    idx = idx[:mm.start()] + idx[mm.end():]

# ---- 3. bkRelocate: drop es-home branch (block + mount removed) ----
old_branch = """  if (id === 'es-home') {
    const m = document.getElementById('es-bk-mount');
    if (m && !m.contains(w)) m.appendChild(w);
    bkSetLang('es');
  } else if (id === 'home') {"""
new_branch = """  if (id === 'home') {"""
assert old_branch in idx
idx = idx.replace(old_branch, new_branch)

# ---- 4. SPA lang toggle should navigate to the real /es/ homepage ----
idx = idx.replace(
    "const ES_PAGES = ['/fleet.html','/booking.html','/contact.html',",
    "const ES_PAGES = ['/','/fleet.html','/booking.html','/contact.html',")

# ---- 5. purge unused CSS rules ----
DEAD = re.compile(r"\.(svc-hero|breadcrumb|faq-list|faq-item|faq-q|faq-a|faq-icon|"
                  r"legal-page|legal-date|sitemap-grid|sitemap-col)\b|#es-home-page")

sm = re.search(r"<style>(.*?)</style>", idx, re.S)
css = sm.group(1)

def parse_rules(block):
    out, i = [], 0
    while True:
        b1 = block.find("{", i)
        if b1 == -1:
            out.append((None, block[i:]))
            return out
        sel = block[i:b1]
        depth, j = 1, b1 + 1
        while depth and j < len(block):
            if block[j] == "{":
                depth += 1
            elif block[j] == "}":
                depth -= 1
            j += 1
        out.append((sel, block[b1 + 1:j - 1]))
        i = j

def clean(block):
    parts = []
    for sel, body in parse_rules(block):
        if sel is None:
            parts.append(body)
            continue
        s = sel.strip()
        if s.startswith("@media"):
            inner = clean(body)
            if re.search(r"[^\s{}]", re.sub(r"/\*.*?\*/", "", inner, flags=re.S)):
                parts.append(f"{sel}{{{inner}}}")
            continue
        selectors = [x.strip() for x in s.split(",")]
        kept = [x for x in selectors if not DEAD.search(x)]
        if kept:
            parts.append("%s { %s }\n" % (", ".join(kept), body.strip()) if kept != selectors else f"{sel}{{{body}}}")
    return "".join(parts)

new_css = clean(css)
idx = idx[:sm.start(1)] + new_css + idx[sm.end(1):]

p.write_text(idx, encoding="utf-8")
print("index.html now", p.stat().st_size, "bytes")

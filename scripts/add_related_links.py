import glob, os, re, html

files = sorted(f for f in glob.glob("blog/*.html") if os.path.basename(f) != "index.html")

def get_title(path):
    t = open(path, encoding="utf-8").read()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else os.path.basename(path)

titles = {f: get_title(f) for f in files}
n = len(files)
SECTION_RE = re.compile(r'\n?<section class="related-posts".*?</section>', re.S)
changed = 0

for i, f in enumerate(files):
    src = open(f, encoding="utf-8").read()
    src = SECTION_RE.sub("", src)  # remove any existing block (idempotent)
    rel = [files[(i + k) % n] for k in range(1, 7)]
    items = ""
    for r in rel:
        href = "/blog/" + os.path.basename(r)
        items += ('<li><a href="%s" style="color:rgba(255,255,255,0.85);'
                  'font-weight:600;">%s</a></li>' % (href, html.escape(titles[r])))
    block = (
        '<section class="related-posts" aria-label="Related articles" '
        'style="max-width:820px;margin:0 auto;padding:10px 5% 0;">'
        '<h2 style="font-family:\'Cormorant Garamond\',serif;font-size:1.4rem;font-weight:400;'
        'color:#fff;margin:0 0 1rem;padding-bottom:6px;'
        'border-bottom:1px solid rgba(201,168,76,0.18);">Keep Reading</h2>'
        '<ul>' + items + '</ul></section>'
    )
    new = src.replace("<footer", block + "\n<footer", 1)
    if new == src:
        print("NO FOOTER ANCHOR:", f); continue
    open(f, "w", encoding="utf-8").write(new)
    changed += 1

print(f"files={n} changed={changed}")

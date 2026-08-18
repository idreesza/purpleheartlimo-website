#!/usr/bin/env python3
"""H1/1c: Delete all hidden .page blocks from index.html except home-page."""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
p = ROOT / "index.html"
idx = p.read_text(encoding="utf-8")

pat_open = re.compile(r'<div class="page" id="([a-z0-9-]+)-page">')
pat_div = re.compile(r"<div\b|</div>")
removed = []
while True:
    m = next((m for m in pat_open.finditer(idx) if m.group(1) != "home"), None)
    if not m:
        break
    depth, i = 1, m.end()
    while depth:
        m2 = pat_div.search(idx, i)
        depth += 1 if m2.group(0) == "<div" else -1
        i = m2.end()
    # also swallow a preceding comment banner if directly above
    start = m.start()
    pre = idx.rfind("<!-- ==", 0, start)
    if pre != -1 and idx[pre:start].count("-->") == 1 and not idx[idx.find("-->", pre) + 3:start].strip():
        start = pre
    removed.append(m.group(1))
    idx = idx[:start] + idx[i:]

p.write_text(idx, encoding="utf-8")
print("removed %d blocks:" % len(removed), ", ".join(removed))
print("index.html now", p.stat().st_size, "bytes")

#!/usr/bin/env python3
"""Tie legacy destination/travel articles to chauffeured transportation intent."""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent.parent
TRANSPORT = re.compile(r"\b(limo|limousine|car service|chauffeur|transportation|party bus|airport transfer|shuttle)\b", re.I)
MARKER = 'data-phl-transport-intent="true"'


def clean(v):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", v))).strip()


def clip(v, n):
    v = clean(v).strip(" -|:—")
    return v if len(v) <= n else v[:n + 1].rsplit(" ", 1)[0].strip(" -|:—")


def transform(path):
    s = path.read_text(encoding="utf-8")
    tm = re.search(r"<title\b[^>]*>(.*?)</title>", s, re.I | re.S)
    hm = re.search(r"<h1\b[^>]*>(.*?)</h1>", s, re.I | re.S)
    if not tm or not hm or MARKER in s or TRANSPORT.search(clean(tm.group(1))):
        return False
    topic = clean(hm.group(1))
    lower = (topic + " " + path.as_posix()).lower()
    if "austin" in lower or "round rock" in lower:
        service, label = "/limo-service-austin-tx/", "Austin limo service"
    elif "houston" in lower:
        service, label = "/limo-service-houston-tx/", "Houston limo service"
    else:
        service, label = "/limo-service-dallas-tx/", "Dallas limo service"
    short = clip(topic, 34)
    title = clip(short + " Limo Guide", 39) + " | Purple Heart Limo"
    s = s[:tm.start()] + f"<title>{html.escape(title)}</title>" + s[tm.end():]
    section = f'''<section {MARKER} class="phl-transport-intent">
<h2>{html.escape(short)} Transportation Planning</h2>
<p>Planning a visit to {html.escape(short)}? Purple Heart Limo provides prearranged chauffeured transportation for airport arrivals, dinners, events, and groups. Choose a sedan, luxury SUV, stretch limousine, Sprinter, or party bus based on passenger and luggage needs, with a confirmed pickup plan instead of parking or rideshare uncertainty.</p>
<p>Review our <a href="{service}">{label}</a>, compare the <a href="/fleet.html">chauffeured fleet</a>, or <a href="/booking.html">request a quote online</a>. For timing and vehicle guidance, call <a href="tel:+18337400700">(833) 740-0700</a> 24/7.</p>
</section>'''
    anchor = re.search(r"<(?:article|main)\b[^>]*>", s, re.I)
    if not anchor:
        raise ValueError(f"{path}: no article/main")
    s = s[:anchor.end()] + "\n" + section + s[anchor.end():]
    path.write_text(s, encoding="utf-8")
    return True


def main():
    changed = [p for p in sorted((ROOT / "blog").rglob("*.html"))
               if p != ROOT / "blog" / "index.html" and transform(p)]
    print(f"reframed {len(changed)} blog posts")


if __name__ == "__main__":
    main()
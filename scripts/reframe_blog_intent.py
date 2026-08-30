#!/usr/bin/env python3
"""Reframe legacy destination posts around chauffeured transportation intent.

High-confidence articles have bespoke source rewrites. This pass covers the
remaining rendered legacy posts whose titles do not mention transportation,
preserving their URLs while adding topic-specific limo context and conversion
links. Run after blog generators and before seo_normalize.py.
"""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent.parent
TRANSPORT = re.compile(r"\b(limo|limousine|car service|chauffeur|transportation|party bus|airport transfer)\b", re.I)
MARKER = 'data-phl-transport-intent="true"'


def text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value))).strip()


def clip(value: str, limit: int) -> str:
    value = re.sub(r"\s+", " ", value).strip(" -|:—")
    if len(value) <= limit:
        return value
    return value[:limit + 1].rsplit(" ", 1)[0].strip(" -|:—")


def service_link(topic: str) -> tuple[str, str]:
    lower = topic.lower()
    if "austin" in lower or "round rock" in lower:
        return "/limo-service-austin-tx/", "Austin limo service"
    if "houston" in lower:
        return "/limo-service-houston-tx/", "Houston limo service"
    return "/limo-service-dallas-tx/", "Dallas limo service"


def transform(path: Path) -> bool:
    source = path.read_text(encoding="utf-8")
    title_match = re.search(r"<title\b[^>]*>(.*?)</title>", source, re.I | re.S)
    h1_match = re.search(r"<h1\b[^>]*>(.*?)</h1>", source, re.I | re.S)
    if not title_match or not h1_match:
        return False
    old_title = text(title_match.group(1))
    topic = text(h1_match.group(1)) or path.stem.replace("-", " ").title()
    if TRANSPORT.search(old_title) or MARKER in source:
        return False

    short_topic = clip(topic, 35)
    new_title = clip(short_topic + " Limo Guide", 39) + " | Purple Heart Limo"
    link, label = service_link(topic)
    section = (
        f'<section {MARKER} class="phl-transport-intent">'
        f'<h2>{html.escape(short_topic)} Transportation Planning</h2>'
        f'<p>Visiting {html.escape(short_topic)}? Purple Heart Limo provides prearranged '
        f'chauffeured transportation for airport arrivals, dinners, events, and groups. '
        f'Choose a sedan, luxury SUV, stretch limousine, Sprinter, or party bus based on '
        f'passenger and luggage needs, with a confirmed pickup plan instead of parking or '
        f'rideshare uncertainty.</p>'
        f'<p>Review our <a href="{link}">{label}</a>, compare the '
        f'<a href="/fleet.html">chauffeured fleet</a>, or '
        f'<a href="/booking.html">request a quote online</a>. For timing and vehicle help, '
        f'call <a href="tel:+18337400700">(833) 740-0700</a> 24/7.</p></section>'
    )
    source = source[:title_match.start()] + f"<title>{html.escape(new_title)}</title>" + source[title_match.end():]

    article = re.search(r"<article\b[^>]*>", source, re.I)
    if article:
        source = source[:article.end()] + "\n" + section + source[article.end():]
    else:
        main = re.search(r"<main\b[^>]*>", source, re.I)
        if not main:
            raise ValueError(f"{path}: no article or main element")
        source = source[:main.end()] + "\n" + section + source[main.end():]

    path.write_text(source, encoding="utf-8")
    if len(new_title) > 60:
        raise ValueError(f"{path}: title too long ({len(new_title)})")
    return True


def main() -> None:
    changed = []
    for path in sorted((ROOT / "blog").rglob("*.html")):
        if path == ROOT / "blog" / "index.html":
            continue
        if transform(path):
            changed.append(path.relative_to(ROOT).as_posix())
    print(f"reframed {len(changed)} blog posts around limo transportation intent")
    for path in changed:
        print(" ", path)


if __name__ == "__main__":
    main()
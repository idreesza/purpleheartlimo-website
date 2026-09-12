#!/usr/bin/env python3
"""Inline the homepage's small local stylesheets without changing their order."""
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
STYLESHEETS = ("/css/global.css", "/css/sitewide-leads.css")


def _attribute(tag, name):
    match = re.search(
        r"\b" + re.escape(name) + r"\s*=\s*(['\"])(.*?)\1",
        tag,
        re.I | re.S,
    )
    return match.group(2) if match else ""


def _style_tag(url):
    css_path = ROOT / url.lstrip("/")
    css = css_path.read_text(encoding="utf-8")
    if not css:
        raise ValueError(f"{css_path}: stylesheet is empty")
    # Keep the source CSS readable and untouched; only add the style wrapper.
    return f'<style data-inline-source="{url}">\n{css}\n</style>'


def inline_styles(source, path):
    """Replace homepage stylesheet links with fresh source-CSS style blocks."""
    if Path(path).resolve() != ROOT / "index.html":
        return source

    for url in STYLESHEETS:
        style = _style_tag(url)
        marker_count = [0]

        def replace_marker(match):
            if _attribute(match.group(0), "data-inline-source") == url:
                marker_count[0] += 1
                return style
            return match.group(0)

        source = re.sub(
            r"<style\b[^>]*>.*?</style\s*>",
            replace_marker,
            source,
            flags=re.I | re.S,
        )
        if marker_count[0]:
            if marker_count[0] != 1:
                raise ValueError(f"{path}: duplicate inline stylesheet marker {url}")
            continue

        link_count = [0]

        def replace_link(match):
            tag = match.group(0)
            rel = _attribute(tag, "rel").casefold().split()
            if _attribute(tag, "href") == url and "stylesheet" in rel:
                link_count[0] += 1
                return style
            return tag

        source = re.sub(r"<link\b[^>]*>", replace_link, source, flags=re.I | re.S)
        if link_count[0] != 1:
            raise ValueError(f"{path}: expected one homepage stylesheet link for {url}")

    return source
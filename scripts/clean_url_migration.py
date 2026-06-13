#!/usr/bin/env python3
"""One-off: migrate blog /blog/<slug>.html -> /blog/<slug> (clean URLs).

- Rewrites canonical, og:url, JSON-LD url, and all internal links across served
  *.html + sitemap.xml.
- Adds forced 301 redirects /blog/<slug>.html -> /blog/<slug> in netlify.toml.
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"attached_assets", "scripts", "node_modules", ".git", ".local", ".agents"}
PATTERN = re.compile(r"/blog/([a-z0-9-]+)\.html")


def served_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if fn.endswith(".html") or fn == "sitemap.xml":
                yield os.path.join(dirpath, fn)


def rewrite_files():
    total_files = 0
    total_repl = 0
    for path in served_files():
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        new_content, n = PATTERN.subn(r"/blog/\1", content)
        if n:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            total_files += 1
            total_repl += n
    print(f"Rewrote {total_repl} occurrences across {total_files} files.")


def add_redirects():
    toml_path = os.path.join(ROOT, "netlify.toml")
    with open(toml_path, "r", encoding="utf-8") as f:
        toml = f.read()

    slugs = sorted(
        os.path.basename(p)[:-5]
        for p in glob.glob(os.path.join(ROOT, "blog", "*.html"))
        if os.path.basename(p) != "index.html"
    )

    lines = [
        "# ─────────────────────────────────────────────────────────────",
        "# 3a-bis. Legacy blog .html -> clean extensionless URL (301).",
        "# force=true because the .html file still exists on disk; without",
        "# force, static files win and the redirect is skipped. Must stay",
        "# ABOVE the /blog/:slug trailing-slash rule (first match wins).",
        "# ─────────────────────────────────────────────────────────────",
    ]
    for slug in slugs:
        lines.append("[[redirects]]")
        lines.append(f'  from = "/blog/{slug}.html"')
        lines.append(f'  to = "/blog/{slug}"')
        lines.append("  status = 301")
        lines.append("  force = true")
    block = "\n".join(lines) + "\n\n"

    anchor = "# ─────────────────────────────────────────────────────────────\n# 3b. Canonicalize blog URLs to a trailing slash."
    assert anchor in toml, "anchor not found in netlify.toml"
    assert "3a-bis" not in toml, "redirects already added"
    toml = toml.replace(anchor, block + anchor, 1)

    with open(toml_path, "w", encoding="utf-8") as f:
        f.write(toml)
    print(f"Added {len(slugs)} forced .html->clean redirects to netlify.toml.")


if __name__ == "__main__":
    rewrite_files()
    add_redirects()

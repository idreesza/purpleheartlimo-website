#!/usr/bin/env python3
"""Generate vercel.json from the same sources of truth server.py uses:

* netlify.toml legacy redirects (301) and retired URLs (410),
* each page's own <link rel="canonical"> (duplicate URL forms -> one 301),
* the dynamic endpoints implemented in server.py (served by api/index.py).

    python3 scripts/gen_vercel.py          # write vercel.json
    python3 scripts/gen_vercel.py --check  # exit 1 if vercel.json is stale
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import server  # noqa: E402
from build_vercel import is_public  # noqa: E402

FUNCTION = "/api/index"
# Paths handled by server.py's Handler rather than static files.
DYNAMIC = [
    "/.netlify/functions/contact", "/api/contact",
    "/api/distance", "/api/positioning", "/api/hourly-hub",
    "/api/google-maps-browser-key", "/config.js",
]
SECURITY_HEADERS = [
    {"key": "X-Content-Type-Options", "value": "nosniff"},
    {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
    {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
    {"key": "Permissions-Policy",
     "value": "camera=(), microphone=(), payment=(), usb=(), geolocation=(self)"},
    {"key": "Content-Security-Policy-Report-Only",
     "value": "default-src 'self' https: data: blob: 'unsafe-inline' 'unsafe-eval'; "
              "frame-ancestors 'self'; object-src 'none'; base-uri 'self'"},
]


def to_function(path):
    return f"{FUNCTION}?__path={path}"


def final_destination(path):
    """Follow legacy aliases and canonical forms to the final URL (one hop)."""
    seen = set()
    while path not in seen:
        seen.add(path)
        hit = server._redirect_destination(path)
        if hit and hit[1] == 301:
            path = hit[0]
            continue
        canonical = server._canonical_redirect_target(str(ROOT), path)
        if canonical:
            path = canonical
            continue
        break
    return path


def html_pages():
    for page in sorted(ROOT.rglob("*.html")):
        rel = page.relative_to(ROOT).as_posix()
        if any(part.startswith(".") for part in rel.split("/")) or not is_public(rel):
            continue
        yield page, rel


def url_forms(rel):
    """Every URL that static serving or server.py maps to this file."""
    if rel == "index.html":
        return ["/index.html", "/"]
    if rel.endswith("/index.html"):
        d = "/" + rel[: -len("index.html")]
        return [d + "index.html", d.rstrip("/"), d]
    stem = "/" + rel[: -len(".html")]
    return ["/" + rel, stem, stem + "/"]


def build_config():
    redirects, rewrites, sources = [], [], set()

    def add_redirect(source, destination):
        if source in sources or source == destination:
            return
        sources.add(source)
        redirects.append({"source": source, "destination": destination, "statusCode": 301})

    # Retired URLs answer 410 Gone via server.py; old blog search/paging URLs
    # are cleaned up by server.py as well.
    for src, (_, status) in sorted(server.REDIRECTS_EXACT.items()):
        if status == 410:
            for form in sorted({src, src.rstrip("/") or "/", src.rstrip("/") + "/"}):
                if form not in sources:
                    sources.add(form)
                    rewrites.append({"source": form, "destination": to_function(form)})
    for source in ("/blog", "/blog/"):
        for key in ("q", "p"):
            rewrites.append({"source": source, "has": [{"type": "query", "key": key}],
                             "destination": to_function(source)})

    # Legacy slug redirects (server matches with and without trailing slash).
    for src, (_, status) in sorted(server.REDIRECTS_EXACT.items()):
        if status != 301:
            continue
        dest = final_destination(src)
        for form in (src, src.rstrip("/") + "/" if not src.endswith("/") else src.rstrip("/")):
            if form and form != dest:
                add_redirect(form, dest)
    for prefix, to, status in server.REDIRECT_PREFIXES:
        if status == 301:
            add_redirect(prefix + ":path*", final_destination(to))

    # Duplicate forms of each page -> its canonical URL; extensionless
    # canonicals are served from their .html file.
    for page, rel in html_pages():
        canonical = server._canonical_path(str(page.resolve()))
        if not canonical or server._page_file_for(str(ROOT), canonical) != str(page.resolve()):
            continue
        for form in url_forms(rel):
            if form != canonical and server._page_file_for(str(ROOT), form) == str(page.resolve()):
                add_redirect(form, canonical)
        if rel.endswith(".html") and not rel.endswith("index.html") \
                and canonical == "/" + rel[: -len(".html")]:
            rewrites.append({"source": canonical, "destination": "/" + rel})

    for path in DYNAMIC:
        rewrites.append({"source": path, "destination": to_function(path)})

    return {
        "$schema": "https://openapi.vercel.sh/vercel.json",
        "framework": None,
        "installCommand": "npm ci",
        "buildCommand": "python3 scripts/build_vercel.py",
        "outputDirectory": "dist",
        "cleanUrls": False,
        "functions": {
            "api/index.py": {
                "includeFiles": "{server.py,netlify.toml,404.html}",
                "maxDuration": 30,
            }
        },
        "headers": [
            {"source": "/(.*)", "headers": SECURITY_HEADERS},
            {"source": "/(.*)", "has": [{"type": "query", "key": "v"}],
             "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
        ],
        "redirects": redirects,
        "rewrites": rewrites,
    }


def main():
    text = json.dumps(build_config(), indent=2, ensure_ascii=False) + "\n"
    target = ROOT / "vercel.json"
    if "--check" in sys.argv:
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        if current != text:
            print("vercel.json is out of date: run python3 scripts/gen_vercel.py")
            raise SystemExit(1)
        print("vercel.json up to date")
        return
    target.write_text(text, encoding="utf-8", newline="\n")
    cfg = json.loads(text)
    print(f"vercel.json: {len(cfg['redirects'])} redirects, {len(cfg['rewrites'])} rewrites")


if __name__ == "__main__":
    main()

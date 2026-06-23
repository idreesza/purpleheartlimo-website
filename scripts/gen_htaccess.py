#!/usr/bin/env python3
"""
Generate an Apache .htaccess (for Hostinger / cPanel shared hosting) from the
Netlify configuration in netlify.toml.

Netlify does not run on Hostinger, so its netlify.toml is ignored there. This
script ports every [[redirects]] rule and the [[headers]] blocks into the
equivalent Apache rewrite/header directives, plus the clean-URL behaviour
Netlify provides automatically (pretty URLs: /foo serves foo.html, /foo.html
redirects to /foo).

Run:  python3 scripts/gen_htaccess.py
Output: ./.htaccess
"""
import re
import sys

SRC = "netlify.toml"
OUT = ".htaccess"
APEX = "purpleheartlimo.com"


def parse_blocks(text):
    """Return (redirects, headers) parsed from a netlify.toml subset."""
    redirects, headers = [], []
    cur = None
    mode = None          # 'redirect' | 'header'
    in_values = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line == "[[redirects]]":
            if cur is not None and mode == "redirect":
                redirects.append(cur)
            elif cur is not None and mode == "header":
                headers.append(cur)
            cur, mode, in_values = {}, "redirect", False
            continue
        if line == "[[headers]]":
            if cur is not None and mode == "redirect":
                redirects.append(cur)
            elif cur is not None and mode == "header":
                headers.append(cur)
            cur, mode, in_values = {"values": {}}, "header", False
            continue
        if line.startswith("[") and line.endswith("]"):
            # other top-level tables ([build], [headers.values], etc.)
            if line == "[headers.values]":
                in_values = True
            else:
                # flush any open block we were building
                if cur is not None and mode == "redirect":
                    redirects.append(cur)
                    cur, mode = None, None
                elif cur is not None and mode == "header":
                    headers.append(cur)
                    cur, mode = None, None
                in_values = False
            continue
        if cur is None:
            continue
        m = re.match(r'^([\w.-]+)\s*=\s*(.+)$', line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if mode == "redirect":
            if key == "query":
                cur["query"] = val  # keep raw inline table
            else:
                cur[key] = _scalar(val)
        elif mode == "header":
            if in_values:
                cur["values"][key] = _scalar(val)
            elif key == "for":
                cur["for"] = _scalar(val)
    if cur is not None and mode == "redirect":
        redirects.append(cur)
    elif cur is not None and mode == "header":
        headers.append(cur)
    return redirects, headers


def _scalar(val):
    val = val.strip()
    if val.startswith('"') and val.endswith('"'):
        return val[1:-1]
    if val in ("true", "false"):
        return val == "true"
    if re.fullmatch(r'-?\d+', val):
        return int(val)
    return val


def esc(path):
    """Escape a literal URL path for use inside a RewriteRule regex."""
    return re.sub(r'([.\-+?^${}()|\[\]\\])', r'\\\1', path)


def build_htaccess(redirects, headers):
    out = []
    warnings = []
    a = out.append

    a("# ==========================================================================")
    a("# .htaccess for purpleheartlimo.com on Hostinger / Apache shared hosting")
    a("# AUTO-GENERATED from netlify.toml by scripts/gen_htaccess.py — do not edit")
    a("# by hand; edit netlify.toml and re-run the script so both stay in sync.")
    a("# ==========================================================================")
    a("")
    a("Options -MultiViews -Indexes")
    a("DirectoryIndex index.html")
    a("")
    a("<IfModule mod_rewrite.c>")
    a("RewriteEngine On")
    a("RewriteBase /")
    a("")
    a("# --- 1. Canonical domain: force HTTPS + strip www -> https://%s ---" % APEX)
    a("RewriteCond %{HTTPS} off [OR]")
    a("RewriteCond %{HTTP_HOST} ^www\\. [NC]")
    a("RewriteRule ^(.*)$ https://%s/$1 [R=301,L]" % APEX)
    a("")
    a("# --- 2. Redirects ported from netlify.toml (order preserved) ---")

    seen = set()
    for r in redirects:
        frm = r.get("from", "")
        to = r.get("to", "")
        status = int(r.get("status", 301))
        force = bool(r.get("force", False))

        # Host-level rules are already covered by the canonical block above.
        if frm.startswith("http://") or frm.startswith("https://"):
            continue
        # Catch-all 404 -> handled by ErrorDocument below.
        if frm == "/*" and status == 404:
            continue
        # Netlify Functions cannot run on Hostinger shared hosting.
        if to.startswith("/.netlify/functions/"):
            warnings.append(
                "SKIPPED function proxy %s -> %s (Netlify Functions do not exist "
                "on Hostinger; the distance lookup needs a separate backend / PHP "
                "endpoint or a third-party API call)." % (frm, to))
            a("# NOTE: %s -> %s requires a serverless backend; not portable to Apache." % (frm, to))
            continue

        # Query-string gated rule (old paginated blog URLs).
        if "query" in r:
            keys = re.findall(r'(\w+)\s*=', r["query"])
            cond = "|".join(keys) if keys else "q|p"
            patt = esc(frm.lstrip("/"))
            a("RewriteCond %%{QUERY_STRING} (?:^|&)(?:%s)= [NC]" % cond)
            a("RewriteRule ^%s/?$ %s? [R=301,L]" % (patt, to))
            continue

        # Splat handling.
        if frm.endswith("/*"):
            base = esc(frm[:-2].lstrip("/"))
            patt = "^%s(?:/.*)?$" % base
            target = to.replace(":splat", "$1")
        elif re.search(r':\w+', frm):
            # Named path params (e.g. /blog/:slug -> /blog/:slug/). Translate
            # each :param to an Apache capture group and back-reference. Anchor
            # exactly (no optional trailing slash) and guard with file/dir
            # existence checks so we don't loop on the already-slashed target
            # or rewrite real files.
            n = [0]

            def _cap(_m):
                n[0] += 1
                return "([^/]+)"

            patt = "^%s$" % re.sub(r':\w+', _cap, esc(frm.lstrip("/")))
            target = to
            for i in range(1, n[0] + 1):
                target = re.sub(r':\w+', "$%d" % i, target, count=1)
            a("RewriteCond %{REQUEST_FILENAME} !-f")
            a("RewriteCond %{REQUEST_FILENAME} !-d")
            line = "RewriteRule %s %s [R=%d,L]" % (patt, target, status)
            if line not in seen:
                seen.add(line)
                a(line)
            continue
        else:
            norm = frm.rstrip("/").lstrip("/")
            patt = "^%s/?$" % esc(norm)
            target = to.replace(":splat", "$1")

        if status == 200:
            # Internal rewrite (rewrite, no redirect).
            line = "RewriteRule %s %s [L]" % (patt, target)
        elif status == 410:
            line = "RewriteRule %s - [G,L]" % patt
        else:
            line = "RewriteRule %s %s [R=%d,L]" % (patt, target, status)

        if line in seen:
            continue
        seen.add(line)
        a(line)

    a("")
    a("# --- 3. Pretty URLs: redirect *.html and /dir/index.html to clean URLs ---")
    a("RewriteCond %{THE_REQUEST} \\s/+(.+/)?index\\.html[\\s?] [NC]")
    a("RewriteRule ^ /%1 [R=301,L]")
    a("RewriteCond %{THE_REQUEST} \\s/+([^.\\s?]+)\\.html[\\s?] [NC]")
    a("RewriteRule ^ /%1 [R=301,L]")
    a("")
    a("# --- 4. Serve extensionless URLs from their .html file ---")
    a("RewriteCond %{REQUEST_FILENAME} !-d")
    a("RewriteCond %{REQUEST_FILENAME}\\.html -f")
    a("RewriteRule ^(.+?)/?$ /$1.html [L]")
    a("</IfModule>")
    a("")
    a("# --- 5. Custom error page (Netlify catch-all /* -> /404.html) ---")
    a("ErrorDocument 404 /404.html")
    a("")

    # Headers
    a("# --- 6. Security & content headers (ported from netlify [[headers]]) ---")
    a("<IfModule mod_headers.c>")
    for h in headers:
        scope = h.get("for", "/*")
        vals = h.get("values", {})
        if scope == "/*":
            for k, v in vals.items():
                a('Header set %s "%s"' % (k, v))
    a("")
    a("# Aggressive caching for static assets (Netlify /css/*, /js/*, /images/*)")
    a('<FilesMatch "\\.(css|js|png|jpe?g|gif|webp|svg|ico|woff2?|ttf|eot)$">')
    a('  Header set Cache-Control "public, max-age=31536000, immutable"')
    a("</FilesMatch>")
    a("</IfModule>")
    a("")
    a("# Content-type + caching for AI/discovery text files")
    a("<IfModule mod_headers.c>")
    a('<FilesMatch "\\.(txt)$">')
    a('  Header set Cache-Control "public, max-age=86400"')
    a("</FilesMatch>")
    a("</IfModule>")
    a('<IfModule mod_mime.c>')
    a('  AddType text/plain .txt')
    a("</IfModule>")
    a("")

    return "\n".join(out) + "\n", warnings


def main():
    with open(SRC, encoding="utf-8") as f:
        text = f.read()
    redirects, headers = parse_blocks(text)
    content, warnings = build_htaccess(redirects, headers)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(content)
    print("Wrote %s (%d redirect rules parsed, %d header blocks)." %
          (OUT, len(redirects), len(headers)))
    for w in warnings:
        print("  WARNING:", w)


if __name__ == "__main__":
    sys.exit(main())

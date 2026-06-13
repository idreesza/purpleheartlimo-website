---
name: Netlify clean-URL blog redirects
description: Why .html->extensionless redirects need force=true, and what NOT to "clean up".
---

# Blog clean-URL canonical migration (Netlify)

Blog posts exist as two distinct sets: flat `blog/<slug>.html` files and folder posts
`blog/<slug>/index.html`. They are DIFFERENT articles, not twins. Flat posts serve at
extensionless `/blog/<slug>` (no trailing slash); folder posts serve at `/blog/<slug>/`
(trailing slash, via the non-forced `/blog/:slug -> /blog/:slug/` rule).

**Rule:** to make a legacy `/blog/<slug>.html` URL 301 to its extensionless clean URL,
the redirect MUST use `force = true`.
**Why:** on Netlify, static files take precedence over NON-forced redirects. The `.html`
file still exists on disk, so a non-forced redirect is silently skipped and the file is
served 200 (no redirect). Only `force = true` overrides that.
**How to apply:** keep these forced `.html` rules ABOVE the `/blog/:slug` trailing-slash
rule (first match wins). No loop: `/blog/foo.html` -> `/blog/foo`, and `/blog/foo` serves
`blog/foo.html` via static resolution (the non-forced rule is skipped because the file exists).

**Canonical/internal-link consistency:** canonical, og:url, JSON-LD url, sitemap.xml, and
all internal `/blog/<slug>.html` links must be extensionless to avoid redirect hops. One
regex `/blog/([a-z0-9-]+)\.html` -> `/blog/\1` over served *.html + sitemap.xml does it.

**Do NOT "clean up" `.html` in `scripts/data/*.json`** — those are the blog generator's
source inputs (the `path`/`url` of the source file) and must keep `.html`. Same for
`attached_assets/` (audit CSVs + prompt files): not served, leave alone.

**Dev parity:** `server.py` (SimpleHTTPRequestHandler) does NOT resolve extensionless URLs
by default; it was patched to serve `/blog/foo` from `blog/foo.html` so the Replit preview
matches Netlify prod.

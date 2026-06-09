---
name: Netlify redirect architecture & live-page caveats
description: How redirects/headers are managed on this site and which "legacy-looking" pages are actually live and must not be redirected.
---

# Redirects & headers live in netlify.toml, not _redirects

The site deploys with `publish = "."` (root files, NO `/public/` dir). ALL redirects and
headers are managed in the root `netlify.toml [[redirects]]` / `[[headers]]`.

**Why:** there is no `_redirects` file, and netlify.toml ends with a catch-all
`/* -> /404.html 404`. Netlify processes netlify.toml rules before `_redirects`, so any
rule placed in a new `_redirects` file would be shadowed by that catch-all and never fire.

**How to apply:** add new redirect/header rules to `netlify.toml`, never a `_redirects` file.
First-match-wins — keep specific rules above broader globs, and the `/*` 404 catch-all MUST stay
last. For a URL that must return Gone, add a `status = 410` block (with `to = "/404.html"`)
BEFORE any broader glob that would otherwise 301 it (e.g. `/html/head/title` before `/html/*`).

# rates.html and service-areas.html: live pages the OWNER chose to retire

`/rates.html` (Pricing) and `/service-areas.html` (full A–Z city list) were substantial,
self-canonical, sitemap'd, heavily-linked pages (~49 and ~14 inbound links) — NOT legacy.
The owner was warned of the SEO cost and explicitly chose to redirect them anyway:
`/rates.html → /fleet.html` and `/service-areas.html → /locations/` (301, `force = true`
required because the files still exist), and they were removed from sitemap.xml.

**Why:** owner intent overrode the SEO caveat. The files still physically exist, so the
redirects MUST keep `force = true` or Netlify will serve the stale files instead.

**How to apply:** keep these as forced 301s. ~63 internal links still point at the old URLs
(1-hop 301s) — only rewrite them to the final targets if the owner asks. If the owner ever
reverses this, drop the two redirect blocks and restore the sitemap entries.

# Blog consolidation winners

Dead/duplicate blog slugs are consolidated via 301 to three canonical "winner" posts (trailing slash):
`/blog/5-myths-about-limousine-services-in-austin-debunked/`,
`/blog/the-ultimate-guide-to-booking-a-limo-service-in-austin/`,
`/blog/5-tips-for-booking-a-limo-in-austin-for-your-special-event/`.
Folder-based posts only serve at the trailing-slash URL, so always point redirects to the slash form.
Do not redirect a LIVE post file (e.g. `top-5-reasons-to-hire-a-limo-for-your-austin-event`) to a winner without explicit confirmation.

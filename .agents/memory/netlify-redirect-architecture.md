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

# rates.html and service-areas.html are LIVE, not legacy

Despite SEO prompts that assume `/rates.html` and `/service-areas.html` are old pages to redirect
(to `/fleet.html` and `/locations/`), both are substantial, self-canonical, in sitemap.xml, and
heavily internally linked (~49 and ~14 inbound links). `rates.html` = Pricing page (distinct from
fleet/vehicles); `service-areas.html` = full A–Z city list (complementary to the `/locations/`
metro overview, which even links to it as "the full list").

**Why:** redirecting them would delete indexed content and turn dozens of internal links into 301 hops — a net SEO loss.

**How to apply:** do NOT redirect these two; treat them as canonical destinations.

# Blog consolidation winners

Dead/duplicate blog slugs are consolidated via 301 to three canonical "winner" posts (trailing slash):
`/blog/5-myths-about-limousine-services-in-austin-debunked/`,
`/blog/the-ultimate-guide-to-booking-a-limo-service-in-austin/`,
`/blog/5-tips-for-booking-a-limo-in-austin-for-your-special-event/`.
Folder-based posts only serve at the trailing-slash URL, so always point redirects to the slash form.
Do not redirect a LIVE post file (e.g. `top-5-reasons-to-hire-a-limo-for-your-austin-event`) to a winner without explicit confirmation.

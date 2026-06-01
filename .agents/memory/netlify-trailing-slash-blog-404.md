---
name: Netlify blog trailing-slash 404s (GSC)
description: Why /blog/<slug> (no trailing slash) 404s on this static Netlify site and how it ties to GSC "Not found" + "Alternate page with proper canonical tag"
---

# Netlify directory-post trailing-slash 404s

Blog posts live at `blog/<slug>/index.html` and **only serve at the trailing-slash URL** `/blog/<slug>/`. A request to `/blog/<slug>` (no slash) has no exact static file, so it falls through to the catch-all `/* -> /404.html (404)` and returns 404. Legacy posts that exist as `blog/<slug>.html` are fine — they serve directly.

**Why:** Netlify evaluates redirects first-match top-to-bottom; static files take precedence over *non-forced* redirects, but only at the *exact* path. `/blog/<slug>/index.html` maps to URL `/blog/<slug>/`, not `/blog/<slug>`, so the no-slash form isn't a static hit and the catch-all wins.

**How to apply:** A general rule near the end (after all specific dead-post `/blog/<x> -> /blog/` rules, before the catch-all) canonicalizes them:
`from="/blog/:slug" to="/blog/:slug/" status=301` (plus `/blog -> /blog/`). This also collapses the no-slash duplicates GSC reports as "Alternate page with proper canonical tag" (blog post self-canonicals already use trailing slash). Keep it non-forced so legacy `/blog/*.html` keep serving. Catch-all 404 must stay last.

GSC "Alternate page with proper canonical tag" is an *excluded/informational* status, not an error — for self-canonical pages it usually needs no action beyond ensuring one consistent URL form (apex, https, trailing slash).

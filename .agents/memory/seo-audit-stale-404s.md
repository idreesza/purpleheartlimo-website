---
name: Stale SEO audit 404s
description: Why SEMrush/GSC "404" findings on purpleheartlimo.com are often phantom, and how to triage them.
---

# Stale SEO audit 404s

When a SEMrush or GSC audit reports a blog/page URL as 404, do NOT assume the page is missing.

**Why:** The live domain only recently cut over to Netlify. Audits dated after the cutover frequently
reflect a crawl of the OLD broken host (stale/self-signed, served wrong content), so the "404" is an
artifact, not reality. Multiple reported-404 pages already existed on disk with full content.

**How to apply:**
1. First check the repo: `ls blog/<slug>*` and folder posts `blog/<slug>/index.html`.
2. If the file exists, the issue is almost always a **slug mismatch** — the audit's URL differs from the
   real canonical slug. Fix with a `status = 301` in netlify.toml pointing the audit slug → real URL.
3. Place specific blog redirects BEFORE the `/blog/:slug` trailing-slash catch-all and the final
   `/* → /404.html` (first match wins).
4. Only create a new page if the file genuinely does not exist.

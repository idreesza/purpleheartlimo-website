---
name: robots meta dedupe
description: How robots meta tags are set across the static HTML pages; pitfall of duplicate tags
---
Every indexable page already has ONE full robots directive:
`<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">`
(some pages self-close with `/>`). `thank-you.html` is intentionally `noindex, nofollow` — leave it.

**Pitfall:** a prior pass left a redundant second `<meta content="index, follow" name="robots"/>` (content-before-name ordering) in ~12 files, creating duplicate/conflicting robots tags. When asked to "add max-image-preview", do NOT add a new tag — the directive is already present; instead grep for files with >1 `name="robots"` and remove the stale one.

**Why:** Google honors the most restrictive of conflicting robots metas, and SEO audits flag duplicates. Adding image-preview directives to a noindex page is pointless.

**How to apply:** `rg -c 'name="robots"'` per file to find duplicates; the keeper is the long directive with max-image-preview.

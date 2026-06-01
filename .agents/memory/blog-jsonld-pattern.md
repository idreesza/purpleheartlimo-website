---
name: Blog BlogPosting JSON-LD required fields
description: The canonical JSON-LD shape every blog/*/index.html post must use, and what SEMrush flags when fields are missing
---

# Blog post BlogPosting JSON-LD pattern

Every `blog/<slug>/index.html` has exactly ONE `application/ld+json` block of @type `BlogPosting`. SEMrush "Structured data that contains markup errors" fires when a post omits `image` or `author` (publisher.logo also expected).

**Canonical shape** (match the posts that already pass): headline, description, `image` (post's own og:image meta, else `https://purpleheartlimo.com/images/og-image.jpg`), datePublished, dateModified, `author` = `{@type:Organization, name:"Purple Heart Limo", url:...}`, `publisher` = `{@type:Organization, name, logo:{@type:ImageObject, url:"https://purpleheartlimo.com/logo.webp"}}`, mainEntityOfPage, articleSection, url.

**Why:** Google Article/BlogPosting eligibility wants image + publisher.logo; SEMrush errors on missing image/author. ~30 of 45 posts shipped without them.

**How to apply:** When adding/auditing posts, ensure these fields exist. Most posts lack a per-post `og:image` tag, so they fall back to the site default image — adding per-post og:image would strengthen specificity but the fallback validates fine.

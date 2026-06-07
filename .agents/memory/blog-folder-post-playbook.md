---
name: Blog folder-post playbook
description: How to add a new SEO blog post on purpleheartlimo.com so it's indexed, linked, and Google-compliant.
---

# New blog post playbook (folder format)

Canonical post format is `blog/<slug>/index.html` (rich: full head/meta/OG/JSON-LD/nav/footer).
Flat `blog/*.html` posts are the older format. Copy an existing folder post as the template.

## Inbound links are MANUAL for folder posts
`scripts/add_related_links.py` only globs flat `blog/*.html` files — it does NOT touch folder
posts. So a new folder post will have no inbound links unless you add them by hand:
- Add a post card in `blog/index.html` (under the right city section — keep DFW vs Austin
  taxonomy correct; don't drop DFW posts under "Austin Metroplex").
- Add the URL to `sitemap.xml`.
- Cross-link from the new post's "Keep Reading" + ideally one or two existing posts.

**Why:** Semrush flags "only one internal link" = too few INBOUND links; folder posts silently
miss the auto-related-links pass.

## FAQPage schema must have matching VISIBLE FAQ
If a post injects `FAQPage` JSON-LD, the page MUST render a visible FAQ section whose
question/answer text matches the JSON-LD. Otherwise Google's structured-data content-match
guidance is violated and rich results can be suppressed.

**How to apply:** when adding FAQPage JSON-LD, also add `<h3>question</h3><p>answer</p>` blocks
with identical wording.

## Internal-link target set ("the main 10 pages")
User calls internal links "backlinks." Link contextually (descriptive anchors, no stuffing) to:
`/`, `/booking.html`, `/fleet.html`, `/limo-service-dallas-tx/`, `/dfw-airport-car-service/`,
`/dallas-party-bus/`, `/car-service-dallas-love-field/`, `/dallas-corporate-car-service/`,
`/dallas-wedding-transportation/`, `/contact.html`.

## Content strategy
One comprehensive post per Semrush topic (title-idea angles become H2 sections), not many thin
posts — helpful-content/Google-compliant. Images: use Unsplash w/ descriptive alt like the
template; never reference `attached_assets/` paths in src/URLs (not web-served).

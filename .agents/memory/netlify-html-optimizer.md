---
name: Netlify HTML optimizer rewrites markup
description: Live HTML differs from source — quotes and .html extensions get rewritten, breaking naive greps
---
Netlify's asset optimization rewrites served HTML: attribute quotes may flip to single quotes and internal `href="/page.html"` links become `href='/page'` (Pretty URLs).

**Why:** Verifying a deploy with `grep 'href="/booking.html"'` against live HTML returned 0 matches even though the link was present — the live markup was `href='/booking'`.

**How to apply:** When verifying live pages with curl+grep, use quote-agnostic, extension-agnostic patterns (e.g. `grep -o "href=.[^\"']*booking"`) or match on visible text/canonical URLs instead of exact source markup.

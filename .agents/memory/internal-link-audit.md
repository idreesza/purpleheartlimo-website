---
name: Semrush "only one internal link" fix
description: What the issue means on this site and how it was resolved for blog posts
---

Semrush "Pages with only one internal link" counts **inbound** internal links (how many site pages link TO the page), not outbound links in the page body.

**Why:** The flat `/blog/*.html` DFW posts each had only the blog index linking to them (1 inbound), so all 69 were flagged. They already had plenty of outbound nav/footer links — that was never the problem. The dir-based Austin posts (`/blog/<slug>/index.html`) were NOT flagged because they already carry a "Keep Reading" related-posts block cross-linking siblings.

**How to apply:** Inbound-link gaps on blog posts are fixed by `scripts/add_related_links.py` — it injects one `<section class="related-posts">` ("Keep Reading", 6 sibling links) before `<footer` in each flat `blog/*.html`. It is idempotent (strips any existing block, then reinserts) and handles both `<footer class="foot">` and `<footer class="ft">` variants. Re-run it after adding new flat posts. Do NOT add an inline arrow to the `<li>` — the flat-post template already has a global `li::before { content:"→" }`; adding one causes a double arrow.

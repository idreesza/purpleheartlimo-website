# Retired article redirect audit

## Scope and evidence

The two supplied October Search Console text lists (`attached_assets/Pasted-Examples-https-search-google-com-URL-Last-crawled-http-_1792344424152.txt` and `attached_assets/Pasted-Examples-https-search-google-com-URL-Last-crawled-https_1792344561016.txt`) contain nine distinct article paths currently mapped to `/blog/`. Blog pagination and the blog index itself are not articles and are excluded.

Checked the current blog files, available Git history (900 commits), generated article data, the exported website ZIP, and the supplied SEO-fixes ZIP. Seven paths have no article file/history at their exact slug and no original article in either ZIP. This is not proof that an offsite backup does not exist; no external archive recovery has been verified.

## Findings and proposed decisions

All paths below are relative to `/blog/`. **Owner approved “Restore two; retire seven.”** The proposed actions below have been implemented, preserving the original article files without replacement writing.

| Path | Recovery / equivalent assessment | Proposed action |
| --- | --- | --- |
| `prom-night-perfection--tips-for-booking-a-limo-in-austin` | Full original article remains in its `index.html`, Git history, and exported website. Covers booking lead time, vehicle choices, safety and prom-night routing in Austin. The forced homepage redirect hides it. | Restore the existing article at its trailing-slash URL; no replacement writing needed. |
| `prom-season-limo-booking-tips-for-austin-teens-and-parents` | Full original article remains in its `index.html`, Git history, and exported website. Covers parent checks, group planning, vehicles and timing in Austin. The forced homepage redirect hides it. | Restore the existing article at its trailing-slash URL; no replacement writing needed. |
| `a-comprehensive-guide-to-transportation-services-in-austin--texas` | No original recovered. The existing Austin limo-booking guide explains booking a limo, not the broader transportation-services subject. | Retire with 410 unless an original backup is supplied. |
| `case-study--success-stories-from-austin-s-prom-season-limo-bookings` | No original recovered. Prom planning guides are not evidence of actual customer case studies. | Retire with 410; do not fabricate customer stories. |
| `exploring-advanced-limousine-booking-systems--a-look-at-purple-heart-limo-s-technology` | No original recovered. Booking instructions and dynamic-map guides do not establish the former technology article's content or claims. | Retire with 410 rather than redirect to generic booking advice. |
| `how-purple-heart-limousine-uses-ai-for-seamless-booking-experiences` | No original recovered or verified article supporting this specific AI-use topic. | Retire with 410; do not invent AI capabilities. |
| `the-future-of-transportation-booking-systems--how-innovations-are-changing-the-game` | No original recovered. A present-day limo-booking checklist is not a future-technology article. | Retire with 410. |
| `why-austin-locals-love-purple-heart-limousine-services` | No original recovered. The company-comparison article discusses pricing, vehicles and standards, not verified local customer experiences. | Retire with 410 rather than assume equivalence from brand/location overlap. |
| `why-purple-heart-limousine-stands-out-among-austin-s-limo-services` | No original recovered. The company-comparison article is a possible topical candidate, but the original is unavailable to verify equivalent content. | Retire with 410 unless original content establishes equivalence. |

## Approval consequences and implementation checks

Restoration would expose the two existing prom articles unchanged; it does not independently verify their historical fleet, availability or safety claims. Content improvement remains separate from this routing audit.

A 410 explicitly tells crawlers the seven other URLs are permanently gone, rather than sending visitors to an unrelated blog index. It does not delete any files. Owners with original copies may prefer recovery before retirement.

Implementation checks:

- Update only these nine rules in `netlify.toml`; preserve unrelated mappings.
- Ensure restored folder URLs resolve to 200 without self-redirects and use matching canonicals, sitemap entries and inbound links.
- Ensure retired bare and trailing-slash paths return 410, including GET/HEAD and www handling.
- Regenerate `.htaccess` using `scripts/gen_htaccess.py`; do not hand-edit the generated file.
- Extend routing regression tests to cover the decisions and Apache parity; retain existing tests for unrelated routes.

The nine homepage redirects have been replaced by the approved restoration and retirement rules. No article files were deleted or rewritten.

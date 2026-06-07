# Blog post authoring spec — Purple Heart Limo

You are writing **one JSON file per blog post** into `scripts/data/<NN-slug>.json`.
A Python renderer (`scripts/blog_template.py`) wraps your JSON in the site's real
template (nav, hero, footer, schema, CTA). **You only write the data fields below.**

Reference gold standard (read it): `blog/limo-service-cost-dallas-tx/index.html`.
Match its depth, tone, and HTML conventions in `body_html`.

## JSON schema (all fields required)
```json
{
  "slug": "best-limo-service-dallas-tx",
  "path": "blog/best-limo-service-dallas-tx/index.html",
  "url": "https://purpleheartlimo.com/blog/best-limo-service-dallas-tx/",
  "title_tag": "Best Limo Service in Dallas TX — What to Look For | Purple Heart Limo",
  "meta_desc": "<=155 chars, compelling, includes keyword",
  "keywords": "primary, secondary1, secondary2, secondary3",
  "og_title": "short social title",
  "og_desc": "<=110 chars social description",
  "h1": "Main headline (NO emphasis part)",
  "h1_em": "italic gold tail of the headline",
  "breadcrumb_label": "Best Dallas Limo",
  "date_iso": "2026-06-03",
  "date_human": "June 3, 2026",
  "read_time": "8 min read",
  "hero_img": "https://images.unsplash.com/PHOTO?w=820&q=80&auto=format",
  "hero_alt": "descriptive alt with city + topic",
  "headline": "Full BlogPosting headline (can equal h1 + h1_em)",
  "jsonld_desc": "one-sentence description for schema",
  "body_html": "ARTICLE INNER HTML — see rules",
  "faqs": [{"q":"...","a":"..."},{"q":"...","a":"..."},{"q":"...","a":"..."}],
  "related": [{"url":"/blog/.../","title":"..."}, {"...":"..."}, {"...":"..."}],
  "cta_h3": "Short CTA heading",
  "cta_p": "One-line CTA paragraph",
  "card_section": "Dallas-Fort Worth Limo Guides",
  "card_tag": "DFW · Pricing Guide",
  "card_title": "Card title for the blog index (can be shorter than title_tag)",
  "card_url": "/blog/best-limo-service-dallas-tx/"
}
```

## body_html rules (THIS IS THE REAL WORK)
- Start with ONE intro `<p>` that gives the direct answer / hook.
- Then 5–7 `<h2>` sections, each with `<p>`, and `<ul>`/`<ol>` or a
  `<table class="fare-table">` where the brief calls for a table/chart.
- Include exactly ONE `<div class="callout"><p>...</p></div>` mid-article that
  references the 4.9★/214 reviews + 60-min free wait + a booking link.
- **Word count 1,400–2,200** (West Texas posts 1,400–1,700). Be genuinely useful,
  specific, and local — never filler.
- **Do NOT** include: the FAQ section, the "Keep Reading" block, the CTA box,
  nav, or footer. The renderer adds those. The renderer also adds the visible
  FAQ from your `faqs` list, so do not duplicate it.
- Internal links use `<a class="inline" href="...">`. You MUST link at least 4 of
  these real pages contextually (natural anchor text, no stuffing):
  `/`, `/booking.html`, `/fleet.html`, `/limo-service-dallas-tx/`,
  `/services.html`, `/contact.html`, `/flight-tracker.html`,
  `/testimonials.html`, `/about.html`, plus city pages
  `/limo-service-austin-tx/`, `/limo-service-houston-tx/` when relevant.
- Cross-link 1–2 sibling blog posts from this batch where natural.
- Tables: `<table class="fare-table"><thead><tr><th>..</th></tr></thead><tbody>..</tbody></table>`.
- `<strong>` for emphasis (renders purple). Use `<a class="inline">` for links.

## Brand facts (TRUE — use freely; do NOT invent others)
- Veteran-owned AND Texan-owned; military values: punctuality, reliability, honor.
- Flat-rate pricing, **zero surge** (contrast Uber/Lyft).
- **60-minute free wait** on airport pickups.
- **4.9 stars from 214+ riders.**
- Phone **(833) 740-0700**. Book online in 60 seconds.
- Fleet: Executive Sedan (Cadillac), Luxury Sedan (Mercedes S-Class), Executive
  SUV (Yukon), Luxury SUV (Escalade), Stretch Limo, Stretched SUV (Navigator),
  Executive Sprinter Van, Party Bus, Sprinter Jet.
- Service areas: Dallas-Fort Worth, Austin, Houston, plus West Texas routes to
  Abilene, Midland, Odessa. Bilingual English/Spanish service.
- Pricing reference (2026 flat hourly): Sedan $75–120, SUV $95–160, Stretch
  $130–180, Sprinter $150–200, Party Bus $200–300.

## Rules
- Real 2026 dates only (assigned per post). No backdating to 2025.
- NO `aggregateRating`/`LocalBusiness` schema (renderer handles BlogPosting+FAQ).
- Tone: warm, professional, confidence-inspiring. Not salesy or robotic. 100% unique.
- Quinceañera post (17): add a warm closing paragraph in Spanish inside body_html.
- Write valid JSON (escape quotes inside strings). Verify with `python3 -m json.tool`.

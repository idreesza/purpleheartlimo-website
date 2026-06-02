# Titanium Garage Door — Reusable SEO Prompt Pack

A collection of copy-paste prompts and templates for getting a local service
website indexed, crawled, and ranking at the top of Google search.

**Markets:** PRIMARY = Austin, TX · SECONDARY = Dallas, TX and Houston, TX
**Business:** Titanium Garage Door (garage door repair, installation, springs, openers, etc.)

> All limo-specific content has been stripped out. These are the general-purpose
> SEO build/audit prompts and templates — adapt the city/service lists as needed.

---

## PROMPT 1 — Master SEO build & indexing prompt (paste into Replit)

You are an SEO + web engineer working on the Titanium Garage Door website
(garage door repair, installation, spring/opener service, etc.). My goal is to
get every page indexed and crawled by Google and to rank at the top of search —
PRIMARY market: Austin, TX. SECONDARY: Dallas and Houston, TX.

Work through ALL of the following and fix every issue you find. Don't ask me to
confirm each step — do the work, then report what you changed.

**1. Technical crawl & index audit (fix everything):**
- Verify every page has a unique, descriptive `<title>` (under ~60 chars) and meta description (under ~155 chars) with the target keyword + city.
- Ensure exactly ONE `<meta name="robots">` tag per page set to `index, follow` — remove duplicates or conflicting directives.
- Add a self-referencing `<link rel="canonical">` to every page.
- Confirm there's a valid `robots.txt` that allows crawling and points to the sitemap.
- Generate/repair `sitemap.xml` with every real URL, valid XML, accurate lastmod dates, and make sure any URL count in a header comment matches the actual number of `<url>` entries.
- Make sure all internal links and image references resolve (no 404s, no broken image paths).
- Confirm the contact/booking/quote form actually submits — check that the front-end field names map correctly to whatever the backend expects before POSTing.

**2. Build dedicated service + city landing pages (the main ranking lever):**
- Create unique, ~1,200+ word pages for each core SERVICE × CITY combination. Services: garage door repair, broken spring repair/replacement, garage door opener repair & installation, new garage door installation, off-track/cable repair, and 24/7 emergency/same-day repair.
- PRIMARY city + neighborhoods: Austin, Round Rock, Cedar Park, Leander, Georgetown, Pflugerville, Lakeway, Kyle/Buda.
- SECONDARY cities: Dallas (+ Plano, Frisco, Arlington, Irving), Houston (+ Katy, Sugar Land, The Woodlands, Cypress, Pearland).
- Each page must have GENUINELY UNIQUE local content (neighborhood references, local landmarks, service-specific details) — NOT spun/duplicated boilerplate, or Google will treat them as thin doorway pages. Build a generator/template so design is consistent but write distinct copy per page.
- Every page needs: one H1, a clear quote/call CTA with the phone number, 4 unique FAQs, and an internal-link cluster to related service/city pages.

**3. Structured data (JSON-LD) on every page:**
- Add a single valid JSON-LD `@graph` per page containing: (1) a `Service` + `LocalBusiness` node with name, phone, areaServed (the cities), priceRange, and aggregateRating; (2) a `BreadcrumbList`; (3) a `FAQPage` matching the on-page FAQs. Validate that it parses cleanly.

**4. Hub pages + internal linking:**
- Build/strengthen an Austin hub page, a Dallas hub, and a Houston hub. Each hub links out to all its service and city pages with a visible link cluster. Add the new URLs to the sitemap.

**5. After building, validate everything:** confirm all JSON-LD parses, no broken internal links, sitemap is well-formed, no duplicate meta tags, and every page is crawlable. Report a summary of what you changed and a list of all new URLs.

**Important context:** the business's physical address determines where it can
rank in Google's local "map pack." It can rank in the map pack near its real
address; for cities where it has no physical location, the city landing pages
can still rank in normal (organic) results but likely NOT in the map pack. Keep
that distinction in mind and tell me which cities qualify for map-pack vs
organic-only.

---

## PROMPT 2 — SEO / crawl & index audit only (use on an existing site)

Audit the entire Titanium Garage Door website for crawlability, indexability,
and on-page SEO, then FIX every issue. Specifically check and repair:

1. Titles & meta descriptions — unique per page, correct length, keyword + city.
2. Robots directives — exactly one `meta name="robots"` set to `index, follow`; no duplicates or conflicts; a valid `robots.txt` that points to the sitemap.
3. Canonical tags — one self-referencing canonical per page.
4. Sitemap — well-formed XML, every live URL included, no dead/duplicate URLs, accurate counts.
5. Broken links & images — every internal href and image path must resolve.
6. Headings — exactly one H1 per page, logical H2/H3 structure.
7. Structured data — valid JSON-LD (LocalBusiness, Service, FAQPage, BreadcrumbList) that parses with no errors.
8. Forms — the quote/contact form must actually submit (verify field-name mapping front-end → backend).
9. Page speed basics — compressed images (WebP), no render-blocking junk.
10. Mobile friendliness — responsive viewport tag present and layout works on mobile.

Report a prioritized list of what was broken and what you fixed.

---

## PROMPT 3 — Landing-page generator (reusable build methodology)

Build a landing-page generator (a script + a data file) for Titanium Garage Door
so I can scale to many unique service + city pages without copy-pasting HTML.

- The generator should clone the site's existing design, header, footer, nav, and styling so new pages match the brand exactly.
- Keep per-page CONTENT in a separate data file: one entry per page with its slug, title, meta, H1, hero text, service cards, body sections, FAQs, and internal links.
- Each generated page must include: breadcrumb, valid JSON-LD `@graph` (Service/LocalBusiness + BreadcrumbList + FAQPage), a working quote form, and an internal-link cluster.
- Content must be unique per page (different local references and service details) to avoid thin/duplicate-content penalties.
- After generating, validate: JSON-LD parses, no broken links, images resolve, sitemap updated.

Then generate the first batch: garage door repair, spring replacement, opener
installation, and new door installation — for Austin plus Round Rock, Cedar Park,
and Georgetown.

---

## PROMPT 4 — Google Business Profile setup (local map-pack)

Help me set up and optimize a Google Business Profile (GBP) for Titanium Garage
Door so it ranks in the local map pack.

- Set it up at the real business address. If we serve customers at their homes rather than at a storefront, configure it as a SERVICE-AREA business and list the cities/zip codes we cover.
- Choose the best primary category (e.g., "Garage door supplier" or "Garage door repair service") plus relevant secondary categories.
- Write a compelling business description (no keyword stuffing) that mentions the core services and service area.
- Add all services with short descriptions, hours (including 24/7 emergency if applicable), service areas, and high-quality photos of completed jobs, trucks, and the team.
- Explain the difference: we can rank in the map pack near our verified address; cities far from it will mostly rank in organic results, not the map pack.

### GBP business description template (fill in the blanks)
> Titanium Garage Door provides fast, reliable garage door repair and
> installation across [PRIMARY CITY] and the surrounding area. From broken
> springs and noisy openers to brand-new doors, our experienced technicians
> deliver upfront pricing, quality parts, and same-day service. Locally owned
> and fully insured. Call [PHONE] for a free quote.

### GBP service descriptions (one per service — fill in)
- **Garage Door Repair** — [1–2 sentences on diagnosis, common fixes, same-day service]
- **Broken Spring Replacement** — [torsion/extension springs, safety, fast turnaround]
- **Opener Repair & Installation** — [brands serviced, smart openers, warranty]
- **New Garage Door Installation** — [styles/materials, free in-home estimate]
- **Off-Track & Cable Repair** — [emergency availability]
- **24/7 Emergency Service** — [response time, areas covered]

---

## PROMPT 5 — Review-request message (SMS + email templates)

Generate me a short, friendly review-request message I can send to customers
after a completed job, with a direct link to leave a Google review. Keep it under
2 sentences for SMS.

### SMS template
> Hi [NAME], thanks for choosing Titanium Garage Door! If we did a great job,
> would you mind leaving us a quick Google review? It really helps our small
> business: [GOOGLE REVIEW LINK]

### Email template
> Subject: How did we do?
>
> Hi [NAME],
>
> Thank you for trusting Titanium Garage Door with your garage door service. Your
> feedback means a lot to us and helps other local homeowners find a repair team
> they can rely on.
>
> If you have a moment, we'd be grateful for a quick Google review:
> [GOOGLE REVIEW LINK]
>
> Thanks again,
> The Titanium Garage Door Team · [PHONE]

> Tip: get your review link from your Google Business Profile → "Ask for reviews."
> A steady flow of fresh reviews is one of the strongest local-ranking signals.

---

## PROMPT 6 — Google Business Profile "Posts" (keep the profile active)

Write me a rotation of short Google Business Profile posts (each with a photo +
a "Call now" button) that I can publish 1–2 times per week to keep my profile
active. Cover: emergency repair, spring replacement, opener installation, new
door installation, seasonal tune-ups, and a "locally owned / trust" post.

### Ready-to-use examples
1. **Emergency repair** — 🚪 Garage door stuck, off-track, or won't open? We offer fast, same-day garage door repair across [CITY]. Upfront pricing, no surprises. Call now: [PHONE].
2. **Broken spring** — ⚠️ Loud bang and now the door won't lift? That's usually a broken spring — and it's a job for a pro. We replace springs same-day with quality parts. [PHONE].
3. **Opener installation** — 🔧 Upgrade to a quiet, smart garage door opener you can control from your phone. Professional installation with warranty. Book today: [PHONE].
4. **New door installation** — 🏡 Boost your curb appeal and security with a new garage door. Free in-home estimate, dozens of styles. Call [PHONE].
5. **Seasonal tune-up** — 🛠️ Keep your garage door running smoothly — book a maintenance tune-up before the busy season. Catch small problems before they become big ones. [PHONE].
6. **Locally owned / trust** — ✅ Locally owned, fully insured, and trusted by [CITY] homeowners. Honest pricing and quality workmanship on every job. That's the Titanium standard. [PHONE].

> Whenever you finish a memorable job, post a quick "recent work" update with a
> before/after photo — fresh, original posts signal an active business to Google.

---

## PROMPT 7 — Submit sitemap & request indexing (do this after the build)

1. In Google Search Console, add and verify the property for the site's domain.
2. Go to **Sitemaps**, enter `sitemap.xml`, and submit. This handles automatic discovery of all URLs over time.
3. Use **URL Inspection** on your highest-priority pages and click **Request Indexing** to push them to the front of the line (Search Console allows roughly 10/day).
4. Prioritize: the Austin hub, your easiest-win city pages, and your highest-value service pages (emergency repair, spring replacement, installation) first.
5. Repeat the next day for the remaining pages until all priority URLs are submitted.

---

## Quick reference — what actually moves local rankings

- **Unique, useful content per page** (no thin/duplicate doorway pages).
- **Clean technical SEO**: one title, one canonical, one robots tag, valid sitemap, no broken links.
- **Valid structured data** (LocalBusiness + Service + FAQ + Breadcrumb).
- **A complete, active Google Business Profile** with the right categories and service area.
- **A steady stream of genuine Google reviews.**
- **Local citations** (consistent Name/Address/Phone on Yelp, Angi, BBB, Nextdoor, etc.).
- **Internal linking** between hubs and service/city pages.
- **Patience**: indexing takes days to weeks; ranking gains build over weeks to months.

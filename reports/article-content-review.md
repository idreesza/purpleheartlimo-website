# Crawled but not indexed: article content review

Review date: October 31, 2026  
Site: Purple Heart Limo  
Input: `attached_assets/Pasted-Examples-https-search-google-com-URL-Last-crawled-https_1792344561016.txt`

## Decision summary

**Recommend targeted factual corrections first, followed by distinct trip-planning briefs—not a sitewide rewrite or longer articles for their own sake.**

The 40 supplied examples resolve to 20 unique article destinations, six non-article destinations and the blog index. Several examples are host, slash or legacy-slug variants, not separate content problems. All 20 article destinations were read. The most serious problems are unsupported operational promises, inconsistent prices and capacity, aging venue/event details, and articles serving nearly the same purpose.

This deliverable is a review and proposed editorial plan. **No public article, canonical URL, redirect, sitemap or discovery link has been changed.** Substantial rewrites should follow approval of these recommendations and confirmation of the unresolved facts below. Retired articles pointing at the blog index belong to the separate retirement task; do not revive or rewrite them here.

This is a repository review, not a fresh Search Console inspection or production crawl. The supplied last-crawled dates do not prove Google's current status or explain its indexing decisions. Content improvements can improve usefulness; they cannot guarantee indexing.

### Recommended order

1. **P0 — booking accuracy and traveler risk:** airport, Round Rock transfer, FAQ, wedding, Kalahari, SXSW and COTA articles. Resolve conflicting policies before publishing specific promises.
2. **P1 — distinct utility:** map/traffic cluster, night-out/weekend/top-five cluster, corporate and booking guides. Replace sales repetition with a concrete planning tool unique to each page.
3. **P2 — selective maintenance:** Near Southside and Plano/Frisco destination lists; preserve the stronger Universal family checklist and DFW source-verification sections.

P0 denotes potential traveler harm or financial misunderstanding, not an assertion that Google prioritizes these pages.

## Evidence and publication rules

### What the current business implementation supports

| Evidence | Supported statement | Boundary |
|---|---|---|
| `booking.html`, especially the estimate, review and submission messages | The website accepts a **quote/request**; a representative confirms price and reservation details. | A request acknowledgement is not guaranteed vehicle availability, payment, or a finalized reservation. Remove “confirmed within one hour” unless supported by an approved service commitment. |
| `js/pricing.js`, `PHL_CLASSES` and `phlComputeFare` | Four live-priced classes: Business Sedan, Luxury Sedan, Business SUV, Luxury SUV. The current configured limits are 3 passengers/2 bags for sedans and 6 passengers/5 bags for SUVs. | These are booking-system limits, not an independent inspection of actual luggage fit. Confirm large bags, strollers, mobility equipment and restraints. Do not advertise a four-passenger sedan contrary to the form. |
| Same pricing source | Base transfer rates cover the first 20 miles; excess miles and trips over 40 minutes affect the calculation. The latter use hourly pricing with a two-hour minimum. Positioning can also affect a quote. | A displayed starting rate is not a universal airport-to-anywhere fare. Route-specific articles need an approved quote or the current estimator, not hand-calculated permanent tables. |
| `js/pricing.js` and `js/price-sync.js` | Live class prices have a shared source and display bindings. | Use `data-phl-flat` for a base transfer rate, `data-phl-hourly` for hourly and `data-phl-from` only for “from” wording. Synchronize no-JS text and schema too. Do not hardcode derived package totals. |
| `booking.html` contact/support copy | Booking requests and route questions can use `/booking.html` or (833) 740-0700. | Do not substitute an invented phone number, promise response times, or imply that submission guarantees a car. |
| `cancellation-policy.html`, standard, wedding and major-event sections | Published cancellation terms differ by booking type. Weddings currently state a 25% non-refundable deposit and balance due seven days before the event. Major events have separate payment/refund terms. | Link the current policy rather than promise universally free changes. Publication evidence is not independent verification of actual operations; the business must resolve policy conflicts. |

### Claims that are not sufficiently verified

- **Airport wait:** `airport-transfer.html` advertises 60 minutes, while `rates.html` says 30 minutes. Several articles also specify that the clock starts at landing. Resolve duration, clock start, extra wait charges and cancellations with the business. Neither number belongs in a wedding-delay promise.
- **Gratuity:** the Austin FAQ says gratuity is included; `rates.html` says no mandatory gratuity and optional tips. Do not equate optional tipping with prepaid gratuity.
- **Airport meeting service:** the AUS article charges $25 for an inside meet-and-greet, while the Round Rock article includes it. Confirm airport-specific options, charges and authorized pickup locations.
- **Child restraints:** requests can be made in booking notes. That does not establish free seats, preinstallation, suitability, or availability. Confirm restraint type, responsibility and charges in writing.
- **Live routing and dispatch:** route-estimation code in `server.py` includes an OSRM fallback. A map estimator and flight-status feature do not establish continuous chauffeur tracking, automatic dispatch changes, live traffic at all times or guaranteed arrival. Driver operating procedures need business confirmation.
- **Fleet and amenities:** four live-priced classes do not establish availability of every specialty vehicle, exact model assignment, Wi-Fi, champagne, wraps, red carpets, or NDA arrangements. Quote specialty vehicles individually.
- **Reputation and experience:** “214+ verified reviews,” “hundreds of weddings,” “thousands of times,” named corporate customers, driver screening claims and anecdotal success stories require an attributable record or approval. Repetition across site pages is not verification.
- **Third-party facts:** venue opening/closure, current event calendar, airport curbs, VIP parking permissions, admission prices and promotions need current first-party evidence before publication. This review did not independently revalidate external websites. Suspect statements below are marked for verification, not replaced with guessed facts.

## Page-by-page recommendations

All paths below are the existing canonical destinations and must be preserved, including the DFW `.html` suffix and extensionless Near Southside/Plano paths. Folder paths correspond to `blog/<slug>/index.html`; the two extensionless destination guides correspond to `blog/<slug>.html`.

### 1. Austin night out — P1
Canonical: `/blog/how-to-plan-the-perfect-night-out-with-a-limo-in-austin/`

**Evidence:** Recommends Container Bar more than once, includes EP & LP and a claimed Nickel City relocation, and promises “no waiting” and an hourly rate that stays the same “no matter what time” the group goes home. These venue references need current address/operating checks; the rate wording obscures booked hours and overtime. Most of the article is subjective venue praise.

**Recommend:** Retain an evening-only purpose. Replace the bar directory with a dinner → show → return worksheet: reservation time, doors/show end, complete addresses, walking tolerance, legal meeting point, group contact and last booked departure. Explain reserved hourly time versus two separate transfers, overtime approval and a backup pickup location. Name venues only after checking their own pages.

**Distinct value:** A timed evening plan, not another general Austin sightseeing list. Use the proposed evening worksheet below.

### 2. Austin traffic — P1
Canonical: `/blog/navigating-austin-s-traffic--why-a-limo-service-is-your-best-choice/`

**Evidence:** Unsupported TomTom ranking, precise congestion windows, “our drivers…master it,” “every back street,” and an assertion that executive performance data are unambiguous without a citation. It overlaps both mapping articles.

**Recommend:** Keep this page about **when to leave**, not technology or promotional claims. Work backward from an appointment, venue entry requirement or airline arrival recommendation; add loading time, route estimate and a separate contingency allowance. Explain that a chauffeur does not remove congestion. Refer to current TxDOT/City of Austin notices when verified; do not prescribe fixed shortcuts.

**Distinct value:** A departure-time worksheet with adjustable inputs rather than a universal travel-time table.

### 3. Dallas wedding — P0
Canonical: `/blog/wedding-limo-rental-dallas-tx/`

**Evidence:** Says “60-minute free wait” protects delayed wedding photos; presents decorations as approved policy; labels a long booking lead time “non-negotiable”; lists The Bell Tower on 34th in a Dallas venue section without validating its location; uses an unverified review count.

**Recommend:** Remove the airport-wait implication. Separate reserved standby time, guest shuttle loops and a final getaway transfer. Replace rigid lead-time claims with availability confirmation once date and venues are known. Check every venue's actual address and decoration rules. Add the current wedding cancellation-policy link rather than imply all delays or changes are free.

**Distinct value:** A coordinator handoff sheet with passenger counts for each leg, loading time, photo stops, venue access contact and final return.

**Editing source:** `scripts/data/04-wedding-limo-rental-dallas-tx.json`, its rendered page, and any applicable `scripts/blog_addenda.py` text must stay consistent.

### 4. Near Southside Fort Worth — P2
Canonical: `/blog/near-southside-fort-worth`

**Evidence:** Short destination list includes Little Red Wasp as a “live music venue,” unverified venue status and neighborhood membership, and $95/hour/$199 trip prices without an approved quote basis. “Right at the door” is presented as assured.

**Recommend:** Verify listed places and replace the directory with a Magnolia versus South Main choice: destination address, dinner reservation, walking/accessibility needs and agreed return meeting point. Treat a Stockyards extension as a separate vehicle leg, not an implied walk. Replace unsupported rates with a quote request.

**Distinct value:** A two-area evening comparison and return-pickup checklist. More adjectives or a longer attraction list would not improve it.

### 5. AUS airport — P0
Canonical: `/blog/austin-bergstrom-airport-limo-service-guide/`

**Evidence:** Fixed curb directions, “no wait,” unsupported rideshare wait/surge figures, a $25 meet-and-greet, guaranteed availability with 24 hours' notice, and an all-metro flat-rate claim. Vehicle labels associate Escalade with the business tier and Navigator with luxury, unlike current booking classes. Sprinter $159 appears as both transfer and hourly pricing.

**Recommend:** Replace the broad price matrix with how to request an exact-route quote. Separate arrival from departure planning; distinguish flight landing, passenger-ready time and vehicle meeting time. Confirm the current airport-approved meeting instructions and fee/wait policies before stating them. Remove the instant-car guarantee and named corporate-client implications.

**Distinct value:** A passenger-ready checklist: operating flight/date, terminal when known, mobile contact, passengers/bags, exact destination and special equipment. Refer Round Rock-specific route planning to its own guide.

### 6. Kalahari family guide — P0
Canonical: `/blog/kalahari-round-rock-family-guide/`

**Evidence:** Long content is not automatically useful: it mixes unverified room/day-pass prices, admission timing, attraction lists, “insider” testimony, precise transfer times, free preinstalled child seats, free snack stops and a $25 discount. The generic opening reads “Kalahari Round Rock — The Complete Transportation Planning.”

**Recommend:** Replace the awkward generic introduction and unsupported first-hand claims. Retain a family transportation focus: day pass versus overnight stay, resort entry/address verification, bags and wet clothing, stroller/restraint needs, scheduled return and off-site meal transport. Send admission, check-in, attraction and dining questions to current official resort pages. Do not publish the discount or free-equipment offer without business confirmation and terms.

**Distinct value:** An airport-to-resort and return-day packing/loading plan, not a speculative resort price guide.

**Editing source:** `scripts/generate_partner_blogs.py` and the generated page.

### 7. DFW airport — P0
Canonical: `/blog/dfw-airport-limo-guide.html`

**Evidence:** Useful source-verification section already exists. Earlier content still guarantees automatic pickup changes, “no extra charge,” driver photo delivery and on-time presence, and hardcodes terminal/curb instructions. A paragraph calls the public side “post-security” while referring to Skylink, contradicting the preceding inside-security description. Short departure recommendations may not fit airline requirements.

**Recommend:** Preserve the existing official-resource section and make it control the whole article, not just an addendum. Replace authoritative curb/airline tables with current airport directions and reservation-specific instructions. Separate flight cancellation, delayed landing and post-landing baggage delays. Clarify landside versus airside transfers after checking DFW guidance. Replace fixed leave-home timing with the airline-required arrival time plus ground travel and contingency.

**Distinct value:** DFW arrival coordination, including terminal changes and baggage/customs communication. Do not create another generic airport sales page.

**Editing source:** Update `scripts/data/03-dfw-airport-limo-service-guide.json`, applicable `scripts/blog_addenda.py` text and the rendered page together. `scripts/seo_normalize.py` also maps a legacy DFW guide URL to this canonical `.html` destination. Preserve that destination when regenerating.

### 8. Universal Kids Resort — P2
Canonical: `/blog/universal-kids-resort-frisco-family-guide/`

**Evidence:** Already has useful bag/restraint guidance, separates hotel and park addresses, avoids a permanent ticket-price table, and offers rental-car tradeoffs. It asserts a July 1, 2026 opening, exact addresses, hotel details and seven lands as official facts.

**Recommend:** No broad rewrite. Revalidate those assertions against the resort's current official pages and retain source links. The September update stamp is not evidence by itself. Keep conditional schedules and practical family guidance. Add only a concise return-to-airport checklist if approved.

**Distinct value:** Airport/hotel/park coordination for families; no need to pad it with generic limo benefits.

**Editing source:** `scripts/generate_partner_blogs.py` and the generated page.

### 9. Round Rock to AUS — P0
Canonical: `/blog/round-rock-to-austin-airport-limo-transfers/`

**Evidence:** Describes one-way prices as covering “the 30-mile drive each way”; promises a fixed $165 sedan and included meet-and-greet, “40 minutes flat,” guaranteed pickup and specific corporate customers. A 40–50 minute trip can cross the current estimator's hourly-pricing threshold, so the table cannot be inferred from the shared base rates.

**Recommend:** Keep this as a route-specific guide. Replace unsupported fixed fares with an exact-address estimate and representative confirmation. Contrast route options without promising SH 130 is always fastest or tolls always included. Separate outbound flight timing from return-flight readiness. Remove customer names unless authorized.

**Distinct value:** A Round Rock departure worksheet that accounts for origin, airline arrival requirement, bags, route estimate and traffic allowance. Avoid repeating the AUS curb guide.

### 10. Austin/Hill Country wedding — P0
Canonical: `/blog/austin-wedding-limo-hill-country-venue-guide/`

**Evidence:** Claims “8,000 weddings,” “hundreds…served,” unsupported package/discount/amenity policies, rigid sellout windows and unconditional venue coverage. Mercury Hall appears under multiple locations; other venue placements need address checks. A promise of two or three shuttle loops ignores actual round-trip duration.

**Recommend:** Replace the venue directory with verified addresses and access questions: gate code, vehicle size limits, turnaround, loading area and last departure. Build shuttle capacity from seats × feasible loops, with loading and round-trip time included. Confirm decorations, champagne and standby rather than treat them as standard. Use current wedding terms and remove invented experience figures.

**Distinct value:** Rural venue access and realistic return-loop planning, separate from Dallas's coordinator checklist.

### 11. Austin hiring FAQ — P0
Canonical: `/blog/frequently-asked-questions-about-hiring-a-limo-service-in-austin/`

**Evidence:** Says sedans take four passengers; current booking configuration says three. Says gratuity is included, promotes standing/moving around in a Sprinter Party Bus, makes broad screening claims and gives confident availability advice.

**Recommend:** Correct the capacity mismatch when publishing; say people and bags must both fit. Remove language inviting passengers to move around while traveling. Replace the gratuity answer with confirmation of the quote's inclusions pending policy clarification. Keep only questions not fully answered in the booking walkthrough: requested changes, quote confirmation, luggage fit, restraints and cancellation terms. Link the policy instead of inventing refund rules.

**Distinct value:** Short answers resolving uncertainty, not a second “how to book” article.

### 12. SXSW — P0
Canonical: `/blog/sxsw-limo-service-austin-transportation-guide/`

**Evidence:** October review finds forward-looking “SXSW 2026” booking advice and a January deadline already past. The route plan assumes Austin Convention Center panels; current venue use must be verified. Unsupported 4–7× surge figures, guaranteed January availability, exact closure workarounds and branded-wrap service. Compares a whole-group rideshare total with a per-person chauffeur amount.

**Recommend:** Use an evergreen planning guide at the same URL; add a dated next-edition section only after official dates, venues and access information are verified. Compare complete group totals on both sides, including booked time and constraints. Explain when walking between nearby venues is simpler than retaining a vehicle. Confirm major-event payment/cancellation terms and authorized meeting points.

**Distinct value:** A venue-cluster schedule with vehicle legs, walking legs, fixed appointments and a contact plan. Do not merely replace “2026” with “2027.”

### 13. Austin mapping — P1
Canonical: `/blog/how-dynamic-maps-enhance-limousine-services-in-austin/`

**Evidence:** Repeats the traffic and general mapping articles; claims continuous corridor monitoring and specific rerouting before an incident without evidence.

**Recommend:** Retain the URL but narrow content to how an Austin traveler communicates road-closure or venue-entrance changes. Explain that a map pin may not be a legal loading point and that traffic estimates cannot guarantee arrival. Describe actual passenger actions, not an unverified dispatch system.

**Distinct value:** An Austin event pickup-change checklist. Do not consolidate with a redirect without a separately approved URL strategy.

### 14. F1/COTA — P0
Canonical: `/blog/f1-cota-limo-service-austin-grand-prix-transportation/`

**Evidence:** Guarantees VIP-lot waiting, a $250 pass, Paddock access, “5 minutes” to the car and “35 minutes” back downtown. Package arithmetic is inconsistent: six hours at $119 is $714, not $715; other totals are similarly rounded without explanation. Claims guaranteed August availability and NDA-eligible chauffeurs.

**Recommend:** Remove access and travel-time guarantees. The event organizer controls credentials, commercial vehicle permissions, holding areas and loading. Confirm pass type and vehicle eligibility for the exact event before offering a meeting point. Replace static package totals with an itemized quote and contingency/return plan. Use verified current-event dates; no automatic annual rollover.

**Distinct value:** A credential/access checklist and post-race regrouping plan. Include parking/holding costs, overtime authorization, a backup contact and a safe fallback meeting process; no secret traffic bypass.

### 15. Plano/Frisco — P2
Canonical: `/blog/plano-frisco-guide`

**Evidence:** Mostly an attraction list; Dr Pepper Ballpark and Riders Field appear separately without clarifying whether they are one renamed venue. “Top 10 malls…by sales,” corporate-customer claims and a $89 airport fare have no evidence supplied.

**Recommend:** Check venue names, addresses and whether listings duplicate one another. Organize by purpose—Legacy West meeting/dinner, Frisco event, airport connection—with exact destination entrance, passenger/luggage and return requirements. Remove the unsupported ranking, customer relationship and fare.

**Distinct value:** An airport + business visit + evening event itinerary worksheet, not another metro-wide directory.

### 16. Austin corporate — P1
Canonical: `/blog/why-choose-purple-heart-for-your-corporate-transportation-needs-in-austin/`

**Evidence:** Predominantly promotional claims about operational discipline, confidentiality, preferred rates and consistent vehicle assignment. “They walk out, the car is there” promises an immediate airport pickup.

**Recommend:** Replace claims of superior performance with an organizer handoff checklist: traveler versus booker contacts, flight/date, office entrance, itinerary changes, invoicing questions and approval contact. Present accounts, privacy requirements and same-driver assignments as items to confirm, not guaranteed benefits.

**Distinct value:** A travel coordinator's briefing form for one or several travelers. Do not claim famous local employers are customers.

### 17. Austin weekend — P1
Canonical: `/blog/things-to-do-in-austin-texas-weekend-guide/`

**Evidence:** Overlaps night-out/top-five pages. Contains check-worthy “Free on Thursdays” museum advice, business names, venue geography and firm Hill Country travel times.

**Recommend:** Keep the weekend structure but offer a choice of one compact area at a time rather than a densely packed universal itinerary. Verify museum hours/admission and named stops directly. Include weather alternative, walking tolerance, hotel downtime, baggage storage arrangements and optional next-day trip. Do not imply a chauffeured car is necessary for every short leg.

**Distinct value:** A two-day planning framework with selectable activities. Send late-night detail to the night-out page and destination comparison to top-five.

### 18. General mapping — P1
Canonical: `/blog/how-dynamic-map-integration-enhances-your-limo-experience/`

**Evidence:** Repeats the Austin mapping narrative while claiming automatic incident avoidance, precise exit prediction and “on time, every time.” No operational evidence establishes that system.

**Recommend:** Reframe at the same URL as a plain-language guide to map estimates and accurate pickup information. Explain address versus entrance, pin versus authorized curb, estimated drive time versus actual traffic, and why a passenger should report a changed terminal or delayed bags. Do not expose internal implementation details as a substitute for useful advice.

**Distinct value:** A location-information checklist across markets. The Austin map article should handle local event changes, not repeat this explanation.

### 19. Five Austin destinations — P1
Canonical: `/blog/top-5-destinations-to-visit-with-a-limo-in-austin/`

**Evidence:** Overlaps the night-out and weekend guides; includes multiple venue names needing current checks, “zero convenient parking,” guaranteed text-anywhere pickup and a claim that personal-vehicle transportation at COTA is effectively unusable.

**Recommend:** Keep five broad destination types but replace superlatives with a decision table: group size, number of stops, return-time certainty, baggage, walking segment and when a car is not necessary. Validate named businesses before recommending them.

**Distinct value:** Help readers choose an outing and transfer versus hourly service—not duplicate a full weekend itinerary.

### 20. Booking walkthrough — P1
Canonical: `/blog/the-ultimate-guide-to-booking-a-limo-service-in-austin/`

**Evidence:** The supplied legacy booking slug resolves here. The page promises responses and written confirmation within one hour, exact vehicle assignment and all-inclusive terms. Current booking UI explicitly distinguishes a received request from confirmation by a representative.

**Recommend:** Match the actual journey: collect trip details → request estimate → review details with representative → confirm terms/availability → receive final instructions. Keep the useful quote-comparison questions, add bags/restraints/accessibility, and remove unsupported service-level promises.

**Distinct value:** A realistic booking walkthrough. Use the FAQ for exception questions rather than repeat it.

## Proposed original planning content

These are review drafts, not newly published company policies, customer stories or descriptions of rides actually performed.

### Draft A — quote request versus confirmed reservation

> Submit your pickup and destination addresses, travel date, passenger count and luggage details to request a quote. The website's estimate is not a confirmed reservation. A representative will review the route, vehicle availability, price and any special requirements with you. Before relying on the booking, confirm the pickup time, meeting instructions, included waiting time, change/cancellation terms and how to contact the team on the day.

**Best home:** booking walkthrough. The FAQ should link to it rather than reproduce it in full.

### Draft B — evening worksheet

| Fill in before requesting a quote | Why it changes the plan |
|---|---|
| Dinner address, reservation time and expected finish | A reservation time is an arrival deadline, not a pickup time. |
| Show address, doors/start time and likely finish | Allow for entry and regrouping; a show may finish later than scheduled. |
| Passengers, equipment and walking/accessibility needs | Seat count alone does not establish fit or a suitable pickup point. |
| Separate transfers or reserved hourly service | Confirm whether the vehicle stays available between stops. |
| Final departure and any overtime approval | An hourly rate does not mean unlimited hours. |
| Primary group contact and backup contact | Changes should reach one person who can account for the whole group. |
| Agreed pickup location and fallback instructions | Venue restrictions may prevent a vehicle from stopping at the door. |

**Best home:** Austin night-out article. No fabricated itinerary duration or venue endorsement is required.

### Draft C — work backward from a flight

> Start with your airline's recommended airport arrival time for your flight and circumstances. Add the current drive estimate from your exact pickup address, time to load your party and bags, and a separate allowance for traffic or weather. Do not use the flight's departure time as your airport-arrival target. Confirm the proposed pickup time with your transportation provider. For the return journey, share the operating flight number and tell the team if baggage, customs or your terminal changes affect where or when you can meet.

**Best home:** Round Rock–AUS guide, with short links from the airport guides. No fixed journey time or universal buffer is presented as guaranteed.

### Draft D — wedding shuttle feasibility

> List each passenger movement separately: getting-ready location to ceremony, ceremony to reception, early guest return and final departure. For each leg, record the number of people, confirmed usable seats, loading time and route time. A vehicle can make another loop only after completing its outbound trip, unloading, return drive and next loading period. Ask the coordinator and transport provider to agree the schedule before assuming one vehicle can carry everyone. Include venue access instructions and a decision-maker who can authorize changes.

**Best home:** Hill Country wedding guide; adapt the Dallas page to coordinator handoff rather than duplicate all of this text.

## Coverage of every supplied example

Rows refer to URL occurrence order in the supplied file, not crawl-date order.

| Input rows | Destination / disposition |
|---|---|
| 1, 25, 26 | Article 1: Austin night out; host/slash variants deduplicated. |
| 2 | Article 2: Austin traffic. |
| 3 | Article 3: Dallas wedding. |
| 4 | Article 4: Near Southside. |
| 5 | `/austin-limo-rental/` — service landing page, not an article; no rewrite in this review. |
| 6 | Article 5: AUS airport. |
| 7 | Article 6: Kalahari. |
| 8 | Article 7: DFW airport; preserve canonical `.html`. |
| 9 | Article 8: Universal Kids Resort. |
| 10 | Article 9: Round Rock–AUS. |
| 11 | Article 10: Hill Country wedding. |
| 12 | Article 11: Austin FAQ. |
| 13 | `/cancellation-policy.html` — policy page; used as business-policy evidence, not rewritten. |
| 14 | Article 12: SXSW. |
| 15 | `/flight-tracker.html` — utility, not an article; no rewrite. |
| 16 | Article 13: Austin mapping. |
| 17 | Article 14: COTA. |
| 18 | `/austin-wedding-limo/` — service landing page; no rewrite. |
| 19 | Article 15: Plano/Frisco; `.html` alias resolves to extensionless canonical. |
| 20 | `/es/booking.html` — transaction page; no rewrite. |
| 21, 37 | Retired prom-night article → `/blog/`; separate retirement work. |
| 22 | Article 16: corporate. |
| 23, 27 | Article 17: weekend; host variant deduplicated. |
| 24 | Article 18: general mapping. |
| 28 | Article 19: top-five destinations. |
| 29, 30 | Retired prom-season article → `/blog/`; separate retirement work. |
| 31 | Retired “why…stands out” article → `/blog/`; separate retirement work. |
| 32, 35, 36 | Legacy blog query/pagination variants → `/blog/`; index, not article content. |
| 33 | Article 20: legacy booking slug → existing ultimate-booking guide. |
| 34 | `/our-services` → `/services.html`; service page, not article content. |
| 38 | Retired “why Austin locals love…” → `/blog/`; separate retirement work. |
| 39, 40 | Retired prom “case study” → `/blog/`; separate retirement work. Do not reuse anecdotal claims as evidence. |

Resolution was checked using the current `_load_redirects` and `_redirect_destination` functions from `server.py` with `netlify.toml`, including trailing-slash and pagination handling. Active article canonical tags were then checked against the resolved files. This does not claim that an unmerged workspace state is already deployed.

## Approval and implementation checklist

Before substantial rewriting:

1. Approve the distinct purpose and proposed structure for each priority article.
2. Obtain business confirmation of waiting policy, gratuity, meeting options, special equipment, promotions, specialty capacity, event access commitments and service-level claims. Mark unresolved facts **omit/confirm at quote**, not “probably true.”
3. Check volatile external facts against the source that controls them: airport ground-transportation information, event organizer access plans, venue address/operations pages, and official resort admissions/calendar. Record source URL, checked date and supported claim.
4. Verify author/reviewer identity before adding any experience or expertise attribution. Do not invent a driver byline, customer story or first-hand inspection.

For an approved publication pass:

- Preserve every canonical URL in this report. Do not change redirects, retire pages or add duplicate articles.
- Edit generator sources as well as generated HTML where applicable; avoid running a whole-site generator merely to change one article.
- Update visible answers and matching FAQ/Article structured data together. Remove the old contradictory sentences rather than leave a correction appended underneath.
- Keep live price bindings, metadata and no-JS fallbacks consistent. Prefer a quote explanation to unsupported permanent route prices.
- Use relevant existing cross-links, not repeated keyword anchors or a new discovery-link campaign.
- Keep revisions useful at any length; do not pursue a word-count target. Update dates only for real, verified editorial changes.
- Check the exact changed pages, schema/visible-answer consistency and canonical preservation before merging.

After publication, record the actual release date and monitor the canonical URLs in Search Console after recrawling. Compare indexing state, Google-selected canonical and relevant impressions/clicks with the baseline, allowing for demand and crawl timing. Do not invent a numeric improvement target or promise that recrawling will result in indexing.

---
name: Booking pricing rules
description: Canonical live-pricing rules and vehicle class contract shared by homepage widget and booking page
---
Ride classes (canonical source: `js/pricing.js` PHL_CLASSES) — order: Luxury SUV (default), Business SUV, Luxury Sedan, Business Sedan. Caps: SUVs 6 pax/5 bags, sedans 3 pax/2 bags. booking.html VEHICLES must stay hard-synced (names, order, caps, rates) — no shared import there yet, so drift is the main risk.

Fare rules (both pages): flat first 20 mi — Business Sedan $120 / Luxury Sedan $190 / Business SUV $150 / Luxury SUV $190; +$2 per mile over 20 (partial miles rounded UP); trips >40 min switch to hourly: hours = max(2, ceil(minutes/60)) × hourly rates 119/229/149/179. Larger vehicles (stretch/sprinter/party bus) have NO live pricing.

**Why:** owner-specified pricing spec (July 2026 rework); success messages show the estimated fare, so both pages must compute identically.

Distance backend: /api/distance (server.py dev, netlify/functions/distance.js prod) tries Google Routes API first, then falls back to Nominatim geocode + public OSRM routing. **Google Routes AND all legacy Maps APIs are DISABLED on the owner's Google project (403/REQUEST_DENIED)** — the OSRM fallback is what actually serves until the owner enables Routes API. Interior/trunk vehicle photos are Unsplash placeholders flagged `photoPlaceholder` — owner to swap with real photos.

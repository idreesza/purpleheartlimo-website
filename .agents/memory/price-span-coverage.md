---
name: Live price copy rules
description: Rules for quoting live class prices in page copy (span semantics, what stays static)
---
Any copy quoting a live-priced class must use a `data-phl-*` span (page loads /js/pricing.js then /js/price-sync.js); never hardcode those dollar amounts.

**Why:** rates change only in js/pricing.js; hardcoded amounts go stale silently — that's how the site drifted before.

**How to apply:**
- Semantics matter: `data-phl-flat` for "flat-rate transfer" claims, `data-phl-hourly` for "/hr", `data-phl-from` ONLY for "from $X" marketing (it renders min(flat,hourly), e.g. 119 vs flat 120 — pairing it with "flat-rate" wording misquotes the price; a completion review rejected exactly this).
- Static span text = current value (no-JS fallback) — keep it matching pricing.js.
- Leave static: industry-range comparisons, competitor/rideshare prices, non-live classes (stretch, Sprinter, party bus, coach), route-specific flats.
- Homepage myths copy is duplicated in the blog 5-myths post — edit both.
- Derived math examples ("6-hr day $715") don't sync; reword or treat as approximate.

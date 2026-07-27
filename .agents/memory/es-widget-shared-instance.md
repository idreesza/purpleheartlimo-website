---
name: Shared booking widget across EN/ES homepages
description: How the single #booking-widget serves both the English and Spanish SPA homepages
---
There is exactly ONE `#booking-widget` (IDs inside are singletons: pickup-input, bk-bar, price-estimate…). The Spanish homepage (`#es-home-page`, shown via `showPage('es-home')`) does NOT have its own copy — `bkRelocate(pageId)` moves the widget DOM node into `#es-bk-mount` / back into `#home-page .hero-inner`, then `bkSetLang('es'|'en')` swaps every visible string.

**Why:** duplicating the widget would break all `getElementById`-driven logic (pricing, tabs, layout zones) and double maintenance.

**How to apply:**
- Never add a second booking form to es-home; extend `BK_L10N` + `bkSetLang` instead.
- Language gate is `document.documentElement[data-lang]` (`bkEs()` helper); dynamic JS strings (bkApplyLayout buttons, refreshLivePricing, addQuoteStop, submitQuote, renderVehicleDisplay, focusFleetPhoto) branch on it — new user-visible strings in widget JS must too.
- `pricing.js` breakdown strings stay English (shared with booking.html); they are translated display-side in `refreshLivePricing` via `.replace()`.
- Luggage csel options' onclick display arg is rewritten per language by `bkSetLang`.

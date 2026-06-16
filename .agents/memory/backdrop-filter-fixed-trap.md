---
name: backdrop-filter traps position:fixed
description: Why home-hero bar dropdowns/overlays must be appended to <body>, not positioned in place.
---

The home hero booking bar (`#home-page .bk-bar`) and several hero panels use
`backdrop-filter: blur(...)`. Any element with backdrop-filter (also transform,
filter, perspective, will-change) becomes the **containing block for
position:fixed descendants**. So a dropdown/popover that lives inside the bar and
uses `position:fixed` resolves its top/left against the BAR, not the viewport —
it renders off-screen / clipped, not where you computed.

**Rule:** for any overlay anchored to a bar/input inside a backdrop-filtered
ancestor (csel time dropdowns, nominatim autocomplete list, custom date picker),
append the overlay to `document.body` and fixed-position it from the anchor's
getBoundingClientRect(). The csel engine tracks the home wrap via
`data-owner` and moves the list back on close (cselCloseAll).

**Also:** when measuring `offsetWidth` of a just-appended list, set
`position:fixed` + an explicit width FIRST. The base `.csel-list` CSS has
`left:0;right:0`, so an absolutely-positioned freshly-appended list stretches to
full body width and your right-edge clamp math goes negative.

**Also:** `bkApplyLayout()` must call `cselCloseAll()` before reshuffling fields,
so switching tabs while a dropdown is open returns the body-detached list to its
wrap instead of orphaning it.

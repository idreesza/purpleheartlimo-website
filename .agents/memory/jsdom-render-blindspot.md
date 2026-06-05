---
name: jsdom render blindspot vs unclosed-div in display:none pool
description: why a structurally "passing" jsdom test can still hide a real browser layout bug
---

When fields are stored in a hidden pool (`<div style="display:none">`) and JS moves them into
visible step containers, a single missing `</div>` in the pool can make the browser parse the
following SIBLINGS (the step containers, fleet strip, etc.) as DESCENDANTS of the hidden pool —
so they inherit `display:none` and never render, even though every element exists and has the
right children/IDs.

**Why:** jsdom (parse5) parses the same as the browser, but a test that only asserts
`getElementById(...)` + `children.length` NEVER inspects `parentElement` or computed layout.
Such a test passes while the real page shows nothing. `getComputedStyle(el).display` on the
element itself is ALSO misleading: it returns the element's own `display` value (e.g. `block`)
even when an ancestor is `display:none`.

**How to apply:**
- The decisive in-browser probe is `el.offsetHeight === 0` while the element's own
  `display` is block → an ANCESTOR is hidden. Then check `el.parentElement.id` and
  `getComputedStyle(ancestor).display`.
- When console logs don't surface and no headless Chromium is available, write probe results
  into a VISIBLE on-page element (e.g. the card subtitle) and read them via app_preview
  screenshot. Remove the probe afterward.
- Validate moved-node layouts by checking the parent chain / `offsetHeight`, not just ID lookup.
- Verify div balance per region: `awk 'NR>=A&&NR<=B' file | grep -o '<div\|</div>' | sort | uniq -c`.

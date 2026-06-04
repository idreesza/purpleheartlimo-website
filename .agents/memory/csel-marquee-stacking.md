---
name: csel dropdown vs mask-image marquee stacking
description: Why the time-picker dropdown hid behind the fleet car strip, and the fix.
---

The booking-card time-picker uses a custom-select ("csel") engine. Its open list is
`.csel-list { position:absolute; z-index:99999 }`. The sliding fleet car strip below
it (`.fleet-marquee`) uses `mask-image`, which **creates its own stacking context**.

**Symptom:** dropdown options were painted BEHIND the car strip (middle options hidden)
even though z-index was 99999.

**Why:** z-index:99999 was trapped inside the `.csel` wrapper context; the wrapper
itself competed with the marquee at the auto/0 level and lost because the marquee
comes later in DOM order.

**Fix:** elevate the wrapper, not just the list: `.csel.open, .csel:has(.csel-list.open){ z-index:1000 }`.
The `.open` class is toggled on the `.csel` wrapper in JS across ALL paths
(cselToggle open + close-all loop, cselPick, outside-click handler) — every close
path must clear `.open` on the wrapper or a stale elevated z-index lingers.

**How to apply:** any time a positioned overlay must sit above a sibling that uses
mask-image / filter / transform / opacity, elevate the overlay's positioned ANCESTOR,
not just the overlay itself.

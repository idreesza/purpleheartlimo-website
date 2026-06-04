---
name: time-picker dropdown hidden behind fleet car strip
description: Why the booking-form dropdowns hid behind the sliding car marquee, and the real fix.
---

The booking-card (home hero) multi-step form: `.bk-step`, `.bk-step`, `.bk-step` and
`.fleet-marquee` (sliding car strip) are all DIRECT SIBLINGS inside `.booking-card`
(which is the stacking-context root via `backdrop-filter`).

**Symptom:** the Step-2 time-picker custom-select ("csel") dropdown was painted BEHIND
the car strip — middle options hidden by the cars — even with `.csel-list{z-index:99999}`.

**Real root cause:** `.bk-step.active` runs `animation: bkStepIn .35s ease both`. The
`fill: both` (and the animated `transform`/`opacity`) makes the active step retain a
STACKING CONTEXT in practice, which TRAPS the csel's z-index inside the step. The
marquee uses `mask-image` (its own stacking context) and comes LATER in DOM at the same
auto level, so it paints over the trapped dropdown. Elevating only `.csel` did NOT work
because the csel's z-index can't escape the bk-step context.

**Fix that works:** lift the whole step context above the marquee, don't fight inside it:
  `.booking-card .bk-step { position:relative; z-index:2; }`
  `.booking-card .fleet-marquee { position:relative; z-index:1; }`
Kept `.csel.open{z-index:1000}` for ordering csels among sibling fields (harmless).

**How to apply:** when an overflowing overlay (dropdown/popover) hides behind a sibling
that has mask/transform/filter, the overlay's own z-index is useless if an ancestor
(here an animated step with fill:both) forms a trapping stacking context. Elevate that
ANCESTOR above the competing sibling instead.

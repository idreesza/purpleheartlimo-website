---
name: Fleet marquee ride-type focus
description: How the sliding fleet strip stops/magnifies the picked Ride Type car, and the centering gotcha behind it.
---

# Fleet marquee "focus on picked car"

When a Ride Type is picked (Step 3, `#csel-vehicle` → `onVehicleChange`), the sliding
fleet strip stops, centers the matching car, magnifies it with a gold "selected" frame,
dims the others, and shows a `#fleet-caption` badge. Driven by `focusFleetPhoto()` +
`VEHICLE_PHOTO` map (one ride type → one image filename substring).

## Centering gotcha (the durable lesson)
Centering uses `getBoundingClientRect` deltas to translate the track. **Any
layout-affecting property that is *animated* on the selected image (e.g. `margin`)
will shift the car AFTER the delta is computed, leaving it off-center.**

**Rule:** apply layout-affecting spacing (margin) *instantly* (keep it OUT of the
`transition` list); only transition non-layout properties (transform/scale, opacity,
filter, box-shadow, border-color). Then a single rAF measurement reflects final layout.
A delayed corrective `recenter()` pass (~760ms) guards against late reflow from
lazy-loaded marquee images.

**Why:** `transform: scale()` does NOT affect the layout box, so center stays stable
under scale — but `margin` does, so animating it breaks the math.

## Clipping note
Magnified car is `scale(1.7)` on 56px images inside `overflow:hidden` + mask. Focus
mode adds vertical padding (`.car-focus` padding-top/bottom) so the scaled image paints
into the padding area (clip is at the padding box) instead of being cut off.

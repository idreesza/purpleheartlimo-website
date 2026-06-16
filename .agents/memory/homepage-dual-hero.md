---
name: Homepage scoping rules
description: Why home-only visual changes must be scoped to #home-page, not .hero or bare button classes.
---

# Home-only styling must be scoped to `#home-page`

`index.html` is a single-file multi-"page" app. The homepage is `#home-page`; there
is also a Spanish home `#es-home-page`, plus many service pages (`#airport-page`, etc.).

**Rule:** Any styling intended for *only* the English homepage must be scoped to
`#home-page ...`. Do NOT rely on `.hero` or bare button classes.

**Why:**
- `.hero` is shared by BOTH `#home-page` and `#es-home-page`. Editing `.hero` (background,
  smoke, column layout, h1 font) changes the Spanish home too.
- `.btn-primary` / `.btn-secondary` / `.btn-white` are global across every service page,
  so unscoped button restyles leak everywhere.

**How to apply:**
- Home redesign (Portfolite dark-minimal look) lives under `#home-page` selectors, often
  with `!important` to beat earlier inline/`.hero` rules. Hero motion (glow-pulse buttons,
  scroll indicator, services marquee) is intentionally home-only.
- The services marquee shows the *services we provide* (not brand logos) — a deliberate
  repurpose of Portfolite's logo marquee.
- The booking form contract (field IDs, `submitQuote()`) is independent of styling — never
  let a visual edit touch those IDs.

## Home hero backdrop lives on pseudo-elements, not `.hero`
The home hero's backdrop is painted by `.hero::before` / `.hero::after`
(with `mix-blend-mode:screen` + a drift animation), NOT by `.hero { background }`.
Setting a background image on `.hero` alone shows nothing — the blended
pseudo-element layer covers it.
**Why:** screen-blend on the pseudo-elements washes out anything set on `.hero`.
**How to apply:** to change the home backdrop, override `#home-page .hero::before`
(new image + `mix-blend-mode:normal; animation:none; opacity:1`, and reset its
`top/left/width/height` to `0 / 0 / 100% / 100%`) and hide `::after`.

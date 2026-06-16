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

## Swapping the home hero background — neutralize the smoke layers
`.hero::before` and `.hero::after` (base rule) paint `hero-smoke.webp` with
`mix-blend-mode:screen` + drift animations, positioned `top:-25%;left:-25%;150%`.
When replacing the home background image you MUST override `#home-page .hero::before`
(set the new image, `mix-blend-mode:normal; opacity:1; animation:none; top:0;left:0;100%`)
AND `#home-page .hero::after{display:none}` — otherwise the smoke screen-blend washes
out any photo you set on `.hero`. The purple-Escalade direction (images/hero-escalade.webp)
supersedes the old monochrome smoke hero.
**Why:** the smoke is on pseudo-elements, not the `.hero` background, so changing
`.hero{background}` alone does nothing visible.

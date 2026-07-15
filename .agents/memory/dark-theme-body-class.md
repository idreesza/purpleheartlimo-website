---
name: Site theme is class-gated, not stylesheet-gated
description: How the light/dark treatments are toggled across the static site and where purple can hide.
---

# Theme is gated by body classes, and purple hides in many layers

The site was converted to a LIGHT gold/cream theme (July 2026). Dark/purple styling was
never one stylesheet — it lived in several independent layers:

- Standalone pages (about/contact/fleet/flight-tracker/gallery/services/testimonials)
  were dark only via `body.dark-theme` rules in `css/global.css`. Removing the class from
  `<body>` flips a page light; the dark-theme block is now inert but still present.
- `css/header.css` (`body.hdr-v2`) styles the shared inner-page header; index.html has its
  own duplicate inline header rules. Both must change together or nav pills mismatch.
- Purple constants to grep when hunting remnants: `7C3AED 5B21B6 8B4DF2 6926C9 3d0060
  534ab7 a89fd4 83,74,183 138,43,226 12121f f5f0ff` — including a JS hover fallback in
  index.html's custom select code.

**Why:** "remove the purple theme" required edits in 4 CSS layers + inline JS; a single
stylesheet pass misses live purple in hover states and dropdown panels.
**How to apply:** for any future theme shift, grep the constants above across index.html
AND css/*.css, and check body class gates (`dark-theme`, `hdr-v2`, `home-active`) before
editing selectors.

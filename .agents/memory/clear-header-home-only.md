---
name: Clear (transparent) header is home-only
description: The navbar is a single global element shared by all pages; the transparent "clear" treatment must be gated to home pages only.
---

# Clear/transparent header is scoped to home pages

The `<nav class="navbar">` on the index.html SPA is ONE global element shared by
every JS-toggled page (including the light interior pages: fleet/about/Spanish).

The transparent treatment is gated with `body.home-active`, toggled in
`showPage()` (for `home` and `es-home`) and set on `DOMContentLoaded` (home is the
default page). When scrolled, the bar becomes a dark glass via `.navbar.scrolled`.

**Why:** Making the navbar transparent globally would put dark logo/link text over
the dark hero (invisible) AND would break the white interior pages. The hero is
dark (`#0f0f0f → #1a0533`), so nav text/logo/links are forced white only while
`home-active`.

**How to apply:** Any new dark full-bleed page that should use the clear header must
be added to the `clearPages` array in `showPage()`; never make `.navbar` transparent
unconditionally. Keep light-text overrides under `body.home-active .navbar ...`.

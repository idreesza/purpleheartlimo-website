---
name: Homepage has two .hero sections
description: index.html renders both an English and a Spanish home hero sharing the .hero class; any hero restyle hits both.
---

# Homepage has two `.hero` sections

`index.html` is a single-file multi-"page" app (divs `.page#home-page`,
`.page#es-home-page`, etc., toggled by a language/nav switcher). The home page
exists twice: the English hero inside `#home-page` and the Spanish hero inside
`#es-home-page`. Both use `<section class="hero">`, and they are the ONLY two
`.hero` elements in the file (service/blog/city pages do not use `.hero`).

**Why it matters:** Any rule scoped to `.hero ...` (or a global hero restyle)
applies to BOTH language versions of the home hero — and to nothing else. So a
"home hero only" change is naturally satisfied by `.hero` scoping without
leaking to other pages. Conversely, if you ever need English-only hero styling,
scope with `#home-page .hero`; the Spanish twin then needs its own treatment or
it will look inconsistent.

**How to apply:** When restyling the home hero, edit shared `.hero` CSS and
duplicate any hero-markup-level changes (overlay divs, inline color attrs) into
BOTH `<section class="hero">` blocks so the two language heroes stay consistent.
